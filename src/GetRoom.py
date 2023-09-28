import ast
import pandas as pd
from shapely.geometry import Point
from shapely.geometry import Polygon

def getRoom(df):
    """
    This function takes a DataFrame `df` and returns a new DataFrame with an additional column `room`.
    The `room` column contains the room number for each point in the DataFrame.

    The function first reads the `raumkoordinaten_prep.csv` file, which contains the coordinates of all the rooms in the building.
    The function then creates a new column `y_binary` in `df`. This column is 1 if the point is located on the upper floor of the building and 0 if the point is located on the lower floor.
    The function then loops through each point in `df`. For each point, the function finds the room that contains the point. The function then assigns the room number to the `room` column in `df`.
    The function returns the new DataFrame with the `room` column.

    Parameters
    ----------
    df : DataFrame
        A DataFrame containing the coordinates of the points.

    Returns
    -------
    DataFrame
        A new DataFrame with an additional column `room`.

    """

    room_coordinates = pd.read_csv('data/preprocessed/Raumkoordinaten/raumkoordinaten_prep_unity.csv', index_col = 0)
    df.columns = df.columns.str.lower()
    if 'y_binary' in df:
        pass
    else:
        df["y_binary"] = ""
        df.loc[(df["y"] >= -1) & (df["y"] <= 3), "y_binary"] = 1
        df.loc[(df["y"] >= -10) & (df["y"] < -1), "y_binary"] = 0
        df = df.loc[df["y_binary"].isin([0,1])]
        df = df.reset_index(drop=True)
    
    df["room"] = ""
    
    for i in range(len(df["x"])):
        x = df["x"][i]
        z = df["z"][i]
        floor = df["y_binary"][i]
        coor_help = room_coordinates.loc[room_coordinates["floor"] == floor]
        coor_help = coor_help.reset_index(drop=True)

        point = Point(x, z)
        for c in range(len(coor_help)):
            polygon = Polygon(ast.literal_eval(coor_help["coor"][c]))
            res = polygon.contains(point)
            if res:
                df.loc[i, "room"] = coor_help["room"][c]
    return df





