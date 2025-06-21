import streamlit as st
import openai
from datetime import date
from common import database

# Try to get OpenAI API key
try:
    openai.api_key = st.secrets["openai_api_key"]
    AI_ENABLED = True
except:
    openai.api_key = None
    AI_ENABLED = False

# Mock AI responses for free usage (fallback)
MOCK_SYMPTOM_RESPONSES = [
    "That sounds like a common reaction. Try staying hydrated and getting some rest. If symptoms persist, consider consulting your healthcare provider.",
    "This could be a side effect. Monitor your symptoms and stay well-hydrated. Contact your doctor if you're concerned.",
    "Your reaction seems mild. Rest and hydration often help. Keep track of any changes and discuss with your healthcare provider if needed."
]

MOCK_JOURNAL_RESPONSES = [
    "I notice you're expressing some concerns. Remember to be kind to yourself and consider reaching out to friends or family for support.",
    "Your feelings are valid. Sometimes writing helps process emotions. Consider what small steps might help you feel better today.",
    "Thank you for sharing. It's important to acknowledge your emotions. What's one thing that might bring you comfort today?"
]

MOCK_INSIGHTS = [
    "You've been consistent with your mood tracking this week. That's great self-awareness!",
    "I notice some patterns in your entries. Consider what might be contributing to your current state.",
    "Your wellness journey is unique. Keep up the good work with your daily reflections."
]

def get_today():
    return date.today().isoformat()

def gpt_ask(prompt, system=None, model="gpt-4o"):
    """Real GPT function with fallback to mock responses"""
    if AI_ENABLED and openai.api_key:
        try:
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})
            
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=0.7,
                max_tokens=300
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            st.warning(f"AI API error: {str(e)}. Using fallback response.")
            return _get_mock_response(prompt)
    else:
        return _get_mock_response(prompt)

def _get_mock_response(prompt):
    """Get appropriate mock response based on prompt content"""
    import random
    prompt_lower = prompt.lower()
    
    if any(word in prompt_lower for word in ["symptom", "medication", "side effect", "reaction"]):
        return random.choice(MOCK_SYMPTOM_RESPONSES)
    elif any(word in prompt_lower for word in ["journal", "mood", "feeling", "emotion"]):
        return random.choice(MOCK_JOURNAL_RESPONSES)
    else:
        return random.choice(MOCK_INSIGHTS)

@st.cache_data(show_spinner=False)
def cache_ai_summary(prompt, system=None):
    return gpt_ask(prompt, system)

def show_ai_insights():
    st.subheader("AI Insights")
    
    # Show AI status
    if AI_ENABLED and openai.api_key:
        st.success("🤖 Real AI enabled")
    else:
        st.info("🤖 Using demo AI responses (add OpenAI API key for real AI)")
    
    moods = database.get_moods()
    journals = database.get_journals()
    meds, logs = database.get_today_medications()
    
    if not moods and not journals:
        st.info("Not enough data for insights.")
        return
    
    mood_text = "\n".join([f"{d}: {e} ({s})" for s, e, d in moods])
    journal_text = "\n".join([f"{d}: {j}" for j, d in journals])
    prompt = f"Here are the user's recent moods:\n{mood_text}\n\nAnd recent journal entries:\n{journal_text}\n\nGenerate a friendly weekly summary, highlight any patterns (e.g. mood drops after missed meds), and offer a gentle suggestion."
    system = "You are a wellness assistant. Summarize the user's week, spot patterns, and give gentle, non-medical suggestions."
    
    if st.button("Generate Weekly AI Summary"):
        with st.spinner("Generating insights..."):
            summary = cache_ai_summary(prompt, system)
        st.success("AI Weekly Summary:")
        st.write(summary) 