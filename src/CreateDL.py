from pytorch_forecasting import TimeSeriesDataSet
from pytorch_forecasting.data import GroupNormalizer

def CreateDataLoader(input_df, batch_size, num_workers,  max_prediction_length, max_encoder_length):
    
    """
    Erstellt den Trainings- und Validationloader und spezifiziert das Dataset

    Args:
        input_df, batch_size, num_workers,  max_prediction_length, max_encoder_length

    Returns:
        Trainings-Set, Train_Loader und Validation_Loader
    """

    time_df = input_df
    max_prediction_length = max_prediction_length # one week prediction with 12 weeks of data
    max_encoder_length = max_encoder_length
    training_cutoff = time_df["idx"].max() - max_prediction_length

    training = TimeSeriesDataSet(
    time_df[lambda x: x.idx <= training_cutoff],
    time_idx="idx",
    target="coordinate",
    group_ids=["coordinate_var"],
    min_encoder_length=max_encoder_length // 2,  # keep encoder length long (as it is in the validation set)
    max_encoder_length=max_encoder_length,
    min_prediction_length=1,
    max_prediction_length=max_prediction_length,
    static_categoricals=["coordinate_var"],
    #static_reals=["avg_population_2017", "avg_yearly_household_income_2017"],
    time_varying_known_categoricals=["day_new"],
    #variable_groups={"special_days": special_days},  # group of categorical variables can be treated as one variable
    time_varying_known_reals=["hour", "minute", "day", "week_num", "idx"],
    #time_varying_unknown_categoricals=[],
    time_varying_unknown_reals=["coordinate"],
    
    target_normalizer=GroupNormalizer(
        groups=["coordinate_var"], transformation="softplus",
    ),  # use softplus and normalize by group

    add_relative_time_idx=True,
    add_target_scales=True,
    add_encoder_length=True,
    allow_missing_timesteps=True,

    )

    validation = TimeSeriesDataSet.from_dataset(training, time_df, predict=True, stop_randomization=True)

    # create dataloaders for  our model
    # if you have a strong GPU, feel free to increase the number of workers
    train_dataloader = training.to_dataloader(train=True, batch_size = batch_size, num_workers = num_workers)
    val_dataloader = validation.to_dataloader(train=False, batch_size = batch_size * 10, num_workers = num_workers)

    return training, train_dataloader, val_dataloader