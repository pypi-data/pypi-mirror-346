""" Copyright (c) 2021 RoZetta Technology Pty Ltd. All rights reserved."""
from datetime import datetime, timezone, date


class TimeFormatter:
    """ TimeFormatter subclasses GenericDateTimeFormatter to safely convert string that are expected to be in ISO 8601
    datetime format to a datetime object and vice versa.
    """
    def __init__(self, dt_format: str):
        self.dt_format = dt_format

    # Method name does not reflect correct return type however there are existing consumers of this method and the
    # interface cannot be changed.
    def str_to_date(self, date_str: str) -> datetime:
        return datetime.strptime(date_str, self.dt_format)

    def format_utc_datetime(self, dt: datetime) -> str:
        """Formats a datetime as a UTC ISO 8601 string. It accepts a `datetime` that has a UTC timezone, or that has no
        timezone but is implicitly UTC, and returns a ISO 8601 string with the `Z` suffix. (`datetime.isoformat()`
        does not support the `Z` suffix).

        If the datetime has a non-UTC timezone associated with it, this function raises an exception.

        :param dt: a timezone-agnostic or UTC datetime
        :return: an ISO 8601 datetime string
        """
        if dt.tzinfo and dt.tzinfo != timezone.utc:
            raise ValueError('Non-UTC datetime provided, cannot format')
        return dt.strftime(self.dt_format)


class DateFormatter:
    """ DateFormatter converts string that are expected to be in ISO 8601 date format to a Date object and vice versa.
    """
    def __init__(self, d_format: str):
        self.d_format = d_format

    def date_to_str(self, d: date) -> str:
        """ Parses a given Date object into a ISO 8601 Date string: YYYY-MM-DD.

        :param d: Date object to be converted into a string
        :return: String representing the datetime in ISO 8601 date format
        """
        return d.strftime(self.d_format)

    def str_to_date(self, date_str: str) -> date:
        """ Parses a given date string of the format YYYY-MM-DD into a Date object.

        :param date_str: String representing a Georgian date
        :return: Date object that the string represents
        """
        return datetime.strptime(date_str, self.d_format).date()


UTC_FORMATTER = TimeFormatter("%Y-%m-%dT%H:%M:%SZ")
DATE_FORMATTER = DateFormatter("%Y-%m-%d")
