
# -*- coding: utf-8 -*-
# Time       : 2025/05/27
# Author     : Shypilo Oleksandr | shypilo.com

import email as email_emal
import imaplib
from email.header import decode_header
from email.utils import parsedate_to_datetime
from bs4 import BeautifulSoup
import re

class EmailReader():

    def __init__(self, email, password):
        self.email = email
        self.password_mail = password
    
    def sync_read_messages_in_email(self, code=True, count_number=6):
        TEMPLATE_SETTINGS = [
            {
                "service": "inbox.lv",
                "server": "mail.inbox.lv",
                "port": "993"
            },
            {
                "service": "rambler.ru",
                "server": "imap.rambler.ru",
                "port": "993"
            },
            {
                "service": "gmail.com",
                "server": "imap.gmail.com",
                "port": "993"
            },
            {
                "service": "firstmail.ru",
                "server": "mail.firstmail.ru",
                "port": "993"
            },
            {
                "service": "firstmail.fun",
                "server": "mail.firstmail.fun",
                "port": "993"
            },
            {
                "service": "firstmail.site",
                "server": "mail.firstmail.site",
                "port": "993"
            },
            {
                "service": "gazeta.pl",
                "server": "imap.gazeta.pl",
                "port": "993"
            },
            {
                "service": "outlook.com",
                "server": "imap-mail.outlook.com",
                "port": "993"
            },
            {
                "service": "office365.com",
                "server": "outlook.office365.com",
                "port": "993"
            },
            {
                "service": "hotmail.com",
                "server": "outlook.office365.com",
                "port": "993"
            },
            {
                "service": "rambler.ru",
                "server": "imap.rambler.ru",
                "port": "993"
            }
        ]

        parse_strintg = str(self.email).split('@')
        parse_strintg = parse_strintg[1]

        valid       = False
        imap_server = None
        imap_port   = None
        for mail_service in TEMPLATE_SETTINGS:
            if mail_service['service'] == parse_strintg:
                valid = True
                imap_server = mail_service['server']
                imap_port = mail_service['port']
                break

        if not valid:
            return False, False

        if int(imap_port) == 993:
            server = imaplib.IMAP4_SSL(imap_server, port=int(imap_port))
        else:
            server = imaplib.IMAP4(imap_server, port=int(imap_port))

        server.login(self.email, self.password_mail)
        typ, folders = server.list()
        if typ != 'OK':
            server.logout()
            return None

        latest_message = None
        latest_date = None

        for folder in folders:
            folder_name = folder.decode().split(' "/" ')[1].strip('"')

            typ, data = server.select(f'"{folder_name}"')
            if typ != 'OK':
                continue

            typ, data = server.search(None, 'ALL')
            if typ != 'OK' or not data[0]:
                continue

            for num in data[0].split():
                typ, data = server.fetch(num, '(RFC822)')
                if typ != 'OK':
                    continue

                raw_email = data[0][1].decode('utf-8')
                message = email_emal.message_from_string(raw_email)
                date_str = message.get('Date')
                try:
                    mail_date = parsedate_to_datetime(date_str)
                except Exception as e:
                    continue
                
                if mail_date.tzinfo is not None and latest_date and latest_date.tzinfo is None:
                    latest_date = latest_date.replace(tzinfo=mail_date.tzinfo)
                elif mail_date.tzinfo is None and latest_date and latest_date.tzinfo is not None:
                    mail_date = mail_date.replace(tzinfo=latest_date.tzinfo)
                
                if not latest_date or mail_date > latest_date:
                    latest_date = mail_date
                    latest_message = message

        server.logout()
        if latest_message:
            from_email = latest_message['from']
            subject = decode_header(latest_message["subject"])[0][0]
            if isinstance(subject, bytes):
                subject = subject.decode()
            
            body = ""
            if latest_message.is_multipart():
                html_part = None
                plain_part = None

                for part in latest_message.walk():
                    content_type = part.get_content_type()
                    if content_type == "text/html":
                        html_part = part
                    elif content_type == "text/plain":
                        plain_part = part

                if html_part:
                    body = html_part.get_payload(decode=True).decode('utf-8', errors='replace')
                elif plain_part:
                    body = plain_part.get_payload(decode=True).decode('utf-8', errors='replace')
            else:
                body = latest_message.get_payload(decode=True).decode('utf-8', errors='replace')

            verification_code = None
            soup = BeautifulSoup(body, 'html.parser')
            verification_code = None
            pattern = r'\b\d{{{}}}\b'.format(count_number)
            match = re.search(pattern, soup.get_text())
            if match:
                code = match.group()
                verification_code = code

            return {
                "from_email": from_email, 
                "subject": subject,
                "body": body,
                "verification_code": verification_code
            }
        
        return None
    
    async def async_read_messages_in_email(self, code=True, count_number=6):
        return self.sync_read_messages_in_email(code=code, count_number=count_number)
    
if __name__ == "__main__":
    result = EmailReader(
        email="jnelson_nhzleyfm8lxxx2j@inbox.lv",
        password="Qg6awYCJ5?"
    ).sync_read_messages_in_email()
    
    print(result)
