from django.contrib.auth.decorators import login_required
from django.urls import path
from django.contrib import admin

from .views import (
    VehicleListView,
    VehicleDetailView,
    VehicleCreateView,
    VehicleSearchView,
)

urlpatterns = [
    path("all/", login_required(VehicleListView.as_view())),
    path(
        "<int:pk>/details/",
        login_required(VehicleDetailView.as_view()),
        name="vehicle-detail",
    ),
    path("create/", login_required(VehicleCreateView.as_view()), name="vehicle-create"),
    path("search/", VehicleSearchView.as_view(), name="vehicle-search"),
]
