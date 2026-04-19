import re

import pandas as pd
from glob import glob

files = glob("./data/raw/MetaMotion/*.csv")
def read_date_from_file(file):
    acc_df = pd.DataFrame()
    gyro_df = pd.DataFrame()

    acc_set = 1
    gyro_set = 1

    for f in files:
        participant = f.split('-')[0].replace(data_path, '')
        label = f.split('-')[1]
        category = f.split('-')[2].rsplit("3")[0]
        category = re.sub(r"\d+","",category.split("_")[0])

        df = pd.read_csv(f)
        
        df['participant'] = participant
        df['label'] = label
        df['category'] = category

        if "Accelerometer" in f:
            df['set']=acc_set
            acc_set += 1
            acc_df = pd.concat([acc_df, df], ignore_index=True)
        elif "Gyroscope" in f:
            df['set']=gyro_set
            gyro_set += 1
            gyro_df = pd.concat([gyro_df, df], ignore_index=True)

    acc_df.index=pd.to_datetime(acc_df['epoch (ms)'], unit='ms')
    gyro_df.index=pd.to_datetime(gyro_df['epoch (ms)'], unit='ms')

    acc_df.drop(columns=['epoch (ms)','time (01:00)','elapsed (s)'], inplace=True)
    gyro_df.drop(columns=['epoch (ms)','time (01:00)','elapsed (s)'], inplace=True)

    return acc_df, gyro_df

acc_df, gyro_df = read_date_from_file(files)

