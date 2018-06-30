#! /usr/bin/env python 
import sys 

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import getopt
from os.path import basename
import toolkit_config


#Usage: python send_an_email_with_attachment.py subject content (-f FILEPATH -r "RECIPIENT_1@gmail.com,RECIPIENT_2@gmail.com")

config = toolkit_config.read_config_mail('config.ini')


class Smtp():
	"""Send mail if DISTRI_LIST is None, send mail to myself
		DISTRI_LIST example: a@mail.com, b@gmail.com
	"""
	def __init__(self, SMTP_SERVER, EMAIL_ACCOUNT, EMAIL_PASSWORD, DISTRI_LIST = None):
		self.SMTP_SERVER = SMTP_SERVER
		self.EMAIL_ACCOUNT = EMAIL_ACCOUNT
		self.EMAIL_PASSWORD = EMAIL_PASSWORD
		if DISTRI_LIST:
			self.DISTRI_LIST = [ i.strip() for i in DISTRI_LIST.split(',') ]
		else:
			self.DISTRI_LIST = EMAIL_ACCOUNT

		# print(self.SMTP_SERVER, self.EMAIL_ACCOUNT, self.EMAIL_PASSWORD, self.DISTRI_LIST)

	def send_mail(self, subject, content, attach_file = None):
		msg = MIMEMultipart()
		msg['Subject'] = subject
		msg['From'] = self.EMAIL_ACCOUNT
		msg['To'] = ', '.join(self.DISTRI_LIST)

		if attach_file:
			attachFileList = [ i.strip() for i in attach_file.split(',') ]
			for file in attachFileList:
				try:
					file_name=basename(file)
					part = MIMEBase('application', "octet-stream")
					part.set_payload(open(file, "rb").read())
					encoders.encode_base64(part)
					part.add_header('Content-Disposition', 'attachment' ,filename=file_name)
					msg.attach(part)
					print('Attached file {}'.format(file))
				except Exception as e:
					print("could not attach file")

		body = ''.join(content)
		body = body.replace('\n', '<br />')
		msg.attach(MIMEText('<html><body>'+ body +'</body></html>','html','utf-8'))

		try: 
			server = smtplib.SMTP(self.SMTP_SERVER)
			server.starttls()
			server.login(self.EMAIL_ACCOUNT, self.EMAIL_PASSWORD)
			print('Send mail to {}'.format(msg['To']))
			print('Subject: {}'.format(msg['Subject']))
			# print(msg.as_string())
			server.sendmail(self.EMAIL_ACCOUNT, self.DISTRI_LIST, msg.as_string())
			print("Mail sent")
		except Exception as e:
			print('Failed to send mail: '+ str(e))
		finally:
			server.quit()


if __name__ == '__main__':
	'''Usage: python send_an_email_with_attachment.py subject content (-f FILEPATH -r "RECIPIENT_1@gmail.com,RECIPIENT_2@gmail.com")'''

	config.pop('IMAP_SERVER')
	test = Smtp(**config)
	test.send_mail('Requested action not taken', 'cilbox unavailabllass sdf', r'E:\python_test\QRCodeViewer.py, E:\python_test\auto_shutdown.bat')