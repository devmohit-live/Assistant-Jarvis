from __future__ import print_function
from googleapiclient import discovery
from googleapiclient.discovery import build
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
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
from googleapiclient import errors

def create_sesion():
    scopes = ['https://www.googleapis.com/auth/gmail.modify']

    flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes=scopes)

    try:
        credentials = pickle.load(open("caltoken.pkl", "rb"))
    except Exception :
    #     speak('please follow this link to allow jarvis to vreate evnts')
        print('please follow this link to allow jarvis to vreate evnts\n')
    #     speak('Copy and paste the token to autorize the app')
        print('Copy and paste the token to autorize the app\n')
        credentials = flow.run_console()
        pickle.dump(credentials, open("caltoken.pkl", "wb"))

    servicecal = build("calendar", "v3", credentials=credentials)
    service = build("gmail", "v1", credentials=credentials)
    return service,servicecal

# Getit(service, 'me', '16bb36e3b2a1f095', prefix="")