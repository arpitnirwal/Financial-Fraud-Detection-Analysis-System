CREATE DATABASE FinancialFraudDB;

USE FinancialFraudDB;

CREATE TABLE transactions (
    Transaction_ID VARCHAR(20) PRIMARY KEY,
    Customer_ID VARCHAR(20),
    Customer_Name VARCHAR(100),
    Transaction_Date DATE,
    Transaction_Time VARCHAR(20),
    City VARCHAR(50),
    Home_City VARCHAR(50),
    Transaction_Type VARCHAR(30),
    Merchant_Category VARCHAR(50),
    Amount DECIMAL(10,2),
    Payment_Method VARCHAR(30),
    Device_Type VARCHAR(30),
    Previous_Fraud_History VARCHAR(10),
    Fraud_Flag VARCHAR(10)
);

SELECT COUNT(*) FROM transactions;

SELECT * FROM transactions
LIMIT 10;

SELECT COUNT(*) AS Total_Transactions
FROM transactions;

SELECT COUNT(*) AS Fraud_Transactions
FROM transactions
WHERE Fraud_Flag='Fraud';

SELECT
ROUND(
COUNT(CASE WHEN Fraud_Flag='Fraud' THEN 1 END)*100.0/
COUNT(*),2
) AS Fraud_Percentage
FROM transactions;

SELECT City,
COUNT(*) AS Fraud_Cases
FROM transactions
WHERE Fraud_Flag='Fraud'
GROUP BY City
ORDER BY Fraud_Cases DESC;


SELECT Payment_Method,
COUNT(*) AS Fraud_Count
FROM transactions
WHERE Fraud_Flag='Fraud'
GROUP BY Payment_Method;

SELECT Merchant_Category,
COUNT(*) AS Fraud_Count
FROM transactions
WHERE Fraud_Flag='Fraud'
GROUP BY Merchant_Category
ORDER BY Fraud_Count DESC;


ALTER TABLE transactions
DROP COLUMN Fraud_Flag;

DESC transactions;

TRUNCATE TABLE transactions;
SELECT COUNT(*) FROM transactions;