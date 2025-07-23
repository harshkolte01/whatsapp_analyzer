import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import re
from datetime import datetime, timedelta

def create_visualizations(chat_data, person_data, selected_person=None):
    if selected_person and selected_person != "Overall":
        data = person_data.get(selected_person, [])
    else:
        data = chat_data

    # Monthly Timeline (Line Graph)
    monthly_counts = Counter(
        datetime.strptime(entry['date'], '%d/%m/%Y').strftime('%Y-%m')
        for entry in data if entry.get('date')
    )
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(list(monthly_counts.keys()), list(monthly_counts.values()), marker='o')
    ax1.set_title("Monthly Timeline", color='darkblue')
    plt.xticks(rotation=45, ha='right')
    plt.xlabel("Months", color='darkgreen')
    plt.ylabel("Message Count", color='darkgreen')

    # Daily Timeline (Last 10 Days from last chat date)
    daily_counts = Counter(
        datetime.strptime(entry['date'], '%d/%m/%Y').strftime('%Y-%m-%d')
        for entry in data if entry.get('date')
    )
    # Find the last date in the chat data
    date_objs = [
        datetime.strptime(entry['date'], '%d/%m/%Y')
        for entry in data if entry.get('date')
    ]
    # If dates exist, use the latest; else fallback to today
    if date_objs:
        last_date = max(date_objs)
    else:
        last_date = datetime.today()
    # Generate last 10 days from last_date
    last_10_days = [
        (last_date - timedelta(days=i)).strftime('%Y-%m-%d')
        for i in range(9, -1, -1)
    ]
    filtered_daily_counts = {date: daily_counts.get(date, 0) for date in last_10_days}
    fig2, ax2 = plt.subplots(figsize=(12, 5))
    ax2.bar(filtered_daily_counts.keys(), filtered_daily_counts.values())
    ax2.set_title("Daily Timeline (Last 10 Days)", color='darkblue')
    plt.xticks(rotation=90, ha='right')
    plt.xlabel("Dates", color='darkgreen')
    plt.ylabel("Message Count", color='darkgreen')

    # Activity Map (Pie Chart for Days)
    days = Counter(
        datetime.strptime(entry['date'], '%d/%m/%Y').strftime('%A')
        for entry in data if entry.get('date')
    )
    fig3, ax3 = plt.subplots(figsize=(6, 6))
    ax3.pie(days.values(), labels=days.keys(), autopct='%1.1f%%', startangle=90, colors=plt.cm.Pastel1.colors)
    ax3.set_title("Activity Map (Days)", color='darkblue')

    # Most Busy User (Pie Chart)
    user_counts = Counter(entry['user'] for entry in chat_data if entry.get('user'))
    total_messages = sum(user_counts.values())
    most_busy_user_data = {user: (count / total_messages * 100) for user, count in user_counts.items() if count > 0}
    fig4, ax4 = plt.subplots(figsize=(6, 6))
    ax4.pie(most_busy_user_data.values(), labels=most_busy_user_data.keys(), autopct='%1.1f%%', startangle=90, colors=plt.cm.Pastel2.colors)
    ax4.set_title("Most Busy User", color='darkblue')

    # Wordcloud
    words = ' '.join(entry['message'] for entry in data if entry.get('message'))
    wordcloud = WordCloud(width=800, height=400).generate(words) if words else WordCloud(width=800, height=400).generate("No data")
    fig5, ax5 = plt.subplots()
    ax5.imshow(wordcloud, interpolation='bilinear')
    ax5.axis('off')
    ax5.set_title("Wordcloud", color='darkblue')

    # Most Common Words
    word_freq = Counter(re.findall(r'\w+', words)) if words else Counter()
    common_words = word_freq.most_common(10)  # Limit to top 10 for readability
    fig6, ax6 = plt.subplots(figsize=(10, 5))
    ax6.bar([word[0] for word in common_words], [word[1] for word in common_words])
    ax6.set_title("Most Common Words", color='darkblue')
    plt.xticks(rotation=45, ha='right')
    plt.xlabel("Words", color='darkgreen')
    plt.ylabel("Frequency", color='darkgreen')

    # Emoji Analysis
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F6FF"
        u"\U0001F1E0-\U0001F1FF"
        "]+", flags=re.UNICODE)
    emojis = Counter(
        emoji
        for entry in data if entry.get('message')
        for emoji in emoji_pattern.findall(entry['message'])
    )
    top_emojis = emojis.most_common(5)
    fig7, ax7 = plt.subplots(figsize=(6, 6))
    ax7.bar([emoji[0] for emoji in top_emojis], [count[1] for count in top_emojis])
    ax7.set_title("Emoji Analysis", color='darkblue')
    plt.xticks(rotation=45, ha='right')
    plt.xlabel("Emojis", color='darkgreen')
    plt.ylabel("Count", color='darkgreen')

    return {
        "monthly_timeline": fig1,
        "daily_timeline": fig2,
        "activity_map": fig3,
        "most_busy_user": fig4,
        "wordcloud": fig5,
        "most_common_words": fig6,
        "emoji_analysis": fig7
    }
