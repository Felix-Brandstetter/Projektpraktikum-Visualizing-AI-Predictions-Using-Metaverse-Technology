import pandas as pd
from src.GetRoom import *
from pytorch_forecasting import TemporalFusionTransformer

def CreatePersonPredictions(best_model_path, val_dataloader, input_df):
    
    """
    Macht eine Prediction mit dem Modell, welches über den Pfad übergeben bekommt.
    Transformiert die Koordinaten wieder zurück in ihre ursprüngliche Form. 
    Dazu wir das Tupel-XYZ zum jeweiligen Raum gemappt.  

    Args:
        Path to Model, Val_Dataloader und Input_df

    Returns:
        Datensatz zu jeweiligen Person mit den Prediction results
    """

    
    best_tft = TemporalFusionTransformer.load_from_checkpoint(best_model_path)
    raw_predictions = best_tft.predict(val_dataloader, mode="prediction", return_x=True, return_y=True, return_index=True, return_decoder_lengths=True)
    
    start_idx = raw_predictions[2]["idx"][0]
    int(start_idx)
    decoder_length = raw_predictions[3][0].item()
    int(decoder_length)
    idx_length = [x for x in range(start_idx, start_idx+decoder_length)]
    idx_length
    decoder_length

    x_pred = raw_predictions[0][0]
    x_pred = x_pred.tolist()
    
    y_pred = raw_predictions[0][1]
    y_pred = y_pred.tolist()
    
    z_pred = raw_predictions[0][2]
    z_pred = z_pred.tolist()
    

    final_df = pd.DataFrame({
        'idx': idx_length,
        'x': x_pred,
        'y': y_pred,
        'z': z_pred
    })
    final_df["x"] = final_df["x"] - 55
    final_df["y"] = final_df["y"] - 10
    final_df["z"] = final_df["z"] - 40

    final_df_room = getRoom(final_df)
    final_df_room["index_join"] = range(len(final_df_room)) 
    

    data = input_df
    data = data.loc[data["no_movement_15min"].isin([1])]
    data["idx"] = range(len(data))
    data = data.loc[data["week_num"] == 43]
    help_df = data.loc[data["coordinate_var"] == "x"]
    help_df = help_df[["idx", "coordinate"]]
    
    help_df["index_join"] = range(len(help_df)) 
    
    

    pivoted_df = data.pivot(index=['hour', 'minute', 'day', 'day_new', 'week_num'],
                      columns='coordinate_var', values='coordinate').reset_index()
    pivoted_df = pivoted_df.sort_values(by=['day', 'hour', 'minute'])
    pivoted_df["index_join"] = range(len(pivoted_df)) 
    
    if(len(help_df) != len(pivoted_df)):
        print("Warning: Join dfs with different lengths! \nCreatePersonPredictions: Check the Join help_df & pivoted_df")
    pivoted_df
    pivoted_df = pd.merge(pivoted_df, help_df, left_on=["index_join"], right_on=["index_join"])#, " y_actual", "z_actual"])              
    pivoted_df = pivoted_df.drop(["coordinate"], axis=1)
    pivoted_df
    pivoted_df["x"] = pivoted_df["x"] - 55
    pivoted_df["y"] = pivoted_df["y"] - 10
    pivoted_df["z"] = pivoted_df["z"] - 40
    pivoted_df = pivoted_df.sort_values(by=['day', 'hour', 'minute'])
    pivoted_df_room = getRoom(pivoted_df)
    pivoted_df_room
    

    if(len(pivoted_df_room) != len(final_df_room)):
        print("Warning: Join dfs with different lengths! \nCreatePersonPredictions: Check the Join pivoted_df & final_df_room")

    merged_df = pd.merge(pivoted_df_room, final_df_room, left_on=["index_join"], right_on=["index_join"], suffixes=('_actual', '_prediction'))
    merged_df
    person_df_extended = merged_df[['idx_prediction', "week_num", "day", "day_new", "hour", "minute", "x_actual", "y_actual", "z_actual", "room_actual", "x_prediction", "y_prediction",  "z_prediction", "room_prediction"]]
    person_df_extended
    
    ################################
    ### Person DataFrame VR Team ###
    ################################
    
    # Start Punkt mit Minuten Ablauf, einheitlich für alle Personen, evt Montag 8 Uhr morgen bis Freitag 18 Uhr
    # Jeden Tag zwischen 8 Uhr und 18 Uhr (day:215 until 219)
    # Ort für None/no Room definieren

    #minuten_Tag = 10*60
    def getMinuteOfWeek(day, hour, minute):
        print("Getting minutes")
        my_dictionary = {215: 0, 216: 1, 217: 2, 218: 3, 219:4}
        if day in my_dictionary:
            factor = my_dictionary[day]
        else:
            print("Wrong Week Days")

        minute_output = 600 * factor
        minute_output = minute_output + (hour - 8) * 60 + minute
        return minute_output


    person_df_vr_pred = person_df_extended[["day", "hour", "minute", "room_prediction"]]
    person_df_vr_pred["minute_idx"] = ""
    for i in range(len(person_df_vr_pred)):
        person_df_vr_pred["minute_idx"][i] = getMinuteOfWeek(person_df_extended["day"][i], person_df_extended["hour"][i], person_df_extended["minute"][i])

    person_df_vr_actual = person_df_extended[["day", "hour", "minute", "room_actual"]]
    person_df_vr_actual["minute_idx"] = ""
    for i in range(len(person_df_vr_actual)):
        person_df_vr_actual["minute_idx"][i] = getMinuteOfWeek(person_df_vr_actual["day"][i], person_df_vr_actual["hour"][i], person_df_vr_actual["minute"][i])

    return person_df_extended, person_df_vr_pred, person_df_vr_actual

    

