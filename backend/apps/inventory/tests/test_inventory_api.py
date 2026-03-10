from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from apps.inventory.models import Stock
from apps.products.models import Category, Product


class InventoryApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.merchant = get_user_model().objects.create_user(
            username="merchant_inventory",
            password="12345678",
            phone="13600000003",
            role="merchant",
        )
        category = Category.objects.create(name="闆堕")
        self.product = Product.objects.create(
            category=category,
            name="鍘熷懗钖墖",
            price="6.00",
            status=Product.STATUS_ON_SHELF,
        )
        self.stock = Stock.objects.create(
            product=self.product,
            quantity=4,
            alert_threshold=5,
        )

    def test_merchant_can_list_inventory(self):
        self.client.force_authenticate(user=self.merchant)

        response = self.client.get("/api/admin/inventory")

        self.assertEqual(response.status_code, 200)
        inventory_payload = next(item for item in response.data if item["product_id"] == self.product.id)
        self.assertEqual(inventory_payload["product_name"], "鍘熷懗钖墖")
        self.assertTrue(inventory_payload["is_alert"])

    def test_merchant_can_adjust_inventory(self):
        self.client.force_authenticate(user=self.merchant)

        response = self.client.post(
            f"/api/admin/inventory/{self.product.id}/adjust",
            {
                "quantity": 9,
                "remark": "鎵嬪姩琛ヨ揣",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["quantity"], 9)
        self.assertFalse(response.data["is_alert"])
