"""
Useful functions.
"""

import datetime as dt
import os
from pathlib import Path
from typing import (Literal,
                    Tuple,
                    Union)

from herman_code import logging_choices_string


def choose_path_to_log(path: Path,
                       root_path: Path) -> Path:
    """
    Decides if a path is a subpath of `root_path`. If it is, display it reltaive to `root_path`. If it is not, display it as an absolute path.
    """
    common_path = os.path.commonpath([path.absolute(), root_path.absolute()])

    len_common_path = len(common_path)
    len_root_path = len(str(root_path.absolute()))
    if len_common_path < len_root_path:
        path_to_display = path
    elif len_common_path == len_root_path:
        path_to_display = path.absolute().name
    elif len_common_path > len_root_path:
        path_to_display = path.absolute().relative_to(root_path)
    else:
        raise Exception("An unexpected error occurred.")

    return path_to_display


def logging_choice_parser(string_: str) -> Union[int, str]:
    """
    Checks if a string is in one of the choices for the "logging" module's log level. This function is case sensitive because the `setLevel` method is case sensitive; e.g., `logger.setLevel("DEBUG")` works while `logger.setLevel("debug")` produces an error.
    """
    try:
        return int(string_)
    except ValueError:
        if string_ in logging_choices_string:
            return string_
        else:
            raise Exception(f"""Input was not found in any of the possible log level choices for the "logging" module. You supplied "{string_}".""")
    else:
        raise Exception


def make_dir_path(directory_path: str) -> None:
    """
    Check if all directories exists in a path. If not, create them
    """
    path_obj = Path(directory_path)
    paths = list(path_obj.parents)[::-1] + [path_obj]
    for dir in paths:
        if not os.path.exists(dir):
            os.mkdir(dir)


def successive_parents(path_obj: Path,
                       num_levels: int) -> Tuple[Path, int]:
    """
    Successively get the parents of the Path object submitted.
    """
    while num_levels > 0:
        path_obj = path_obj.parent
        num_levels -= 1
    return path_obj, num_levels


def get_timestamp(mode: Literal["date", "time"] = "time"):
    if mode == "date":
        return dt.datetime.now().strftime("%Y-%m-%d")
    elif mode == "time":
        return dt.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    else:
        raise Exception("Option must be one of {date, time}.")
