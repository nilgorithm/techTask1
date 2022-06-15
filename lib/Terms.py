

class Terms:

    def __init__(self, base_sd, data, month_idx, d, current_service, PERIOD, BASE_CHECK, changes_names):
        self.base_sd = base_sd
        self.changes_names = changes_names
        self.data = data
        self.month_idx = month_idx
        self.d = d
        self.period = PERIOD
        self.current_service = current_service
        self.base_check = BASE_CHECK
        self.res = self.resulter()
    
        
    # Отключение услуги/клиента
    def Churn_Current_Service_Client(self):
        # print(self.base_sd)
        # print(self.data)
        # print(self.current_service)
        # print(self.period[self.month_idx])
        # input()
        if self.month_idx-1 < 0:
            return False
        # print('sucsess')
        val_k = self.data[self.period[self.month_idx-1]][1]
        # print(val_k)
        # print(self.base_check)
        # input()
        if val_k not in self.base_check:
            # print('поч то тут обосралось')
            # input()
            return False
        val = self.data[self.period[self.month_idx]][0]
        prev_val = self.data[self.period[self.month_idx-1]][0]
        # print('sucsess2')
        # input()
        if val: # если вал есть 
            return False
        # print('sucsess3')
        # input()
        if not prev_val: # если преввал нет 
            return False
        # print('sucsess4')
        # input()
        if len(self.base_sd['base_check'][self.period[self.month_idx]]['service']) == 0:
            self.d[self.period[self.month_idx]]['type'] = self.changes_names['Churn Client']
            self.GetDefinition()
        else:
            self.d[self.period[self.month_idx]]['type'] = self.changes_names['Churn Service']
            self.GetDefinition()


    # Новая услуга
    def New_Service_Client(self):
        if self.month_idx-1 < 0:
            return False
        val_k = self.data[self.period[self.month_idx]][1]
        if val_k not in self.base_check:
            return False
        val = self.data[self.period[self.month_idx]][0]
        prev_val = self.data[self.period[self.month_idx-1]][0]
        if prev_val:
            return False
        if not val:
            return False
        vals = 0
        vals_k_check = 0
        start = self.month_idx - 6 if self.month_idx - 6 >= 0 else 0
        for month in self.period[start:self.month_idx]:
            vals += len(self.base_sd['base_check'][month]['service'])
            # print('\n')
            # print(self.base_sd['base_check'][month]['service'])
            # print(len(self.base_sd['base_check'][month]['service']))
            # print('\n')
            for service in set(self.base_sd['base_check'][month]['service']):
                if service == self.current_service:
                    vals_k_check +=1
        # print('месяц', self.period[self.month_idx])
        # print('диапазон', self.period[start:self.month_idx])
        # print('проверяемая услуга: ',self.current_service)
        # print('эта услуга в прошлом: ',vals_k_check)
        # print('другие в прошлом: ',vals)
        # print(self.base_sd)
        # input()
        if vals > 0:
            if vals_k_check == 0:            
                self.d[self.period[self.month_idx]]['type'] = self.changes_names['New Service']
                self.GetDefinition()
                # print('New Service')
                # input()
            elif len(self.base_sd['base_check'][self.period[self.month_idx-1]]['service'])>0:
                self.d[self.period[self.month_idx]]['type'] = self.changes_names['Service Return']
                self.GetDefinition()
                # print('Service Return')
                # input()
            else:
                self.d[self.period[self.month_idx]]['type'] = self.changes_names['Client Return']
                self.GetDefinition()
                # print('Client Return')
                # input()
        else:
            self.d[self.period[self.month_idx]]['type'] = self.changes_names['New Client']
            self.GetDefinition()
            # print('New Client')
            # input()
        
        # Поднятие чека 
    def Raise_Fix(self):
        if self.month_idx-1 < 0:
            return False
        val_k = self.data[self.period[self.month_idx]][1]
        
        if val_k not in self.base_check or val_k == 'Performance':
            return False
        val = self.data[self.period[self.month_idx]][0]
        prev_val = self.data[self.period[self.month_idx-1]][0]
        if not prev_val or not val:
            return False
        if prev_val > val:
            self.d[self.period[self.month_idx]]['type'] = self.changes_names['Reduce Fix']
            self.GetDefinition()
        elif prev_val < val:
            self.d[self.period[self.month_idx]]['type'] = self.changes_names['Raise Fix']
            self.GetDefinition()



    def Churn_CPA(self):
        # print('kaka')
        # input()
        if self.month_idx-1 < 0:
            return False
        val_k = self.data[self.period[self.month_idx]][1]
        if not val_k:
            return False
        if val_k.find('Overlimit') !=-1:
            self.d[self.period[self.month_idx]]['type'] = self.changes_names['CPA']
            self.GetDefinition()
            if self.month_idx < len(self.period)-1:
                self.d[self.period[self.month_idx+1]]['type'] = self.changes_names['CPA']
        elif val_k == 'Performance':
            start = self.month_idx - 3 if self.month_idx - 3 > 0 else 0
            pvals = 0
            for month in self.period[start:self.month_idx]:
                if self.data[month][1] == 'Performance':
                    pvals += self.data[month][0]
            if self.d[self.period[self.month_idx]]['type'] == 'No Changes':
                if pvals/len(self.period[start:self.month_idx])/2 > self.data[self.period[self.month_idx]][0]:
                    self.d[self.period[self.month_idx]]['type'] = self.changes_names['Churn CPA']
                    self.GetDefinition()
                else:
                    self.d[self.period[self.month_idx]]['type'] = self.changes_names['CPA']
                    self.GetDefinition()


    def One_time_service(self):
        if self.month_idx-1 < 0:
            return False
        val_k = self.data[self.period[self.month_idx]][1]
        if not val_k:
            return False
        if val_k.find('Validation') == -1:
            return False
        else:
            self.d[self.period[self.month_idx]]['type'] = self.changes_names['One-time service']
            self.GetDefinition()
            if self.month_idx < len(self.period)-1:
                self.d[self.period[self.month_idx+1]]['type'] = self.changes_names['One-time service']
                # print(self.d)
                # print('ok')
                # print(self.d[self.period[self.month_idx+1]]['type'])

    def GetDefinition(self):
        if self.month_idx-1 < 0:
            return False
        curr_val_check = self.data[self.period[self.month_idx]][0]
        val = curr_val_check if curr_val_check else 0
        prev_check = self.data[self.period[self.month_idx-1]][0]
        prev_val = prev_check if prev_check else 0 
        self.d[self.period[self.month_idx]]['amount'] = val - prev_val #if prev_check or curr_val_check else  '-'
        

    def resulter(self):
        for f in [self.Churn_Current_Service_Client, self.New_Service_Client, self.Raise_Fix, self.One_time_service, self.GetDefinition, self.Churn_CPA]:
            tmp = f()
            if tmp:
                break
        return self.d
