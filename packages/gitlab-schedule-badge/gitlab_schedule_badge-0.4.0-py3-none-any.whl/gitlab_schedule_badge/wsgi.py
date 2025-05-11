# SPDX-License-Identifier: BSD-2-Clause
# Copyright jdknight

from concurrent.futures import ThreadPoolExecutor
from flask import Flask
from gitlab_schedule_badge.httpd import build_httpd
from gitlab_schedule_badge.state import State
from werkzeug.middleware.proxy_fix import ProxyFix


def main() -> Flask:
    """
    mainline (wsgi)

    The mainline for gitlab-schedule-badge when managed by a web service.
    """
    executor = ThreadPoolExecutor()

    state = State(executor)
    state.setup()

    if not state.cfg:
        msg = 'Configuration not setup.'
        raise RuntimeError(msg)

    app = build_httpd(state)

    # if flagged behind a reverse proxy, register the proxy middleware to
    # ensure resources are properly referenced
    chain_count = state.cfg.reverse_proxy_chain()
    if chain_count:
        app.wsgi_app = ProxyFix(  # type: ignore[method-assign]
            app.wsgi_app,
            x_for=chain_count,
            x_host=chain_count,
            x_prefix=chain_count,
            x_proto=chain_count,
        )

    return app
