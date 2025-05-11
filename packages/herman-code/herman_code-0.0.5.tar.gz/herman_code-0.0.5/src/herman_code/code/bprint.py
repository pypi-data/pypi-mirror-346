"""
"""

from pprint import pformat
from textwrap import indent
from typing import Any


def bprint(obj: Any,
           prefix: str):
    """
    Better pprint
    """
    text = indent(pformat(object=obj,
                          compact=True),
                  prefix=prefix)
    print(text)
