# SPDX-License-Identifier: BSD-2-Clause
# Copyright jdknight

from __future__ import annotations
from gitlab_schedule_badge import __version__ as gsb_version
from gitlab_schedule_badge.defs import InstanceKey
from gitlab_schedule_badge.defs import DEFAULT_REST_TIMEOUT
from gitlab_schedule_badge.defs import GITLAB_DEFAULT_API_ENDPOINT
from gitlab_schedule_badge.log import verbose
from requests import Session
from requests.adapters import HTTPAdapter
from typing import TYPE_CHECKING
from urllib.parse import urljoin
import ssl

if TYPE_CHECKING:
    from requests.models import Response
    from gitlab_schedule_badge.config import Config


class Rest:
    def __init__(self, cfg: Config, instance: dict) -> None:
        """
        a rest api client

        Defines a REST API client which can be used to perform GitLab API
        requests for a configured intsance.
        """
        api_endpoint_override = instance.get(InstanceKey.API_ENDPOINT_OVERRIDE)
        ca_certificate = instance.get(InstanceKey.CA_CERTIFICATE)
        ignore_tls = instance.get(InstanceKey.IGNORE_TLS)
        instance_url = instance.get(InstanceKey.URL)
        namespace = instance.get(InstanceKey.NAMESPACE)
        session_cookies = instance.get(InstanceKey.SESSION_COOKIES)
        session_headers = instance.get(InstanceKey.SESSION_HEADERS)
        token = instance.get(InstanceKey.TOKEN)

        if not instance_url:
            msg = 'invalid instance url'
            raise RuntimeError(msg)

        if api_endpoint_override:
            api_endpoint = api_endpoint_override
        else:
            api_endpoint = GITLAB_DEFAULT_API_ENDPOINT

        self.base_url = urljoin(instance_url, api_endpoint)
        self.instance_url = instance_url
        self.namespace = f'; {namespace}' if namespace else ''
        self.timeout = cfg.timeout() or DEFAULT_REST_TIMEOUT

        # build a session
        self.session = Session()
        self.session.headers.update({
            # explicit hint we only support json
            'Accept': 'application/json; charset=utf-8',
            # gitlab api token
            'Authorization': f'Bearer {token}',
            # notify instances what application is talking
            'User-Agent': f'GitLabScheduleBadge/{gsb_version}',
        })

        # append cookies (if any)
        if session_cookies:
            self.session.cookies.update(session_cookies)

        # append headers (if any)
        if session_headers:
            self.session.headers.update(session_headers)

        # configure users desire for certificates/verification
        if ca_certificate:
            self.session.verify = ca_certificate
        else:
            self.session.verify = not ignore_tls

        # register support for system certificates
        self.session.mount('https://', SystemCaCertificatesAdapter())

    def get(self, path: str, *, params: dict | None = None) -> Response:
        req_url = urljoin(self.base_url, path)
        verbose(f'(fetch{self.namespace}) {req_url}')

        return self.session.get(req_url, params=params)

    def close(self) -> None:
        if hasattr(self, 'session'):
            self.session.close()

    def __del__(self) -> None:
        self.close()


class SystemCaCertificatesAdapter(HTTPAdapter):
    """
    a system ca certificate requests adapter

    Provides an adapter which can be mounted into Requests to use
    Python's SSL library, which should help support local system CA
    certificates.
    """

    def init_poolmanager(self, *args: int, **kwargs: int) -> None:
        context = ssl.create_default_context()
        super().init_poolmanager(*args, **kwargs, ssl_context=context)
