import os
from sys import path

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

path.append(f'{__location__}/.transmogrify')
from credentials import get_sheet_id # personal package for credentials


sheet_id = get_sheet_id()

def get_service():
    credentials = Credentials.from_authorized_user_file(
        f'{__location__}/.transmogrify/token.json',
        ['https://www.googleapis.com/auth/spreadsheets']
    )
    return build('sheets', 'v4', credentials=credentials)

def get_sheet(service):
    return service.spreadsheets().values().get(
        spreadsheetId=sheet_id,
        range="A:Z"
    ).execute().get('values',[])

def set_sheet(service,page,table):
    service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        valueInputOption='RAW',
        range=f"{page}!{"A:Z"}",
        body={'majorDimension':'ROWS', 'values':table}
    ).execute()

class sheet_handler:
    def __init__(self):
        self.service = get_service()
    
    def write(self, page, table):
        set_sheet(self.service, page, table)
    
    def read(self):
        return get_sheet(self.service)

if __name__ == "__main__":
    service = get_service()
    print(get_sheet(service))
    set_sheet(service,[['a','b','c'],['it\'s easy as'],['1','2','3']])