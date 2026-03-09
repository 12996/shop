from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from apps.inventory.models import Stock
from apps.orders.models import Order
from apps.products.models import Category, Product


class PermissionBoundaryTest(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        user_model = get_user_model()

        self.user = user_model.objects.create_user(
            username="permission_user",
            password="12345678",
            phone="13700000100",
            role="user",
        )
        self.other_user = user_model.objects.create_user(
            username="permission_other_user",
            password="12345678",
            phone="13700000101",
            role="user",
        )
        self.merchant = user_model.objects.create_user(
            username="permission_merchant",
            password="12345678",
            phone="13700000102",
            role="merchant",
        )

        category = Category.objects.create(name="权限测试分类")
        self.product = Product.objects.create(
            category=category,
            name="权限测试商品",
            price="9.90",
            status=Product.STATUS_ON_SHELF,
        )
        Stock.objects.create(product=self.product, quantity=20, alert_threshold=5)

        self.other_user_order = Order.objects.create(
            order_number="permission-order-001",
            user=self.other_user,
            total_amount="19.80",
            pay_amount="19.80",
            status=Order.STATUS_PENDING_PAYMENT,
        )

    def test_user_cannot_access_admin_api(self):
        self.api_client.force_authenticate(user=self.user)

        response = self.api_client.get("/api/admin/products")

        self.assertEqual(response.status_code, 403)

    def test_merchant_cannot_view_private_user_order_from_user_endpoint(self):
        self.api_client.force_authenticate(user=self.merchant)

        response = self.api_client.get(f"/api/orders/{self.other_user_order.id}")

        self.assertEqual(response.status_code, 404)

    def test_user_cannot_view_other_user_order(self):
        self.api_client.force_authenticate(user=self.user)

        response = self.api_client.get(f"/api/orders/{self.other_user_order.id}")

        self.assertEqual(response.status_code, 404)
