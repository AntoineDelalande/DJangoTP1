from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from .serializers import VehicleSerializer
from django.conf import settings


class APIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        api_key = request.META.get("HTTP_API_KEY")
        print(api_key)
        if not api_key or api_key != settings.API_KEY:
            raise AuthenticationFailed("Invalid API key")
        if request.method == "GET":
            pass
        if request.method == "POST":
            pass

        return None, None

    def has_permission(self, request, *args):
        return True

    def has_object_permission(self, request, *args):
        return True
