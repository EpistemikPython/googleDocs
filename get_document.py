##############################################################################################################################
# coding=utf-8
#
# get_document.py -- get a document from my Google Docs
#
# includes some code from Google quickstart examples
#
# Copyright (c) 2019-21 Mark Sattolo <epistemik@gmail.com>

__author__         = "Mark Sattolo"
__author_email__   = "epistemik@gmail.com"
__google_api_python_client_py3_version__ = "1.2"
__created__ = "2019-02-13"
__updated__ = "2021-05-15"

import sys
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
sys.path.append("/newdata/dev/git/Python/utils")
from mhsUtils import osp

CURRENT_READING_GDOC = "1VlYk7qu7DFarxYOwK78TeoxAbwA3gCjza751xlDBxzU"

SECRETS_DIR = "/newdata/dev/git/Python/Google/Docs/secrets"
CREDENTIALS_FILE:str = osp.join(SECRETS_DIR, "credentials" + osp.extsep + "json")
DOCS_ACCESS_SCOPE:list  = ["https://www.googleapis.com/auth/documents"]
DOCS_JSON_TOKEN:str     = "token.json"
DOCS_TOKEN_LOCATION:str = osp.join(SECRETS_DIR, DOCS_JSON_TOKEN)


def get_credentials():
    """Get the proper credentials needed to access my Google drive."""
    creds = None
    # The TOKEN file stores the user's access and refresh tokens & is
    # created automatically when the authorization flow completes for the first time
    if osp.exists(DOCS_TOKEN_LOCATION):
        creds = Credentials.from_authorized_user_file(DOCS_TOKEN_LOCATION, DOCS_ACCESS_SCOPE)
    # if there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, DOCS_ACCESS_SCOPE)
            creds = flow.run_local_server(port=0)
        # save the credentials for the next run
        with open("token.json", 'w') as token:
            token.write( creds.to_json() )

    return creds


def main_doc():
    """
    Shows basic usage of the Docs API.
    Prints the title of a sample document.
    """
    try:
        creds = get_credentials()

        service = build("docs", "v1", credentials = creds)

        # Retrieve the documents contents from the Docs service.
        document = service.documents().get(documentId = CURRENT_READING_GDOC).execute()
    except Exception as me:
        print( repr(me) )
        return

    print(F"The title of the document is: {document.get('title')}")
    print(F"The body of the document is: {document.get('body')}")


if __name__ == "__main__":
    main_doc()
    exit()
