import pandas as pd
import numpy as np
# import matplotlib as plt
import os
from tqdm import tqdm
from collections import defaultdict
import shutil, sys
import datetime
import pickle
dest_path = "..\my_dataset"
walking_data = []
onTable_data = []
onLaptop_data = []
all_data = defaultdict(None)
all_data['user_1'] = defaultdict(list)
all_data['user_2'] = defaultdict(list)
all_data['user_3'] = defaultdict(list)
for root, dirs, files in os.walk("..\Raw_data"):
    # print(root) 
    # exit()

    
    for name in files:
        
        print(name)
        print(dirs)
        print(root)
        motherf, raw_data_p, user, label, instance_id = root.split('\\')    # get info from directory name
        instance_id , year, month , date, hours,minutes,seconds = instance_id.split('_') # get info from file name
        instance_data = pd.read_csv(os.path.join(root,name) )
        user = 'user_1' if 'andreas' in user else 'user_2' if 'soti' in user else 'user_3'  # get which user the data belongs to
        
        instance_cols = list(instance_data.columns) 
        # print(instance_cols)
        np_data = instance_data.to_numpy() # numpy version  of the data
        # print(np_data.shape)
        if np_data.shape[0] == 0:
            continue     #skip if no data


        format_str = '%Y/%m/%d %H:%M:%S:%f' # The format
        date_foo = str(year) + '/'+str(month) + '/'+str(date) + ' '+str(hours) + ':'+str(minutes) +':' +str(seconds) +':0000'
        # print(date_foo)
        start_time = datetime.datetime.strptime(date_foo, format_str) # start time of the measurement
        minn = np_data[:,0].min()    #earliest time
        maxx = np_data[:,0].max()   #oldest time
        # print('here')
        # print(np_data[0,0])
        # print(np_data[-1,0])
        print(minn,maxx)
        if minn < 0 :
            np_data[:,0] = abs(abs(np_data[:,0]) - abs(minn) -abs(maxx))     #handle negative times

        minn = np_data[:,0].min()
        maxx = np_data[:,0].max()
        # print(np_data)
        print(minn,maxx)

        for row in range(len(np_data)):#change the timestamp with the correct format of timestamp
            np_data[row][0] = datetime.datetime.timestamp(start_time+datetime.timedelta(milliseconds=np_data[row][0])) *1000000000   


        all_data[user][name[:-4].lower()].extend(np_data)    #extend user sensor list with the measurement data

pickle.dump(all_data,open('../temp_data/temp_data.pkl','wb')) #save te8mp data into pickle to be used from create_data_csv.py
