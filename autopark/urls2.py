from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import (
    BookingCreateView,
    BookingDeleteView,
    BookingListView,
)

urlpatterns = [
    path("all/", login_required(BookingListView.as_view()), name="booking-list"),
    path("new/", login_required(BookingCreateView.as_view()), name="booking-create"),
    path(
        "<int:pk>/delete/",
        login_required(BookingDeleteView.as_view()),
        name="booking-delete",
    ),
]
