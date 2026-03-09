from django.urls import path

from .views import InventoryAdjustView, InventoryListView


urlpatterns = [
    path("admin/inventory", InventoryListView.as_view(), name="admin-inventory-list"),
    path("admin/inventory/<int:product_id>/adjust", InventoryAdjustView.as_view(), name="admin-inventory-adjust"),
]
