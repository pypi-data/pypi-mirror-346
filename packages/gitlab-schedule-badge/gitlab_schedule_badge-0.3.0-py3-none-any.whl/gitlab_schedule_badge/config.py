# SPDX-License-Identifier: BSD-2-Clause
# Copyright jdknight

from __future__ import annotations
from gitlab_schedule_badge.defs import CONFIG_BASE_SECTION
from gitlab_schedule_badge.defs import CONFIG_INSTANCE_SECTION
from gitlab_schedule_badge.defs import CfgKey
from gitlab_schedule_badge.defs import InstanceKey
from gitlab_schedule_badge.defs import SUPPORTED_CONFIG_NAMES
from gitlab_schedule_badge.log import err
from gitlab_schedule_badge.log import verbose
from gitlab_schedule_badge.log import warn
from pathlib import Path
from typing import TYPE_CHECKING
from urllib.parse import urljoin
from urllib.parse import urlparse
import tomllib

if TYPE_CHECKING:
    from collections.abc import ValuesView
    from typing import Any


class Config:
    def __init__(self) -> None:
        """
        configuration instance

        Holds the extracted configuration information from a
        gitlab-schedule-badge TOML file.
        """
        self._config: dict[str, Any] = {}
        self._instances: dict[str, Any] = {}
        self.path: Path | None = None

    def load(self, path: Path) -> bool:
        """
        load configuration information from a provided file

        This call will open a TOML configuration file and populate various
        configuration options.

        Args:
            path: the path of the configuration file to load

        Returns:
            whether a file was loaded
        """

        self._config = {}
        self._instances = {}
        self.path = path

        try:
            verbose(f'attempting to load configuration file: {path}')
            with path.open('rb') as f:
                raw_config = tomllib.load(f)

                self._config = raw_config.get(CONFIG_BASE_SECTION, {})
                instances_cfg = raw_config.get(CONFIG_INSTANCE_SECTION, [])

                for key in self._config:
                    if CfgKey(key) not in CfgKey:
                        warn(f'unknown configuration key: {key}')

                for instance_cfg in instances_cfg:
                    instance_token = instance_cfg.get(InstanceKey.TOKEN, None)
                    instance_ns = instance_cfg.get(InstanceKey.NAMESPACE, '')
                    instance_url = instance_cfg.get(InstanceKey.URL, '')

                    instance_ns = instance_ns.strip('/')
                    instance_url = instance_url.strip('/')

                    if instance_url and instance_token:
                        instance_ref = f'{instance_url}/{instance_ns}'
                        instance_cfg[InstanceKey.FQPN] = instance_ref
                        if instance_ref in self._instances:
                            warn(f'overriding instance entry: {instance_ref}')
                        self._instances[instance_ref] = instance_cfg

                        for key in instance_cfg:
                            if InstanceKey(key) not in InstanceKey:
                                warn('unknown instance key '
                                    f'({instance_ref}): {key}')
                    else:
                        if not instance_url:
                            warn('ignoring instance entry with no url')
                        if not instance_token:
                            pf = f': {instance_url}' if instance_url else ''
                            warn(f'fignoring instance entry with no token{pf}')

                return True

        except tomllib.TOMLDecodeError as e:
            err(f'unable to load configuration file: {path}\n{e}')
        except FileNotFoundError:
            err(f'configuration file does not exist: {path}')
        except OSError as e:
            err(f'unable to load configuration file: {path}\n{e}')
        finally:
            self._finalize()

        return False

    def cache_seconds(self) -> int | None:
        """
        returns the configured cached duration (in seconds) value

        Returns:
            the cached duration value
        """
        raw_value = self._config.get(CfgKey.CACHE_SECONDS, None)
        if raw_value is None:
            return None

        try:
            parsed_value = int(raw_value)
        except ValueError:
            return None
        else:
            return parsed_value if parsed_value >= 0 else None

    def instance(self, path: str) -> dict | None:
        """
        returns the specific instance configuration registered

        Args:
            path: the instance path

        Returns:
            the instance configuration
        """
        raw_value = self._instances.get(path, None)
        if not raw_value:
            return None

        return raw_value

    def instances(self) -> ValuesView:
        """
        returns all registered instance configurations

        Returns:
            the instance configurations
        """
        return self._instances.values()

    def reverse_proxy_chain(self) -> int | None:
        """
        returns the configured reverse proxy chain count

        Returns:
            the reverse proxy chain count
        """
        raw_value = self._config.get(CfgKey.REVERSE_PROXY_CHAIN, None)
        if raw_value is None:
            return None

        try:
            parsed_value = int(raw_value)
        except ValueError:
            return None
        else:
            return parsed_value if parsed_value > 0 else None

    def server_name(self) -> str | None:
        """
        returns the configured server name value

        Returns:
            the server name value
        """
        raw_value = self._config.get(CfgKey.SERVER_NAME, None)
        if raw_value is None:
            return None

        server_name = raw_value.strip('/')

        parsed_server_name = None
        try:
            parsed_server_name = urlparse(server_name)
        except ValueError:
            err('(cfg) server-name is not a valid hostname(:port) value')
            return None
        else:
            # when parsed without a scheme, the hostname is parsed into the
            # scheme entry; and any port value goes into path
            if parsed_server_name.netloc:
                err('(cfg) server-name should not set scheme')
                return None

        return server_name

    def timeout(self) -> int | None:
        """
        returns the configured timeout value

        Returns:
            the timeout value
        """
        raw_value = self._config.get(CfgKey.TIMEOUT, None)
        if raw_value is None:
            return None

        try:
            parsed_value = int(raw_value)
        except ValueError:
            return None
        else:
            return parsed_value if parsed_value >= 1 else None

    def validate(self) -> bool:
        """
        validates required options for this configuration

        A subset of configuration options need to be set in order for the
        engine to operate as expected. For example, configuring the API
        credentials to interact with GitLab. This call will return whether
        the minimum configuration options has been set, and populate stderr
        with any detected issues.

        Returns:
            whether the configuration is valid
        """

        rv = True

        if self._instances:
            for entry in self._instances:
                instance_cfg = self._instances[entry]

                # validate url
                purl = None
                try:
                    purl = urlparse(entry)
                except ValueError:
                    err(f'(cfg) invalid url defined: {entry}')
                    rv = False
                else:
                    if purl.scheme not in ['http', 'https']:
                        scheme = purl.scheme if purl.scheme else '(none)'
                        err(f'(cfg) invalid schema ({entry}): {scheme}')
                        rv = False

                # validate api endpoint override
                aeo = instance_cfg.get(InstanceKey.API_ENDPOINT_OVERRIDE)
                if aeo and purl:
                    try:
                        urljoin(entry, aeo)
                    except TypeError:
                        err(f'(cfg) invalid api override ({entry}): {aeo}')
                        rv = False

                # validate ca certificate
                cert = instance_cfg.get(InstanceKey.CA_CERTIFICATE)
                if cert and not cert.exists():
                    err(f'(cfg) ca-certificate missing ({entry}): {cert}')
                    rv = False

                # validate session cookies
                cookies = instance_cfg.get(InstanceKey.SESSION_COOKIES)
                if cookies:
                    for cookie_name, cookie_value in cookies.items():
                        if not cookie_name:
                            err(f'(cfg) invalid cookie name ({entry})')
                            rv = False
                            break

                        if not cookie_value:
                            err(f'(cfg) invalid cookie value ({entry})')
                            rv = False
                            break

                # validate session headers
                headers = instance_cfg.get(InstanceKey.SESSION_HEADERS)
                if headers:
                    for header_name, header_value in headers.items():
                        if not header_name:
                            err(f'(cfg) invalid session header name ({entry})')
                            rv = False
                            break

                        if not header_value:
                            err(f'(cfg) invalid session header value ({entry})')
                            rv = False
                            break

                # validate token
                if not instance_cfg[InstanceKey.TOKEN].startswith('glpat-'):
                    warn(f'(cfg) token might be invalid ({entry}): '
                          'missing "glpat-" prefix')
        else:
            err('(cfg) no instances configured')
            rv = False

        return rv

    def _finalize(self) -> None:
        """
        finalize the internal configuration

        Updates the internal configuration from a load attempt to configured
        expected values for various types. For example, converting path-string
        entries to Paths.
        """

        def kentry_convert(cfg: dict, key: InstanceKey) -> None:
            original = cfg.get(key)
            if original:
                new_value = {}
                for entry in original:
                    entry_name = entry.get('name')
                    entry_value = entry.get('value')
                    new_value[entry_name] = entry_value

                cfg[key] = new_value

        for instance_cfg in self._instances.values():
            # ensure ca certificates are always Paths
            cert = instance_cfg.get(InstanceKey.CA_CERTIFICATE)
            if cert:
                instance_cfg[InstanceKey.CA_CERTIFICATE] = Path(cert)

            # ensure url and api-endpoint override ends with a forward flash
            instance_url = instance_cfg.get(InstanceKey.URL)
            if not instance_url.endswith('/'):
                instance_cfg[InstanceKey.URL] = f'{instance_url}/'

            aeo = instance_cfg.get(InstanceKey.API_ENDPOINT_OVERRIDE)
            if isinstance(aeo, str) and not aeo.endswith('/'):
                instance_cfg[InstanceKey.API_ENDPOINT_OVERRIDE] = f'{aeo}/'

            # ensure session cookies/headers are made into simple dictionaries
            kentry_convert(instance_cfg, InstanceKey.SESSION_COOKIES)
            kentry_convert(instance_cfg, InstanceKey.SESSION_HEADERS)

def find_configuration(path: Path) -> Path | None:
    """
    find a configuration in a provided path

    This call can be used to find an expected gitlab-schedule-badge
    configuration file in a provided path (of known default names). If no
    configuration file can be found, this call will return ``None``.

    Args:
        path: the path to search

    Returns:
        the configuration filename; otherwise ``None``
    """

    for fname in SUPPORTED_CONFIG_NAMES:
        cfg_file = path / fname
        if cfg_file.is_file():
            return cfg_file

    return None
