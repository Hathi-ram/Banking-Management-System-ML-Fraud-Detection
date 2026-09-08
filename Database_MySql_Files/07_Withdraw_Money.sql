USE BankingDB;

-- ==========================================
-- FILE 07 : WITHDRAW MONEY
-- ==========================================

START TRANSACTION;

-- Step 1 : Check Current Balance
SELECT
    account_id,
    account_number,
    balance
FROM Accounts
WHERE account_id = 1;

-- Step 2 : Withdraw Money
UPDATE Accounts
SET balance = balance - 5000.00
WHERE account_id = 'SB100001'
AND balance >= 5000.00;

-- Step 3 : Record the Transaction
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
    'TXN200002',
    1,
    'Withdrawal',
    5000.00,
    'Success',
    'ATM Cash Withdrawal'
);

-- Step 4 : Save Changes
COMMIT;

-- ==========================================
-- Verify Updated Balance
-- ==========================================

SELECT
    account_id,
    account_number,
    balance
FROM Accounts
WHERE account_id = 1;

-- ==========================================
-- View Latest Transactions
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