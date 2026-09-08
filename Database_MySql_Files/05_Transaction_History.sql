USE BankingDB;

-- ==========================================
-- TRANSACTION HISTORY
-- ==========================================

SELECT
    t.transaction_reference,
    a.account_number,
    t.transaction_type,
    t.amount,
    t.transaction_status,
    t.transaction_date,
    t.remarks

FROM Transactions t

JOIN Accounts a
ON t.account_id = a.account_id

ORDER BY t.transaction_date DESC;


# Search transactions of one account
SELECT
    t.transaction_reference,
    a.account_number,
    t.transaction_type,
    t.amount,
    t.transaction_status,
    t.transaction_date

FROM Transactions t

JOIN Accounts a
ON t.account_id = a.account_id

WHERE a.account_number='SB100001';