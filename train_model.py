import pandas as pd
import numpy as np
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

# Create folders
os.makedirs("models", exist_ok=True)
os.makedirs("results", exist_ok=True)

# Load Dataset
df = pd.read_csv("dataset/water_potability.csv")

print("Dataset Loaded Successfully!")
print("Dataset Shape:", df.shape)

# Separate Features and Target
X = df.drop("Potability", axis=1)
y = df["Potability"]

# Split Dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining Samples:", len(X_train))
print("Testing Samples:", len(X_test))

# Define Machine Learning Models
models = {
    "Logistic Regression": Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
        ("model", LogisticRegression(
            max_iter=1000,
            class_weight="balanced"
        ))
    ]),

    "Decision Tree": Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("model", DecisionTreeClassifier(
            random_state=42,
            class_weight="balanced"
        ))
    ]),

    "Random Forest": Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("model", RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            class_weight="balanced"
        ))
    ])
}

# Train and Evaluate Models
results = []
best_model = None
best_score = -1
best_model_name = ""

for name, model in models.items():

    print("\nTraining:", name)

    # Train Model
    model.fit(X_train, y_train)

    # Prediction
    y_pred = model.predict(X_test)

    # Evaluation
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)

    results.append({
        "Model": name,
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1
    })

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, zero_division=0))

    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    # Select Best Model using F1 Score
    if f1 > best_score:
        best_score = f1
        best_model = model
        best_model_name = name

# Save Results
results_df = pd.DataFrame(results)

results_df.to_csv(
    "results/model_comparison.csv",
    index=False
)

# Save Best Model
joblib.dump(best_model, "models/best_water_model.pkl")

# Display Comparison
print("\n========== MODEL COMPARISON ==========")
print(results_df.to_string(index=False))

print("\nBest Model:", best_model_name)
print("Best F1 Score:", round(best_score, 4))

print("\nBest Model Saved Successfully!")