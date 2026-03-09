from django.conf import settings
from django.db import models

from apps.products.models import Product


class Announcement(models.Model):
    STATUS_DRAFT = "draft"
    STATUS_PUBLISHED = "published"

    STATUS_CHOICES = (
        (STATUS_DRAFT, "草稿"),
        (STATUS_PUBLISHED, "已发布"),
    )

    title = models.CharField(max_length=100)
    content = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_DRAFT,
    )
    publisher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="announcements",
    )
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at", "-id"]
        indexes = [
            models.Index(fields=["status"]),
        ]


class Recommendation(models.Model):
    STATUS_ENABLED = "enabled"
    STATUS_DISABLED = "disabled"

    STATUS_CHOICES = (
        (STATUS_ENABLED, "启用"),
        (STATUS_DISABLED, "禁用"),
    )

    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name="recommendation",
    )
    sort_order = models.IntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_ENABLED,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "id"]
        indexes = [
            models.Index(fields=["sort_order"]),
        ]

