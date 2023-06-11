from rest_framework import serializers
from autopark.models import Vehicle, Location
from django.core.validators import RegexValidator


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = "__all__"


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"
