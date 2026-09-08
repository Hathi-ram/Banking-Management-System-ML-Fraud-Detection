# Procedure 1: Deposit Money

USE bankingdb;

DELIMITER $$

DROP PROCEDURE IF EXISTS DepositMoney $$

CREATE PROCEDURE DepositMoney
(
    IN p_account_number VARCHAR(20),
    IN p_amount DECIMAL(15,2)
)
BEGIN

    DECLARE v_account_id INT;

    SELECT account_id
    INTO v_account_id
    FROM Accounts
    WHERE account_number = p_account_number;

    UPDATE Accounts
    SET balance = balance + p_amount
    WHERE account_id = v_account_id;

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
    (
        CONCAT('TXN', UNIX_TIMESTAMP()),
        v_account_id,
        'Deposit',
        p_amount,
        'Success',
        'Cash Deposit'
    );

END $$

DELIMITER ;

# Procedure 2: Withdraw Money

DELIMITER $$

DROP PROCEDURE IF EXISTS WithdrawMoney $$

CREATE PROCEDURE WithdrawMoney
(
    IN p_account_number VARCHAR(20),
    IN p_amount DECIMAL(15,2)
)
BEGIN

    DECLARE v_account_id INT;
    DECLARE v_balance DECIMAL(15,2);

    SELECT account_id, balance
    INTO v_account_id, v_balance
    FROM Accounts
    WHERE account_number = p_account_number;

    IF v_balance >= p_amount THEN

        UPDATE Accounts
        SET balance = balance - p_amount
        WHERE account_id = v_account_id;

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
        (
            CONCAT('TXN', UNIX_TIMESTAMP()),
            v_account_id,
            'Withdrawal',
            p_amount,
            'Success',
            'ATM Withdrawal'
        );

    ELSE

        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT='Insufficient Balance';

    END IF;

END $$

DELIMITER ;

# Procedure 3: Transfer Money

DELIMITER $$

DROP PROCEDURE IF EXISTS TransferMoney $$

CREATE PROCEDURE TransferMoney
(
    IN sender_account VARCHAR(20),
    IN receiver_account VARCHAR(20),
    IN transfer_amount DECIMAL(15,2)
)
BEGIN

    DECLARE sender_id INT;
    DECLARE receiver_id INT;
    DECLARE sender_balance DECIMAL(15,2);

    SELECT account_id, balance
    INTO sender_id, sender_balance
    FROM Accounts
    WHERE account_number = sender_account;

    SELECT account_id
    INTO receiver_id
    FROM Accounts
    WHERE account_number = receiver_account;

    IF sender_balance >= transfer_amount THEN

        UPDATE Accounts
        SET balance = balance - transfer_amount
        WHERE account_id = sender_id;

        UPDATE Accounts
        SET balance = balance + transfer_amount
        WHERE account_id = receiver_id;

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
        (
            CONCAT('TXN', UNIX_TIMESTAMP()),
            sender_id,
            'Transfer',
            transfer_amount,
            'Success',
            CONCAT('Transfer to ', receiver_account)
        );

    ELSE

        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT='Insufficient Balance';

    END IF;

END $$

DELIMITER ;
