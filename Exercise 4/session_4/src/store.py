import os
import joblib
from datetime import datetime
from metadata import MODELS_FOLDER, YOUR_NAME


def store_model(model, model_name: str) -> None:
    os.makedirs(MODELS_FOLDER, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    model_path = f"{MODELS_FOLDER}/{model_name}-{YOUR_NAME}-{timestamp}.joblib"
    joblib.dump(model, model_path)
    print(f"Model stored as: {model_path}")
