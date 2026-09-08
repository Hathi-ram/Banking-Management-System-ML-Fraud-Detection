# ==========================================================
# evaluate_model.py
# Random Forest Fraud Detection - Model Evaluation
# ==========================================================

import os
import json
import pickle

import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
    roc_auc_score
)
from sklearn.ensemble import RandomForestClassifier


# ==========================================================
# PATHS
# ==========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_FILE = os.path.join(
    BASE_DIR,
    "transactions_ml.csv"
)

MODEL_FILE = os.path.join(
    BASE_DIR,
    "fraud_model.pkl"
)

SCALER_FILE = os.path.join(
    BASE_DIR,
    "scaler.pkl"
)

ENCODER_FILE = os.path.join(
    BASE_DIR,
    "encoder.pkl"
)

FEATURE_FILE = os.path.join(
    BASE_DIR,
    "feature_columns.pkl"
)

THRESHOLD_FILE = os.path.join(
    BASE_DIR,
    "threshold.pkl"
)

METRICS_FILE = os.path.join(
    BASE_DIR,
    "model_metrics.json"
)


# ==========================================================
# LOAD DATA
# ==========================================================

print("\n" + "=" * 60)
print("RANDOM FOREST FRAUD DETECTION - MODEL EVALUATION")
print("=" * 60)

print("\nLoading dataset...")

df = pd.read_csv(DATA_FILE)

print("Dataset shape:", df.shape)


# ==========================================================
# TARGET
# ==========================================================

TARGET = "is_anomaly"

if TARGET not in df.columns:

    raise ValueError(
        f"Target column '{TARGET}' not found in dataset."
    )


y = df[TARGET].astype(int)


# ==========================================================
# DATETIME FEATURES
# ==========================================================

df["transaction_date"] = pd.to_datetime(
    df["transaction_date"],
    errors="coerce"
)


# ==========================================================
# CREATE FEATURES
# ==========================================================

df["amount_to_average_ratio"] = (
    df["amount"] /
    (df["account_average_amount"] + 1e-6)
)

df["amount_z_score"] = (
    df["amount_deviation"] /
    (df["account_std_amount"] + 1e-6)
)

df["hour_sin"] = np.sin(
    2 * np.pi * df["hour"] / 24
)

df["hour_cos"] = np.cos(
    2 * np.pi * df["hour"] / 24
)


# ==========================================================
# NUMERICAL FEATURES
# ==========================================================

numeric_features = [

    "amount",

    "hour",

    "day_of_week",

    "day_of_month",

    "month",

    "is_weekend",

    "account_average_amount",

    "account_std_amount",

    "account_transaction_count",

    "amount_deviation",

    "amount_to_average_ratio",

    "amount_z_score",

    "hour_sin",

    "hour_cos"
]


# ==========================================================
# CATEGORICAL FEATURES
# ==========================================================

categorical_features = [

    "transaction_type",

    "transaction_status"
]


# ==========================================================
# PREPARE X
# ==========================================================

X_numeric = df[numeric_features].copy()

X_categorical = df[categorical_features].copy()


# ==========================================================
# HANDLE MISSING VALUES
# ==========================================================

X_numeric = X_numeric.fillna(0)

X_categorical = X_categorical.fillna("Unknown")


# ==========================================================
# TRAIN / TEST SPLIT
# ==========================================================

X_num_train, X_num_test, X_cat_train, X_cat_test, y_train, y_test = train_test_split(

    X_numeric,
    X_categorical,
    y,

    test_size=0.20,

    random_state=42,

    stratify=y
)


print("\nTrain samples:", len(y_train))
print("Test samples :", len(y_test))


# ==========================================================
# SCALE NUMERICAL FEATURES
# ==========================================================

scaler = StandardScaler()

X_num_train_scaled = scaler.fit_transform(
    X_num_train
)

X_num_test_scaled = scaler.transform(
    X_num_test
)


# ==========================================================
# ENCODE CATEGORICAL FEATURES
# ==========================================================

encoder = OneHotEncoder(
    handle_unknown="ignore",
    sparse_output=False
)

X_cat_train_encoded = encoder.fit_transform(
    X_cat_train
)

X_cat_test_encoded = encoder.transform(
    X_cat_test
)


# ==========================================================
# COMBINE FEATURES
# ==========================================================

X_train = np.hstack([
    X_num_train_scaled,
    X_cat_train_encoded
])

X_test = np.hstack([
    X_num_test_scaled,
    X_cat_test_encoded
])


print("\nNumber of features:", X_train.shape[1])


# ==========================================================
# LOAD EXISTING MODEL
# ==========================================================

print("\nLoading trained Random Forest model...")

with open(MODEL_FILE, "rb") as file:

    model = pickle.load(file)


print("Model loaded successfully.")


# ==========================================================
# LOAD THRESHOLD
# ==========================================================

if os.path.exists(THRESHOLD_FILE):

    with open(THRESHOLD_FILE, "rb") as file:

        threshold = pickle.load(file)

    threshold = float(threshold)

else:

    threshold = 0.55


print("Detection threshold:", threshold)


# ==========================================================
# PREDICT PROBABILITIES
# ==========================================================

probabilities = model.predict_proba(
    X_test
)


# ==========================================================
# FIND CLASS 1 INDEX
# ==========================================================

if hasattr(model, "classes_"):

    classes = list(model.classes_)

    if 1 in classes:

        anomaly_index = classes.index(1)

    else:

        raise ValueError(
            "Model does not contain anomaly class 1."
        )

else:

    anomaly_index = 1


risk_scores = probabilities[:, anomaly_index]


# ==========================================================
# APPLY PROJECT THRESHOLD
# ==========================================================

y_pred = (
    risk_scores >= threshold
).astype(int)


# ==========================================================
# METRICS
# ==========================================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

precision = precision_score(
    y_test,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    zero_division=0
)

roc_auc = roc_auc_score(
    y_test,
    risk_scores
)


# ==========================================================
# CONFUSION MATRIX
# ==========================================================

cm = confusion_matrix(
    y_test,
    y_pred,
    labels=[0, 1]
)

tn, fp, fn, tp = cm.ravel()


# ==========================================================
# CLASSIFICATION REPORT
# ==========================================================

report = classification_report(

    y_test,

    y_pred,

    labels=[0, 1],

    target_names=[
        "Normal",
        "Suspicious"
    ],

    output_dict=True,

    zero_division=0
)


# ==========================================================
# DISPLAY RESULTS
# ==========================================================

print("\n" + "=" * 60)

print("MODEL PERFORMANCE")

print("=" * 60)

print(
    f"\nAccuracy  : {accuracy:.4f} "
    f"({accuracy * 100:.2f}%)"
)

print(
    f"Precision : {precision:.4f} "
    f"({precision * 100:.2f}%)"
)

print(
    f"Recall    : {recall:.4f} "
    f"({recall * 100:.2f}%)"
)

print(
    f"F1 Score  : {f1:.4f} "
    f"({f1 * 100:.2f}%)"
)

print(
    f"ROC-AUC   : {roc_auc:.4f}"
)


# ==========================================================
# CONFUSION MATRIX
# ==========================================================

print("\n" + "=" * 60)

print("CONFUSION MATRIX")

print("=" * 60)

print("\n                 Predicted")

print("              Normal  Suspicious")

print(
    f"Actual Normal     {tn:4d}      {fp:4d}"
)

print(
    f"Actual Suspicious {fn:4d}      {tp:4d}"
)


# ==========================================================
# CLASSIFICATION REPORT
# ==========================================================

print("\n" + "=" * 60)

print("CLASSIFICATION REPORT")

print("=" * 60)

print(
    classification_report(

        y_test,

        y_pred,

        labels=[0, 1],

        target_names=[
            "Normal",
            "Suspicious"
        ],

        zero_division=0
    )
)


# ==========================================================
# SAVE METRICS
# ==========================================================

metrics = {

    "model_name": "Random Forest",

    "model_version": "v1.0",

    "total_features": int(X_test.shape[1]),

    "test_samples": int(len(y_test)),

    "threshold": float(threshold),

    "accuracy": float(accuracy),

    "precision": float(precision),

    "recall": float(recall),

    "f1_score": float(f1),

    "roc_auc": float(roc_auc),

    "confusion_matrix": {

        "true_negative": int(tn),

        "false_positive": int(fp),

        "false_negative": int(fn),

        "true_positive": int(tp)
    },

    "classification_report": report
}


with open(
    METRICS_FILE,
    "w"
) as file:

    json.dump(
        metrics,
        file,
        indent=4
    )


print("\nMetrics saved to:")

print(METRICS_FILE)

print("\nEvaluation completed successfully.")

print("=" * 60)