# 🩺 CareSync - AI-Powered Personal Wellness Tracker

CareSync is a comprehensive wellness companion that combines medication adherence tracking with mental health journaling and AI-powered insights.

## ✨ Features

### 💊 Medication Management

- **Medication Tracker**: Add, schedule, and track daily medications
- **AI Symptom Checker**: Get personalized insights about medication side effects
- **Smart Reminders**: Visual alerts for overdue and upcoming medications
- **Adherence Tracking**: Monitor your medication compliance over time

### 🧠 Mental Health & Wellness

- **Mood Tracker**: Daily mood logging with emoji-based interface
- **Journaling**: Quick thoughts and detailed daily reflections
- **AI Reflection**: Get AI-powered insights on your journal entries
- **Mood Trends**: Visualize your emotional patterns over time

### 📊 AI-Powered Insights

- **Weekly Summaries**: AI-generated wellness summaries
- **Pattern Recognition**: Identify connections between mood and medication adherence
- **Personalized Suggestions**: Gentle, supportive recommendations

### 🔔 Advanced Notifications

- **Email Notifications**: Configure SMTP for email reminders
- **Desktop Notifications**: System alerts for medication reminders
- **Mobile Notifications**: Framework for mobile push notifications
- **Customizable Settings**: Choose which notification types to enable

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project**

   ```bash
   cd CareSync
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**

   ```bash
   streamlit run main.py
   ```

5. **Open your browser**
   - Local URL: http://localhost:8501
   - The app will automatically open in your default browser

## 🔧 Configuration

### AI Integration (Optional)

For real AI responses instead of demo responses:

1. **Get an OpenAI API key** from [OpenAI Platform](https://platform.openai.com/)
2. **Create a `.streamlit/secrets.toml` file** in your project root:
   ```toml
   openai_api_key = "your-api-key-here"
   ```

### Email Notifications (Optional)

To enable email notifications:

1. **Use Gmail App Password** (recommended for security)
2. **Configure in the Settings tab**:
   - Enable Email Notifications
   - Enter your email address
   - Enter your Gmail App Password

## 📱 Usage Guide

### Home Dashboard

- **Overview**: See today's medications and quick mood/journal input
- **Reminder Status**: Check for overdue or upcoming medications
- **Wellness Status**: AI-generated wellness summary

### Medication Tracker

- **Add Medications**: Name, dose, frequency, and reminder time
- **Track Adherence**: Mark medications as taken or missed
- **AI Symptom Analysis**: Get insights about medication reactions

### Mood & Journal

- **Mood Tracking**: Select your daily mood with emoji interface
- **Journaling**: Write quick thoughts or detailed reflections
- **AI Reflection**: Get AI analysis of your journal entries

### Insights

- **Mood Trends**: Visual charts of your emotional patterns
- **AI Summaries**: Weekly wellness summaries and patterns
- **Adherence Charts**: Medication compliance over time

### Settings

- **Notification Configuration**: Set up email, desktop, and mobile notifications
- **Test Notifications**: Verify your notification setup
- **AI Settings**: Configure OpenAI API for real AI responses

## 🛡️ Privacy & Security

- **Local Storage**: All data is stored locally in SQLite database
- **No Cloud Sync**: Your data stays on your device
- **Optional AI**: AI features work with demo responses without API key
- **Secure Notifications**: Email notifications use secure SMTP

## ⚠️ Important Disclaimers

- **Not Medical Advice**: This app is for wellness tracking only
- **Consult Healthcare Providers**: For medical concerns, consult professionals
- **Data Backup**: Consider backing up your local database regularly
- **AI Limitations**: AI insights are supportive, not diagnostic

## 🛠️ Technical Details

### Architecture

- **Frontend**: Streamlit web interface
- **Backend**: Python with SQLite database
- **AI**: OpenAI GPT-4o integration with fallback responses
- **Notifications**: Multi-channel notification system

### File Structure

```
CareSync/
├── main.py                 # Entry point
├── caresync/
│   ├── app.py             # Main Streamlit app
│   ├── common/            # Shared utilities
│   │   ├── database.py    # SQLite database operations
│   │   ├── notifications.py # Notification system
│   │   └── utils.py       # AI and utility functions
│   ├── medication/        # Medication tracking features
│   │   ├── med_schedule.py
│   │   └── side_effects_ai.py
│   └── mental_health/     # Mental health features
│       ├── mood_tracker.py
│       ├── journal.py
│       └── mood_trends.py
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🤝 Contributing

This is a personal wellness project. Feel free to:

- Report bugs or issues
- Suggest new features
- Improve the documentation
- Share your experience

## 📄 License

This project is for educational and personal use. Please respect privacy and medical ethics when using or modifying this application.

---

**Take care of yourself! 💙** CareSync is here to support your wellness journey.
