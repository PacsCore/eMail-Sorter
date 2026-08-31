mails = [
    {"sender": "newsletter@zalando.com", "subject": "Your discount for you!"},
    {"sender": "billing@gmail.com", "subject": "Your invoice for August!"},
    {"sender": "grandma@gmail.com", "subject": "How are you doing?"},
    {"sender": "no-reply@amazon.com", "subject": "Your order has arrived!"},

]

def categorize(mail):
    sender = mail["sender"].lower()
    subject = mail["subject"].lower()

    if "invoice" in subject or "billing" in sender:
        return "Invoice"
    elif "newsletter" in sender or "no-reply" in sender:
        return "Advertising"
    else:
        return "Personal"

counts = {}

for mail in mails:
    category = categorize(mail)
    print(f"{mail['subject']} -> {category}")
    counts[category] = counts.get(category, 0) + 1

print("\nSummary:")
for category, total in counts.items():
    print(f"{category}: {total}")

