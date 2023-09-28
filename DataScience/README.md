# Data Science 

## Beschreibung der Orderstruktur

### Data
Beinhaltet die neuen und alten raw Data.
Verschiedene Arten preprocessed Data und die TFT Datasets.
Die dummy Datafiles zum Testen für das AR Team.
Sowie die Ergebnisse der Vorhersage.


### Docs
Enthält die ursprüngliche Beschreibung des Problems und
die Rollen der einzelnen Personen.


### Models
Enthält die trainierten TFT (Temporal Fusion Transformer) Modelle mit ihren jeweiligen Checkpoints
für die einzelnen Personen


### Notebooks
Enthält das Notebooks zum Heizungsalgorithmus.
Dazu Notebooks zur Datenanalyse, 
die restlichen Notebooks dienten vor allem zu Testzwecken.


### Source
------------
```
├── src
    ├── BaselineModelTFT.py                 <-- Ermöglicht eine Baseline Prediction auf dem untrainierten Modell
    ├── CreateDL.py                         <-- Erstellt den TrainLoader und ValidationLoader
    ├── CreatePersonPredictions.py          <-- Macht eine Prediction mit dem trainierten Modell für eine Person
    ├── CreateResults.py                    <-- Schreibt die Ergebnisse in ein csv file
    ├── CreateRoomDF.py                     <-- Erstellt die Ergebnisse für die Raumprognose
    ├── DataPrepTFT.py                      <-- Erstellt DataFrame im passenden TFT Format
    ├── GetDataPaths.py                     <-- Hilfsfunktion für den Pfad zu den Datasets
    ├── GetModelPaths.py                    <-- Hilfsfunktion für den Pfad zu dem Model
    ├── GetRoom.py                          <-- Weißt Koordinaten den Räumen zu
    ├── LearningRateFinder.py               <-- Ermittelt die optimale Learningrate für ein Modell
    ├── MainTFTModel.py                     <-- Main Funktion: Auswahl der Person, Starten des Trainings
    ├── Preprocessing.py                    <-- Preprocessing der raw Data, bevor ein TFT Dataset erstellt wird 
    ├── ResultSummary.py                    <-- Summary der Ergebnisse aller Modelle
    └── trainTFT.py                         <-- Übernimmt das Training der Modelle
```