from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import random

# Set up credentials and authorize API
SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'path/to/credentials.json'
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('calendar', 'v3', credentials=creds)

# Set up list of chores and family members
chores = ['Vacuuming', 'Dishes', 'Laundry', 'Garbage', 'Bathroom cleaning']
family_members = ['Alice', 'Bob', 'Charlie', 'Dave', 'Eve']

# Set up rotation schedule
num_weeks = 8
num_chores = len(chores)
num_family_members = len(family_members)
rotation = []
for i in range(num_weeks):
    week = []
    for j in range(num_chores):
        chore = chores[j]
        person = family_members[(i + j) % num_family_members]
        week.append((chore, person))
    random.shuffle(week)  # Randomize order of chores for each week
    rotation.append(week)

# Create calendar events for rotation
calendar_id = 'primary'  # Replace with your calendar ID
start_date = datetime.now().date()
for i in range(num_weeks):
    for j in range(num_chores):
        chore, person = rotation[i][j]
        start = start_date + timedelta(days=i*7 + j)
        end = start + timedelta(days=1)
        event = {
            'summary': chore + ' - ' + person,
            'start': {
                'dateTime': start.isoformat() + '-07:00',  # Replace with your timezone
                'timeZone': 'America/Los_Angeles',  # Replace with your timezone
            },
            'end': {
                'dateTime': end.isoformat() + '-07:00',  # Replace with your timezone
                'timeZone': 'America/Los_Angeles',  # Replace with your timezone
            },
        }
        service.events().insert(calendarId=calendar_id, body=event).execute()
