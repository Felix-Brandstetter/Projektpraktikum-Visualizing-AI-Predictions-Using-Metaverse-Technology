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
    return best_tft