from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

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

service = get_labels()

results = service.users().messages().list(userId='me', maxResults=10).execute()
messages = results.get('messages', [])

counts = {}

for msg in messages:
    msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
    headers = msg_data["payload"]["headers"]

    sender = get_header(headers, "From")
    subject = get_header(headers, "Subject")

    category = categorize(sender, subject)
    print(f"{subject} -> {category}")

    counts[category] = counts.get(category, 0) + 1

print("\nSummary:")
for category, total in counts.items():
    print(f"{category}: {total}")