# SPDX-License-Identifier: BSD-2-Clause
# Copyright jdknight

from __future__ import annotations
from gitlab_schedule_badge.config import Config
from gitlab_schedule_badge.defs import InstanceKey
from gitlab_schedule_badge.defs import SUPPORTED_CONFIG_NAMES
from gitlab_schedule_badge.log import err
from gitlab_schedule_badge.rest import Rest
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from concurrent.futures import ThreadPoolExecutor
    from pathlib import Path


class State:
    def __init__(self, executor: ThreadPoolExecutor,
            cfg_file: Path | None = None) -> None:
        self.cfg: Config | None = None
        self.cfg_file = cfg_file
        self.executor = executor
        self.rest_clients: dict[str, Rest] = {}

    def setup(self) -> None:
        # if not configuration files, check for a default-named one
        if not self.cfg_file:
            new_cfg_file = None

            for default_cfg in SUPPORTED_CONFIG_NAMES:
                if default_cfg.is_file():
                    new_cfg_file = default_cfg
                    break

            if not new_cfg_file:
                err(f'missing configuration file: {default_cfg}')
                raise StateSetupError

            self.cfg_file = new_cfg_file

        # prepare configuration
        cfg = Config()
        if not cfg.load(self.cfg_file):
            raise StateSetupError

        if not cfg.validate():
            raise StateSetupError

        # prepare all rest clients
        for instance in cfg.instances():
            instance_ref = instance[InstanceKey.FQPN]
            self.rest_clients[instance_ref] = Rest(cfg, instance)

        self.cfg = cfg


class StateSetupError(Exception):
    pass
