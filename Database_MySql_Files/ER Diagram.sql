                              +----------------------+
                              |      Branches        |
                              +----------------------+
                              | branch_id (PK)       |
                              | branch_name          |
                              | branch_code          |
                              | city                 |
                              | state                |
                              +----------+-----------+
                                         |
                        One Branch has Many Accounts
                                         |
                                         |
                                         v
+----------------------+        +-----------------------+
|      Customers       |        |       Accounts        |
+----------------------+        +-----------------------+
| customer_id (PK)     |<------>| account_id (PK)       |
| first_name           |        | account_number        |
| last_name            |        | customer_id (FK)      |
| gender               |        | branch_id (FK)        |
| dob                  |        | account_type          |
| phone                |        | balance               |
| email                |        | account_status        |
| city                 |        | open_date             |
+----------+-----------+        +-----------+-----------+
           |                                |
           |                                |
           |                                |
           |                                |
           |                                |
           |                                |
           |                     +----------+----------+
           |                     |                     |
           |                     |                     |
           |                     |                     |
           |                     |                     |
           |                     |                     |
           |                     v                     v
           |          +------------------+     +------------------+
           |          |   Transactions   |     |      Cards       |
           |          +------------------+     +------------------+
           |          | transaction_id   |     | card_id          |
           |          | transaction_ref  |     | card_number      |
           |          | account_id (FK)  |     | account_id (FK)  |
           |          | transaction_type |     | card_type        |
           |          | amount           |     | issue_date       |
           |          | transaction_date |     | expiry_date      |
           |          | transaction_status|    | cvv              |
           |          | remarks          |     | card_status      |
           |          +------------------+     +------------------+
           |
           |
           |
           |
           |
           v
+----------------------+
|        Loans         |
+----------------------+
| loan_id (PK)         |
| loan_number          |
| customer_id (FK)     |
| loan_type            |
| loan_amount          |
| interest_rate        |
| loan_tenure          |
| emi                  |
| loan_status          |
| start_date           |
| end_date             |
+----------------------+




+----------------------+
|     Employees        |
+----------------------+
| employee_id (PK)     |
| branch_id (FK)       |
| first_name           |
| last_name            |
| designation          |
| salary               |
| hire_date            |
+----------+-----------+
           |
           |
           |
           v
      Branches