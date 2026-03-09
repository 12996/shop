from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.permissions import IsMerchant

from .models import Category, Product
from .serializers import AdminProductSerializer, CategorySerializer, ProductSerializer


class CategoryListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, _request):
        categories = Category.objects.filter(status=Category.STATUS_ENABLED).order_by("sort_order", "id")
        return Response(CategorySerializer(categories, many=True).data)


class ProductListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        queryset = Product.objects.filter(status=Product.STATUS_ON_SHELF).select_related("category", "stock")

        category_id = request.query_params.get("category_id")
        keyword = request.query_params.get("keyword")

        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if keyword:
            queryset = queryset.filter(Q(name__icontains=keyword) | Q(description__icontains=keyword))

        return Response(ProductSerializer(queryset.order_by("id"), many=True).data)


class ProductDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, _request, product_id):
        product = get_object_or_404(
            Product.objects.filter(status=Product.STATUS_ON_SHELF).select_related("category", "stock"),
            id=product_id,
        )
        return Response(ProductSerializer(product).data)


class AdminProductListCreateView(APIView):
    permission_classes = [IsMerchant]

    def get(self, _request):
        products = Product.objects.select_related("category", "stock").order_by("id")
        return Response(AdminProductSerializer(products, many=True).data)

    def post(self, request):
        serializer = AdminProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        return Response(AdminProductSerializer(product).data, status=201)


class AdminProductDetailView(APIView):
    permission_classes = [IsMerchant]

    def put(self, request, product_id):
        product = get_object_or_404(Product.objects.select_related("stock"), id=product_id)
        serializer = AdminProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class AdminProductOnShelfView(APIView):
    permission_classes = [IsMerchant]

    def post(self, _request, product_id):
        product = get_object_or_404(Product.objects.select_related("stock"), id=product_id)
        product.status = Product.STATUS_ON_SHELF
        product.save(update_fields=["status", "updated_at"])
        return Response(AdminProductSerializer(product).data)


class AdminProductOffShelfView(APIView):
    permission_classes = [IsMerchant]

    def post(self, _request, product_id):
        product = get_object_or_404(Product.objects.select_related("stock"), id=product_id)
        product.status = Product.STATUS_OFF_SHELF
        product.save(update_fields=["status", "updated_at"])
        return Response(AdminProductSerializer(product).data)
