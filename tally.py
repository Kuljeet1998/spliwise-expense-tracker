from __future__ import print_function

import sys
import argparse
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import requests
from oauth2client import file as f, client, tools
from httplib2 import Http
from google.oauth2 import service_account
from splitwise import Splitwise
from settings.base import get_splitwise_secret, get_spreadsheet_secret
from utils import convert_date

import os

os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

SPREADSHEET_ID = get_spreadsheet_secret('spreadsheet_id')
CELL_RANGE = 'July'
redirect_uri = 'https://secure.splitwise.com/#/dashboard'
EXPENSE_TYPE = [0,1,2]

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/documents.readonly',
            'https://www.googleapis.com/auth/userinfo.email',
            'https://www.googleapis.com/auth/userinfo.profile',
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/drive.metadata']


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("-d", help="Date till tally",
                        default='')

    args = parser.parse_args()
    return args


def main():
    args = get_args()
    if args.d is not None:
        DATE = args.d
    print("Tallying from {}".format(DATE))
    google_key_file_path = 'config/service_account_secrets.json'
    google_credentials = service_account.Credentials.from_service_account_file(google_key_file_path,scopes=SCOPES)

    if google_credentials.expired and google_credentials.refresh_token:
        google_credentials.refresh(Request())

    splitwise_key_file_path = 'config/splitwise_secrets.json'

    try:
        #Get splitwise secrets
        CONSUMER_KEY = get_splitwise_secret('consumer_key')
        CONSUMER_SECRET = get_splitwise_secret('consumer_secret')
        API_KEY = get_splitwise_secret('api_key')
        USER_ID = get_splitwise_secret('user_id')

        service = build('sheets', 'v4', credentials=google_credentials)

        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID, range=CELL_RANGE).execute()
        rows = result.get('values', [])
        print(f"{len(rows)} rows retrieved")

        sObj = Splitwise(CONSUMER_KEY,CONSUMER_SECRET,api_key=API_KEY)

        notifications = sObj.getNotifications()
        exp_id = notifications[0].source.id
        for notification in notifications:
            if notification.getType() in EXPENSE_TYPE:
                exp_id = notification.source.id
                expense = sObj.getExpense(exp_id)
                
                for user in expense.users:
                    if user.id == USER_ID: #Kuljeet
                        OWED_SHARE = user.owed_share
                        if OWED_SHARE != '0.0':
                            DATE = convert_date(expense.date)
                            PRODUCT = expense.description
                            NOTES = '{}/{}'.format(expense.cost,len(expense.users))
                            print("PRODUCT:",PRODUCT)
                            print(OWED_SHARE)
                            print("NOTES:",NOTES)
                            print("____________")
        
        # current = sObj.getCurrentUser()
        # friends = sObj.getFriends()
        # print(current)


        return result
        
        
    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()