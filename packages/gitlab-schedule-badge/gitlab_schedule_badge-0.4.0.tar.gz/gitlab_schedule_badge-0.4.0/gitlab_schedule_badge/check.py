# SPDX-License-Identifier: BSD-2-Clause
# Copyright jdknight

from __future__ import annotations
from gitlab_schedule_badge.log import err
from gitlab_schedule_badge.log import log
from gitlab_schedule_badge.log import verbose
from gitlab_schedule_badge.log import success
from gitlab_schedule_badge.log import warn
from requests.exceptions import HTTPError


def perform_api_check(rest_clients: dict) -> None:
    """
    perform an api check

    Using the provided configuration, cycle through all configured instances
    and sanity check that we can query each one.

    Args:
        rest_clients: rest clients for each instance
    """

    failure = False

    for instance, rest in rest_clients.items():
        verbose(f'processing api-check for instance: {instance}')
        # GitLab: Version API
        # https://docs.gitlab.com/ee/api/version.html

        try:
            rsp = rest.get('version')
            rsp.raise_for_status()

            gitlab_version = rsp.json().get('version')
            if gitlab_version:
                log(f'verified api check to instance: {instance}')
            else:
                warn(f'unexpected response ({instance}): no version entry')
        except HTTPError as e:
            err(f'failed to query instance: {instance}\n {e}')
            failure = True

    if not failure:
        success('verified access to all gitlab instances!')
    else:
        if len(rest_clients) > 1:
            err('fail to access at least one gitlab instance')
        raise SystemExit(1)
