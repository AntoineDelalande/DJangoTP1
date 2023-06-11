from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from .forms import VehicleSearchForm
from django.views.generic import FormView
from django.db.models import Q
import requests

from django.views.generic.list import ListView
from django.views.generic import DetailView, DeleteView
from django.views.generic.edit import CreateView

from .models import Vehicle, Booking


class VehicleListView(ListView):
    model = Vehicle


class VehicleDetailView(DetailView):
    model = Vehicle
    context_object_name = "vehicle"

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vehicle = self.object
        if self.request.user.is_superuser:
            current_datetime = timezone.now()
            upcoming_bookings = Booking.objects.filter(
                vehicle=vehicle, booking_from__gte=current_datetime
            ).order_by("booking_from")[:5]
            context["upcoming_bookings"] = upcoming_bookings
        return context


class VehicleCreateView(CreateView):
    model = Vehicle
    fields = ["description", "number", "vehicle_type", "location"]
    success_url = "/autopark/all"


class BookingCreateView(CreateView):
    model = Booking
    fields = ["vehicle", "booking_from", "booking_to", "comments"]
    success_url = "/booking/all"

    def form_valid(self, form):
        form.instance.user = self.request.user

        vehicle = form.cleaned_data["vehicle"]
        booking_from = form.cleaned_data["booking_from"]
        booking_to = form.cleaned_data["booking_to"]

        if vehicle.next_check_at == None or vehicle.next_check_at < timezone.now():
            form.add_error(
                "booking_from",
                "This vehicle is not operational, it needs a maintenance check.",
            )
            return self.form_invalid(form)

        if booking_from >= booking_to:
            form.add_error(
                "booking_from",
                "The 'booking_from' datetime must be earlier than the 'booking_to' datetime.",
            )
            return self.form_invalid(form)

        current_datetime = timezone.now()
        if booking_from < current_datetime:
            form.add_error(
                "booking_from",
                "The 'booking_from' datetime must be equal to or later than the current datetime.",
            )
            return self.form_invalid(form)

        if self.model.objects.filter(
            vehicle=vehicle, booking_from__lte=booking_to, booking_to__gte=booking_from
        ).exists():
            form.add_error(
                "booking_from",
                "A reservation already exists for the selected vehicle and time period.",
            )
            return self.form_invalid(form)

        super().form_valid(form)

        superusers = User.objects.filter(is_superuser=True)

        collaborator = self.request.user
        vehicle = form.cleaned_data["vehicle"]
        booking_from = form.cleaned_data["booking_from"]
        booking_to = form.cleaned_data["booking_to"]
        email_subject = "Nouvelle réservation de véhicule"
        email_message = f"Chers super-utilisateurs,\n\nUne nouvelle réservation de véhicule a été effectuée.\n\nCollaborateur : {collaborator}\nVéhicule : {vehicle}\nPériode de réservation : {booking_from} - {booking_to}"

        email_message = render_to_string(
            "reservation_email.html",
            {
                "collaborator": collaborator,
                "vehicle": vehicle,
                "booking_from": booking_from,
                "booking_to": booking_to,
            },
        )

        if (
            settings.EMAIL_BACKEND
            and settings.EMAIL_HOST_USER
            and settings.EMAIL_HOST_PASSWORD
        ):
            try:
                send_mail(
                    email_subject,
                    email_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [superuser.email for superuser in superusers],
                    fail_silently=False,
                    html_message=email_message,
                )
                print("Email sent successfully")

            except Exception as e:
                print(e)
                pass

        return super().form_valid(form)


class BookingListView(ListView):
    model = Booking
    ordering = ["booking_from"]


class BookingDeleteView(DeleteView):
    model = Booking
    success_url = "/booking/all"
    context_object_name = "booking"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class VehicleSearchView(FormView):
    template_name = "vehicle_search.html"
    form_class = VehicleSearchForm

    def form_valid(self, form):
        start_date = form.cleaned_data["start_date"]
        end_date = form.cleaned_data["end_date"]
        location = form.cleaned_data.get("location")

        if location:
            vehicles = Vehicle.objects.filter(
                Q(location=location) | Q(location__isnull=True)
            )
        else:
            vehicles = Vehicle.objects.all()

        booked_vehicles = Booking.objects.filter(
            booking_from__lte=end_date, booking_to__gte=start_date
        ).values_list("vehicle", flat=True)
        available_vehicles = vehicles.exclude(pk__in=booked_vehicles)

        if available_vehicles:
            context = self.get_context_data(form=form, vehicles=available_vehicles)
        else:
            context = self.get_context_data(form=form, no_results=True)

        return self.render_to_response(context)


def refresh_maintenance(request):
    id = request.POST.get("id")
    if request.method == "POST":
        url = "https://api.raviou.li/vehicle/" + Vehicle.objects.get(id=id).number + "/"
        headers = {"API-TOKEN": settings.RAVIOLI_KEY}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()

            instance = Vehicle.objects.get(id=id)

            instance.last_maintenance_at = data["last_maintenance_at"]
            instance.next_check_at = data["next_control_at"]

            instance.save()
        else:
            raise Exception("Error: " + str(response.status_code))
    model = Vehicle.objects.get(id=id)
    context = {"vehicle": model}
    return render(request, "vehicle_detail.html", context)
