"""
Copyright (c) 2019-2020 RoZetta Technology Pty Ltd. All rights reserved.
"""


class DataHexError(Exception):
    """ Base DataHex Error

    How to use:
    1. Use the `error_code` attribute an `error_message()` method to populate the API response.
    2. Use the `str()` on the error to get the raw error.

    For example:
    ```
    try:
        handle_your_methods()
        resp = api_response(200, {"results": "..."})
    except DataHexError as error:
        logger.error("Error: %s", str(error))  # log error
        resp = api_response(error.error_code, {"message": error.error_message()})  # return to caller
    ```
    """
    def __init__(self, error_code: int, message: str):
        super().__init__(message)
        self._error_code = error_code

    @property
    def error_code(self):
        return self._error_code

    def error_message(self):
        return str(self)


class APIError(DataHexError):
    """Invalid API Input Parameter error"""
    def __init__(self, message: str):
        super().__init__(400, message)

    def error_message(self):
        return f"Invalid request: {str(self)}"


class ParamError(DataHexError):
    """Invalid Input Parameter error"""
    def __init__(self, message: str):
        super().__init__(400, message)

    def error_message(self):
        return f"Invalid request parameters: {str(self)}"


class ForbiddenError(DataHexError):
    """The caller is forbidden from carrying out the operation"""
    def __init__(self, message: str):
        super().__init__(403, message)

    def error_message(self):
        return f"Request forbidden: {str(self)}"


class ResourceNotFound(DataHexError):
    """The requested resource is not found"""
    def __init__(self, message: str):
        super().__init__(404, message)

    def error_message(self):
        return f"Resource not found: {str(self)}"


class ServerError(DataHexError):
    """Something went wrong in the backend server, which is likely to lead to a 500 API response."""
    def __init__(self, message: str):
        super().__init__(500, message)

    def error_message(self):
        return f"Unexpected server error: {str(self)}"


class SQLExecutionError(DataHexError):
    """SQL Execution failed error"""
    def __init__(self, message: str):
        super().__init__(500, message)

    def error_message(self):
        # Note: the actual error is not returned to the caller to avoid information leakage.
        return "Unexpected database error"


# This error appears to be an odd one out so we will leave it out of the family tree of DataHex errors.
class DuplicateKeyError(Exception):
    """Failure because of duplicated key"""
