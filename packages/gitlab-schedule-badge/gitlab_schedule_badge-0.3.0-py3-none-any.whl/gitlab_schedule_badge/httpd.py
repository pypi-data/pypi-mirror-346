# SPDX-License-Identifier: BSD-2-Clause
# Copyright jdknight

from __future__ import annotations
from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
from flask.logging import default_handler
from gitlab_schedule_badge import __version__ as gitlab_schedule_badge_version
from gitlab_schedule_badge.cache import Cache
from gitlab_schedule_badge.defs import DEFAULT_IMAGE_CACHE_DURATION
from gitlab_schedule_badge.defs import QUERY_FAILED_COLOR
from gitlab_schedule_badge.pipeline_schedule import PipelineSchedule
from gitlab_schedule_badge.query import QueryError
from gitlab_schedule_badge.query import query_pipeline_schedule
from gitlab_schedule_badge.query import query_pipeline_schedules
from gitlab_schedule_badge.query import query_project_id
from gitlab_schedule_badge.theme import status2color
from gitlab_schedule_badge.util import build_badge_part
from gitlab_schedule_badge.util import decode_badge_part
from hashlib import sha256
from pathlib import Path
from pathlib import PurePosixPath
from pybadges2 import badge as build_badge
from typing import TYPE_CHECKING
from urllib.parse import quote as urlquote
from urllib.parse import urlparse

if TYPE_CHECKING:
    from flask import Response
    from gitlab_schedule_badge.state import State


def build_httpd(state: State) -> Flask:
    if not state.cfg:
        msg = 'No configuration setup before preparing application.'
        raise RuntimeError(msg)

    runtime_cfg = state.cfg

    # pre-build a series of badges
    ## when provided no or a bad badge identifier
    BADGE_INVALID_IDENTIFIER=build_badge(
        left_text='400',
        right_color='inactive',
        right_text='Invalid Identifier',
    )
    ## when provided a badge identifier for an instance not configured
    BADGE_UNSUPPORTED_INSTANCE=build_badge(
        left_text='404',
        right_color='inactive',
        right_text='Unknown Instance',
    )

    # determine seconds to force for non-erred badge images
    img_cache_age = runtime_cfg.cache_seconds() or DEFAULT_IMAGE_CACHE_DURATION

    # prepare a instance to manage caching badge statuses
    cache = Cache(img_cache_age, state.executor)

    # main flask application
    static_path = Path(__file__).parent / 'static'
    template_path = Path(__file__).parent / 'templates'

    app = Flask(
        __name__,
        static_folder=static_path,
        template_folder=template_path,
    )

    # support setting an explicit server name
    server_name = state.cfg.server_name()
    if server_name:
        app.config.update(
            SERVER_NAME=server_name,
        )

    # custom configuration to apply
    app.config.from_envvar('GSB_FLASK_CONFIG', silent=True)

    # disable the default handler; we do logging in our own way
    app.logger.removeHandler(default_handler)

    @app.route('/')
    def index() -> \
            str | Response | tuple[Response, int]:
        return render_template(
            'index.html',
            version=gitlab_schedule_badge_version,
        )

    @app.route('/badge/')
    @app.route('/badge/<path:bid>')
    @app.route('/badge/<path:bid>/')
    @app.route('/badge/<path:bid>/<path:text>')
    def badge(bid: str | None = None, text: str | None = None) -> \
            str | Response | tuple[Response, int]:
        if not bid:
            rsp = app.make_response(BADGE_INVALID_IDENTIFIER)
            rsp.headers.set('Content-Type', 'image/svg+xml')
            return rsp

        badge_details = decode_badge_part(bid)
        if not badge_details:
            rsp = app.make_response(BADGE_INVALID_IDENTIFIER)
            rsp.headers.set('Content-Type', 'image/svg+xml')
            return rsp

        instance, pid, sid = badge_details

        api = state.rest_clients.get(instance)
        if not api:
            rsp = app.make_response(BADGE_UNSUPPORTED_INSTANCE)
            rsp.headers.set('Content-Type', 'image/svg+xml')
            return rsp

        schedule = PipelineSchedule(pid, sid)
        pending_result = cache.fetch(api, schedule)

        try:
            status, desc, web_url = pending_result.result()
            schedule.description = desc
            schedule.status = status
            schedule.url = web_url
        except QueryError as exc:
            failed_query_badge=build_badge(
                left_text=str(exc.return_code),
                right_color=QUERY_FAILED_COLOR,
                right_text=str(exc),
            )

            rsp = app.make_response(failed_query_badge)
            rsp.headers.set('Content-Type', 'image/svg+xml')
            return rsp

        banner_text = text or schedule.description or 'Build'
        status_color = status2color(schedule.status)
        status_text = str(schedule.status)

        img_data = build_badge(
            left_text=banner_text,
            right_color=status_color,
            right_text=status_text,
        )

        rsp = app.make_response(img_data)
        rsp.headers.set('Content-Type', 'image/svg+xml')
        rsp.headers.set('ETag', sha256(img_data.encode('utf-8')).hexdigest())
        rsp.headers.set('Cache-Control', f'max-age={img_cache_age}, '
            'stale-while-revalidate={img_cache_age*2}')
        return rsp

    @app.route('/find', methods=['POST'])
    def find_project() -> \
            str | Response | tuple[Response, int]:
        content = request.get_json(silent=True)
        if not content:
            return jsonify({'message': 'Invalid request.'}), 400

        # verify the "url" looks like an expected gitlab project path
        instance_search_path = None
        project_url = content.get('url')
        if project_url:
            try:
                purl = urlparse(project_url)
            except ValueError:
                pass
            else:
                if purl.scheme and purl.path:
                    # extract the url path; we should have at least two parts;
                    # the group part(s) and the project part
                    full_path = PurePosixPath(purl.path)
                    dropped_project = full_path.parent

                    # and if the project was not empty, we should have both
                    # a possible group and project part; use the full path
                    # for the search attempt
                    if dropped_project != PurePosixPath('/'):
                        instance_search_path = full_path

        if not instance_search_path:
            return jsonify({'message': 'Invalid project URL.'}), 400

        # find an instance associated with the url provided by the user
        while True:
            check_path = f'{purl.scheme}://{purl.netloc}{instance_search_path}'
            instance = runtime_cfg.instance(check_path)
            if instance:
                break

            # if we are already at the end of our search, stop
            if instance_search_path == PurePosixPath('/') or \
                    instance_search_path == PurePosixPath('.'):
                break

            # if an instance could not be found, remove another (sub)group
            # and try again
            instance_search_path = instance_search_path.parent

        if not instance:
            return jsonify({'message': 'GitLab instance not configured.'}), 400

        # find the rest api client for this instance
        # (in theory, this should not fail)
        instance_key = check_path
        api = state.rest_clients.get(instance_key)
        if not api:
            return jsonify({'message': 'Instance REST-API failure.'}), 500

        # build a project namespace identifier; gitlab api supports using
        # a url-quoted full-name over a project identifier
        project_namespace = urlquote(str(full_path)[1:], safe='')

        # find any pipeline schedules for this project namespace
        try:
            project_id = query_project_id(api, project_namespace)
        except QueryError as exc:
            return jsonify({'message': str(exc)}), exc.return_code

        # find any pipeline schedules for this project namespace
        try:
            pipeline_schedules = query_pipeline_schedules(api, project_id)
        except QueryError as exc:
            return jsonify({'message': str(exc)}), exc.return_code

        # query GitLab for each pipeline's schedule state
        try:
            for entry in pipeline_schedules:
                status, _, web_url = query_pipeline_schedule(api, entry)
                entry.status = status
                entry.url = web_url
        except QueryError as exc:
            return jsonify({'message': str(exc)}), exc.return_code

        # build a response of each found pipeline schedule
        pipeline_schedules_entries: list[dict]
        pipeline_schedules_entries = []
        rsp = {
            'project': str(full_path)[1:],
            'schedules': pipeline_schedules_entries,
        }
        for entry in pipeline_schedules:
            badge_id = build_badge_part(instance_key, entry.pid, entry.sid)
            if not badge_id:
                continue

            pipeline_schedules_entries.append({
                'badge': badge_id,
                'badge_url': app.url_for('badge', _external=True) + badge_id,
                'description': entry.description,
                'pid': entry.pid,
                'sid': entry.sid,
                'status': entry.status,
                'url': entry.url,
            })

        return jsonify(rsp)

    # return the prepared flash application
    return app
