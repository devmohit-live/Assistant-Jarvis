from basic import *
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from datetime import datetime, timedelta
import datefinder
scopes = ['https://www.googleapis.com/auth/calendar.events']
flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes=scopes)
import pickle
try:
    credentials = pickle.load(open("token.pkl", "rb"))
except Exception :
    speak('please follow this link to allow jarvis to vreate evnts')
    print('please follow this link to allow jarvis to vreate evnts\n')
    speak('Copy and paste the token to autorize the app')
    print('Copy and paste the token to autorize the app\n')
    credentials = flow.run_console()
    pickle.dump(credentials, open("token.pkl", "wb"))

service = build("calendar", "v3", credentials=credentials)

def create_event(start_time_str, summary, duration=1, description=None, location=None):
    matches = list(datefinder.find_dates(start_time_str))
    if len(matches):
        start_time = matches[0]
        end_time = start_time + timedelta(hours=duration)
    
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'Asia/Kolkata',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }
    return servicecal.events().insert(calendarId='primary', body=event).execute()

def crcal():
    x=input('Enter the date and time exapmle : 10 july 2PM')
    y=input('Enter teh Event Name  ')
    if create_event(x, y):
        print('You will be notified 1 day before via mail, and ten minutes before the event via popup')
        return True
