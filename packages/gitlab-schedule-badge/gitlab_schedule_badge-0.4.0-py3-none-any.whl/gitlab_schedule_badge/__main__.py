# SPDX-License-Identifier: BSD-2-Clause
# Copyright jdknight

from concurrent.futures import ThreadPoolExecutor
from gitlab_schedule_badge import __version__ as gitlab_schedule_badge_version
from gitlab_schedule_badge.check import perform_api_check
from gitlab_schedule_badge.defs import DEFAULT_WORKER_THREADS
from gitlab_schedule_badge.httpd import build_httpd
from gitlab_schedule_badge.log import err
from gitlab_schedule_badge.log import gsb_log_configuration
from gitlab_schedule_badge.log import log
from gitlab_schedule_badge.log import verbose
from gitlab_schedule_badge.state import State
from gitlab_schedule_badge.win32 import enable_ansi_win32
from pathlib import Path
import argparse
import os
import sys


def main() -> None:
    """
    mainline

    The mainline for gitlab-schedule-badge.
    """

    try:
        parser = argparse.ArgumentParser(prog='gitlab-schedule-badge')
        parser.add_argument('--api-check', action='store_true',
            help='Perform an API check and exit')
        parser.add_argument('--config', '-C', type=Path,
            help='Configuration file to load')
        parser.add_argument('--development', action='store_true',
            help='Run the application in a development mode')
        parser.add_argument('--host',
            help='Host address to bind to')
        parser.add_argument('--port', type=int,
            help='Port to host on')
        parser.add_argument('--nocolorout', action='store_true',
            help='Explicitly disable colorized output')
        parser.add_argument('--verbose', '-V', action='store_true',
            help='Show additional messages')
        parser.add_argument('--version', '-v', action='version',
            version='%(prog)s ' + gitlab_schedule_badge_version)
        parser.add_argument('--workers', type=int,
            default=DEFAULT_WORKER_THREADS,
            help='Port to host on')
        args = parser.parse_args()

        # force color off if `NO_COLOR` is configured
        if os.getenv('NO_COLOR'):
            args.nocolorout = True

        # prepare logging
        gsb_log_configuration(nocolor=args.nocolorout, verbose_=args.verbose)

        # toggle on ansi colors by default for commands
        if not args.nocolorout:
            os.environ['CLICOLOR_FORCE'] = '1'

            # support character sequences (for color output on win32 cmd)
            if sys.platform == 'win32':
                enable_ansi_win32()

        # banner
        log('gitlab-schedule-badge {}', gitlab_schedule_badge_version)
        verbose('({})', __file__)

        # verify if a provided configuration exists
        cfg_file = args.config
        if cfg_file and not cfg_file.is_file():
            err(f'missing provided configuration file: {cfg_file}')
            raise SystemExit(1)

        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            state = State(executor, cfg_file=cfg_file)
            state.setup()

            # perform the api check; otherwise start the httpd server
            if args.api_check:
                perform_api_check(state.rest_clients)
            else:
                app = build_httpd(state)
                app.run(host=args.host, port=args.port, debug=args.development)

    except KeyboardInterrupt:
        print()


if __name__ == '__main__':
    main()
