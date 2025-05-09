"""
 Copyright (c) 2021 RoZetta Technology Pty Ltd. All rights reserved.
"""
import os
from typing import Any, Dict

import requests
from requests import Response
from dhx_utils.errors import ServerError
from dhx_utils.resolver import resolve_url
from dhx_utils.catalog.utils import requests_get, requests_post

HOSTED_ZONE = "datahex.internal"
CATALOG_API = "https://catalog.{ENVIRONMENT}.{HOSTED_ZONE}/{ENVIRONMENT}"


class CatalogService:

    INTERNAL_API_TIMEOUT = 30

    def __init__(self, catalog_api=None, env=None):
        self._catalog_url = catalog_api
        self._env = env or os.getenv("ENVIRONMENT")

    @property
    def catalog_url(self):
        if not self._catalog_url:
            catalog_api = os.getenv("CATALOG_API") \
                          or CATALOG_API.format(ENVIRONMENT=self._env, HOSTED_ZONE=HOSTED_ZONE)
            self._catalog_url = resolve_url(catalog_api)

        return self._catalog_url

    def get_sub_data_asset_locations(self, data_asset_id: str, start_date: str, end_date: str,
                                     partition: Dict[str, Any] = None):
        """ Get sub data asset locations for a given date range

        :param data_asset_id: the ID of data_asset
        :param start_date: the start date in YYYY-MM-DD format
        :param end_date: end date in YYYY-MM-DD format
        :param partition: optional dictionary of partition information
        :returns: The data_asset locations
        :raises: ServerError when request exception
        """
        data = {
            'data_asset_id': data_asset_id,
            'partition': partition,
            'start': start_date,
            'end': end_date
        }
        sda_locations_url = f'{self.catalog_url}/api/queries/sub_data_locations'

        response = requests_post(sda_locations_url, data=data)
        return [(result.get('partition_key'), result.get('location'))
                for result in response.get('results', {}).get('sub_data_locations', [])]

    def get_sub_data_asset_location(self, data_asset_id: str, period: str, partition: Dict[str, Any] = None):
        """Get the location from catalog API

        :param data_asset_id: uuid1 data asset id
        :param period: period eg 2021-12-31
        :param partition: optional dictionary of partition information
        :raises: ServerError when request exception
        """
        data = {
            'data_asset_id': data_asset_id,
            'period': period,
            'partition': partition
        }
        sda_location_url = f'{self.catalog_url}/api/queries/sub_data_location'
        return requests_post(
            sda_location_url,
            data=data
        ).get('results', {}).get('sub_data_location', {}).get('data_location')

    def get_data_asset_location(self, data_asset_id: str) -> str:
        """ Get the location from catalog API

        :param data_asset_id: uuid1 data asset id
        :return: the output location of the data asset
        :raises: ServerError
        """
        da_url = self.data_asset_url()
        data_asset_url = f'{da_url}/{data_asset_id}'
        return requests_get(data_asset_url).get('data_location')

    def data_asset_url(self) -> str:
        """
        Return the url to data_asset endpoint.
        """
        return f'{self.catalog_url}/api/data_assets'

    def sub_data_asset_url(self) -> str:
        """
        Return the url to data_asset endpoint.
        """
        return f'{self.catalog_url}/api/sub_data_assets'

    def get_data_asset(self, data_asset_id: str):
        """ Get details of data_asset

        :param data_asset_id: the ID of data_asset
        :returns: The response in json
        :raises: ServerError when request exception
        """
        da_url = self.data_asset_url()
        data_asset_url = f'{da_url}/{data_asset_id}'
        result = requests_get(data_asset_url)
        if not result:
            raise ServerError(f'No data_asset found on {data_asset_url}')
        return result

    def get_data_assets_by_asset_code(self, data_asset_code: str):
        """ Get details of all data assets with specified data asset code

        :param data_asset_code: the asset code of the data asset
        :returns: The response in json
        :raises: ServerError when request exception
        """
        da_url = self.data_asset_url()
        data_asset_query = f'{da_url}?data_asset_code={data_asset_code}'
        return requests_get(data_asset_query).get('data_assets')

    def get_data_assets_by_file_name(self, file_name: str):
        """ Get details of all data assets with a data location which matches the specified file name

        :param file_name: the file name to find the asset code(s) for
        :returns: The response in json
        :raises: ServerError when request exception
        """
        da_url = self.data_asset_url()
        data_asset_query = f'{da_url}?file_name={file_name}'
        return requests_get(data_asset_query).get('data_assets')

    def put_sub_data_asset(self, details: dict) -> Response:
        """ Put details of a sub data asset into the catalog
        :param details: subdata asset details
        :returns: request result dict
        :raises: ServerError
        """
        sda_url = self.sub_data_asset_url()
        return requests.post(sda_url, json=details, timeout=self.INTERNAL_API_TIMEOUT)

    def get_data_asset_schemas(self, data_asset_id: str, period: str):
        """ Get schemas of data_asset

        :param data_asset_id: the ID of data_asset
        :param period: the period of schema belongs to
        :returns: The data_asset schemas
        :raises: ServerError when request exception
        """
        params = {
            'status': 'active',
            'period': period
        }
        da_url = self.data_asset_url()
        data_asset_url = f'{da_url}/{data_asset_id}/schemas'
        return requests_get(data_asset_url, params=params)

    def download_data_asset_schema(self, schema_details: dict):
        """ Download schema

        :param schema_details: the dictionary of schema
        :returns: The schema
        :raises: ServerError when request exception
        """
        params = {
            'schema_id': schema_details['schema_id']
        }
        da_url = self.data_asset_url()
        download_schema_url = f"{da_url}/{schema_details['data_asset_id']}/schemas/download"
        result = requests_get(download_schema_url, params=params)
        if not result:
            raise ServerError(f'No data_asset schema found on {download_schema_url} with {params}')
        return result

    def get_dataset_assets(self, dataset_id: str) -> dict:
        """ Get list of assets in dataset

        :param dataset_id: the dataset to be queried
        :returns: The response in json
        :raises: ServerError when request exception
        """
        data_asset_query = f'{self.catalog_url}/api/datasets/{dataset_id}/data_assets'
        return requests_get(data_asset_query).get('data_assets')
