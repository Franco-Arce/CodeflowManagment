import mlflow.sklearn
import pandas as pd
import os

class MLService:
    def __init__(self):
        self.model = None
        self.load_model()

    def load_model(self):
        try:
            # Try loading from MLflow registry or specific run
            # For simplicity, we'll try to load a local artifact or a specific run ID if env var is set
            model_uri = os.getenv("MODEL_URI", "models:/churn_prediction/Production")
            self.model = mlflow.sklearn.load_model(model_uri)
            print("Model loaded from MLflow")
        except Exception as e:
            print(f"Could not load model from MLflow: {e}")
            self.model = None

    def predict_churn(self, data: dict):
        if not self.model:
            return 0.5 # Default fallback
        
        df = pd.DataFrame([data])
        # Ensure columns match training data
        # In a real app, we'd have a schema validator here
        try:
            prediction = self.model.predict(df)
            return int(prediction[0])
        except Exception as e:
            print(f"Prediction error: {e}")
            return 0.5

ml_service = MLService()
