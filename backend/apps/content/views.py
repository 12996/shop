from django.shortcuts import get_object_or_404
from django.db.models import Sum, Count
from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.permissions import IsMerchant
from apps.orders.models import Order, OrderItem

from .models import Announcement, Recommendation
from .serializers import AnnouncementSerializer, RecommendationSerializer


class HomeView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        announcement = (
            Announcement.objects.filter(status=Announcement.STATUS_PUBLISHED)
            .order_by("-published_at", "-id")
            .first()
        )
        recommendations = Recommendation.objects.filter(
            status=Recommendation.STATUS_ENABLED,
            product__status="on_shelf",
        ).select_related("product")

        return Response(
            {
                "announcement": AnnouncementSerializer(announcement).data if announcement else None,
                "recommendations": RecommendationSerializer(recommendations, many=True).data,
            }
        )


class AdminAnnouncementListCreateView(APIView):
    permission_classes = [IsMerchant]

    def get(self, request):
        announcements = Announcement.objects.all().order_by("-published_at", "-id")
        return Response(AnnouncementSerializer(announcements, many=True).data)

    def post(self, request):
        serializer = AnnouncementSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        published_at = None
        if serializer.validated_data["status"] == Announcement.STATUS_PUBLISHED:
            published_at = timezone.now()

        announcement = serializer.save(
            publisher=request.user,
            published_at=published_at,
        )
        return Response(
            AnnouncementSerializer(announcement).data,
            status=status.HTTP_201_CREATED,
        )


class AdminAnnouncementDetailView(APIView):
    permission_classes = [IsMerchant]

    def put(self, request, announcement_id):
        announcement = get_object_or_404(Announcement, id=announcement_id)
        serializer = AnnouncementSerializer(announcement, data=request.data)
        serializer.is_valid(raise_exception=True)

        published_at = announcement.published_at
        if serializer.validated_data["status"] == Announcement.STATUS_PUBLISHED and not published_at:
            published_at = timezone.now()

        serializer.save(
            publisher=announcement.publisher or request.user,
            published_at=published_at,
        )
        return Response(serializer.data)

    def delete(self, request, announcement_id):
        announcement = get_object_or_404(Announcement, id=announcement_id)
        announcement.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminRecommendationListCreateView(APIView):
    permission_classes = [IsMerchant]

    def get(self, request):
        recommendations = Recommendation.objects.select_related("product").all().order_by("sort_order", "id")
        return Response(RecommendationSerializer(recommendations, many=True).data)

    def post(self, request):
        serializer = RecommendationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        recommendation = serializer.save()
        return Response(
            RecommendationSerializer(recommendation).data,
            status=status.HTTP_201_CREATED,
        )


class AdminRecommendationDetailView(APIView):
    permission_classes = [IsMerchant]

    def put(self, request, recommendation_id):
        recommendation = get_object_or_404(Recommendation, id=recommendation_id)
        serializer = RecommendationSerializer(recommendation, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, recommendation_id):
        recommendation = get_object_or_404(Recommendation, id=recommendation_id)
        recommendation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminStatisticsOverviewView(APIView):
    permission_classes = [IsMerchant]

    def get(self, request):
        sales_amount = Order.objects.aggregate(total=Sum("pay_amount"))["total"] or 0
        return Response(
            {
                "order_count": Order.objects.count(),
                "completed_order_count": Order.objects.filter(status=Order.STATUS_COMPLETED).count(),
                "sales_amount": f"{sales_amount:.2f}",
            }
        )


class AdminHotProductsView(APIView):
    permission_classes = [IsMerchant]

    def get(self, request):
        rows = (
            OrderItem.objects.filter(order__status__in=[Order.STATUS_PAID, Order.STATUS_COMPLETED])
            .values("product_id", "product_name")
            .annotate(sales_count=Sum("quantity"), order_count=Count("order_id", distinct=True))
            .order_by("-sales_count", "product_id")[:10]
        )
        return Response(
            [
                {
                    "product_id": row["product_id"],
                    "product_name": row["product_name"],
                    "sales_count": row["sales_count"],
                    "order_count": row["order_count"],
                }
                for row in rows
            ]
        )
