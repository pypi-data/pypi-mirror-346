# SPDX-License-Identifier: BSD-2-Clause
# Copyright jdknight

from gitlab_schedule_badge.pipeline_schedule import PipelineScheduleStatus


def status2color(status: PipelineScheduleStatus) -> str:
    # See also: pybadge2's "_NAME_TO_COLOR" definition
    match status:
        case PipelineScheduleStatus.PENDING | \
             PipelineScheduleStatus.PREPARING | \
             PipelineScheduleStatus.RUNNING | \
             PipelineScheduleStatus.SCHEDULED | \
             PipelineScheduleStatus.WAITING_FOR_RESOURCE:
            return 'informational'

        case PipelineScheduleStatus.SUCCESS:
            return 'success'

        case PipelineScheduleStatus.FAILED:
            return 'critical'

        case PipelineScheduleStatus.CANCELED | \
             PipelineScheduleStatus.SKIPPED:
            return 'important'

        case PipelineScheduleStatus.CREATED | \
             PipelineScheduleStatus.MANUAL:
            return 'inactive'

        case _:
            return 'inactive'
