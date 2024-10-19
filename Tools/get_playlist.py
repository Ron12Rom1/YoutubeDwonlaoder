import os, pickle
import google_auth_oauthlib
from google.auth.transport.requests import Request
from Tools.Google_API import set_SCOPES
from googleapiclient.discovery import build


def get_user_playlists():
    credentials = None

    SCOPES = set_SCOPES()
    CLIENT_SECRETS_FILE = 'Tools/Google/client_secret.json'
    CREDENTIALS_PICKLE_FILE = 'Tools/Google/token.pickle'

    if os.path.exists(CREDENTIALS_PICKLE_FILE):
        with open(CREDENTIALS_PICKLE_FILE, 'rb') as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES)
            credentials = flow.run_local_server(port=0)

            with open(CREDENTIALS_PICKLE_FILE, 'wb') as token:
                pickle.dump(credentials, token)

    youtube = build('youtube', 'v3', credentials=credentials)

    # Get the user's playlists
    request = youtube.playlists().list(
        part="snippet",
        mine=True,  # To get the playlists of the authenticated user
        maxResults=50
    )
    response = request.execute()

    playlists = []
    for playlist in response['items']:
        playlists.append({
            'title': playlist['snippet']['title'],
            'id': playlist['id']
        })

    return playlists




def get_playlist_urls(playlist_id):
    from pytubefix import YouTube
    credentials = None
    
    SCOPES = set_SCOPES()

    CLIENT_SECRETS_FILE = 'Tools/Google/client_secret.json'

    # File to store the credentials
    CREDENTIALS_PICKLE_FILE = 'Tools/Google/token.pickle'

    if os.path.exists(CREDENTIALS_PICKLE_FILE):
        with open(CREDENTIALS_PICKLE_FILE, 'rb') as token:
            credentials = pickle.load(token)

    # If no valid credentials are available, ask the user to log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            # Refresh the credentials if they are expired
            credentials.refresh(Request())
        else:
            # Perform OAuth 2.0 flow for new login
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES)
            credentials = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open(CREDENTIALS_PICKLE_FILE, 'wb') as token:
                pickle.dump(credentials, token)

    # Build the YouTube API client using the credentials
    youtube = build('youtube', 'v3', credentials=credentials)

    # Get the playlist's videos
    request = youtube.playlistItems().list(
        part="contentDetails",
        playlistId=playlist_id,
        maxResults=50
    )
    response = request.execute()

    videos = []
    for video in response['items']:
        url = f"https://www.youtube.com/watch?v={video['contentDetails']['videoId']}"
        title =  YouTube(url).title
        videos.append({
            'title':  title,
            'url': url
        })

    return(videos)
    # return(playlist_id)

if __name__ == '__main__':
    get_playlist_urls("RDuDXMDiL7R8w")
    # get_user_playlists()