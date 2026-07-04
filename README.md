# SilverCare AI: Proactive Senior Companion

> **An autonomous, voice-enabled AI companion that empowers senior citizens to manage medications, appointments, and daily health routines independently through proactive reminders and natural conversation.**

**Project Submission:** Kaggle AI Agents: Intensive Vibe Coding Capstone (Agents for Good Track)

---

## 📌 Overview

SilverCare AI is an intelligent healthcare companion designed specifically for senior citizens. Unlike traditional reminder applications that rely solely on user interaction, SilverCare AI continuously monitors medication schedules and medical appointments, proactively notifying users before important events.

The application combines:

- 🤖 Google Gemini AI for intelligent conversations
- 🔒 Secure Django backend with authenticated AI tools
- 🗄️ SQLite database for local and private data storage
- 🎤 Voice interaction using the Web Speech API
- ♿ Accessibility-focused interface for elderly users

The goal is to promote independent living while ensuring important health routines are never missed.

---

# Features

## 🧠 AI Health Companion

- Natural language conversations powered by Google Gemini
- Health-related assistance and guidance
- Context-aware responses
- Voice and text interaction

---

## 🔔 Proactive Medication Alerts

The AI autonomously monitors medication schedules and provides reminders **5 minutes before** the scheduled time.

Example:

> "It's almost time to take your Blood Pressure medication."

---

## 📅 Appointment Reminders

Automatically reminds users **1 hour before** upcoming medical appointments.

Example:

> "You have a doctor's appointment at 3:00 PM today."

---

## 🎤 Voice Interaction

Supports:

- Speech-to-text
- Text-to-speech
- Hands-free conversations
- Browser microphone integration

Built using the browser's Web Speech API.

---

## ✍️ Manual Record Management

Users can manually manage:

- Medications
- Appointments
- Health records

through a simple dashboard.

---

## 🔒 Secure Multi-User Architecture

Every AI action is scoped to the currently authenticated user.

This ensures:

- One user cannot access another user's medications.
- One user cannot access another user's appointments.
- Complete data isolation.
- Secure authenticated tool execution.

---

## ♿ Accessibility First

Designed specifically for senior citizens.

Features include:

- High-contrast UI
- Large readable fonts
- Simple navigation
- Minimal distractions
- Voice-first interaction

---

# Technology Stack

| Layer | Technology |
|--------|------------|
| Backend | Django |
| AI | Google Gemini API |
| Database | SQLite |
| Frontend | HTML, CSS, JavaScript |
| Voice Recognition | Web Speech API |
| Text-to-Speech | SpeechSynthesis API |
| Authentication | Django Authentication |

---

# Project Structure

```
SilverCare-AI/
│
├── companion/
│   ├── templates/
│   ├── static/
│   ├── views.py
│   ├── models.py
│   ├── urls.py
│   └── agent.py
│
├── users/
│
├── silvercare/
│
├── db.sqlite3
├── manage.py
├── requirements.txt
├── .env
└── README.md
```

---

# Installation

## 1. Clone Repository

```bash
git clone https://github.com/yourusername/silvercare-ai.git

cd silvercare-ai
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If you don't have a requirements file:

```bash
pip install django google-genai python-dotenv
```

---

# Google Gemini API Setup

Create a **.env** file in the project root.

```
GEMINI_API_KEY=your_api_key_here
```

You can obtain a free API key from:

https://aistudio.google.com/

---

# Database Setup

Run migrations:

```bash
python manage.py makemigrations

python manage.py migrate
```

---

# Run the Project

```bash
python manage.py runserver
```

Open:

```
http://127.0.0.1:8000/
```

Allow microphone permission when prompted.

---

# Usage

## Register

Create a new account.

Each account has completely isolated health records.

---

## Add Medication

Navigate to:

```
Manage Records
```

Add:

- Medication Name
- Dosage
- Time

---

## Add Appointment

Create upcoming appointments including:

- Doctor Name
- Date
- Time
- Notes

---

## Talk with SilverCare AI

Open the **Companion** page.

You can:

- Speak naturally
- Type messages
- Ask health-related questions
- Receive proactive reminders

---

# How Proactive Alerts Work

SilverCare AI continuously checks upcoming schedules.

It automatically provides:

| Alert Type | Notification Time |
|------------|------------------|
| Medication | 5 minutes before |
| Appointment | 1 hour before |

No manual interaction is required.

---

# Security

SilverCare AI follows a secure, authenticated architecture.

### User Isolation

Every request is associated with the logged-in user.

Example:

User A

```
Medication:
Blood Pressure Tablet
```

User B

```
Medication:
Vitamin D
```

Neither user can access the other's information.

---

## AI Tool Scoping

The Gemini agent never receives unrestricted database access.

Instead, it only accesses:

- Current user's medications
- Current user's appointments
- Current user's health records

This prevents accidental data leakage across users.

---

# Accessibility Features

Designed for senior citizens with:

- High contrast interface
- Large text
- Simple layouts
- Voice interaction
- Minimal clicks
- Easy navigation

---

# Demo Workflow

### Step 1

Register a new account.

---

### Step 2

Add a medication scheduled **2–5 minutes ahead**.

Example:

```
Medicine:
Aspirin

Time:
2 minutes from now
```

---

### Step 3

Keep the Companion page open.

---

### Step 4

Wait until the reminder time.

SilverCare AI will automatically announce:

> "It's time to take your Aspirin."

---

### Step 5

Log out.

Create another account.

Notice that no medications or appointments from the previous account are visible, demonstrating secure multi-tenant isolation.

---

# Future Improvements

- Wearable device integration
- Emergency SOS calling
- Family caregiver dashboard
- Medication adherence analytics
- AI health insights
- Smart prescription scanning
- Calendar synchronization
- Cloud backup support
- WhatsApp reminders
- Multi-language voice support

---

# Why SilverCare AI?

Many reminder applications only react when users open the app.

SilverCare AI is different.

It actively watches schedules, proactively reminds users, understands natural language, and provides an accessible experience tailored for senior citizens while maintaining strong privacy through authenticated AI tools.

---

# Acknowledgements

- Google Gemini API
- Django Framework
- Web Speech API
- SQLite
- Kaggle AI Agents Intensive Capstone

---

# Developed For

**Kaggle AI Agents: Intensive Vibe Coding Capstone (Agents for Good Track)**

**July 2026**

---

## License

This project is intended for educational and hackathon purposes.

Feel free to fork, improve, and build upon it.
