USE BankingDB;

-- ==========================================
-- FILE 13 : BUSINESS REPORTS
-- ==========================================

-- ==========================================
-- Report 1 : Top 5 Customers by Account Balance
-- ==========================================

SELECT
    CONCAT(c.first_name,' ',c.last_name) AS Customer_Name,
    a.account_number,
    a.balance
FROM Customers c
JOIN Accounts a
ON c.customer_id = a.customer_id
ORDER BY a.balance DESC
LIMIT 5;

-- ==========================================
-- Report 2 : Branch-wise Total Deposits
-- ==========================================

SELECT
    b.branch_name,
    COUNT(a.account_id) AS Total_Accounts,
    IFNULL(SUM(a.balance),0) AS Total_Deposits
FROM Branches b
LEFT JOIN Accounts a
ON b.branch_id = a.branch_id
GROUP BY b.branch_name
ORDER BY Total_Deposits DESC;

-- ==========================================
-- Report 3 : Branch-wise Loan Amount
-- ==========================================

SELECT
    b.branch_name,
    COUNT(l.loan_id) AS Total_Loans,
    IFNULL(SUM(l.loan_amount),0) AS Total_Loan_Amount
FROM Branches b
LEFT JOIN Accounts a
ON b.branch_id = a.branch_id
LEFT JOIN Loans l
ON a.customer_id = l.customer_id
GROUP BY b.branch_name
ORDER BY Total_Loan_Amount DESC;

-- ==========================================
-- Report 4 : Transaction Summary
-- ==========================================

SELECT
    transaction_type,
    COUNT(*) AS Total_Transactions,
    SUM(amount) AS Total_Amount
FROM Transactions
GROUP BY transaction_type
ORDER BY Total_Amount DESC;

-- ==========================================
-- Report 5 : Highest Loan Customer
-- ==========================================

SELECT
    CONCAT(c.first_name,' ',c.last_name) AS Customer_Name,
    l.loan_number,
    l.loan_amount
FROM Customers c
JOIN Loans l
ON c.customer_id = l.customer_id
ORDER BY l.loan_amount DESC
LIMIT 1;

-- ==========================================
-- Report 6 : Highest Paid Employee
-- ==========================================

SELECT
    CONCAT(first_name,' ',last_name) AS Employee_Name,
    designation,
    salary
FROM Employees
ORDER BY salary DESC
LIMIT 1;

-- ==========================================
-- Report 7 : Card Type Summary
-- ==========================================

SELECT
    card_type,
    COUNT(*) AS Total_Cards
FROM Cards
GROUP BY card_type;

-- ==========================================
-- Report 8 : Active vs Blocked Cards
-- ==========================================

SELECT
    card_status,
    COUNT(*) AS Total
FROM Cards
GROUP BY card_status;

-- ==========================================
-- Report 9 : Customers Having Loans
-- ==========================================

SELECT
    CONCAT(c.first_name,' ',c.last_name) AS Customer_Name,
    l.loan_type,
    l.loan_amount
FROM Customers c
JOIN Loans l
ON c.customer_id = l.customer_id
ORDER BY Customer_Name;

-- ==========================================
-- Report 10 : Customers with Highest Total Balance
-- ==========================================

SELECT
    CONCAT(c.first_name,' ',c.last_name) AS Customer_Name,
    SUM(a.balance) AS Total_Balance
FROM Customers c
JOIN Accounts a
ON c.customer_id = a.customer_id
GROUP BY c.customer_id
ORDER BY Total_Balance DESC;