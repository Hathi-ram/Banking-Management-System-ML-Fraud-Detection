USE BankingDB;

-- ==========================================
-- FILE 06 : DEPOSIT MONEY
-- ==========================================

START TRANSACTION;

-- Step 1 : Insert Deposit Transaction
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
    'TXN200001',
    1,
    'Deposit',
    10000.00,
    'Success',
    'Cash Deposit'
);

-- Step 2 : Update Account Balance
UPDATE Accounts
SET balance = balance + 10000.00
WHERE account_id = 'SB100001';

-- Step 3 : Save Changes
COMMIT;

-- ==========================================
-- Verify Updated Account
-- ==========================================

SELECT
    account_id,
    account_number,
    balance
FROM Accounts
WHERE account_id = 1;

-- ==========================================
-- Verify Latest Transaction
-- ==========================================

SELECT
    transaction_reference,
    transaction_type,
    amount,
    transaction_status,
    transaction_date
FROM Transactions
WHERE account_id = 1
ORDER BY transaction_date DESC;