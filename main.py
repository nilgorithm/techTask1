from lib.Model import Agregate

file = r".\example\ТЗ, макрос от программиста.xlsx"
delimiter = ',' #delimiter for csv

if __name__ == '__main__':
    app = Agregate(file=file, delim_csv=delimiter)
    app.result