USE BankingDB;

-- ==========================================
-- FILE 11 : LOAN MANAGEMENT
-- ==========================================

-- ==========================================
-- Query 1 : View All Loans
-- ==========================================

SELECT
    loan_id,
    loan_number,
    customer_id,
    loan_type,
    loan_amount,
    interest_rate,
    loan_tenure,
    emi,
    loan_status
FROM Loans;

-- ==========================================
-- Query 2 : Approved Loans
-- ==========================================

SELECT *
FROM Loans
WHERE loan_status='Approved';

-- ==========================================
-- Query 3 : Pending Loans
-- ==========================================

SELECT *
FROM Loans
WHERE loan_status='Pending';

-- ==========================================
-- Query 4 : Rejected Loans
-- ==========================================

SELECT *
FROM Loans
WHERE loan_status='Rejected';

-- ==========================================
-- Query 5 : Approve Loan
-- ==========================================

UPDATE Loans
SET loan_status='Approved'
WHERE loan_number='EL100004';

-- ==========================================
-- Query 6 : Reject Loan
-- ==========================================

UPDATE Loans
SET loan_status='Rejected'
WHERE loan_number='HL100005';

-- ==========================================
-- Query 7 : Close Loan
-- ==========================================

UPDATE Loans
SET loan_status='Closed'
WHERE loan_number='PL100003';

-- ==========================================
-- Query 8 : High Value Loans (>10 Lakhs)
-- ==========================================

SELECT
    loan_number,
    loan_type,
    loan_amount,
    loan_status
FROM Loans
WHERE loan_amount > 1000000
ORDER BY loan_amount DESC;

-- ==========================================
-- Query 9 : Total Loan Amount
-- ==========================================

SELECT
    COUNT(*) AS Total_Loans,
    SUM(loan_amount) AS Total_Loan_Amount,
    AVG(loan_amount) AS Average_Loan
FROM Loans;

-- ==========================================
-- Query 10 : Customer Loan Details
-- ==========================================

SELECT

    CONCAT(c.first_name,' ',c.last_name) AS Customer_Name,

    l.loan_number,

    l.loan_type,

    l.loan_amount,

    l.interest_rate,

    l.emi,

    l.loan_status

FROM Customers c

JOIN Loans l

ON c.customer_id=l.customer_id

ORDER BY l.loan_amount DESC;