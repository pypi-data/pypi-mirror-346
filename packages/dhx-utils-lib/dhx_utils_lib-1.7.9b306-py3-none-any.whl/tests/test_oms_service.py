import pytest
from dhx_utils.oms_service import OMSService


@pytest.fixture
def mock_resolve_url(mocker):
    mocked_resolve_url = mocker.patch("dhx_utils.oms_service.resolve_url", return_value="fake_url")
    return mocked_resolve_url


@pytest.fixture
def mock_request_get(mocker):
    mocked = mocker.patch("dhx_utils.oms_service.requests_get")
    return mocked


@pytest.fixture
def mock_os(mocker):
    mocked = mocker.patch("dhx_utils.oms_service.os")
    return mocked


def test_get_data_location(mock_os, mock_request_get, mock_resolve_url):
    OMSService().get_data_location_by_id("test_id")
    mock_request_get.assert_called_with("fake_url/api/data_locations/test_id")
