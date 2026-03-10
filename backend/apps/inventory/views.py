from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from apps.common.permissions import IsMerchant
from apps.common.views import LoggedAPIView
from apps.products.models import Product

from .models import Stock, StockLog
from .serializers import AdjustStockSerializer, StockSerializer


class InventoryListView(LoggedAPIView):
    permission_classes = [IsMerchant]

    def get(self, _request):
        stocks = Stock.objects.select_related("product", "product__category").order_by("product_id")
        return Response(StockSerializer(stocks, many=True).data)


class InventoryAdjustView(LoggedAPIView):
    permission_classes = [IsMerchant]

    def post(self, request, product_id):
        serializer = AdjustStockSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = get_object_or_404(Product, id=product_id)
        stock = get_object_or_404(Stock.objects.select_related("product", "product__category"), product=product)

        before_qty = stock.quantity
        after_qty = serializer.validated_data["quantity"]
        stock.quantity = after_qty
        stock.save(update_fields=["quantity", "updated_at"])

        StockLog.objects.create(
            product=product,
            change_type=StockLog.CHANGE_MANUAL,
            change_amount=abs(after_qty - before_qty),
            before_qty=before_qty,
            after_qty=after_qty,
            operator=request.user,
            remark=serializer.validated_data.get("remark", ""),
        )

        stock.refresh_from_db()
        return Response(StockSerializer(stock).data)
