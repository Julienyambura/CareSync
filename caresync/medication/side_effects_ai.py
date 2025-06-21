import streamlit as st
from common.utils import gpt_ask

def symptom_checker():
    st.write("**🤖 AI Symptom Analysis**")
    st.caption("Share how you felt after taking your medication for personalized insights")
    
    with st.form("symptom_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            med_name = st.text_input(
                "Medication Name",
                placeholder="e.g., Aspirin, Ibuprofen"
            )
        with col2:
            severity = st.selectbox(
                "Symptom Severity",
                ["Mild", "Moderate", "Severe"],
                help="How intense are your symptoms?"
            )
        
        reaction = st.text_area(
            "How did you feel after taking it?",
            placeholder="Describe any symptoms, side effects, or changes you noticed...",
            height=100,
            help="Be as detailed as possible for better analysis"
        )
        
        submitted = st.form_submit_button("🔍 Analyze Symptoms", use_container_width=True)
        
        if submitted and med_name and reaction:
            system = f"You are a helpful assistant analyzing a reaction to {med_name}. The user said: '{reaction}'. Give friendly, informative insight without diagnosing. Suggest hydration, rest, or medical attention if needed."
            
            with st.spinner("🤖 AI is analyzing your symptoms..."):
                feedback = gpt_ask(reaction, system)
            
            st.markdown("### 💡 AI Analysis")
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%); 
                        padding: 1.5rem; border-radius: 10px; border-left: 4px solid #ff9800;">
                <h4>📋 Analysis for {med_name}</h4>
                <p><strong>Severity:</strong> {severity}</p>
                <p><strong>Your description:</strong> {reaction}</p>
                <hr>
                <h5>🤖 AI Feedback:</h5>
                {feedback}
            </div>
            """, unsafe_allow_html=True)
            
            # Additional recommendations
            st.markdown("### 💡 General Tips")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.info("💧 Stay hydrated")
            with col2:
                st.info("😴 Get adequate rest")
            with col3:
                st.info("📞 Contact doctor if concerned") 