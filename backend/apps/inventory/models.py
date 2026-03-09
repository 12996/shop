from django.conf import settings
from django.db import models

from apps.products.models import Product


class Stock(models.Model):
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name="stock",
    )
    quantity = models.IntegerField(default=0)
    alert_threshold = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["quantity"]),
        ]

    def __str__(self):
        return f"{self.product.name}: {self.quantity}"


class StockLog(models.Model):
    CHANGE_IN = "in"
    CHANGE_OUT = "out"
    CHANGE_ROLLBACK = "rollback"
    CHANGE_MANUAL = "manual"

    CHANGE_TYPE_CHOICES = (
        (CHANGE_IN, "入库"),
        (CHANGE_OUT, "出库"),
        (CHANGE_ROLLBACK, "回补"),
        (CHANGE_MANUAL, "人工调整"),
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="stock_logs",
    )
    change_type = models.CharField(max_length=20, choices=CHANGE_TYPE_CHOICES)
    change_amount = models.IntegerField()
    before_qty = models.IntegerField()
    after_qty = models.IntegerField()
    operator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="stock_logs",
    )
    remark = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-id"]

    def __str__(self):
        return f"{self.product.name}: {self.change_type}"
