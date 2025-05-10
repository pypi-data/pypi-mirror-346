# SPDX-License-Identifier: BSD-2-Clause
# Copyright jdknight

from enum import StrEnum
from pathlib import Path
import sys

# list of support configuration names
if sys.platform != 'win32':
    SUPPORTED_CONFIG_NAMES = [
        Path('.gitlab-schedule-badge.toml'),
        Path('gitlab-schedule-badge.toml'),
        Path('/etc/gitlab-schedule-badge.toml'),
    ]
else:
    SUPPORTED_CONFIG_NAMES = [
        Path('.gitlab-schedule-badge.toml'),
        Path('gitlab-schedule-badge.toml'),
    ]

# the minimum cache window duration for internally cached images states
CACHE_WINDOW_MIN = 2

# the maximum cache window duration for internally cached image states
CACHE_WINDOW_MAX = 60

# expected section to parse configuration data in the toml file
CONFIG_BASE_SECTION = 'gitlab-schedule-badge'

# expected section to parse instance data in the toml file
CONFIG_INSTANCE_SECTION = 'gitlab-schedule-badge-instance'

# duration (in seconds) to hold the cache state of badges
DEFAULT_IMAGE_CACHE_DURATION = 10

# time (in seconds) for all requests
DEFAULT_REST_TIMEOUT = 10

# number of threads to allocate
DEFAULT_WORKER_THREADS = 8

# default api endpoint to use
GITLAB_DEFAULT_API_ENDPOINT = 'api/v4/'

# theme/color to apply when a query for a pipeline status has failed
QUERY_FAILED_COLOR = '#9b7d7d'


class CfgKey(StrEnum):
    """
    configuration keys

    Defines a series of attributes which define various keys used to hold
    various configuration values.

    Attributes:
        CACHE_SECONDS: the total time to permit caching data
        REVERSE_PROXY_CHAIN: number of reverse proxies in the request chain
        SERVER_NAME: the explicit server name the tool will be hosted on
        TIMEOUT: the timeout for all api requests
    """
    CACHE_SECONDS = 'cache-seconds'
    REVERSE_PROXY_CHAIN = 'reverse-proxy-chain'
    SERVER_NAME = 'server-name'
    TIMEOUT = 'timeout'


class InstanceKey(StrEnum):
    """
    instance configuration keys

    Defines a series of attributes which define various keys used to hold
    various instance-specific configuration values.

    Attributes:
        API_ENDPOINT_OVERRIDE: the api-endpoint to override (over `api/v4`)
        CA_CERTIFICATE: the ca certificate to use
        FQPN: the fully qualified project namespace
        IGNORE_TLS: whether to ignore tls certificate issues
        NAMESPACE: namespace a configuration entry is specific to
        SESSION_COOKIES: the session cookies to apply for all api requests
        SESSION_HEADERS: the session headers to apply for all api requests
        TOKEN: the token to use to query gitlab api
        URL: the gitlab instance url
    """
    API_ENDPOINT_OVERRIDE = 'api-endpoint-override'
    CA_CERTIFICATE = 'ca-certificate'
    FQPN = 'fqpn'
    IGNORE_TLS = 'ignore-tls'
    NAMESPACE = 'namespace'
    SESSION_COOKIES = 'session-cookies'
    SESSION_HEADERS = 'session-headers'
    TOKEN = 'token'  # noqa: S105
    URL = 'url'
