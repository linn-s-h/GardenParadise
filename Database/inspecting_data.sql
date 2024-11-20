/*

Inspecting data queries

*/


CREATE DATABASE garden_paradise;
USE garden_paradise;

SELECT DISTINCT `Why Plant Removes`
FROM plants;

#Frost Tolerance are 5 different categories, uncluding Unknown
SELECT DISTINCT `Frost Tolerance`, COUNT(`Frost Tolerance`)
FROM plants
GROUP BY `Frost Tolerance`
ORDER BY `Frost Tolerance` ASC;

#Bird Attracting are 3 different categories
SELECT DISTINCT `Bird Attracting`, COUNT(`Bird Attracting`)
FROM plants
GROUP BY `Bird Attracting`
ORDER BY `Bird Attracting` ASC;

#Succulents are small lol
SELECT DISTINCT `Plant Type`, `Height Ranges`, COUNT(*) AS amount
FROM plants
WHERE `Plant Type` LIKE "%Succulent%"
GROUP BY `Plant Type`, `Height Ranges`
ORDER BY amount DESC 
LIMIT 1;

#
SELECT `Plant Type`, `Climate Zones`, COUNT(*) AS amount
FROM plants
WHERE `Plant Type` LIKE "%Succulent%"
GROUP BY `Plant Type`, `Climate Zones`
ORDER BY amount DESC
LIMIT 1;

SELECT DISTINCT `Climate Zones`
FROM plants
ORDER BY `Climate Zones` DESC;

#Checking if there are some plants that can't be sold, there are since they're endangered
SELECT * FROM plants
WHERE `Status` NOT LIKE "Active";

#Checking plant types, and and how many of each type. Some spacing errors
SELECT DISTINCT `Plant Type`, COUNT(`Plant Type`)
FROM plants
GROUP BY `Plant Type`
ORDER BY `Plant Type` ASC;

SELECT DISTINCT `Climate Zones`, COUNT(`Climate Zones`)
FROM plants
GROUP BY `Climate Zones`
ORDER BY `Climate Zones` ASC;

#Checking duplcates in categories, there isn't
SELECT COUNT(*)
FROM plants
WHERE `Light Needs` LIKE "%Semi-shade%"
OR `Light Needs` LIKE "Semi-shade";

SELECT COUNT(DISTINCT `Plant Code`)
FROM plants
WHERE `Light Needs` LIKE "%Semi-shade%"
OR `Light Needs` LIKE "Semi-shade";

#Comparing CSV file last value and last value imported here
SELECT * FROM plants
ORDER BY id DESC
LIMIT 1;

#To observe the different notes
SELECT DISTINCT `Notes` FROM plants
WHERE `Notes` NOT LIKE "";

SELECT p.`Common Name`, img.`Image Location`
FROM plants p
JOIN images img ON p.`Image ID` = img.`Image ID`
WHERE img.`Image` NOT LIKE "NO"
GROUP BY `Common Name`, `Image Location`;




