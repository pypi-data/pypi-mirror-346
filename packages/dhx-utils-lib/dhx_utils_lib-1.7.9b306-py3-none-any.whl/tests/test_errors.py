"""
Copyright (c) 2019-2020 RoZetta Technology Pty Ltd. All rights reserved.
"""
import pytest
from dhx_utils.errors import DataHexError, APIError, ParamError, \
    ForbiddenError, ResourceNotFound, ServerError, SQLExecutionError


@pytest.mark.parametrize(
    'exc, msg, code',
    (
        (ParamError, "bad params", 400),
        (APIError, "api error", 400),
        (ForbiddenError, "forbidden", 403),
        (ResourceNotFound, "not found", 404),
        (ServerError, "server error", 500),
        (SQLExecutionError, "db error", 500),
    )
)
def test_errors(exc, msg, code):
    def handler():
        try:
            raise exc(msg)  # simulate the error
        except DataHexError as e:
            return e.error_code, str(e)

    ret_code, ret_msg = handler()
    assert ret_code == code
    assert ret_msg == msg


def test_sensitive_errors():
    # DB error can contain sensitive info so check that we have a way to hide that.
    secret = "sensitive"
    try:
        raise SQLExecutionError(secret)
    except DataHexError as e:
        assert e.error_code == 500
        assert str(e) == secret
        assert e.error_message() != secret