from rest_framework import serializers

from apps.inventory.models import Stock

from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "sort_order")


class ProductSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(source="category.id", read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)
    stock_quantity = serializers.IntegerField(source="stock.quantity", read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "category_id",
            "category_name",
            "name",
            "main_image",
            "description",
            "price",
            "status",
            "stock_quantity",
        )


class AdminProductSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(write_only=True)
    alert_threshold = serializers.IntegerField(write_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "category",
            "category_name",
            "name",
            "main_image",
            "description",
            "price",
            "status",
            "quantity",
            "alert_threshold",
        )

    def create(self, validated_data):
        quantity = validated_data.pop("quantity")
        alert_threshold = validated_data.pop("alert_threshold")
        product = Product.objects.create(**validated_data)
        Stock.objects.create(
            product=product,
            quantity=quantity,
            alert_threshold=alert_threshold,
        )
        return product

    def update(self, instance, validated_data):
        quantity = validated_data.pop("quantity")
        alert_threshold = validated_data.pop("alert_threshold")

        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()

        stock, _ = Stock.objects.get_or_create(product=instance)
        stock.quantity = quantity
        stock.alert_threshold = alert_threshold
        stock.save(update_fields=["quantity", "alert_threshold", "updated_at"])

        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        stock = Stock.objects.filter(product=instance).first()
        data["quantity"] = stock.quantity if stock else 0
        data["alert_threshold"] = stock.alert_threshold if stock else 0
        return data
