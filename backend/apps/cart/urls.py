from django.urls import path

from .views import CartCheckoutView, CartItemDetailView, CartItemListCreateView, CartView


urlpatterns = [
    path("", CartView.as_view(), name="cart-detail"),
    path("items", CartItemListCreateView.as_view(), name="cart-item-create"),
    path("items/<int:item_id>", CartItemDetailView.as_view(), name="cart-item-detail"),
    path("checkout", CartCheckoutView.as_view(), name="cart-checkout"),
]
