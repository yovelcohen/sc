from datetime import timedelta, datetime

from django.utils import timezone


def convert_unix_time_to_datetime(timestamp, date_only=False):
    """
    :rtype datetime.datetime
    """
    timestamp = int(timestamp) if isinstance(timestamp, str) else timestamp
    return datetime.fromtimestamp(timestamp) if date_only is False else datetime.fromtimestamp(timestamp).date()


def convert_datetime_to_unix(date):
    date = convert_str_to_date(date) if not isinstance(date, datetime) else date
    return int(date.strftime("%s"))


def convert_str_to_date(date_to_convert):
    """
    converts a stringed date to date object
    :rtype datetime.date
    """
    return datetime.strptime(date_to_convert, '%Y-%m-%d').date() if isinstance(date_to_convert,
                                                                               str) else date_to_convert


def construct_dates_dict(days, end_date, as_tup=False):
    """
    the front needs values for all last 30 days for the graph even if don't have them.
    these method construct a dictionary containing the last 30 days as keys and 0 for there values.
    later on the days that have real values will replace the zeros.
    :param as_tup: returns dates tuple instead of dict
    :param days: number of days to construct the dict for, defaults to 30
    :param end_date: date to end the dictionary with, defaults to today
    :rtype: dict
    """
    days = days if isinstance(days, int) else days.days
    date_list = tuple(end_date - timedelta(days=x) for x in range(days + 1))
    return {date: 0 for date in date_list} if as_tup is False else date_list


def create_dates_range(days: int, date=None, forward=False):
    """
    creates date range list for Django QuerySet filtering
    :param days: amount of days to filter by
    :param date: the date to start from, defaults to today
    :param forward: specify weather to go forward or backwards from given date, defaults to back
    :rtype: list
    """
    date = timezone.now().date() if date is None else date
    if forward:
        second_date = date + timedelta(days=days)
        return [date, second_date]
    else:
        second_date = date - timedelta(days=days)
        return [second_date, date]


def clean_dates_in_dict(_dict):
    """
    takes in a dictionary that has dates as keys and stringifies those dates
    """
    new_dict = {}
    for item in _dict.items():
        new_dict.update({str(item[0]): item[1]})
    del _dict
    return new_dict


def get_first_day_of_the_quarter(date):
    """
    this function returns the start date for the quarter
    """
    return timezone.datetime(date.year, 3 * ((date.month - 1) // 3) + 1, 1)


def dates_list_generator(start, days):
    for x in range(days):
        yield start + timedelta(days=x)


def get_mock_df(name, name_field, fields, dates_list):
    import pandas as pd
    fields = {field: 0 for field in fields}
    df = pd.DataFrame({'date': dates_list, name_field: name, **fields})
    return df
