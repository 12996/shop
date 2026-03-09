from django.test import TestCase
from rest_framework.test import APIClient

from apps.inventory.models import Stock
from apps.products.models import Category, Product


class ProductApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.drink_category = Category.objects.create(name="饮料", sort_order=1)
        self.snack_category = Category.objects.create(name="零食", sort_order=2)

        self.cola = Product.objects.create(
            category=self.drink_category,
            name="可口可乐 500ml",
            price="3.50",
            status=Product.STATUS_ON_SHELF,
        )
        Stock.objects.create(product=self.cola, quantity=10, alert_threshold=3)

        self.chips = Product.objects.create(
            category=self.snack_category,
            name="原味薯片",
            price="6.00",
            status=Product.STATUS_OFF_SHELF,
        )
        Stock.objects.create(product=self.chips, quantity=0, alert_threshold=3)

    def test_list_categories_returns_enabled_categories(self):
        response = self.client.get("/api/categories")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_list_products_only_returns_on_shelf_products(self):
        response = self.client.get("/api/products")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(len(payload), 1)
        self.assertEqual(payload[0]["name"], "可口可乐 500ml")
        self.assertEqual(payload[0]["stock_quantity"], 10)

    def test_list_products_supports_category_filter_and_keyword_search(self):
        response = self.client.get("/api/products", {"category_id": self.drink_category.id, "keyword": "可乐"})

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(len(payload), 1)
        self.assertEqual(payload[0]["id"], self.cola.id)

    def test_product_detail_returns_stock_information(self):
        response = self.client.get(f"/api/products/{self.cola.id}")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["name"], "可口可乐 500ml")
        self.assertEqual(payload["stock_quantity"], 10)
