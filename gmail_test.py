from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
cred = flow.run_local_server(port=0)

service = build('gmail', 'v1', credentials=cred)
results = service.users().labels().list(userId='me').execute()
labels = results.get('labels', [])

print("Connected! Found these labels:")
for label in labels:
    print(f"- {label['name']}")