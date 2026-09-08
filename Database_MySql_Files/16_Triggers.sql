# Audit Table

CREATE TABLE IF NOT EXISTS Transaction_Audit
(
    audit_id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_reference VARCHAR(25),
    account_id INT,
    transaction_type VARCHAR(30),
    amount DECIMAL(15,2),
    transaction_status VARCHAR(20),
    audit_time DATETIME DEFAULT CURRENT_TIMESTAMP
);

# Trigger
DELIMITER $$

DROP TRIGGER IF EXISTS trg_transaction_audit $$

CREATE TRIGGER trg_transaction_audit

AFTER INSERT ON Transactions

FOR EACH ROW

BEGIN

    INSERT INTO Transaction_Audit
    (
        transaction_reference,
        account_id,
        transaction_type,
        amount,
        transaction_status
    )
    VALUES
    (
        NEW.transaction_reference,
        NEW.account_id,
        NEW.transaction_type,
        NEW.amount,
        NEW.transaction_status
    );

END $$

DELIMITER ;

# Test

CALL DepositMoney('SB100001',1000);

SELECT * FROM Transaction_Audit;