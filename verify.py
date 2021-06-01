from __future__ import print_function
import os.path, pickle, time
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
##    return service
    request = service.people().listDirectoryPeople(
        mergeSources="DIRECTORY_MERGE_SOURCE_TYPE_CONTACT",
        pageSize=1000,
        readMask="names,emailAddresses",
        sources="DIRECTORY_SOURCE_TYPE_DOMAIN_CONTACT")
    c = 0
    while request != None:
        if c != 0:
            request = service.people().listDirectoryPeople(
                mergeSources="DIRECTORY_MERGE_SOURCE_TYPE_CONTACT",
                pageSize=1000,
                pageToken=req.get("nextPageToken"),
                readMask="names,emailAddresses",
                sources="DIRECTORY_SOURCE_TYPE_DOMAIN_CONTACT")
        req = request.execute()
        contacts = req.get("people", [])
        with open("loot2.txt", 'a') as f:
            for person in contacts:
                names = person.get("names", [])
                emails = person.get("emailAddresses", [])
                if names and emails:
                    name = names[0].get("displayName")
                    email = emails[0].get("value")
                    f.write(f"{name}\t{email}\n")
            print(name, email)
            print(req.get("nextPageToken"))
            c += 1
        time.sleep(60)
    print("Escaped with", c, "records!")

if __name__ == "__main__":
    t0 = time.process_time()
    service = main()
    t1 = time.process_time()
    total = t1 - t0
    print(f"\nTimestamp 1: {t0} secs\nTimestamp 2: {t1} secs")
    print("Module Time Elapsed:", total, "seconds")
