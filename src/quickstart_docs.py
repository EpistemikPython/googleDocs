
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
RO_SCOPE = ['https://www.googleapis.com/auth/documents.readonly']
RW_SCOPE = ['https://www.googleapis.com/auth/documents']

# The ID of a sample document.
DOCUMENT_ID = '195j9eDD3ccgjQRttHhJPymLJUCOUjs-jmwTrekvdjFE'

CURRENT_READING = '1VlYk7qu7DFarxYOwK78TeoxAbwA3gCjza751xlDBxzU'

DOCS_TOKEN = "secrets/token.docs.epistemik.rw.pickle4"


def main():
    """
    Shows basic usage of the Docs API.
    Prints the title of a sample document.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists(DOCS_TOKEN):
        with open(DOCS_TOKEN, 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', RW_SCOPE)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.docs.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('docs', 'v1', credentials = creds)

    # Retrieve the documents contents from the Docs service.
    document = service.documents().get(documentId = CURRENT_READING).execute()

    print(F"The title of the document is: {document.get('title')}")
    print(F"The body of the document is: {document.get('body')}")


if __name__ == '__main__':
    main()
