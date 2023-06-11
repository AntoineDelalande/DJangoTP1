from django.contrib.auth.decorators import login_required
from django.urls import path
from django.contrib import admin

from .views import (
    VehicleListView,
    VehicleDetailView,
    VehicleCreateView,
    VehicleSearchView,
    refresh_maintenance,
)

urlpatterns = [
    path("all/", login_required(VehicleListView.as_view())),
    path(
        "<int:pk>/details/",
        login_required(VehicleDetailView.as_view()),
        name="vehicle-detail",
    ),
    path("create/", login_required(VehicleCreateView.as_view()), name="vehicle-create"),
    path("search/", login_required(VehicleSearchView.as_view()), name="vehicle-search"),
    path(
        "refresh_maintenance/",
        login_required(refresh_maintenance),
        name="refresh_maintenance",
    ),
]
