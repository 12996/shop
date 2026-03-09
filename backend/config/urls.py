from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path, re_path


def health_check(_request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", health_check, name="health-check"),
    path("api/", include("apps.products.urls")),
    path("api/", include("apps.inventory.urls")),
    path("api/home", include("apps.content.urls")),
    path("api/", include("apps.content.urls")),
    path("api/", include("apps.vision.urls")),
    path("api/auth/", include("apps.users.urls")),
    path("api/cart/", include("apps.cart.urls")),
    re_path(r"^api/admin/orders/?", include("apps.orders.admin_urls")),
    re_path(r"^api/orders/?", include("apps.orders.urls")),
]
