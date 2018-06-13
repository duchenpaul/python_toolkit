import win32com.client as win32
import sys

default_recipients = 'chdu@merkleinc.com'

class _Outlook():
	def __init__(self):
		app = 'Outlook'
		self.app = win32.gencache.EnsureDispatch("%s.Application" % app)
		self.outlookAPI = self.app.GetNamespace("MAPI")
		self.inbox = self.outlookAPI.GetDefaultFolder(win32.constants.olFolderInbox)
		self.deletedBox = self.outlookAPI.GetDefaultFolder(win32.constants.olFolderDeletedItems)

	def send_mail(self, subj, body, recipients = ['chdu@merkleinc.com'], attachment_path = None):
		'''
		Attachment can be list or string
		'''
		print("Subject: " + subj)
		print("Body: " + body)
		print("Send to: " + str(recipients))
		mail = self.app.CreateItem(win32.constants.olMailItem)
		for i in recipients:
			mail.Recipients.Add(i)


		if attachment_path is not None:
			if type(attachment_path) is str:
				mail.Attachments.Add(Source=attachment_path)
			elif type(attachment_path) is list:
				for i in attachment_path:
					print('Add {} as attachment'.format(i))
					mail.Attachments.Add(Source=i)

		mail.Subject = subj
		mail.Body = body
		mail.Send()
		print('Mail sent')

	def fetch_inbox_folders(self):
		'''
		Return the list of outlook folders
		'''
		fldr_iterator = self.inbox.Folders
		return [i.Name for i in fldr_iterator]


	def fetch_folder(self, folderName):
		'''
		Fetch the subject of mail in a folder
		'''
		# Fetch inbox
		folder = self.outlookAPI.GetDefaultFolder(6)

		# folder = self.inbox.Folders[folderName]
		messages = folder.Items
		return [ message.Subject for message in messages ]

	def empty_folder(self, folderName):
		'''
		Put all mails in the folder into deleted box
		'''
		folder = self.inbox.Folders[folderName]
		messages = folder.Items
		deletedItem = ['init']
		while len(deletedItem):
			deletedItem = []
			for message in messages:
				print('Delete {}'.format(message.Subject))
				deletedItem.append(message.Subject)
				try:
					message.Delete()
				except Exception as e:
					print("Err, try again")
					self.empty_folder(folderName)

				

	def empty_junkbox(self):
		'''
		Purge all mails in the deleted box
		'''
		deletedItem = ['init']
		while len(deletedItem):
			deletedItem = []
			for i in self.deletedBox.Items:
				deletedItem.append(i.Subject)
				i.Delete()
			print('Deleted {} mails'.format(len(deletedItem)))

		print("Purge done")


outlook = _Outlook()

def outlook_send_mail(subj, body, recipients = [default_recipients], attachment_path = None):
	outlook.send_mail(subj, body, attachment_path = None)


if __name__ == '__main__':
	# folder = outlook.empty_folder('[ Notification ] Filebridge')
	clear_list = ['[ Notification ] Carters', '[ Notification ] iBase', '[ Notification ] Bose', '[ Notification ] System', '[ Notification ] Filebridge']
	# folder = outlook.empty_folder('[ Notification ] Carters')
	
	for i in clear_list:
		outlook.empty_folder(i)
		pass

	print('Dumping junkbox...')
	outlook.empty_junkbox()

	# for message in folder.Items:
	# 	print('Del: ' + message.Subject)
	# 	message.Delete()
	# 	list.append(message.Subject)
	# 	a = message	
	
	# outlook_send_mail('23', '33')
	# 

