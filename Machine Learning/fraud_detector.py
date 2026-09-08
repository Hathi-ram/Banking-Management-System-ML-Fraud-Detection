# ============================================================
# FRAUD DETECTION SERVICE
# ============================================================

import os
import joblib
import pandas as pd
import numpy as np


# ============================================================
# ML FILE LOCATION
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "Machine Learning",
    "fraud_detection"
)


# ============================================================
# MODEL FILES
# ============================================================

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "fraud_model.pkl"
)

SCALER_PATH = os.path.join(
    MODEL_DIR,
    "scaler.pkl"
)

ENCODER_PATH = os.path.join(
    MODEL_DIR,
    "encoder.pkl"
)

FEATURE_PATH = os.path.join(
    MODEL_DIR,
    "feature_columns.pkl"
)

THRESHOLD_PATH = os.path.join(
    MODEL_DIR,
    "threshold.pkl"
)


# ============================================================
# LOAD ML OBJECTS
# ============================================================

try:

    model = joblib.load(MODEL_PATH)

    scaler = joblib.load(SCALER_PATH)

    encoder = joblib.load(ENCODER_PATH)

    feature_columns = joblib.load(FEATURE_PATH)

    threshold = float(
        joblib.load(THRESHOLD_PATH)
    )

    print(
        "Fraud Detection ML system loaded successfully."
    )

    print(
        "Number of features:",
        len(feature_columns)
    )

    print(
        "ML threshold:",
        round(threshold, 4)
    )


except Exception as e:

    print(
        "ERROR: Could not load fraud detection ML system."
    )

    print(
        "Reason:",
        e
    )

    raise


# ============================================================
# VALIDATE MODEL
# ============================================================

if not hasattr(model, "predict_proba"):

    raise TypeError(
        "The loaded fraud model does not support predict_proba()."
    )


# ============================================================
# PREDICT TRANSACTION
# ============================================================

def predict_transaction(
    amount,
    transaction_type,
    transaction_status,
    transaction_date,
    account_average_amount,
    account_std_amount,
    account_transaction_count
):

    # ========================================================
    # 1. VALIDATE / CONVERT INPUTS
    # ========================================================

    amount = float(amount)

    account_average_amount = float(
        account_average_amount or 0
    )

    account_std_amount = float(
        account_std_amount or 0
    )

    account_transaction_count = int(
        account_transaction_count or 0
    )

    transaction_date = pd.to_datetime(
        transaction_date
    )


    # ========================================================
    # 2. DATE / TIME FEATURES
    # ========================================================

    hour = transaction_date.hour

    day_of_week = transaction_date.dayofweek

    day_of_month = transaction_date.day

    month = transaction_date.month

    is_weekend = (
        1
        if day_of_week >= 5
        else 0
    )


    # ========================================================
    # 3. AMOUNT DEVIATION
    # ========================================================

    if account_std_amount > 0:

        amount_deviation = (
            abs(
                amount -
                account_average_amount
            )
            /
            account_std_amount
        )

    else:

        amount_deviation = 0.0


    # ========================================================
    # 4. AMOUNT / AVERAGE RATIO
    # ========================================================

    if account_average_amount > 0:

        amount_to_average_ratio = (
            amount /
            account_average_amount
        )

    else:

        amount_to_average_ratio = 0.0


    # ========================================================
    # 5. AMOUNT Z-SCORE
    # ========================================================

    if account_std_amount > 0:

        amount_z_score = (
            (
                amount -
                account_average_amount
            )
            /
            account_std_amount
        )

    else:

        amount_z_score = 0.0


    # ========================================================
    # 6. CYCLICAL TIME FEATURES
    # ========================================================

    hour_sin = np.sin(
        2 *
        np.pi *
        hour /
        24
    )

    hour_cos = np.cos(
        2 *
        np.pi *
        hour /
        24
    )


    # ========================================================
    # 7. NUMERICAL FEATURES
    # ========================================================

    numerical_data = pd.DataFrame([{

        "amount": amount,

        "hour": hour,

        "day_of_week": day_of_week,

        "day_of_month": day_of_month,

        "month": month,

        "is_weekend": is_weekend,

        "account_average_amount":
            account_average_amount,

        "account_std_amount":
            account_std_amount,

        "account_transaction_count":
            account_transaction_count,

        "amount_deviation":
            amount_deviation,

        "amount_to_average_ratio":
            amount_to_average_ratio,

        "amount_z_score":
            amount_z_score,

        "hour_sin":
            hour_sin,

        "hour_cos":
            hour_cos

    }])


    # ========================================================
    # 8. SCALE NUMERICAL FEATURES
    # ========================================================

    scaled_data = scaler.transform(
        numerical_data
    )

    scaled_df = pd.DataFrame(
        scaled_data,
        columns=numerical_data.columns
    )


    # ========================================================
    # 9. CATEGORICAL FEATURES
    # ========================================================

    categorical_data = pd.DataFrame([{

        "transaction_type":
            transaction_type,

        "transaction_status":
            transaction_status

    }])


    # ========================================================
    # 10. ENCODE CATEGORICAL FEATURES
    # ========================================================

    encoded_data = encoder.transform(
        categorical_data
    )

    encoded_columns = (
        encoder.get_feature_names_out()
    )

    encoded_df = pd.DataFrame(
        encoded_data,
        columns=encoded_columns
    )


    # ========================================================
    # 11. COMBINE FEATURES
    # ========================================================

    final_features = pd.concat(
        [
            scaled_df,
            encoded_df
        ],
        axis=1
    )


    # ========================================================
    # 12. ENSURE EXACT TRAINING FEATURE ORDER
    # ========================================================

    final_features = final_features.reindex(
        columns=feature_columns,
        fill_value=0
    )


    # ========================================================
    # 13. FINAL FEATURE VALIDATION
    # ========================================================

    if list(final_features.columns) != list(
        feature_columns
    ):

        raise ValueError(
            "Feature mismatch between training "
            "and prediction."
        )


    # ========================================================
    # 14. MODEL SCORE
    # ========================================================

    class_probabilities = model.predict_proba(
        final_features
    )[0]


    # --------------------------------------------------------
    # Find class-1 probability safely
    # --------------------------------------------------------

    if hasattr(model, "classes_"):

        classes = list(
            model.classes_
        )

        if 1 in classes:

            fraud_class_index = classes.index(1)

        else:

            raise ValueError(
                "Fraud/anomaly class '1' "
                "is not present in the trained model."
            )

    else:

        # Fallback for normal binary classifier
        fraud_class_index = 1


    risk_score = float(
        class_probabilities[
            fraud_class_index
        ]
    )


    # ========================================================
    # 15. APPLY TRAINED THRESHOLD
    # ========================================================

    prediction = (
        1
        if risk_score >= threshold
        else 0
    )


    # ========================================================
    # 16. RISK LEVEL
    # ========================================================

    if risk_score < 0.40:

        risk_level = "Low"

    elif risk_score < 0.70:

        risk_level = "Medium"

    else:

        risk_level = "High"


    # ========================================================
    # 17. RESULT
    # ========================================================

    return {

        "prediction": prediction,

        "is_anomaly": prediction,

        "risk_score": round(
            risk_score,
            5
        ),

        "risk_percentage": round(
            risk_score * 100,
            2
        ),

        "risk_level": risk_level,

        "threshold": round(
            threshold,
            5
        ),

        "model_version": "v1.0"

    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    result = predict_transaction(

        amount=50000,

        transaction_type="Withdrawal",

        transaction_status="Success",

        transaction_date="2026-08-21 22:29:16",

        account_average_amount=15000,

        account_std_amount=8500,

        account_transaction_count=20

    )


    print("\n")
    print("=" * 55)
    print("FRAUD DETECTION TEST")
    print("=" * 55)

    print(
        "Prediction:",
        result["prediction"]
    )

    print(
        "Risk Score:",
        result["risk_score"]
    )

    print(
        "Risk Percentage:",
        f'{result["risk_percentage"]:.2f}%'
    )

    print(
        "Threshold:",
        result["threshold"]
    )

    print(
        "Risk Level:",
        result["risk_level"]
    )

    print(
        "Model Version:",
        result["model_version"]
    )

    print("-" * 55)


    if result["prediction"] == 1:

        print(
            "Result: SUSPICIOUS TRANSACTION"
        )

    else:

        print(
            "Result: NORMAL TRANSACTION"
        )

    print("=" * 55)