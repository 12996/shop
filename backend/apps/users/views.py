from django.contrib.auth import login
from rest_framework import permissions, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from apps.common.views import LoggedAPIView

from .serializers import (
    CodeLoginSerializer,
    PasswordLoginSerializer,
    PasswordUpdateSerializer,
    RegisterSerializer,
    UserSerializer,
)


def build_auth_payload(user):
    return {
        "token": f"mock-token-{user.pk}",
        "user": UserSerializer(user).data,
    }


class RegisterView(LoggedAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class PasswordLoginView(LoggedAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return Response(build_auth_payload(user))


class CodeLoginView(LoggedAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = CodeLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return Response(build_auth_payload(user))


class ProfileView(LoggedAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class AvatarUploadView(LoggedAPIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        avatar = request.data.get("avatar")
        if avatar is None:
            return Response({"detail": "未上传头像文件"}, status=status.HTTP_400_BAD_REQUEST)

        request.user.avatar = getattr(avatar, "name", str(avatar))
        request.user.save(update_fields=["avatar", "updated_at"])
        return Response(UserSerializer(request.user).data)


class PasswordUpdateView(LoggedAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        serializer = PasswordUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not request.user.check_password(serializer.validated_data["old_password"]):
            return Response({"detail": "旧密码错误"}, status=status.HTTP_400_BAD_REQUEST)

        request.user.set_password(serializer.validated_data["new_password"])
        request.user.save(update_fields=["password", "updated_at"])
        return Response(status=status.HTTP_204_NO_CONTENT)
