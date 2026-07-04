import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.utils import timezone
from django.utils.dateparse import parse_datetime, parse_time
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required

from .forms import AppointmentForm, MedicationForm
from .models import Medication, Appointment
from .agent import query_gemini_agent


# Authentication Views

def register_view(request):
    """
    View for registering new users.
    """
    if request.user.is_authenticated:
        return redirect('companion')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, f"Welcome to SilverCare AI, {user.username}!")
            return redirect('companion')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = UserCreationForm()
    return render(request, 'companion/register.html', {'form': form})


def login_view(request):
    """
    View for authenticating existing users.
    """
    if request.user.is_authenticated:
        return redirect('companion')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('companion')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'companion/login.html', {'form': form})


def logout_view(request):
    """
    View for logging out users.
    """
    auth_logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('login')


@login_required
@ensure_csrf_cookie
def companion_view(request):
    """
    Renders the main voice/text companion dashboard.
    Ensures a CSRF cookie is set for API fetch calls.
    """
    return render(request, 'companion/companion.html')


@login_required
def add_data_view(request):
    """
    Handles rendering the form and processing manually entered 
    Medications and Appointments for the logged-in user.
    """
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        
        try:
            if form_type == 'medication':
                name = request.POST.get('name')
                dosage = request.POST.get('dosage')
                time_str = request.POST.get('time_to_take')
                
                if not name or not dosage or not time_str:
                    messages.error(request, "Please fill out all fields for Medication.")
                else:
                    time_to_take = parse_time(time_str)
                    if time_to_take is None:
                        messages.error(request, "Invalid time format.")
                    else:
                        Medication.objects.create(
                            user=request.user,
                            name=name,
                            dosage=dosage,
                            time_to_take=time_to_take
                        )
                        messages.success(request, f"Successfully added medication: {name}")
                        return redirect('add_data')
                        
            elif form_type == 'appointment':
                doctor_name = request.POST.get('doctor_name')
                location = request.POST.get('location')
                datetime_str = request.POST.get('date_time')
                
                if not doctor_name or not location or not datetime_str:
                    messages.error(request, "Please fill out all fields for Appointment.")
                else:
                    date_time = parse_datetime(datetime_str)
                    if date_time is None:
                        # Fallback for formats without seconds like YYYY-MM-DDTHH:MM
                        for fmt in ('%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S'):
                            try:
                                from datetime import datetime
                                date_time = datetime.strptime(datetime_str, fmt)
                                break
                            except ValueError:
                                continue
                                
                    if date_time is None:
                        messages.error(request, "Invalid date/time format. Use YYYY-MM-DD HH:MM")
                    else:
                        # Make timezone-aware if naive
                        if timezone.is_naive(date_time):
                            date_time = timezone.make_aware(date_time)
                        Appointment.objects.create(
                            user=request.user,
                            doctor_name=doctor_name,
                            location=location,
                            date_time=date_time
                        )
                        messages.success(request, f"Successfully scheduled appointment with {doctor_name}")
                        return redirect('add_data')
            else:
                messages.error(request, "Invalid form type submitted.")
                
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            
    # Retrieve current items to show list below forms - filtered by logged-in user
    medications = Medication.objects.filter(user=request.user).order_by('time_to_take')
    appointments = Appointment.objects.filter(user=request.user).order_by('date_time')
    
    context = {
        'medications': medications,
        'appointments': appointments
    }
    return render(request, 'companion/add_data.html', context)


@login_required
def manage_records_view(request):
    """
    Dashboard view showing the logged-in user's medications and appointments.
    """
    medications = Medication.objects.filter(user=request.user).order_by('time_to_take')
    appointments = Appointment.objects.filter(user=request.user).order_by('date_time')

    return render(
        request,
        'companion/manage_records.html',
        {
            'medications': medications,
            'appointments': appointments,
        }
    )


@login_required
@require_POST
def delete_medication(request, med_id):
    """
    Securely delete a medication owned by the logged-in user.
    """
    med = get_object_or_404(Medication, id=med_id, user=request.user)
    med.delete()
    messages.success(request, f"Successfully deleted medication: {med.name}")
    return redirect('manage_records')


@login_required
@require_POST
def delete_appointment(request, app_id):
    """
    Securely delete an appointment owned by the logged-in user.
    """
    appt = get_object_or_404(Appointment, id=app_id, user=request.user)
    appt.delete()
    messages.success(request, f"Successfully deleted appointment with {appt.doctor_name}")
    return redirect('manage_records')


@login_required
def update_medication(request, med_id):
    """
    Display and process a form for editing a medication owned by the current user.
    """
    medication = get_object_or_404(Medication, id=med_id, user=request.user)

    if request.method == 'POST':
        form = MedicationForm(request.POST, instance=medication)
        if form.is_valid():
            form.save()
            messages.success(request, "Medication updated successfully.")
            return redirect('manage_records')
    else:
        form = MedicationForm(instance=medication)

    return render(request, 'companion/update_medication.html', {'form': form, 'medication': medication})


@login_required
def update_appointment(request, app_id):
    """
    Display and process a form for editing an appointment owned by the current user.
    """
    appointment = get_object_or_404(Appointment, id=app_id, user=request.user)

    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, "Appointment updated successfully.")
            return redirect('manage_records')
    else:
        form = AppointmentForm(instance=appointment)

    return render(request, 'companion/update_appointment.html', {'form': form, 'appointment': appointment})


@login_required
@require_POST
def chat_api(request):
    """
    POST API endpoint for voice and text chat requests.
    Expects JSON body: {"message": "...", "history": [...]}
    Returns JSON body: {"reply": "..."}
    """
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        chat_history = data.get('history', [])
        
        if not user_message:
            return JsonResponse({'error': 'Message is empty'}, status=400)
            
        # Get AI response from agent, securely passing request.user context
        reply_text = query_gemini_agent(request.user, user_message, chat_history)
        
        return JsonResponse({'reply': reply_text})
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)


@login_required
def check_alerts_api(request):
    """
    API endpoint that checks for medication and appointment alerts for the logged-in user:
    - Medications due in exactly 5 minutes OR due right now.
    - Appointments due in exactly 1 hour OR due right now.
    """
    now = timezone.localtime(timezone.now())
    now_minutes = now.hour * 60 + now.minute
    
    alerts = []
    
    # 1. Check Medications
    for med in Medication.objects.filter(user=request.user):
        med_minutes = med.time_to_take.hour * 60 + med.time_to_take.minute
        # Difference in minutes modulo a full day (1440 minutes)
        diff = (med_minutes - now_minutes) % 1440
        if diff == 5:
            alerts.append(f"Excuse me, in 5 minutes it is time to take your {med.name}.")
        elif diff == 0:
            alerts.append(f"Excuse me, it is time to take your {med.name}.")
            
    # 2. Check Appointments
    start_time = now - timezone.timedelta(minutes=5)
    end_time = now + timezone.timedelta(minutes=65)
    upcoming_appts = Appointment.objects.filter(user=request.user, date_time__gte=start_time, date_time__lte=end_time)
    
    for appt in upcoming_appts:
        appt_local = timezone.localtime(appt.date_time)
        diff = appt_local - now
        diff_minutes = round(diff.total_seconds() / 60.0)
        
        if diff_minutes == 60:
            alerts.append("Reminder, you have a doctor appointment in 1 hour.")
        elif diff_minutes == 0:
            alerts.append("Reminder, you have a doctor appointment now.")
            
    return JsonResponse({'alerts': alerts})




