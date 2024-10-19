import os, pickle
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import google_auth_oauthlib
from google.auth.transport.requests import Request
from Tools.Google_API import set_SCOPES


# Path to your OAuth2 credentials file (from Google Cloud Console)
# GOOGLE_CLIENT_SECRETS_FILE = "Tools\Google\client_secret.json"

# Scopes for retrieving user info, including 'openid' to match Google's changes
# SCOPES = [
#     'https://www.googleapis.com/auth/userinfo.email',   #for email
#     'https://www.googleapis.com/auth/userinfo.profile', #for email
#     'openid'                                            #for email
# ]

def get_user_email():
    """
    Returns user email.

    And same as get user info, Just pray to god you will never look at this code...
    """
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

    # Use credentials to call Google's People API
    service = build('people', 'v1', credentials=credentials)
    profile = service.people().get(resourceName='people/me', personFields='emailAddresses').execute()

    # Extract and print the user's email address
    email = profile['emailAddresses'][0]['value']
    
    return email

if __name__ == '__main__':
    get_user_email()
