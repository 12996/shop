import logging
import time

from django.conf import settings
from django.middleware.csrf import CsrfViewMiddleware

from .origin import is_local_origin


logger = logging.getLogger("apps.api")


class LocalDevCsrfViewMiddleware(CsrfViewMiddleware):
    """Allow local origins in DEBUG mode while keeping default CSRF behavior."""

    def _origin_verified(self, request):
        if super()._origin_verified(request):
            return True

        if not settings.DEBUG:
            return False

        return is_local_origin(request.META.get("HTTP_ORIGIN", ""))


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        started_at = time.monotonic()
        self._log_request(request)

        try:
            response = self.get_response(request)
        except Exception:
            logger.exception(
                "http_exception method=%s path=%s user_id=%s query=%s",
                request.method,
                request.path,
                self._get_user_id(request),
                request.META.get("QUERY_STRING", ""),
            )
            raise

        self._log_response(request, response, started_at)
        return response

    def _log_request(self, request):
        logger.info(
            "http_request method=%s path=%s user_id=%s query=%s",
            request.method,
            request.path,
            self._get_user_id(request),
            request.META.get("QUERY_STRING", ""),
        )

    def _log_response(self, request, response, started_at):
        duration_ms = int((time.monotonic() - started_at) * 1000)
        logger.info(
            "http_response method=%s path=%s user_id=%s status_code=%s duration_ms=%s",
            request.method,
            request.path,
            self._get_user_id(request),
            response.status_code,
            duration_ms,
        )

    @staticmethod
    def _get_user_id(request):
        user = getattr(request, "user", None)
        if user is None or not getattr(user, "is_authenticated", False):
            return None
        return user.pk
