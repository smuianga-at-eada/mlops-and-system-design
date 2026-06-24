
YOUR_NAME = "Shelcia"

MODELS_FOLDER = "session_4/models"
DATASETS_FOLDER = "session_4/datasets"
MODEL_NAME = "class_model"

TARGET_COLUMN = "Exited"


COLUMNS_TO_DROP = ["RowNumber", "CustomerId", "Surname"]


MODE_IMPUTE_COLUMNS = ["Geography"]


MEDIAN_IMPUTE_COLUMNS = ["Age", "HasCrCard"]


GENDER_MAPPING = {"Male": 1, "Female": 0}


BINARY_NUMERIC_COLUMNS = ["HasCrCard", "IsActiveMember"]

ONE_HOT_ENCODE_COLUMNS = ["Geography"]

MODEL_PARAMS = {
    "max_depth": 6,
    "min_samples_leaf": 20,
    "random_state": 8888,
}
