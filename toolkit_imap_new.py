import imaplib
import getpass
import email
import datetime
import re

class Imap():
	"""docstring for Imap"""
	def __init__(self, EMAIL_SERVER, EMAIL_ACCOUNT, EMAIL_PASSWORD):
		self.con = imaplib.IMAP4_SSL(EMAIL_SERVER, port = 993)

		try:
			rv, data = self.con.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
		except imaplib.IMAP4.error:
			print ("LOGIN FAILED!!! ")
			raise
		else:
			print(rv, data)

	def __enter__(self):
		return self

	def __exit__(self,Type, value, traceback):  
		'''
		Executed after "with"
		'''
		print('Close the imap connection')
		self.con.close()

	def get_mail_folder(self):
		rv, mailboxes = self.con.list()
		if rv == 'OK':
			print("mailboxes:")
			# print(mailboxes)

			# get inbox alias
			print(mailboxes)
			g = lambda i: re.compile(r'(?<=" ")(.*)(?=")', re.IGNORECASE).findall(i.decode('utf-8'))[0]
			return list(map(g, mailboxes))
			
	def set_mail_read(self, mail):
		pass
		# self.con.store(num,'+FLAGS','\Seen')

######################################
	def walk_mail_folder(self, mailFolder):
		rv, data = self.con.select(mailFolder)
		if rv != 'OK':
			print("ERROR: Unable to open mailbox ", rv)
			return
		print("Processing mailbox...\n")
		rv, data = self.con.search(None, "ALL")
		
		for mail_num in data[0].split():
			rv, data = self.con.fetch(mail_num, '(RFC822)')
			if rv != 'OK':
				print("ERROR getting message", num)
				return
			


if __name__ == '__main__':
	config = {
	'EMAIL_SERVER' : 'imap.126.com',
	'EMAIL_ACCOUNT' : 'qq859755014@126.com',
	'EMAIL_PASSWORD' : 'lrvxmouxswxizkgq'
	}


	imap = Imap(**config)
	print(imap.get_mail_folder())
	imap.walk_mail_folder('"INBOX"')
