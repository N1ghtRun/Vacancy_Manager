import smtplib, ssl, imaplib, poplib
from email.header import decode_header
import re
import email


class EmailWrapper:
    def __init__(self, user_email, login, password, smtp_server, smtp_port, pop_server=0, imap_server=0, pop_port=0,
                 imap_port=0):
        self.user_email = user_email
        self.login = login
        self.password = password
        self.smtp_server = smtp_server
        self.pop_server = pop_server
        self.imap_server = imap_server
        self.smtp_port = smtp_port
        self.pop_port = pop_port
        self.imap_port = imap_port

    def send_email(self, recipient, subject, text):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
            message = 'Subject: {}\n\n{}'.format(subject, text)
            server.login(self.login, self.password)
            server.sendmail(self.user_email, recipient, message)

    def imap_connect(self):
        # connect to the server
        imap_conn = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)

        # Log in to the server
        imap_conn.login(self.user_email, self.password)

        # select the mailbox to search
        return imap_conn.select("inbox")

    def imap_receive(self):
        imap_conn = self.imap_connect()


    def imap_receiver(self):

        # connect to the server
        imap_conn = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)

        # Log in to the server
        imap_conn.login(self.user_email, self.password)

        # select the mailbox to search
        imap_conn.select("inbox")

        # search for messages
        result, data = imap_conn.search(None, "ALL")

        # Getting the 5 most recent messages. data[0] containes ID's of emailes
        message_ids = data[0].split()[-5:]

        # Create a list to store the messages
        messages = []

        # Retrieve the messages and add their dates, subjects, senders, and content to the list of messages
        for message_id in message_ids:
            # fetch the message data using the message id
            result, data = imap_conn.fetch(message_id, "(RFC822)")

            # convert the message data to an email message object
            message = email.message_from_bytes(data[0][1])
            date = message.get('Date')
            subject = message.get('Subject')
            sender = message.get('From')

            # Decode the subject and sender if necessary
            if subject:
                subject = decode_header(subject)[0][0]
                if isinstance(subject, bytes):
                    subject = subject.decode()
            if sender:
                sender = decode_header(sender)[0][0]
                if isinstance(sender, bytes):
                    sender = sender.decode()

            # Add the date, subject, and sender to the dictionary for this message
            message_dict = {'date': date, 'subject': subject, 'sender': sender}

            if message.is_multipart():
                for part in message.walk():
                    content_type = part.get_content_type()
                    if content_type == 'text/plain':
                        content = part.get_payload(decode=True)
                        charset = part.get_content_charset()
                        if charset:
                            content = content.decode(charset)
                        message_dict['content'] = content
                        try:
                            content = re.sub(r'http\S+', '', content)  # Remove URLs
                        except:
                            pass
                        message_dict['content'] = content.strip()  # Strip whitespace from the beginning and end
                        break
                    elif content_type.startswith('image/') or content_type.startswith(
                            'video/') or content_type.startswith('audio/'):
                        # Skip any non-text content
                        continue
            else:
                content = message.get_payload(decode=True)
                charset = message.get_content_charset()
                if charset:
                    content = content.decode(charset)
                message_dict['content'] = content

            # Add the dictionary for this message to the list of messages
            messages.append(message_dict)

        # Close the connection to the server
        imap_conn.close()

        return messages[::-1]

    def pop3_receiver(self):
        # Connect to the POP3 server using SSL
        pop_conn = poplib.POP3_SSL(self.pop_server, self.pop_port)

        # Log in to the server
        pop_conn.user(f'recent:{self.user_email}')
        pop_conn.pass_(self.password)

        # Get the number of messages in the inbox
        num_messages = len(pop_conn.list()[1])

        # Retrieving 5 most recent messages
        start = num_messages - 4
        end = num_messages
        message_ids = range(start, end + 1)

        # Creating a list to store the messages
        messages = []

        # Retrieve the messages and add their dates, subjects, senders, and content to the list of messages
        for message_id in message_ids:
            raw_message = b'\n'.join(pop_conn.retr(message_id)[1])
            message = email.message_from_bytes(raw_message)
            date = message.get('Date')
            subject = message.get('Subject')
            sender = message.get('From')

            # Decode the subject and sender if necessary
            if subject:
                subject = decode_header(subject)[0][0]
                if isinstance(subject, bytes):
                    subject = subject.decode()
            if sender:
                sender = decode_header(sender)[0][0]
                if isinstance(sender, bytes):
                    sender = sender.decode()

            # Add the date, subject, and sender to the dictionary for this message
            message_dict = {'date': date, 'subject': subject, 'sender': sender}

            if message.is_multipart():
                for part in message.walk():
                    content_type = part.get_content_type()
                    if content_type == 'text/plain':
                        content = part.get_payload(decode=True)
                        charset = part.get_content_charset()
                        if charset:
                            content = content.decode(charset)
                        # content = re.sub(r'http\S+', '', content)  # Remove URLs
                        message_dict['content'] = content.strip()  # Strip whitespace from the beginning and end
                        break
                    elif content_type.startswith('image/') or content_type.startswith(
                            'video/') or content_type.startswith('audio/'):
                        # Skip any non-text content
                        continue
            else:
                content = message.get_payload(decode=True)
                charset = message.get_content_charset()
                if charset:
                    content = content.decode(charset)
                message_dict['content'] = content

            # Add the dictionary for this message to the list of messages
            messages.append(message_dict)

        # Close the connection to the server
        pop_conn.quit()

        return messages[::-1]
