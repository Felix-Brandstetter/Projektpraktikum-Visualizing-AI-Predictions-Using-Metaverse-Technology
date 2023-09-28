import os
import glob
import pandas as pd
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt

##########################################################
###   Mit Hilfe der Vorhersage Ergebnisse der Personen ###
###   wird für jeden Raum ein Belegungsplan erstellt   ###
##########################################################


Locations_01_ar_actual = pd.read_csv("data/results/person_df_ar_actual/Locations_00_ar_actual.csv")


minute_range = range(0, 3001, 1)

# Create a DataFrame with the minute_idx column
timeline_df = pd.DataFrame({'minute_idx': minute_range})

merge_df = pd.merge(timeline_df, Locations_01_ar_actual, on='minute_idx', how='outer')
merge_df = merge_df.fillna(method='ffill')
merge_df.head()

pivot_test = merge_df[["minute_idx", "room_actual"]]
pivot_test
pivot_test = pivot_test.dropna()
pivoted_df = pivot_test.pivot(index='minute_idx', columns='room_actual', values='room_actual').notna().astype(int)
pivoted_df = pivoted_df.fillna(0)
pivoted_df.head(5)


folder_path = "data/results/person_df_pred_v2/"

# Get a list of all the CSV files in the folder
csv_files = glob.glob(os.path.join(folder_path, '*.csv'))
csv_files
for i in csv_files:
    filename = os.path.splitext(os.path.basename(i))[0]
    print(filename)
    data = pd.read_csv("data/results/person_df_pred_v2/" + filename + ".csv")

    minute_range = range(0, 3001, 1)

    # Create a DataFrame with the minute_idx column
    timeline_df = pd.DataFrame({'minute_idx': minute_range})

    merge_df = pd.merge(timeline_df, data, on='minute_idx', how='outer')
    merge_df = merge_df.fillna(method='ffill')

    pivot_test = merge_df[["minute_idx", "room_prediction"]]
    pivot_test
    pivot_test = pivot_test.dropna()
    pivoted_df = pivot_test.pivot(index='minute_idx', columns='room_prediction', values='room_prediction').notna().astype(int)
    pivoted_df = pivoted_df.fillna(0)
    pivoted_df.head()
    pivoted_df.to_csv("data/results/Raumdaten/Person_RaumPivot/prediction/v1/" + filename + ".csv")
    print(filename)





rooms = pd.read_csv("data/preprocessed/Raumkoordinaten/raumkoordinaten_prep_unity.csv", index_col=0)
room_list = rooms["room"].to_list()
room_list

folder_path = ("data/results/Raumdaten/Person_RaumPivot/prediction/v1/")

# Get a list of all the CSV files in the folder
csv_files = glob.glob(os.path.join(folder_path, '*.csv'))
csv_files

for s in range(len(room_list)):
    minute_range = range(0, 3001, 1)
    # Create a DataFrame with the minute_idx column
    room_df = pd.DataFrame({'minute_idx': minute_range})
    #i = 5
    room_name = room_list[s]
    for i in csv_files:
        filename = os.path.splitext(os.path.basename(i))[0]
    
        #filename = "Locations_01_ar_actual"
        data = pd.read_csv("data/results/Raumdaten/Person_RaumPivot/prediction/v1/" + filename + ".csv")
      
        try:
            data = data.rename(columns={room_name: filename})
            data = data[["minute_idx", filename]]
            room_df = pd.merge(room_df, data, on='minute_idx', how='left')
            
        except KeyError:
            print(f"Key '{room_name}' not found. Continuing...")
            continue
    if room_df.shape[1] > 1:
        print("DataFrame is not empty")
        room_df['PersonenAnzahl'] = room_df.iloc[:, 1:].sum(axis=1)
        #room_df = room_df.loc[room_df["PersonenAnzahl"] > 0]
        room_df = room_df[["minute_idx", "PersonenAnzahl"]]
        room_df = room_df[room_df['PersonenAnzahl'].ne(room_df['PersonenAnzahl'].shift())]
        temperatures = np.random.uniform(low=18, high=23, size=len(room_df))
        # Add the dummy temperature column to the DataFrame
        room_df['temp'] = temperatures
        min_temperature = 18.0
        max_temperature = 23.0

        normalized_temperatures = (room_df['temp'] - min_temperature) / (max_temperature - min_temperature)
        cmap = cm.get_cmap('coolwarm')
        rgb_values = normalized_temperatures.apply(lambda x: cmap(x)[:3])
        room_df['rgb_value'] = rgb_values
        room_df['rgb_value'] = room_df['rgb_value'].apply(lambda rgb: tuple(int(val * 255) for val in rgb))
        room_df = room_df.drop(0)
        room_df = room_df.reset_index(drop=True)
        room_df.to_csv("data/results/Raumdaten/RaumDF/prediction_v1/" + room_name + ".csv", index=False)


room_df = pd.read_csv("data/preprocessed/Raumdaten/RaumDF/5C-02.1.csv", index_col=0)
room_df['PersonenAnzahl'] = room_df.iloc[:, 1:].sum(axis=1)
room_df = room_df.loc[room_df["PersonenAnzahl"] > 0]
room_df = room_df[["minute_idx", "PersonenAnzahl"]]
room_df.head()
    



####################################
####  Add 0 Minutes to Room DF  ####
####################################

folder_path = 'data/preprocessed/Raumdaten/RaumDF/actual'

# Get a list of all the CSV files in the folder
csv_files = glob.glob(os.path.join(folder_path, '*.csv'))
print(csv_files)
for i in csv_files:
    filename = os.path.splitext(os.path.basename(i))[0]
    data = pd.read_csv('data/preprocessed/Raumdaten/RaumDF/actual/' + filename + ".csv")
    new_row = {'minute_idx': [0], 'PersonenAnzahl': [0], 'temp': [18], 'rgb_value': [(221, 96, 76)]}
    new_row_df = pd.DataFrame(new_row, index=[0])
    data = pd.concat([new_row_df, data]).reset_index(drop=True)
    data.to_csv('data/preprocessed/Raumdaten/RaumDF/actual_v1/' + filename + ".csv")
    




def getMinuteOfWeek(day, hour, minute):
    print("Getting minutes")
    my_dictionary = {1: 0, 2: 1, 3: 2, 6: 3, 7:4}
    if day in my_dictionary:
        factor = my_dictionary[day]
    else:
        print("Wrong Week Days")

    minute_output = 600 * factor
    minute_output = minute_output + (hour - 8) * 60 + minute
    return minute_output


