USE BankingDB;

SELECT
    c.customer_id,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    c.phone,
    c.email,
    c.city,

    a.account_number,
    a.account_type,
    a.balance,

    cd.card_type,
    cd.card_status,

    l.loan_type,
    l.loan_amount,
    l.loan_status

FROM Customers c

LEFT JOIN Accounts a
ON c.customer_id = a.customer_id

LEFT JOIN Cards cd
ON a.account_id = cd.account_id

LEFT JOIN Loans l
ON c.customer_id = l.customer_id

ORDER BY c.customer_id;