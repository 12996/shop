from django.db import models


class Category(models.Model):
    STATUS_ENABLED = "enabled"
    STATUS_DISABLED = "disabled"

    STATUS_CHOICES = (
        (STATUS_ENABLED, "启用"),
        (STATUS_DISABLED, "禁用"),
    )

    name = models.CharField(max_length=50, unique=True)
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

    def __str__(self):
        return self.name


class Product(models.Model):
    STATUS_ON_SHELF = "on_shelf"
    STATUS_OFF_SHELF = "off_shelf"

    STATUS_CHOICES = (
        (STATUS_ON_SHELF, "上架"),
        (STATUS_OFF_SHELF, "下架"),
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
    )
    name = models.CharField(max_length=100)
    main_image = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_OFF_SHELF,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["id"]
        indexes = [
            models.Index(fields=["category"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return self.name

