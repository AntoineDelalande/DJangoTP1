from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from .models import Vehicle
import requests


@receiver([post_save], sender=Vehicle)
def fill_vehicle_data(sender, instance, created, **kwargs):
    if created:
        url = "https://api.raviou.li/vehicle/" + instance.number + "/"
        headers = {"API-TOKEN": settings.RAVIOLI_KEY}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()

            instance.last_maintenance_at = data["last_maintenance_at"]
            instance.next_check_at = data["next_control_at"]

            instance.save()
        else:
            raise Exception("Error: " + str(response.status_code))
