"""
 Copyright (c) 2022 RoZetta Technology Pty Ltd. All rights reserved.
"""
import os
from typing import Dict

from dhx_utils.errors import ServerError
from dhx_utils.resolver import resolve_url
from dhx_utils.catalog.utils import requests_post

OPS_API = "https://ops.{ENVIRONMENT}.{HOSTED_ZONE}/{ENVIRONMENT}"
HOSTED_ZONE = "datahex.internal"


class OPSService:
    """
        utils class for OPS services
    """
    def __init__(self, ops_api=None, env=None):
        self._ops_url = ops_api
        self._env = env or os.getenv("ENVIRONMENT")

    @property
    def ops_url(self):
        """Return resolved OPS URL if None
        :return: Resolved OPS URL
        """
        if not self._ops_url:
            ops_api = os.getenv("OPS_API") \
                          or OPS_API.format(ENVIRONMENT=self._env, HOSTED_ZONE=HOSTED_ZONE)
            self._ops_url = resolve_url(ops_api)

        return self._ops_url

    def record_data_staged(self, data_staged: Dict) -> Dict:
        """ Records data staged event

        :param details: data staged details
        :return: response
        """
        target_path = f'{self.ops_url}/api/data_staged'
        resp = requests_post(target_path, data_staged)
        if resp:
            return resp
        raise ServerError(f"Response Error calling {target_path}")
