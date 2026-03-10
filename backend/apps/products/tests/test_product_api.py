from django.test import TestCase
from rest_framework.test import APIClient

from apps.inventory.models import Stock
from apps.products.models import Category, Product


DEMO_PRODUCT_NAME = "\u7edf\u4e00\u51b0\u7ea2\u8336 500ml"


class ProductApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.drink_category = Category.objects.create(name="楗枡", sort_order=1)
        self.snack_category = Category.objects.create(name="闆堕", sort_order=2)

        self.cola = Product.objects.create(
            category=self.drink_category,
            name="鍙彛鍙箰 500ml",
            price="3.50",
            status=Product.STATUS_ON_SHELF,
        )
        Stock.objects.create(product=self.cola, quantity=10, alert_threshold=3)

        self.chips = Product.objects.create(
            category=self.snack_category,
            name="鍘熷懗钖墖",
            price="6.00",
            status=Product.STATUS_OFF_SHELF,
        )
        Stock.objects.create(product=self.chips, quantity=0, alert_threshold=3)

    def test_list_categories_returns_enabled_categories(self):
        response = self.client.get("/api/categories")

        self.assertEqual(response.status_code, 200)
        category_names = {item["name"] for item in response.json()}
        self.assertIn(self.drink_category.name, category_names)
        self.assertIn(self.snack_category.name, category_names)

    def test_list_products_only_returns_on_shelf_products(self):
        response = self.client.get("/api/products")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        product_names = {item["name"] for item in payload}
        self.assertIn("鍙彛鍙箰 500ml", product_names)
        self.assertNotIn("鍘熷懗钖墖", product_names)
        cola_payload = next(item for item in payload if item["id"] == self.cola.id)
        self.assertEqual(cola_payload["stock_quantity"], 10)

    def test_list_products_supports_category_filter_and_keyword_search(self):
        response = self.client.get("/api/products", {"category_id": self.drink_category.id, "keyword": "鍙箰"})

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertGreaterEqual(len(payload), 1)
        self.assertEqual(payload[0]["id"], self.cola.id)

    def test_product_detail_returns_stock_information(self):
        response = self.client.get(f"/api/products/{self.cola.id}")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["name"], "鍙彛鍙箰 500ml")
        self.assertEqual(payload["stock_quantity"], 10)

    def test_seeded_demo_products_are_visible_in_public_product_list(self):
        response = self.client.get("/api/products")

        self.assertEqual(response.status_code, 200)
        product_names = {item["name"] for item in response.json()}
        self.assertIn(DEMO_PRODUCT_NAME, product_names)

    def test_product_api_emits_request_and_response_logs(self):
        with self.assertLogs("apps.api", level="INFO") as captured:
            response = self.client.get("/api/products")

        self.assertEqual(response.status_code, 200)
        output = "\n".join(captured.output)
        self.assertIn("http_request", output)
        self.assertIn("http_response", output)
        self.assertIn("method=GET", output)
        self.assertIn("path=/api/products", output)
        self.assertIn("status_code=200", output)
