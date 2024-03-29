#! /usr/bin/env python
import sys
import argparse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders
import getopt
from os.path import basename
import socket

import logging
import toolkit_config

HOSTNAME = socket.gethostname()

# Usage: python send_an_email_with_attachment.py subject content (-f FILEPATH -r "RECIPIENT_1@gmail.com,RECIPIENT_2@gmail.com")

config = toolkit_config.read_config_mail('config_test.ini')
config.pop('IMAP_SERVER')


class Smtp():
    """Send email
    If DISTRI_LIST is None, send mail to myself
    DISTRI_LIST example: a@mail.com, b@gmail.com
    """

    def __init__(self, SMTP_SERVER, EMAIL_ACCOUNT, EMAIL_PASSWORD, DISTRI_LIST=None):
        self.SMTP_SERVER = SMTP_SERVER
        self.EMAIL_ACCOUNT = EMAIL_ACCOUNT
        self.EMAIL_PASSWORD = EMAIL_PASSWORD
        if DISTRI_LIST:
            self.DISTRI_LIST = [i.strip() for i in DISTRI_LIST.split(',')]
        else:
            self.DISTRI_LIST = EMAIL_ACCOUNT

        # print(self.SMTP_SERVER, self.EMAIL_ACCOUNT, self.EMAIL_PASSWORD, self.DISTRI_LIST)

    def send_mail(self, subject, content, attach_file=None, image=None):
        msg = MIMEMultipart()
        msg['Subject'] = subject
        # msg['From'] = self.EMAIL_ACCOUNT
        msg['From'] = '{0}  <{1}>'.format(HOSTNAME, self.EMAIL_ACCOUNT)
        if type(self.DISTRI_LIST) is list:
            msg['To'] = ', '.join(self.DISTRI_LIST)
        else:
            msg['To'] = self.DISTRI_LIST

        if attach_file:
            attachFileList = [i.strip() for i in attach_file.split(',')]
            for file in attachFileList:
                try:
                    file_name = basename(file)
                    part = MIMEBase('application', "octet-stream")
                    part.set_payload(open(file, "rb").read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition',
                                    'attachment', filename=file_name)
                    msg.attach(part)
                    logging.info('Attached file {}'.format(file))
                except Exception as e:
                    logging.info("could not attach file")
                    raise

        if image:
            # Add <img src="cid:{}"><br>'.format(image) in body
            imageList = [i.strip() for i in image.split(',')]
            for file in imageList:
                try:
                    file_name = basename(file)
                    with open(file, 'rb') as f:
                        img = MIMEImage(f.read())
                    img.add_header('Content-ID', '<{}>'.format(file))
                    msg.attach(img)
                    logging.info('Attached image {}'.format(file))
                except Exception as e:
                    logging.info("could not attach image")
                    raise

        body = ''.join(content)
        body = body.replace('\n', '<br />')
        msg.attach(MIMEText('<html><body>' + body +
                            '</body></html>', 'html', 'utf-8'))
        try:
            server = smtplib.SMTP(self.SMTP_SERVER)
            server.starttls()
            server.login(self.EMAIL_ACCOUNT, self.EMAIL_PASSWORD)
            logging.info('Send mail to {}'.format(msg['To']))
            logging.info('Subject: {}'.format(msg['Subject']))

            print('Send mail to {}'.format(msg['To']))
            print('Subject: {}'.format(msg['Subject']))
            # print(msg.as_string())
            server.sendmail(self.EMAIL_ACCOUNT,
                            self.DISTRI_LIST, msg.as_string())
        except Exception as e:
            logging.error('Failed to send mail: ' + str(e))
            raise
        else:
            logging.info("Mail sent")
            print("Mail sent")
        finally:
            server.quit()


def send_mail(subject, content, attach_file=None, image=None):
    smtp = Smtp(**config)
    smtp.send_mail(subject, content, attach_file, image)


def script_send_mail():
    '''Put this in the main to run as script.'''
    helpMsg = '''
Send email to the reciever in DISTRI_LIST item of the config file
e.g. {} --subject Hello --content 'How are you.' --attach_file 'file1, file2'
'''.format(__file__)

    helpMsg_subject = 'Subject of the email'
    helpMsg_content = 'Content of the email'
    helpMsg_attach_file = 'Attachment seperated by \',\''

    parser = argparse.ArgumentParser(description=helpMsg)
    parser.add_argument('-s', '--subject', help=helpMsg_subject, required=True)
    parser.add_argument('-c', '--content', help=helpMsg_content, required=True)
    parser.add_argument('-f', '--attach_file',
                        help=helpMsg_attach_file, required=False)

    args = parser.parse_args()
    parameterDict = vars(args)

    send_mail(**parameterDict)


if __name__ == '__main__':
    script_send_mail()
    # send_mail('subject', 'content', r'toolkit_imap.py, toolkit_sqlite.py')
