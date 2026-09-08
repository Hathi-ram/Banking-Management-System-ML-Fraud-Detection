USE BankingDB;

-- ==========================================
-- FILE 12 : CARD MANAGEMENT
-- ==========================================

-- ==========================================
-- Query 1 : View All Cards
-- ==========================================

SELECT
    card_id,
    card_number,
    account_id,
    card_type,
    expiry_date,
    card_status
FROM Cards;

-- ==========================================
-- Query 2 : Active Cards
-- ==========================================

SELECT *
FROM Cards
WHERE card_status = 'Active';

-- ==========================================
-- Query 3 : Blocked Cards
-- ==========================================

SELECT *
FROM Cards
WHERE card_status = 'Blocked';

-- ==========================================
-- Query 4 : Expired Cards
-- ==========================================

SELECT *
FROM Cards
WHERE expiry_date < CURDATE();

-- ==========================================
-- Query 5 : Block a Card
-- ==========================================

UPDATE Cards
SET card_status = 'Blocked'
WHERE card_number = '4111111111111111';

-- ==========================================
-- Query 6 : Activate a Card
-- ==========================================

UPDATE Cards
SET card_status = 'Active'
WHERE card_number = '4111111111111111';

-- ==========================================
-- Query 7 : Replace an Expired Card
-- ==========================================

UPDATE Cards
SET
    expiry_date = '2031-12-31',
    card_status = 'Active'
WHERE card_number = '4111111111111111';

-- ==========================================
-- Query 8 : Count Cards by Type
-- ==========================================

SELECT
    card_type,
    COUNT(*) AS Total_Cards
FROM Cards
GROUP BY card_type;

-- ==========================================
-- Query 9 : Card Details with Customer
-- ==========================================

SELECT

    CONCAT(c.first_name,' ',c.last_name) AS Customer_Name,

    a.account_number,

    cd.card_number,

    cd.card_type,

    cd.expiry_date,

    cd.card_status

FROM Customers c

JOIN Accounts a
ON c.customer_id = a.customer_id

JOIN Cards cd
ON a.account_id = cd.account_id

ORDER BY Customer_Name;

-- ==========================================
-- Query 10 : Cards Expiring Within 1 Year
-- ==========================================

SELECT
    card_number,
    card_type,
    expiry_date
FROM Cards
WHERE expiry_date <= DATE_ADD(CURDATE(), INTERVAL 1 YEAR)
ORDER BY expiry_date;

