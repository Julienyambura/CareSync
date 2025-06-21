import streamlit as st
from medication import med_schedule, side_effects_ai
from mental_health import mood_tracker, journal, mood_trends
from common import database, utils
from common.notifications import notification_manager

# Custom CSS for beautiful styling
st.set_page_config(
    page_title="CareSync", 
    page_icon="🩺", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    .success-card {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .warning-card {
        background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .disclaimer {
        background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f6;
        border-radius: 8px 8px 0px 0px;
        padding: 10px 16px;
        color: #262730;
    }
    .stTabs [aria-selected="true"] {
        background-color: #667eea;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Beautiful header
st.markdown("""
<div class="main-header">
    <h1>🩺 CareSync</h1>
    <p style="font-size: 1.2rem; margin: 0;">Your AI-powered wellness companion</p>
</div>
""", unsafe_allow_html=True)

# Navigation with better styling
TABS = ["🏠 Home", "💊 Medication Tracker", "🧠 Mood & Journal", "📊 Insights", "⚙️ Settings"]
tab_home, tab_meds, tab_mind, tab_insights, tab_settings = st.tabs(TABS)

with tab_home:
    st.markdown("### 🏠 Welcome to Your Wellness Dashboard")
    st.markdown("Here's your personalized overview for today.")
    
    # Reminder status at the top
    med_schedule.show_reminder_status()
    
    # Main content in columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.subheader("💊 Today's Medications")
        med_schedule.show_today_schedule()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.subheader("😊 Mood Picker")
        mood_tracker.mood_input("_home")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.subheader("📝 Quick Journal")
        journal.quick_journal()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Wellness status card
    st.markdown("""
    <div class="metric-card">
        <h3>Wellness Status</h3>
        <h2>🟢 Stable</h2>
        <p>Based on your recent logs and mood patterns</p>
    </div>
    """, unsafe_allow_html=True)

with tab_meds:
    st.markdown("### 💊 Medication Management")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        med_schedule.medication_manager()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        side_effects_ai.symptom_checker()
        st.markdown('</div>', unsafe_allow_html=True)

with tab_mind:
    st.markdown("### 🧠 Mental Health & Wellness")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        mood_tracker.mood_input("_mind")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        journal.journal_entry()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        journal.gpt_reflection()
        st.markdown('</div>', unsafe_allow_html=True)

with tab_insights:
    st.markdown("### 📊 Wellness Insights & Trends")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        mood_trends.plot_mood_trends()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        med_schedule.plot_adherence()
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    utils.show_ai_insights()
    st.markdown('</div>', unsafe_allow_html=True)

with tab_settings:
    st.markdown("### ⚙️ Notification Settings")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.subheader("📧 Email Notifications")
        
        email_enabled = st.checkbox("Enable Email Notifications", 
                                  value=st.session_state.notification_settings.get('email_enabled', False))
        
        if email_enabled:
            email = st.text_input("Email Address", 
                                value=st.session_state.notification_settings.get('email_address', ''),
                                type="email")
            password = st.text_input("App Password", 
                                   value=st.session_state.notification_settings.get('email_password', ''),
                                   type="password",
                                   help="Use Gmail App Password for security")
            
            if st.button("Test Email Setup"):
                if notification_manager.setup_email_notifications(email, password):
                    st.success("✅ Email notifications configured!")
                else:
                    st.error("❌ Email setup failed. Check your credentials.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.subheader("🖥️ Desktop Notifications")
        
        desktop_enabled = st.checkbox("Enable Desktop Notifications",
                                    value=st.session_state.notification_settings.get('desktop_enabled', False))
        
        if desktop_enabled:
            st.info("Desktop notifications will appear as system alerts.")
            if st.button("Test Desktop Notification"):
                if notification_manager.send_desktop_notification("CareSync Test", "Desktop notifications are working!"):
                    st.success("✅ Desktop notification sent!")
                else:
                    st.warning("⚠️ Desktop notifications may not be supported on this system.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Mobile notifications section
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.subheader("📱 Mobile Notifications")
    
    mobile_enabled = st.checkbox("Enable Mobile Notifications",
                               value=st.session_state.notification_settings.get('mobile_enabled', False))
    
    if mobile_enabled:
        st.info("Mobile notifications require additional setup with Firebase Cloud Messaging or similar service.")
        st.markdown("""
        **To enable mobile notifications:**
        1. Set up Firebase Cloud Messaging (FCM)
        2. Configure your mobile app
        3. Add FCM credentials to settings
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Test notifications
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.subheader("🧪 Test Notifications")
    
    if st.button("Send Test Reminder"):
        test_meds = [("Test Medication", "100mg", "09:00:00")]
        sent = notification_manager.send_medication_reminder("Test Medication", "100mg", "09:00:00")
        if sent:
            st.success("✅ Test notification sent!")
        else:
            st.warning("⚠️ No notifications configured or failed to send.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Beautiful disclaimer
st.markdown("""
<div class="disclaimer">
    <h4>⚠️ Important Notice</h4>
    <p>This is not medical advice. For serious concerns, consult a healthcare provider.</p>
</div>
""", unsafe_allow_html=True) 