"""
Copyright (c) 2019-2020 RoZetta Technology Pty Ltd. All rights reserved.
"""
from datetime import datetime, date
import pytest

from dhx_utils.api import api_response, validate_allowed_parameters, get_optionals_parameters, get_event_parameter, \
    get_parameter, validate_mandatory_parameters
import dhx_utils.api
from dhx_utils.errors import APIError


# Verifies different combination of input argument does not throw an error.
@pytest.mark.parametrize(
    'payload, status_code, json_body',
    (
        ({'k1': 'v1'}, 200, '{"k1": "v1"}'),
        (None, 201, 'null'),
        ({}, 400, '{}'),
        ({'dt': date(2021, 12, 13)}, 200, '{"dt": "2021-12-13"}'),
        ({'dt': datetime(2021, 12, 13, 1, 2, 3)}, 200, '{"dt": "2021-12-13T01:02:03"}'),
    )
)
def test_api_response(payload, status_code, json_body):
    assert api_response(status_code, payload) == {'statusCode': status_code, 'body': json_body}


@pytest.mark.parametrize('params, name', (
        ({}, ''),
        ({}, 'field1'),
        ({'field1': 'value1'}, ''),
        ({'field1': None}, 'field1'),
))
def test_get_parameter_denied(params, name):
    with pytest.raises(APIError):
        get_parameter(params, name, '')


@pytest.mark.parametrize('params, name', (
        ({'field1': 'value1'}, 'field1'),
        ({'field1': 'value1', 'field2': 'value2'}, 'field1'),
        ({'field1': ''}, 'field1'),
))
def test_get_parameter_validated(params, name):
    get_parameter(params, name, '')


@pytest.mark.parametrize('event, name, expected', (
        ({'key': None}, 'key', {}),
        ({}, 'key', {}),
        ({'key': ''}, 'key', {}),
        ({'key': {'inner_key': 'inner_val'}}, 'key', {'inner_key': 'inner_val'}),
))
def test_get_event_parameter(event, name, expected):
    actual_results = get_event_parameter(event, name)
    assert actual_results == expected  # nosec - Assert_used rule applies only to non-test code, pytest recommends
    # using assert for testing purposes.


@pytest.mark.parametrize('params, optional_list, expected', (
        ({}, [], {}),
        ({}, ['key1', 'key2', 'key3'], {}),
        ({'key1': 'val1', 'key3': 'val3'}, ['key1', 'key2', 'key3'], {'key1': 'val1', 'key3': 'val3'}),
        ({'key1': 'val1', 'key2': 'val2'}, ['key3', 'key4'], {}),
))
def test_get_optionals_parameters(params, optional_list, expected):
    actual_results = get_optionals_parameters(params, optional_list)
    assert actual_results == expected  # nosec - Assert_used rule applies only to non-test code, pytest recommends
    # using assert for testing purposes.


@pytest.mark.parametrize('params, allowed_list', (
        ({'k1': 'v1'}, []),
        ({'k1': 'v1', 'k2': 'v2'}, ['k1']),
))
def test_validate_allowed_parameters_denied(params, allowed_list):
    with pytest.raises(APIError):
        validate_allowed_parameters(params, allowed_list)


@pytest.mark.parametrize('params, allowed_list', (
        ({}, []),
        ({'k1': 'v1'}, ['k1']),
))
def test_validate_allowed_parameters_validated(params, allowed_list):
    validate_allowed_parameters(params, allowed_list)


@pytest.mark.parametrize('params, mandatory_keys', (
        ({}, []),
        ({'k1': 'v1'}, []),
        ({'k1': 'v1'}, ['k1']),
        ({'k1': 'v1', 'k2': 'v2'}, ['k1']),
        ({'k1': 'v1', 'k2': 'v2'}, ['k1', 'k2']),
        ({'k1': 'v1', 'k2': ''}, ['k1', 'k2']),
))
def test_validate_mandatory_parameters_success(params, mandatory_keys):
    validate_mandatory_parameters(params, mandatory_keys)


@pytest.mark.parametrize('params, mandatory_keys', (
        ({}, ['k1']),
        ({'k1': 'v1', 'k2': 'v2'}, ['k3']),
        ({'k1': 'v1', 'k2': None}, ['k2']),
))
def test_validate_mandatory_parameters_forbidden(params, mandatory_keys):
    with pytest.raises(APIError):
        validate_mandatory_parameters(params, mandatory_keys)


def test_lambda_main_no_args(mocker):
    class TestException(Exception):
        pass
    mock_sys = mocker.patch("dhx_utils.api.sys")
    mock_sys.argv = ["app"]
    mock_sys.exit.side_effect = TestException

    with pytest.raises(TestException):
        dhx_utils.api.lambda_main(lambda evt: evt)
    mock_sys.exit.asset_called()


def test_lambda_main_with_payload(mocker):
    dummy_func = mocker.Mock()
    dummy_func.return_value = {'status': '200'}
    mock_sys = mocker.patch("dhx_utils.api.sys")
    mock_sys.argv = ["app", '{"dummy":"value"}']  # emulate command line args
    dhx_utils.api.lambda_main(dummy_func)

    # Expect the arg JSON payload to be passed to the dummy lambda handler and context is set to None
    dummy_func.asset_called_with({'dummy': 'value'}, None)
