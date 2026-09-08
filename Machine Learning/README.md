## ML-Based Transaction Fraud Detection

This module provides real-time transaction scoring, risk assessment, and anomaly detection using an ensemble Machine Learning pipeline built into the Banking Management System.

---

## Overview & Architecture

The ML pipeline analyzes incoming banking transactions to flag potential fraud before completion or route suspicious activities for administrative review.

* **Model Type:** Random Forest Classifier (`v1.0`)
* **Features Analyzed:** 24 engine-derived behavioral and transactional features
* **Classification Threshold:** `0.55` (configurable)
* **Risk Categorization:** Low Risk, Medium Risk, High Risk

## Methodology:





### <img width="1024" height="559" alt="image" src="https://github.com/user-attachments/assets/76777adf-c5ed-47f5-988a-8d159c14f07f" />

                     ┌────────────────────────┐
                     │  Incoming Transaction  │
                     └───────────┬────────────┘
                                 │
                                 ▼
                     ┌────────────────────────┐
                     │  Feature Engineering   │
                     │ (24 Features Extracted)│
                     └───────────┬────────────┘
                                 │
                                 ▼
                     ┌────────────────────────┐
                     │  ML Inference Engine   │
                     │ (Random Forest Model)  │
                     └───────────┬────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Risk < 50%    │    │ 50% ≤ Risk < 85% │    │   Risk ≥ 85%    │
├─────────────────┤    ├──────────────────┤    ├─────────────────┤
│    Low Risk     │    │   Medium Risk    │    │    High Risk    │
│   (Approved)    │    │  (OTP / Flagged) │    │ (Hold / Review) │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         


---

##  Performance & Metrics

Model evaluation is conducted on real-time transaction data using standard classification metrics:

| Metric | Score | Description |
| :--- | :--- | :--- |
| **Accuracy** | `98.0%` | Ratio of overall correct predictions |
| **Precision** | `76.0%` | Accuracy of flagged fraud predictions |
| **Recall** | `47.0%` | Percentage of total actual fraud cases captured |
| **F1-Score** | `58.0%` | Harmonic mean of Precision and Recall |

> **Note on Tuning:** The current threshold (`0.55`) emphasizes High Precision to minimize false alerts. Lowering the prediction threshold to `0.35 - 0.40` or implementing **SMOTE** re-sampling can significantly improve **Recall** for higher fraud capture rates.

---

## Feature Engineering (24 Key Drivers)

The model extracts and evaluates 24 dynamic features per transaction:
* **Transaction Characteristics:** Amount, Transaction Type (`Transfer`, `RTGS`, `Withdrawal`, `Deposit`), Time of Day, Day of Week.
* **Account Dynamics:** Sender/Receiver account balances, historical transaction frequency, average transaction size, balance-to-amount ratios.
* **Velocity Metrics:** Transaction frequency over short time windows (e.g., 1 hour / 24 hours), sudden balance depletion indicators.

---

###  How to Run & Re-train

### 1. Requirements
Ensure your Python environment has the necessary ML packages installed:
```bash
pip install pandas numpy scikit-learn joblib

## Model Training & Export
To re-train the Random Forest model on updated database records:

Bash
python ml/train_model.py

## Real-Time Inference (Flask Integration)The model is automatically invoked within the Flask transaction processing routes (app.py):Pythonimport joblib

## Load trained model & scaler
model = joblib.load('ml/model.pkl')
scaler = joblib.load('ml/scaler.pkl')

def predict_fraud(transaction_data):
    features = extract_features(transaction_data) # Returns 24-feature vector
    scaled_features = scaler.transform([features])
    
    probability = model.predict_proba(scaled_features)[0][1] # Fraud Probability
    is_suspicious = probability >= 0.55
    
    return {
        "risk_score": round(probability * 100, 2),
        "prediction": "Suspicious" if is_suspicious else "Normal",
        "risk_status": "High Risk" if probability >= 0.85 else ("Medium Risk" if is_suspicious else "Low Risk")
    }


** ## Risk Handling Protocol **

**## Risk Assessment Levels**

Risk Level	Score Range	Automated Protocol
🟢 Low Risk	0.0% – 49.9%	Instantly process and log transaction.
🟡 Medium Risk	50.0% – 84.9%	Flag transaction; trigger Multi-Factor Authentication (MFA / OTP).
🔴 High Risk	85.0% – 100.0%	Block/Hold funds; send alert to admin dashboard for manual review.

**## Protocol Action Summary**

```mermaid
flowchart TD
    A[Incoming Transaction] --> B["Feature Engineering<br/>(24 Features Extracted)"]
    B --> C["ML Inference Engine<br/>(Random Forest Model)"]
    
    C --> D["Risk < 50%<br/><b>Low Risk</b><br/>(Approved)"]
    C --> E["50% ≤ Risk < 85%<br/><b>Medium Risk</b><br/>(OTP / Flagged)"]
    C --> F["Risk ≥ 85%<br/><b>High Risk</b><br/>(Hold / Review)"]
