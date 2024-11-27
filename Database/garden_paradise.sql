
/*

Our Garden Paradise Database
Creation!

*/

#Create plants table
CREATE TABLE plants (
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

#Create table
CREATE TABLE images (
	`Image ID` INT NOT NULL AUTO_INCREMENT, 
    `Plant ID` INT,
    `Image` TEXT,
    `Image Location` TEXT,
    `Image Owner` TEXT,
    `Herb Images Change To` TEXT,
    `Why Photo Removed` TEXT,
    PRIMARY KEY (`Image ID`),
    FOREIGN KEY (`Plant ID`) REFERENCES plants(`Plant ID`)
);

SELECT * FROM plants;

#Insert data
INSERT INTO images (`Plant ID`,`Image`, `Image Location`, `Image Owner`, `Herb Images Change To`, `Why Photo Removed`)
SELECT `Plant ID`, `Image`, `Image Location`, `Image Owner`, `Herb Images Change To`, `Why Photo Removed` FROM plants;

#Making column/index
ALTER TABLE plants 
ADD COLUMN `Image ID` 
INT NOT NULL AFTER `Butterfly Type`;

#Updating rows to corresponding ids
UPDATE plants
SET `Image ID` = (SELECT images.`Image ID` 
                  FROM images 
                  WHERE images.`Plant ID` = plants.`Plant ID`);
 
#Modifying foreign key      
ALTER TABLE plants 
ADD CONSTRAINT fk_images_id
FOREIGN KEY (`Image ID`) 
REFERENCES images(`Image ID`);

#Commands when inserts goes wrong
ALTER TABLE plants DROP CONSTRAINT fk_images_id;
ALTER TABLE plants DROP FOREIGN KEY `Image ID`;
ALTER TABLE plants DROP COLUMN `Image ID`;

SELECT * FROM images;

#Deleted columns from plants that have been moved to images table
ALTER TABLE plants
DROP COLUMN `Image`,
DROP COLUMN `Image Location`,
DROP COLUMN `Image Owner`,
DROP COLUMN `Herb Images Change To`,
DROP COLUMN `Why Photo Removed`;

ALTER TABLE plants
DROP COLUMN id;

SELECT COUNT(`Plant Type`), (SELECT DISTINCT `Plant Type`) FROM plants GROUP BY `Plant Type`;
















