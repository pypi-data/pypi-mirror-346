import collections.abc
import datetime

import holidays


def clean_phone_number(phone_number):
    """
    Converts phone number from the format +1(812) 4321-543 into the format +1 8124321543.

    Args:
        phone_number (str): A phone number in the format +1(812) 4321-543.

    Returns:
        str: The phone number in the format +1 8124321543.
    """
    for r in (("(", " "), (") ", ""), ("-", "")):
        phone_number = phone_number.replace(*r)
    return phone_number


def mask_phone_number(phone_number):
    """
    Masks a phone number by replacing the first five digits with 'X'.

    Args:
        phone_number (str): The phone number to be masked.

    Returns:
        str: The masked phone number.
    """
    if phone_number is None:
        return phone_number
    phone_number = str(phone_number)
    length = len(phone_number)
    masked = ""

    last_digits = phone_number[5:]
    for i in range(length - 5):
        if phone_number[i].isalnum():
            masked += "X"
        else:
            masked += phone_number[i]  # keep delimiter(s)
    return masked + last_digits


def recursive_update(d, u):
    """
    Recursively updates a dictionary with another dictionary.

    Args:
        d (dict): The dictionary to be updated.
        u (dict): The dictionary to update with.

    Returns:
        dict: The updated dictionary.
    """
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = recursive_update(d.get(k, {}), v)
        else:
            d[k] = v
    return d


def next_business_day(date=None):
    """
    Returns the next business day from the given date.

    Args:
        date (datetime.date, optional): The date to start from. Defaults to today.

    Returns:
        datetime.date: The next business day.
    """
    if date is None:
        date = datetime.date.today()

    us_holidays = holidays.US()
    while date.isoweekday() > 5 or date in us_holidays:
        date += datetime.timedelta(days=1)
    return date


def tz_aware(dt):
    """
    Checks if a datetime object is timezone aware.

    Args:
        dt (datetime.datetime): The datetime object to check.

    Returns:
        bool: True if the datetime object is timezone aware, False otherwise.
    """
    return dt.tzinfo is not None and dt.tzinfo.utcoffset(dt) is not None
