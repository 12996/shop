import logging
import os
from unittest import TestCase
from unittest.mock import patch

from django.test import Client, TestCase as DjangoTestCase


class RequestLoggingTest(DjangoTestCase):
    def setUp(self):
        self.client = Client()

    def test_health_endpoint_emits_request_and_response_logs(self):
        with self.assertLogs("apps.api", level="INFO") as captured:
            response = self.client.get("/health/")

        self.assertEqual(response.status_code, 200)
        output = "\n".join(captured.output)
        self.assertIn("http_request", output)
        self.assertIn("http_response", output)
        self.assertIn("path=/health/", output)
        self.assertIn("status_code=200", output)


class StartupLoggingTest(TestCase):
    def test_runserver_serving_process_emits_startup_log(self):
        from apps.common.apps import emit_startup_log

        environ = {"DJANGO_SETTINGS_MODULE": "config.settings", "RUN_MAIN": "true"}

        with self.assertLogs("apps.lifecycle", level="INFO") as captured:
            emit_startup_log(["manage.py", "runserver", "127.0.0.1:18000"], environ)

        output = "\n".join(captured.output)
        self.assertIn("django_startup", output)
        self.assertIn("bind=127.0.0.1:18000", output)
        self.assertIn("settings=config.settings", output)

    def test_parent_runserver_process_does_not_emit_startup_log(self):
        from apps.common.apps import emit_startup_log

        with patch.object(logging.getLogger("apps.lifecycle"), "info") as info_mock:
            emit_startup_log(
                ["manage.py", "runserver", "127.0.0.1:18000"],
                {"DJANGO_SETTINGS_MODULE": "config.settings"},
            )

        info_mock.assert_not_called()
