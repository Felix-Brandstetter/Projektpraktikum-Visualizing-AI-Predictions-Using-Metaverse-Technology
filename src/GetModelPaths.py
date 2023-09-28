<<<<<<< HEAD
import os
def getModelPaths():
    """
    Hilfsfunktion um die Pfade zu den jeweiligen Modelle abzurufen
        

    Returns:
        Pfade zu den Modellen
    """
    person_list = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
    model_list = []
    # Always uses version_0 -> maybe extend so it uses the highest version
    for i in person_list:
        root_folder = 'models/Locations_'+ i +'_prep_v2_tft/lightning_logs_tft/lightning_logs/version_0/'
        if os.path.exists(root_folder):
            path = os.path.join(root_folder)
            checkpoint_folder = os.path.join(path, "checkpoints")
            if os.path.exists(checkpoint_folder):
                path = os.listdir(checkpoint_folder)
                for file in os.listdir(checkpoint_folder):
                    file_path = os.path.join(checkpoint_folder, file)

                    # Check if the file ends with '.ckpt'
                    if file.endswith(".ckpt"):
                        model_list.append(file_path)
=======
import os
def getModelPaths():
    person_list = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
    model_list = []
    # Always uses version_0 -> maybe extend so it uses the highest version
    for i in person_list:
        root_folder = 'teamblue/models/Locations_'+ i +'_prep_v2_tft/lightning_logs_tft/lightning_logs/version_0/'
        if os.path.exists(root_folder):
            path = os.path.join(root_folder)
            checkpoint_folder = os.path.join(path, "checkpoints")
            if os.path.exists(checkpoint_folder):
                path = os.listdir(checkpoint_folder)
                for file in os.listdir(checkpoint_folder):
                    file_path = os.path.join(checkpoint_folder, file)

                    # Check if the file ends with '.ckpt'
                    if file.endswith(".ckpt"):
                        model_list.append(file_path)
>>>>>>> 48356b7e9e2c429c30e06ae92529e55b235f8c67
    return model_list