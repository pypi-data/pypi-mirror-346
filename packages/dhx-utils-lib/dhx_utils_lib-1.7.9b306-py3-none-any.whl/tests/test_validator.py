"""
Copyright (c) 2019-2020 RoZetta Technology Pty Ltd. All rights reserved.
"""
import pytest

from dhx_utils.validator import is_valid_email


# Test a small set of sample emails for validity
@pytest.mark.parametrize('email, expected', (
    ("test@gmail.com", True),
    ("o'connor@gmail.com", True),
    ("developers@rozettatech.com", True),
    ("", False),
    ("abc@@abc.com", False),
    ("developers@rozettatech", False),
))
def test_is_valid_email(email, expected):
    assert expected == is_valid_email(email)  # nosec - Assert_used rule applies only to non-test code, pytest
    # recommends using assert for testing purposes.
