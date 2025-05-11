"""
"""

import datetime as dt


class ElapsedTimeString(str):
    """
    """

    def __new__(etstring,
                years: int,
                months: int,
                weeks: int,
                days: int,
                hours: int,
                minutes: int,
                seconds: int,
                microseconds: int):
        etstring.years = years
        etstring.months = months
        etstring.weeks = weeks
        etstring.days = days
        etstring.hours = hours
        etstring.minutes = minutes
        etstring.seconds = seconds
        etstring.microseconds = microseconds

        etstring.string = f"""\
{etstring.years}-Y \
{etstring.months}-M \
{etstring.weeks}-W \
{etstring.days}-D \
\
{etstring.hours}:\
{etstring.minutes}:\
{etstring.seconds}.\
\
{etstring.microseconds}\
"""
        return str.__new__(etstring, object=etstring.string)


def get_elapsed_time(t1: float,
                     t0: float,
                     verbose: bool = False) -> str:
    """
    Returns the elapsed time in the format `Y M W D hh:mm:ss`.
    NOTE: This function uses the statistical average for units of time. That means:
        1 month = 4.3 weeks
        1 year = 364.25 days
    """
    time_elapsed_float = t1 - t0
    dt0 = dt.datetime.fromtimestamp(0)
    dt1 = dt.datetime.fromtimestamp(time_elapsed_float)

    time_elapsed_delta_obj = dt1 - dt0

    time_elapsed_days = time_elapsed_delta_obj.days
    time_elapsed_seconds = time_elapsed_delta_obj.seconds
    time_elapsed_microseconds = time_elapsed_delta_obj.microseconds
    if verbose:
        message = f"""
        Time elapsed (days): {time_elapsed_days}
        Time elapsed (seconds): {time_elapsed_seconds}
        Time elapsed (microseconds): {time_elapsed_microseconds}
        """
        print(message)

    integer_microseconds, remainder_microseconds = divmod(time_elapsed_microseconds, 1)

    if verbose:
        message = f"""\
        Integer microseconds: {integer_microseconds}
            remainder microseconds: {remainder_microseconds}
        """
        print(message)

    integer_minutes, remainder_seconds = divmod(time_elapsed_seconds, 60)
    integer_hours, remainder_minutes = divmod(integer_minutes, 60)

    if verbose:
        message = f"""\
        Integer hours: {integer_hours}
            remainder minutes: {remainder_minutes}
        Integer minutes: {integer_minutes}
            remainder seconds: {remainder_seconds}
        """
        print(message)

    integer_weeks, remainder_days = divmod(time_elapsed_days, 7)
    integer_months, remainder_weeks = divmod(integer_weeks, 52 / 12)
    integer_years, remainder_months = divmod(integer_months, 12)

    if verbose:
        message = f"""Integer years: {integer_years}
            Remainder months: {remainder_months}
        Integer months: {integer_months}
            Remainder weeks: {remainder_weeks}
        Integer weeks: {integer_weeks}
            Remainder days: {remainder_days}
        Integer hours: {integer_hours}
            Remainder minutes: {remainder_minutes}
        """
        print(message)

    if verbose:
        message = f"""
        {integer_years} Years
        {remainder_months} Months
        {remainder_weeks} Weeks
        {remainder_days} Days

        {integer_hours} Hours
        {remainder_minutes} Minutes
        {remainder_seconds} Seconds

        {integer_microseconds} Microseconds
        """
        print(message)

    time_elapsed_string = ElapsedTimeString(years=int(integer_years),
                                            months=int(remainder_months),
                                            weeks=int(remainder_weeks),
                                            days=int(remainder_days),
                                            hours=integer_hours,
                                            minutes=remainder_minutes,
                                            seconds=remainder_seconds,
                                            microseconds=integer_microseconds)

    return time_elapsed_string
