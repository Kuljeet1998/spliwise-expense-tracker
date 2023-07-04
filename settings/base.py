import sys
import os
import json

SPLITWISE_SECRETS_FILE = str('config/splitwise_secrets.json')
if os.path.exists(SPLITWISE_SECRETS_FILE) is False:
    sys.exit(" Please add 'splitwise_secrets.json' file in config/ folder.")

with open(SPLITWISE_SECRETS_FILE) as f:
    splitwise_secrets = json.loads(f.read())


def get_splitwise_secret(setting, secrets=splitwise_secrets):
    '''get the secret variable value of return exception'''
    try:
        return splitwise_secrets[setting]
    except KeyError:
        error_message = 'Set the {0} environment variable'.format(setting)
        sys.exit(error_message)


SHEET_SECRETS_FILE = str('config/spreadsheet_secrets.json')
if os.path.exists(SHEET_SECRETS_FILE) is False:
    sys.exit(" Please add 'spreadheet_secrets.json' file in config/ folder.")

with open(SHEET_SECRETS_FILE) as f:
    spreadheet_secrets = json.loads(f.read())


def get_spreadsheet_secret(setting, secrets=spreadheet_secrets):
    '''get the secret variable value of return exception'''
    try:
        return spreadheet_secrets[setting]
    except KeyError:
        error_message = 'Set the {0} environment variable'.format(setting)
        sys.exit(error_message)