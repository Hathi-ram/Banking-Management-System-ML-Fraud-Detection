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
## Complete End-to-End System Workflow

## <img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/9119b1bd-4d98-48bc-8fe5-ee8381bdbace" />


## Key Features & Capabilities
##  1. Customer Management

## <img width="386" height="1212" alt="Customer List_page" src="https://github.com/user-attachments/assets/03a847c4-8478-498f-9948-5676cf18d010" />

The Customer Management module allows administrators to:

- Add customers
- View customer details
- Update customer information
- Delete customer records
- Search customers
- Manage customer-related banking information

Customer information is stored securely in the MySQL database.

## Customer Management Workflow
Admin Login
     │
     ▼
Customer Management
     │
     ├── Add Customer
     │
     ├── View Customer
     │
     ├── Search Customer
     │
     ├── Update Customer
     │
     └── Delete Customer
              │
              ▼
        MySQL Customers
              │
              ▼
       Customer ID Created

## 2. Account Management

## <img width="2384" height="1134" alt="Account_Page" src="https://github.com/user-attachments/assets/00a86283-b1bc-4716-9d9a-2f9c104e76bb" />


The Account Management module provides:

- Account creation
- Savings and Current account support
- Account balance management
- Account status tracking
- Customer-account relationship management
- Account search and viewing

Each account is linked to its respective customer.

## 3. Transaction Management

The system supports major banking transactions:

 Deposit
 
- Allows money to be deposited into a customer account.

Withdrawal

- Allows money to be withdrawn while checking the available account balance.

Transfer

- Allows money to be transferred between accounts.

Transaction History

- All transactions are recorded and can be searched and reviewed.

Supported transaction types include:

- Deposit
- Withdrawal
- Transfer
- UPI
- NEFT
- RTGS
- IMPS

## 4. Machine Learning Fraud Detection

## <img width="2880" height="1420" alt="Machine_Learning_page" src="https://github.com/user-attachments/assets/45f0dd34-25b8-4bbb-ba69-f79983bb55e2" />


The major feature of this project is the integrated Machine Learning fraud detection module.

- Whenever a new transaction is created:

- The model analyzes transaction characteristics such as:

- Transaction amount
- Transaction hour
- Day of week
- Day of month
- Month
- Weekend information
- Account average transaction amount
- Account standard deviation
- Account transaction count
- Amount deviation
- Amount-to-average ratio
- Amount z-score
- Transaction type
- Transaction status

## Random Forest Model

The project uses a Random Forest Classifier for transaction classification.

The model uses transaction and account-behavior features to estimate the likelihood that a transaction is suspicious.

- Feature categories
- Transaction Features
- Amount
- Transaction type
- Transaction status
- Transaction hour
- Day of week
- Day of month
- Month
- Weekend indicator
- Account Behavioral Features
- Account average transaction amount
- Account standard deviation
- Account transaction count
- Amount deviation
- Amount-to-average ratio
- Amount z-score
- Encoded Features

Categorical values are converted into numerical features before being passed to the model.


## 5. Risk Scoring

The system generates two related outputs.

- Transaction Classification
  
- ML Score	Classification
- < 55%	Normal
- >= 55%	Suspicious

- Risk Level
- 
- Risk Score	Risk Level
- < 40%	Low
- 40% – 69.99%	Medium
- >= 70%	High



## 6. ML Analytics Dashboard

The ML Analytics module provides an overview of transaction risk.

It displays:

- ML model name
- Model version
- Number of features
- Classification threshold
- Transactions analyzed
- Normal transactions
- Suspicious transactions
- Low-risk transactions
- Medium-risk transactions
- High-risk transactions
- High-risk transaction details
- Recent ML analysis


## 7. Administrative Features

## <img width="674" height="1504" alt="Banking Activity Log_page" src="https://github.com/user-attachments/assets/16f900f1-13a6-43b6-b50c-077c33db54bb" />


The system includes administrative functionality for managing the banking application.

Administrative features include:

- Admin login
- Session-based access control
- Logout
- Customer management
- Account management
- Transaction management
- Loan management
- Card management
- Employee management
- Activity logs
- Reports
- ML analytics

 ## 8. Activity Logging

 ## <img width="2874" height="1528" alt="Admin_Login_page" src="https://github.com/user-attachments/assets/40c73f06-a86e-40e1-bb22-e1e4f099b91f" />

Important application activities are recorded through the activity logging module.

This provides traceability between banking operations and Machine Learning analysis.

 ## 9. Real-Time MySQL Logging

The application uses MySQL as its persistent database.

When a transaction is created, the transaction information and ML analysis results are stored in the database.

ML-related fields include:

- ml_prediction
- ml_risk_score
- ml_risk_level
- ml_checked_at
- ml_model_version

## 10.LOAN 

## <img width="586" height="1516" alt="Loan List_page" src="https://github.com/user-attachments/assets/f0aa1689-e3a0-43d7-8ec4-bdd933b6f8eb" />

## 11. CARD
## <img width="430" height="1268" alt="Card List_page" src="https://github.com/user-attachments/assets/bfa5bb48-53e4-4bea-acb9-e494a9ac78d0" />

## 12.Employees

## <img width="728" height="1388" alt="Employee List_page" src="https://github.com/user-attachments/assets/72f630e2-b448-42ac-b2f3-1c416893a9be" />

