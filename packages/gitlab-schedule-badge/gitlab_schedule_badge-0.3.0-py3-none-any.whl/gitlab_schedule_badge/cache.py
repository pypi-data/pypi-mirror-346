# SPDX-License-Identifier: BSD-2-Clause
# Copyright jdknight

from __future__ import annotations
from functools import lru_cache
from gitlab_schedule_badge.defs import CACHE_WINDOW_MAX
from gitlab_schedule_badge.defs import CACHE_WINDOW_MIN
from gitlab_schedule_badge.query import query_pipeline_schedule
from typing import TYPE_CHECKING
import time

if TYPE_CHECKING:
    from concurrent.futures import Future
    from concurrent.futures import ThreadPoolExecutor
    from gitlab_schedule_badge.pipeline_schedule import PipelineSchedule
    from gitlab_schedule_badge.rest import Rest


class Cache:
    def __init__(self, img_maxage: int, executor: ThreadPoolExecutor) -> None:
        self.executor = executor
        self.window = max(CACHE_WINDOW_MIN, min(img_maxage, CACHE_WINDOW_MAX))

    def fetch(self, api: Rest, schedule: PipelineSchedule) -> Future:
        return _cache(self.executor, api, schedule, _cache_ttl(self.window))


# prepare a caching call to limit querying the same badge status over
# a configured amount of time (ttl-like; more so windowed)
@lru_cache
def _cache(executor: ThreadPoolExecutor, api: Rest,
        schedule: PipelineSchedule, ttl: int) -> Future:  # noqa: ARG001
    return executor.submit(query_pipeline_schedule, api, schedule)


# defines the ttl cycle for a cache window
def _cache_ttl(secs: int) -> int:
    return round(time.time() / secs)
