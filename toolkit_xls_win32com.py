import win32com
from win32com.client import *
import sys

import toolkit_file, toolkit_xls



class _Excel():
	"""docstring for _Excel"""
	def __init__(self, xls_file):
		self.xlApp = win32com.client.Dispatch("Excel.Application")
		self.xlApp.Visible = False
		self.xlBook = self.xlApp.Workbooks.Open(xls_file)
		self.ws = self.xlBook.Worksheets("Sheet")

	def __enter__(self):
		return self

	def __exit__(self,Type, value, traceback):  
		'''
		Executed after "with"
		'''
		self.xlBook.Close(SaveChanges=1)
		self.xlApp.Quit()
		
	def get_table_size(self):
		'''
		Return the size of the table
		'''
		row = col = 1
		while self.ws.Cells(row, 1).Value:
			row += 1
		while self.ws.Cells(1, col).Value:
			col += 1
		return row, col

	def color_header(self, rgb):
		'''
		Paint header line with color (r, g, b)
		'''
		i = 1
		while self.ws.Cells(1, i).Value and i < 100:
			# self.ws.Cells(1, i).Value = i
			self.ws.Cells(1, i).Interior.color = toolkit_xls.rgb_to_hex(rgb)
			i += 1

if __name__ == '__main__':
	pass