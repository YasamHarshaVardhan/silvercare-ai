from django import forms

from .models import Medication, Appointment


class MedicationForm(forms.ModelForm):
    class Meta:
        model = Medication
        fields = ['name', 'dosage', 'time_to_take']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Medication Name'}),
            'dosage': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dosage details'}),
            'time_to_take': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor_name', 'location', 'date_time']
        widgets = {
            'doctor_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Doctor or Clinic Name'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
            'date_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }
