from openpyxl import load_workbook
import pandas as pd

class ExReader:

    def __init__(self, file_name):
        self.file_name = file_name
        self.res = self.returner()
         

    def get_source_from_excel(self):
        wb = load_workbook(self.file_name)
        xls = pd.ExcelFile(self.file_name)
        sheets = xls.book.worksheets
        variable_index = [i.title for i in sheets].index('revenue 1C') # получили индекс нужного листа чтобы закинуть его в WB => должен существовать лист с названием: revenue 1C
        ws = wb[sheets[variable_index].title]
        data = []
        for row in ws: 
            if ws.row_dimensions[row[0].row].hidden == False:
                row_values = [cell.value for cell in row]
                data.append(row_values)
        return data

    def returner(self):
        fpddata = self.get_source_from_excel()
        special_hat = fpddata[0][:2]
        hat = fpddata[0]
        period = hat[3:]
        data = fpddata[1:20]
        df = pd.DataFrame(data, columns = hat).T.to_dict().values()
        companies = set(map(lambda x : x['Домен'], df))
        counter = set(map(lambda x : x['Форма расчета'], df))
        return {'special_hat':special_hat, 'hat':hat, 'period':period, 'companies':companies, 'counter':dict(zip(range(len(counter)),counter)), 'data':list(df)}