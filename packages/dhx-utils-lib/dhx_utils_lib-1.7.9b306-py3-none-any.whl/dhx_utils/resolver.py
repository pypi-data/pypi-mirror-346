"""
Copyright (c) 2021 RoZetta Technology Pty Ltd. All rights reserved.
"""
from urllib.parse import urlparse
from retrying import retry
import dns.resolver

MAX_RETRIES = 1  # retry only one time for less latency
MIN_WAIT_BEFORE_RETRY = 1000
MAX_WAIT_BEFORE_RETRY = 2000


def is_dns_timeout(exception):
    """
    Check the exception types matching DNS Timeout failure.
    """
    if isinstance(exception, dns.resolver.Timeout):
        return True
    return False


@retry(retry_on_exception=is_dns_timeout,
       stop_max_attempt_number=MAX_RETRIES,
       wait_random_min=MIN_WAIT_BEFORE_RETRY,
       wait_random_max=MAX_WAIT_BEFORE_RETRY)
def resolve_for_cname(source_domain: str) -> str:
    """ Resolve source domain for CNAME record

    :param source_domain: domain to be resovled
    :return: domain in the cname record
    """
    result = dns.resolver.query(source_domain, 'CNAME')
    # Maximum one record for CNAME, index out of bound error if empty
    return result[0].to_text()


def resolve_url(source_url: str) -> str:
    """ Resolve the netloc for the url, keep scheme and path unchanged

    :param source_url: url to be resolved
    :return: resolved url
    """
    parsed = urlparse(source_url)
    port = f":{parsed.port}" if parsed.port else ""
    return f'{parsed.scheme}://{dns.resolver.canonical_name(parsed.hostname).to_text()}{port}{parsed.path}'
