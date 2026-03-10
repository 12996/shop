from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response

from apps.common.views import LoggedAPIView
from apps.products.models import Product

from .models import Cart, CartItem
from .serializers import (
    AddCartItemSerializer,
    CartItemSerializer,
    CartSerializer,
    UpdateCartItemSerializer,
)


def get_or_create_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


class CartView(LoggedAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart = get_or_create_cart(request.user)
        return Response(CartSerializer(cart).data)


class CartItemListCreateView(LoggedAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = AddCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart = get_or_create_cart(request.user)
        product = get_object_or_404(Product, id=serializer.validated_data["product_id"])
        quantity = serializer.validated_data["quantity"]

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={"quantity": quantity},
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save(update_fields=["quantity", "updated_at"])

        return Response(CartItemSerializer(cart_item).data, status=status.HTTP_200_OK)


class CartItemDetailView(LoggedAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, item_id):
        cart = get_or_create_cart(request.user)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

        serializer = UpdateCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if "quantity" in serializer.validated_data:
            cart_item.quantity = serializer.validated_data["quantity"]
        if "selected" in serializer.validated_data:
            cart_item.selected = serializer.validated_data["selected"]

        cart_item.save()
        return Response(CartItemSerializer(cart_item).data)

    def delete(self, request, item_id):
        cart = get_or_create_cart(request.user)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartCheckoutView(LoggedAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        cart = get_or_create_cart(request.user)
        items = cart.items.filter(selected=True)
        total_amount = sum(item.product.price * item.quantity for item in items)
        return Response(
            {
                "cart_id": cart.id,
                "items": CartItemSerializer(items, many=True).data,
                "total_amount": total_amount,
            }
        )
