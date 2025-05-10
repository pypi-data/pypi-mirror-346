# SPDX-License-Identifier: BSD-2-Clause
# Copyright jdknight

from enum import StrEnum
from enum import auto


class PipelineSchedule:
    def __init__(self, pid: int, sid: int, desc: str = '') -> None:
        self.description = desc
        self.pid = pid
        self.sid = sid
        self.status = PipelineScheduleStatus.NONE
        self.url = ''

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PipelineSchedule):
            return NotImplemented

        return self.pid == other.pid and self.sid == other.sid

    def __hash__(self) -> int:
        return hash(f'{self.pid}-{self.sid}')

    def __repr__(self) -> str:
        return f'{self.pid}-{self.sid}: {self.status}'


class PipelineScheduleStatus(StrEnum):
    # gitlab pipeline statuses
    # See: https://docs.gitlab.com/ee/api/pipelines.html#list-project-pipelines
    CANCELED = auto()
    CREATED = auto()
    FAILED = auto()
    MANUAL = auto()
    PENDING = auto()
    PREPARING = auto()
    RUNNING = auto()
    SCHEDULED = auto()
    SKIPPED = auto()
    SUCCESS = auto()
    WAITING_FOR_RESOURCE = auto()
    # additional/custom entries
    NONE = auto()

    def __str__(self) -> str:
        match self.value:
            case PipelineScheduleStatus.CANCELED:
                return 'Canceled'
            case PipelineScheduleStatus.CREATED:
                return 'Created'
            case PipelineScheduleStatus.FAILED:
                return 'Failed'
            case PipelineScheduleStatus.MANUAL:
                return 'Manual'
            case PipelineScheduleStatus.NONE:
                return 'Never Run'
            case PipelineScheduleStatus.PENDING:
                return 'Pending'
            case PipelineScheduleStatus.PREPARING:
                return 'Preparing'
            case PipelineScheduleStatus.RUNNING:
                return 'Running'
            case PipelineScheduleStatus.SCHEDULED:
                return 'Scheduled'
            case PipelineScheduleStatus.SKIPPED:
                return 'Skipped'
            case PipelineScheduleStatus.SUCCESS:
                return 'Success'
            case PipelineScheduleStatus.WAITING_FOR_RESOURCE:
                return 'Waiting for resource'
            case _:
                return 'Unknown'
