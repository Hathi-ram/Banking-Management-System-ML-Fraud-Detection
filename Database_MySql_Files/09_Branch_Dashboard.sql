USE BankingDB;

-- ==========================================
-- FILE 09 : BRANCH DASHBOARD
-- ==========================================
# Step 1: Branch Summary Dashboard
SELECT
    b.branch_id,
    b.branch_name,
    b.city,

    COUNT(DISTINCT e.employee_id) AS Total_Employees,

    COUNT(DISTINCT a.customer_id) AS Total_Customers,

    COUNT(DISTINCT a.account_id) AS Total_Accounts,

    IFNULL(SUM(DISTINCT a.balance),0) AS Total_Deposits

FROM Branches b

LEFT JOIN Employees e
ON b.branch_id = e.branch_id

LEFT JOIN Accounts a
ON b.branch_id = a.branch_id

GROUP BY
    b.branch_id,
    b.branch_name,
    b.city

ORDER BY b.branch_id;


# Query 2 : Branch Loan Report

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

# Query 3 : Employees Working in Each Branch
SELECT

    b.branch_name,

    CONCAT(e.first_name,' ',e.last_name) AS Employee_Name,

    e.designation,

    e.salary

FROM Employees e

JOIN Branches b

ON e.branch_id = b.branch_id

ORDER BY b.branch_name;

# Query 4 : Branch-wise Account Balance
SELECT

    b.branch_name,

    COUNT(a.account_id) AS Total_Accounts,

    IFNULL(SUM(a.balance),0) AS Total_Balance

FROM Branches b

LEFT JOIN Accounts a

ON b.branch_id = a.branch_id

GROUP BY b.branch_name

ORDER BY Total_Balance DESC;

# Query 5 : Branch-wise Customers
SELECT

    b.branch_name,

    COUNT(a.customer_id) AS Customers

FROM Branches b

LEFT JOIN Accounts a

ON b.branch_id = a.branch_id

GROUP BY b.branch_name;
