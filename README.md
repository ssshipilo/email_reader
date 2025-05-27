# EmailReader

The simplest possible solution for reading messages via IMAP, just to avoid writing over and over again. Maybe in the future I will add AI to use the free Gemini to get code or links from a message. I use this code very often in automation projects

This Python class, `EmailReader`, provides functionality to read the latest email from various mail services using the IMAP protocol. It supports extracting the sender's email, subject, body, and optionally a verification code from the email content.

---

## Features

* **Multi-service support**: Pre-configured settings for popular email providers like inbox.lv, rambler.ru, gmail.com, outlook.com, and more.
* **Latest email retrieval**: Fetches the most recent email across all accessible folders for a given account.
* **Content parsing**: Extracts the sender's email, subject, and both plain text and HTML body content.
* **Verification code extraction**: Can identify and extract a numerical verification code of a specified length from the email body.
* **Synchronous and Asynchronous methods**: Offers both `sync_read_messages_in_email` for direct use and `async_read_messages_in_email` for integration into asynchronous applications.

---

## Installation

This project requires the following Python libraries:

* `imaplib` (built-in)
* `email` (built-in)
* `bs4` (BeautifulSoup)
* `re` (built-in)

You can install `BeautifulSoup` using pip:

```bash
pip install beautifulsoup4
```

## Usage
To use the EmailReader class, instantiate it with your email address and password, then call the sync_read_messages_in_email method.

```python
from email_reader import EmailReader

# Replace with your email and password
my_email = "your_email@example.com"
my_password = "your_password"

reader = EmailReader(email=my_email, password=my_password)
result = reader.sync_read_messages_in_email(count_number=6) # Extracts a 6-digit code

if result:
    print(f"From: {result['from_email']}")
    print(f"Subject: {result['subject']}")
    print(f"Body (snippet): {result['body'][:200]}...") # Print first 200 characters of body
    if result['verification_code']:
        print(f"Verification Code: {result['verification_code']}")
else:
    print("Could not read messages or no new messages found.")
```

## Supported Email Services
The EmailReader currently supports the following email services out of the box:

inbox.lv
rambler.ru
gmail.com
firstmail.ru
firstmail.fun
firstmail.site
gazeta.pl
outlook.com
office365.com
hotmail.com
