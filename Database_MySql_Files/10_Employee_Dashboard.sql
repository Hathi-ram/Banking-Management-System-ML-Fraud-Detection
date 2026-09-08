USE BankingDB;

-- ==========================================
-- FILE 10 : EMPLOYEE DASHBOARD
-- ==========================================

-- ==========================================
-- Query 1 : Employee Details
-- ==========================================

SELECT
    e.employee_id,
    CONCAT(e.first_name,' ',e.last_name) AS Employee_Name,
    e.designation,
    e.salary,
    e.hire_date,
    b.branch_name,
    b.city
FROM Employees e
JOIN Branches b
ON e.branch_id = b.branch_id
ORDER BY e.employee_id;

-- ==========================================
-- Query 2 : Employees Working in Each Branch
-- ==========================================

SELECT
    b.branch_name,
    COUNT(e.employee_id) AS Total_Employees
FROM Branches b
LEFT JOIN Employees e
ON b.branch_id = e.branch_id
GROUP BY b.branch_name
ORDER BY Total_Employees DESC;

-- ==========================================
-- Query 3 : Highest Paid Employee
-- ==========================================

SELECT
    CONCAT(e.first_name,' ',e.last_name) AS Employee_Name,
    e.designation,
    e.salary,
    b.branch_name
FROM Employees e
JOIN Branches b
ON e.branch_id = b.branch_id
ORDER BY e.salary DESC
LIMIT 1;

-- ==========================================
-- Query 4 : Employee Salary Report
-- ==========================================

SELECT
    b.branch_name,
    SUM(e.salary) AS Total_Salary,
    ROUND(AVG(e.salary),2) AS Average_Salary,
    MAX(e.salary) AS Highest_Salary,
    MIN(e.salary) AS Lowest_Salary
FROM Employees e
JOIN Branches b
ON e.branch_id = b.branch_id
GROUP BY b.branch_name;

-- ==========================================
-- Query 5 : Customers Handled by Each Branch
-- ==========================================

SELECT
    b.branch_name,
    COUNT(DISTINCT a.customer_id) AS Total_Customers
FROM Branches b
LEFT JOIN Accounts a
ON b.branch_id = a.branch_id
GROUP BY b.branch_name;

-- ==========================================
-- Query 6 : Branch Business Report
-- ==========================================

SELECT
    b.branch_name,
    COUNT(DISTINCT a.account_id) AS Total_Accounts,
    SUM(a.balance) AS Total_Deposits
FROM Branches b
LEFT JOIN Accounts a
ON b.branch_id = a.branch_id
GROUP BY b.branch_name
ORDER BY Total_Deposits DESC;