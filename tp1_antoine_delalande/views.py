from django.views.generic import TemplateView
from django.utils import timezone
from .serializers import VehicleSerializer, LocationSerializer
from autopark.models import Vehicle, Booking, Location
from rest_framework import viewsets
from .authentication import APIKeyAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from rest_framework.decorators import api_view, authentication_classes


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated:
            current_datetime = timezone.now()

            upcoming_bookings = Booking.objects.filter(
                user=user, booking_from__gte=current_datetime
            ).order_by("booking_from")[:5]
            context["upcoming_bookings"] = upcoming_bookings

            booked_vehicles = Booking.objects.filter(
                booking_from__lte=current_datetime, booking_to__gte=current_datetime
            ).values_list("vehicle", flat=True)
            available_vehicles = Vehicle.objects.exclude(pk__in=booked_vehicles)
            context["available_vehicles"] = available_vehicles

        return context


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    authentication_classes = [APIKeyAuthentication]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["number", "vehicle_type", "created_at"]
    ordering_fields = ["number", "vehicle_type", "created_at"]


class LocationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
