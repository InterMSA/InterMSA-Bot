from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/directory.readonly"]

def main():
    """Shows basic usage of the People API.
    Prints the name of the first 10 connections.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('people', 'v1', credentials=creds)

    # Call the People API
    print('List 10 connection names')
##    return service
    results = service.people().listDirectoryPeople(
        mergeSources="DIRECTORY_MERGE_SOURCE_TYPE_CONTACT",
        pageSize=10,
        readMask="names,emailAddresses",
        sources="DIRECTORY_SOURCE_TYPE_DOMAIN_CONTACT").execute()
    contacts = results.get("people", [])

    for person in contacts:
        names = person.get("names", [])
        emails = person.get("emailAddresses", [])
        if names:
            name = names[0].get("displayName")
            print(name)
        if emails:
            email = emails[0].get("value")
            print(email)

if __name__ == "__main__":
    service = main()
