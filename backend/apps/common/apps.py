import logging
import os
import sys

from django.apps import AppConfig


lifecycle_logger = logging.getLogger("apps.lifecycle")


def emit_startup_log(argv=None, environ=None):
    argv = argv or sys.argv
    environ = environ or os.environ

    if "runserver" not in argv:
        return

    if "--noreload" not in argv and environ.get("RUN_MAIN") != "true":
        return

    bind = "127.0.0.1:8000"
    runserver_index = argv.index("runserver")
    if runserver_index + 1 < len(argv) and not argv[runserver_index + 1].startswith("-"):
        bind = argv[runserver_index + 1]

    lifecycle_logger.info(
        "django_startup command=runserver bind=%s settings=%s debug=%s",
        bind,
        environ.get("DJANGO_SETTINGS_MODULE", ""),
        environ.get("DJANGO_DEBUG", "true"),
    )


class CommonConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.common"

    def ready(self):
        emit_startup_log()
