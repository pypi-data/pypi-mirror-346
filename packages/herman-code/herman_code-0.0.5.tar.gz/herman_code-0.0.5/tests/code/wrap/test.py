"""
"""

from herman_code.code.wrap import wrap

case_1 = """\
If true, wrapping will occur preferably on whitespaces and right after hyphens in compound words, as it is customary in English. If false, only whitespaces will be considered as potentially good places for line breaks, but you need to set break_long_words to false if you want truly insecable words. Default behaviour in previous versions was to always allow breaking hyphenated words.
And here's a very short paragraph.
"""

sltn_1 = """  If true, wrapping will occur preferably on whitespaces and right after hyphens
   in compound words, as it is customary in English. If false, only whitespaces 
  will be considered as potentially good places for line breaks, but you need to
   set break_long_words to false if you want truly insecable words. Default beha
  viour in previous versions was to always allow breaking hyphenated words.
  And here's a very short paragraph.

"""

case_2 = case_1[:]

sltn_2 = """--->If true, wrapping will occur preferably on whitespaces and right after hyphe
..ns in compound words, as it is customary in English. If false, only whitespa
..ces will be considered as potentially good places for line breaks, but you n
..eed to set break_long_words to false if you want truly insecable words. Defa
..ult behaviour in previous versions was to always allow breaking hyphenated w
..ords.
--->And here's a very short paragraph.

"""

rslt_1 = wrap(text=case_1,
              initial_indent="  ",
              subsequent_indent="  ")
test_1 = rslt_1 == sltn_1

rslt_2 = wrap(text=case_2,
              initial_indent="--->",
              subsequent_indent="..",
              wrap_width=80)
test_2 = rslt_2 == sltn_2

results = {1: {"case": case_1,
               "sltn": sltn_1,
               "rslt": rslt_1,
               "test": test_1},
           2: {"case": case_2,
               "sltn": sltn_2,
               "rslt": rslt_2,
               "test": test_2}}

print("We prepend and append case, solution, and test result strings with markers (`>>>`, `<<<`) to more easily identify subtle differences in whitespace.")
for it, case_di in results.items():
    case_it = case_di["case"]
    sltn_it = case_di["sltn"]
    rslt_it = case_di["rslt"]
    test_it = case_di["test"]
    print(f"Case {it}:\n")
    print(f">>>{case_it}<<<")
    print("")
    print(f">>>{sltn_it}<<<")
    print("")
    print(f">>>{rslt_it}<<<")
    print("")
    print(test_it)
    print("")
