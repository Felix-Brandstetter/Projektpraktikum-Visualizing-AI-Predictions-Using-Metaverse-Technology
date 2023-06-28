import os 
import lightning.pytorch as pl
import pandas as pd
from teamblue.src.CreateDL import *
from teamblue.src.CreatePersonPredictions import CreatePersonPredictions
from teamblue.src.GetDataPaths import getDataPaths
from teamblue.src.GetModelPaths import getModelPaths
from teamblue.src.ResultSummary import resultsSummary

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
    
    person_df_extended.to_csv("teamblue/data/results/extended/"+name+"_extended.csv", index=False)
    person_df_vr_pred.to_csv("teamblue/data/results/person_df_ar_pred/"+name+"_ar_pred.csv", index=False)
    person_df_vr_actual.to_csv("teamblue/data/results/person_df_ar_actual/"+name+"_ar_actual.csv", index=False)




##################################
###   Create Metrics Summary   ### 
##################################
summary_df = pd.DataFrame()
for i in range(len(data_list)):
    i = 14
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

    filename = data_list[i].split('/')[-1]
    name, extension = os.path.splitext(filename)
    name = name.split('_prep')[0]
    summary_dict = resultsSummary(name, "/media/testit/Data/Visual_3D_Position/visual_3d_git_project/teamblue/models/Locations_16_prep_v2_tft/lightning_logs_tft/lightning_logs/version_1/checkpoints/epoch=119-step=1200.ckpt", val_dataloader)
    summary_df = pd.concat([summary_df, pd.DataFrame([summary_dict])], ignore_index=True)
    summary_df

summary_df.to_csv("teamblue/data/results/summary_v3.csv", index=False)
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