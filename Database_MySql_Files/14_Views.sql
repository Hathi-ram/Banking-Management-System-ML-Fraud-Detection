USE BankingDB;

-- ==========================================
-- FILE 14 : VIEWS
-- ==========================================

-- ==========================================
-- View 1 : Customer Dashboard
-- ==========================================

CREATE OR REPLACE VIEW Customer_Dashboard_View AS

SELECT

    c.customer_id,

    CONCAT(c.first_name,' ',c.last_name) AS customer_name,

    c.phone,

    c.email,

    c.city,

    a.account_number,

    a.account_type,

    a.balance

FROM Customers c

JOIN Accounts a

ON c.customer_id = a.customer_id;

-- View Data

SELECT * FROM Customer_Dashboard_View;

-- ==========================================
-- View 2 : Transaction Report
-- ==========================================

CREATE OR REPLACE VIEW Transaction_Report_View AS

SELECT

    t.transaction_reference,

    a.account_number,

    t.transaction_type,

    t.amount,

    t.transaction_status,

    t.transaction_date

FROM Transactions t

JOIN Accounts a

ON t.account_id = a.account_id;

SELECT * FROM Transaction_Report_View;

-- ==========================================
-- View 3 : Loan Report
-- ==========================================

CREATE OR REPLACE VIEW Loan_Report_View AS

SELECT

    CONCAT(c.first_name,' ',c.last_name) AS Customer_Name,

    l.loan_number,

    l.loan_type,

    l.loan_amount,

    l.loan_status

FROM Customers c

JOIN Loans l

ON c.customer_id = l.customer_id;

SELECT * FROM Loan_Report_View;

-- ==========================================
-- View 4 : Employee Report
-- ==========================================

CREATE OR REPLACE VIEW Employee_Report_View AS

SELECT

    CONCAT(e.first_name,' ',e.last_name) AS Employee_Name,

    e.designation,

    e.salary,

    b.branch_name

FROM Employees e

JOIN Branches b

ON e.branch_id = b.branch_id;

SELECT * FROM Employee_Report_View;

-- ==========================================
-- View 5 : Branch Summary
-- ==========================================

CREATE OR REPLACE VIEW Branch_Summary_View AS

SELECT

    b.branch_name,

    COUNT(DISTINCT a.account_id) AS Total_Accounts,

    IFNULL(SUM(a.balance),0) AS Total_Deposits

FROM Branches b

LEFT JOIN Accounts a

ON b.branch_id = a.branch_id

GROUP BY b.branch_name;

SELECT * FROM Branch_Summary_View;


SHOW FULL TABLES
WHERE TABLE_TYPE='VIEW';


SELECT * FROM Customer_Dashboard_View;

SELECT * FROM Transaction_Report_View;

SELECT * FROM Loan_Report_View;

SELECT * FROM Employee_Report_View;

SELECT * FROM Branch_Summary_View;