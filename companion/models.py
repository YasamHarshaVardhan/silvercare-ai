from django.db import models
from django.contrib.auth.models import User

# IMPORTANT MIGRATION NOTE:
# After updating models:
# 1. Run: python manage.py makemigrations
# 2. Run: python manage.py migrate
# 3. For existing rows, set a default user (e.g., select an existing user or create one).

class Medication(models.Model):
    """
    Model representing a medication that the senior citizen needs to take.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="User (senior) this medication belongs to")
    name = models.CharField(max_length=200, help_text="Name of the medication (e.g., Lisinopril)")
    dosage = models.CharField(max_length=100, help_text="Dosage details (e.g., 10mg, 1 tablet)")
    time_to_take = models.TimeField(help_text="Time of day when the medication should be taken")

    def __str__(self):
        return f"{self.name} - {self.dosage} at {self.time_to_take.strftime('%I:%M %p')}"


class Appointment(models.Model):
    """
    Model representing a doctor or medical appointment.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="User (senior) this appointment belongs to")
    doctor_name = models.CharField(max_length=200, help_text="Name of the doctor or clinic (e.g., Dr. Smith)")
    location = models.CharField(max_length=300, help_text="Location/address of the appointment")
    date_time = models.DateTimeField(help_text="Date and time of the scheduled appointment")

    def __str__(self):
        return f"Appointment with {self.doctor_name} at {self.date_time.strftime('%Y-%m-%d %I:%M %p')}"

