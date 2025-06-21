import streamlit as st
import plotly.graph_objs as go
from common import database

def plot_mood_trends():
    st.subheader("Mood Trends Over Time")
    moods = database.get_moods()
    if not moods:
        st.info("No mood data yet.")
        return
    dates = [m[2] for m in moods][::-1]
    scores = [m[0] for m in moods][::-1]
    emojis = [m[1] for m in moods][::-1]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=scores, mode='lines+markers', text=emojis, marker=dict(size=12)))
    fig.update_layout(yaxis=dict(range=[0,5], tickvals=[1,2,3,4,5]), xaxis_title="Date", yaxis_title="Mood (1-5)")
    st.plotly_chart(fig, use_container_width=True) 