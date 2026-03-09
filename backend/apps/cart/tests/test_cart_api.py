from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.test import TestCase

from apps.products.models import Category, Product


class CartApiTest(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="cart_user",
            password="12345678",
            phone="13900000000",
            role="user",
        )
        category = Category.objects.create(name="零食")
        self.product = Product.objects.create(
            category=category,
            name="薯片",
            price="6.00",
            status=Product.STATUS_ON_SHELF,
        )

    def test_add_same_product_accumulates_quantity(self):
        self.api_client.force_authenticate(user=self.user)

        self.api_client.post(
            "/api/cart/items",
            {"product_id": self.product.id, "quantity": 1},
            format="json",
        )
        response = self.api_client.post(
            "/api/cart/items",
            {"product_id": self.product.id, "quantity": 2},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
