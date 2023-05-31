from django.urls import path
from django.contrib import admin

from .views import VehicleListView, VehicleDetailView

urlpatterns = [
    path("all/", VehicleListView.as_view()),
    path("<int:pk>/details/", VehicleDetailView.as_view(), name="vehicle-detail")
]