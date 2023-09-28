import os
def getDataPaths():
    """
    Hilfsfunktion um die Pfade zu den jeweiligen Datasets abzurufen
        

    Returns:
        Pfade zum Dataset
    """
    person_list = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
    data_list = []
    # Always uses version_0 -> maybe extend so it uses the highest version
    for i in person_list:
        root_folder = 'data/preprocessed/TFT_DataSets/Locations_'+ i +'_prep_v2_tft.csv'
        if os.path.exists(root_folder):
            path = os.path.join(root_folder)
            data_list.append(path)
    return data_list


