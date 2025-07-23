import re

def calculate_stats(chat_data):
    total_messages = len(chat_data)
    total_words = sum(len(re.findall(r'\w+', entry['message'])) for entry in chat_data if entry['message'])
    total_media = sum(1 for entry in chat_data if "image omitted" in entry['message'] or "video omitted" in entry['message'])
    total_links = sum(1 for entry in chat_data if re.search(r'http[s]?://', entry['message']))
    
    return {
        'total_messages': total_messages,
        'total_words': total_words,
        'total_media': total_media,
        'total_links': total_links
    }