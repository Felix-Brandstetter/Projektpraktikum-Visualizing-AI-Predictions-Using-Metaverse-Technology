import pandas as pd
from datetime import datetime, timedelta
import os
import glob

def Preprocess(df):
    """
    Funktion zum Preprocessing der raw Daten

    Args:
        raw Dataset  

    Returns:
        Transformierter DataFrame
    """
    
    df = pd.read_csv("data/raw/Locations_10.csv")
    len(df)
    df.columns = df.columns.str.lower()

    df["hour"] = df["time"].astype(int)
    df["minute"] = (60 * (df["time"] - df["hour"])).astype(int)
    df['minute'] = df['minute'].apply(lambda x: f"0{x}" if x < 10 else str(x))  # fill minutes with 0
    df['time_new'] = df['hour'].astype('str') + ':' + df['minute'].astype('str')

    df["day_new"] = df["day"] % 5

    day_old = 0
    week_number = 0

    for i in range(len(df)):
        df.loc[i, "day_new"] = df["day"][i] % 5

        day_new = df["day"][i] % 5
        if day_new < day_old:
            week_number += 1
        day_old = df["day"][i] % 5
        df.loc[df.index == i, 'week_num'] = week_number

        if(i < len(df)-1): 
            duration = (df["time"][i+1] - df["time"][i]) * 60
            if (duration >= 1):
                df.loc[i, "no_movement_1min"] = 1
            else:
                df.loc[i, "no_movement_1min"] = 0

        if(i < len(df)-1): 
            duration = (df["time"][i+1] - df["time"][i]) * 60
            if (duration >= 5):
                df.loc[i, "no_movement_5min"] = 1
            else:
                df.loc[i, "no_movement_5min"] = 0

        if(i < len(df)-1): 
            duration = (df["time"][i+1] - df["time"][i]) * 60
            if (duration >= 15):
                df.loc[i, "no_movement_15min"] = 1
            else:
                df.loc[i, "no_movement_15min"] = 0


    df['time_new'] = pd.to_datetime(df['time_new'], format='%H:%M').dt.time

    start_date = datetime(2023, 1, 1)
    df['datetime'] = df.apply(lambda row: datetime.combine(start_date + timedelta(days=row['day']), row['time_new']),
                            axis=1)

    start_time = min(df["datetime"])
    end_time = max(df["datetime"])
    datetime_column = pd.date_range(start=start_time, end=end_time, freq="1T")
    datetime_df = pd.DataFrame({"datetime": datetime_column})

    datetime_df['date'] = datetime_df['datetime'].dt.date
    unique_dates = datetime_df['date'].unique()

    l = []
    for day, dates in enumerate(unique_dates):
        try:
            day_df = df.loc[df["day"] == day]
            start_time = min(day_df["time_new"])
            end_time = max(day_df["time_new"])
        except ValueError:
            continue
        l.append(datetime_df[(datetime_df['datetime'].dt.time >= start_time)
            & (datetime_df['datetime'].dt.time <= end_time)])

    df_date = pd.concat(l)
    df_date = df_date["datetime"]
    datetime_df['date'] = datetime_df['datetime'].dt.date
    datetime_df.head()

    new_df = df.merge(datetime_df, on="datetime", how="left")
    len(new_df)
    new_df = new_df.fillna(method="ffill")


    

    new_df = new_df[["day", "time", "x", "y", "z", "hour", "minute", "time_new", "day_new", "week_num", "no_movement_1min", "no_movement_5min", "no_movement_15min", "datetime"]]  
    new_df.head()

    return new_df





folder_path = 'data/raw/'


# Get a list of all the CSV files in the folder
csv_files = glob.glob(os.path.join(folder_path, '*.csv'))
print(csv_files)
for i in csv_files:
    filename = os.path.splitext(os.path.basename(i))[0]
    data = pd.read_csv('data/raw/'+ filename + ".csv")
    data_new = Preprocess(data)
    data_new.to_csv('data/preprocessed/v3/' + filename + "_prep_v3.csv", index=False)    
    print(filename)
