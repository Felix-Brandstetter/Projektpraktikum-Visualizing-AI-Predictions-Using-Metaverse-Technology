<<<<<<< HEAD
import warnings
import matplotlib.pyplot as plt
import lightning.pytorch as pl
from lightning.pytorch.callbacks import EarlyStopping, LearningRateMonitor
from lightning.pytorch.loggers import TensorBoardLogger
import numpy as np
import pandas as pd
import torch
from pytorch_forecasting import TemporalFusionTransformer
from pytorch_forecasting.metrics import MAE, SMAPE, PoissonLoss, QuantileLoss
from pytorch_forecasting import Baseline
from src.CreateDL import *
from src.trainTFT import *
from src.BaselineModelTFT import *
from src.LearningRateFinder import *
from src.GetRoom import *
from src.CreatePersonPredictions import *
pl.seed_everything(42)

# Configuration TimeSeriesDataSet
person = "Locations_17_prep_v2_tft"
#person = person
input_df = pd.read_csv('data/preprocessed/TFT_DataSets/' + person + ".csv")
input_df = input_df.loc[input_df["no_movement_15min"].isin([1])]
input_df = input_df.loc[input_df["coordinate"] > 0]
input_df["idx"] = range(len(input_df))
week_43_length =  input_df.loc[input_df["week_num"] == 43]
week_43_length =  week_43_length.loc[week_43_length["coordinate_var"] == "x"]
week_43_length = len(week_43_length)
week_43_length

batch_size = 128 
num_workers = 6
# Evaluate: Set max_prediction_length to len(week_num) or more
max_prediction_length = week_43_length
max_encoder_length = 600

#Create Training-Set, Train-und Validationloader
training, train_dataloader, val_dataloader = CreateDataLoader(input_df, batch_size, num_workers,  max_prediction_length, max_encoder_length)


#Make Basline Predictions
baseline_predictions = Baseline().predict(val_dataloader)
PredictBaseline(baseline_predictions,val_dataloader) 


#Check for GPU/CPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)



# configure network and trainer
early_stop_callback = EarlyStopping(monitor="train_loss", min_delta=1e-4, patience=30, verbose=False, mode="min")
lr_logger = LearningRateMonitor()  # log the learning rate
logger = TensorBoardLogger("models/lightning_logs_tft/"+person)  # logging results to a tensorboard

trainer = pl.Trainer(
    max_epochs=120,
    accelerator="gpu",
    enable_model_summary=True,
    gradient_clip_val=0.1,
    limit_train_batches=10,  # coment in for training, running valiation every 10 batches
    # fast_dev_run=True,  # comment in to check that networkor dataset has no serious bugs
    callbacks=[lr_logger, early_stop_callback],
    logger=logger,
)

  

#LearningRate Finder

lr = OptimalLR(trainer, training, train_dataloader, val_dataloader); print(lr)

#Define model specifications
tft = TemporalFusionTransformer.from_dataset(
    training,
    learning_rate=0.1514,
    hidden_size=16,
    attention_head_size=2,
    dropout=0.1,
    hidden_continuous_size=8,
    loss=QuantileLoss(),
    log_interval=10,  # uncomment for learning rate finder and otherwise, e.g. to 10 for logging every 10 batches
    optimizer="Ranger",
    reduce_on_plateau_patience=4,
)
print(f"Number of parameters in network: {tft.size()/1e3:.1f}k")


# Traing tft model and return best_tft
tft = train(tft, trainer, train_dataloader, val_dataloader)



# Check model results and compute metrics
best_model_path = trainer.checkpoint_callback.best_model_path
best_tft = TemporalFusionTransformer.load_from_checkpoint(best_model_path)

predictions = best_tft.predict(val_dataloader, return_y=True, trainer_kwargs=dict(accelerator="gpu"))
MAE()(predictions.output, predictions.y)

import torch.nn.functional as F
actuals = torch.cat([y for x, (y, weight) in iter(val_dataloader)])
actuals

predictions = best_tft.predict(val_dataloader)
device = torch.device("cpu")
actuals = actuals.to(device)
predictions = predictions.to(device)

for i in range(3):
  var = ["x:", "y:", "z:"]
  print(var[i])
  # Calculate the Mean Absolute Error (MAE)
  mae = F.l1_loss(actuals[i], predictions[i])
  print("MAE:", mae.item())

  # Calculate the Mean Squared Error (MSE)
  mse = F.mse_loss(actuals[i], predictions[i])
  print("MSE:", mse.item())

  # Calculate the Root Mean Squared Error (RMSE)
  rmse = torch.sqrt(mse)
  print("RMSE:", rmse.item())






# Compute the room accuracy for the model
df_actuals = pd.DataFrame({'x': actuals[0], 'y': actuals[1], 'z': actuals[2]})
df_actuals.head(20)

df_actuals["x"] = df_actuals["x"] - 55
df_actuals["y"] = df_actuals["y"] - 10
df_actuals["z"] = df_actuals["z"] - 40
df_actuals = getRoom(df_actuals)

df_actuals = df_actuals.reset_index()
df_actuals["room"].value_counts()


df_predictions = pd.DataFrame({'x': predictions[0], 'y': predictions[1], 'z': predictions[2]})

df_predictions["x"] = df_predictions["x"] - 55
df_predictions["y"] = df_predictions["y"] - 10
df_predictions["z"] = df_predictions["z"] - 40
df_predictions = df_predictions.reset_index()

df_predictions = getRoom(df_predictions)

df_predictions["room"].value_counts()


# Accuracy
merged_df = pd.merge(df_actuals, df_predictions, on='index', suffixes=('_actual', '_prediction'))
accuracy = (merged_df['room_actual'] == merged_df['room_prediction']).mean()

print(f"Accuracy: {accuracy * 100:.2f}%")
=======
import warnings
import lightning.pytorch as pl
from lightning.pytorch.callbacks import EarlyStopping, LearningRateMonitor
from lightning.pytorch.loggers import TensorBoardLogger
import numpy as np
import pandas as pd
import torch
from pytorch_forecasting import TemporalFusionTransformer
from pytorch_forecasting.metrics import MAE, SMAPE, PoissonLoss, QuantileLoss
from pytorch_forecasting import Baseline
from teamblue.src.CreateDL import *
from teamblue.src.trainTFT import *
from teamblue.src.BaselineModelTFT import *
from teamblue.src.LearningRateFinder import *
from teamblue.src.GetRoom import *
from teamblue.src.CreatePersonPredictions import *
pl.seed_everything(42)

# Configuration TimeSeriesDataSet
person = "Locations_14_prep_v2_tft"
#person = person
input_df = pd.read_csv('teamblue/data/preprocessed/TFT_DataSets/' + person + ".csv")
input_df
input_df = input_df.loc[input_df["week_num"] < 44]
input_df = input_df.loc[input_df["no_movement_15min"].isin([1])]
input_df["idx"] = range(len(input_df))
week_43_length =  input_df.loc[input_df["week_num"] == 43]
week_43_length =  week_43_length.loc[week_43_length["coordinate_var"] == "x"]
week_43_length = len(week_43_length)
week_43_length

batch_size = 128 
num_workers = 12
# Evaluate: Set max_prediction_length to len(week_num) or more
max_prediction_length = 17
max_encoder_length = 600

training, train_dataloader, val_dataloader = CreateDataLoader(input_df, batch_size, num_workers,  max_prediction_length, max_encoder_length)


###############################
### Start Result DataFrame
###############################
name_var = "Locations_00_prep_v2_tft"

best_model_path = 'teamblue/models/Locations_14_prep_v2_tft/lightning_logs_tft/lightning_logs/version_0/checkpoints\epoch=119-step=1200.ckpt'
person_df_extended, person_df_vr_pred, person_df_vr_actual = CreatePersonPredictions(best_model_path, val_dataloader, input_df)
person_df_vr_actual.head()
###############################
### Ende Result DataFrame
###############################




#Make Basline Predictions
baseline_predictions = Baseline().predict(val_dataloader)
PredictBaseline(baseline_predictions,val_dataloader) 

# configure network and trainer

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)




early_stop_callback = EarlyStopping(monitor="train_loss", min_delta=1e-4, patience=30, verbose=False, mode="min")
lr_logger = LearningRateMonitor()  # log the learning rate
logger = TensorBoardLogger("teamblue/models/"+ person + "/lightning_logs_tft")  # logging results to a tensorboard

trainer = pl.Trainer(
    max_epochs=120,
    accelerator="gpu",
    enable_model_summary=True,
    gradient_clip_val=0.1,
    limit_train_batches=10,  # coment in for training, running valiation every 10 batches
    # fast_dev_run=True,  # comment in to check that networkor dataset has no serious bugs
    callbacks=[lr_logger, early_stop_callback],
    logger=logger,
)

  #return trainer, training, train_dataloader, val_dataloader

#LearningRate Finder

lr = OptimalLR(trainer, training, train_dataloader, val_dataloader); print(lr)
lr = print(list(lr)[0])


tft = TemporalFusionTransformer.from_dataset(
    training,
    learning_rate=0.01514,
    hidden_size=16,
    attention_head_size=2,
    dropout=0.1,
    hidden_continuous_size=8,
    loss=QuantileLoss(),
    log_interval=10,  # uncomment for learning rate finder and otherwise, e.g. to 10 for logging every 10 batches
    optimizer="Ranger",
    reduce_on_plateau_patience=4,
)
print(f"Number of parameters in network: {tft.size()/1e3:.1f}k")


# Traing tft model and return best_tft
tft = train(tft, trainer, train_dataloader, val_dataloader)


best_model_path = trainer.checkpoint_callback.best_model_path
best_model_path = 'teamblue/models/Locations_14_prep_v2_tft/lightning_logs_tft/lightning_logs/version_0/checkpoints/epoch=119-step=1200.ckpt'
best_tft = TemporalFusionTransformer.load_from_checkpoint(best_model_path)


predictions = best_tft.predict(val_dataloader, return_y=True, trainer_kwargs=dict(accelerator="gpu"))
MAE()(predictions.output, predictions.y)

import torch.nn.functional as F
actuals = torch.cat([y for x, (y, weight) in iter(val_dataloader)])
actuals

predictions = best_tft.predict(val_dataloader)
device = torch.device("cpu")
actuals = actuals.to(device)
predictions = predictions.to(device)

for i in range(3):
  var = ["x:", "y:", "z:"]
  print(var[i])
  # Calculate the Mean Absolute Error (MAE)
  mae = F.l1_loss(actuals[i], predictions[i])
  print("MAE:", mae.item())

  # Calculate the Mean Squared Error (MSE)
  mse = F.mse_loss(actuals[i], predictions[i])
  print("MSE:", mse.item())

  # Calculate the Root Mean Squared Error (RMSE)
  rmse = torch.sqrt(mse)
  print("RMSE:", rmse.item())


import matplotlib.pyplot as plt
actual_x = actuals[2].tolist()

predictions_x = predictions[2].tolist()

# Generate the index values based on the length of the lists
index = range(len(actual_x))

# Plot the lists
plt.plot(index, actual_x, label='Actual')
plt.plot(index, predictions_x, label='Predictions')

# Set labels and title
plt.xlabel('Index')
plt.ylabel('Value')
plt.title('z: Actual vs. Predicted')

# Show the legend
plt.legend()

# Display the plot
plt.show()


df_actuals = pd.DataFrame({'x': actuals[0], 'y': actuals[1], 'z': actuals[2]})
df_actuals.head(20)

df_actuals["x"] = df_actuals["x"] - 55
df_actuals["y"] = df_actuals["y"] - 10
df_actuals["z"] = df_actuals["z"] - 40
df_actuals = getRoom(df_actuals)

len(df_actuals)
df_actuals.head(20)
df_actuals = df_actuals.reset_index()

df_actuals["room"].value_counts()


df_predictions = pd.DataFrame({'x': predictions[0], 'y': predictions[1], 'z': predictions[2]})

df_predictions["x"] = df_predictions["x"] - 55
df_predictions["y"] = df_predictions["y"] - 10
df_predictions["z"] = df_predictions["z"] - 40
df_predictions = df_predictions.reset_index()

len(df_predictions)

df_predictions = getRoom(df_predictions)
df_predictions.head()

df_predictions["room"].value_counts()


# Accuracy
merged_df = pd.merge(df_actuals, df_predictions, on='index', suffixes=('_actual', '_prediction'))
accuracy = (merged_df['room_actual'] == merged_df['room_prediction']).mean()

print(f"Accuracy: {accuracy * 100:.2f}%")
>>>>>>> 48356b7e9e2c429c30e06ae92529e55b235f8c67
