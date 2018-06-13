import csv
import openpyxl

# Create a workbook
wb = openpyxl.Workbook()
# Create a worksheet
ws = wb.active


def csv2xlsx(csvFile, xlsxFile):
	with open(csvFile, 'r', encoding = 'utf-8') as f:
		reader = csv.reader(f, delimiter=',')
		for row in reader:
			ws.append(row)
	wb.save(xlsxFile)
	wb.close()


if __name__ == '__main__':
	# csv2xlsx('ss_server.csv')
