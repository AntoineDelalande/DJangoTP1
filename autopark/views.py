from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView

from .models import Vehicle

class VehicleListView(ListView):
    model = Vehicle

class VehicleDetailView(DetailView):
    model = Vehicle
    context_object_name = "vehicle"
    
class VehicleCreateView(CreateView):
    model = Vehicle
    fields = ["description", "number", "vehicle_type", "location"]
    success_url = "/autopark/all"

