"""
Tests for "git_commit.py"
"""

from itertools import zip_longest
from pathlib import Path
from pickle import load
from pprint import pformat
from typing import Literal

from herman_code.code.wrap import wrap
from herman_code.git_commit import parse_git_commit_editmsg
from herman_code.tests.match_test_files import match_test_files
from herman_code.tests.git_commit.data.positives import __file__ as fp_poss
from herman_code.tests.git_commit.data.solutions_p import __file__ as fp_poss_s

dir_test_cases = Path(fp_poss).parent
dir_test_solns = Path(fp_poss_s).parent

def test_parse_git_commit_editmsg_(verbose: Literal[1, 2] = 0):
    """
    """
    if verbose >= 0:
        pass
    else:
        raise Exception("Parameter `verbose` must be a non-negative integer.")
    
    if True:
        case_file_li = sorted([fp for fp in dir_test_cases.iterdir() if fp.suffix == ".text"])
        soln_file_li = sorted([fp for fp in dir_test_solns.iterdir() if fp.suffix == ".pickle"])
        matched_files = zip_longest(case_file_li, soln_file_li, fillvalue=None)
    elif True:
        # TODO, implement `match_test_files`
        matched_files = match_test_files()

    num_tests = 0
    results_li = []
    for (case_file, soln_file) in matched_files:
        num_tests += 1

        if soln_file:
            with open(file=soln_file, mode="rb") as file_:
                expc_result = load(file_)
        else:
            expc_result = None

        if case_file:
            with open(case_file, "r") as file_:
                case_text = file_.read()

            case_result = parse_git_commit_editmsg(filepath=case_file)
            test_result = case_result == expc_result
        else:
            case_text = ""
            test_result = None
        results_li.append(test_result)

        if verbose > 1:
            message_1 = f"""\
>>> Case {num_tests} >>> 
{case_text}
<<< Case {num_tests} <<<
>>> Solution {num_tests} >>>
{pformat(expc_result)}
<<< Solution {num_tests} <<<
>>> Test Output {num_tests} >>>
{pformat(case_result)}
<<< Test Output {num_tests} <<<
>>> Test Result {num_tests} >>>
Pass: {test_result}
<<< Test Result {num_tests} <<<
"""
            print(f"""Working on test case #{num_tests}:""")
            message_wrapped_1 = wrap(text=message_1,
                                    initial_indent=" " * 2,
                                    subsequent_indent=" " * 2,
                                    wrap_width=100)
            print(message_wrapped_1)

    num_passed = sum(results_li)
    battery_result = num_passed == num_tests
    battery_detail = {"num_tests": num_tests,
                      "num_passed": num_passed}

    if verbose == 0:
        return battery_result
    elif verbose > 0:
        return battery_result, battery_detail


def test_parse_git_commit_editmsg(verbose: int = 0):
    """
    """
    if verbose == 0:
        battery_result = test_parse_git_commit_editmsg_(verbose=verbose)
    elif verbose > 0:
        battery_result, battery_details = test_parse_git_commit_editmsg_(verbose=verbose)
        num_tests = battery_details["num_tests"]
        num_passed = battery_details["num_passed"]
        print(f"{num_passed} of {num_tests} tests passed.")

    if battery_result:
        print("Test battery passed ✅")
    else:
        print("Test battery failed ❌")


def mf_1(args):
    """
    """
    test_parse_git_commit_editmsg(args.v)
