"""
Copyright (c) 2021 RoZetta Technology Pty Ltd. All rights reserved.
"""
from typing import Dict

import requests
from retrying import retry

from dhx_utils.errors import ServerError

MAX_RETRIES = 3
MIN_WAIT_BEFORE_RETRY = 1000
MAX_WAIT_BEFORE_RETRY = 2000

VALID_CODES = {requests.codes.ok, requests.codes.created}
TIMEOUT_CODES = {requests.codes.request_timeout, requests.codes.gateway_timeout}
INTERNAL_API_TIMEOUT = 30


class RequestTimeout(Exception):
    """Http Request Timeout"""


@retry(retry_on_exception=lambda e: isinstance(e, RequestTimeout),
       stop_max_attempt_number=MAX_RETRIES,
       wait_random_min=MIN_WAIT_BEFORE_RETRY,
       wait_random_max=MAX_WAIT_BEFORE_RETRY)
def requests_get(target_path: str, params: dict = None) -> dict:
    """ Get via requests

    :param target_path: the API endpoint url
    :param params: the parameters for the query
    :returns: The response in json
    :raises: ServerError when request exception
    """
    try:
        resp = requests.get(target_path, params=params, timeout=INTERNAL_API_TIMEOUT)
    except requests.exceptions.RequestException as e:
        raise ServerError(f'Error on getting {target_path}') from e
    if resp.status_code == requests.codes.ok:
        return resp.json()
    if resp.status_code in TIMEOUT_CODES:
        raise RequestTimeout('Request timeout, please retry again')
    raise ServerError(f'Error on GET: {target_path} with {resp.status_code}: {resp.json()}')


@retry(retry_on_exception=lambda e: isinstance(e, RequestTimeout),
       stop_max_attempt_number=MAX_RETRIES,
       wait_random_min=MIN_WAIT_BEFORE_RETRY,
       wait_random_max=MAX_WAIT_BEFORE_RETRY)
def requests_post(target_path: str, data: Dict = None) -> Dict:
    """ Submit a query POST request.
    If POST timed out, retry can be performed for additional query.

    :param target_path: The API path
    :param data: the payload for the post
    :returns: The response from the request.
    :raises: ServerError if request failed.
    """
    try:
        resp = requests.post(target_path, json=data, timeout=INTERNAL_API_TIMEOUT)
    except requests.exceptions.RequestException as e:
        raise ServerError(f'Failed to POST {target_path}') from e
    if resp.status_code in VALID_CODES:
        return resp.json()
    if resp.status_code in TIMEOUT_CODES:
        raise RequestTimeout('Request timeout, please retry again')
    raise ServerError(f'Error on POST: {target_path} with {resp.status_code}: {resp.json()}')
