from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pandas as pd
#from pprint import pprint

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive.file']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1nOO7asea325w93ottsoxxG30voUgfdvrRR_Lq8Xz8EE'
SAMPLE_RANGE_NAME = 'sheet1!A1:D51'

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
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

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        
        df=pd.DataFrame(values[1:],columns=values[0])

        print(df)
        #to find the total mark
        print('do yo need total mark: yes/no?')
        ans = input()
        if ans == "yes":
            total= df["physics"].astype(int) + df["maths"].astype(int) + df["chemistry"].astype(int)
            df["total"]=total
            df['total'].astype(int) #to making in to integer
            
            print(df)
          

            print("The student with maximum mark is ")
            print(df[df.total==df.total.max()]) #using max function to selecting the student with highest mark

            list1 = df['total'].to_list() #the coluumn total is converted to list
            list1.insert(0,'total') #adding the column name 'total' to the first position of list


            


if __name__ == '__main__':
    main()