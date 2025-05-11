"""
"""

from herman_code.tests.git_commit.tests import test_parse_git_commit_editmsg

if __name__ == "__main__":

    # Arguments
    VERBOSE = 2

    # Argument parsing
    verbose = VERBOSE

    # Scripts

    if verbose == 0:
        battery_result = test_parse_git_commit_editmsg(verbose=verbose)
    elif verbose > 0:
        battery_result, battery_details = test_parse_git_commit_editmsg(verbose=verbose)
        num_tests = battery_details["num_tests"]
        num_passed = battery_details["num_passed"]
        print(f"{num_passed} of {num_tests} tests passed.")

    if battery_result:
        print("Test battery passed ✅")
    else:
        print("Test battery failed ❌")
