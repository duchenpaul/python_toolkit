import win32com.client as win32

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
		folder = self.inbox.Folders[folderName]
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
					print(e)

				

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

if __name__ == '__main__':
	# outlook.empty_folder('[ Notification ] iBase')
	folder = outlook.empty_junkbox()
	# # print(help(folder))
	# for message in folder.Items:
	# 	# print('Del: ' + message.Subject)
	# 	# message.Delete()
	# 	# list.append(message.Subject)
	# 	a = message	

	# print(type(a))
	# print(help(a))
	# print(dir(a))