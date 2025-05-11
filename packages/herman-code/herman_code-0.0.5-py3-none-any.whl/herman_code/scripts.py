"""
Generate a console script by delegating to a python file script.
"""

import subprocess
import sys
from pathlib import Path

from herman_code.hcode import (__file__ as fp_1,
                               __name__ as sn_1)  # Script name

def hcode():
    script_path = Path(fp_1)
    subprocess.run([script_path, *sys.argv[1:]])


# QA
sn_1 = sn_1.split(".")[-1]
assert hcode.__name__ == sn_1, "Function name doesn't match script name"


if __name__ == "__main__":
    hcode()
