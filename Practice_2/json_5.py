import csv
import numpy as np
import json
import pickle
import msgpack
import os

counter = 1
serum_creatinine_sum = 0.0
men_count = 0
women_count = 0
stat_dict = {}
waistline_list = []
with open('dataset.csv', 'r') as file:

    reader = csv.DictReader(file)
    # sex,age,height,weight,waistline,sight_left,sight_right,hear_left,hear_right,
    # SBP,DBP,BLDS,tot_chole,HDL_chole,LDL_chole,triglyceride,hemoglobin,urine_protein,
    # serum_creatinine,SGOT_AST,SGOT_ALT,gamma_GTP,SMK_stat_type_cd,DRK_YN
    for line in reader:

        if 'max_age' in stat_dict:
            stat_dict['max_age'] = max(int(line['age']), stat_dict['max_age'])
        else:
            stat_dict['max_age'] = 0
            stat_dict['max_age'] = max(int(line['age']), stat_dict['max_age'])

        if 'min_height' in stat_dict:
            stat_dict['min_height'] = min(int(line['height']), stat_dict['min_height'])
        else:
            stat_dict['min_height'] = 250
            stat_dict['min_height'] = min(int(line['height']), stat_dict['min_height'])

        if 'weight_sum' in stat_dict:
            stat_dict['weight_sum'] += int(line['weight'])
        else:
            stat_dict['weight_sum'] = 0
            stat_dict['weight_sum'] += int(line['weight'])
        
        if line['sex'] == 'Male':
            men_count += 1
        else:
            women_count += 1
        waistline_list.append(float(line['waistline']))
        serum_creatinine_sum += float(line['serum_creatinine'])

        counter += 1


    stat_dict['serum_creatinine_avg'] = serum_creatinine_sum / float(counter)
    stat_dict['percent_of_men'] = str(men_count / counter * 100) + '%'
    stat_dict['percent_of_women'] = str(women_count / counter * 100) + '%'

    std_deviation = np.std(waistline_list)
    stat_dict['std_deviation_waistline'] = std_deviation


with open("files/5/stat_dict.json", "w") as r_json:
    r_json.write(json.dumps(stat_dict))

with open("files/5/stat_dict.pkl", "wb") as f:
    f.write(pickle.dumps(stat_dict))

with open('files/5/stat_dict.csv', 'w', encoding="utf-8", newline='') as result:
    writer = csv.writer(result, delimiter=',', quotechar='*', quoting=csv.QUOTE_MINIMAL)

    # Записываем заголовки (названия колонок)
    writer.writerow(stat_dict.keys())
    # Записываем данные
    writer.writerow(stat_dict.values())

with open("files/5/stat_dict.msgpack", "wb") as r_msgpack:
    r_msgpack.write(msgpack.dumps(stat_dict))

print(f"csv        = {os.path.getsize('files/5/stat_dict.csv')}")
print(f"json       = {os.path.getsize('files/5/stat_dict.json')}")
print(f"msgpack    = {os.path.getsize('files/5/stat_dict.msgpack')}")
print(f"pickle     = {os.path.getsize('files/5/stat_dict.pkl')}")


    
