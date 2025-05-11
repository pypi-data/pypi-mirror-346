"""
__init__ file for "herman_code" package
"""

import logging
from pathlib import Path
from os.path import dirname

from herman_code import __about__
from herman_code.classes import SecretString

__version__ = __about__.__version__
PATH = Path(dirname(__file__)).absolute()

# Logging choices
logging_choices_numeric_min = min(logging.getLevelNamesMapping().values())
logging_choices_numeric_max = max(logging.getLevelNamesMapping().values())
logging_choices_numeric = list(range(logging_choices_numeric_min, logging_choices_numeric_max + 1))
logging_choices_string = list(logging.getLevelNamesMapping().keys())
logging_choices = logging_choices_numeric + logging_choices_string
