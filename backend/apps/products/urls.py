from django.urls import path

from .views import (
    AdminProductDetailView,
    AdminProductListCreateView,
    AdminProductOffShelfView,
    AdminProductOnShelfView,
    CategoryListView,
    ProductDetailView,
    ProductListView,
)


urlpatterns = [
    path("categories", CategoryListView.as_view(), name="category-list"),
    path("products", ProductListView.as_view(), name="product-list"),
    path("products/<int:product_id>", ProductDetailView.as_view(), name="product-detail"),
    path("admin/products", AdminProductListCreateView.as_view(), name="admin-product-list-create"),
    path("admin/products/<int:product_id>", AdminProductDetailView.as_view(), name="admin-product-detail"),
    path("admin/products/<int:product_id>/on_shelf", AdminProductOnShelfView.as_view(), name="admin-product-on-shelf"),
    path("admin/products/<int:product_id>/off_shelf", AdminProductOffShelfView.as_view(), name="admin-product-off-shelf"),
]
