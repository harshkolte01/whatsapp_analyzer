import streamlit as st
import matplotlib.pyplot as plt
from src.data_loader import load_chat_data
from src.person_splitter import split_by_person
from src.stats_calculator import calculate_stats
from src.visualizer import create_visualizations
from src.vibeCheck import analyze_vibe

st.set_page_config(page_title="WhatsApp Chat Analyzer", layout="wide")
st.markdown(
    """
    <style>
    .main {
        background-color: #1a1d23;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    .stButton>button {
        background-color: #4a90e2;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        border: none;
        transition: background-color 0.3s;
    }
    .stButton>button:hover {
        background-color: #357abd;
    }
    .stHeader {
        color: #ffffff;
        font-size: 2.8em;
        text-align: center;
        margin-bottom: 25px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    .stSubheader {
        color: #d3d3d3;
        font-size: 1.6em;
        margin-top: 25px;
        border-bottom: 2px solid #4a90e2;
        padding-bottom: 5px;
    }
    .vibe-text {
        color: #e0e0e0;
        font-size: 1.2em;
        margin: 10px 0;
        line-height: 1.5;
    }
    .sidebar .stHeader {
        color: #d3d3d3;
        font-size: 1.8em;
        margin-bottom: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar for upload and selection
st.sidebar.markdown('<div class="stHeader">Controls</div>', unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("Upload your WhatsApp chat backup .txt file", type="txt", key="file_uploader")
if uploaded_file is not None:
    chat_data = load_chat_data(uploaded_file)
    person_data = split_by_person(chat_data)
    selected_person = st.sidebar.selectbox("Select a person for analysis", list(person_data.keys()) + ["Overall"], key="person_select")
else:
    selected_person = "Overall"

# Main page content
st.markdown('<div class="stHeader">WhatsApp Chat Analyzer</div>', unsafe_allow_html=True)

if uploaded_file is not None:
    # Overall statistics
    overall_stats = calculate_stats(chat_data)
    st.markdown('<div class="stSubheader">Overall Statistics</div>', unsafe_allow_html=True)
    st.write(f"Total Messages: {overall_stats['total_messages']}")
    st.write(f"Total Words: {overall_stats['total_words']}")
    st.write(f"Media Shared: {overall_stats['total_media']}")
    st.write(f"Links Shared: {overall_stats['total_links']}")
    
    if selected_person != "Overall":
        person_stats = calculate_stats(person_data[selected_person])
        st.markdown(f'<div class="stSubheader">Statistics for {selected_person}</div>', unsafe_allow_html=True)
        st.write(f"Total Messages: {person_stats['total_messages']}")
        st.write(f"Total Words: {person_stats['total_words']}")
        st.write(f"Media Shared: {person_stats['total_media']}")
        st.write(f"Links Shared: {person_stats['total_links']}")
    
    # Timelines and Activity
    visualizations = create_visualizations(chat_data, person_data, selected_person)
    st.markdown('<div class="stSubheader">Monthly Timeline</div>', unsafe_allow_html=True)
    st.pyplot(visualizations["monthly_timeline"])  # Removed figsize here
    
    st.markdown('<div class="stSubheader">Daily Timeline (Last 10 Days)</div>', unsafe_allow_html=True)
    st.pyplot(visualizations["daily_timeline"])    # Removed figsize here
    
    st.markdown('<div class="stSubheader">Activity Map (Days)</div>', unsafe_allow_html=True)
    st.pyplot(visualizations["activity_map"])      # Removed figsize here
    
    st.markdown('<div class="stSubheader">Most Busy User</div>', unsafe_allow_html=True)
    st.pyplot(visualizations["most_busy_user"])    # Removed figsize here
    
    st.markdown('<div class="stSubheader">Wordcloud</div>', unsafe_allow_html=True)
    st.pyplot(visualizations["wordcloud"])         # Removed figsize here
    
    st.markdown('<div class="stSubheader">Most Common Words</div>', unsafe_allow_html=True)
    st.pyplot(visualizations["most_common_words"]) # Removed figsize here
    
    st.markdown('<div class="stSubheader">Emoji Analysis</div>', unsafe_allow_html=True)
    st.pyplot(visualizations["emoji_analysis"])    # Removed figsize here
    
    # Vibe Check
    st.markdown('<div class="stSubheader">Vibe Check</div>', unsafe_allow_html=True)
    vibe = analyze_vibe(chat_data if selected_person == "Overall" else person_data.get(selected_person, []))
    
    # Pie Chart
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    wedges, texts, autotexts = ax1.pie(
        [vibe['sentiment_analysis']['positive'], vibe['sentiment_analysis']['negative'], vibe['sentiment_analysis']['neutral']],
        labels=['Positive', 'Negative', 'Neutral'],
        autopct='%1.1f%%',
        colors=['#2ecc71', '#e74c3c', '#3498db'],
        startangle=90,
        wedgeprops={'edgecolor': 'white'},
        textprops={'color': 'white'}
    )
    plt.setp(autotexts, size=10, weight="bold")
    ax1.legend(wedges, ['Positive', 'Negative', 'Neutral'], loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), frameon=False, labelcolor='black')
    ax1.set_title("Sentiment Distribution", color='white', fontsize=14, pad=15)
    ax1.set_xlabel("Sentiment Type", color='white', fontsize=12)
    ax1.set_ylabel("Percentage", color='white', fontsize=12)
    st.pyplot(fig1)  
    
    st.markdown('<div class="vibe-text">Dominant Sentiment: {dominant_sentiment} ({sentiment:.1f}%)</div>'.format(
        dominant_sentiment=vibe['dominant_sentiment'],
        sentiment=vibe['sentiment_analysis'][vibe['dominant_sentiment']]), unsafe_allow_html=True)
    st.markdown('<div class="vibe-text">Dominant Emotion: {dominant_emotion}</div>'.format(
        dominant_emotion=vibe['dominant_emotion']), unsafe_allow_html=True)
    st.markdown('<div class="vibe-text">Vibe Summary: {summary}</div>'.format(
        summary=vibe['vibe_summary']), unsafe_allow_html=True)
