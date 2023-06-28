import pandas as pd
import os
import glob

def data_prep(input_df):
    #input_df = pd.read_csv("data/preprocessed/v2/Locations_00_prep_v2.csv", index_col=0)
    data = input_df
    #data = data.loc[data["no_movement_15min"].isin([1])]
    data["idx"] = range(len(data))
    data["idx"] = data["idx"].astype(int)
    data = data[["idx", "x", "y", "z", "hour", "minute","day", "day_new", "week_num", "no_movement_5min",  "no_movement_15min"]]


    #x_min = data["x"].min()
    #y_min = data["y"].min()
    #z_min = data["z"].min()


    # min abs idee doch nicht so gut!!!

    data["x"] = data["x"] + 55
    data["y"] = data["y"] + 10
    data["z"] = data["z"] + 40

    df = data[["x", "y", "z"]]

    # Check if any NaN values exist in the DataFrame
    nan_values = data.isna()
    has_nan_values = nan_values.any().any()
    print("data has NaN values:", has_nan_values)

    df_list = []

    for label in df:

        ts = df[label]
        print(label)
        #data_tmp = data.loc[data[""]]


        tmp = pd.DataFrame({'coordinate': ts})
        tmp['coordinate_var'] = label
        tmp['hour'] = data['hour']
        tmp['minute'] = data['minute']
        tmp['day'] = data['day']
        tmp['day_new'] = data['day_new']
        tmp['week_num'] = data['week_num']
        tmp['idx'] = range(len(ts))
        tmp['idx'] = tmp['idx'].astype('int')
        tmp["no_movement_5min"] = data["no_movement_5min"]
        tmp["no_movement_15min"] = data["no_movement_15min"]


        #stack all time series vertically
        df_list.append(tmp)
        #df_list.append(ts["id"])



    time_df = pd.concat(df_list).reset_index(drop=True)

    # Check if any NaN values exist in the DataFrame
    nan_values = data.isna()
    has_nan_values = nan_values.any().any()
    print("time_df has NaN values:", has_nan_values)


    # Replace the numbers with day names
    day_mapping = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri'}
    time_df['day_new'] = time_df['day_new'].replace(day_mapping)

    output_df = time_df

    return output_df



folder_path = 'data/preprocessed/v2/'

# Get a list of all the CSV files in the folder
csv_files = glob.glob(os.path.join(folder_path, '*.csv'))
print(csv_files)
for i in csv_files:
    print("test")
    filename = os.path.splitext(os.path.basename(i))[0]
    data = pd.read_csv("data/preprocessed/v2/" + filename + ".csv")
    data_new = data_prep(data)
    data_new.to_csv('data/preprocessed/TFT_DataSets/' + filename + "_tft.csv", index=False)    
    print(filename)

