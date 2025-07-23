import re

def load_chat_data(uploaded_file):
    chat_data = []
    content = uploaded_file.getvalue().decode("utf-8")
    lines = content.split('\n')
    
    # Updated regex to match 'dd/mm/yy, hh:mm pm - Name: message'
    pattern = r'(\d{2}/\d{2}/\d{2}), (\d{1,2}:\d{2}\s?(?:am|pm)) - (.*?): (.*)'
    for line in lines:
        match = re.match(pattern, line.strip())
        if match:
            date, time, user, message = match.groups()
            # Convert 2-digit year to 4-digit and format as dd/mm/yyyy
            day, month, year = date.split('/')
            full_year = f"20{year}" if int(year) < 100 else year
            date = f"{day}/{month}/{full_year}"
            # Normalize time to 24h format if pm/am is present
            time = time.replace(' ', ' ').strip()
            if 'pm' in time.lower() and time.split(':')[0] != '12':
                hours = (int(time.split(':')[0]) + 12) % 24
                time = f"{hours}:{time.split(':')[1].replace('pm', '').strip()}"
            elif 'am' in time.lower() and time.split(':')[0] == '12':
                time = f"0:{time.split(':')[1].replace('am', '').strip()}"
            else:
                time = time.replace('am', '').replace('pm', '').strip()
            
            chat_data.append({
                'date': date,
                'time': time,
                'user': user,
                'message': message
            })
        # Handle deleted or system messages
        elif "deleted" in line or "created" in line:
            match = re.match(r'(\d{2}/\d{2}/\d{2}), (\d{1,2}:\d{2}\s?(?:am|pm)) - (.*)', line.strip())
            if match:
                date, time, content = match.groups()
                day, month, year = date.split('/')
                full_year = f"20{year}" if int(year) < 100 else year
                date = f"{day}/{month}/{full_year}"
                time = time.replace(' ', ' ').strip()
                if 'pm' in time.lower() and time.split(':')[0] != '12':
                    hours = (int(time.split(':')[0]) + 12) % 24
                    time = f"{hours}:{time.split(':')[1].replace('pm', '').strip()}"
                elif 'am' in time.lower() and time.split(':')[0] == '12':
                    time = f"0:{time.split(':')[1].replace('am', '').strip()}"
                else:
                    time = time.replace('am', '').replace('pm', '').strip()
                chat_data.append({
                    'date': date,
                    'time': time,
                    'user': None,
                    'message': content
                })
    
    return chat_data if chat_data else []