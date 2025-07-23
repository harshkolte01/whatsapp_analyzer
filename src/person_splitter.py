def split_by_person(chat_data):
    person_data = {}
    for entry in chat_data:
        user = entry['user']
        if user and user != "System":
            if user not in person_data:
                person_data[user] = []
            person_data[user].append(entry)
    return person_data