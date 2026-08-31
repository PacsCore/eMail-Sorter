import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def get_service():
    creds = None
    
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
            print("Token saved to token.json")
    return build('gmail', 'v1', credentials=creds)

def get_labels():
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    return build('gmail', 'v1', credentials=creds)

def categorize(sender, subject):
    sender = sender.lower()
    subject = subject.lower()

    if "invoice" in subject or "billing" in sender:
        return "Invoice"
    elif "secruity" in subject or "sicherheitswarnung" in subject or "authentifizierung" in subject:
        return "Security Alert"
    elif "noreply" in sender or "no-reply" in sender or "notifications" in sender:
        return "Notification"
    elif "newsletter" in sender or "update" in subject.lower():
        return "Newsletter/Update"
    else:
        return "Uncategorized"
    
def get_header(headers, name):
    for header in headers:
        if header["name"] == name:
            return header["value"]
    return ""

def get_or_create_label(service, label_name, existing_labels):
    for label in existing_labels:
        if label["name"] == label_name:
            return label["id"]

    new_label = service.users().labels().create(userId="me", body={'name': label_name, "labelListVisibility": "labelShow", "messageListVisibility": "show"}).execute()
    existing_labels.append(new_label)
    return new_label["id"]


service = get_service()

#fetch existing labels
label_results = service.users().labels().list(userId='me').execute()
existing_labels = label_results.get('labels', [])

results = service.users().messages().list(userId='me', maxResults=100).execute()
messages = results.get('messages', [])

counts = {}

for msg in messages:
    msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
    headers = msg_data["payload"]["headers"]

    sender = get_header(headers, "From")
    subject = get_header(headers, "Subject")
    category = categorize(sender, subject)

    label_id = get_or_create_label(service, category, existing_labels)

    service.users().messages().modify(userId="me", id=msg['id'], body={'addLabelIds': [label_id]}).execute()

    counts[category] = counts.get(category, 0) + 1

print("\nSummary:")
for category, total in counts.items():
    print(f"{category}: {total}")