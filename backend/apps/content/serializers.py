from rest_framework import serializers

from .models import Announcement, Recommendation


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = (
            "id",
            "title",
            "content",
            "status",
            "published_at",
        )
        read_only_fields = ("id", "published_at")


class RecommendationSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_price = serializers.DecimalField(
        source="product.price",
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )
    product_image = serializers.CharField(source="product.main_image", read_only=True)

    class Meta:
        model = Recommendation
        fields = (
            "id",
            "sort_order",
            "status",
            "product",
            "product_name",
            "product_price",
            "product_image",
        )
