############################### CREATING IMAGES TABLE ############################

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

ALTER TABLE images
DROP COLUMN `Image Owner`,
DROP COLUMN `Herb Images Change To`,
DROP COLUMN `Why Photo Removed`;

############################# ADDING IMAGES ###########################
  
SET SQL_SAFE_UPDATES = 0;

SELECT * FROM images;

#Set default for every plant that has image
UPDATE images
SET `Image Location` = 'plants/default_plant.png'
WHERE `Image` LIKE "Yes";

#Set default for every plant that doesn't have image
UPDATE images
SET `Image Location` = 'plants/no_image.png'
WHERE `Image` LIKE "No";

#Set Orchid Default Image
UPDATE images
SET `Image Location` = 'plants/orchid/orchid_default.png'
WHERE `Plant ID` IN (
    SELECT `Plant ID`
    FROM plants
    WHERE `Plant Type` LIKE "%Orchid%"
);

#White Orchid
UPDATE images
SET `Image Location` = 'plants/orchid/orchid_white.png'
WHERE `Image` LIKE "Yes"
AND `Plant ID` IN (
    SELECT `Plant ID`
    FROM plants
    WHERE `Plant Type` LIKE "%Orchid%"
    AND `Flower Colour` LIKE "%White%"
);

#Yellow Orchid
UPDATE images
SET `Image Location` = 'plants/orchid/orchid_yellow.png'
WHERE `Plant ID` IN (
    SELECT `Plant ID`
    FROM plants
    WHERE `Plant Type` LIKE "%Orchid%"
    AND `Flower Colour` LIKE "%Yellow%"
);

#White and purple orchid
UPDATE images
SET `Image Location` = 'plants/orchid/orchid_white_purple.png'
WHERE `Image` LIKE "Yes"
AND `Plant ID` IN (
    SELECT `Plant ID`
    FROM plants
    WHERE `Plant Type` LIKE "%Orchid%"
    AND `Flower Colour` LIKE "%White%" 
    AND `Flower Colour` LIKE "%Purple%"
);

#Varied orchid
UPDATE images
SET `Image Location` = 'plants/orchid/orchid_varied.png'
WHERE `Image` LIKE "Yes"
AND `Plant ID` IN (
    SELECT `Plant ID`
    FROM plants
    WHERE `Plant Type` LIKE "%Orchid%"
    AND `Flower Colour` LIKE "%Varied%"
);

#Red orchid
UPDATE images
SET `Image Location` = 'plants/orchid/orchid_red.png'
WHERE `Image` LIKE "Yes"
AND `Plant ID` IN (
    SELECT `Plant ID`
    FROM plants
    WHERE `Plant Type` LIKE "%Orchid%"
    AND `Flower Colour` LIKE "%Red%"
);

#Purple orchid
UPDATE images
SET `Image Location` = 'plants/orchid/orchid_purple.png'
WHERE `Image` LIKE "Yes"
AND `Plant ID` IN (
    SELECT `Plant ID`
    FROM plants
    WHERE `Plant Type` LIKE "%Orchid%"
    AND `Flower Colour` LIKE "%Purple%"
);

#Pink orchid
UPDATE images
SET `Image Location` = 'plants/orchid/orchid_pink.png'
WHERE `Image` LIKE "Yes"
AND `Plant ID` IN (
    SELECT `Plant ID`
    FROM plants
    WHERE `Plant Type` LIKE "%Orchid%"
    AND `Flower Colour` LIKE "%Pink%"
);

#Orange orchid
UPDATE images
SET `Image Location` = 'plants/orchid/orchid_orange.png'
WHERE `Image` LIKE "Yes"
AND `Plant ID` IN (
    SELECT `Plant ID`
    FROM plants
    WHERE `Plant Type` LIKE "%Orchid%"
    AND `Flower Colour` LIKE "%Orange%"
);

#Lavender orchid
UPDATE images
SET `Image Location` = 'plants/orchid/orchid_lavender.png'
WHERE `Image` LIKE "Yes"
AND `Plant ID` IN (
    SELECT `Plant ID`
    FROM plants
    WHERE `Plant Type` LIKE "%Orchid%"
    AND `Flower Colour` LIKE "%Lavender%"
);

#Cream orchid
UPDATE images
SET `Image Location` = 'plants/orchid/orchid_cream.png'
WHERE `Image` LIKE "Yes"
AND `Plant ID` IN (
    SELECT `Plant ID`
    FROM plants
    WHERE `Plant Type` LIKE "%Orchid%"
    AND `Flower Colour` LIKE "%Cream%"
);

#Vegetable default
UPDATE images
SET `Image Location` = 'plants/vegetable/vegetable_default.png'
WHERE `Image` LIKE "Yes"
AND `Plant ID` IN (
    SELECT `Plant ID`
    FROM plants
    WHERE `Plant Type` LIKE "Vegetable"
);

#Vegetable default
UPDATE images
SET `Image Location` = 'plants/vegetable/vegetable_default.png'
WHERE `Image` LIKE "Yes"
AND `Plant ID` IN (
    SELECT `Plant ID`
    FROM plants
    WHERE `Plant Type` LIKE "Vegetable"
);

#Tree default
UPDATE images
SET `Image Location` = 'plants/tree/tree_default.png'
WHERE `Image` LIKE "Yes"
AND `Plant ID` IN (
    SELECT `Plant ID`
    FROM plants
    WHERE `Plant Type` LIKE "%Tree%"
);
#Small tree default
UPDATE images
SET `Image Location` = 'plants/tree/small_tree_default.png'
WHERE `Image` LIKE "Yes"
AND `Plant ID` IN (
    SELECT `Plant ID`
    FROM plants
    WHERE `Plant Type` LIKE "%Small tree%"
);

#Medium tree default
UPDATE images
SET `Image Location` = 'plants/tree/medium_tree_default.png'
WHERE `Image` LIKE "Yes"
AND `Plant ID` IN (
    SELECT `Plant ID`
    FROM plants
    WHERE `Plant Type` LIKE "%Medium tree%"
);

#Large tree default
UPDATE images
SET `Image Location` = 'plants/tree/large_tree_default.png'
WHERE `Image` LIKE "Yes"
AND `Plant ID` IN (
    SELECT `Plant ID`
    FROM plants
    WHERE `Plant Type` LIKE "%Large tree%"
);

#Succulent default
UPDATE images
SET `Image Location` = 'plants/succulent/succulent_default.png'
WHERE `Image` LIKE "Yes"
AND `Plant ID` IN (
    SELECT `Plant ID`
    FROM plants
    WHERE `Plant Type` LIKE "%Succulent%"
);

#Shrub default
UPDATE images
SET `Image Location` = 'plants/shrub/shrub_default.png'
WHERE `Image` LIKE "Yes"
AND `Plant ID` IN (
    SELECT `Plant ID`
    FROM plants
    WHERE `Plant Type` LIKE "%Shrub%"
);

#Shrub, vegetable
UPDATE images
SET `Image Location` = 'plants/shrub/shrub_vegetables.png'
WHERE `Image` LIKE "Yes"
AND `Plant ID` IN (
    SELECT `Plant ID`
    FROM plants
    WHERE `Plant Type` LIKE "%Shrub%"
    AND `Plant Type` LIKE "%vegetable%"
);

#Perennial default
UPDATE images
SET `Image Location` = 'plants/perennial/perennial_default.png'
WHERE `Image` LIKE "Yes"
AND `Plant ID` IN (
    SELECT `Plant ID`
    FROM plants
    WHERE `Plant Type` LIKE "%Perennial%"
);

#Annual default
UPDATE images
SET `Image Location` = 'plants/annual/annual_default.png'
WHERE `Image` LIKE "Yes"
AND `Plant ID` IN (
    SELECT `Plant ID`
    FROM plants
    WHERE `Plant Type` LIKE "%Annual%"
);

#Annual pink
UPDATE images
SET `Image Location` = 'plants/annual/annual_pink.png'
WHERE `Image` LIKE "Yes"
AND `Plant ID` IN (
    SELECT `Plant ID`
    FROM plants
    WHERE `Plant Type` LIKE "%Annual%"
    AND `Flower Colour` LIKE "%Pink%"
);

#Annual orange
UPDATE images
SET `Image Location` = 'plants/annual/annual_orange.png'
WHERE `Image` LIKE "Yes"
AND `Plant ID` IN (
    SELECT `Plant ID`
    FROM plants
    WHERE `Plant Type` LIKE "%Annual%"
    AND `Flower Colour` LIKE "%Orange%"
);

SET SQL_SAFE_UPDATES = 1;