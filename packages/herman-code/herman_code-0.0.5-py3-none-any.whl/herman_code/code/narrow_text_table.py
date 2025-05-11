"""
File for function `narrow_text_table`
"""

from typing import List


def narrow_text_table(strings: List[str],
                      chunksize: int,
                      pad_strings: bool = False,
                      pad_char: str = " ") -> str:
    """
    Narrows a text table by splitting the lines in a string.
    
    For a text table with headers, a number of data rows n, and lines of width w_1, w_2, ..., w_i, ... w_n, this function reduces all lines, starting from the header and then including the data rows, from their original width w_i to the requested width `chunksize`. If padding is necessary, the character `pad_char` will be used to pad the lines. Padding can be forced when unnecessary using the boolean parameter `pad_strings`.

    Example:
    string_ = \"\"\"\\
    header_1 header_2 header_3
    val_1_1  val_2    vaaaaaaaaaaaal_3
    val_1_2\"\"\"
    narrow_text_table(strings=string_.split("\n"),
                      chunksize=9)
    # Result:
    header_1
    val_1_1
    val_1_2
    header_2
    val_2

    header_3
    vaaaaaaaa
    
    
    aaaal_3
    """

    # Determine if padding is necessary
    lens = [len(string_) for string_ in strings]
    max_len = max(lens)
    min_len = min(lens)
    rmax = max_len / chunksize
    rmin = min_len / chunksize
    if int(rmin) < int(rmax):
        need_padding = True
    else:
        need_padding = False

    # Pad strings to same length

    if pad_strings or need_padding:
        strings_2 = []
        for string_1 in strings:
            string_len = len(string_1)
            if string_len > max_len:
                pass
            else:
                string_2 = string_1 + pad_char * (max_len - string_len)
                strings_2.append(string_2)

    # Chunk
    num_strings = len(strings_2)
    index_0 = 0
    index_1 = index_0 + chunksize
    result = ""
    it_1 = 0
    while index_0 < max_len:
        it_1 += 1
        for it_2, string_ in enumerate(strings_2, start=1):

            if it_2 == num_strings:
                if it_1 >= rmax:
                    row_len = len(string_)
                else:
                    row_len = index_1
                string_cap = f"|<---end {it_1} ({row_len})"
            else:
                string_cap = "|"
            line_part = string_[index_0:index_1]
            line_part = line_part + string_cap
            result += line_part + "\n"
        index_0 += chunksize
        index_1 += chunksize
    return result
