from rest_framework import serializers

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = (
            "id",
            "product_id",
            "product_name",
            "product_image",
            "product_price",
            "quantity",
            "subtotal",
        )


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "order_number",
            "user",
            "status",
            "total_amount",
            "pay_amount",
            "payment_method",
            "address_id",
            "address_snapshot",
            "created_at",
            "items",
        )
        extra_kwargs = {
            "user": {"read_only": True},
        }


class AdminOrderSerializer(OrderSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta(OrderSerializer.Meta):
        fields = (
            "id",
            "order_number",
            "user",
            "username",
            "status",
            "total_amount",
            "pay_amount",
            "payment_method",
            "address_id",
            "address_snapshot",
            "created_at",
            "items",
        )
