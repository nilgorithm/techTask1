# class Clock:
#     __DAY = 86400   # число секунд в одном дне
 
#     def __init__(self, seconds: int):
#         if not isinstance(seconds, int):
#             raise TypeError("Секунды должны быть целым числом")
#         self.seconds = seconds % self.__DAY
 
#     def get_time(self):
#         s = self.seconds % 60            # секунды
#         m = (self.seconds // 60) % 60    # минуты
#         h = (self.seconds // 3600) % 24  # часы
#         return f"{self.__get_formatted(h)}:{self.__get_formatted(m)}:{self.__get_formatted(s)}"
 
#     @classmethod
#     def __get_formatted(cls, x):
#         return str(x).rjust(2, "0")

# c1 = Clock(1000)
# c2 = Clock(1000)
# print(c1.get_time())
# print(c1 == c2)


# class A:
#     def __init__(self, d):
#         self.d = d

#     def res(self):
#         self.__all()
#         r = self.d
#         if hasattr(self, 'pif'):
#             r['pif'] = self.pif
#         return r

#     def __all(self):
#         print(self.__dict__)
#         method_keys = [key for key in A.__dict__.keys() if 'calc' in key and callable(A.__dict__[key])]
#         print(A.__dict__.keys())
#         for method_key in method_keys:
#             print(method_key)
#             method = A.__dict__[method_key]
#             method(self)


#     def __calc_pif(self):
#         self.pif = self.d['a']**2 + self.d['b']**2 == self.d['c']**2

        



# d = {'a':4, 'b':3, 'c':5}

# a = A(d)

# print(a.res())



data = [
    {
        'fruits': {
            'apples': 1,
            'oranges': 1,
            'grapes': 2
            },
        'vegetables': {
            'carrots': 6,
            'beans': 3,
            'peas': 2
        },
        'grains': 4,
        'meats': 1  
    },
    {
        'fruits': {
            'apples': 3,
            'oranges': 5,
            'grapes': 8
            },
        'vegetables': {
            'carrots': 7,
            'beans': 4,
            'peas': 3
        },
        'grains': 3,
        'meats': 2  
    },
    {
        'fruits': {
            'apples': 13,
            'oranges': 21,
            'grapes': 34
            },
        'vegetables': {
            'carrots': 8,
            'beans': 5,
            'peas': 4
        },
        'grains': 2,
        'meats': 3
    },
]


from collections import defaultdict
import pprint

def merge(d, s_d):
    for k, v in s_d.items():
        if isinstance(v, dict):
            merge(d[k], v)
        else: 
            d[k] = d.setdefault(k, 0) + v

# https://stackoverflow.com/a/19189356/4909087    
nested = lambda: defaultdict(nested)
d = nested()

for subd in data:
    merge(d, subd)

pprint.pprint(d)




from ExcelReader import *
import numpy as np
from collections import defaultdict
import pprint

data = ExReader(r'C:\it\way\ТЗ, макрос.xlsx').res

class Company:
    hat = data['hat'] # шапка для таблицы (пока хз нужна тут или нет)
    period = data['period'] # весь период месяцов
    fm = period[0] # first month
    lm = period[-1] #last month

    def __init__(self, name:str):
        self.name = name # super_dict k
        self.kept_data = {} # super_dict v
        
        
    def add_data(self, got_data:pd.Series):
        self.service_type = got_data['Услуга']
        self.calc_type = got_data['Форма расчета']
        self.paid_months = {i:got_data[i] for i in self.period}
        # self.paid_months = {i:got_data[i] for i in self.period if got_data[i]}
        # self.p_d = {'col1':pd.Series({i:self.calc_type for i in self.period if got_data[i]}), 'col2':pd.Series(self.paid_months)}
        # self.p_d = {'value':pd.Series(self.paid_months), 'type':pd.Series([self.calc_type]*len(self.paid_months), index = list(self.paid_months.keys()))}
        # self.paid_months = {i:got_data[i] for i in self.period}
        # print(pd.DataFrame(data = self.p_d, index=self.period))
        # self.merge(self.kept_data, self.service_type, self.calc_type, pd.DataFrame(data = self.p_d, index=self.period))

        # получив тип услуги, тип расчета и оплаченные месяца по этому типу, 
        # формируем под каждый доммен свой агрегированный дикт
        self.merge(self.kept_data, self.service_type, self.calc_type, pd.Series(self.paid_months))


        
    def merge(self, d, gen_key, calc_key, s_d):
            if gen_key not in d:
                d[gen_key] = {calc_key:s_d}
            elif calc_key not in d[gen_key]:
                d[gen_key][calc_key] = s_d
            else:
                d[gen_key][calc_key] = d[gen_key][calc_key].add(s_d, fill_value=0)

# class A(Company):

#     def res(self):
#         self.__all()
#         r = self.d
#         if hasattr(self, 'pif'):
#             r['pif'] = self.pif
#         return r

#     def __all(self):
#         print(self.__dict__)
#         method_keys = [key for key in A.__dict__.keys() if 'calc' in key and callable(A.__dict__[key])]
#         for method_key in method_keys:
#             print(method_key)
#             method = A.__dict__[method_key]
#             method(self)


#     def __calc_pif(self):
#         self.pif = self.d['a']**2 + self.d['b']**2 == self.d['c']**2
        
super_dict = {i:Company(i) for i in data['companies']}

for i in data['data']:
    super_dict[i['Домен']].add_data(pd.Series(i).fillna(0))
print(super_dict['domen1'].kept_data)




# Отключение услуги 
def Churn_Current_Service_Client(base_sd, data, month_idx, d, period, current_service):
    val_k = data[period[month_idx-1]][1]
    if val_k not in base_check:
        return False
    val = data[period[month_idx]][0]
    if month_idx-1 < 0:
        return False
    prev_val = data[period[month_idx-1]][0]
    if val:
        return False
    if not prev_val:
        return False
    if len([i for i in base_sd['base_check'][period[month_idx]].keys() if i != 'service']) == 0:
        d[period[month_idx]]['type'] = 'Churn Current Client'
    else:
        d[period[month_idx]]['type'] = 'Churn Current Service' 

# Новая услуга
def New_Service_Client(base_sd, data, month_idx, d, period, current_service):
    if month_idx-1 < 0:
        return False
    val_k = data[period[month_idx]][1]
    if val_k not in base_check:
        return False
    val = data[period[month_idx]][0]
    prev_val = data[period[month_idx-1]][0]
    if prev_val:
        return False
    if not val:
        return False
    vals = 0
    vals_k_check = 0
    start = month_idx - 6 if month_idx - 6 > 0 else 0
    for month in period[start:month_idx]:
        vals += len([ i for i in base_sd['base_check'][month].keys() if i != 'service'])
        for service in set(base_sd['base_check'][month]['service']):
            if service == current_service:
                vals_k_check +=1
    if vals_k_check == 0:
        if vals > 0:
            if len(base_sd['base_check'][period[month_idx-1]].keys()) <=1:
                d[period[month_idx]]['type'] = 'Client Return'
            else: 
                d[period[month_idx]]['type'] = 'New Service'
        else:
            d[period[month_idx]]['type'] = 'New Client'
    else:
        if vals > 0 and len(base_sd['base_check'][period[month_idx-1]].keys())>1:
            d[period[month_idx]]['type'] = 'Service Return'
    
    # Поднятие чека 
def Raise_Fix(base_sd, data, month_idx, d, period, current_service):
    if month_idx-1 < 0:
        return False
    val_k = data[period[month_idx]][1]
    
    if val_k not in base_check or val_k == 'Performance':
        return False
    val = data[period[month_idx]][0]
    prev_val = data[period[month_idx-1]][0]
    if not prev_val or not val:
        return False
    if prev_val > val:
        d[period[month_idx]]['type'] = 'Reduce Fix'
    elif prev_val < val:
        d[period[month_idx]]['type'] = 'Raise Fix'


def Churn_CPA(base_sd, data, month_idx, d, period, current_service):
    if month_idx-1 < 0:
        return False
    val_k = data[period[month_idx]][1]
    if not val_k:
        return False
    if val_k.find('Overlimit') !=-1:
        d[period[month_idx]]['type'] = 'CPA'
    elif val_k == 'Performance':
        start = month_idx - 3 if month_idx - 3 > 0 else 0
        pvals = 0
        for month in period[start:month_idx]:
            if data[month][1] == 'Performance':
                pvals += data[month][0]
        if pvals/len(period[start:month_idx])/2 > data[period[month_idx]][0]:
            d[period[month_idx]]['type'] = 'Churn CPA'
        else:
            d[period[month_idx]]['type'] = 'CPA'

def One_time_service(base_sd, data, month_idx, d, period, current_service):
    val_k = data[period[month_idx]][1]
    if not val_k:
        return False
    if val_k.find('Validation') == -1:
        return False
    else:
        d[period[month_idx]]['type'] = 'One-time service'