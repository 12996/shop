from django.db import migrations


SEED_CATEGORIES = [
    {
        "name": "\u5373\u996e\u996e\u54c1",
        "sort_order": 1,
        "status": "enabled",
    },
    {
        "name": "\u4f11\u95f2\u98df\u54c1",
        "sort_order": 2,
        "status": "enabled",
    },
    {
        "name": "\u5c45\u5bb6\u65e5\u7528",
        "sort_order": 3,
        "status": "enabled",
    },
]

SEED_PRODUCTS = [
    {
        "category": "\u5373\u996e\u996e\u54c1",
        "name": "\u7edf\u4e00\u51b0\u7ea2\u8336 500ml",
        "main_image": "demo/iced-tea.png",
        "description": "\u7ecf\u5178\u8336\u996e\uff0c\u9002\u5408\u7528\u4e8e\u5546\u54c1\u5c55\u793a\u4e0e\u4e0b\u5355\u6f14\u793a\u3002",
        "price": "4.00",
        "status": "on_shelf",
        "quantity": 25,
        "alert_threshold": 5,
    },
    {
        "category": "\u5373\u996e\u996e\u54c1",
        "name": "\u519c\u592b\u5c71\u6cc9 550ml",
        "main_image": "demo/water.png",
        "description": "\u5e38\u89c4\u996e\u7528\u6c34\uff0c\u7528\u4e8e\u6f14\u793a\u57fa\u7840\u5546\u54c1\u4fe1\u606f\u3002",
        "price": "2.00",
        "status": "on_shelf",
        "quantity": 40,
        "alert_threshold": 8,
    },
    {
        "category": "\u4f11\u95f2\u98df\u54c1",
        "name": "\u5965\u5229\u5965\u5939\u5fc3\u997c\u5e72",
        "main_image": "demo/oreo.png",
        "description": "\u5e38\u89c1\u96f6\u98df\uff0c\u5e93\u5b58\u8bbe\u7f6e\u4e3a\u9884\u8b66\u573a\u666f\u3002",
        "price": "6.50",
        "status": "on_shelf",
        "quantity": 2,
        "alert_threshold": 3,
    },
    {
        "category": "\u5c45\u5bb6\u65e5\u7528",
        "name": "\u7ef4\u8fbe\u62bd\u7eb8 3\u5305\u88c5",
        "main_image": "demo/tissue.png",
        "description": "\u5bb6\u5c45\u65e5\u7528\u5546\u54c1\uff0c\u9002\u5408\u6f14\u793a\u5206\u7c7b\u4e0e\u5546\u54c1\u7ef4\u62a4\u3002",
        "price": "12.90",
        "status": "on_shelf",
        "quantity": 12,
        "alert_threshold": 4,
    },
    {
        "category": "\u5373\u996e\u996e\u54c1",
        "name": "\u65e0\u7cd6\u82cf\u6253\u6c34 330ml",
        "main_image": "demo/soda-water.png",
        "description": "\u7528\u4e8e\u6f14\u793a\u4e0b\u67b6\u5546\u54c1\uff0c\u4e0d\u5728\u7528\u6237\u7aef\u5217\u8868\u4e2d\u5c55\u793a\u3002",
        "price": "5.50",
        "status": "off_shelf",
        "quantity": 6,
        "alert_threshold": 2,
    },
]

SEED_CATEGORY_NAMES = [item["name"] for item in SEED_CATEGORIES]
SEED_PRODUCT_NAMES = [item["name"] for item in SEED_PRODUCTS]


def seed_demo_products(apps, _schema_editor):
    Category = apps.get_model("products", "Category")
    Product = apps.get_model("products", "Product")
    Stock = apps.get_model("inventory", "Stock")

    categories = {}
    for category_data in SEED_CATEGORIES:
        category, _ = Category.objects.get_or_create(
            name=category_data["name"],
            defaults={
                "sort_order": category_data["sort_order"],
                "status": category_data["status"],
            },
        )
        categories[category.name] = category

    for product_data in SEED_PRODUCTS:
        product, created = Product.objects.get_or_create(
            name=product_data["name"],
            defaults={
                "category": categories[product_data["category"]],
                "main_image": product_data["main_image"],
                "description": product_data["description"],
                "price": product_data["price"],
                "status": product_data["status"],
            },
        )

        if created:
            Stock.objects.get_or_create(
                product=product,
                defaults={
                    "quantity": product_data["quantity"],
                    "alert_threshold": product_data["alert_threshold"],
                },
            )
            continue

        Stock.objects.get_or_create(
            product=product,
            defaults={
                "quantity": product_data["quantity"],
                "alert_threshold": product_data["alert_threshold"],
            },
        )


def unseed_demo_products(apps, _schema_editor):
    Category = apps.get_model("products", "Category")
    Product = apps.get_model("products", "Product")
    Stock = apps.get_model("inventory", "Stock")

    Stock.objects.filter(product__name__in=SEED_PRODUCT_NAMES).delete()
    Product.objects.filter(name__in=SEED_PRODUCT_NAMES).delete()

    for category_name in SEED_CATEGORY_NAMES:
        category = Category.objects.filter(name=category_name).first()
        if category is not None and not category.products.exists():
            category.delete()


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0001_initial"),
        ("inventory", "0002_initial"),
    ]

    operations = [
        migrations.RunPython(seed_demo_products, unseed_demo_products),
    ]
