"""
Test
"""

import datetime as dt

from herman_code.code.utilities import get_elapsed_time


t1 = dt.datetime.now().timestamp()

# Units of time expressed as seconds
SECONDS = 1
MINUTES = SECONDS * 60
HOURS = MINUTES * 60
DAYS = HOURS * 24
WEEKS = DAYS * 7
if False:
    MONTHS = 364.25 * DAYS / 12
elif True:
    MONTHS = 52 / 12 * WEEKS
YEARS = MONTHS * 12

# Constants
CONSTANT = 0.123456789

LIST_OF_STARTING_TIMES = [t1 - (1 * YEARS + CONSTANT),  # 1-Y 0-M 0-W 0-D 0:0:0.123457
                          t1 - (1 * YEARS + 1 * MONTHS + CONSTANT),  # 1-Y 1-M 0-W 0-D 0:0:0.123457
                          t1 - (1 * YEARS + 1 * MONTHS + 1 * WEEKS + CONSTANT),  # 1-Y 1-M 1-W 0-D 0:0:0.123457
                          t1 - (1 * YEARS + 1 * MONTHS + 1 * WEEKS + 1 * DAYS + CONSTANT),  # 1-Y 1-M 1-W 1-D 0:0:0.123457
                          t1 - (1 * YEARS + 1 * MONTHS + 1 * WEEKS + 1 * DAYS + 1 * HOURS + CONSTANT),  # 1-Y 1-M 1-W 1-D 1:0:0.123457
                          t1 - (1 * YEARS + 1 * MONTHS + 1 * WEEKS + 1 * DAYS + 1 * HOURS + 1 * MINUTES + CONSTANT),  # 1-Y 1-M 1-W 1-D 1:1:0.123457
                          t1 - (1 * YEARS + 1 * MONTHS + 1 * WEEKS + 1 * DAYS + 1 * HOURS + 1 * MINUTES + 1 * SECONDS + CONSTANT),  # 1-Y 1-M 1-W 1-D 1:1:1.123457
                          t1 - (1 * MONTHS + 1 * WEEKS + 1 * DAYS + 1 * HOURS + 1 * MINUTES + 1 * SECONDS + CONSTANT),  # 0-Y 1-M 1-W 1-D 1:1:1.123457
                          t1 - (1 * WEEKS + 1 * DAYS + 1 * HOURS + 1 * MINUTES + 1 * SECONDS + CONSTANT),  # 0-Y 0-M 1-W 1-D 1:1:1.123457
                          t1 - (1 * DAYS + 1 * HOURS + 1 * MINUTES + 1 * SECONDS + CONSTANT),  # 0-Y 0-M 0-W 1-D 1:1:1.123457
                          t1 - (1 * HOURS + 1 * MINUTES + 1 * SECONDS + CONSTANT),  # 0-Y 0-M 0-W 0-D 1:1:1.123457
                          t1 - (1 * MINUTES + 1 * SECONDS + CONSTANT),  # 0-Y 0-M 0-W 0-D 0:1:1.123457
                          t1 - (1 * SECONDS + CONSTANT),  # 0-Y 0-M 0-W 0-D 0:0:1.123457
                          t1 - (CONSTANT)  # 0-Y 0-M 0-W 0-D 0:0:0.123457
                          ]
LIST_OF_CHECKS = ["1-Y 0-M 0-W 0-D 0:0:0.123457",
                  "1-Y 1-M 0-W 0-D 0:0:0.123457",
                  "1-Y 1-M 1-W 0-D 0:0:0.123457",
                  "1-Y 1-M 1-W 1-D 0:0:0.123457",
                  "1-Y 1-M 1-W 1-D 1:0:0.123457",
                  "1-Y 1-M 1-W 1-D 1:1:0.123457",
                  "1-Y 1-M 1-W 1-D 1:1:1.123457",
                  "0-Y 1-M 1-W 1-D 1:1:1.123457",
                  "0-Y 0-M 1-W 1-D 1:1:1.123457",
                  "0-Y 0-M 0-W 1-D 1:1:1.123457",
                  "0-Y 0-M 0-W 0-D 1:1:1.123457",
                  "0-Y 0-M 0-W 0-D 0:1:1.123457",
                  "0-Y 0-M 0-W 0-D 0:0:1.123457",
                  "0-Y 0-M 0-W 0-D 0:0:0.123457"
                  ]

print("Starting test suite for `get_elapsed_time`.")
results_list = []
for el, check in zip(LIST_OF_STARTING_TIMES, LIST_OF_CHECKS):
    if False:
        message = f"""
    t1 = {t1}
    t0 = {el}\
"""
        print(message)
    elapsed_time_string = get_elapsed_time(t1=t1,
                                           t0=el,
                                           verbose=False)
    result = elapsed_time_string == check
    result_message = f"""\
    Pass: {result}\
"""
    print(result_message)
    results_list.append(result)
print(f"Percentage of test passed: {sum(results_list) / len(results_list):0.2%}")
