"""
 Copyright (c) 2022 RoZetta Technology Pty Ltd. All rights reserved.
"""
import os
from typing import Dict

from dhx_utils.errors import ServerError
from dhx_utils.resolver import resolve_url
from dhx_utils.catalog.utils import requests_get

OMS_API = "https://oms.{ENVIRONMENT}.{HOSTED_ZONE}/{ENVIRONMENT}"
HOSTED_ZONE = "datahex.internal"


class OMSService:
    """
        utils class for OMS services
    """
    def __init__(self, oms_api=None, env=None):
        self._oms_url = oms_api
        self._env = env or os.getenv("ENVIRONMENT")

    @property
    def oms_url(self):
        """Return resolved OMS URL if None
        :return: Resolved OMS URL
        """
        if not self._oms_url:
            oms_api = os.getenv("OMS_API") \
                          or OMS_API.format(ENVIRONMENT=self._env, HOSTED_ZONE=HOSTED_ZONE)
            self._oms_url = resolve_url(oms_api)

        return self._oms_url

    def get_data_location_by_id(self, data_location_id: str) -> Dict:
        """ Retrieves the Azure credentials from a data location using the data location API

        :param data_location_id: ID of the data_location to load from.
        :return: data location dictionary combining the secret stored in secret manager and data location db record
        """
        target_path = f'{self.oms_url}/api/data_locations/{data_location_id}'
        resp = requests_get(target_path)
        # data location response shouldn't be empty when status code == ok
        if resp:
            return resp
        raise ServerError(f"Response Error calling {target_path}")
