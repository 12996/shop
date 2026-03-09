from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.permissions import IsMerchant

from .models import Order
from .serializers import AdminOrderSerializer, OrderSerializer
from .services import cancel_order, complete_order, create_order_from_cart, pay_order


class OrderListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).prefetch_related("items").order_by("-id")
        return Response(OrderSerializer(orders, many=True).data)

    def post(self, request):
        try:
            order = create_order_from_cart(user=request.user)
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class OrderDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, order_id):
        order = get_object_or_404(Order.objects.prefetch_related("items"), id=order_id, user=request.user)
        return Response(OrderSerializer(order).data)


class OrderCancelView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)

        try:
            order = cancel_order(order=order, user=request.user)
        except PermissionError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_403_FORBIDDEN)
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)


class OrderPayView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        payment_method = request.data.get("payment_method")

        try:
            order = pay_order(
                order=order,
                user=request.user,
                payment_method=payment_method,
            )
        except PermissionError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_403_FORBIDDEN)
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)


class AdminOrderListView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsMerchant]

    def get(self, request):
        orders = Order.objects.select_related("user").prefetch_related("items").order_by("-id")
        status_value = request.query_params.get("status")
        if status_value:
            orders = orders.filter(status=status_value)
        return Response(AdminOrderSerializer(orders, many=True).data)


class AdminOrderDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsMerchant]

    def get(self, request, order_id):
        order = get_object_or_404(
            Order.objects.select_related("user").prefetch_related("items"),
            id=order_id,
        )
        return Response(AdminOrderSerializer(order).data)


class AdminOrderCompleteView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsMerchant]

    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)

        try:
            order = complete_order(order=order, user=request.user)
        except PermissionError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_403_FORBIDDEN)
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(AdminOrderSerializer(order).data, status=status.HTTP_200_OK)
