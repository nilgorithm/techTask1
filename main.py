from lib.Model import Agregate

file = r".\example\ТЗ, макрос от программиста.xlsx"
delimiter = ',' #delimiter for csv

# file = r"C:\Users\User\OneDrive\Рабочий стол\RR\отток бизнеса\РБ\отток бизнеса RR.xlsx"
# delimiter = ';' #delimiter for csv

if __name__ == '__main__':
    app = Agregate(file=file, delim_csv=delimiter)
    app.result