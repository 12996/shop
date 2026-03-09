from django.urls import path

from .views import (
    AdminAnnouncementDetailView,
    AdminAnnouncementListCreateView,
    AdminHotProductsView,
    AdminRecommendationDetailView,
    AdminRecommendationListCreateView,
    AdminStatisticsOverviewView,
    HomeView,
)


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("admin/announcements", AdminAnnouncementListCreateView.as_view(), name="admin-announcement-list-create"),
    path("admin/announcements/<int:announcement_id>", AdminAnnouncementDetailView.as_view(), name="admin-announcement-detail"),
    path("admin/recommendations", AdminRecommendationListCreateView.as_view(), name="admin-recommendation-list-create"),
    path("admin/recommendations/<int:recommendation_id>", AdminRecommendationDetailView.as_view(), name="admin-recommendation-detail"),
    path("admin/statistics/overview", AdminStatisticsOverviewView.as_view(), name="admin-statistics-overview"),
    path("admin/statistics/hot-products", AdminHotProductsView.as_view(), name="admin-hot-products"),
]
