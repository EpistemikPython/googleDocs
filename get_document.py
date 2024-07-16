##############################################################################################################################
# coding=utf-8
#
# get_document.py -- retrieve and display a document from my Google Docs
#
# includes some code from Google quickstart examples
#
# Copyright (c) 2024 Mark Sattolo <epistemik@gmail.com>

__author__         = "Mark Sattolo"
__author_email__   = "epistemik@gmail.com"
__python_version__ = "3.11"
__google_api_python_client_version__ = "2.137.0"
__google_auth_oauthlib_version__     = "1.2.1"
__created__ = "2019-02-13"
__updated__ = "2024-07-16"

from sys import path, argv
import os
import time
import shutil
from argparse import ArgumentParser
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
path.append("/home/marksa/git/Python/utils")
from mhsUtils import *
from mhsLogging import MhsLogger

start = time.perf_counter()

# see https://github.com/googleapis/google-api-python-client/issues/299
lg.getLogger("googleapiclient.discovery_cache").setLevel(lg.ERROR)

base_run_file = get_base_filename(__file__)
CURRENT_READING_GDOC_ID = "1VlYk7qu7DFarxYOwK78TeoxAbwA3gCjza751xlDBxzU"
READING_TEST_GDOC_ID    = "1TeFPDuI1ergAi4RAifoht6XkM-QA-kxdL98eYKEOM6k"
READING_GDOC_ID         = "1VVT2nEN04ZaPbm6LQUpAu7Dqnur6y3drkP9DWxO9OHE"

SECRETS_DIR = osp.join(BASE_PYTHON_FOLDER, "google" + osp.sep + "docs" + osp.sep + "secrets")
CREDENTIALS_FILE:str = osp.join(SECRETS_DIR, "credentials" + osp.extsep + "json")
DOCS_ACCESS_SCOPE:list  = ["https://www.googleapis.com/auth/documents"]
# The TOKEN file stores the user's access & refresh tokens and is
# created automatically when the authorization flow completes for the first time
JSON_TOKEN:str = "token.json"
DOCS_TOKEN_PATH:str = osp.join(SECRETS_DIR, JSON_TOKEN)

def get_credentials():
    """Get the proper credentials needed to access my Google drive."""
    access_token = None
    if osp.exists( DOCS_TOKEN_PATH ):
        access_token = Credentials.from_authorized_user_file( DOCS_TOKEN_PATH, DOCS_ACCESS_SCOPE )
    # if authorization fails, have the user log in and obtain a fresh token file
    if not access_token or not access_token.valid:
        if access_token and access_token.expired and access_token.refresh_token:
            show("Need to refresh token.")
            access_token.refresh( Request() )
        else:
            show("Need to regenerate token.")
            flow = InstalledAppFlow.from_client_secrets_file( CREDENTIALS_FILE, DOCS_ACCESS_SCOPE )
            access_token = flow.run_local_server(port=0)
        # save the credentials for the next run
        with open(JSON_TOKEN, 'w') as token:
            token.write( access_token.to_json() )
        shutil.move(JSON_TOKEN, SECRETS_DIR)

    return access_token

def main_doc():
    """
    Test basic usage of the Google Docs API.
    Get the title and body of a sample document.
    """
    show("starting main_doc()")
    try:
        creds = get_credentials()
        service = build("docs", "v1", credentials = creds)
        show(f"service = {repr(service)} >> get document")
        # Retrieve the documents contents from the Docs service.
        document = service.documents().get(documentId = doc_id).execute()
    except Exception as mde:
        show(f"problem = '{repr(mde)}'")
        raise mde

    show(f"\nacquire document elapsed time = {time.perf_counter() - start}")

    doc_title = str( document.get('title') )
    show(f"The title of the document is: {doc_title}")
    doc_body = document.get('body')
    show(f"The body of the document is:\n{repr(doc_body)}")
    show(f"\nacquire & display document elapsed time = {time.perf_counter() - start}")

    if save_option:
        save_name = save_to_json(fname = doc_title.replace(osp.extsep, '_'), json_data = doc_body, indt = 2)
        show(f"Saved output to file '{save_name}'.")

def set_args():
    arg_parser = ArgumentParser(description="get a document from my Google Docs", prog=f"python3 {get_filename(__file__)}")
    # optional arguments
    arg_parser.add_argument('-s', '--save', action="store_true", default=False, help="Write the results to a JSON file")
    arg_parser.add_argument('-i', '--id', type=str, default=READING_TEST_GDOC_ID, help="Google ID of an accessible document")
    return arg_parser

def prepare_args(argl:list):
    args = set_args().parse_args(argl)
    show(f"save option = '{args.save}'")
    return args.save, args.id


if __name__ == "__main__":
    log_control = MhsLogger( get_base_filename(__file__) )
    show = log_control.show
    code = 0
    try:
        save_option, doc_id = prepare_args(argv[1:])
        show(f"doc ID = '{doc_id}'")
        main_doc()
    except KeyboardInterrupt:
        show(">> User interruption.")
        code = 13
    except Exception as mex:
        show(f"Problem: {repr(mex)}.")
        code = 66

    show(f"\nfinal elapsed time = {time.perf_counter() - start}")
    exit(code)
