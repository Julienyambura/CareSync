import streamlit as st
from common import database
from common.utils import gpt_ask

def quick_journal():
    st.write("**How do you feel? (1-2 sentences)**")
    entry = st.text_area(
        "Quick thoughts for today",
        key="quick_journal",
        placeholder="e.g., Feeling a bit tired but hopeful about the day ahead...",
        max_chars=200,
        help="Share a brief reflection on your current state"
    )
    
    if entry:
        char_count = len(entry)
        st.caption(f"Characters: {char_count}/200")
        
        if st.button("💾 Save Quick Journal", use_container_width=True):
            database.add_journal(entry)
            st.success("✅ Journal entry saved!")
            st.balloons()

def journal_entry():
    st.write("**Write your thoughts for today**")
    entry = st.text_area(
        "Daily reflection",
        key="full_journal",
        placeholder="Share your thoughts, feelings, experiences, or anything on your mind...",
        height=150,
        help="Take your time to reflect on your day"
    )
    
    if entry:
        char_count = len(entry)
        st.caption(f"Characters: {char_count}")
        
        if st.button("💾 Save Journal Entry", use_container_width=True):
            database.add_journal(entry)
            st.success("✅ Journal entry saved!")
            st.balloons()

def gpt_reflection():
    st.write("**🤖 AI Reflection**")
    
    journals = database.get_journals()
    if not journals:
        st.info("📝 No journal entries yet. Write something first!")
        return
    
    # Show recent entries
    with st.expander("📖 Recent Journal Entries", expanded=False):
        for i, (entry, date) in enumerate(journals[:3]):
            st.markdown(f"**{date}:**")
            st.write(entry)
            if i < len(journals) - 1:
                st.markdown("---")
    
    last_entry = journals[0][0]
    st.markdown(f"**Latest entry:** {journals[0][1]}")
    
    if st.button("🧠 Analyze My Journal", use_container_width=True):
        with st.spinner("🤖 AI is reflecting on your entry..."):
            system = "You are a supportive assistant. Analyze the user's journal entry for emotional tone, repeated negative patterns, and offer a gentle suggestion if needed."
            reflection = gpt_ask(last_entry, system)
        
        st.markdown("### 💭 AI Reflection")
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); 
                    padding: 1rem; border-radius: 10px; border-left: 4px solid #2196F3;">
            {reflection}
        </div>
        """, unsafe_allow_html=True) 