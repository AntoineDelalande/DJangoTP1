from django.contrib.auth.decorators import login_required
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from .views import IndexView, VehicleViewSet, LocationViewSet

router = routers.DefaultRouter()
router.register(r"vehicle", VehicleViewSet, basename="vehicle")
router.register(r"location", LocationViewSet, basename="location")


urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
    path("autopark/", include("autopark.urls")),
    path("", login_required(IndexView.as_view()), name="index"),
    path("booking/", include("autopark.urls2")),
    path("api/", include(router.urls)),
    path("api/auth/", include("rest_framework.urls", namespace="rest_framework")),
]
