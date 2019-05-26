import os
import smtplib
from email.mime.text import MIMEText


class Mailer(object):

    def __init__(self):

        self.host = 'smtp.gmail.com'
        self.port = 465
        self.sender = 'phillycheesesteak432@gmail.com'
        self.password = os.envi

        self.receiver = 'caoda0711@gmail.com'


    def create_message(self):
        message = MIMEText('content', 'plain', 'utf-8')
        message['Subject'] = 'test'
        message['From'] = self.sender
        message['To'] = self.receiver
        return message

    def send(self):
        try:
            server_ssl = smtplib.SMTP_SSL(self.host, self.port)
            # server_ssl.ehlo()
            # server_ssl.starttls()
            server_ssl.ehlo()
            server_ssl.login(self.sender, 'pass-word')

            message = self.create_message()
            server_ssl.sendmail(self.sender, self.receiver, message.as_string())
            server_ssl.close()
            print('success')
        except Exception as e:
            print('Failed !!! ')
            print(e)





if __name__ == '__main__':

    mailer = Mailer()
    mailer.send()
