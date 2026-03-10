from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from apps.inventory.models import Stock
from apps.products.models import Category, Product


DEMO_PRODUCT_NAME = "\u7edf\u4e00\u51b0\u7ea2\u8336 500ml"


class AdminProductApiTest(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        self.merchant = get_user_model().objects.create_user(
            username="merchant_product",
            password="12345678",
            phone="13600000001",
            role="merchant",
        )
        self.category = Category.objects.create(name="\u996e\u6599")
        self.product = Product.objects.create(
            category=self.category,
            name="\u53ef\u53e3\u53ef\u4e50 500ml",
            price="3.50",
            status=Product.STATUS_OFF_SHELF,
        )
        Stock.objects.create(product=self.product, quantity=10, alert_threshold=3)

    def test_merchant_can_list_products(self):
        self.api_client.force_authenticate(user=self.merchant)

        response = self.api_client.get("/api/admin/products")

        self.assertEqual(response.status_code, 200)
        product_ids = {item["id"] for item in response.data}
        self.assertIn(self.product.id, product_ids)
        current_product = next(item for item in response.data if item["id"] == self.product.id)
        self.assertEqual(current_product["name"], "\u53ef\u53e3\u53ef\u4e50 500ml")
        self.assertEqual(current_product["quantity"], 10)

    def test_merchant_can_create_product_with_stock(self):
        self.api_client.force_authenticate(user=self.merchant)

        response = self.api_client.post(
            "/api/admin/products",
            {
                "category": self.category.id,
                "name": "\u96ea\u78a7 500ml",
                "main_image": "sprite.png",
                "description": "\u67e0\u6aac\u5473\u6c7d\u6c34",
                "price": "3.00",
                "status": Product.STATUS_ON_SHELF,
                "quantity": 20,
                "alert_threshold": 5,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], "\u96ea\u78a7 500ml")
        self.assertEqual(response.data["quantity"], 20)

    def test_merchant_can_update_product_and_stock(self):
        self.api_client.force_authenticate(user=self.merchant)

        response = self.api_client.put(
            f"/api/admin/products/{self.product.id}",
            {
                "category": self.category.id,
                "name": "\u53ef\u53e3\u53ef\u4e50 330ml",
                "main_image": "cola-330.png",
                "description": "\u5c0f\u89c4\u683c\u53ef\u4e50",
                "price": "2.50",
                "status": Product.STATUS_OFF_SHELF,
                "quantity": 8,
                "alert_threshold": 2,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "\u53ef\u53e3\u53ef\u4e50 330ml")
        self.assertEqual(response.data["quantity"], 8)
        self.assertEqual(response.data["alert_threshold"], 2)

    def test_merchant_can_on_shelf_product(self):
        self.api_client.force_authenticate(user=self.merchant)

        response = self.api_client.post(f"/api/admin/products/{self.product.id}/on_shelf")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], Product.STATUS_ON_SHELF)

    def test_merchant_can_off_shelf_product(self):
        self.product.status = Product.STATUS_ON_SHELF
        self.product.save(update_fields=["status", "updated_at"])
        self.api_client.force_authenticate(user=self.merchant)

        response = self.api_client.post(f"/api/admin/products/{self.product.id}/off_shelf")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], Product.STATUS_OFF_SHELF)

    def test_seeded_demo_products_are_visible_in_admin_product_list(self):
        self.api_client.force_authenticate(user=self.merchant)

        response = self.api_client.get("/api/admin/products")

        self.assertEqual(response.status_code, 200)
        product_names = {item["name"] for item in response.data}
        self.assertIn(DEMO_PRODUCT_NAME, product_names)
