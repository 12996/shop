from django.contrib.auth import get_user_model
from rest_framework import authentication, exceptions


User = get_user_model()


class MockTokenAuthentication(authentication.BaseAuthentication):
    keyword = "Bearer"
    token_prefix = "mock-token-"

    def authenticate(self, request):
        authorization = authentication.get_authorization_header(request).decode("utf-8")
        if not authorization:
            return None

        parts = authorization.split()
        if len(parts) != 2 or parts[0] != self.keyword:
            return None

        token = parts[1]
        if not token.startswith(self.token_prefix):
            return None

        try:
            user_id = int(token.removeprefix(self.token_prefix))
        except ValueError as exc:
            raise exceptions.AuthenticationFailed("Invalid token.") from exc

        try:
            user = User.objects.get(pk=user_id, status=User.STATUS_ENABLED)
        except User.DoesNotExist as exc:
            raise exceptions.AuthenticationFailed("User not found.") from exc

        return (user, token)
