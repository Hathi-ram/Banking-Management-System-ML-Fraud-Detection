USE BankingDB;

CREATE TABLE Branches
(
    branch_id INT AUTO_INCREMENT PRIMARY KEY,
    branch_name VARCHAR(100) NOT NULL,
    branch_code VARCHAR(10) UNIQUE NOT NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    phone VARCHAR(15),
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

SHOW TABLES;

DESC Branches;

INSERT INTO Branches
(branch_name, branch_code, city, state, phone, email)
VALUES
('Hyderabad Main', 'HYD001', 'Hyderabad', 'Telangana', '0401111111', 'hyd@bank.com'),
('Chennai Central', 'CHE001', 'Chennai', 'Tamil Nadu', '0442222222', 'che@bank.com'),
('Bangalore City', 'BLR001', 'Bengaluru', 'Karnataka', '0803333333', 'blr@bank.com'),
('Mumbai West', 'MUM001', 'Mumbai', 'Maharashtra', '0224444444', 'mum@bank.com'),
('Delhi North', 'DEL001', 'New Delhi', 'Delhi', '0115555555', 'del@bank.com');

SELECT * FROM Branches;

#Module 2: Create Customers Table

-- ==========================================
-- Customers Table
-- ==========================================

CREATE TABLE Customers
(
    customer_id INT AUTO_INCREMENT PRIMARY KEY,

    first_name VARCHAR(50) NOT NULL,

    last_name VARCHAR(50) NOT NULL,

    gender ENUM('Male','Female','Other') NOT NULL,

    dob DATE NOT NULL,

    phone VARCHAR(15) UNIQUE NOT NULL,

    email VARCHAR(100) UNIQUE NOT NULL,

    aadhaar_number CHAR(12) UNIQUE NOT NULL,

    pan_number CHAR(10) UNIQUE NOT NULL,

    address VARCHAR(255),

    city VARCHAR(50),

    state VARCHAR(50),

    pincode CHAR(6),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

SHOW TABLES;

DESC Customers;


-- ==========================================
-- Accounts Table
-- ==========================================

CREATE TABLE Accounts
(
    account_id INT AUTO_INCREMENT PRIMARY KEY,

    account_number VARCHAR(20) UNIQUE NOT NULL,

    customer_id INT NOT NULL,

    branch_id INT NOT NULL,

    account_type ENUM('Savings','Current') NOT NULL,

    balance DECIMAL(15,2) DEFAULT 0,

    account_status ENUM('Active','Inactive','Closed')
    DEFAULT 'Active',

    open_date DATE NOT NULL,

    FOREIGN KEY (customer_id)
        REFERENCES Customers(customer_id),

    FOREIGN KEY (branch_id)
        REFERENCES Branches(branch_id)
);

DESC Accounts;


-- ==========================================
-- Employees Table
-- ==========================================

CREATE TABLE Employees
(
    employee_id INT AUTO_INCREMENT PRIMARY KEY,

    employee_code VARCHAR(10) UNIQUE NOT NULL,

    first_name VARCHAR(50) NOT NULL,

    last_name VARCHAR(50) NOT NULL,

    gender ENUM('Male','Female','Other') NOT NULL,

    designation VARCHAR(50) NOT NULL,

    salary DECIMAL(10,2) NOT NULL,

    phone VARCHAR(15) UNIQUE,

    email VARCHAR(100) UNIQUE,

    hire_date DATE NOT NULL,

    branch_id INT NOT NULL,

    FOREIGN KEY(branch_id)
        REFERENCES Branches(branch_id)
);

DESC Employees;


-- ==========================================
-- Cards Table
-- ==========================================

CREATE TABLE Cards
(
    card_id INT AUTO_INCREMENT PRIMARY KEY,

    card_number VARCHAR(16) UNIQUE NOT NULL,

    account_id INT NOT NULL,

    card_type ENUM('Debit','Credit') NOT NULL,

    issue_date DATE NOT NULL,

    expiry_date DATE NOT NULL,

    cvv CHAR(3) NOT NULL,

    card_status ENUM('Active','Blocked','Expired')
    DEFAULT 'Active',

    FOREIGN KEY(account_id)
        REFERENCES Accounts(account_id)
);

DESC Cards;


-- ==========================================
-- Loans Table
-- ==========================================

CREATE TABLE Loans
(
    loan_id INT AUTO_INCREMENT PRIMARY KEY,

    loan_number VARCHAR(20) UNIQUE NOT NULL,

    customer_id INT NOT NULL,

    loan_type ENUM('Home','Car','Education','Personal') NOT NULL,

    loan_amount DECIMAL(15,2) NOT NULL,

    interest_rate DECIMAL(5,2) NOT NULL,

    loan_tenure INT NOT NULL COMMENT 'Tenure in Months',

    emi DECIMAL(12,2) NOT NULL,

    loan_status ENUM('Approved','Pending','Rejected','Closed')
    DEFAULT 'Pending',

    start_date DATE,

    end_date DATE,

    FOREIGN KEY(customer_id)
        REFERENCES Customers(customer_id)
);

DESC Loans;


-- ==========================================
-- Transactions Table
-- ==========================================

CREATE TABLE Transactions
(
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,

    transaction_reference VARCHAR(25) UNIQUE NOT NULL,

    account_id INT NOT NULL,

    transaction_type ENUM
    (
        'Deposit',
        'Withdrawal',
        'Transfer',
        'UPI',
        'NEFT',
        'RTGS',
        'IMPS'
    ) NOT NULL,

    amount DECIMAL(15,2) NOT NULL,

    transaction_date DATETIME DEFAULT CURRENT_TIMESTAMP,

    transaction_status ENUM
    (
        'Success',
        'Pending',
        'Failed'
    ) DEFAULT 'Success',

    remarks VARCHAR(255),

    FOREIGN KEY(account_id)
    REFERENCES Accounts(account_id)
);

DESC Transactions;

