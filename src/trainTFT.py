<<<<<<< HEAD
# fit network
def train(tft, trainer, train_dataloader, val_dataloader):
    """
    Traing der Modells

    Args:
        tft, trainer: Konfiguration des Modells
        Trainings und Validation-Loader

    Returns:
        Trainiertes Modell
    """
    trainer.fit(
        tft,
        train_dataloaders=train_dataloader,
        val_dataloaders=val_dataloader,
    )
    best_tft = trainer.checkpoint_callback.best_model_path
=======
# fit network
def train(tft, trainer, train_dataloader, val_dataloader):
    trainer.fit(
        tft,
        train_dataloaders=train_dataloader,
        val_dataloaders=val_dataloader,
    )
    best_tft = trainer.checkpoint_callback.best_model_path
>>>>>>> 48356b7e9e2c429c30e06ae92529e55b235f8c67
    return best_tft