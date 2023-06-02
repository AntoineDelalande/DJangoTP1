from django.db import models
from django.contrib.auth.models import User


class Location(models.Model):
    label = models.CharField(max_length=255)

    def __str__(self):
        return self.label


class V_Types(models.TextChoices):
    ELECTRIQUE = "ELECTRIQUE"
    DIESEL = "DIESEL"
    ESSENCE = "ESSENCE"


class Vehicle(models.Model):
    description = models.TextField()
    number = models.CharField(max_length=255)
    vehicle_type = models.CharField(max_length=255, choices=V_Types.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.number


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    booking_from = models.DateTimeField()
    booking_to = models.DateTimeField()
    comments = models.TextField(blank=True, null=True)
    approved = models.BooleanField(null=True, default=None)

    def get_approved_display(self):
        if self.approved is None:
            return "En attente"
        elif self.approved:
            return "Approuvée"
        else:
            return "Non approuvée"
