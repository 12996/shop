from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_USER = "user"
    ROLE_MERCHANT = "merchant"
    STATUS_ENABLED = "enabled"
    STATUS_DISABLED = "disabled"

    ROLE_CHOICES = (
        (ROLE_USER, "普通用户"),
        (ROLE_MERCHANT, "商家"),
    )
    STATUS_CHOICES = (
        (STATUS_ENABLED, "启用"),
        (STATUS_DISABLED, "禁用"),
    )

    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    avatar = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_USER)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_ENABLED,
    )
    updated_at = models.DateTimeField(auto_now=True)

