# from os import pread
import pandas  as pd
from ExcelReader import *
import numpy as np
from CONSTANTS import *



        
super_dict = {i:Company(i) for i in data['companies']}

for i in data['data']:
    super_dict[i['Домен']].add_data(pd.Series(i).fillna(False))

test_frame = super_dict['domen1'].kept_data
period = data['period']
name = 'domen1'
base_check = [re.findall(r'^\s*(.*)\n$',i)[0] for i in list(open('base_check.txt'))]

tab_1 = []
tab_2 = []
tab_3 = []
for service in test_frame:
    info = [name, service]
    temp = {'base':{}, 'not_base':{}}
    
    for payment in test_frame[service]:
        for month in period:
            if month in test_frame[service][payment]:
                if payment in base_check:
                    temp['base'][month] = [test_frame[service][payment][month],payment]
                else:
                    if payment not in temp['not_base']:
                        temp['not_base'][payment] = {month:[test_frame[service][payment][month],payment]}
                    else:
                        temp['not_base'][payment][month] = [test_frame[service][payment][month],payment]    
    temp_p = []
    temp_t = []
    for i in period:
        if i in temp['base']:
            temp_p.append(temp['base'][i][0])
            temp_t.append(temp['base'][i][1])
        else:
            temp_p.append(None)
            temp_t.append(None)

    tab_1.append(info+temp_p)
    tab_2.append(info+temp_t)

    for payment in temp['not_base']:
        more_temps_p_ex = []
        more_temps_t_ex = []
        for i in period:
            if i in temp['not_base'][payment]:
                more_temps_p_ex.append(temp['not_base'][payment][i][0])
                more_temps_t_ex.append(temp['not_base'][payment][i][1])
            else:
                more_temps_p_ex.append(None)
                more_temps_t_ex.append(None)
        tab_1.append(info + more_temps_p_ex)
        tab_2.append(info + more_temps_t_ex)

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
    if len(base_sd['base_check'][period[month_idx]]) == 0:
        d[period[month_idx]] = 'Churn Current Client'
    else:
        d[period[month_idx]] = 'Churn Current Service' 

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
        # print(base_sd['base_check'][month]['service'])
        for service in set(base_sd['base_check'][month]['service']):
            if service == current_service:
                vals_k_check +=1
    if vals_k_check == 0:
        if vals > 0:
            if len(base_sd['base_check'][period[month_idx-1]].keys()) <=1:
                d[period[month_idx]] = 'Client Return'
            else: 
                d[period[month_idx]] = 'New Service'
        else:
            d[period[month_idx]] = 'New Client'
    else:
        if vals > 0 and len(base_sd['base_check'][period[month_idx-1]].keys())>1:
            d[period[month_idx]] = 'Service Return'
    
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
        d[period[month_idx]] = 'Reduce Fix'
    if prev_val < val:
        d[period[month_idx]] = 'Raise Fix'
    else:
        return False

def Churn_CPA(base_sd, data, month_idx, d, period, current_service):
    if month_idx-1 < 0:
        return False
    val_k = data[period[month_idx]][1]
    if not val_k:
        return False
    if val_k.find('Overlimit') !=-1:
        d[period[month_idx]] = 'CPA'
    elif val_k == 'Performance':
        start = month_idx - 3 if month_idx - 3 > 0 else 0
        pvals = 0
        for month in period[start:month_idx]:
            if data[month][1] == 'Performance':
                pvals += data[month][0]
        if pvals/len(period[start:month_idx])/2 > data[period[month_idx]][0]:
            d[period[month_idx]] = 'Churn CPA'
        else:
            d[period[month_idx]] = 'CPA'

def One_time_service(base_sd, data, month_idx, d, period, current_service):
    val_k = data[period[month_idx]][1]
    if not val_k:
        return False
    if val_k.find('Validation') == -1:
        return False
    else:
        d[period[month_idx]] = 'One-time service'

    
mega_kaka = [list(zip(tab_1[x][2:], tab_2[x][2:])) for x in range(len(tab_1))]
df = pd.DataFrame(data = mega_kaka, columns=period)
slice_dict = {'base_check':{m:{'service':[]} for m in period}, 'not_base_check':{m:{} for m in period}}
service_dict = {i:tab_1[i][1] for i in range(len(tab_1))}

for i, m in enumerate(period):
    t =-1
    for price, payment_t in df[m]:
        t+=1
        if payment_t in base_check:
            if payment_t not in slice_dict['base_check'][m]:
                slice_dict['base_check'][m][payment_t] = price
                slice_dict['base_check'][m]['service'] = [service_dict[t]]
            else:
                slice_dict['base_check'][m][payment_t] += price
                slice_dict['base_check'][m]['service'] += [service_dict[t]]
        else:
            if payment_t:
                if payment_t not in slice_dict['not_base_check'][m]:
                    slice_dict['not_base_check'][m][payment_t] = price
                    slice_dict['not_base_check'][m]['service'] = [service_dict[t]]
                else:
                    slice_dict['not_base_check'][m][payment_t] += price
                    slice_dict['not_base_check'][m]['service'] += [service_dict[t]]

df = df.T

for i in range(len(tab_1)):
    dicter = {m:'No Changes' for m in period}

    for mth_idx, _ in enumerate(period):
        for f in [Churn_CPA,Churn_Current_Service_Client, New_Service_Client, Raise_Fix, One_time_service]:
            tmp = f(slice_dict, df[i], mth_idx, dicter, period,service_dict[i])
            if tmp:
                break
    tab_3.append(list(dicter.values()))

jopny_vypuk = [tab_1[x]+tab_2[x][2:]+tab_3[x] for x in range(len(tab_1))]
print(pd.DataFrame(data = jopny_vypuk, columns=data['special_hat']+period*3).T)
print(test_frame)

