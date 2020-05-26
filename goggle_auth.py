from basic import *
# from __future__ import print_function
from googleapiclient import discovery
from googleapiclient.discovery import build
from googleapiclient import errors
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import httplib2
import os
import pickle
import os.path
import base64
from email.mime.text import MIMEText
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import mimetypes
import datefinder
from datetime import datetime, timedelta

# scopes = ['https://www.googleapis.com/auth/gmail.modify','https://www.googleapis.com/auth/calendar.events']
# scopes = ['https://www.googleapis.com/auth/gmail.modify']

flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes=scopes)

try:
    credentials = pickle.load(open("token.pkl", "rb"))
except Exception :
#     speak('please follow this link to allow jarvis to vreate evnts')
    print('please follow this link to allow jarvis to vreate evnts\n')
#     speak('Copy and paste the token to autorize the app')
    print('Copy and paste the token to autorize the app\n')
    credentials = flow.run_console()
    pickle.dump(credentials, open("token.pkl", "wb"))

servicecal = build("calendar", "v3", credentials=credentials)
serviceml = build("gmail", "v1", credentials=credentials)

# <------------------------Calendar----------------------------->

def view_event():
    result = servicecal.events().list(calendarId='primary',orderBy='updated').execute()
    for i in range(len(result)):
        print('Summary : '+result['items'][i]['summary'])
        try:
            print('Description : '+result['items'][i]['description'])
        except Exception:
            print('No description available')
        try:
            print('Starts at : '+result['items'][i]['start']['dateTime']+'\n')
        except Exception:
            print('No start time found')
# view_event()

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



# <-----------------------------Mail--------------------------------->

# sending--------------->

def CreateMessage(sender, to, subject, message_text):
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}


def SendMessage(serviceml, user_id, message):
  try:
    message = (serviceml.users().messages().send(userId=user_id, body=message)
               .execute())
    print('Message Id: %s' %message['id'])
    return message
  except errors.HttpError as error:
    print('An error occurred: %s' % error)


# receiving------->

def ListMessagesWithLabels(serviceml, user_id, label_ids=[]):
  try:
    response = serviceml.users().messages().list(userId=user_id,
                                               labelIds=label_ids).execute()
    messages = []
    if 'messages' in response:
      messages.extend(response['messages'])

    while 'nextPageToken' in response:
      page_token = response['nextPageToken']
      response = serviceml.users().messages().list(userId=user_id,
                                                 labelIds=label_ids,
                                                 pageToken=page_token).execute()
      messages.extend(response['messages'])

    return messages
  except errors.HttpError as error:
    print('An error occurred: %s' % error)

def GetAttachments(service, user_id, msg_id, prefix=""):
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id).execute()

        for part in message['payload']['parts']:
            if part['filename']:
                #print('No attachemnet')
                if 'data' in part['body']:
                    data=part['body']['data']
                else:
                    print('Attachment Found, want to download it?')
                    x=input('Enter y to download ').lower()
                    if x=='y':
                        att_id=part['body']['attachmentId']
                        att=service.users().messages().attachments().get(userId=user_id, messageId=msg_id,id=att_id).execute()
                        data=att['data']
                        file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
                        path = prefix+part['filename']

                        with open(path, 'wb+') as f:
                            f.write(file_data)
                            print('Download Done\n')

                    else:
                        print('Download Ignored\n')
                        
    except errors.HttpError as error:
        print('An error occurred: %s' % error)


def ModifyMessage(service, user_id, msg_id, msg_labels):
    
  try:
    message = service.users().messages().modify(userId=user_id, id=msg_id,body=msg_labels).execute()
    label_ids = message['labelIds']
  except errors.HttpError as error:
    print('An error occurred: in label %s' % error)

def receive_mail():
    a=ListMessagesWithLabels(serviceml, 'me', label_ids=['INBOX','UNREAD'])
    if not a:
        print("No messages found.")
    else:
        print("Message snippets:")
        for i in range(len(a)):
            msg = serviceml.users().messages().get(userId='me', id=a[i]['id']).execute()
            print('From : ',msg['payload']['headers'][16]['value'])
            if msg['snippet']+'\n':
                print('Messages : ',msg['snippet']+'\n')
            else:
                print('No body Found, maybe there is only attachemnt\n')
            GetAttachments(serviceml, 'me',a[i]['id'] , prefix="")
            ModifyMessage(serviceml,'me',a[i]['id'],{'removeLabelIds': ['UNREAD'], 'addLabelIds': ['INBOX']})

