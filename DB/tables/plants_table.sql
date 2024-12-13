
/*

Our Garden Paradise Database
Creation!

*/
CREATE DATABASE garden_paradise;
USE garde_paradise;

########################### CREATING PLANTS TABLE #########################

#Create plants table
CREATE TABLE IF NOT EXISTS plants (
	id INT,
    `Plant ID` INT NOT NULL AUTO_INCREMENT,
    `Plant Code` TEXT,
    `Botanical Name` TEXT,
    `Common Name` TEXT,
    `Previous Name` TEXT,
    `Plant Type` TEXT,
    `Water Needs` TEXT,
    `Climate Zones` TEXT,
    `Light Needs` TEXT,
    `Soil Type` TEXT,
    `Soil Additional` TEXT,
    `Maintenance` TEXT,
    `Abcission` TEXT,
    `Height Ranges` TEXT,
    `Spread Ranges` TEXT,
    `Flower Colour` TEXT,
    `Foliage Colour` TEXT,
    `Perfume` TEXT,
    `Aromatic` TEXT,
    `Edible` TEXT,
    `Bird Attracting` TEXT,
    `Bird Attractant` TEXT,
    `Bore Water Tolerance` TEXT,
    `Frost Tolerance` TEXT,
    `Greywater Tolerance` TEXT,
    `Native` TEXT,
    `Butterfly Attracting` TEXT,
    `Butterfly Type` TEXT,
    `Image` TEXT,
    `Image Location` TEXT,
    `Image Owner` TEXT,
    `Herb External Have` TEXT,
    `Herb Images Change To` TEXT,
    `Notes` TEXT,
    `Why Photo Removed` TEXT,
    `Why Plant Removed` TEXT,
    `Actioned By` TEXT,
    `Date Actioned` TEXT,
    `Status` TEXT,
    PRIMARY KEY (`Plant ID`)
);

#Edited out because it didn' work. Used Load Data Import Wizard instead
/*
LOAD DATA LOCAL INFILE '/path/waterwise-plants.csv'
INTO TABLE garden_paradise.plants
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
*/