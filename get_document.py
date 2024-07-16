##############################################################################################################################
# coding=utf-8
#
# get_document.py -- get a document from my Google Docs
#
# includes some code from Google quickstart examples
#
# Copyright (c) 2024 Mark Sattolo <epistemik@gmail.com>

__author__         = "Mark Sattolo"
__author_email__   = "epistemik@gmail.com"
__python_version__ = "3.6+"
__google_api_python_client_version__     = "2.137.0"
__created__ = "2019-02-13"
__updated__ = "2024-07-15"

from sys import path
import os
import shutil
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
path.append("/home/marksa/git/Python/utils")
from mhsUtils import *
from mhsLogging import MhsLogger, DEFAULT_LOG_LEVEL

# see https://github.com/googleapis/google-api-python-client/issues/299
lg.getLogger("googleapiclient.discovery_cache").setLevel(lg.ERROR)

base_run_file = get_base_filename(__file__)
CURRENT_READING_GDOC_ID = "1VlYk7qu7DFarxYOwK78TeoxAbwA3gCjza751xlDBxzU"
READING_TEST_GDOC_ID    = "1TeFPDuI1ergAi4RAifoht6XkM-QA-kxdL98eYKEOM6k"
READING_GDOC_ID         = "1VVT2nEN04ZaPbm6LQUpAu7Dqnur6y3drkP9DWxO9OHE"

SECRETS_DIR = osp.join(BASE_PYTHON_FOLDER, "google" + osp.sep + "docs" + osp.sep + "secrets")
CREDENTIALS_FILE:str = osp.join(SECRETS_DIR, "credentials" + osp.extsep + "json")
DOCS_ACCESS_SCOPE:list  = ["https://www.googleapis.com/auth/documents"]
JSON_TOKEN:str     = "token.json"
DOCS_TOKEN_PATH:str = osp.join(SECRETS_DIR, JSON_TOKEN)

def get_credentials(lgr:lg.Logger):
    """Get the proper credentials needed to access my Google drive."""
    lgr.debug("get_credentials()")
    creds = None
    # The TOKEN file stores the user's access & refresh tokens and is
    # created automatically when the authorization flow completes for the first time
    if osp.exists( DOCS_TOKEN_PATH ):
        lgr.debug("osp.exists")
        creds = Credentials.from_authorized_user_file( DOCS_TOKEN_PATH, DOCS_ACCESS_SCOPE )
    # if there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        lgr.debug("not creds or not creds.valid")
        if creds and creds.expired and creds.refresh_token:
            lgr.warning("Need to refresh creds.")
            creds.refresh( Request() )
        else:
            lgr.warning("Need to regenerate creds.")
            flow = InstalledAppFlow.from_client_secrets_file( CREDENTIALS_FILE, DOCS_ACCESS_SCOPE )
            creds = flow.run_local_server(port=0)
        # save the credentials for the next run
        with open(JSON_TOKEN, 'w') as token:
            token.write( creds.to_json() )
        if osp.exists(DOCS_TOKEN_PATH):
            os.rename(DOCS_TOKEN_PATH, DOCS_TOKEN_PATH + osp.extsep + get_current_time(FILE_DATETIME_FORMAT))
        shutil.move(JSON_TOKEN, SECRETS_DIR)

    lgr.debug("valid creds")
    return creds

def main_doc():
    """
    Test basic usage of the Google Docs API.
    Prints the title and body of a sample document.
    """
    start_time = dt.now()
    log_control = MhsLogger(base_run_file, con_level = DEFAULT_LOG_LEVEL)
    lgr = log_control.get_logger()
    lgr.info(f"Start time = {start_time.strftime(RUN_DATETIME_FORMAT)}")
    try:
        creds = get_credentials(lgr)
        lgr.debug("build service")
        service = build("docs", "v1", credentials = creds)
        lgr.debug(f"service = {repr(service)} >> get document")
        # Retrieve the documents contents from the Docs service.
        document = service.documents().get(documentId = CURRENT_READING_GDOC_ID).execute()
    except Exception as mde:
        lgr.exception(mde)
        return 66

    lgr.info(f"The title of the document is: {document.get('title')}")
    lgr.info(f"The body of the document is: {document.get('body')}")


if __name__ == "__main__":
    exit( main_doc() )
