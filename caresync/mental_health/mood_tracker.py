import streamlit as st
from common import database

MOODS = [
    ("😃", 5, "Great"),
    ("🙂", 4, "Good"),
    ("😐", 3, "Okay"),
    ("😔", 2, "Low"),
    ("😢", 1, "Bad")
]

def mood_input(key_suffix=""):
    st.write("**How are you feeling today?**")
    
    # Create mood selection with better styling
    mood_cols = st.columns(len(MOODS))
    selected_mood = None
    
    for i, (emoji, score, label) in enumerate(MOODS):
        with mood_cols[i]:
            if st.button(
                f"{emoji}\n{label}",
                key=f"mood_{score}_{key_suffix}",
                use_container_width=True,
                help=f"Rate: {score}/5"
            ):
                selected_mood = (emoji, score, label)
    
    # Show selected mood and log button
    if selected_mood:
        emoji, score, label = selected_mood
        st.markdown(f"**Selected:** {emoji} {label}")
        
        if st.button("📝 Log This Mood", key=f"log_mood{key_suffix}", use_container_width=True):
            database.add_mood(score, emoji)
            st.success(f"✅ Mood logged: {emoji} {label}")
            st.balloons()
    
    # Show today's mood if already logged
    else:
        # Check if mood was already logged today
        moods = database.get_moods()
        if moods and moods[0][2] == database.get_today():
            today_mood = moods[0]
            st.info(f"📊 Today's mood: {today_mood[1]} {today_mood[0]}") 