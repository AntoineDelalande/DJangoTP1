from django import forms
from django.utils import timezone

from autopark.models import Location


class VehicleSearchForm(forms.Form):
    start_date = forms.DateTimeField(
        label="Date de début",
        initial=timezone.now(),
        widget=forms.DateTimeInput(attrs={"class": "form-control"}),
    )
    end_date = forms.DateTimeField(
        label="Date de fin", widget=forms.DateTimeInput(attrs={"class": "form-control"})
    )
    location = forms.ModelChoiceField(
        label="Localisation",
        queryset=Location.objects.all(),
        required=False,
        empty_label="Tous les emplacements",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
