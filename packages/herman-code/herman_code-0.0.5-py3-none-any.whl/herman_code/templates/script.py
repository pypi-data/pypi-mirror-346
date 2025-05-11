"""
A template python script.
"""

import logging
import os
from pathlib import Path
# Third-party packages
import pandas as pd
from sqlalchemy import URL
# Local packages
from herman_code import __version__ as hc_version
from herman_code.code.utilities import (choose_path_to_log,
                                        get_timestamp,
                                        make_dir_path)

# Arguments: Main
pass

# Arguments: General
LOG_LEVEL = "INFO"

# Arguments: SQL parameters
DRIVER_NAME = None
USER_ID = None
USER_PWD = None
USER_DOMAIN = None
USERNAME = None
SERVER = None
DATABASE = None


if __name__ == "__main__":
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
    if USER_ID:
        user_id = USER_ID[:]
    else:
        user_id = fr"{USER_DOMAIN}\{USERNAME}"
    if USER_PWD:
        user_pwd = USER_PWD
    else:
        raise Exception("Need password.")
    connection_string = URL.create(drivername=DRIVER_NAME,
                                   username=user_id,
                                   password=user_pwd,
                                   host=SERVER,
                                   database=DATABASE)

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
    stream_handler.setLevel(LOG_LEVEL)
    stream_handler.setFormatter(log_format)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    logger.setLevel(9)

    logger.info(f"""Begin running "{choose_path_to_log(path=this_file_path, root_path=project_dir)}".""")
    logger.info(f"""Herman's Code version is "{hc_version}".""")
    logger.info(f"""All other paths will be reported in debugging relative to the current working directory: "{choose_path_to_log(path=project_dir, root_path=project_dir)}".""")
    logger.info(f"""Script arguments:


    # Arguments
    ``: "{""}"

    # Arguments: General
    `LOG_LEVEL` = "{LOG_LEVEL}"
    """)

    # >>> Begin script body >>>

    _ = pd

    # Output location summary
    logger.info(f"""Script output is located in the following directory: "{choose_path_to_log(path=run_output_dir, root_path=project_dir)}".""")

    # <<< End script body <<<
    logger.info(f"""Finished running "{choose_path_to_log(path=this_file_path, root_path=project_dir)}".""")
