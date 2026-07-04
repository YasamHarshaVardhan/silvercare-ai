from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import time
import json

from .models import Medication, Appointment

class SilverCareModelTests(TestCase):
    """
    Test suite for Medication and Appointment database models.
    """
    def test_medication_creation(self):
        med = Medication.objects.create(
            name="Aspirin",
            dosage="81mg",
            time_to_take=time(8, 0) # 8:00 AM
        )
        self.assertEqual(med.name, "Aspirin")
        self.assertEqual(med.dosage, "81mg")
        self.assertEqual(str(med), "Aspirin - 81mg at 08:00 AM")

    def test_appointment_creation(self):
        dt = timezone.now() + timezone.timedelta(days=1)
        appt = Appointment.objects.create(
            doctor_name="Dr. Watson",
            location="Baker St.",
            date_time=dt
        )
        self.assertEqual(appt.doctor_name, "Dr. Watson")
        self.assertEqual(appt.location, "Baker St.")
        expected_str = f"Appointment with Dr. Watson at {timezone.localtime(dt).strftime('%Y-%m-%d %I:%M %p')}"
        self.assertEqual(str(appt), expected_str)


class SilverCareViewTests(TestCase):
    """
    Test suite for web pages and API routing.
    """
    def setUp(self):
        self.client = Client()

    def test_companion_page_status(self):
        response = self.client.get(reverse('companion'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'companion/companion.html')

    def test_add_data_page_status(self):
        response = self.client.get(reverse('add_data'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'companion/add_data.html')

    def test_add_medication_post(self):
        response = self.client.post(reverse('add_data'), {
            'form_type': 'medication',
            'name': 'Ibuprofen',
            'dosage': '200mg',
            'time_to_take': '14:30'
        })
        self.assertEqual(response.status_code, 302) # Redirects back on success
        self.assertTrue(Medication.objects.filter(name='Ibuprofen').exists())

    def test_add_appointment_post(self):
        future_dt = (timezone.now() + timezone.timedelta(days=2)).strftime('%Y-%m-%dT%H:%M')
        response = self.client.post(reverse('add_data'), {
            'form_type': 'appointment',
            'doctor_name': 'Dr. Evans',
            'location': 'Downtown Clinic',
            'date_time': future_dt
        })
        self.assertEqual(response.status_code, 302) # Redirects back on success
        self.assertTrue(Appointment.objects.filter(doctor_name='Dr. Evans').exists())

    def test_chat_api_invalid_methods(self):
        response = self.client.get(reverse('chat_api'))
        self.assertEqual(response.status_code, 405) # POST only method allowed

    def test_chat_api_empty_message(self):
        response = self.client.post(
            reverse('chat_api'),
            data=json.dumps({'message': ''}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_check_alerts_empty(self):
        response = self.client.get(reverse('check_alerts'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['alerts'], [])

    def test_check_alerts_medication(self):
        now_local = timezone.localtime(timezone.now())
        Medication.objects.create(
            name="MedFive",
            dosage="1 pill",
            time_to_take=(now_local + timezone.timedelta(minutes=5)).time()
        )
        Medication.objects.create(
            name="MedNow",
            dosage="2 pills",
            time_to_take=now_local.time()
        )
        response = self.client.get(reverse('check_alerts'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn("Excuse me, in 5 minutes it is time to take your MedFive.", data['alerts'])
        self.assertIn("Excuse me, it is time to take your MedNow.", data['alerts'])

    def test_check_alerts_appointment(self):
        now_local = timezone.localtime(timezone.now())
        Appointment.objects.create(
            doctor_name="Dr. AlertHour",
            location="Alert Clinic",
            date_time=now_local + timezone.timedelta(hours=1)
        )
        Appointment.objects.create(
            doctor_name="Dr. AlertNow",
            location="Immediate Clinic",
            date_time=now_local
        )
        response = self.client.get(reverse('check_alerts'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn("Reminder, you have a doctor appointment in 1 hour.", data['alerts'])
        self.assertIn("Reminder, you have a doctor appointment now.", data['alerts'])

