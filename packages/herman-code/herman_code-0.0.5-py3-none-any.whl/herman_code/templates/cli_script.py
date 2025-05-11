"""
A template python script that uses command-line argument parsing.
"""

import argparse
import logging
import os
import pprint
from pathlib import Path
# Third-party packages
import pandas as pd
from sqlalchemy import URL
# Local packages
from herman_code import __version__ as hc_version
from herman_code.code.utilities import (choose_path_to_log,
                                        get_timestamp,
                                        make_dir_path)

if __name__ == "__main__":
    # >>> `Argparse` arguments >>>
    parser = argparse.ArgumentParser()

    # Arguments: Main
    pass

    # Arguments: Meta-parameters
    parser.add_argument("--log_level",
                        default=10,
                        type=int,
                        help="""Increase output verbosity. See "logging" module's log level for valid values.""")

    # Arguments: SQL connection settings
    parser.add_argument("--driver_name",
                        type=str,
                        help="")
    parser.add_argument("--server",
                        type=str,
                        help="")
    parser.add_argument("--database",
                        type=str,
                        help="")
    parser.add_argument("--user_domain",
                        type=str,
                        help="")
    parser.add_argument("--username",
                        default=os.environ["USER"],
                        type=str,
                        help="")
    parser.add_argument("--user_id",
                        default=None,
                        help="")
    parser.add_argument("--user_pwd",
                        default=None,
                        help="")

    arg_namespace = parser.parse_args()

    # Parsed arguments: Main
    pass

    # Parsed arguments: Meta-parameters
    log_level = arg_namespace.log_level

    # Parsed arguments: SQL connection settings
    driver_name = arg_namespace.driver_name
    server = arg_namespace.server
    database = arg_namespace.database
    user_domain = arg_namespace.user_domain
    username = arg_namespace.username
    user_id = arg_namespace.user_id
    user_pwd = arg_namespace.user_pwd
    # <<< `Argparse` arguments <<<

    # >>> Argument checks >>>
    # NOTE TODO Look into handling this natively with `argparse` by using `subcommands`. See "https://stackoverflow.com/questions/30457162/argparse-with-different-modes"
    pass
    # <<< Argument checks <<<

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

    # Variables: Path construction: Project-specific
    pass

    # Variables: SQL Parameters
    if user_id:
        user_id = user_id[:]
    else:
        user_id = fr"{user_domain}\{username}"
    if user_pwd:
        user_pwd = user_pwd
    else:
        raise Exception("Need password.")
    connection_string = URL.create(drivername=driver_name,
                                   username=user_id,
                                   password=user_pwd,
                                   host=server,
                                   database=database)

    # Variables: Other
    pass

    # Directory creation: General
    make_dir_path(run_intermediate_dir)
    make_dir_path(run_output_dir)
    make_dir_path(run_logs_dir)

    # Logging block
    logpath = run_logs_dir.joinpath(f"log {run_timestamp}.log")
    log_format = logging.Formatter("""[%(asctime)s][%(levelname)s](%(funcName)s): %(message)s""")

    logger = logging.getLogger(__name__)

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
    arg_list_string = pprint.pformat(arg_list)  # TODO Remove secrets from list to print, e.g., passwords.
    logger.info(f"""Script arguments:\n{arg_list_string}""")

    # >>> Begin script body >>>

    _ = pd

    # Output location summary
    logger.info(f"""Script output is located in the following directory: "{choose_path_to_log(path=run_output_dir, root_path=project_dir)}".""")

    # <<< End script body <<<
    logger.info(f"""Finished running "{choose_path_to_log(path=this_file_path, root_path=project_dir)}".""")
