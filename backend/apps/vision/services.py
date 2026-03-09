from apps.products.models import Category


def recognize_product(_image):
    category = Category.objects.order_by("id").first()

    return {
        "recognized_name": "示例商品",
        "recommended_category_id": category.id if category else None,
        "recommended_category_name": category.name if category else None,
        "confidence": "0.90",
    }
