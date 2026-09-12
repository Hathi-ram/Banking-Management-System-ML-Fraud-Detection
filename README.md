# 🏦 Banking Management System with Machine Learning Fraud Detection

A full-stack **Banking Management System** built with **Flask, Python, MySQL, and Scikit-Learn**, integrated with a **Random Forest-based Machine Learning fraud detection module**.

The system manages core banking operations such as customers, accounts, deposits, withdrawals, transfers, loans, cards, employees, reports, and activity logs while automatically analyzing transactions and generating **fraud predictions, risk scores, and risk levels**.

---

## 🛠️ Tech Stack

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

# 📌 Problem Statement

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

```text
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
