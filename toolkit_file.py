import os
import os.path
import glob
from pathlib import Path


def get_basename(FILE):
    '''
    Return the basename of a file. e.g. example.txt -> example
    '''
    return os.path.splitext(os.path.basename(FILE))[0]


def file_path(FILE):
    return os.path.dirname(os.path.realpath(FILE)) + os.sep


def script_path():
    return os.path.dirname(os.path.realpath(__file__))


def line_prepender(filename, line):
    '''
    Add line to the head of a file
    '''
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)


def get_file_list(folder):
    file_list = []
    for path, subdirs, files in os.walk(folder):
        for name in files:
            file_list.append(os.path.join(path, name))
    return file_list


def purge_folder(folder):
    # filelist = [ f for f in os.listdir(folder) ] #if f.endswith(".bak") ]
    filelist = glob.glob(folder + os.sep + '*')
    for f in filelist:
        print(f)
        # os.remove(os.path.join(f)) # using glob
        # os.remove(os.path.join(folder, f)) # using listdir


def create_folder(folderName):
    '''Create folder if not exists'''
    my_file = Path(folderName)
    if not my_file.is_dir():
        print('Folder {} not found, creating a new one'.format(folderName))
        os.mkdir(folderName)


if __name__ == '__main__':
    print(get_file_list('E:\\'))