USE BankingDB;

-- ==========================================
-- FILE 08 : TRANSFER MONEY
-- ==========================================

START TRANSACTION;

-- Step 1 : Check Sender Account
SELECT account_id, account_number, balance
FROM Accounts
WHERE account_id = 1;

-- Step 2 : Check Receiver Account
SELECT account_id, account_number, balance
FROM Accounts
WHERE account_id = 2;

-- Step 3 : Debit Sender Account
UPDATE Accounts
SET balance = balance - 10000.00
WHERE account_id = 1
AND balance >= 10000.00;

-- Step 4 : Credit Receiver Account
UPDATE Accounts
SET balance = balance + 10000.00
WHERE account_id = 2;

-- Step 5 : Record Debit Transaction
INSERT INTO Transactions
(
    transaction_reference,
    account_id,
    transaction_type,
    amount,
    transaction_status,
    remarks
)
VALUES
(
    'TXN200003',
    1,
    'Transfer',
    10000.00,
    'Success',
    'Transferred to Account 2'
);

-- Step 6 : Record Credit Transaction
INSERT INTO Transactions
(
    transaction_reference,
    account_id,
    transaction_type,
    amount,
    transaction_status,
    remarks
)
VALUES
(
    'TXN200004',
    2,
    'Deposit',
    10000.00,
    'Success',
    'Received from Account 1'
);

-- Step 7 : Commit Transaction
COMMIT;

-- ==========================================
-- Verify Updated Balances
-- ==========================================

SELECT
    account_id,
    account_number,
    balance
FROM Accounts
WHERE account_id IN (1,2);

-- ==========================================
-- Verify Transactions
-- ==========================================

SELECT
    transaction_reference,
    account_id,
    transaction_type,
    amount,
    transaction_status,
    transaction_date
FROM Transactions
WHERE account_id IN (1,2)
ORDER BY transaction_date DESC;