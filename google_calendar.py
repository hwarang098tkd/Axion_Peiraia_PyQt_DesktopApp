from __future__ import print_function
import httplib2
import os

# from apiclient import discovery
# Commented above import statement and replaced it below because of
# reader Vishnukumar's comment
# Src: https://stackoverflow.com/a/30811628

import googleapiclient.discovery as discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from datetime import datetime

class calendar_data:
    global flags
    try:
        import argparse
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    except ImportError:
        flags = None

    # If modifying these scopes, delete your previously saved credentials
    # at ~/.credentials/calendar-python-quickstart.json
    global SCOPES
    global CLIENT_SECRET_FILE
    global APPLICATION_NAME
    SCOPES = 'https://www.googleapis.com/auth/calendar.events'
    CLIENT_SECRET_FILE = 'credentials/client_secret_231080718247-51irsvd4vmi4ji43gop2c3sjt2uururh.apps.googleusercontent.com.json'
    APPLICATION_NAME = 'AxionPiraeus'


    def main(self):
        """Shows basic usage of the Google Calendar API.

        Creates a Google Calendar API service object and outputs a list of the next
        10 events on the user's calendar.
        """
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)

        # This code is to fetch the calendar ids shared with me
        # Src: https://developers.google.com/google-apps/calendar/v3/reference/calendarList/list
        page_token = None
        calendar_ids = []
        while True:
            calendar_list = service.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                if 'axionpeiraia@gmail.com' in calendar_list_entry['id']:
                    calendar_ids.append(calendar_list_entry['id'])
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break

        # This code is to look for all-day events in each calendar for the month of September
        # Src: https://developers.google.com/google-apps/calendar/v3/reference/events/list
        # You need to get this from command line
        # Bother about it later!
        start_date = datetime(
            2021, 10, 18, 00, 00, 00, 0).isoformat() + 'Z'
        end_date = datetime(2021, 10, 24, 23, 59, 59, 0).isoformat() + 'Z'
        #print(calendar_ids)
        for calendar_id in calendar_ids:
            count = 0
            #print('\n----%s:\n' % calendar_id)
            eventsResult = service.events().list(
                calendarId=calendar_id,
                timeMin=start_date,
                timeMax=end_date,
                singleEvents=True,
                orderBy='startTime').execute()
            events = eventsResult.get('items', [])
            result_list = []
            if not events:
                print('No upcoming events found.')
            for event in events:
                count += 1
                start = event['start'].get('dateTime')
                end = event['end'].get('dateTime')
                start_date = datetime.fromisoformat(start).date().strftime('%d-%m-%Y')
                start_time = datetime.fromisoformat(start).time().strftime('%H:%M')
                end_time = datetime.fromisoformat(end).time().strftime('%H:%M')
                duration = datetime.strptime(end_time, '%H:%M') - datetime.strptime(start_time, '%H:%M')
                list2 = [start_date, start_time, duration, event['summary'], event['colorId']]
                result_list.append(list2)
                #print(start_date, start_time, duration, event['summary'])
            print('Total events for %s is %d' % (calendar_id, count))
        return result_list

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.abspath('')
    credential_dir = os.path.join(home_dir, 'credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'quickstart.py')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials