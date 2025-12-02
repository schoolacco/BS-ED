import pyperclip
from pathlib import Path
import os
if os.path.exists(Path.home()/"Documents"/"toodarktosee"):
    file = open(Path.home()/"Documents"/"toodarktosee", "r")
    content = file.read()
    content = list(content)
    code = content[19]+content[34]+content[49]+content[53]+content[54]+content[72]+content[83]+content[103]+content[118]+content[137]+content[142]+content[147]
    print(code)
    pyperclip.copy(code)