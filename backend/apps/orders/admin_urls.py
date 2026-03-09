from django.urls import path

from .views import AdminOrderCompleteView, AdminOrderDetailView, AdminOrderListView


urlpatterns = [
    path("", AdminOrderListView.as_view(), name="admin-order-list"),
    path("<int:order_id>", AdminOrderDetailView.as_view(), name="admin-order-detail"),
    path("<int:order_id>/complete", AdminOrderCompleteView.as_view(), name="admin-order-complete"),
]
