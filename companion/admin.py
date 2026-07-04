from django.contrib import admin
from .models import Medication, Appointment

@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'dosage', 'time_to_take')
    list_filter = ('user', 'time_to_take')
    search_fields = ('user__username', 'name', 'dosage')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'doctor_name', 'location', 'date_time')
    list_filter = ('user', 'date_time')
    search_fields = ('user__username', 'doctor_name', 'location')

