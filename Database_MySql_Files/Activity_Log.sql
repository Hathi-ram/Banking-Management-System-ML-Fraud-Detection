USE BankingDB;
CREATE TABLE Activity_Log (

    log_id INT AUTO_INCREMENT PRIMARY KEY,

    activity VARCHAR(255) NOT NULL,

    activity_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);


CREATE TABLE Admin(

    admin_id INT AUTO_INCREMENT PRIMARY KEY,

    username VARCHAR(50) UNIQUE NOT NULL,

    password VARCHAR(100) NOT NULL,

    full_name VARCHAR(100),

    email VARCHAR(100),

    phone VARCHAR(15)

);
SHOW TABLES;