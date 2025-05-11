#!/usr/bin/env python

"""
Package CLI script.
"""

import argparse
import logging
import os
import sys
from pathlib import Path
from pprint import pformat, pprint

pass

from herman_code import __version__ as hc_version
from herman_code.git_commit import (mf_1 as mf_2,
                                    mf_2 as mf_3)
from herman_code.code.utilities import (choose_path_to_log,
                                        get_timestamp,
                                        make_dir_path)
from herman_code.tests.git_commit.tests import mf_1 as mf_4


def mf_1():
    print("Be strong!")


# Argparse constants
TEXT_HELP_V = "The verbosity level, a non-negative integer."


if __name__ == "__main__":
    # >>> Argument parsing >>>
    parser = argparse.ArgumentParser()

    # Meta-options
    parser.add_argument("--log_level",
                        default=10,
                        type=int,
                        help="""Increase log verbosity. See "logging" module's log level for valid values.""")

    # Subparsing
    subparsers = parser.add_subparsers(required=True)

    # ::: Arguments: Command "Help" :::
    PARSER_HELP_NAME = "help"
    parser_help = subparsers.add_parser(name=PARSER_HELP_NAME)
    parser_help.set_defaults(func=mf_1, _command=PARSER_HELP_NAME)

    # ::: Arguments: Command "Parse Git commit message file" :::
    PARSER_PARSE_GIT_CMT_NAME = "parse_git_cmt"
    parser_parse_git_cmt = subparsers.add_parser(name=PARSER_PARSE_GIT_CMT_NAME,
                                               help="Parses a Git commit `COMMIT_EDITMSG` file.")
    parser_parse_git_cmt.add_argument("file_path",
                                      help="The path to the COMMIT_EDITMSG file.")
    parser_parse_git_cmt.add_argument("-v",
                                      type=int,
                                      default=0,
                                      help=TEXT_HELP_V)
    parser_parse_git_cmt.set_defaults(func=mf_2,
                                      _command=PARSER_PARSE_GIT_CMT_NAME)

    # ::: Arguments: Command "Check Git commit message file" :::
    PARSER_CHK_GIT_CMT_NAME = "chk_git_cmt"
    parser_chk_git_cmt = subparsers.add_parser(name=PARSER_CHK_GIT_CMT_NAME,
                                               help="Checks if a Git commit `COMMIT_EDITMSG` file is descriptive enough.")
    parser_chk_git_cmt.add_argument("-fp",
                                    "--file_path",
                                    default="COMMIT_EDITMSG",
                                    help="The path to the COMMIT_EDITMSG file.")
    parser_chk_git_cmt.add_argument("-v",
                                    type=int,
                                    default=0,
                                    help=TEXT_HELP_V)
    parser_chk_git_cmt.set_defaults(func=mf_3,
                                    _command=PARSER_CHK_GIT_CMT_NAME)

    # ::: Arguments: Command "Tests" :::
    PARSER_TESTS_NAME = "tests"
    parser_chk_git_cmt = subparsers.add_parser(name=PARSER_TESTS_NAME,
                                               help="Tests modules and their functions.")
    parser_chk_git_cmt.add_argument("module",
                                    help="The module to test.")
    parser_chk_git_cmt.add_argument("function",
                                    help="The module's function to test.")
    parser_chk_git_cmt.add_argument("-v",
                                    type=int,
                                    help="The verbosity level, a non-negative integer.")
    parser_chk_git_cmt.set_defaults(_command=PARSER_TESTS_NAME,
                                    v=0)

    # Parse arguments
    arg_namespace = parser.parse_args()

    # Parsed arguments: "Help"
    if arg_namespace._command == PARSER_HELP_NAME:
        result = arg_namespace.func()
    elif arg_namespace._command == PARSER_PARSE_GIT_CMT_NAME:
        result = arg_namespace.func(arg_namespace)
        pprint(result)
    elif arg_namespace._command == PARSER_CHK_GIT_CMT_NAME:
        result = arg_namespace.func(arg_namespace)
        pprint(result)
    elif arg_namespace._command == PARSER_TESTS_NAME:
        if arg_namespace.module == "git_commit":
            if arg_namespace.function == "parse_git_commit_editmsg":
                mf_4(arg_namespace)
            else:
                print("Bad function choice.")
                sys.exit(1)
        else:
            print("Bad module choice.")
            sys.exit(1)
    else:
        print("Bad command choice.")
        parser.print_usage()
        sys.exit(1)

    sys.exit(0)

    # Parsed arguments: Meta-parameters
    log_level = arg_namespace.log_level

    # <<< Argument parsing <<<

    # Variables: Path construction: General
    run_timestamp = get_timestamp()
    this_file_path = Path(__file__)
    this_file_stem = this_file_path.stem
    current_working_dir = Path(os.getcwd()).absolute()
    project_dir = current_working_dir
    data_dir = project_dir.joinpath("data")
    if data_dir:
        input_data_dir = data_dir.joinpath("input")
        intermediate_data_dir = data_dir.joinpath("intermediate")
        output_data_dir = data_dir.joinpath("output")
        if intermediate_data_dir:
            run_intermediate_dir = intermediate_data_dir.joinpath(this_file_stem, run_timestamp)
        if output_data_dir:
            run_output_dir = output_data_dir.joinpath(this_file_stem, run_timestamp)
    logs_dir = project_dir.joinpath("logs")
    if logs_dir:
        run_logs_dir = logs_dir.joinpath(this_file_stem)
    sql_dir = project_dir.joinpath("sql")

    # Directory creation: General
    make_dir_path(run_intermediate_dir)
    make_dir_path(run_output_dir)
    make_dir_path(run_logs_dir)

    # Logging block
    logpath = run_logs_dir.joinpath(f"log {run_timestamp}.log")
    log_format = logging.Formatter("""[%(asctime)s][%(levelname)s](%(funcName)s): %(message)s""")

    logger = logging.getLogger("herman_code.manly")

    file_handler = logging.FileHandler(logpath)
    file_handler.setLevel(9)
    file_handler.setFormatter(log_format)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)
    stream_handler.setFormatter(log_format)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    logger.setLevel(9)

    logger.info(f"""Begin running "{choose_path_to_log(path=this_file_path, root_path=project_dir)}".""")
    logger.info(f"""Herman's Code version is "{hc_version}".""")
    logger.info(f"""All other paths will be reported in debugging relative to the current working directory: "{choose_path_to_log(path=project_dir, root_path=project_dir)}".""")

    arg_list = arg_namespace._get_args() + arg_namespace._get_kwargs()
    arg_list_string = pformat(arg_list)  # TODO Remove secrets from list to print, e.g., passwords.
    logger.info(f"""Script arguments:\n{arg_list_string}""")

    # >>> Begin script body >>>

    pass

    # Output location summary
    logger.info(f"""Script output is located in the following directory: "{choose_path_to_log(path=run_output_dir, root_path=project_dir)}".""")

    # <<< End script body <<<
    logger.info(f"""Finished running "{choose_path_to_log(path=this_file_path, root_path=project_dir)}".""")
