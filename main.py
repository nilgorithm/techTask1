from lib.Model import Agregate

file = r".\example\ТЗ, макрос от программиста.xlsx"

if __name__ == '__main__':
    app = Agregate(file=file)
    app.result