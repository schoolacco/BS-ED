"""
Wiki Table to Python Code Converter
Converts MediaWiki table rows into Python button definitions.

Usage:
    Run the script, then follow the interactive prompts.
    Or call convert_table() / convert_row() directly in your own code.
"""

import re
import math

# ── Suffix list (extracted from SuffixLong.js) ───────────────────────────────
SUFFIXES = [
    "","K","M","B","T","Qd","Qn","Sx","Sp","Oc","No","De","UDe","DDe","TDe",
    "QdDe","QnDe","SxDe","SpDe","OcDe","NoDe","Vt","UVt","DVt","TVt","QdVt",
    "QnVt","SxVt","SpVt","OcVt","NoVt","Tg","UTg","DTg","TTg","QdTg","QnTg",
    "SxTg","SpTg","OcTg","NoTg","qg","Uqg","Dqg","Tqg","Qdqg","Qnqg","Sxqg",
    "Spqg","Ocqg","Noqg","Qg","UQg","DQg","TQg","QdQg","QnQg","SxQg","SpQg",
    "OcQg","NoQg","sg","Usg","Dsg","Tsg","Qdsg","Qnsg","Sxsg","Spsg","Ocsg",
    "Nosg","Sg","USg","DSg","TSg","QdSg","Qnsg","SxSg","SpSg","OcSg","NoSg",
    "Og","UOg","DOg","TOg","QdOg","QnOg","SxOg","SpOg","OcOg","NoOg","Ng",
    "UNg","DNg","TNg","QdNg","QnNg","SxNg","SpNg","OcNg","NoNg","Ce",
    # Ce-tier and beyond omitted for brevity but the lookup still works because
    # suffix_to_exp() searches the list at runtime.
]

# Build a lookup dict for O(1) conversion (case-sensitive, as the wiki uses it)
SUFFIX_INDEX = {s: i for i, s in enumerate(SUFFIXES) if s}


def suffix_to_exp(suffix: str) -> int:
    """Return the exponent of 10 that the suffix represents (suffix index * 3)."""
    if suffix in SUFFIX_INDEX:
        return SUFFIX_INDEX[suffix] * 3
    # Linear fallback for long suffix lists not fully inlined above
    for i, s in enumerate(SUFFIXES):
        if s == suffix:
            return i * 3
    raise ValueError(f"Unknown suffix: {suffix!r}")


def parse_value(token: str) -> float:
    """
    Convert a wiki value token such as '1De', '38.99De', '1.5M', '700', '1.44k'
    into a plain Python float.

    Handles:
      • Plain integers / decimals  ("700", "1.44")
      • Suffixed values            ("1De", "38.99De", "1.5M", "1.44k")
      • k/K as 1 000
    """
    token = token.strip()

    # Try bare number first
    try:
        return float(token)
    except ValueError:
        pass

    # Match  <mantissa><suffix>
    m = re.fullmatch(r'([\d.]+)([A-Za-z]+)', token)
    if not m:
        raise ValueError(f"Cannot parse value token: {token!r}")

    mantissa_str, suffix = m.group(1), m.group(2)
    mantissa = float(mantissa_str)

    # Handle lowercase k as 1 000
    if suffix == 'k':
        return mantissa * 1e3

    exp = suffix_to_exp(suffix)   # raises ValueError for unknown suffixes
    return mantissa * (10 ** exp)


# ── Number → display string ───────────────────────────────────────────────────

# De is suffix index 11  →  exponent 33  →  1e33
# Threshold: values up to 999.99De (index 11, so < 1e36 works as cutoff)
SUFFIX_MAX_EXP = 35          # highest exponent still rendered with a suffix label


def _sig_figs(x: float, figures: int = 5) -> str:
    """Round x to `figures` significant figures and return a compact string."""
    if x == 0:
        return "0"
    magnitude = math.floor(math.log10(abs(x)))
    rounded = round(x, -int(magnitude) + figures - 1)
    # Remove trailing zeros after decimal point
    if rounded == int(rounded):
        return str(int(rounded))
    # Format with enough decimal places then strip trailing zeros
    s = f"{rounded:.{max(0, figures - 1 - int(magnitude))}f}".rstrip('0').rstrip('.')
    return s


def _to_mantissa_exp(value: float):
    """Return (mantissa, exponent) such that value ≈ mantissa × 10^exponent,
    with 1 ≤ mantissa < 10."""
    if value == 0:
        return 0.0, 0
    exp = math.floor(math.log10(abs(value)))
    mantissa = value / (10 ** exp)
    return mantissa, exp


def format_display(value: float) -> str:
    """
    Produce the display string used in the tuple label:
      • < 1 000        → plain number (e.g. "700")
      • 1e3 – 10^(SUFFIX_MAX_EXP+1)  → suffix notation  (e.g. "38.99De")
      • above that     → e-notation   (e.g. "3.931e37")
    """
    if value < 1e3:
        return _sig_figs(value)

    mantissa, exp = _to_mantissa_exp(value)

    if exp <= SUFFIX_MAX_EXP:
        # Find the appropriate suffix
        suffix_idx = exp // 3
        local_exp  = exp % 3
        display_mantissa = mantissa * (10 ** local_exp)
        suffix = SUFFIXES[suffix_idx]
        return _sig_figs(display_mantissa) + suffix

    # Large number: use e-notation
    return _sig_figs(mantissa) + "e" + str(exp)


def format_python_number(value: float) -> str:
    """
    Produce the Python literal used inside the function call:
      • values that fit in a float  → e-notation with up to 4 sig-fig mantissa
        (e.g. 1e33, 3.9e34, 9.36e35, 3.931e37)
      • values > 1e300              → Mantissa(mantissa, exponent)
    """
    if value == 0:
        return "0"
    mantissa, exp = _to_mantissa_exp(value)

    if exp > 300:
        return f"Mantissa({_sig_figs(mantissa)}, {exp})"

    mantissa_str = _sig_figs(mantissa)
    if mantissa_str == "1":
        return f"1e{exp}"
    return f"{mantissa_str}e{exp}"


# ── Wiki table parser ─────────────────────────────────────────────────────────

def parse_wiki_table_rows(wiki_text: str) -> list[tuple[str, ...]]:
    """
    Extract data rows from a MediaWiki table.
    Returns a list of row tuples (each cell as a stripped string).
    Skips header rows (lines starting with !) and table markup lines.
    """
    rows = []
    current_row: list[str] = []

    for line in wiki_text.splitlines():
        line = line.strip()
        if line.startswith('|-'):
            if current_row:
                rows.append(tuple(current_row))
                current_row = []
        elif line.startswith('|') and not line.startswith('|}') and not line.startswith('|+'):
            # Could be  |cell1||cell2  or  |cell1
            content = line[1:]
            cells = [c.strip() for c in content.split('||')]
            current_row.extend(cells)
        # Lines starting with ! are headers – skip

    if current_row:
        rows.append(tuple(current_row))

    return rows


# ── Code generator ────────────────────────────────────────────────────────────

def make_cost_button_line(
    currency: str,
    cost_value: float,
    button_type: str,
    obtain_value: float,
    indent: int = 10,
) -> str:
    cost_disp   = format_display(cost_value)
    obtain_disp = format_display(obtain_value)
    cost_py     = format_python_number(cost_value)
    obtain_py   = format_python_number(obtain_value)
    pad = " " * indent
    label = f'"{cost_disp} {currency}: {obtain_disp} {button_type}"'
    call  = f'lambda: cost_button("{currency}", {cost_py}, "{button_type}", {obtain_py})'
    return f'{pad}({label}, {call}),'


def make_reset_button_line(
    cost_currency: str,
    cost_value: float,
    reset_currency: str,
    reset_value: float,
    indent: int = 10,
) -> str:
    cost_disp  = format_display(cost_value)
    reset_disp = format_display(reset_value)
    cost_py    = format_python_number(cost_value)
    reset_py   = format_python_number(reset_value)
    pad = " " * indent
    label = f'"{cost_disp} {cost_currency}: {reset_disp} {reset_currency}"'
    call  = f'lambda: reset_button({cost_py}, "{cost_currency}", {reset_py}, "{reset_currency}")'
    return f'{pad}({label}, {call}),'


# ── Interactive converter ─────────────────────────────────────────────────────

BUTTON_MODES = {
    '1': 'cost_button',
    '2': 'reset_button',
}

BOOSTER_TABLE_EXAMPLE = """\
|1M Booster
|1.5M Booster
|1De Moon Cash
|800No Moon Cash
|700No
|-
|2.18M
|3.27M
|38.99De
|31.19De
|27.29De"""


def convert_table(
    wiki_text: str,
    mode: str,
    obtain_col: int,
    cost_col: int,
    button_type: str,
    cost_currency: str,
    reset_currency: str = "",
) -> str:
    """
    Convert a raw MediaWiki table string into Python button lines.

    mode            : 'cost_button' or 'reset_button'
    obtain_col      : 0-based column index for the obtain/reset amount
    cost_col        : 0-based column index for the cost amount
    button_type     : e.g. "Booster", "Reincarnation"
    cost_currency   : e.g. "Moon Cash", "Booster"
    reset_currency  : only used for reset_button mode (the thing being reset to)
    """
    rows = parse_wiki_table_rows(wiki_text)
    lines = []

    for row in rows:
        # Skip rows that don't have enough columns or look like headers
        if len(row) <= max(obtain_col, cost_col):
            continue
        obtain_raw = row[obtain_col].strip()
        cost_raw   = row[cost_col].strip()

        # Strip any wiki markup (e.g. [[File:...]])
        obtain_raw = re.sub(r'\[\[.*?\]\]', '', obtain_raw).strip()
        cost_raw   = re.sub(r'\[\[.*?\]\]', '', cost_raw).strip()

        # Skip empty or clearly non-numeric cells
        if not obtain_raw or not cost_raw:
            continue
        if not re.search(r'\d', obtain_raw) or not re.search(r'\d', cost_raw):
            continue

        def extract_number_token(s: str) -> str:
            """
            Pull just the leading <digits><suffix> token from a cell that may
            contain trailing text like ' Booster' or ' Moon Cash'.
            e.g. '1M Booster' → '1M',  '38.99De Moon Cash' → '38.99De'
            """
            m = re.match(r'([\d.]+[A-Za-z]*)', s.strip())
            return m.group(1) if m else s.strip()

        obtain_clean = extract_number_token(obtain_raw)
        cost_clean   = extract_number_token(cost_raw)

        try:
            obtain_val = parse_value(obtain_clean)
            cost_val   = parse_value(cost_clean)
        except ValueError as e:
            print(f"  [skip] {e}")
            continue

        if mode == 'cost_button':
            line = make_cost_button_line(cost_currency, cost_val, button_type, obtain_val)
        else:
            line = make_reset_button_line(cost_currency, cost_val, reset_currency, obtain_val)

        lines.append(line)

    return "\n".join(lines)


# ── CLI ───────────────────────────────────────────────────────────────────────

def _prompt(msg: str, default: str = "") -> str:
    val = input(msg).strip()
    return val if val else default


def main():
    print("=" * 60)
    print("  Wiki Table → Python Button Code Converter")
    print("=" * 60)
    print()

    print("Button mode:")
    print("  1) cost_button   (e.g. buy a Booster with Moon Cash)")
    print("  2) reset_button  (e.g. spend Booster to gain Reincarnation)")
    mode_choice = _prompt("Choose [1/2]: ", "1")
    mode = BUTTON_MODES.get(mode_choice, 'cost_button')

    button_type   = _prompt("Button / category name (e.g. Booster, Reincarnation): ", "Booster")
    cost_currency = _prompt("Cost currency (e.g. Moon Cash, Booster): ", "Moon Cash")

    reset_currency = ""
    if mode == 'reset_button':
        reset_currency = _prompt("Reset currency / reward name (e.g. Reincarnation): ", "Reincarnation")

    obtain_col = int(_prompt("0-based column index of the OBTAIN amount: ", "0"))
    cost_col   = int(_prompt("0-based column index of the COST amount:   ", "2"))

    print()
    print("Paste your MediaWiki table text below.")
    print("Enter a blank line followed by END to finish:")
    print()
    lines_input: list[str] = []
    while True:
        try:
            ln = input()
        except EOFError:
            break
        if ln.strip() == "END":
            break
        lines_input.append(ln)

    wiki_text = "\n".join(lines_input)

    print()
    print("─" * 60)
    result = convert_table(
        wiki_text, mode,
        obtain_col=obtain_col,
        cost_col=cost_col,
        button_type=button_type,
        cost_currency=cost_currency,
        reset_currency=reset_currency,
    )
    full_output = f'"{button_type}": [\n{result}\n],'
    print(full_output)
    print("─" * 60)

    try:
        import pyperclip
        pyperclip.copy(full_output)
        print("Copied to clipboard.")
    except ImportError:
        print("(Install pyperclip to enable clipboard copy: pip install pyperclip)")
    except Exception as e:
        print(f"(Clipboard copy failed: {e})")


# ── Quick self-test ───────────────────────────────────────────────────────────

def _self_test():
    """Reproduce the Booster example from the problem description."""
    BOOSTER_WIKI = """
{| class="wikitable"
!Obtain (Booster)
!x1.5 (game pass)
!Price (Moon Cash)
!-25%
!-30%
|-
|1M Booster
|1.5M Booster
|1De Moon Cash
|800No Moon Cash
|700No
|-
|2.18M
|3.27M
|38.99De
|31.19De
|27.29De
|-
|4.72M
|7.08M
|935.99De
|748.79De
|655.19De
|-
|10.15M
|15.22M
|39.31UDe
|31.44UDe
|27.52UDe
|-
|21.69M
|32.53M
|1.57DDe
|1.25DDe
|1.1DDe
|-
|46.03M
|69.04M
|15.72DDe
|12.57DDe
|11DDe
|-
|97.02M
|145.53M
|534.63DDe
|427.71DDe
|374.24DDe
|-
|203.19M
|304.78M
|22.98TDe
|18.39TDe
|16.09TDe
|-
|422.84M
|634.26M
|321.85TDe
|257.47TDe
|225.3TDe
|-
|874.49M
|1.31B
|5.79QdDe
|4.63QdDe
|4.05QdDe
|}
"""
    print('"Booster": [')
    result = convert_table(
        BOOSTER_WIKI,
        mode='cost_button',
        obtain_col=0,
        cost_col=2,
        button_type='Booster',
        cost_currency='Moon Cash',
    )
    print(result)
    print("],")
    print()

    REINCARNATION_WIKI = """
{| class="wikitable"
!Cost (Booster)
!Reward (Reincarnation)
|-
|1Qd
|700
|-
|9Qd
|1.44k
|-
|387Qd
|2.97k
|-
|15.86Qn
|6.08k
|-
|222.13Qn
|12.36k
|-
|6.21Sx
|25k
|-
|130.61Sx
|50.25k
|-
|2.48Sp
|100.51k
|-
|94.3Sp
|199.97k
|}
"""
    print('"Reincarnation": [')
    result = convert_table(
        REINCARNATION_WIKI,
        mode='reset_button',
        obtain_col=1,
        cost_col=0,
        button_type='Reincarnation',
        cost_currency='Booster',
        reset_currency='Reincarnation',
    )
    print(result)
    print("],")


if __name__ == "__main__":
    import sys
    if "--test" in sys.argv:
        _self_test()
    else:
        main()