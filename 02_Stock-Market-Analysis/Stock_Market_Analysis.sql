
CREATE DATABASE IF NOT EXISTS stock_market_analysis;
USE stock_market_analysis; 
SHOW TABLES;

-- Count total rows in all six stock tables

SELECT 'Bajaj auto' AS stock_name, COUNT(*) AS total_rows
FROM `Bajaj auto`

UNION ALL

SELECT 'Eicher motors', COUNT(*)
FROM `Eicher motors`

UNION ALL

SELECT 'Hero motocorp', COUNT(*)
FROM `Hero motocorp`

UNION ALL

SELECT 'Infosys', COUNT(*)
FROM `Infosys`

UNION ALL

SELECT 'TCS', COUNT(*)
FROM `Tcs`

UNION ALL

SELECT 'TVS motors', COUNT(*)
FROM `Tvs motors`;

-- Step 2: Check column names and data types
-- of the Bajaj Auto stock table

DESCRIBE `Bajaj auto`;

-- Step 3: Display the first 5 records
-- from the Bajaj Auto table

SELECT *
FROM `Bajaj auto`
LIMIT 5;


-- Step 4: Check total records in the Bajaj Auto table

SELECT COUNT(*) AS total_rows
FROM `Bajaj auto`;

-- Step 4: Find the date range covered by each stock table

SELECT 'Bajaj auto' AS stock_name, MIN(`Date`) AS start_date, MAX(`Date`) AS end_date
FROM `Bajaj auto`

UNION ALL

SELECT 'Eicher motors', MIN(`Date`), MAX(`Date`)
FROM `Eicher motors`

UNION ALL

SELECT 'Hero motocorp', MIN(`Date`), MAX(`Date`)
FROM `Hero motocorp`

UNION ALL

SELECT 'Infosys', MIN(`Date`), MAX(`Date`)
FROM `Infosys`

UNION ALL

SELECT 'TCS', MIN(`Date`), MAX(`Date`)
FROM `Tcs`

UNION ALL

SELECT 'TVS motors', MIN(`Date`), MAX(`Date`)
FROM `Tvs motors`;

-- Step 5: Calculate the average closing price of each stock

SELECT 'Bajaj auto' AS stock_name, ROUND(AVG(`Close Price`), 2) AS avg_closing_price
FROM `Bajaj auto`

UNION ALL

SELECT 'Eicher motors', ROUND(AVG(`Close Price`), 2)
FROM `Eicher motors`

UNION ALL

SELECT 'Hero motocorp', ROUND(AVG(`Close Price`), 2)
FROM `Hero motocorp`

UNION ALL

SELECT 'Infosys', ROUND(AVG(`Close Price`), 2)
FROM `Infosys`

UNION ALL

SELECT 'TCS', ROUND(AVG(`Close Price`), 2)
FROM `Tcs`

UNION ALL

SELECT 'TVS motors', ROUND(AVG(`Close Price`), 2)
FROM `Tvs motors`;

-- Step 6: Find the highest and lowest closing price of each stock

SELECT
    'Bajaj auto' AS stock_name,
    MAX(`Close Price`) AS highest_close,
    MIN(`Close Price`) AS lowest_close
FROM `Bajaj auto`

UNION ALL

SELECT 'Eicher motors', MAX(`Close Price`), MIN(`Close Price`)
FROM `Eicher motors`

UNION ALL

SELECT 'Hero motocorp', MAX(`Close Price`), MIN(`Close Price`)
FROM `Hero motocorp`

UNION ALL

SELECT 'Infosys', MAX(`Close Price`), MIN(`Close Price`)
FROM `Infosys`

UNION ALL

SELECT 'TCS', MAX(`Close Price`), MIN(`Close Price`)
FROM `Tcs`

UNION ALL

SELECT 'TVS motors', MAX(`Close Price`), MIN(`Close Price`)
FROM `Tvs motors`;

-- Step 7: Combine all six stock tables into one master table

CREATE TABLE master_table AS
SELECT 'Bajaj auto' AS stock_name, `Date`, `Close Price`
FROM `Bajaj auto`

UNION ALL

SELECT 'Eicher motors', `Date`, `Close Price`
FROM `Eicher motors`

UNION ALL

SELECT 'Hero motocorp', `Date`, `Close Price`
FROM `Hero motocorp`

UNION ALL

SELECT 'Infosys', `Date`, `Close Price`
FROM `Infosys`

UNION ALL

SELECT 'Tcs', `Date`, `Close Price`
FROM `Tcs`

UNION ALL

SELECT 'Tvs motors', `Date`, `Close Price`
FROM `Tvs motors`;

-- Step 8: Verify the master table and its total records

SELECT stock_name, COUNT(*) AS total_rows
FROM master_table
GROUP BY stock_name;

-- Step 9: Calculate 20-day and 50-day moving averages for Bajaj Auto

CREATE TABLE bajaj1 AS
SELECT
    `Date`,
    `Close Price`,
    AVG(`Close Price`) OVER (
        ORDER BY STR_TO_DATE(`Date`, '%d-%M-%Y')
        ROWS BETWEEN 19 PRECEDING AND CURRENT ROW
    ) AS moving_avg_20,
    AVG(`Close Price`) OVER (
        ORDER BY STR_TO_DATE(`Date`, '%d-%M-%Y')
        ROWS BETWEEN 49 PRECEDING AND CURRENT ROW
    ) AS moving_avg_50
FROM `Bajaj auto`;

-- Step 10: Display the first 10 rows of Bajaj Auto moving averages
SELECT *
FROM bajaj1
ORDER BY STR_TO_DATE(`Date`, '%d-%M-%Y')
LIMIT 10;

-- Step 11: Generate trading signals from 20-day and 50-day moving averages
CREATE TABLE bajaj2 AS
SELECT
    `Date`,
    `Close Price`,
    moving_avg_20,
    moving_avg_50,
    CASE
        WHEN moving_avg_20 > moving_avg_50 THEN 'BUY'
        WHEN moving_avg_20 < moving_avg_50 THEN 'SELL'
        ELSE 'HOLD'
    END AS signal_type
FROM bajaj1;

-- Step 12: Count BUY, SELL, and HOLD signals
SELECT signal_type, COUNT(*) AS total_signals
FROM bajaj2
GROUP BY signal_type;

-- Step 13: Display the latest trading signals for Bajaj Auto
SELECT
    `Date`,
    `Close Price`,
    moving_avg_20,
    moving_avg_50,
    signal_type
FROM bajaj2
ORDER BY STR_TO_DATE(`Date`, '%d-%M-%Y') DESC
LIMIT 10;

-- Step 14: Find the trading signal for Bajaj Auto on a specific date
SELECT *
FROM bajaj2
WHERE STR_TO_DATE(`Date`, '%d-%M-%Y') = STR_TO_DATE('31-July-2018', '%d-%M-%Y');

-- Step 14: Find the Bajaj Auto trading signal on 31 July 2018
SELECT *
FROM bajaj2
WHERE STR_TO_DATE(`Date`, '%d-%M-%Y') =
      STR_TO_DATE('31-July-2018', '%d-%M-%Y');
      
-- Step 15: Generate BUY, SELL, and HOLD signals for all six stocks
SELECT
    stock_name,
    COUNT(*) AS total_records,
    SUM(CASE WHEN moving_avg_20 > moving_avg_50 THEN 1 ELSE 0 END) AS buy_signals,
    SUM(CASE WHEN moving_avg_20 < moving_avg_50 THEN 1 ELSE 0 END) AS sell_signals,
    SUM(CASE WHEN moving_avg_20 = moving_avg_50 THEN 1 ELSE 0 END) AS hold_signals
FROM (
    SELECT
        'Bajaj auto' AS stock_name,
        AVG(`Close Price`) OVER (
            ORDER BY STR_TO_DATE(`Date`, '%d-%M-%Y')
            ROWS BETWEEN 19 PRECEDING AND CURRENT ROW
        ) AS moving_avg_20,
        AVG(`Close Price`) OVER (
            ORDER BY STR_TO_DATE(`Date`, '%d-%M-%Y')
            ROWS BETWEEN 49 PRECEDING AND CURRENT ROW
        ) AS moving_avg_50
    FROM `Bajaj auto`

    UNION ALL

    SELECT
        'Eicher motors',
        AVG(`Close Price`) OVER (ORDER BY STR_TO_DATE(`Date`, '%d-%M-%Y') ROWS BETWEEN 19 PRECEDING AND CURRENT ROW),
        AVG(`Close Price`) OVER (ORDER BY STR_TO_DATE(`Date`, '%d-%M-%Y') ROWS BETWEEN 49 PRECEDING AND CURRENT ROW)
    FROM `Eicher motors`

    UNION ALL

    SELECT
        'Hero motocorp',
        AVG(`Close Price`) OVER (ORDER BY STR_TO_DATE(`Date`, '%d-%M-%Y') ROWS BETWEEN 19 PRECEDING AND CURRENT ROW),
        AVG(`Close Price`) OVER (ORDER BY STR_TO_DATE(`Date`, '%d-%M-%Y') ROWS BETWEEN 49 PRECEDING AND CURRENT ROW)
    FROM `Hero motocorp`

    UNION ALL

    SELECT
        'Infosys',
        AVG(`Close Price`) OVER (ORDER BY STR_TO_DATE(`Date`, '%d-%M-%Y') ROWS BETWEEN 19 PRECEDING AND CURRENT ROW),
        AVG(`Close Price`) OVER (ORDER BY STR_TO_DATE(`Date`, '%d-%M-%Y') ROWS BETWEEN 49 PRECEDING AND CURRENT ROW)
    FROM `Infosys`

    UNION ALL

    SELECT
        'Tcs',
        AVG(`Close Price`) OVER (ORDER BY STR_TO_DATE(`Date`, '%d-%M-%Y') ROWS BETWEEN 19 PRECEDING AND CURRENT ROW),
        AVG(`Close Price`) OVER (ORDER BY STR_TO_DATE(`Date`, '%d-%M-%Y') ROWS BETWEEN 49 PRECEDING AND CURRENT ROW)
    FROM `Tcs`

    UNION ALL

    SELECT
        'Tvs motors',
        AVG(`Close Price`) OVER (ORDER BY STR_TO_DATE(`Date`, '%d-%M-%Y') ROWS BETWEEN 19 PRECEDING AND CURRENT ROW),
        AVG(`Close Price`) OVER (ORDER BY STR_TO_DATE(`Date`, '%d-%M-%Y') ROWS BETWEEN 49 PRECEDING AND CURRENT ROW)
    FROM `Tvs motors`
) AS all_stocks
GROUP BY stock_name;      

-- Step 16: Calculate daily percentage returns for all six stocks
SELECT
    stock_name,
    `Date`,
    `Close Price`,
    ROUND(
        (
            `Close Price` - LAG(`Close Price`) OVER (
                PARTITION BY stock_name
                ORDER BY STR_TO_DATE(`Date`, '%d-%M-%Y')
            )
        ) /
        NULLIF(
            LAG(`Close Price`) OVER (
                PARTITION BY stock_name
                ORDER BY STR_TO_DATE(`Date`, '%d-%M-%Y')
            ), 0
        ) * 100,
        2
    ) AS daily_return_percent
FROM master_table
ORDER BY stock_name, STR_TO_DATE(`Date`, '%d-%M-%Y');

-- Step 17: Identify the largest one-day percentage drop for each stock
WITH daily_changes AS (
    SELECT
        stock_name,
        `Date`,
        `Close Price`,
        LAG(`Close Price`) OVER (
            PARTITION BY stock_name
            ORDER BY STR_TO_DATE(`Date`, '%d-%M-%Y')
        ) AS previous_close
    FROM master_table
)
SELECT
    stock_name,
    `Date`,
    previous_close,
    `Close Price`,
    ROUND(
        (`Close Price` - previous_close) / NULLIF(previous_close, 0) * 100,
        2
    ) AS daily_change_percent
FROM daily_changes
WHERE previous_close IS NOT NULL
ORDER BY daily_change_percent ASC
LIMIT 1;

-- Step 18: Display the latest 5 records for TCS and Infosys
SELECT *
FROM (
    SELECT 'TCS' AS stock_name, `Date`, `Close Price`
    FROM `Tcs`
    ORDER BY STR_TO_DATE(`Date`, '%d-%M-%Y') DESC
    LIMIT 5
) AS tcs_latest

UNION ALL

SELECT *
FROM (
    SELECT 'Infosys' AS stock_name, `Date`, `Close Price`
    FROM `Infosys`
    ORDER BY STR_TO_DATE(`Date`, '%d-%M-%Y') DESC
    LIMIT 5
) AS infosys_latest;

-- Step 19: Final verification of the stock analysis tables
SELECT 'Bajaj auto' AS table_name, COUNT(*) AS total_rows FROM `Bajaj auto`
UNION ALL
SELECT 'Eicher motors', COUNT(*) FROM `Eicher motors`
UNION ALL
SELECT 'Hero motocorp', COUNT(*) FROM `Hero motocorp`
UNION ALL
SELECT 'Infosys', COUNT(*) FROM `Infosys`
UNION ALL
SELECT 'Tcs', COUNT(*) FROM `Tcs`
UNION ALL
SELECT 'Tvs motors', COUNT(*) FROM `Tvs motors`
UNION ALL
SELECT 'master_table', COUNT(*) FROM master_table
UNION ALL
SELECT 'bajaj1', COUNT(*) FROM bajaj1
UNION ALL
SELECT 'bajaj2', COUNT(*) FROM bajaj2;

-- Step 20: Verify the earliest and latest dates in all six stock tables
SELECT 'Bajaj auto' AS stock_name,
       MIN(STR_TO_DATE(`Date`, '%d-%M-%Y')) AS first_date,
       MAX(STR_TO_DATE(`Date`, '%d-%M-%Y')) AS last_date
FROM `Bajaj auto`

UNION ALL
SELECT 'Eicher motors',
       MIN(STR_TO_DATE(`Date`, '%d-%M-%Y')),
       MAX(STR_TO_DATE(`Date`, '%d-%M-%Y'))
FROM `Eicher motors`

UNION ALL
SELECT 'Hero motocorp',
       MIN(STR_TO_DATE(`Date`, '%d-%M-%Y')),
       MAX(STR_TO_DATE(`Date`, '%d-%M-%Y'))
FROM `Hero motocorp`

UNION ALL
SELECT 'Infosys',
       MIN(STR_TO_DATE(`Date`, '%d-%M-%Y')),
       MAX(STR_TO_DATE(`Date`, '%d-%M-%Y'))
FROM `Infosys`

UNION ALL
SELECT 'TCS',
       MIN(STR_TO_DATE(`Date`, '%d-%M-%Y')),
       MAX(STR_TO_DATE(`Date`, '%d-%M-%Y'))
FROM `Tcs`

UNION ALL
SELECT 'TVS motors',
       MIN(STR_TO_DATE(`Date`, '%d-%M-%Y')),
       MAX(STR_TO_DATE(`Date`, '%d-%M-%Y'))
FROM `Tvs motors`;

-- Step 21: Calculate TCS average closing price for each year
SELECT
    YEAR(STR_TO_DATE(`Date`, '%d-%M-%Y')) AS year,
    AVG(`Close Price`) AS average_closing_price
FROM `Tcs`
GROUP BY YEAR(STR_TO_DATE(`Date`, '%d-%M-%Y'))
ORDER BY year;

-- Step 22: Count NULL values in Deliverable Quantity for all six stocks

SELECT 'Bajaj auto' AS stock_name, COUNT(*) AS missing_values
FROM `Bajaj auto`
WHERE `Deliverable Quantity` IS NULL

UNION ALL

SELECT 'Eicher motors', COUNT(*)
FROM `Eicher motors`
WHERE `Deliverable Quantity` IS NULL

UNION ALL

SELECT 'Hero motocorp', COUNT(*)
FROM `Hero motocorp`
WHERE `Deliverable Quantity` IS NULL

UNION ALL

SELECT 'Infosys', COUNT(*)
FROM `Infosys`
WHERE `Deliverable Quantity` IS NULL

UNION ALL

SELECT 'TCS', COUNT(*)
FROM `Tcs`
WHERE `Deliverable Quantity` IS NULL

UNION ALL

SELECT 'TVS motors', COUNT(*)
FROM `Tvs motors`
WHERE `Deliverable Quantity` IS NULL;

-- Step 23: Verify 20-day and 50-day moving averages for Bajaj Auto

SELECT
    `Date`,
    `Close Price`,
    moving_avg_20,
    moving_avg_50
FROM bajaj1
ORDER BY STR_TO_DATE(`Date`, '%d-%M-%Y')
LIMIT 10;

-- Step 24: Count BUY, SELL and HOLD signals for Bajaj Auto

SELECT
    signal_type,
    COUNT(*) AS total_signals
FROM bajaj2
GROUP BY signal_type
ORDER BY signal_type;

-- Step 25: Find the latest trading signal for Bajaj Auto

SELECT
    `Date`,
    `Close Price`,
    moving_avg_20,
    moving_avg_50,
    signal_type
FROM bajaj2
ORDER BY STR_TO_DATE(`Date`, '%d-%M-%Y') DESC
LIMIT 1;

-- Step 26: Check Bajaj Auto trading signal on 31 July 2018

SELECT
    `Date`,
    `Close Price`,
    moving_avg_20,
    moving_avg_50,
    signal_type
FROM bajaj2
WHERE STR_TO_DATE(`Date`, '%d-%M-%Y') = '2018-07-31';

-- Step 27: Calculate BUY, SELL and HOLD signals for all six stocks

WITH moving_averages AS (
    SELECT
        stock_name,
        `Date`,
        `Close Price`,
        AVG(`Close Price`) OVER (
            PARTITION BY stock_name
            ORDER BY STR_TO_DATE(`Date`, '%d-%M-%Y')
            ROWS BETWEEN 19 PRECEDING AND CURRENT ROW
        ) AS moving_avg_20,
        AVG(`Close Price`) OVER (
            PARTITION BY stock_name
            ORDER BY STR_TO_DATE(`Date`, '%d-%M-%Y')
            ROWS BETWEEN 49 PRECEDING AND CURRENT ROW
        ) AS moving_avg_50
    FROM master_table
)
SELECT
    stock_name,
    CASE
        WHEN moving_avg_20 > moving_avg_50 THEN 'BUY'
        WHEN moving_avg_20 < moving_avg_50 THEN 'SELL'
        ELSE 'HOLD'
    END AS signal_type,
    COUNT(*) AS total_signals
FROM moving_averages
GROUP BY stock_name, signal_type
ORDER BY stock_name, signal_type;

-- Step 28: Calculate daily percentage returns for all six stocks

WITH daily_returns AS (
    SELECT
        stock_name,
        `Date`,
        `Close Price`,
        LAG(`Close Price`) OVER (
            PARTITION BY stock_name
            ORDER BY STR_TO_DATE(`Date`, '%d-%M-%Y')
        ) AS previous_close
    FROM master_table
)
SELECT
    stock_name,
    `Date`,
    `Close Price`,
    previous_close,
    ROUND(
        (`Close Price` - previous_close) / previous_close * 100,
        2
    ) AS daily_return_percent
FROM daily_returns
ORDER BY stock_name, STR_TO_DATE(`Date`, '%d-%M-%Y')
LIMIT 20;

-- Step 29: Find the biggest daily percentage fall for each stock

WITH daily_returns AS (
    SELECT
        stock_name,
        `Date`,
        `Close Price`,
        LAG(`Close Price`) OVER (
            PARTITION BY stock_name
            ORDER BY STR_TO_DATE(`Date`, '%d-%M-%Y')
        ) AS previous_close
    FROM master_table
),
returns_calculated AS (
    SELECT
        stock_name,
        `Date`,
        ROUND(
            (`Close Price` - previous_close) / previous_close * 100,
            2
        ) AS daily_return_percent
    FROM daily_returns
),
ranked_returns AS (
    SELECT *,
        ROW_NUMBER() OVER (
            PARTITION BY stock_name
            ORDER BY daily_return_percent
        ) AS row_num
    FROM returns_calculated
    WHERE daily_return_percent IS NOT NULL
)
SELECT
    stock_name,
    `Date`,
    daily_return_percent
FROM ranked_returns
WHERE row_num = 1
ORDER BY daily_return_percent;

-- Step 30: Check TCS closing prices around 31 May 2018

SELECT
    `Date`,
    `Close Price`
FROM `Tcs`
WHERE STR_TO_DATE(`Date`, '%d-%M-%Y')
      BETWEEN '2018-05-28' AND '2018-06-04'
ORDER BY STR_TO_DATE(`Date`, '%d-%M-%Y');

-- Step 30: Check Infosys closing prices around 15 June 2015

SELECT
    `Date`,
    `Close Price`
FROM `Infosys`
WHERE STR_TO_DATE(`Date`, '%d-%M-%Y')
      BETWEEN '2015-06-11' AND '2015-06-18'
ORDER BY STR_TO_DATE(`Date`, '%d-%M-%Y');

-- Step 31: Check TCS prices around the unusual fall on 31 May 2018

SELECT
    `Date`,
    `Close Price`
FROM `Tcs`
WHERE STR_TO_DATE(`Date`, '%d-%M-%Y')
      BETWEEN '2018-05-28' AND '2018-06-04'
ORDER BY STR_TO_DATE(`Date`, '%d-%M-%Y');

-- Step 32: Check latest available dates and closing prices for TCS and Infosys

SELECT
    'TCS' AS stock_name,
    `Date`,
    `Close Price`
FROM `Tcs`
ORDER BY STR_TO_DATE(`Date`, '%d-%M-%Y') DESC
LIMIT 5;

SELECT
    'Infosys' AS stock_name,
    `Date`,
    `Close Price`
FROM `Infosys`
ORDER BY STR_TO_DATE(`Date`, '%d-%M-%Y') DESC
LIMIT 5;

-- Step 33: Create a separate copy of Infosys for bonus adjustment
CREATE TABLE `Infosys_adjusted` AS
SELECT *
FROM `Infosys`;

-- Step 34: Create a separate copy of TCS for bonus adjustment
CREATE TABLE `Tcs_adjusted` AS
SELECT *
FROM `Tcs`;

-- Step 35: Verify the row counts in original and copied tables

SELECT 'Infosys' AS table_name, COUNT(*) AS total_rows
FROM `Infosys`

UNION ALL

SELECT 'Infosys_adjusted', COUNT(*)
FROM `Infosys_adjusted`

UNION ALL

SELECT 'Tcs', COUNT(*)
FROM `Tcs`

UNION ALL

SELECT 'Tcs_adjusted', COUNT(*)
FROM `Tcs_adjusted`;

-- Step 36: Compare Infosys prices around its bonus-event date

SELECT
    'Infosys_adjusted' AS stock_name,
    `Date`,
    `Close Price`
FROM `Infosys_adjusted`
WHERE STR_TO_DATE(`Date`, '%d-%M-%Y')
      BETWEEN '2015-06-11' AND '2015-06-18'
ORDER BY STR_TO_DATE(`Date`, '%d-%M-%Y');

-- Step 36: Compare TCS prices around its bonus-event date

SELECT
    'Tcs_adjusted' AS stock_name,
    `Date`,
    `Close Price`
FROM `Tcs_adjusted`
WHERE STR_TO_DATE(`Date`, '%d-%M-%Y')
      BETWEEN '2018-05-28' AND '2018-06-04'
ORDER BY STR_TO_DATE(`Date`, '%d-%M-%Y');

-- Step 37: Check Infosys prices around the bonus-event date

SELECT
    'Infosys_adjusted' AS stock_name,
    `Date`,
    `Close Price`
FROM `Infosys_adjusted`
WHERE STR_TO_DATE(`Date`, '%d-%M-%Y')
      BETWEEN '2015-06-11' AND '2015-06-18'
ORDER BY STR_TO_DATE(`Date`, '%d-%M-%Y');

-- Step 39: Verify the number of rows in both adjusted tables

SELECT 'Infosys_adjusted' AS table_name, COUNT(*) AS total_rows
FROM `Infosys_adjusted`

UNION ALL

SELECT 'Tcs_adjusted', COUNT(*)
FROM `Tcs_adjusted`;

-- Step 40: Temporarily disable safe update mode
SET SQL_SAFE_UPDATES = 0;

-- Adjust Infosys prices before its 1:1 bonus date
UPDATE `Infosys_adjusted`
SET
    `Open Price` = `Open Price` / 2,
    `High Price` = `High Price` / 2,
    `Low Price` = `Low Price` / 2,
    `Close Price` = `Close Price` / 2,
    `WAP` = `WAP` / 2
WHERE STR_TO_DATE(`Date`, '%d-%M-%Y') < '2015-06-15';

-- Adjust TCS prices before its 1:1 bonus date
UPDATE `Tcs_adjusted`
SET
    `Open Price` = `Open Price` / 2,
    `High Price` = `High Price` / 2,
    `Low Price` = `Low Price` / 2,
    `Close Price` = `Close Price` / 2,
    `WAP` = `WAP` / 2
WHERE STR_TO_DATE(`Date`, '%d-%M-%Y') < '2018-05-31';

-- Turn safe update mode back on
SET SQL_SAFE_UPDATES = 1;

-- Step 42: Check adjusted closing prices around the bonus dates
SELECT
    'Infosys' AS stock_name,
    `Date`,
    `Close Price`
FROM `Infosys_adjusted`
WHERE STR_TO_DATE(`Date`, '%d-%M-%Y')
      BETWEEN '2015-06-12' AND '2015-06-16'

UNION ALL

SELECT
    'TCS' AS stock_name,
    `Date`,
    `Close Price`
FROM `Tcs_adjusted`
WHERE STR_TO_DATE(`Date`, '%d-%M-%Y')
      BETWEEN '2018-05-29' AND '2018-06-01';