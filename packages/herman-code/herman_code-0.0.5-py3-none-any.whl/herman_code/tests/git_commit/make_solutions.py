"""
Create solution files for positive and negative test cases.

*NOTE* Negative test cases solutions are not yet implemented.
"""

from pathlib import Path
from pickle import dump

from herman_code.git_commit import parse_git_commit_editmsg
from herman_code.tests.git_commit import __file__ as fp
from herman_code.tests.git_commit.data.negatives import __file__ as fp_negs
from herman_code.tests.git_commit.data.positives import __file__ as fp_poss
from herman_code.tests.git_commit.data.solutions_p import __file__ as fp_poss_s
from herman_code.tests.git_commit.data.solutions_p import __file__ as fp_negs_s

if __name__ == "__main__":

    dir_poss = Path(fp_poss).parent
    dir_negs = Path(fp_negs).parent
    dir_poss_s = Path(fp_poss_s).parent
    dir_negs_s = Path(fp_negs_s).parent

    input_files = []
    for dir_ in [dir_poss]:
        for fp in dir_.iterdir():
            if fp.suffix == ".text":
                input_files.append(fp)

    for fp in input_files:
        rr = parse_git_commit_editmsg(filepath=fp)
        st = fp.stem
        to_path = dir_poss_s.joinpath(f"{st}.pickle")
        with open(to_path, "wb") as file_:
            dump(rr, file_)
