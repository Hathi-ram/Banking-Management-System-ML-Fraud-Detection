## Banking Management System with Machine Learning Fraud Detection

A full-stack Banking Management System built using Python, Flask, MySQL, HTML/CSS, Bootstrap, and Scikit-Learn, integrated with a Random Forest-based Machine Learning transaction fraud detection system.

The application manages the complete banking workflow including:

### <img width="2878" height="1536" alt="HomeScreen_page_1" src="https://github.com/user-attachments/assets/e487790a-4be2-4f6e-b015-0aa02f23eeab" />

### <img width="2880" height="1524" alt="HomeScreen_page_2" src="https://github.com/user-attachments/assets/ea577444-122e-48b3-beb0-fa92e0aab8eb" />

### <img width="2880" height="1534" alt="HomeScreen_page_3" src="https://github.com/user-attachments/assets/c081195b-3f9c-4729-a6c5-0f8363209cd0" />


##  Tech Stack

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black?logo=flask)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange?logo=mysql&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine%20Learning-F7931E?logo=scikit-learn&logoColor=white)

### Backend
- Python
- Flask
- MySQL Connector

### Machine Learning
- Scikit-Learn
- Random Forest Classifier
- Pandas
- NumPy
- Joblib

### Frontend
- HTML5
- CSS3
- Bootstrap 5
- JavaScript
- Chart.js

### Database
- MySQL
- MySQL Workbench

---

## Problem Statement

Traditional banking management systems primarily focus on storing customer information and processing transactions.

However, transaction processing alone is not sufficient for identifying potentially fraudulent activities.

Some common challenges include:

- Limited real-time transaction risk assessment
- Difficulty identifying unusual transaction behavior
- Manual fraud monitoring
- Financial losses caused by suspicious transactions
- Lack of automated risk scoring
- Limited visibility into transaction-level risk
- Separation between banking operations and fraud detection systems

A banking application therefore needs a mechanism that can analyze transactions automatically and provide an immediate indication of potential risk.

---

## Solution Overview

This project combines a complete **Banking Management System** with an integrated **Machine Learning-based transaction fraud detection module**.

The application provides normal banking operations through a Flask web interface while automatically sending transaction information to a trained Machine Learning model.

The proposed system provides two major capabilities:

## 1. Banking Management

The Flask application manages:

- Customer information
- Bank accounts
- Deposits
- Withdrawals
- Transfers
- Loans
- Cards
- Employees
- Activity logs
- Reports
- Dashboard analytics

## 2. Machine Learning Fraud Detection

Whenever a transaction is created, the system:

- Collects transaction information
- Generates transaction features
- Preprocesses the features
- Sends them to the trained Random Forest model
- Generates a fraud probability/risk score
- Applies the classification threshold
- Classifies the transaction as Normal or Suspicious
- Assigns a Low, Medium, or High risk level
- Stores the ML result in MySQL
- Displays the result in the dashboard, transactions page, activity logs, and ML analytics

## Key Features & Capabilities
##  1. Customer Management

The Customer Management module allows administrators to:

Add customers
View customer details
Update customer information
Delete customer records
Search customers
Manage customer-related banking information

Customer information is stored securely in the MySQL database.

## 2. Account Management

The Account Management module provides:

Account creation
Savings and Current account support
Account balance management
Account status tracking
Customer-account relationship management
Account search and viewing

Each account is linked to its respective customer.

## 3. Transaction Management

The system supports major banking transactions:

Deposit

Allows money to be deposited into a customer account.

Withdrawal

Allows money to be withdrawn while checking the available account balance.

Transfer

Allows money to be transferred between accounts.

Transaction History

All transactions are recorded and can be searched and reviewed.

Supported transaction types include:

Deposit
Withdrawal
Transfer
UPI
NEFT
RTGS
IMPS

## 4. Machine Learning Fraud Detection

The major feature of this project is the integrated Machine Learning fraud detection module.

Whenever a new transaction is created:

The model analyzes transaction characteristics such as:

Transaction amount
Transaction hour
Day of week
Day of month
Month
Weekend information
Account average transaction amount
Account standard deviation
Account transaction count
Amount deviation
Amount-to-average ratio
Amount z-score
Transaction type
Transaction status

## Random Forest Model

The fraud detection module uses a Random Forest Classifier.

The trained model is integrated directly into the Flask application for transaction-level inference.

The ML pipeline contains:

Raw Transaction Data
        ↓
Data Preprocessing
        ↓
Feature Engineering
        ↓
Numerical Scaling
        ↓
Categorical Encoding
        ↓
Random Forest Classifier
        ↓
Risk Score
        ↓
Threshold Evaluation
        ↓
Normal / Suspicious


## 5. Risk Scoring

Each analyzed transaction receives a Machine Learning risk score.

Example:

Prediction: Suspicious
Risk Score: 95.21%
Risk Level: High

Risk levels are categorized as:

Risk Score	Risk Level
Below 40%	Low
40% – 69.99%	Medium
70% and above	High

The classification threshold used by the system is:

55%

A transaction with a model score below the classification threshold is classified as Normal, while a transaction meeting or exceeding the threshold is classified as Suspicious.

## 6. ML Analytics Dashboard

The ML Analytics module provides an overview of transaction risk.

It displays:

ML model name
Model version
Number of features
Classification threshold
Transactions analyzed
Normal transactions
Suspicious transactions
Low-risk transactions
Medium-risk transactions
High-risk transactions
High-risk transaction details
Recent ML analysis

Example model information:

Model: Random Forest
Version: v1.0
Features: 24
Threshold: 55%


## 7. Administrative Features

The system includes administrative functionality for managing the banking application.

Administrative features include:

Admin login
Session-based access control
Logout
Customer management
Account management
Transaction management
Loan management
Card management
Employee management
Activity logs
Reports
ML analytics

 ## 8. Activity Logging

Important application activities are recorded through the activity logging module.

For example:

Admin created transaction:
TXN202609031410366806
Deposit
₹2,500
ML: Normal
Risk: 1.28%
Risk Level: Low

This provides traceability between banking operations and Machine Learning analysis.

 ## 9. Real-Time MySQL Logging

The application uses MySQL as its persistent database.

When a transaction is created, the transaction information and ML analysis results are stored in the database.

ML-related fields include:

ml_prediction
ml_risk_score
ml_risk_level
ml_checked_at
ml_model_version

Example:

Transaction ID     : 67
Transaction Type   : Deposit
Amount             : ₹2500.00
ML Prediction      : Normal
Risk Score         : 0.01278
Risk Level         : Low
Model Version      : v1.0

This demonstrates the complete connection between:

Flask
  ↓
MySQL
  ↓
Transaction Processing
  ↓
Machine Learning
  ↓
ML Result Persistence


