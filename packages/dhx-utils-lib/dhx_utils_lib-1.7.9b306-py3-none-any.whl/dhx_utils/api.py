"""
Copyright (c) 2019-2020 RoZetta Technology Pty Ltd. All rights reserved.
"""
import sys
import dataclasses
from typing import List, Callable, Dict, Any, Tuple
from datetime import datetime, date
from enum import Enum
from sortedcontainers import SortedSet, SortedDict, SortedList
import simplejson as json
from dhx_utils.errors import APIError


def api_response(status_code: int, body: Any) -> dict:
    """ Return a standard API response to the caller that is compatible with AWS API Gateway, in the form:
        {
            "statusCode": xxx,
            "body": xxx
        }

    :param status_code: HTTP response code
    :param body: Body of the response
    :return: A standard API response {"statusCode: xxx, "body": json_body}
    """
    return {"statusCode": status_code, "body": json.dumps(body, cls=ExtendedJsonEncoder)}


class ExtendedJsonEncoder(json.JSONEncoder):  # pylint: disable=too-few-public-methods
    """ Extend the JSON decoder class so that json.dumps() knows how to encode additional classes into a JSON nodes.
    Additional JSON encoding support includes:
    - SortedSet
    - SortedDict
    - SortedList
    - dataclasses
    - datetime
    - date
    - Enum
    """

    def default(self, o):
        if isinstance(o, (SortedSet, SortedDict, SortedList)):
            return list(o)
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        if isinstance(o, Enum):
            return o.value
        if isinstance(o, (date, datetime)):
            return o.isoformat()
        return super().default(o)


def get_request_body(event: Dict[str, Any]) -> Dict:
    """ Extract the body of an API request and return that as a dict object.

    """
    try:
        request_body = json.loads(event.get('body') or '{}')
    except (TypeError, json.JSONDecodeError) as e:
        raise APIError("Invalid request body") from e
    return request_body


def get_parameter(params: dict, name: str, required_message: str = None) -> any:
    """ Retrieve a mandatory key from a dictionary, an APIError is raised if the key does not exist in the provided
        dictionary.

    :param params: The dictionary of parameters to get a value from.
    :param name: The name of the parameter to retrieve.
    :param required_message: The error message to display if the param is not found.
    :return: The value of the parameter retrieved
    """
    value = params.get(name)
    if value is None:
        message = f": {required_message}" if required_message else "."
        raise APIError(f"Missing parameter '{name}'{message}")
    return value


def get_event_parameter(event: dict, name: str) -> any:
    """ Helper function to get a parameter from a lambda event object.

    Annoyingly the event often contains the value 'None' when not provided, but the parameter will return the
    actual value 'None' rather than defaulting to {} when using event.get('name', {}').
    This function helps reduce code to a single line.

    :param event: Lambda event object
    :param name: Name of the param to return
    :return: A dictionary object for that param, or an empty dict if not found or None.
    """
    params = event.get(name)
    if not params:
        params = {}
    return params


def get_optionals_parameters(params: dict, optionals: List[str]) -> dict:
    """ Returns optional parameters given the full set of parameters.

    This function returns a dictionary where the keys of the input dictionary intersect with the elements in the
    provided optional list.
    :param params: The source parameters (i.e. lambda event object)
    :param optionals: A list of optional parameter names.
    :return: A dictionary containing optional parameters that were found in the source parameters.
             Or an empty dict if none is found.
    """
    results = {}
    for opt in optionals:
        if opt in params:
            results[opt] = params.get(opt)
    return results


def validate_allowed_parameters(params: dict, allowed: List[str]) -> None:
    """ Validate that only allowed parameters are provided.

    This function validates that only allowed params are provided. If an unknown parameter is found, an
    APIParameter exception is raised.

    :param params: The input parameters to check
    :param allowed: The array of allowed parameter names.
    :raises: APIError if unexpected params are found.
    """
    for key in params.keys():
        if key not in allowed:
            raise APIError(f"Unexpected parameter '{key}' detected.")


def validate_mandatory_parameters(params: dict, mandatory_keys: List[str]) -> None:
    """ To validate that mandatory params are provided. Additional parameters are ignored.

    :param params: The input parameters to check
    :param mandatory_keys: Mandatory keys that the parameters must contain.
    :raises: APIError if mandatory params are not provided.
    """

    missing_keys = [key for key in mandatory_keys if params.get(key) is None]

    if missing_keys:
        missing_fields = ', '.join(missing_keys)
        raise APIError(f"Missing mandatory configuration field(s): {missing_fields}")


def get_user_details(event: Dict[str, Any]) -> Tuple[str, str]:
    """Extract idp id and user name from headers (superceded by get_auth_details)
    """
    try:
        claims = json.loads(event.get('headers', {}).get('authorizer', '{}')).get('claims', {})
    except (TypeError, json.JSONDecodeError) as e:
        raise APIError('Invalid authorizer header') from e

    idp_id = claims.get('sub')
    username = claims.get('username')
    if (not idp_id) or (not username):
        raise APIError('Authentication information is missing')
    return idp_id, username


def get_auth_details(event: Dict[str, Any]) -> Dict[str, str]:
    """Extract idp id, groups, origin and user name from headers
    """
    headers = event.get('headers', {})
    try:
        claims = json.loads(headers.get('authorizer', '{}')).get('claims', {})
    except (TypeError, json.JSONDecodeError) as e:
        raise APIError('Invalid authorizer header') from e

    groups = claims.get('cognito:groups')
    return {
        'idp_id': claims.get('sub'),
        'groups': groups.split(',') if groups else [],
        'origin': headers.get('X-RZT-Origin'),
        'username': claims.get('username')
    }


def lambda_main(lambda_handler: Callable, raw: bool = False) -> None:
    """ Provides a simple lambda mainline entry point for testing lambda handlers.

    This function will automatically use the first argument passed in via sys.argv
    as the lambda event payload and prints the response from the lambda handler to
    stdout for testing and viewing. The function will also exit with non-zero if
    no arg have been pased in.

    :param lambda_handler: The lambda handler function to call from your mainline.
    :param raw: Print the results in raw form.
    """
    if not sys.argv or len(sys.argv) < 2:
        sys.exit("Lambda CLI expects 1 param for the payload")
    result = lambda_handler(json.loads(sys.argv[1]), None)
    print(result if raw else json.dumps(result))
