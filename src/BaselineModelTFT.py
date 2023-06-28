import torch
import torch.nn.functional as F
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from pytorch_forecasting import Baseline
import math

def PredictBaseline(baseline_predictions, val_dataloader):
    actuals = torch.cat([y for x, (y, weight) in iter(val_dataloader)])
    #baseline_predictions = Baseline().predict(val_dataloader)
    device = torch.device("cpu")
    actuals = actuals.to(device)
    baseline_predictions = baseline_predictions.to(device)
    for i in range(len(actuals)):
        
        
        # Calculate the Mean Absolute Error (MAE)
        mae = mean_absolute_error(actuals[i], baseline_predictions[i])
        #print("MAE:", mae.item())

        # Calculate the Mean Squared Error (MSE)
        mse = mean_squared_error(actuals[i], baseline_predictions[i])
        #print("MSE:",  mae.item())

        # Calculate the Root Mean Squared Error (RMSE)
        rmse = math.sqrt(mse)
        #print("RMSE:",  mae.item())

        print(f"{i}: MAE: { mae} MSE: { mse} RMSE: { rmse}")

    #return actuals, baseline_predictions


