USE BankingDB;

#Customers
INSERT INTO Customers
(first_name,last_name,gender,dob,phone,email,
aadhaar_number,pan_number,address,city,state,pincode)
VALUES

('Rahul','Sharma','Male','1998-05-10',
'9876543210',
'rahul@gmail.com',
'123456789012',
'ABCDE1234F',
'Madhapur',
'Hyderabad',
'Telangana',
'500081'),

('Priya','Reddy','Female','1999-08-15',
'9876543211',
'priya@gmail.com',
'123456789013',
'ABCDE1235G',
'Anna Nagar',
'Chennai',
'Tamil Nadu',
'600040'),

('Arjun','Kumar','Male','1997-04-20',
'9876543212',
'arjun@gmail.com',
'123456789014',
'ABCDE1236H',
'Whitefield',
'Bengaluru',
'Karnataka',
'560066'),

('Sneha','Patil','Female','1996-09-11',
'9876543213',
'sneha@gmail.com',
'123456789015',
'ABCDE1237J',
'Andheri',
'Mumbai',
'Maharashtra',
'400053'),

('Karan','Singh','Male','1995-01-22',
'9876543214',
'karan@gmail.com',
'123456789016',
'ABCDE1238K',
'Rohini',
'New Delhi',
'Delhi',
'110085');

#Show all customers
SELECT * FROM Customers;

#Show first names only
SELECT first_name
FROM Customers;

# Show first and last names
SELECT first_name,last_name
FROM Customers;

# Show customers from Hyderabad
SELECT *
FROM Customers
WHERE city='Hyderabad';

# Show female customers
SELECT *
FROM Customers
WHERE gender='Male';

# Sort by first name
SELECT *
FROM Customers
ORDER BY first_name;

# Sort by city
SELECT *
FROM Customers
ORDER BY city;

# Count customers
SELECT COUNT(*)
FROM Customers;

# account
INSERT INTO Accounts
(account_number,customer_id,branch_id,
account_type,balance,account_status,open_date)

VALUES

('SB100001',1,1,'Savings',50000,'Active','2023-01-10'),

('SB100002',2,2,'Savings',75000,'Active','2023-02-15'),

('CA100003',3,3,'Current',150000,'Active','2022-08-11'),

('SB100004',4,4,'Savings',95000,'Active','2023-07-18'),

('CA100005',5,5,'Current',250000,'Active','2022-04-22');

SELECT * FROM Accounts;

# Show account number and balance
SELECT account_number,balance
FROM Accounts;

# Show savings accounts
SELECT *
FROM Accounts
WHERE account_type='Savings';

# Show current accounts
SELECT *
FROM Accounts
WHERE account_type='Current';

# Show balance greater than ₹50,000
SELECT *
FROM Accounts
WHERE balance > 50000;

# Sort by balance
SELECT *
FROM Accounts
ORDER BY balance DESC;

#  Count total accounts
SELECT COUNT(*)
FROM Accounts;

# Employees

INSERT INTO Employees
(employee_code,first_name,last_name,gender,
designation,salary,phone,email,hire_date,branch_id)

VALUES

('EMP001','Ramesh','Kumar','Male',
'Branch Manager',85000,
'9000000001',
'ramesh@bank.com',
'2019-01-10',1),

('EMP002','Lakshmi','Rao','Female',
'Cashier',45000,
'9000000002',
'lakshmi@bank.com',
'2020-03-15',2),

('EMP003','Arun','Patel','Male',
'Relationship Manager',65000,
'9000000003',
'arun@bank.com',
'2021-05-12',3),

('EMP004','Divya','Sharma','Female',
'Loan Officer',70000,
'9000000004',
'divya@bank.com',
'2022-01-20',4),

('EMP005','Suresh','Reddy','Male',
'Operations Manager',90000,
'9000000005',
'suresh@bank.com',
'2018-07-18',5);

# Display all employees
SELECT * FROM Employees;

# Display employee names
SELECT first_name,last_name
FROM Employees;

# Employees with salary above 60000
SELECT *
FROM Employees
WHERE salary > 60000;

# Employees sorted by salary
SELECT *
FROM Employees
ORDER BY salary DESC;

# Count employees
SELECT COUNT(*)
FROM Employees;

# Highest salary
SELECT MAX(salary)
FROM Employees;

# Lowest salary
SELECT MIN(salary)
FROM Employees;

# Average salary
SELECT AVG(salary)
FROM Employees;

# Cards

INSERT INTO Cards
(card_number,
account_id,
card_type,
issue_date,
expiry_date,
cvv,
card_status)

VALUES

('5432123412340001',1,'Debit',
'2023-01-10','2028-01-09',
'321','Active'),

('5432123412340002',2,'Credit',
'2023-02-15','2028-02-14',
'452','Active'),

('5432123412340003',3,'Debit',
'2022-08-11','2027-08-10',
'671','Active'),

('5432123412340004',4,'Debit',
'2023-07-18','2028-07-17',
'198','Blocked'),

('5432123412340005',5,'Credit',
'2022-04-22','2027-04-21',
'567','Active');

# Show all cards
SELECT * FROM Cards;

# Show only debit cards
SELECT *
FROM Cards
WHERE card_type='Debit';

# Show only credit cards
SELECT *
FROM Cards
WHERE card_type='Credit';

# Show blocked cards
SELECT *
FROM Cards
WHERE card_status='Blocked';

# Count debit cards
SELECT COUNT(*)
FROM Cards
WHERE card_type='Debit';

# Count credit cards
SELECT COUNT(*)
FROM Cards
WHERE card_type='Credit';

# Active cards
SELECT *
FROM Cards
WHERE card_status='Active';

# Sort cards by expiry date
SELECT *
FROM Cards
ORDER BY expiry_date;

# Loans

INSERT INTO Loans
(
loan_number,
customer_id,
loan_type,
loan_amount,
interest_rate,
loan_tenure,
emi,
loan_status,
start_date,
end_date
)

VALUES

('HL100001',1,'Home',
2500000,
8.50,
240,
21696.00,
'Approved',
'2023-01-01',
'2042-12-31'),

('CL100002',2,'Car',
800000,
9.20,
60,
16682.00,
'Approved',
'2024-02-15',
'2029-02-14'),

('PL100003',3,'Personal',
300000,
11.50,
36,
9894.00,
'Approved',
'2024-01-20',
'2027-01-19'),

('EL100004',4,'Education',
600000,
7.80,
84,
9325.00,
'Pending',
NULL,
NULL),

('HL100005',5,'Home',
3500000,
8.75,
240,
30935.00,
'Rejected',
NULL,
NULL);


# Show all loans
SELECT * FROM Loans;

# Approved loans
SELECT *
FROM Loans
WHERE loan_status='Approved';

# Pending loans
SELECT *
FROM Loans
WHERE loan_status='Pending';

# Home loans
SELECT *
FROM Loans
WHERE loan_type='Home';

# Loans greater than ₹10,00,000
SELECT *
FROM Loans
WHERE loan_amount > 1000000;

# Highest loan amount
SELECT MAX(loan_amount) AS Highest_Loan
FROM Loans;

# Average loan amount
SELECT AVG(loan_amount) AS Average_Loan
FROM Loans;

# Total loan amount
SELECT SUM(loan_amount) AS Total_Loan
FROM Loans;

# Count approved loans
SELECT COUNT(*) AS Approved_Loans
FROM Loans
WHERE loan_status='Approved';

# Sort by loan amount
SELECT *
FROM Loans
ORDER BY loan_amount DESC;


#Transactions

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

('TXN100001',1,'Deposit',25000,'Success','Cash Deposit'),

('TXN100002',1,'Withdrawal',5000,'Success','ATM Withdrawal'),

('TXN100003',2,'UPI',1200,'Success','UPI Payment'),

('TXN100004',2,'NEFT',25000,'Success','Rent Transfer'),

('TXN100005',3,'Deposit',50000,'Success','Salary Credit'),

('TXN100006',3,'RTGS',100000,'Success','Business Payment'),

('TXN100007',4,'Withdrawal',7000,'Success','ATM Withdrawal'),

('TXN100008',4,'Deposit',18000,'Pending','Cheque Deposit'),

('TXN100009',5,'IMPS',3500,'Success','Online Shopping'),

('TXN100010',5,'Transfer',15000,'Failed','Insufficient Balance');


# Display all transactions
SELECT * FROM Transactions;

# Deposit Transactions
SELECT *
FROM Transactions
WHERE transaction_type='Deposit';

# Withdrawal Transactions
SELECT *
FROM Transactions
WHERE transaction_type='Withdrawal';

# Pending Transactions
SELECT *
FROM Transactions
WHERE transaction_status='Pending';

# Failed Transactions
SELECT *
FROM Transactions
WHERE transaction_status='Failed';

# Transactions greater than ₹20,000
SELECT *
FROM Transactions
WHERE amount > 20000;

# Highest Transaction
SELECT MAX(amount)
FROM Transactions;

# Lowest Transaction
SELECT MIN(amount)
FROM Transactions;

# Average Transaction
SELECT AVG(amount)
FROM Transactions;

# Total Transaction Amount
SELECT SUM(amount)
FROM Transactions;

# Count Transactions
SELECT COUNT(*)
FROM Transactions;

# Sort by Amount
SELECT *
FROM Transactions
ORDER BY amount DESC;

# Sort by Latest Transaction
SELECT *
FROM Transactions
ORDER BY transaction_date DESC;
