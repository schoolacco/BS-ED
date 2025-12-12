import json
import os

def convert_savefile(old_path, new_path=None):
    """
    Converts the old nested save format into the new flat {item: value} format.
    Keeps only the 'Value' field of each item.
    """

    if new_path is None:
        base, ext = os.path.splitext(old_path)
        new_path = base + "_converted" + ext

    with open(old_path, "r") as f:
        old_data = json.load(f)

    new_data = {"Stats": {}}

    # old format: { section: { item: {Value: x, Multis: {...}} } }
    for section, items in old_data.items():
        for item_name, item_info in items.items():
            if isinstance(item_info, dict) and "Value" in item_info:
                new_data["Stats"][item_name] = item_info["Value"]
            else:
                # fallback in case a malformed entry appears
                if section not in new_data:
                    new_data[section] = {}
                if section == "Upgrades":
                    new_data[section][item_name] = item_info.get("current_lvl", 0)
                else:
                  new_data[section][item_name] = item_info

    with open(new_path, "w") as f:
        json.dump(new_data, f, indent=4)

    return new_path

convert_savefile("savefile.json", "test_save.json")