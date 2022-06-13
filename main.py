import csv
from Terms import *
from Companize import *
from constants import *
from clint.textui import progress

   
super_dict = {i:Company(i) for i in COMPANIES}

for i in DATASET:
    super_dict[i['Домен']].add_data(pd.Series(i).fillna(False))
special_period = [PERIOD[i] +' - '+ PERIOD[i+1] for i in range(len(PERIOD)-1)]
[special_period.insert(i, 'Amount') for i in range(len(special_period), 0, -1)]

with open('res.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows([SPECIAL_HAT+PERIOD*2+['-','-']+special_period])

for comp in progress.bar(sorted(COMPANIES)):
    test_frame = super_dict[comp].kept_data
    name = super_dict[comp].name
    tab_1 = []
    tab_2 = []
    tab_3 = []
    
    for service in test_frame:
        info = [name, service]
        temp = {'base':{}, 'not_base':{}}
        
        for payment in test_frame[service]:
            for month in PERIOD:
                if month in test_frame[service][payment]:
                    if payment in BASE_CHECK:
                        temp['base'][month] = [test_frame[service][payment][month],payment]
                    else:
                        if payment not in temp['not_base']:
                            temp['not_base'][payment] = {month:[test_frame[service][payment][month],payment]}
                        else:
                            temp['not_base'][payment][month] = [test_frame[service][payment][month],payment]    
        temp_p = []
        temp_t = []
        for i in PERIOD:
            if i in temp['base']:
                temp_p.append(temp['base'][i][0])
                temp_t.append(temp['base'][i][1])
            else:
                temp_p.append(None)
                temp_t.append(None)

        tab_1.append(info+temp_p)
        tab_2.append(temp_t)

        for payment in temp['not_base']:
            more_temps_p_ex = []
            more_temps_t_ex = []
            for i in PERIOD:
                if i in temp['not_base'][payment]:
                    more_temps_p_ex.append(temp['not_base'][payment][i][0])
                    more_temps_t_ex.append(temp['not_base'][payment][i][1])
                else:
                    more_temps_p_ex.append(None)
                    more_temps_t_ex.append(None)
            tab_1.append(info + more_temps_p_ex)
            tab_2.append(more_temps_t_ex)

    tab_1_tab_2_zip = [list(zip(tab_1[x][2:], tab_2[x])) for x in range(len(tab_1))]
    df = pd.DataFrame(data = tab_1_tab_2_zip, columns=PERIOD)
    slice_dict = {'base_check':{m:{'service':[]} for m in PERIOD}, 'not_base_check':{m:{} for m in PERIOD}}
    service_dict = {i:tab_1[i][1] for i in range(len(tab_1))}

    for i, m in enumerate(PERIOD):
        t=-1
        for price, payment_t in df[m]:
            t+=1
            if payment_t in BASE_CHECK:
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
        dicter = {m:{'type':'No Changes', 'amount':'-'} for m in PERIOD}
        CPA_check = None
        for mth_idx, _ in enumerate(PERIOD):
            Terms(slice_dict, df[i], mth_idx, dicter, service_dict[i]).res
            if df[i][_][1] and (df[i][_][1] == 'Performance' or df[i][_][1].find('Overlimit') != -1):
                CPA_check = True

        if CPA_check:
            for m in PERIOD:
                if dicter[m]['type'] != 'Churn CPA':
                    dicter[m]['type'] = 'CPA'
        temp = []
        for m in PERIOD:
            temp.append(dicter[m]['type'])
            temp.append(dicter[m]['amount'])
        tab_3.append(temp)

    final_res = [tab_1[x]+tab_2[x]+tab_3[x] for x in range(len(tab_1))]
    with open('res.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(final_res)