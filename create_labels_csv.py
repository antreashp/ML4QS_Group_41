import pandas as pd
import numpy as np
# import matplotlib as plt
import os
from tqdm import tqdm
from collections import defaultdict
import shutil, sys
import datetime
import pickle
csv_dict = defaultdict(None)
csv_dict['user_1'] = []
csv_dict['user_2'] = []
csv_dict['user_3'] = []
label_columns_interval = ['sensor_type','device_type','label','label_start','label_start_datetime','label_end','label_end_datetime']
label_columns_point = ['sensor_type','device_type','label','label_start','label_start_datetime','label_end','label_end_datetime']
for root, dirs, files in os.walk("..\Raw_data"):
    for name in files:
            
        motherf, raw_data_p, user, label, instance_id = root.split('\\') # get info from directory name
        user = 'user_1' if 'andreas' in user else 'user_2' if 'soti' in user else 'user_3'   # get which user the data belongs to
        
        instance_data = pd.read_csv(os.path.join(root,name) ) #get the data
        instance_id , year, month , date, hours,minutes,seconds = instance_id.split('_') # get info from file name
        
        if instance_data.to_numpy().shape[0] == 0:
            continue    #skip if no data
        minn = instance_data['Time (s)'].min()
        maxx = instance_data['Time (s)'].max()
        format_str = '%Y/%m/%d %H:%M:%S.%f' # The format
        # print(datetime_obj.date())
        date_foo = str(year) + '/'+str(month) + '/'+str(date) + ' '+str(hours) + ':'+str(minutes) +':' +str(seconds)+'.00'
        # print(date_foo)
        print(maxx,minn)
        np_data = instance_data.to_numpy()
        # print(np_data[0,0])
        if minn < 0 :
            np_data[:,0] = abs(abs(np_data[:,0]) - abs(minn) -abs(maxx)) #fix max min timestamps

        minn = np_data[:,0].min()
        maxx = np_data[:,0].max()
        print(maxx,minn)
        # exit()
        start_time = datetime.datetime.strptime(date_foo, format_str)
        end_time = start_time + datetime.timedelta(seconds=maxx -minn)
        if minn == maxx :
            sensor_type  = 'point_label'
        else:
            sensor_type = 'interval_label'
        s_time = datetime.datetime.timestamp(start_time)*1000000000
        e_time = datetime.datetime.timestamp(end_time)*1000000000
        
        #add labels with their starting and ending time for each user
        csv_dict[user].append([sensor_type,'smartphone',label,s_time,str(start_time),e_time,str(end_time)])
        
for user in csv_dict.keys():   #save label files for each user
    dest_path = '../my_dataset/'+user
    df = pd.DataFrame(csv_dict[user],columns = label_columns_interval )
    df.to_csv(dest_path+'/'+'labels.csv', index=False) 