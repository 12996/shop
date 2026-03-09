from django.test import TestCase

from apps.inventory.models import Stock
from apps.products.models import Category, Product


class ProductStockModelTest(TestCase):
    def test_product_has_one_stock_record(self):
        category = Category.objects.create(name="饮料")
        product = Product.objects.create(
            category=category,
            name="可乐",
            price="3.50",
        )
        stock = Stock.objects.create(
            product=product,
            quantity=10,
            alert_threshold=3,
        )

        self.assertEqual(stock.product, product)
        self.assertEqual(stock.quantity, 10)
