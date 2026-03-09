from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from apps.content.models import Announcement, Recommendation
from apps.orders.models import Order, OrderItem
from apps.products.models import Category, Product


class ContentApiTest(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        self.merchant = get_user_model().objects.create_user(
            username="merchant_user",
            password="12345678",
            phone="13600000000",
            role="merchant",
        )
        category = Category.objects.create(name="乳品")
        self.product = Product.objects.create(
            category=category,
            name="纯牛奶",
            price="5.00",
            status=Product.STATUS_ON_SHELF,
        )

    def test_home_returns_latest_announcement_and_recommendations(self):
        response = self.api_client.get("/api/home")

        self.assertEqual(response.status_code, 200)
        self.assertIn("announcement", response.data)
        self.assertIn("recommendations", response.data)

    def test_merchant_can_list_announcements(self):
        Announcement.objects.create(
            title="今日促销",
            content="部分商品限时优惠",
            status=Announcement.STATUS_PUBLISHED,
            publisher=self.merchant,
        )
        self.api_client.force_authenticate(user=self.merchant)

        response = self.api_client.get("/api/admin/announcements")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "今日促销")

    def test_merchant_can_create_announcement(self):
        self.api_client.force_authenticate(user=self.merchant)

        response = self.api_client.post(
            "/api/admin/announcements",
            {
                "title": "库存提醒",
                "content": "请及时补货",
                "status": Announcement.STATUS_PUBLISHED,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["title"], "库存提醒")

    def test_merchant_can_update_announcement(self):
        announcement = Announcement.objects.create(
            title="原公告",
            content="原内容",
            status=Announcement.STATUS_DRAFT,
            publisher=self.merchant,
        )
        self.api_client.force_authenticate(user=self.merchant)

        response = self.api_client.put(
            f"/api/admin/announcements/{announcement.id}",
            {
                "title": "新公告",
                "content": "新内容",
                "status": Announcement.STATUS_PUBLISHED,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "新公告")

    def test_merchant_can_delete_announcement(self):
        announcement = Announcement.objects.create(
            title="待删除公告",
            content="删除内容",
            status=Announcement.STATUS_DRAFT,
            publisher=self.merchant,
        )
        self.api_client.force_authenticate(user=self.merchant)

        response = self.api_client.delete(f"/api/admin/announcements/{announcement.id}")

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Announcement.objects.filter(id=announcement.id).exists())

    def test_merchant_can_list_recommendations(self):
        Recommendation.objects.create(
            product=self.product,
            sort_order=1,
            status=Recommendation.STATUS_ENABLED,
        )
        self.api_client.force_authenticate(user=self.merchant)

        response = self.api_client.get("/api/admin/recommendations")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["product"], self.product.id)

    def test_merchant_can_create_recommendation(self):
        self.api_client.force_authenticate(user=self.merchant)

        response = self.api_client.post(
            "/api/admin/recommendations",
            {
                "product": self.product.id,
                "sort_order": 2,
                "status": Recommendation.STATUS_ENABLED,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["product"], self.product.id)

    def test_merchant_can_update_recommendation(self):
        recommendation = Recommendation.objects.create(
            product=self.product,
            sort_order=1,
            status=Recommendation.STATUS_ENABLED,
        )
        self.api_client.force_authenticate(user=self.merchant)

        response = self.api_client.put(
            f"/api/admin/recommendations/{recommendation.id}",
            {
                "product": self.product.id,
                "sort_order": 5,
                "status": Recommendation.STATUS_DISABLED,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["sort_order"], 5)
        self.assertEqual(response.data["status"], Recommendation.STATUS_DISABLED)

    def test_merchant_can_delete_recommendation(self):
        recommendation = Recommendation.objects.create(
            product=self.product,
            sort_order=1,
            status=Recommendation.STATUS_ENABLED,
        )
        self.api_client.force_authenticate(user=self.merchant)

        response = self.api_client.delete(f"/api/admin/recommendations/{recommendation.id}")

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Recommendation.objects.filter(id=recommendation.id).exists())

    def test_merchant_can_get_statistics_overview(self):
        Order.objects.create(
            order_number="stats-order-001",
            user=self.merchant,
            total_amount="20.00",
            pay_amount="20.00",
            status=Order.STATUS_COMPLETED,
        )
        Order.objects.create(
            order_number="stats-order-002",
            user=self.merchant,
            total_amount="15.00",
            pay_amount="15.00",
            status=Order.STATUS_PAID,
        )
        self.api_client.force_authenticate(user=self.merchant)

        response = self.api_client.get("/api/admin/statistics/overview")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["order_count"], 2)
        self.assertEqual(response.data["completed_order_count"], 1)
        self.assertEqual(response.data["sales_amount"], "35.00")

    def test_merchant_can_get_hot_products(self):
        completed_order = Order.objects.create(
            order_number="stats-hot-001",
            user=self.merchant,
            total_amount="18.00",
            pay_amount="18.00",
            status=Order.STATUS_COMPLETED,
        )
        another_product = Product.objects.create(
            category=self.product.category,
            name="酸奶",
            price="8.00",
            status=Product.STATUS_ON_SHELF,
        )
        OrderItem.objects.create(
            order=completed_order,
            product_id=self.product.id,
            product_name=self.product.name,
            product_image=None,
            product_price="5.00",
            quantity=4,
            subtotal="20.00",
        )
        OrderItem.objects.create(
            order=completed_order,
            product_id=another_product.id,
            product_name=another_product.name,
            product_image=None,
            product_price="8.00",
            quantity=2,
            subtotal="16.00",
        )
        self.api_client.force_authenticate(user=self.merchant)

        response = self.api_client.get("/api/admin/statistics/hot-products")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["product_id"], self.product.id)
        self.assertEqual(response.data[0]["sales_count"], 4)
