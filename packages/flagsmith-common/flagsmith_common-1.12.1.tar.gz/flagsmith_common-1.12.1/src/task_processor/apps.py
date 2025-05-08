from django.apps import AppConfig
from django.conf import settings
from health_check.plugins import plugin_dir  # type: ignore[import-untyped]

from task_processor.task_run_method import TaskRunMethod


class TaskProcessorAppConfig(AppConfig):
    name = "task_processor"

    def ready(self) -> None:
        if (
            settings.ENABLE_TASK_PROCESSOR_HEALTH_CHECK
            and settings.TASK_RUN_METHOD == TaskRunMethod.TASK_PROCESSOR
        ):
            from .health import TaskProcessorHealthCheckBackend

            plugin_dir.register(TaskProcessorHealthCheckBackend)
