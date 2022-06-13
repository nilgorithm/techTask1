from ExcelReader import *
import re

data = ExReader(r'ТЗ, макрос от программиста.xlsx').res
DATASET = data['data']
BASE_CHECK = [re.findall(r'^\s*(.*)\n$',i)[0] for i in list(open('base_check.txt'))]
PERIOD = data['period']
SPECIAL_HAT = data['special_hat']
COMPANIES = data['companies']