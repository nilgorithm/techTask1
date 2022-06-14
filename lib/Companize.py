import pandas as pd
class Company:

    def __init__(self, name:str, PERIOD):
        self.name = name # super_dict k
        self.kept_data = {} # super_dict v
        self.dalphabet = {chr(lowercase):chr(lowercase+(ord('A')-ord('a'))) for lowercase in range(ord("a"), ord("z")+1)} 
        self.period = PERIOD
        
    def add_data(self, got_data:pd.Series):
        self.service_type = got_data['Услуга']
        self.calc_type = got_data['Форма расчета']
        check_lowercase = self.service_type if self.service_type[0] not in self.dalphabet else self.dalphabet[self.service_type[0]] + self.service_type[1:]
        self.service_type = check_lowercase
        self.paid_months = {i:got_data[i] for i in self.period if got_data[i]}
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