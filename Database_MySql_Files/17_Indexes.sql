USE bankingdb;

-- ==========================================
-- FILE 17 : INDEXES
-- ==========================================

-- ==========================================
-- Customer Indexes
-- ==========================================

CREATE INDEX idx_customer_email
ON Customers(email);

CREATE INDEX idx_customer_phone
ON Customers(phone);

-- ==========================================
-- Account Indexes
-- ==========================================

CREATE INDEX idx_account_number
ON Accounts(account_number);

CREATE INDEX idx_account_customer
ON Accounts(customer_id);

CREATE INDEX idx_account_branch
ON Accounts(branch_id);

-- ==========================================
-- Transaction Indexes
-- ==========================================

CREATE INDEX idx_transaction_reference
ON Transactions(transaction_reference);

CREATE INDEX idx_transaction_account
ON Transactions(account_id);

CREATE INDEX idx_transaction_date
ON Transactions(transaction_date);

-- ==========================================
-- Loan Indexes
-- ==========================================

CREATE INDEX idx_loan_number
ON Loans(loan_number);

CREATE INDEX idx_loan_customer
ON Loans(customer_id);

-- ==========================================
-- Card Indexes
-- ==========================================

CREATE INDEX idx_card_number
ON Cards(card_number);

CREATE INDEX idx_card_account
ON Cards(account_id);

-- ==========================================
-- Employee Indexes
-- ==========================================

CREATE INDEX idx_employee_branch
ON Employees(branch_id);

-- ==========================================
-- Show All Indexes
-- ==========================================

SHOW INDEX FROM Customers;

SHOW INDEX FROM Accounts;

SHOW INDEX FROM Transactions;

SHOW INDEX FROM Loans;

SHOW INDEX FROM Cards;

SHOW INDEX FROM Employees;


# Test Query Performance

# Run these queries to use the indexes:

SELECT *
FROM Accounts
WHERE account_number='SB100001';

SELECT *
FROM Customers
WHERE email='rahul@gmail.com';

SELECT *
FROM Transactions
WHERE transaction_reference='TXN100001';

SELECT *
FROM Loans
WHERE loan_number='HL100001';

SELECT *
FROM Cards
WHERE card_number='4111111111111111';

# You can also check whether MySQL uses an index:

EXPLAIN
SELECT *
FROM Accounts
WHERE account_number='SB100001';


SHOW INDEX FROM Customers;
SHOW INDEX FROM Accounts;
SHOW INDEX FROM Transactions;
SHOW INDEX FROM Loans;
SHOW INDEX FROM Cards;
SHOW INDEX FROM Employees;