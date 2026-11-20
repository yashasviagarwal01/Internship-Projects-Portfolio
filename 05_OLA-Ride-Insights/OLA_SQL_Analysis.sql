CREATE DATABASE OLA_Ride_Insights;
GO

USE OLA_Ride_Insights;
GO

SELECT COUNT(*) AS Total_Rides
FROM ola_rides;

SELECT TOP 5 *
FROM ola_rides;

-- Q1. Retrieve all successful bookings

USE OLA_Ride_Insights;
GO

SELECT *
FROM ola_rides
WHERE Booking_Status = 'Success';

--  Find the total number of successful bookings

SELECT COUNT(*) AS Total_Successful_Bookings
FROM ola_rides
WHERE Booking_Status = 'Success';

-- Q2. Retrieve the average ride distance for each vehicle type

SELECT
    Vehicle_Type,
    AVG(CAST(Ride_Distance AS FLOAT)) AS Average_Ride_Distance
FROM ola_rides
GROUP BY Vehicle_Type
ORDER BY Average_Ride_Distance DESC;

-- Q3. Find the total number of rides cancelled by customers

SELECT
    COUNT(*) AS Total_Cancelled_Rides_By_Customers
FROM ola_rides
WHERE Booking_Status = 'Canceled by Customer';

-- Q4. Find the Top 5 customers who booked the highest number of rides

SELECT TOP 5
    Customer_ID,
    COUNT(Booking_ID) AS Total_Rides
FROM ola_rides
GROUP BY Customer_ID
ORDER BY Total_Rides DESC;

-- Q5. Find the number of rides cancelled by drivers
-- due to personal and car-related issues

SELECT
    COUNT(*) AS Total_Driver_Cancellations
FROM ola_rides
WHERE Booking_Status = 'Canceled by Driver'
AND Canceled_Rides_by_Driver = 'Personal & Car related issue';

-- Q6. Find the maximum and minimum driver ratings
-- for Prime Sedan bookings

SELECT
    MAX(Driver_Ratings) AS Maximum_Driver_Rating,
    MIN(Driver_Ratings) AS Minimum_Driver_Rating
FROM ola_rides
WHERE Vehicle_Type = 'Prime Sedan';

-- Q7. Retrieve all rides that were paid using UPI

SELECT *
FROM ola_rides
WHERE Payment_Method = 'UPI';

--  Find the total number of rides paid using UPI

SELECT
    COUNT(*) AS Total_UPI_Bookings
FROM ola_rides
WHERE Payment_Method = 'UPI';

-- Q8. Find the average customer rating for each vehicle type

SELECT
    Vehicle_Type,
    AVG(Customer_Rating) AS Average_Customer_Rating
FROM ola_rides
GROUP BY Vehicle_Type
ORDER BY Average_Customer_Rating DESC;

-- Q9. Find the total booking value of successfully completed rides

SELECT
    SUM(Booking_Value) AS Total_Successful_Booking_Value
FROM ola_rides
WHERE Booking_Status = 'Success';

-- Q10. Retrieve all incomplete rides along with their reasons

SELECT
    Booking_ID,
    Customer_ID,
    Vehicle_Type,
    Booking_Status,
    Incomplete_Rides,
    Incomplete_Rides_Reason
FROM ola_rides
WHERE Incomplete_Rides = 1;

--  Find the total number of incomplete rides

SELECT
    COUNT(*) AS Total_Incomplete_Rides
FROM ola_rides
WHERE Incomplete_Rides = 1;