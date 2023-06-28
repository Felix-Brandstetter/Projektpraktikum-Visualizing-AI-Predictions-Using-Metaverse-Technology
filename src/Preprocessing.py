import pandas as pd
from datetime import datetime, timedelta

def Preprocess(df):
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
            if (duration >= 5):
                df.loc[i, "no_movement_5min"] = 1
            else:
                df.loc[i, "no_movement_5min"] = 0


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
        day_df = df.loc[df["day"] == day]
        start_time = min(day_df["time_new"])
        end_time = max(day_df["time_new"])
        l.append(datetime_df[(datetime_df['datetime'].dt.time >= start_time)
            & (datetime_df['datetime'].dt.time <= end_time)])

    df_date = pd.concat(l)
    df_date = df_date["datetime"]
    datetime_df['date'] = datetime_df['datetime'].dt.date
    unique_dates = datetime_df['date'].unique()
    new_df = df.merge(df_date, on="datetime", how="right")
    new_df = new_df.fillna(method="ffill")

    new_df["y_binary"] = ""
    new_df.loc[(new_df["y"] >= -1) & (new_df["y"] <= 0), "y_binary"] = 1
    new_df.loc[(new_df["y"] >= -10) & (new_df["y"] <= -6), "y_binary"] = 0
    new_df = new_df.loc[new_df["y_binary"].isin([0, 1])]

    new_df = new_df[["day", "time", "time_new", "day_new", "week_num", "datetime", "x", "y", "z", "y_binary", "no_movement_5min"]]

    return new_df