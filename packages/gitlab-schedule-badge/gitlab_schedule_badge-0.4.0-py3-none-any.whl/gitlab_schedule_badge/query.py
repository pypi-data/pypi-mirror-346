# SPDX-License-Identifier: BSD-2-Clause
# Copyright jdknight

from __future__ import annotations
from gitlab_schedule_badge.pipeline_schedule import PipelineSchedule
from gitlab_schedule_badge.pipeline_schedule import PipelineScheduleStatus
from requests import HTTPError
from requests import JSONDecodeError
from string import digits
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from requests.models import Response
    from gitlab_schedule_badge.rest import Rest


def query_project_id(api: Rest, project_namespace: str) -> int:
    rsp = _get(
        api,
        f'projects/{project_namespace}',
    )

    try:
        data = rsp.json()
    except JSONDecodeError as e:
        raise QueryError(502, 'invalid json response') from e

    project_id = data.get('id')
    if not project_id:
        raise QueryError(502, 'missing project identifier')

    return project_id


def query_pipeline_schedules(api: Rest, project_id: int) \
        -> list[PipelineSchedule]:
    rsp = _get(
        api,
        f'projects/{project_id}/pipeline_schedules',
        params={
            'scope': 'active',
        },
    )

    try:
        data = rsp.json()
    except JSONDecodeError as e:
        raise QueryError(502, 'invalid json response') from e

    # populate a list of pipeline schedules we need to query
    pipeline_schedules = []
    for schedule in data:
        # ignore any non-id'ed entries (should not happen)
        sid = schedule.get('id')
        if not sid:
            continue

        pipeline_desc = schedule.get('description')
        pipeline_schedules.append(
            PipelineSchedule(project_id, sid, desc=pipeline_desc))

    return pipeline_schedules


def query_pipeline_schedule(api: Rest, schedule: PipelineSchedule) \
        -> tuple[PipelineScheduleStatus, str, str]:
    rsp = _get(
        api,
        f'projects/{schedule.pid}/pipeline_schedules/{schedule.sid}',
    )

    try:
        data = rsp.json()
    except JSONDecodeError as e:
        raise QueryError(502, 'invalid json response') from e

    status = PipelineScheduleStatus.NONE
    desc = data.get('description', '')
    web_url = ''

    # check if we have a pipeline status (might not if never run)
    last_pipeline = data.get('last_pipeline')
    if last_pipeline:
        status_raw = last_pipeline.get('status')
        if not status_raw:
            raise QueryError(502, 'missing pipeline status')

        try:
            status = PipelineScheduleStatus(status_raw)
        except ValueError as e:
            raise QueryError(502, 'invalid pipeline status') from e

        # note: not worried if the web-url is not available
        web_url = last_pipeline.get('web_url', '')

    return status, desc, web_url


def _get(api: Rest, path: str, params: dict | None = None) -> Response:
    try:
        rsp = api.get(path, params=params)
        rsp.raise_for_status()
    except HTTPError as e:
        match e.response.status_code:
            # unknown -- either project does not exist or API key does not
            # have access to query this project
            case 404:
                return_code = 404

            # if a connection fails when querying, report the service not
            # being available
            case 408:
                return_code = 503

            # for all other errors, return a server error
            case _:
                return_code = 500

        try:
            # gitlab may provide messages like this:
            #  {'message': '404 Project Not Found'}          noqa=ERA001
            msg = rsp.json().get('message', '')

            # remove any error code added in the message
            msg = msg.lstrip(digits).strip()
        except JSONDecodeError:
            msg = ''

        raise QueryError(return_code, msg, code=e.response.status_code) from e

    return rsp


class QueryError(Exception):
    def __init__(self,
                # the code to return back to the client
                return_code: int,
                # any helpful message related to this exception
                msg: str,
                # the code reported by gitlab on the api request
                code: int | None = None,
            ) -> None:
        super().__init__(f'{msg}' if msg else f'GitLab reports code: {code}')
        self.gitlab_code = code
        self.return_code = return_code
