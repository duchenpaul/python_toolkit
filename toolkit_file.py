import os
import os.path
import glob

def get_basename(FILE):
	'''
	Return the basename of a file. e.g. example.txt -> example
	'''
	return os.path.splitext(FILE)[0]

def script_path():
	return os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')

def line_prepender(filename, line):
	'''
	Add line to the head of a file
	'''
	with open(filename, 'r+') as f:
		content = f.read()
		f.seek(0, 0)
		f.write(line.rstrip('\r\n') + '\n' + content)


def purge_folder(folder):
	filelist = [ f for f in os.listdir(folder) ] #if f.endswith(".bak") ]
	filelist = glob.glob(folder + os.sep + '*')
	for f in filelist:
		print(f)
		# os.remove(os.path.join(folder, f))

if __name__ == '__main__':
	pass