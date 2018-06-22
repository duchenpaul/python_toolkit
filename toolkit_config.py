'''
Retrun the config in dict
'''

import configparser, os.path

config_file = os.path.dirname(os.path.realpath(__file__)) + os.sep + 'config.ini'


def read_config_mail():
	try:
		print('Read config file: ' + config_file )
		configRead = configparser.ConfigParser()
		configRead.read("config.ini")

		sectionName = 'mail'
		options = [ i.upper() for i in configRead.options(sectionName) ]
		config = {}
		for j in options:
			config[j] = configRead[sectionName][j]

	except Exception as e:
		print("Error read config file, check config.ini")
		print(e)
		raise
	return config


def read_config_mysql():
	try:
		print('Read config file: ' + config_file )
		configRead = configparser.ConfigParser()
		configRead.read(config_file)
		config = {
			'host': configRead['datebase']['host'],
			'port': int(configRead['datebase']['port']),
			'user': configRead['datebase']['user'],
			'passwd': configRead['datebase']['passwd'],
			'db': configRead['datebase']['db'],
			'charset': 'utf8'
		}
	except Exception as e:
		print("Error read config file, check config.ini")
		print(e)
		raise
	return config

if __name__ == '__main__':
	config = read_config_mail()
	print(config)