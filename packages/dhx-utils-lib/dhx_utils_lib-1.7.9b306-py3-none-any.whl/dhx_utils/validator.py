"""
Copyright (c) 2019-2020 RoZetta Technology Pty Ltd. All rights reserved.
"""
import re

# Source: https://www.oreilly.com/library/view/regular-expressions-cookbook/9781449327453/ch04s01.html
ADDRESS_PATTERN = re.compile(
    r"""[\w!#$%&'*+/=?`{|}~^-]+(?:\.[\w!#$%&'*+/=?`{|}~^-]+)*@
        (?:[A-Z0-9-]+\.)+[A-Z]{2,6}""", re.VERBOSE | re.IGNORECASE)


def is_valid_email(email_address: str):
    """
        This method performs a regex search against a pre-defined pattern to determine whether the supplied email
        address is valid.
    :param email_address: string representing an email address.
    :return: boolean indicating whether email passes regex validation.
    """
    return bool(re.search(ADDRESS_PATTERN, email_address))
