""" Copyright (c) 2021 RoZetta Technology Pty Ltd. All rights reserved."""
from datetime import datetime

import pytest
from dhx_utils.formatter import UTC_FORMATTER, DATE_FORMATTER


@pytest.mark.parametrize('dt_string, dt_expected', (
    ("2020-10-10T13:50:37Z", datetime(2020, 10, 10, 13, 50, 37)),
))
def test_datetime_formatter_str_to_date(dt_string, dt_expected):
    formatter = UTC_FORMATTER
    actual = formatter.str_to_date(dt_string)
    assert dt_expected == actual  # nosec - Assert_used rule applies only to non-test code, pytest


@pytest.mark.parametrize('dt_string', (
    ("2020-10-10T13:50:37"),
))
def test_datetime_formatter_str_to_date_missing_UTC_signature(dt_string):
    formatter = UTC_FORMATTER
    with pytest.raises(ValueError):
        formatter.str_to_date(dt_string)


@pytest.mark.parametrize('dt_string, dt_expected', (
    ("2020-10-10", datetime(2020, 10, 10, 0, 0, 0)),
))
def test_date_formatter_str_to_date(dt_string, dt_expected):
    formatter = DATE_FORMATTER
    actual = formatter.str_to_date(dt_string)
    assert actual == dt_expected.date()  # nosec - Assert_used rule applies only to non-test code, pytest


@pytest.mark.parametrize('dt_string', (
    "2020-10-10T13:50:37",
))
def test_date_formatter_str_to_date_incorrect_str_format(dt_string):
    # Throw Value error as datetime string provided instead of date string
    formatter = DATE_FORMATTER
    with pytest.raises(ValueError):
        formatter.str_to_date(dt_string)


@pytest.mark.parametrize('dt, dt_str_expected', (
    (datetime(2020, 10, 10, 0, 0, 0), "2020-10-10"),
))
def test_date_formatter_date_to_str(dt, dt_str_expected):
    formatter = DATE_FORMATTER
    actual = formatter.date_to_str(dt.date())
    assert actual == dt_str_expected  # nosec - Assert_used rule applies only to non-test code, pytest
