from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from apps.inventory.models import Stock
from apps.orders.models import Order
from apps.products.models import Category, Product


class OrderFlowApiTest(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="order_user",
            password="12345678",
            phone="13700000000",
            role="user",
        )
        category = Category.objects.create(name="饮品")
        self.product = Product.objects.create(
            category=category,
            name="矿泉水",
            price="2.50",
            status=Product.STATUS_ON_SHELF,
        )
        Stock.objects.create(
            product=self.product,
            quantity=10,
            alert_threshold=3,
        )

    def test_submit_order_creates_pending_payment_order(self):
        self.api_client.force_authenticate(user=self.user)
        self.api_client.post(
            "/api/cart/items",
            {"product_id": self.product.id, "quantity": 2},
            format="json",
        )

        response = self.api_client.post("/api/orders", format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["status"], "pending_payment")

    def test_cancel_order_rolls_back_stock(self):
        self.api_client.force_authenticate(user=self.user)
        self.api_client.post(
            "/api/cart/items",
            {"product_id": self.product.id, "quantity": 2},
            format="json",
        )
        create_response = self.api_client.post("/api/orders", format="json")
        order = Order.objects.get(id=create_response.data["id"])

        stock = Stock.objects.get(product=self.product)
        self.assertEqual(stock.quantity, 8)

        response = self.api_client.post(f"/api/orders/{order.id}/cancel")

        self.assertEqual(response.status_code, 200)
        stock.refresh_from_db()
        order.refresh_from_db()
        self.assertEqual(order.status, Order.STATUS_CANCELLED)
        self.assertEqual(stock.quantity, 10)

    def test_pay_order_updates_status_to_paid(self):
        self.api_client.force_authenticate(user=self.user)
        self.api_client.post(
            "/api/cart/items",
            {"product_id": self.product.id, "quantity": 2},
            format="json",
        )
        create_response = self.api_client.post("/api/orders", format="json")
        order = Order.objects.get(id=create_response.data["id"])

        response = self.api_client.post(
            f"/api/orders/{order.id}/pay",
            {"payment_method": "wechat"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        order.refresh_from_db()
        self.assertEqual(order.status, Order.STATUS_PAID)
        self.assertEqual(response.data["status"], "paid")

    def test_list_orders_returns_current_user_orders(self):
        self.api_client.force_authenticate(user=self.user)
        self.api_client.post(
            "/api/cart/items",
            {"product_id": self.product.id, "quantity": 1},
            format="json",
        )
        self.api_client.post("/api/orders", format="json")

        response = self.api_client.get("/api/orders")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["status"], Order.STATUS_PENDING_PAYMENT)

    def test_get_order_detail_returns_current_user_order(self):
        self.api_client.force_authenticate(user=self.user)
        self.api_client.post(
            "/api/cart/items",
            {"product_id": self.product.id, "quantity": 1},
            format="json",
        )
        create_response = self.api_client.post("/api/orders", format="json")
        order_id = create_response.data["id"]

        response = self.api_client.get(f"/api/orders/{order_id}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], order_id)
        self.assertEqual(response.data["status"], Order.STATUS_PENDING_PAYMENT)


class AdminOrderApiTest(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username="admin_order_user",
            password="12345678",
            phone="13700000010",
            role="user",
        )
        self.merchant = user_model.objects.create_user(
            username="admin_order_merchant",
            password="12345678",
            phone="13700000011",
            role="merchant",
        )
        category = Category.objects.create(name="零食")
        self.product = Product.objects.create(
            category=category,
            name="饼干",
            price="6.50",
            status=Product.STATUS_ON_SHELF,
        )
        Stock.objects.create(
            product=self.product,
            quantity=12,
            alert_threshold=3,
        )

        self.api_client.force_authenticate(user=self.user)
        self.api_client.post(
            "/api/cart/items",
            {"product_id": self.product.id, "quantity": 2},
            format="json",
        )
        create_response = self.api_client.post("/api/orders", format="json")
        self.order_id = create_response.data["id"]
        self.api_client.post(
            f"/api/orders/{self.order_id}/pay",
            {"payment_method": Order.PAYMENT_WECHAT},
            format="json",
        )
        self.api_client.force_authenticate(user=self.merchant)

    def test_merchant_can_list_orders(self):
        response = self.api_client.get("/api/admin/orders")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.order_id)
        self.assertEqual(response.data[0]["status"], Order.STATUS_PAID)

    def test_merchant_can_get_order_detail(self):
        response = self.api_client.get(f"/api/admin/orders/{self.order_id}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], self.order_id)
        self.assertEqual(response.data["status"], Order.STATUS_PAID)

    def test_merchant_can_complete_paid_order(self):
        response = self.api_client.post(f"/api/admin/orders/{self.order_id}/complete")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], Order.STATUS_COMPLETED)

        order = Order.objects.get(id=self.order_id)
        self.assertEqual(order.status, Order.STATUS_COMPLETED)
