import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials


class Case:
    ID: int
    CheckOn: str
    Valid: bool
    Value: str
    Passed: None

    def __init__(self, id, checkOn, value, valid):
        self.ID = id
        self.CheckOn = checkOn
        self.Valid = valid
        self.Value = value
        self.Passed = None

    def __str__(self):
        return f"{self.ID} | {self.CheckOn} | {self.Valid} | {self.Value} | {self.Passed}"


def ReadCases(**kwargs):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(kwargs["CREDENTIALS_FILE"],
                                                                   ['https://www.googleapis.com/auth/spreadsheets',
                                                                    'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)
    Cases = list()
    raw = service.spreadsheets().values().get(spreadsheetId=kwargs["SSID"],
                                              range=f"{kwargs['SheetTitle']}!A2:D{kwargs['Count']}",
                                              majorDimension='ROWS').execute()["values"]
    for case in raw:
        Cases.append(Case(case[0], case[1], case[2], str.lower(case[3]) == 'true'))
    return Cases