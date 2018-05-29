import win32com.client as win32

class _Outlook():
	def __init__(self):
		app = 'Outlook'
		self.app = win32.gencache.EnsureDispatch("%s.Application" % app)
		self.outlookAPI = self.app.GetNamespace("MAPI")
		self.inbox = self.outlookAPI.GetDefaultFolder(win32.constants.olFolderInbox)

	def send_mail(self, subj, body, recipients = ['chdu@merkleinc.com']):
		print("Subject: " + subj)
		print("Body: " + body)
		print("Send to: " + str(recipients))
		mail = self.app.CreateItem(win32.constants.olMailItem)
		for i in recipients:
			mail.Recipients.Add(i)

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

outlook = _Outlook()

if __name__ == '__main__':
	print(outlook.fetch_inbox_folders())