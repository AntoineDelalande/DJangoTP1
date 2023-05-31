from django.db import models

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
    location = models.ForeignKey(Location ,on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.number