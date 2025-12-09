import os
import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score
from faker import Faker
import numpy as np

# Set MLflow tracking URI
mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000"))
mlflow.set_experiment("churn_prediction")

def generate_data(n=1000):
    fake = Faker()
    data = []
    for _ in range(n):
        data.append({
            "tickets": np.random.randint(0, 10),
            "payment_delays": np.random.randint(0, 5),
            "subscription_months": np.random.randint(1, 24),
            "churn": np.random.choice([0, 1], p=[0.8, 0.2])
        })
    return pd.DataFrame(data)

def train():
    with mlflow.start_run():
        # Generate Data
        df = generate_data()
        X = df.drop("churn", axis=1)
        y = df["churn"]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train Model
        clf = RandomForestClassifier(n_estimators=100, random_state=42)
        clf.fit(X_train, y_train)
        
        # Evaluate
        y_pred = clf.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        # Log metrics
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_param("n_estimators", 100)
        
        # Log model
        mlflow.sklearn.log_model(clf, "model")
        
        print(f"Model trained with accuracy: {accuracy}")

if __name__ == "__main__":
    train()
