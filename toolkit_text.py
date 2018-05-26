import re
import base64
import csv

#######################################################################
def decode_base64(data):
	"""Decode base64, padding being optional.

	:param data: Base64 data as an ASCII byte string
	:returns: The decoded byte string.

	"""
	missing_padding = len(data) % 4
	if missing_padding != 0:
		data += '='* (4 - missing_padding)
	return base64.urlsafe_b64decode(data).decode('utf-8')


def encode_base64(data):
	"""
	base64 encode
	"""
	return base64.urlsafe_b64encode(data.encode()).decode('utf-8')

########################################################################
# Regex

def regex_find(text, patten, string):
	'''
	return list
	'''
	match_return = re.compile(patten, re.IGNORECASE).findall(text)
	if match_return:
		print('-'*20)
		print(patten + ' detected. ' + 'Count: ' + str(len(match_return)))
		print(str(match_return), ' -> ', string)
		print('-'*20)
	return match_return

def regex_replace(text, patten, string):
	'''
	return list
	'''
	return re.sub(patten, string, text, flags=re.IGNORECASE)

def regex_replace_file(FILENAME, patten, string, exception = None):
	'''
	Replace the regex patten with string of a file, except exceptions
	'''
	with open(FILENAME, 'r') as f:
		text = f.read()

	if exception and re.compile(exception, re.IGNORECASE).findall(text):
		print(" - Skip " + exception)
		return
	with open(FILENAME, 'w') as f:
		f.write(re.sub(patten, string, text, flags=re.IGNORECASE))

########################################################################


########################################################################
# csv <-> list

def csv2list(FILE):
	'''Import csv to list'''
	csv_list = []
	with open(FILE, encoding = 'utf-8') as csvfile:
		# Detect header, remove if exists
		has_header = csv.Sniffer().has_header(csvfile.read(1024))
		csvfile.seek(0)  # Rewind.
		reader = csv.reader(csvfile)
		if has_header:
			# print("Header detected, skip.")
			next(reader)  # Skip header row
		return list(csv.reader(csvfile, delimiter=','))

def list2csv(list, FILE):
	listHeader = ['col1', 'col2']
	with open(FILE, 'w', encoding = 'utf-8', newline='') as f:
		writer = csv.writer(f)
		f.write(', '.join(listHeader))
		f.write('\n')
		writer.writerows(list)

########################################################################


########################################################################
# csv <-> dict

def dict2csv(dictList, fileName):
	'''
	Input: dictList
	Output: csv file
	'''
	keys = dictList[0].keys()
	with open(fileName, 'w', encoding = 'utf-8', newline='') as output_file:
		dict_writer = csv.DictWriter(output_file, keys)
		dict_writer.writeheader()
		dict_writer.writerows(dictList)

def csv2dict(csv_file):
	'''
	Iutput: csv file
	Onput: dictList
	'''
	pass

########################################################################

def csv2table(fileName, table):
	pass

if __name__ == '__main__':
	print(csv2list('./fileName.csv'))
