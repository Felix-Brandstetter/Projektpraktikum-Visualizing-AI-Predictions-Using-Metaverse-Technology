import os
import glob
import pandas as pd
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt

Locations_01_ar_actual = pd.read_csv("teamblue/data/results/person_df_ar_actual/Locations_01_ar_actual.csv")
Locations_01_ar_actual.head()

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
pivoted_df.to_csv("teamblue/data/preprocessed/Raumdaten/Person_RaumPivot/" + "aa_test" + ".csv", index=True)


folder_path = 'teamblue/data/results/person_df_ar_actual/'

# Get a list of all the CSV files in the folder
csv_files = glob.glob(os.path.join(folder_path, '*.csv'))
csv_files
for i in csv_files:
    filename = os.path.splitext(os.path.basename(i))[0]
    print(filename)
    data = pd.read_csv("teamblue/data/results/person_df_ar_actual/" + filename + ".csv")

    minute_range = range(0, 3001, 1)

    # Create a DataFrame with the minute_idx column
    timeline_df = pd.DataFrame({'minute_idx': minute_range})

    merge_df = pd.merge(timeline_df, data, on='minute_idx', how='outer')
    merge_df = merge_df.fillna(method='ffill')

    pivot_test = merge_df[["minute_idx", "room_actual"]]
    pivot_test
    pivot_test = pivot_test.dropna()
    pivoted_df = pivot_test.pivot(index='minute_idx', columns='room_actual', values='room_actual').notna().astype(int)
    pivoted_df = pivoted_df.fillna(0)
    pivoted_df.head()
    pivoted_df.to_csv("teamblue/data/preprocessed/Raumdaten/Person_RaumPivot/" + filename + ".csv")
    print(filename)





rooms = pd.read_csv("teamblue/data/preprocessed/Raumkoordinaten/raumkoordinaten_prep_unity.csv", index_col=0)
room_list = rooms["room"].to_list()
room_list

folder_path = 'teamblue/data/preprocessed/Raumdaten/Person_RaumPivot/'

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
        data = pd.read_csv('teamblue/data/preprocessed/Raumdaten/Person_RaumPivot/' + filename + ".csv")
      
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
        room_df.to_csv("teamblue/data/preprocessed/Raumdaten/RaumDF/actual/" + room_name + ".csv", index=False)


room_df = pd.read_csv("teamblue/data/preprocessed/Raumdaten/RaumDF/5C-02.1.csv", index_col=0)
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
    


####################################################################################################################################################
####  Testing  ####
####################################################################################################################################################




######
# Add the complete time index then pivot the dataframe -> i get the rooms with the time intervall when this person is there
# maybe add all rooms to it
# !!! maybe create a df with all rooms as columns and the time idx and join the pivot's person dfs





pivot_df = Locations_01_ar_actual.pivot(index='minute_idx', columns='room_actual')
pivot_df.head()









merged_df = pd.merge(Locations_00_ar_actual, Locations_01_ar_actual, on='minute_idx', how='outer')
sorted_df = merged_df.sort_values('minute_idx')
sorted_df.head()


folder_path = 'teamblue/data/results/person_df_ar_actual/'

suffix_l = 0
suffix_r = 1
# Get a list of all the CSV files in the folder
csv_files = glob.glob(os.path.join(folder_path, '*.csv'))
print(csv_files)
csv_files.pop(0)
print(csv_files)
merged_df = pd.read_csv("teamblue/data/results/person_df_ar_actual/Locations_00_ar_actual.csv")
for i in csv_files:
    suffix_l = suffix_l +1
    suffix_r = suffix_r +1
    filename = os.path.splitext(os.path.basename(i))[0]
    data = pd.read_csv("teamblue/data/results/person_df_ar_actual/" + filename + ".csv")
    merged_df = pd.merge(merged_df, data, on='minute_idx', how='outer', suffixes=(str(suffix_l), str(suffix_r)))
    print(filename)
sorted_df = merged_df.sort_values('minute_idx')
sorted_df.tail()


minute_range = range(0, 3001, 1)

# Create a DataFrame with the minute_idx column
timeline_df = pd.DataFrame({'minute_idx': minute_range})

timeline_df.head()


filtered_columns = [col for col in sorted_df.columns if any(keyword in col for keyword in ['room', 'minute_idx'])]
filtered_df = sorted_df[filtered_columns]
filtered_df.head(5)


final_df = pd.merge(timeline_df, filtered_df, on='minute_idx', how='outer')

final_df_filled = final_df.fillna(method='ffill')
final_df_filled = final_df_filled.rename(columns={'room_actual': 'room_actual0'})
final_df_filled = final_df_filled.sort_index(axis=1)
final_df_filled.head()





final_df_columns_list = list(final_df.columns)
final_df_columns_list

final_df["minute_idx"]




dummy_heizen =  pd.read_csv("teamblue/data/preprocessed/Dummy_Heizstrategie.csv", index_col=0)
dummy_heizen = dummy_heizen.loc[dummy_heizen["Tag"] <8]

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

dummy_heizen["hour"] = dummy_heizen["Zeit"].astype(int)
dummy_heizen["minute"] = (60 * (dummy_heizen["Zeit"] - dummy_heizen["hour"])).astype(int)

dummy_heizen["minute_idx"] = ""
dummy_heizen = dummy_heizen.reset_index(drop=True)
dummy_heizen.head(50)
for i in range(len(dummy_heizen)):
        dummy_heizen["minute_idx"][i] = getMinuteOfWeek(dummy_heizen["Tag"][i], dummy_heizen["hour"][i], dummy_heizen["minute"][i])

dummy_heizen.head(50)
temperatures = np.random.uniform(low=18, high=23, size=len(dummy_heizen))

# Add the dummy temperature column to the DataFrame
dummy_heizen['Temp'] = temperatures
min_temperature = 18.0
max_temperature = 23.0

normalized_temperatures = (dummy_heizen['Temp'] - min_temperature) / (max_temperature - min_temperature)
cmap = cm.get_cmap('coolwarm')
rgb_values = normalized_temperatures.apply(lambda x: cmap(x)[:3])
dummy_heizen['rgb_value'] = rgb_values
dummy_heizen = dummy_heizen[["minute_idx", "Raum", "Anzahl", "Temp", "rgb_value"]]
dummy_heizen['rgb_value'] = dummy_heizen['rgb_value'].apply(lambda rgb: tuple(int(val * 255) for val in rgb))
dummy_heizen.head()

dummy_heizen = dummy_heizen.drop_duplicates(subset=['minute_idx', 'Raum'])

dummy_heizen.to_csv("teamblue/data/preprocessed/dummy_heizen_v2.csv", index=False)

# Extract the first 5 values
subset = dummy_heizen.head(5)

# Create a bar plot
fig, ax = plt.subplots()
ax.bar(range(len(subset)), subset['temp'], color=subset['rgb_value'])

# Set the x-axis tick labels
ax.set_xticks(range(len(subset)))
ax.set_xticklabels(range(1, len(subset) + 1))

# Set the axis labels
ax.set_xlabel('Index')
ax.set_ylabel('Temperature')

# Show the plot
plt.show()
