import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import json
from datetime import datetime
import os

class NotificationManager:
    def __init__(self):
        self.email_enabled = False
        self.desktop_enabled = False
        self.mobile_enabled = False
        self.load_settings()
    
    def load_settings(self):
        """Load notification settings from session state"""
        if 'notification_settings' not in st.session_state:
            st.session_state.notification_settings = {
                'email_enabled': False,
                'desktop_enabled': False,
                'mobile_enabled': False,
                'email_address': '',
                'email_password': '',
                'smtp_server': 'smtp.gmail.com',
                'smtp_port': 587
            }
    
    def setup_email_notifications(self, email, password, smtp_server="smtp.gmail.com", smtp_port=587):
        """Setup email notifications"""
        try:
            # Test email connection
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(email, password)
            server.quit()
            
            st.session_state.notification_settings.update({
                'email_enabled': True,
                'email_address': email,
                'email_password': password,
                'smtp_server': smtp_server,
                'smtp_port': smtp_port
            })
            return True
        except Exception as e:
            st.error(f"Email setup failed: {str(e)}")
            return False
    
    def send_email_notification(self, subject, message, recipient=None):
        """Send email notification"""
        if not st.session_state.notification_settings['email_enabled']:
            return False
        
        try:
            settings = st.session_state.notification_settings
            msg = MIMEMultipart()
            msg['From'] = settings['email_address']
            msg['To'] = recipient or settings['email_address']
            msg['Subject'] = subject
            
            body = f"""
            <html>
            <body>
                <h2>🩺 CareSync Reminder</h2>
                <p>{message}</p>
                <hr>
                <p><small>This is an automated reminder from CareSync. Please do not reply to this email.</small></p>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            server = smtplib.SMTP(settings['smtp_server'], settings['smtp_port'])
            server.starttls()
            server.login(settings['email_address'], settings['email_password'])
            server.send_message(msg)
            server.quit()
            
            return True
        except Exception as e:
            st.error(f"Failed to send email: {str(e)}")
            return False
    
    def send_desktop_notification(self, title, message):
        """Send desktop notification"""
        try:
            # For macOS
            os.system(f"""
            osascript -e 'display notification "{message}" with title "{title}"'
            """)
            return True
        except:
            try:
                # For Linux
                os.system(f'notify-send "{title}" "{message}"')
                return True
            except:
                try:
                    # For Windows
                    from plyer import notification
                    notification.notify(
                        title=title,
                        message=message,
                        app_icon=None,
                        timeout=10,
                    )
                    return True
                except:
                    return False
    
    def send_mobile_notification(self, title, message, user_id=None):
        """Send mobile notification via web push or SMS"""
        # This would integrate with services like:
        # - Firebase Cloud Messaging (FCM)
        # - Twilio SMS
        # - Pushbullet
        # For now, we'll simulate with a web-based approach
        
        try:
            # Simulate mobile notification (in real app, this would use FCM)
            st.info(f"📱 Mobile notification would be sent: {title} - {message}")
            return True
        except:
            return False
    
    def send_medication_reminder(self, medication_name, dose, time_str, reminder_type="all"):
        """Send medication reminder via selected channels"""
        title = "💊 Medication Reminder"
        message = f"Time to take {medication_name} ({dose}) at {time_str}"
        
        success_count = 0
        
        if reminder_type in ["all", "email"] and st.session_state.notification_settings['email_enabled']:
            if self.send_email_notification(title, message):
                success_count += 1
        
        if reminder_type in ["all", "desktop"] and st.session_state.notification_settings['desktop_enabled']:
            if self.send_desktop_notification(title, message):
                success_count += 1
        
        if reminder_type in ["all", "mobile"] and st.session_state.notification_settings['mobile_enabled']:
            if self.send_mobile_notification(title, message):
                success_count += 1
        
        return success_count > 0
    
    def check_and_send_reminders(self, medications):
        """Check medications and send reminders for due/overdue ones"""
        current_time = datetime.now()
        sent_reminders = []
        
        for med in medications:
            med_id, name, dose, freq, time_str = med
            try:
                med_time = datetime.strptime(time_str, "%H:%M:%S").time()
                med_datetime = datetime.combine(current_time.date(), med_time)
                time_diff = (med_datetime - current_time).total_seconds() / 60  # minutes
                
                # Send reminder if medication is due within 15 minutes or overdue
                if -30 <= time_diff <= 15:
                    if self.send_medication_reminder(name, dose, time_str):
                        sent_reminders.append((name, time_str))
            except:
                pass
        
        return sent_reminders

# Global notification manager instance
notification_manager = NotificationManager() 