import os
import sys
import argparse
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

SCOPES=['https://www.googleapis.com/auth/drive.file']
print('uploading')

def authenticate(): # it will return valid credentials for Drive api
    print('inside fnc')
    creds=None
    if os.path.exists('token.json'):# if file token.json already exists
        creds=Credentials.from_authorized_user_file('token.json',SCOPES)# return saved credentials of logged in user 
        if not creds or not creds.valid:#if no credentials it means there is no user or token is expired
            if creds and creds.expired and creds.refresh_token:# if token is expired but has refresh token then sliently refresh token without logging in again.
                creds.refresh(Request())

    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)# if there is no refresh token then start the Oauth flow and open browser to sign in and get permissions.
        creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:# save the new access and refresh token to json file
            token.write(creds.to_json())
    return creds# credentials returned to call google apis.


def upload_file(file_path):# this function uploads the file
    creds = authenticate() # This is called authenticate function to get back valid credentials to login to google api
    service = build('drive', 'v3', credentials=creds)#This line builds a service object to interact with Google Drive API version 3 using the authenticated credentials.

    file_name = os.path.basename(file_path)#This gets only the file name from the full path.to name the file in google drive
    media = MediaFileUpload(file_path, resumable=True)# it wraps file into special object to sent to google drive.
    file_metadata = {'name': file_name} # This contains name of file

    uploaded_file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()#This uploads file on google drive

    print(f"✅ Uploaded '{file_name}' to Google Drive. File ID: {uploaded_file.get('id')}")# it confirms uploaded succesfull.

paths=['files/pinterestdownloader.com-1749119714.603491.jpg','files/style.css','files/index.html']
for path in paths:
    if os.path.isfile(path):
        upload_file(path)
    else:
        print(f"❌ File not found: {path}")