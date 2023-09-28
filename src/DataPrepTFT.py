import pandas as pd
import os
import glob

def data_prep(input_df):

    """
    Erstellen des TFT Datasets

    Args:
        input_df der jeweiligen Person

    Returns:
        output_df: angepasstes Dataset
    """
    
    data = input_df
    data["idx"] = range(len(data))
    data["idx"] = data["idx"].astype(int)
    data = data[["idx", "x", "y", "z", "hour", "minute","day", "day_new", "week_num", "no_movement_5min",  "no_movement_15min"]]


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


###########
###
### Um zu testen wie die Ergebnisse, wenn das Stockwerk als binär angesehen wird.
### Y auf 0 bzw 1 setzen 
###
###########

folder_path = 'data/preprocessed/TFT_DataSets/'

# Get a list of all the CSV files in the folder
csv_files = glob.glob(os.path.join(folder_path, '*.csv'))
print(csv_files)
for i in csv_files:
    filename = os.path.splitext(os.path.basename(i))[0]
    data = pd.read_csv('data/preprocessed/TFT_DataSets/' + filename + ".csv")
    data.loc[(data["coordinate_var"] == "y") & (data["coordinate"] >= 9) & (data["coordinate"] <= 12), "coordinate"] = 50
    data.loc[(data["coordinate_var"] == "y") & (data["coordinate"] >= -1) & (data["coordinate"] < 9), "coordinate"] = 40
    data.loc[(data["coordinate_var"] == "y")].head()
    data.to_csv('data/preprocessed/TFT_DataSets_v2/' + filename + "_tft_v2.csv", index=False)    
    print(filename)


    data["y"] = data["y"] + 10
    df.loc[(df["y"] >= -1) & (df["y"] <= 3), "y_binary"] = 1
    df.loc[(df["y"] >= -10) & (df["y"] < -1), "y_binary"] = 0


test = pd.read_csv('data/preprocessed/TFT_DataSets_v2/' + filename + "_tft_v2.csv")
test = test.loc[(data["coordinate_var"] == "y")]
test["coordinate"].value_counts()

folder_path = 'data/preprocessed/v2/'

# Get a list of all the CSV files in the folder
csv_files = glob.glob(os.path.join(folder_path, '*.csv'))
print(csv_files)
for i in csv_files:
    filename = os.path.splitext(os.path.basename(i))[0]
    data = pd.read_csv("data/preprocessed/v2/" + filename + ".csv", index_col=0)
    data.head()
    data.loc[(data["y"] >= -10) & (data["y"] <= -1), "y_binary"] = 0
    data.head()
    data_new = data_prep(data)
    data_new.to_csv('data/preprocessed/TFT_DataSets/' + filename + "_tft.csv", index=False)    
    print(filename)

