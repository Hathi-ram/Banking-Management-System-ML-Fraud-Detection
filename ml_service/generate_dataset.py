# ============================================================
# Banking Transaction ML Dataset Generator
# Fraud / Anomaly Detection Project
# ============================================================

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta


# ============================================================
# Configuration
# ============================================================

NUM_TRANSACTIONS = 10000
NUM_ACCOUNTS = 500

random.seed(42)
np.random.seed(42)


# ============================================================
# Transaction Categories
# ============================================================

transaction_types = [
    "Deposit",
    "Withdrawal",
    "Transfer",
    "UPI",
    "NEFT",
    "RTGS",
    "IMPS"
]

transaction_statuses = [
    "Success",
    "Pending",
    "Failed"
]


# ============================================================
# Generate Account Profiles
# ============================================================

accounts = []

for account_id in range(1, NUM_ACCOUNTS + 1):

    # Normal average transaction amount for each account
    average_amount = np.random.uniform(
        500,
        25000
    )

    accounts.append({
        "account_id": account_id,
        "average_amount": average_amount
    })


# ============================================================
# Generate Transactions
# ============================================================

transactions = []

start_date = datetime(
    2025,
    1,
    1
)


for transaction_id in range(
    1,
    NUM_TRANSACTIONS + 1
):

    account = random.choice(accounts)

    account_id = account["account_id"]

    normal_amount = account["average_amount"]


    # --------------------------------------------------------
    # Transaction Type
    # --------------------------------------------------------

    transaction_type = random.choices(

        transaction_types,

        weights=[
            30,   # Deposit
            20,   # Withdrawal
            15,   # Transfer
            15,   # UPI
            8,    # NEFT
            5,    # RTGS
            7     # IMPS
        ]

    )[0]


    # --------------------------------------------------------
    # Normal Transaction Amount
    # --------------------------------------------------------

    amount = np.random.lognormal(

        mean=np.log(normal_amount),

        sigma=0.55
    )

    amount = max(
        100,
        round(float(amount), 2)
    )


    # --------------------------------------------------------
    # Transaction Date
    # --------------------------------------------------------

    transaction_date = (

        start_date
        +
        timedelta(
            minutes=random.randint(
                0,
                60 * 24 * 365
            )
        )

    )


    # --------------------------------------------------------
    # Transaction Status
    # --------------------------------------------------------

    transaction_status = random.choices(

        transaction_statuses,

        weights=[
            92,     # Success
            5,      # Pending
            3       # Failed
        ]

    )[0]


    # --------------------------------------------------------
    # Remarks
    # --------------------------------------------------------

    remarks = "Normal transaction"


    # --------------------------------------------------------
    # Store Transaction
    # --------------------------------------------------------

    transactions.append({

        "transaction_id":
            transaction_id,

        "transaction_reference":
            f"TXN{transaction_id:08d}",

        "account_id":
            account_id,

        "transaction_type":
            transaction_type,

        "amount":
            amount,

        "transaction_date":
            transaction_date,

        "transaction_status":
            transaction_status,

        "remarks":
            remarks
    })


# ============================================================
# Convert to DataFrame
# ============================================================

df = pd.DataFrame(
    transactions
)


# ============================================================
# Convert Date Column
# ============================================================

df["transaction_date"] = pd.to_datetime(
    df["transaction_date"]
)


# ============================================================
# Feature Engineering
# ============================================================

# Transaction hour
df["hour"] = (
    df["transaction_date"]
    .dt.hour
    .astype("int64")
)


# Day of week
df["day_of_week"] = (
    df["transaction_date"]
    .dt.dayofweek
    .astype("int64")
)


# Day of month
df["day_of_month"] = (
    df["transaction_date"]
    .dt.day
    .astype("int64")
)


# Month
df["month"] = (
    df["transaction_date"]
    .dt.month
    .astype("int64")
)


# Weekend indicator
df["is_weekend"] = (
    df["day_of_week"] >= 5
).astype("int64")


# ============================================================
# Account-Level Statistics
# ============================================================

account_stats = (

    df
    .groupby("account_id")["amount"]
    .agg(

        account_average_amount="mean",

        account_std_amount="std",

        account_transaction_count="count"

    )
    .reset_index()
)


# ============================================================
# Merge Account Statistics
# ============================================================

df = df.merge(

    account_stats,

    on="account_id",

    how="left"
)


# ============================================================
# Handle Missing Standard Deviation
# ============================================================

df["account_std_amount"] = (

    df["account_std_amount"]
    .fillna(0)
)


# ============================================================
# Amount Deviation
# ============================================================

df["amount_deviation"] = np.where(

    df["account_std_amount"] > 0,

    (
        abs(
            df["amount"]
            -
            df["account_average_amount"]
        )
        /
        df["account_std_amount"]
    ),

    0

)


# ============================================================
# Create Anomaly Label
# ============================================================

# Approximately 3% anomalies
num_anomalies = int(
    NUM_TRANSACTIONS * 0.03
)


anomaly_indices = np.random.choice(

    df.index,

    size=num_anomalies,

    replace=False
)


df["is_anomaly"] = 0


df.loc[
    anomaly_indices,
    "is_anomaly"
] = 1


# ============================================================
# Anomaly Type 1
# Unusually Large Transactions
# ============================================================

large_count = int(
    num_anomalies * 0.5
)


large_indices = anomaly_indices[
    :large_count
]


large_multiplier = np.random.uniform(

    5,

    15,

    size=len(large_indices)

)


df.loc[
    large_indices,
    "amount"
] = (

    df.loc[
        large_indices,
        "amount"
    ].astype(float)

    *

    large_multiplier
)


# ============================================================
# Anomaly Type 2
# Unusual Transaction Time
# ============================================================

time_indices = anomaly_indices[
    large_count:
]


# Ensure compatible integer dtype
df["hour"] = (
    df["hour"]
    .astype("int64")
)


unusual_hours = np.random.choice(

    [
        0,
        1,
        2,
        3,
        4
    ],

    size=len(time_indices)

).astype("int64")


df.loc[
    time_indices,
    "hour"
] = unusual_hours


# ============================================================
# Recalculate Amount Deviation
# ============================================================

df["amount_deviation"] = np.where(

    df["account_std_amount"] > 0,

    (
        abs(
            df["amount"]
            -
            df["account_average_amount"]
        )
        /
        df["account_std_amount"]
    ),

    0

)


# ============================================================
# Add Anomaly Remarks
# ============================================================

df.loc[
    large_indices,
    "remarks"
] = "Unusually large transaction"


df.loc[
    time_indices,
    "remarks"
] = "Unusual transaction time"


# ============================================================
# Final Data Cleaning
# ============================================================

df["amount"] = (
    df["amount"]
    .round(2)
)


df["account_average_amount"] = (
    df["account_average_amount"]
    .round(2)
)


df["account_std_amount"] = (
    df["account_std_amount"]
    .round(2)
)


df["amount_deviation"] = (
    df["amount_deviation"]
    .round(4)
)


# ============================================================
# Reorder Columns
# ============================================================

df = df[

    [

        "transaction_id",

        "transaction_reference",

        "account_id",

        "transaction_type",

        "amount",

        "transaction_date",

        "transaction_status",

        "remarks",

        "hour",

        "day_of_week",

        "day_of_month",

        "month",

        "is_weekend",

        "account_average_amount",

        "account_std_amount",

        "account_transaction_count",

        "amount_deviation",

        "is_anomaly"

    ]

]


# ============================================================
# Save Dataset
# ============================================================

output_file = "transactions_ml.csv"


df.to_csv(

    output_file,

    index=False

)


# ============================================================
# Dataset Summary
# ============================================================

print()
print("==============================================")
print("     ML DATASET CREATED SUCCESSFULLY")
print("==============================================")

print()

print(
    f"Total transactions : {len(df)}"
)

print(
    f"Number of accounts : "
    f"{df['account_id'].nunique()}"
)

print()

print(
    f"Normal transactions : "
    f"{(df['is_anomaly'] == 0).sum()}"
)

print(
    f"Anomalous transactions : "
    f"{(df['is_anomaly'] == 1).sum()}"
)

print()

print("Transaction Type Distribution")
print("----------------------------------------------")

print(
    df["transaction_type"]
    .value_counts()
)

print()

print("Transaction Status Distribution")
print("----------------------------------------------")

print(
    df["transaction_status"]
    .value_counts()
)

print()

print("Dataset Shape")
print("----------------------------------------------")

print(
    df.shape
)

print()

print("Dataset Columns")
print("----------------------------------------------")

for column in df.columns:

    print(
        f"- {column}"
    )

print()

print("Dataset saved as:")
print(
    output_file
)

print()

print("==============================================")
print("             GENERATION COMPLETE")
print("==============================================")