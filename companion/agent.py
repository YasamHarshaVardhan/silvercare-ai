import os
import json
import logging
from django.utils import timezone
from .models import Medication, Appointment

# Set up logging
logger = logging.getLogger(__name__)

# Try to import google.generativeai, handle gracefully if missing
try:
    import google.generativeai as genai
    from google.api_core.exceptions import GoogleAPIError
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logger.error("google-generativeai package is not installed.")

# Define Tools for Gemini Function Calling are now scoped inside query_gemini_agent as closures for user data isolation.


def query_gemini_agent(user, user_message: str, chat_history: list = None) -> str:
    """
    Queries the Gemini model with tool support to process user queries.
    
    Args:
        user: The logged-in Django User instance.
        user_message: The text input from the user (typed or spoken).
        chat_history: Optional list of previous chat turn dicts like:
                      [{'role': 'user', 'parts': '...'}, {'role': 'model', 'parts': '...'}]
                      
    Returns:
        str: The generated assistant response.
    """
    def get_daily_medications() -> str:
        """
        Retrieves all daily medications scheduled for the patient. 
        Use this when the user asks about their medications, what pills they need to take, or dosage schedules.
        
        Returns:
            str: A JSON formatted string containing the list of medications, their dosages, and scheduled times.
        """
        try:
            meds = Medication.objects.filter(user=user).order_by('time_to_take')
            if not meds.exists():
                return json.dumps({"status": "no_data", "message": "No medications are listed in the database."})
            
            result = []
            for med in meds:
                result.append({
                    "name": med.name,
                    "dosage": med.dosage,
                    "time_to_take": med.time_to_take.strftime("%I:%M %p")
                })
            return json.dumps({"status": "success", "medications": result})
        except Exception as e:
            logger.exception("Error fetching medications")
            return json.dumps({"status": "error", "message": str(e)})

    def get_upcoming_appointments() -> str:
        """
        Retrieves all upcoming doctor or medical appointments for the patient starting from today.
        Use this when the user asks about their doctor visits, appointments, or schedules.
        
        Returns:
            str: A JSON formatted string containing upcoming appointments with doctor names, locations, and date/time.
        """
        try:
            # Get appointments starting from today (midnight)
            today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
            appts = Appointment.objects.filter(user=user, date_time__gte=today_start).order_by('date_time')
            
            if not appts.exists():
                return json.dumps({"status": "no_data", "message": "No upcoming appointments are listed in the database."})
            
            result = []
            for appt in appts:
                # Convert date_time to local timezone if activated
                local_dt = timezone.localtime(appt.date_time)
                result.append({
                    "doctor_name": appt.doctor_name,
                    "location": appt.location,
                    "date_time": local_dt.strftime("%Y-%m-%d %I:%M %p")
                })
            return json.dumps({"status": "success", "appointments": result})
        except Exception as e:
            logger.exception("Error fetching appointments")
            return json.dumps({"status": "error", "message": str(e)})

    if not GEMINI_AVAILABLE:
        return "I apologize, but the Google Gemini SDK is not installed in the Python environment."

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "YOUR_GEMINI_API_KEY_HERE":
        return (
            "I apologize, but my Gemini API Key is not configured. "
            "Please configure the GEMINI_API_KEY inside your .env file to enable my AI brain."
        )

    try:
        # Configure Gemini
        genai.configure(api_key=api_key)

        # Initialize the model with system instructions and tools
        system_instruction = (
            "You are a gentle, patient, and concise senior care assistant for 'SilverCare AI'. "
            "Your role is to help senior citizens manage their daily medications and doctor appointments. "
            "Always be respectful, friendly, and speak in short, easy-to-understand sentences. "
            "If they ask about their medications, schedule, or doctor visits, use the appropriate tools to "
            "query the database, and then present the information clearly. "
            "For example, explain what time they should take each pill, or where their appointment is located. "
            "Be patient and repeat information if necessary. Do not mention system details, database schemas, "
            "or function names. "
            "If they ask to add data (like 'add a medication' or 'schedule an appointment'), politely let them know "
            "they can easily do so using the manual form on the 'Add Data' page."
        )

        model = genai.GenerativeModel(
            model_name='gemini-2.0-flash',
            tools=[get_daily_medications, get_upcoming_appointments],
            system_instruction=system_instruction
        )

        # Format history for Gemini chat
        formatted_history = []
        if chat_history:
            for turn in chat_history:
                # Turn should have keys 'role' and 'parts'
                role = turn.get('role')
                # Map standard roles to model/user
                if role == 'assistant':
                    role = 'model'
                parts = turn.get('content') or turn.get('parts')
                if role in ['user', 'model'] and parts:
                    formatted_history.append({
                        "role": role,
                        "parts": parts
                    })

        # Start chat with automatic function calling enabled
        chat = model.start_chat(history=formatted_history, enable_automatic_function_calling=True)
        response = chat.send_message(user_message)
        return response.text

    except GoogleAPIError as api_err:
        logger.error(f"Gemini API Error: {api_err}")
        return f"I'm having trouble connecting to my Gemini brain. Details: {str(api_err)}"
    except Exception as e:
        logger.exception("Unexpected error in query_gemini_agent")
        return f"I encountered an unexpected error: {str(e)}"

