from rest_framework.permissions import BasePermission


class IsMerchant(BasePermission):
    message = "仅商家可访问该接口"

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and getattr(user, "role", None) == "merchant"
        )
