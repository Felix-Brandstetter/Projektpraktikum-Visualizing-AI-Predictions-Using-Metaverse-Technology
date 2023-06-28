# fit network
def train(tft, trainer, train_dataloader, val_dataloader):
    trainer.fit(
        tft,
        train_dataloaders=train_dataloader,
        val_dataloaders=val_dataloader,
    )
    best_tft = trainer.checkpoint_callback.best_model_path
    return best_tft