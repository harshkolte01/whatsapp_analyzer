import re
from collections import Counter
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download VADER lexicon (run once)
nltk.download('vader_lexicon', quiet=True)

# Initialize VADER sentiment analyzer
sid = SentimentIntensityAnalyzer()

# Language-specific keyword dictionaries for mood indication (transliterated)
mood_keywords = {
    'english': {
        'positive': ['love', 'great', 'happy', 'lol', 'yay', 'awesome'],
        'negative': ['hate', 'ugh', 'bad', 'sad', 'terrible', 'nope'],
        'emotions': {
            'happy': ['happy', 'joy', 'lol', 'haha'],
            'angry': ['angry', 'hate', 'ugh', 'grr'],
            'sad': ['sad', 'cry', 'tears', 'sigh'],
            'excited': ['wow', 'yay', 'excited', 'yes'],
            'anxious': ['nervous', 'worried', 'oh no', 'help']
        }
    },
    'hindi': {
        'positive': ['pyaar', 'shandaar', 'khush', 'haha', 'vaah'],
        'negative': ['nafrat', 'uf', 'bura', 'dukhi', 'kharab'],
        'emotions': {
            'happy': ['khush', 'haha', 'maza'],
            'angry': ['gussa', 'nafrat', 'uf'],
            'sad': ['dukhi', 'rona', 'aansu'],
            'excited': ['vaah', 'yes', 'romanchit'],
            'anxious': ['chintit', 'dar', 'becheyn']
        }
    },
    'gujarati': {
        'positive': ['prem', 'shandaar', 'khush', 'haha', 'vaah'],
        'negative': ['ghruna', 'uf', 'kharab', 'dukhii', 'na'],
        'emotions': {
            'happy': ['khush', 'haha', 'maja'],
            'angry': ['gussey', 'ghruna', 'uf'],
            'sad': ['dukhii', 'radvu', 'aansu'],
            'excited': ['vaah', 'ha', 'utsahit'],
            'anxious': ['chintit', 'dar', 'becheyn']
        }
    }
}

def detect_language(text):
    """Detect the primary language of the text (simple heuristic)."""
    text = text.lower()
    if re.search(r'pyaar|khush|gussa|uf', text):  # Hindi transliteration
        return 'hindi'
    elif re.search(r'prem|khush|gussey|uf', text):  # Gujarati transliteration
        return 'gujarati'
    else:
        return 'english'

def analyze_vibe(chat_data):
    """
    Analyze the vibe of the chat based on sentiment, emotions, and keywords.
    Returns a summary dictionary.
    """
    if not chat_data:
        return {"message": "No chat data available."}

    sentiment_scores = {'positive': 0, 'negative': 0, 'neutral': 0}
    emotion_counts = {'happy': 0, 'angry': 0, 'sad': 0, 'excited': 0, 'anxious': 0}
    contextual_tone = {'sarcasm': 0, 'slang': 0}

    for entry in chat_data:
        message = entry.get('message', '').lower()
        if not message:
            continue

        # Detect language
        lang = detect_language(message)
        keywords = mood_keywords.get(lang, mood_keywords['english'])

        # Sentiment Analysis with VADER
        sentiment = sid.polarity_scores(message)
        if sentiment['compound'] >= 0.05:
            sentiment_scores['positive'] += 1
        elif sentiment['compound'] <= -0.05:
            sentiment_scores['negative'] += 1
        else:
            sentiment_scores['neutral'] += 1

        # Emotion Detection
        for emotion, emotion_words in keywords['emotions'].items():
            for word in emotion_words:
                if word in message:
                    emotion_counts[emotion] += 1

        # Contextual Tone (Sarcasm and Slang)
        if re.search(r'\b(not|never|no)\s+(good|great|awesome)\b', message) or 'haha' in message:
            contextual_tone['sarcasm'] += 1
        if any(slang in message for slang in ['lol', 'wtf', 'bruh', 'haha', 'ha']):
            contextual_tone['slang'] += 1

        # Keyword Spotting
        for word in keywords['positive']:
            if word in message:
                sentiment_scores['positive'] += 1
        for word in keywords['negative']:
            if word in message:
                sentiment_scores['negative'] += 1

    # Normalize scores
    total_messages = sum(sentiment_scores.values())
    sentiment_scores = {k: (v / total_messages * 100) if total_messages else 0 for k, v in sentiment_scores.items()}
    emotion_counts = {k: v for k, v in emotion_counts.items()}  # Raw counts for simplicity

    # Determine overall vibe
    dominant_sentiment = max(sentiment_scores, key=sentiment_scores.get)
    dominant_emotion = max(emotion_counts, key=emotion_counts.get) if any(emotion_counts.values()) else 'neutral'

    return {
        "sentiment_analysis": sentiment_scores,
        "emotion_detection": emotion_counts,
        "contextual_tone": contextual_tone,
        "dominant_sentiment": dominant_sentiment,
        "dominant_emotion": dominant_emotion,
        "vibe_summary": f"The group vibe is {dominant_sentiment} with a {dominant_emotion} undertone, influenced by {'sarcastic ' if contextual_tone['sarcasm'] > 0 else ''}{'slang-heavy ' if contextual_tone['slang'] > 0 else ''}conversations."
    }