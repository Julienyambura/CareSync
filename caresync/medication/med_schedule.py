import streamlit as st
from common import database
import pandas as pd
from datetime import datetime, time
from common.notifications import notification_manager

def show_today_schedule():
    database.init_db()
    meds, logs = database.get_today_medications()
    
    # Check for upcoming/overdue medications
    current_time = datetime.now().time()
    upcoming_meds = []
    overdue_meds = []
    
    for med in meds:
        med_id, name, dose, freq, time_str = med
        try:
            med_time = datetime.strptime(time_str, "%H:%M:%S").time()
            status = logs.get(med_id, None)
            
            if status is None:  # Not taken yet
                if med_time <= current_time:
                    overdue_meds.append((med_id, name, dose, freq, time_str))
                else:
                    upcoming_meds.append((med_id, name, dose, freq, time_str))
        except:
            pass
    
    # Send notifications for due/overdue medications
    if meds:
        sent_reminders = notification_manager.check_and_send_reminders(meds)
        if sent_reminders:
            st.info(f"🔔 Sent {len(sent_reminders)} reminder(s) for due medications")
    
    # Show overdue medications as urgent alerts
    if overdue_meds:
        st.markdown("### ⚠️ Overdue Medications")
        for med_id, name, dose, freq, time_str in overdue_meds:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%); 
                        padding: 1rem; border-radius: 10px; border-left: 4px solid #f44336;">
                <h4>🚨 {name} - {dose}</h4>
                <p><strong>Due:</strong> {time_str} • <strong>Status:</strong> Overdue</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"✅ Take Now", key=f"take_overdue_{med_id}", use_container_width=True):
                    database.log_medication(med_id, "taken")
                    st.success(f"✅ {name} marked as taken!")
                    st.rerun()
            with col2:
                if st.button(f"❌ Skip", key=f"skip_overdue_{med_id}", use_container_width=True):
                    database.log_medication(med_id, "missed")
                    st.warning(f"❌ {name} marked as missed")
                    st.rerun()
    
    # Show upcoming medications
    if upcoming_meds:
        st.markdown("### ⏰ Upcoming Medications")
        for med_id, name, dose, freq, time_str in upcoming_meds:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%); 
                        padding: 1rem; border-radius: 10px; border-left: 4px solid #4caf50;">
                <h4>⏰ {name} - {dose}</h4>
                <p><strong>Due:</strong> {time_str} • <strong>Status:</strong> Upcoming</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Show all medications with status
    if not meds:
        st.info("✨ No medications scheduled for today.")
        return
    
    st.markdown("### 📋 All Today's Medications")
    for med in meds:
        med_id, name, dose, freq, time_str = med
        status = logs.get(med_id, None)
        
        # Create a card for each medication
        with st.container():
            col1, col2, col3 = st.columns([3, 2, 2])
            with col1:
                st.markdown(f"**💊 {name}**")
                st.caption(f"{dose} • {freq} • {time_str}")
            
            with col2:
                if status == "taken":
                    st.markdown('<div class="success-card">✅ Taken</div>', unsafe_allow_html=True)
                elif status == "missed":
                    st.markdown('<div class="warning-card">❌ Missed</div>', unsafe_allow_html=True)
                else:
                    if st.button(f"✅ Mark Taken", key=f"taken_{med_id}", use_container_width=True):
                        database.log_medication(med_id, "taken")
                        st.success(f"✅ {name} marked as taken!")
                        st.rerun()
            
            with col3:
                if status is None:
                    if st.button(f"❌ Missed", key=f"missed_{med_id}", use_container_width=True):
                        database.log_medication(med_id, "missed")
                        st.warning(f"❌ {name} marked as missed")
                        st.rerun()
            st.markdown("---")

def medication_manager():
    st.subheader("➕ Add New Medication")
    
    with st.form("add_med_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Medication Name", placeholder="e.g., Aspirin")
            dose = st.text_input("Dose", placeholder="e.g., 100mg")
        with col2:
            freq = st.selectbox("Frequency", ["Once daily", "Twice daily", "Three times daily", "As needed"])
            time_input = st.time_input("Reminder Time")
        
        # Reminder settings
        st.markdown("### 🔔 Reminder Settings")
        col1, col2, col3 = st.columns(3)
        with col1:
            enable_reminder = st.checkbox("Enable reminders", value=True)
        with col2:
            reminder_offset = st.number_input("Remind (minutes) before", min_value=0, max_value=60, value=15)
        with col3:
            notification_type = st.selectbox("Notification Type", 
                                           ["All", "Email", "Desktop", "Mobile"],
                                           help="Choose which notifications to send")
        
        submitted = st.form_submit_button("➕ Add Medication", use_container_width=True)
        if submitted and name and dose:
            database.add_medication(name, dose, freq, str(time_input))
            st.success(f"✅ Added {name} successfully!")
            if enable_reminder:
                st.info(f"🔔 Reminder set for {time_input} via {notification_type.lower()} notifications")
            st.rerun()
    
    st.markdown("---")
    st.subheader("📋 Current Medications")
    meds, _ = database.get_today_medications()
    if meds:
        df = pd.DataFrame(meds, columns=["ID", "Name", "Dose", "Frequency", "Time"])
        st.dataframe(
            df.drop(columns=["ID"]),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No medications added yet. Add your first medication above!")

def plot_adherence():
    st.subheader("📈 Medication Adherence Over Time")
    # Placeholder: implement adherence graph using med_logs
    st.info("Adherence tracking will be available once you log some medications.")

def show_reminder_status():
    """Show current reminder status and upcoming medications"""
    st.markdown("### 🔔 Reminder Status")
    
    current_time = datetime.now()
    meds, logs = database.get_today_medications()
    
    if not meds:
        st.info("No medications to remind about.")
        return
    
    # Check for medications due soon
    due_soon = []
    for med in meds:
        med_id, name, dose, freq, time_str = med
        status = logs.get(med_id, None)
        
        if status is None:  # Not taken yet
            try:
                med_time = datetime.strptime(time_str, "%H:%M:%S").time()
                med_datetime = datetime.combine(current_time.date(), med_time)
                time_diff = (med_datetime - current_time).total_seconds() / 60  # minutes
                
                if -30 <= time_diff <= 30:  # Within 30 minutes
                    due_soon.append((name, dose, time_str, time_diff))
            except:
                pass
    
    if due_soon:
        st.markdown("### ⏰ Medications Due Soon")
        for name, dose, time_str, time_diff in due_soon:
            if time_diff < 0:
                status = "Overdue"
                color = "#f44336"
            else:
                status = f"Due in {int(time_diff)} minutes"
                color = "#ff9800"
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%); 
                        padding: 1rem; border-radius: 10px; border-left: 4px solid {color};">
                <h4>⏰ {name} - {dose}</h4>
                <p><strong>Time:</strong> {time_str} • <strong>Status:</strong> {status}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("✅ All medications are up to date!") 