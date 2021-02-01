"""PR13. API."""
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


def get_links_from_spreadsheet(id: str, token: str) -> list:
    """Should get a list of strings from the first column of a Google Spreadsheet with the given ID."""
    scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    spreadsheet_id = id
    range_name = 'A1:A1000'
    credentials = None
    if os.path.exists(token):
        with open(token, 'rb') as tokens:
            credentials = pickle.load(tokens)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                token, scopes)
            credentials = flow.run_local_server(port=0)
        with open(token, 'wb') as tokens:
            pickle.dump(credentials, tokens)

    service = build('sheets', 'v4', credentials=credentials)

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                range=range_name).execute()
    values = result.get('values', [])
    list_to_return = []
    for list_values in values:
        for value in list_values:
            list_to_return.append(value)
    return list_to_return


def get_links_from_playlist(link: str, developer_key: str) -> list:
    """Should get a list of links to songs in the Youtube playlist with the given address."""
    api_service_name = "youtube"
    api_version = "v3"
    playlist_short_url = link.split("list=")[1]
    start_of_video_url = "youtube.com/watch?v="
    youtube = build(api_service_name, api_version, developerKey=developer_key)
    request = youtube.playlistItems().list(part="contentDetails", playlistId=playlist_short_url, maxResults=50)
    response = request.execute()
    list_to_return = []
    operating_list = response.get("items")
    for dicts in operating_list:
        full_video_url = start_of_video_url + dicts.get("contentDetails").get("videoId")
        list_to_return.append(full_video_url)
    while response.get("nextPageToken"):
        next_page = response.get("nextPageToken")
        request_with_next_pages = youtube.playlistItems().list(part="contentDetails", playlistId=playlist_short_url, maxResults=50,
                                                               pageToken=next_page)
        response = request_with_next_pages.execute()
        operating_list_next_pages = response.get("items")
        for dicts_next_pages in operating_list_next_pages:
            full_video_url = start_of_video_url + dicts_next_pages.get("contentDetails").get("videoId")
            list_to_return.append(full_video_url)
    return list_to_return


if __name__ == '__main__':
    get_links_from_playlist("https://www.youtube.com/playlist?list=PL5E4F51699E192081", "AIzaSyBs7h4eXZn-pC1sFiTK-SPI2H_UqBBeHD4")
