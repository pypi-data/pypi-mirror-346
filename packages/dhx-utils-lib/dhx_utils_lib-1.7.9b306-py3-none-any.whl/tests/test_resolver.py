"""
Copyright (c) 2021 RoZetta Technology Pty Ltd. All rights reserved.
"""
import uuid
import pytest

from dhx_utils.resolver import resolve_for_cname, resolve_url


@pytest.mark.parametrize('domain', (
    (uuid.uuid1().hex + ".datahex.internal"),
))
def test_resolve_for_cname(domain, mocker):
    resolver_mock = mocker.patch('dhx_utils.resolver.dns.resolver')
    result_domain = 'test.datahex.internal'
    result_domain_mock = mocker.Mock()
    result_domain_mock.to_text.return_value = result_domain
    resolver_mock.query.return_value = [result_domain_mock]
    assert resolve_for_cname(domain) == result_domain  # nosec - Assert_used rule applies only to non-test code,
    # pytest recommends using assert for testing purposes.
    resolver_mock.query.assert_called_with(domain, 'CNAME')


@pytest.mark.parametrize('source_url', (
    ('https://' + uuid.uuid1().hex + ".datahex.internal" + "/api/"),
))
def test_resolve_url(source_url, mocker):
    resolver_mock = mocker.patch('dhx_utils.resolver.dns.resolver')
    result_domain = 'test.datahex.internal'
    result_domain_mock = mocker.Mock()
    result_domain_mock.to_text.return_value = result_domain
    resolver_mock.canonical_name.return_value = result_domain_mock
    result_url = f'https://{result_domain}/api/'
    assert resolve_url(source_url) == result_url  # nosec - Assert_used rule applies only to non-test code,
