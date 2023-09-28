import os 
import lightning.pytorch as pl
import pandas as pd
import glob
from src.CreateDL import *
from src.CreatePersonPredictions import CreatePersonPredictions
from src.GetDataPaths import getDataPaths
from src.GetModelPaths import getModelPaths
from src.ResultSummary import resultsSummary
from src.CreateRoomDF import getMinuteOfWeek

data_list = getDataPaths()
model_list = getModelPaths()
model_list


#############################
###   Create Person Dfs   ### 
#############################

for i in range(len(data_list)):
    #i = 17
    df_path = data_list[i]
    print(df_path)
    model_path = model_list[i]
    print(model_path)
    #person = person
    input_df = pd.read_csv(df_path)
    input_df = input_df.loc[input_df["week_num"] < 44]
    input_df = input_df.loc[input_df["no_movement_15min"].isin([1])]
    input_df["idx"] = range(len(input_df))
    input_df.tail(20)
    pl.seed_everything(42)

    week_43_length =  input_df.loc[input_df["week_num"] == 43]
    week_43_length =  week_43_length.loc[week_43_length["coordinate_var"] == "x"]
    week_43_length = len(week_43_length)
    week_43_length
    batch_size = 128 
    num_workers = 4
    # Evaluate: Set max_prediction_length to len(week_num) or more
    max_prediction_length = week_43_length
    max_encoder_length = 600
    input_df = input_df.dropna()
    training, train_dataloader, val_dataloader = CreateDataLoader(input_df, batch_size, num_workers,  max_prediction_length, max_encoder_length)

    best_model_path = model_path
    #results = CreatePersonPredictions(best_model_path, val_dataloader, input_df)
    person_df_extended, person_df_vr_pred, person_df_vr_actual = CreatePersonPredictions(best_model_path, val_dataloader, input_df)

    filename = df_path.split('/')[-1]
    name, extension = os.path.splitext(filename)
    name = name.split('_prep')[0]
    
    person_df_extended.to_csv("data/results/extended/"+name+"_extended.csv", index=False)
    person_df_vr_pred.to_csv("data/results/person_df_ar_pred/"+name+"_ar_pred.csv", index=False)
    person_df_vr_actual.to_csv("data/results/person_df_ar_actual/"+name+"_ar_actual.csv", index=False)



#############################################################
###   Create Final Person DF with Start and Ziel Column   ### 
#############################################################

folder_path = 'data/results/person_df_actual_v2/'

csv_files = glob.glob(os.path.join(folder_path, '*.csv'))
print(csv_files)
for i in csv_files:
    filename = os.path.splitext(os.path.basename(i))[0]
    data = pd.read_csv('data/results/person_df_actual_v2/' + filename + ".csv", index_col=0)
    data.head()
    output_df = data[["minute_idx", "room_actual"]]
    output_df['start'] = output_df['room_actual']
    output_df['ziel'] = output_df['start'].shift(-1)
    output_df["minute_idx"] = data["minute_idx"].shift(-1)
    output_df = output_df[["minute_idx", "start", 'ziel']]
    output_df = output_df.drop(output_df.index[-1])
    output_df.head()
    output_df.to_csv('data/results/person_df_actual_v2/' + filename + "_vr_format.csv")


# Add manually a Start and Endpoint for better Experience in AR
# Get from every Person the actual Start- and Endtime -> convert into minutes + add to final df with room = "Übergang"
def getMinuteOfWeek(day, hour, minute):
    my_dictionary = {215: 0, 216: 1, 217: 2, 218: 3, 219:4}
    if day in my_dictionary:
        factor = my_dictionary[day]
    else:
        print("Wrong Week Days")

    minute_output = 600 * factor
    minute_output = minute_output + (hour - 8) * 60 + minute
    return minute_output


folder_path = 'data/preprocessed/v2/'

orginal_csv_files = glob.glob(os.path.join(folder_path, '*.csv'))
print(orginal_csv_files)
for i in orginal_csv_files:
    filename = os.path.splitext(os.path.basename(i))[0]
    data = pd.read_csv('data/preprocessed/v2/' + filename + ".csv", index_col=0)
    data = data.loc[data["week_num"] == 43]
    data.head()

    df = pd.read_csv("data/results/person_df_ar_pred/"+filename[:-8]+"_ar_pred.csv")
    df.head(50)
    if df.isnull().values.any():
        df.fillna(method='ffill', inplace=True)
    for i in data["day"].unique():
        
        df_help = data.loc[data["day"] == i]
        empty_df = df_help.loc[df_help["no_movement_15min"] == 1]
        
        if empty_df.empty:
            print("empty")
            continue
        print(i)
        df_help = df_help.sort_values("datetime")

        first_row = df_help.iloc[0]
        start_time = getMinuteOfWeek(first_row["day"], first_row["hour"], first_row["minute"])
        start_time
        last_row = df_help.iloc[-1]
        end_time = getMinuteOfWeek(last_row["day"], last_row["hour"], last_row["minute"])


        start_time_row = pd.Series([first_row["day"], first_row["hour"], first_row["minute"], "Übergang", start_time], index=['day', 'hour', 'minute', 'room_prediction', 'minute_idx'])
        df = pd.concat([df, pd.DataFrame([start_time_row])], ignore_index=True)

        end_time_row = pd.Series([last_row["day"], last_row["hour"], last_row["minute"], "Übergang", end_time], index=['day', 'hour', 'minute', 'room_prediction', 'minute_idx'])
        df = pd.concat([df, pd.DataFrame([end_time_row])], ignore_index=True)
        # Now add start_endtime to df
    df = df.sort_values("minute_idx")
    df = df.reset_index(drop=True)
    df.head(35)
    df.to_csv("data/results/person_df_pred_v2/"+filename[:-8]+"_pred_v2.csv")
      


##################################
###   Create Metrics Summary   ### 
##################################
summary_df = pd.DataFrame()
for i in range(len(data_list)):
    i = 17
    df_path = data_list[i]
    print(df_path)
    model_path = model_list[i]
    print(model_path)
    #person = person
    input_df = pd.read_csv(df_path)
    input_df = input_df.loc[input_df["week_num"] < 44]
    input_df = input_df.loc[input_df["no_movement_15min"].isin([1])]
    input_df["idx"] = range(len(input_df))
    input_df.tail(20)
    pl.seed_everything(42)

    week_43_length =  input_df.loc[input_df["week_num"] == 43]
    week_43_length =  week_43_length.loc[week_43_length["coordinate_var"] == "x"]
    week_43_length = len(week_43_length)
    week_43_length
    batch_size = 128 
    num_workers = 4
    # Evaluate: Set max_prediction_length to len(week_num) or more
    max_prediction_length = week_43_length
    max_encoder_length = 600
    input_df = input_df.dropna()
    input_df.min()
    training, train_dataloader, val_dataloader = CreateDataLoader(input_df, batch_size, num_workers,  max_prediction_length, max_encoder_length)

    filename = data_list[i].split('/')[-1]
    name, extension = os.path.splitext(filename)
    name = name.split('_prep')[0]
    model_path
    #test_path = 'models/Locations_16_prep_v2_tft/lightning_logs_tft/lightning_logs/version_1/checkpoints\\epoch=119-step=1200.ckpt'
    summary_dict = resultsSummary(name, model_path, val_dataloader)

    summary_dict
    summary_df = pd.concat([summary_df, pd.DataFrame([summary_dict])], ignore_index=True)
    summary_df

summary_df.to_csv("data/results/summary_16_20.csv", index=False)


#####################################
### Get manual prediction results ###
#####################################
#Select Person between 0 and 20
i = 17
df_path = data_list[i]
print(df_path)
model_path = model_list[i]
print(model_path)

#person = person
input_df = pd.read_csv(df_path)
input_df = input_df.loc[input_df["week_num"] < 44]
input_df = input_df.loc[input_df["no_movement_15min"].isin([1])]
input_df["idx"] = range(len(input_df))
input_df.tail()
pl.seed_everything(42)

week_43_length =  input_df.loc[input_df["week_num"] == 43]
week_43_length =  week_43_length.loc[week_43_length["coordinate_var"] == "x"]
week_43_length = len(week_43_length)
week_43_length
batch_size = 128 
num_workers = 4
# Evaluate: Set max_prediction_length to len(week_num) or more
max_prediction_length = week_43_length
max_encoder_length = 600

training, train_dataloader, val_dataloader = CreateDataLoader(input_df, batch_size, num_workers,  max_prediction_length, max_encoder_length)

best_model_path = model_path
#results = CreatePersonPredictions(best_model_path, val_dataloader, input_df)
person_df_extended, person_df_vr_pred, person_df_vr_actual = CreatePersonPredictions(best_model_path, val_dataloader, input_df)

filename = df_path.split('/')[-1]
name, extension = os.path.splitext(filename)
name = name.split('_prep')[0]

person_df_extended.to_csv("teamblue/data/results/extended/"+name+"_extended.csv", index=False)
person_df_vr_pred.to_csv("teamblue/data/results/person_df_ar_pred/"+name+"_ar_pred.csv", index=False)
person_df_vr_actual.to_csv("teamblue/data/results/person_df_ar_actual/"+name+"_ar_actual.csv", index=False)