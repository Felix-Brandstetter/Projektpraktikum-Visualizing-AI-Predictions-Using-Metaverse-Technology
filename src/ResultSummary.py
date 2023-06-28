import pandas as pd
from pytorch_forecasting import TemporalFusionTransformer
import torch
import torch.nn.functional as F
import math
from teamblue.src.GetRoom import getRoom
torch.seed(42)

def resultsSummary(person, best_model_path, val_dataloader):
    
    best_model_path
    best_tft = TemporalFusionTransformer.load_from_checkpoint(best_model_path)
    actuals = torch.cat([y for x, (y, weight) in iter(val_dataloader)])
    predictions = best_tft.predict(val_dataloader)
    device = torch.device("cpu")
    actuals = actuals.to(device)
    predictions = predictions.to(device)


    mae_x = F.l1_loss(actuals[0], predictions[0]).item()
    mae_x
    mse_x = F.mse_loss(actuals[0], predictions[0]).item()
    rmse_x = math.sqrt(mse_x)

    mae_y = F.l1_loss(actuals[0], predictions[0]).item()
    mse_y = F.mse_loss(actuals[0], predictions[0]).item()
    rmse_y = math.sqrt(mse_x)

    mae_z = F.l1_loss(actuals[0], predictions[0]).item()
    mse_z = F.mse_loss(actuals[0], predictions[0]).item()
    rmse_z = math.sqrt(mse_x)



    df_actuals = pd.DataFrame({'x': actuals[0], 'y': actuals[1], 'z': actuals[2]})
    df_actuals["x"] = df_actuals["x"] - 55
    df_actuals["y"] = df_actuals["y"] - 10
    df_actuals["z"] = df_actuals["z"] - 40
    df_actuals = getRoom(df_actuals)
    df_actuals = df_actuals.reset_index()


    df_predictions = pd.DataFrame({'x': predictions[0], 'y': predictions[1], 'z': predictions[2]})
    df_predictions["x"] = df_predictions["x"] - 55
    df_predictions["y"] = df_predictions["y"] - 10
    df_predictions["z"] = df_predictions["z"] - 40
    df_predictions = df_predictions.reset_index()
    df_predictions = getRoom(df_predictions)
    
    # Accuracy
    merged_df = pd.merge(df_actuals, df_predictions, on='index', suffixes=('_actual', '_prediction'))
    accuracy = (merged_df['room_actual'] == merged_df['room_prediction']).mean() * 100

    summary_dict = {
    "person": person,
    "x_MAE": mae_x,
    "x_MSE": mse_x,
    "x_RMSE": rmse_x,
    "y_MAE": mae_y,
    "y_MSE": mse_y,
    "y_RMSE": rmse_y,
    "z_MAE": mae_z,
    "z_MSE": mse_z,
    "z_RMSE": rmse_z,
    "accuracy": accuracy
    }

    return summary_dict





