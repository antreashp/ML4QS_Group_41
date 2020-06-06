import pandas as pd
import numpy as np
# import matplotlib as plt
import os
from tqdm import tqdm
from collections import defaultdict
import shutil, sys

import pickle


all_data = pickle.load(open('..\\temp_data\\temp_data.pkl','rb'))
column_names = {
                'accelerometer':['sensor_type','device_type','timestamps','x','y','z'],
                'gyroscope':['sensor_type','device_type','timestamps','x','y','z'],
                'magnetometer':['sensor_type','device_type','timestamps','x','y','z'],
                'pressure':['sensor_type','device_type','timestamps','pressure'],
                'proximity':['sensor_type','device_type','timestamps','distance'],
                'location':['sensor_type','device_type','timestamps','latitude','longitude','speed'],
                'light':['sensor_type','device_type','timestamps','lux']  ,
                'linear acceleration':['sensor_type','device_type','timestamps','x','y','z'],  
                         
} 






csv_dict = defaultdict(None)
csv_dict['user_1'] = defaultdict(list)
csv_dict['user_2'] = defaultdict(list)
csv_dict['user_3'] = defaultdict(list)
for user in all_data.keys():
    dest_path = '../my_dataset/'+user

    if not os.path.exists(dest_path):
        os.mkdir(dest_path)
    for sensor_type in all_data[user].keys():
        columns = column_names[sensor_type]
        np_data = np.array(all_data[user][sensor_type], dtype=object)
        print('gathering data from...',user,sensor_type)

        for row in  range(1,np_data.shape[0]):
            
            if (sensor_type == 'accelerometer' or sensor_type == 'magnetometer' or sensor_type == 'location' or sensor_type == 'linear acceleration' or sensor_type == 'gyroscope' ):
                foo = [str(np_data[row][1]),str(np_data[row][2]),str(np_data[row][3])]
            else:
                foo = [str(np_data[row][1])]

            csv_dict[user][sensor_type].append([sensor_type,'phone',str(np_data[row][0])]+foo)
        print(np.asarray(csv_dict[user][sensor_type]).shape)
        df = pd.DataFrame(data=csv_dict[user][sensor_type], columns=columns) 
        df.to_csv(dest_path+'/'+sensor_type+'_phone.csv', index=False)
        