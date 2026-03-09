from rest_framework import serializers

from .models import Stock


class StockSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source="product.id", read_only=True)
    product_name = serializers.CharField(source="product.name", read_only=True)
    category_name = serializers.CharField(source="product.category.name", read_only=True)
    product_status = serializers.CharField(source="product.status", read_only=True)
    is_alert = serializers.SerializerMethodField()

    class Meta:
        model = Stock
        fields = (
            "product_id",
            "product_name",
            "category_name",
            "product_status",
            "quantity",
            "alert_threshold",
            "is_alert",
            "updated_at",
        )

    def get_is_alert(self, obj):
        return obj.quantity <= obj.alert_threshold


class AdjustStockSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=0)
    remark = serializers.CharField(required=False, allow_blank=True, max_length=255)
