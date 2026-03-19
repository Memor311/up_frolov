from django import forms
from django.forms import formset_factory  # Используем обычный factory
from .models import Route, Request, Cargo

class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['address_start', 'address_end', 'departure_date', 'driver', 'client', 'transport', 'status']
        widgets = {
            'address_start': forms.Textarea(attrs={'rows': 2, 'class': 'form-control rounded-3'}),
            'address_end': forms.Textarea(attrs={'rows': 2, 'class': 'form-control rounded-3'}),
            'departure_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control rounded-3'}),
            'driver': forms.Select(attrs={'class': 'form-select rounded-3'}),
            'client': forms.Select(attrs={'class': 'form-select rounded-3'}),
            'transport': forms.Select(attrs={'class': 'form-select rounded-3'}),
            'status': forms.Select(attrs={'class': 'form-select rounded-3'}),
        }

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['cargo', 'quantity']
        widgets = {
            'cargo': forms.Select(attrs={'class': 'form-select rounded-3'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control rounded-3', 'min': 1}),
        }

# Создаем ОБЫЧНЫЙ формсет. 
# extra=3 означает, что по умолчанию будет 3 пустые строки для грузов.
RequestFormSet = formset_factory(RequestForm, extra=3, can_delete=True)