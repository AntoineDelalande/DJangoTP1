from django.contrib.auth.decorators import login_required
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

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
    path(
        "openapi",
        get_schema_view(
            title="AutoPark",
            description="API for accessing the autopark data",
            version="1.0.0",
        ),
        name="openapi-schema",
    ),
    path(
        "api-docs/",
        TemplateView.as_view(
            template_name="redoc.html", extra_context={"schema_url": "openapi-schema"}
        ),
        name="redoc",
    ),
]
