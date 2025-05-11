"""
"""

from typing import List


def wrap(text: str,
         initial_indent: str = "  ",
         subsequent_indent: str = "  ",
         wrap_width: int = 80) -> str:
    """
    Wraps text. Better than `textwrap.wrap`, because it doesn't strip newlines, preserving the structure of text with intentional newlines.
    """

    text_li: List = text.split("\n")
    text_new: str = ""
    for text_el in text_li:
        # print(f"  text_el: {text_el}")

        li = []
        text_el_len = len(text_el)
        # print(f"  text_el_len: {text_el_len}")

        is_first = True
        indent = initial_indent
        indent_len = len(indent)
        text_el_len_new = text_el_len - indent_len
        # print(f"  text_el_len_new: {text_el_len_new}")

        width_el = wrap_width - indent_len
        idx_0 = 0
        idx_1 = width_el
        while idx_0 <= text_el_len_new:
            # print(f"    idx_0, idx_1: {idx_0}, {idx_1}")

            if is_first:
                indent = initial_indent
                is_first = False
            else:
                indent = subsequent_indent
            indent_len = len(indent)
            text_el_len_new = text_el_len - indent_len
            # print(f"  text_el_len_new: {text_el_len_new}")

            text_el_new = indent + text_el[idx_0:idx_1]
            li.append(text_el_new)

            width_el = idx_1 - idx_0
            idx_0 += width_el
            idx_1 += width_el
        text_new += "\n".join(li) + "\n"

    return text_new
