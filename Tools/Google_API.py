
def set_SCOPES():
    # Define the required scopes for YouTube API access
    SCOPES = ['https://www.googleapis.com/auth/youtube.readonly',
            'https://www.googleapis.com/auth/userinfo.email',   #for email
            'https://www.googleapis.com/auth/userinfo.profile', #for email
            'openid'                                            #for email
        ]
    
    return SCOPES

def get_user_info():
    """
    Returns user nickname, email and profile picture path.


    Pray to god you never have to look at this
    or even worse...
    Fix a bug here......
    """


    import os
    import pickle
    import google_auth_oauthlib.flow
    from googleapiclient.discovery import build
    from google.auth.transport.requests import Request
    import requests
    from Tools.get_email import get_user_email


    # def get_user_email(credentials):
        
    #     # Use credentials to call Google's People API
    #     service = build('people', 'v1', credentials=credentials)
    #     profile = service.people().get(resourceName='people/me', personFields='emailAddresses').execute()

    #     # Extract and print the user's email address
    #     email = profile['emailAddresses'][0]['value']
    #    return(email)


    SCOPES = set_SCOPES()

    # Path to your OAuth 2.0 credentials file (JSON file downloaded from Google Cloud Console)
    CLIENT_SECRETS_FILE = 'Tools/Google/client_secret.json'

    # File to store the credentials
    CREDENTIALS_PICKLE_FILE = 'Tools/Google/token.pickle'

    def connect_Google():
        credentials = None

        # Check if the credentials are already saved locally
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
        
        return youtube

    def download_image(url, filename):
        if not os.path.exists('user_info'):
            os.makedirs('user_info')

        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Image downloaded successfully: {filename}")
        else:
            print(f"Failed to download image: {response.status_code}")



    youtube_service = connect_Google()

    # Example API call: Fetch the authenticated user's channel info
    request = youtube_service.channels().list(
        part="snippet,contentDetails,statistics",
        mine=True
    )
    response = request.execute()


    prof_pic_url = response["items"][0]["snippet"]["thumbnails"]["high"]["url"]
    prof_nickname = response["items"][0]["snippet"]["title"]
    prof_email = get_user_email()
    
    # print(prof_email)
    
    # Download the profile picture
    download_image(prof_pic_url, "user_info/profile_pic.jpg")

    out = {
        "profile_pic_path": "user_info/profile_pic.jpg",
        "nickname": prof_nickname,
        "email": prof_email
    }

    return(out)


if __name__ == '__main__':
    print(get_user_info())