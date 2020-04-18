from email.message import EmailMessage
from smtplib import SMTP
from os import environ


class EmailService:
    def __init__(self):
        self.from_address = environ['SMTP_FROM']
        self.host = environ['SMTP_HOST']
        self.port = 587
        self.password = environ['SMTP_PASSWORD']
        self.server = None

    def __del__(self):
        if self.server:
            self.server.quit()

    def send(self, to_address, message_content, subject=''):
        if not self.server:
            self._start_server()

        message = EmailMessage()
        message['From'] = self.from_address
        message['To'] = to_address
        message['Subject'] = subject
        message.set_content(message_content)

        self.server.send_message(message)

    def _start_server(self):
        self.server = SMTP(host=self.host, port=self.port)
        self.server.ehlo()
        self.server.starttls()
        self.server.ehlo()
        self.server.login(self.from_address, self.password)
