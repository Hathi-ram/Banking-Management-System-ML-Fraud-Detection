#### Banking Management System with Machine Learning Fraud Detection

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

# 💡 Solution Overview

This project combines a complete **Banking Management System** with an integrated **Machine Learning-based transaction fraud detection module**.

The application provides normal banking operations through a Flask web interface while automatically sending transaction information to a trained Machine Learning model.

The system follows this workflow:

User
 │
 ▼
Banking Web Interface
 │
 ▼
Flask Backend
 │
 ├───────────────► MySQL Database
 │
 ▼
Transaction Feature Generation
 │
 ▼
ML Fraud Detection Model
 │
 ▼
Risk Score
 │
 ▼
Normal / Suspicious
 │
 ▼
Risk Level
 │
 ▼
Store ML Result in MySQL
 │
 ▼
Dashboard / ML Analytics / Reports


The Machine Learning module uses a Random Forest Classifier to analyze transaction-related features and produce:

Fraud/suspicious prediction
Risk score
Risk percentage
Risk level
ML model version
ML analysis timestamp

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

Transaction Created
        ↓
Feature Generation
        ↓
ML Model
        ↓
Fraud Prediction
        ↓
Risk Score
        ↓
Risk Level
        ↓
Database Storage

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

### Methodology & System Architecture

## 1. Overall System Architecture

The complete application follows a full-stack architecture where the user interacts with the Flask web application.

Transaction information is processed by the backend, analyzed by the Machine Learning model, and stored in MySQL.

System Architecture Diagram

Figure 1: Overall system architecture showing User/UI → Flask Backend → ML Inference Pipeline → MySQL Database.

The system can operate with a local MySQL database for development and can be adapted to a cloud-hosted MySQL database for deployment.

## 2. Machine Learning Methodology

The Machine Learning workflow consists of several stages.

Step 1 — Transaction Data

Historical transaction data is used for training the fraud detection model.

Step 2 — Data Preprocessing

The data is cleaned and prepared for Machine Learning.

Step 3 — Feature Engineering

Additional behavioral features are generated, including:

Amount-to-Average Ratio
Amount Z-Score
Amount Deviation
Hour
Day of Week
Weekend Indicator
Account Transaction Count
Step 4 — Encoding

Categorical transaction fields are converted into numerical representations using categorical encoding.

Step 5 — Scaling

Numerical features are standardized using a scaler.

Step 6 — Model Training

A Random Forest Classifier is trained using the processed transaction dataset.

Step 7 — Threshold Evaluation

The model probability is evaluated against the configured classification threshold.

Risk Score >= 55%
        ↓
Suspicious

Risk Score < 55%
        ↓
Normal
Step 8 — Real-Time Inference

When a new transaction is created, the same feature-generation and preprocessing pipeline is applied before the transaction is passed to the trained model.

Step 9 — Persistence

The prediction, risk score, risk level, model version, and analysis timestamp are stored in MySQL.

ML Model Training & Inference Workflow

Figure 2: Machine Learning workflow from preprocessing and feature engineering to Random Forest prediction, threshold evaluation, and real-time inference.

##  3. Database Architecture

The MySQL database stores the main banking entities and their relationships.

Major entities include:

Customers
Accounts
Transactions
Employees
Loans
Cards
Activity Logs
ML Fraud Logs / ML transaction results

The major relationship is:

Customer
   │
   └── Accounts
          │
          └── Transactions
                   │
                   └── ML Fraud Analysis
Entity-Relationship Diagram

Figure 3: Entity-Relationship diagram showing the relationships between Customers, Accounts, Transactions, Employees, and ML fraud analysis records.

##  Screenshots & UI Showcase

The following screenshots demonstrate the working application.

## Banking Dashboard

Figure 4: Main banking dashboard showing banking statistics, transaction information, and ML fraud detection summary.

## ML Fraud Detection

Figure 5: Transaction analysis showing ML prediction, risk score, and risk level.

Example:

Prediction : Suspicious
Risk Score : 95.21%
Risk Level : High

##  MySQL Workbench

Figure 6: MySQL Workbench showing transaction records and stored Machine Learning prediction and risk information.

## ML Analytics Report

Figure 7: ML Analytics dashboard showing analyzed transactions, risk distribution, and high-risk transactions.

### Project Structure

Banking-Management-System-ML-Fraud-Detection/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── models/
│   └── database.py
│
├── routes/
│   ├── customer.py
│   ├── account.py
│   ├── transaction.py
│   ├── loan.py
│   ├── card.py
│   ├── employee.py
│   ├── activity.py
│   └── admin.py
│
├── ml_service/
│   ├── __init__.py
│   ├── fraud_detector.py
│   ├── fraud_model.pkl
│   ├── scaler.pkl
│   ├── encoder.pkl
│   ├── feature_columns.pkl
│   └── threshold.pkl
│
├── templates/
│   ├── login.html
│   ├── dashboard.html
│   ├── customers.html
│   ├── accounts.html
│   ├── transactions.html
│   ├── loans.html
│   ├── cards.html
│   ├── employees.html
│   ├── reports.html
│   └── ml_analytics.html
│
├── static/
│   ├── css/
│   └── js/
│
└── docs/
    ├── system_architecture.png
    ├── ml_pipeline.png
    ├── er_diagram.png
    ├── dashboard_preview.png
    ├── ml_fraud_detection.png
    ├── ml_analytics_report.png
    └── mysql_workbench_proof.png


## 3.Installation & Local Setup

## 1. Clone the Repository
git clone https://github.com/YOUR_USERNAME/Banking-Management-System-ML-Fraud-Detection.git

Move into the project directory:
cd Banking-Management-System-ML-Fraud-Detection

## 2. Create a Virtual Environment
Windows
python -m venv venv

Activate it:

venv\Scripts\activate
Linux / macOS
python3 -m venv venv

Activate it:

source venv/bin/activate

## 4.Configure MySQL

Install and open MySQL Server and MySQL Workbench.

Create the database:

CREATE DATABASE BankingDB;

Select the database:

USE BankingDB;

Create the required banking tables according to the database schema included with the project.

The database contains entities for:

Customers
Accounts
Transactions
Loans
Cards
Employees
Activity Logs

##5. Configure Database Credentials

Configure the MySQL connection using environment variables rather than committing passwords to GitHub.

## 6. Run the Application

Start the Flask application:

python app.py

The application will normally be available at:

http://127.0.0.1:5000

Open the URL in a web browser.

## 7. Test the Application

After starting the application, test the following workflow:

Login
  ↓
Dashboard
  ↓
Customer Management
  ↓
Account Management
  ↓
Deposit / Withdrawal / Transfer
  ↓
Transaction Analysis
  ↓
ML Fraud Detection
  ↓
Risk Score
  ↓
Normal / Suspicious
  ↓
ML Analytics
  ↓
Reports

Verify the corresponding records in MySQL Workbench.

##  Machine Learning Model Performance

The Random Forest model was evaluated using a held-out test dataset.

The obtained evaluation metrics were:

Metric	Score
Accuracy	98.0%
Precision	76.0%
Recall	47.0%
F1-Score	58.0%

These metrics represent the model's evaluation on the held-out test set.

The system uses a 55% operational classification threshold for determining whether a transaction is classified as Normal or Suspicious.

Note: Overall accuracy should not be interpreted as "98% fraud detection accuracy." Fraud-class precision, recall, and F1-score provide additional information about suspicious transaction detection performance.

## Deployment

The application is designed to run locally using Flask and MySQL.

For cloud deployment, the Flask application can be hosted on a cloud platform and connected to a cloud-accessible MySQL database.

The local development architecture is:

Browser
   ↓
Flask Application
   ↓
Local MySQL
   ↓
Machine Learning Model

## Project Demonstration

A complete end-to-end demonstration video can be provided to show:

Admin login
Banking dashboard
Customer management
Account management
Deposit
Withdrawal
Transfer
Transaction history
ML fraud detection
Risk score generation
Suspicious transaction detection
ML analytics
Reports
MySQL Workbench database updates

## Security Considerations

For production deployment, the following improvements should be applied:

Store credentials in environment variables
Use secure password hashing
Enable HTTPS
Use secure session configuration
Apply database access restrictions
Validate and sanitize user inputs
Use appropriate database permissions
Avoid exposing sensitive banking information
Secure ML model files and configuration
Use a production WSGI server

## Future Enhancements

Possible future improvements include:

Cloud deployment
Advanced fraud detection models
Real-time alerts
Email/SMS notifications
Improved fraud investigation tools
More advanced customer behavior analysis
Model retraining pipeline
Authentication improvements
Role-based access control
API integration

## Project Summary

This project demonstrates the integration of full-stack web development, relational database management, and Machine Learning in a banking use case.

The system combines:

Python
+
Flask
+
MySQL
+
Scikit-Learn
+
Random Forest
+
Pandas
+
HTML/CSS
+
Bootstrap

into a single end-to-end application.

The main contribution of the project is the integration of a Machine Learning transaction risk assessment pipeline directly into the banking transaction workflow, allowing transactions to be analyzed and classified as Normal or Suspicious with an associated risk score and risk level.

## Key Technologies

Python
Flask
MySQL
Scikit-Learn
Random Forest
Pandas
NumPy
HTML5
CSS3
Bootstrap
Chart.js
MySQL Workbench

## License

This project is currently provided for educational and portfolio purposes.


### One correction before you upload this README

Your requested architecture diagram says **"Cloud/Local MySQL DB."** Since you decided to demonstrate the project locally rather than provide a live URL, I deliberately worded the README so it **doesn't falsely claim that your application is currently deployed in the cloud**.

Also, I included `ml_analytics_report.png` as a fourth screenshot because your README requirements mention the ML analytics report. You should create that screenshot and put it inside:

```text
docs/

So your final docs folder should contain:

docs/
├── system_architecture.png
├── ml_pipeline.png
├── er_diagram.png
├── dashboard_preview.png
├── ml_fraud_detection.png
├── ml_analytics_report.png
└── mysql_workbench_proof.png
