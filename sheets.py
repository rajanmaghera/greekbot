import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from constants import *

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


def getSheet():

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials avaidocslable, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)

    # Retrieve the documents contents from the Docs service.
    return service.spreadsheets().values()

def getSheetValues(range):
    document = getSheet().get(spreadsheetId=DOCUMENT_ID, range=range).execute()
    return document.get('values', [])

def getSheetAppend(range, body):
    getSheet().append(spreadsheetId=DOCUMENT_ID, valueInputOption="USER_ENTERED", range=range, body=body).execute()
