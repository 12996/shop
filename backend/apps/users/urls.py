from django.urls import path

from .views import (
    AvatarUploadView,
    CodeLoginView,
    PasswordLoginView,
    PasswordUpdateView,
    ProfileView,
    RegisterView,
)


urlpatterns = [
    path("register", RegisterView.as_view(), name="auth-register"),
    path("login/password", PasswordLoginView.as_view(), name="auth-login-password"),
    path("login/code", CodeLoginView.as_view(), name="auth-login-code"),
    path("profile", ProfileView.as_view(), name="auth-profile"),
    path("avatar", AvatarUploadView.as_view(), name="auth-avatar"),
    path("password", PasswordUpdateView.as_view(), name="auth-password"),
]
