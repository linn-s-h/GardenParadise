############################# FAVOURITES TABLE ###########################

# Create favourites table
CREATE TABLE IF NOT EXISTS favourites (
	favourite_id INT AUTO_INCREMENT PRIMARY KEY,
	`User ID` INT NOT NULL,
    `Plant ID` INT NOT NULL,
    FOREIGN KEY (`User ID`) REFERENCES users(`User ID`) ON DELETE CASCADE,
    FOREIGN KEY (`Plant ID`) REFERENCES plants(`Plant ID`) ON DELETE CASCADE,
    UNIQUE(`User ID`, `Plant ID`)
    );
    
# Add timestamp column
ALTER TABLE favourites
ADD COLUMN added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

########################## TESTING ############################

# Test Insert
INSERT INTO favourites (`User ID`, `Plant ID`) VALUES (1, 2);
INSERT INTO favourites (`User ID`, `Plant ID`) VALUES (1, 3);

# Test duplicates
SELECT * FROM favourites WHERE `User ID` = 1 AND `Plant ID` = 2;

# Test Retrieval
SELECT p.*
FROM plants p
JOIN favourites f ON p.`Plant ID` = f.`Plant ID`
WHERE f.`User ID` = 1;

# Test Retrieval
SELECT p.`Common Name`, p.`Botanical Name`, p.`Plant ID`
    FROM favourites f
    JOIN plants p ON f.`Plant ID` = p.`Plant ID`
    WHERE f.`User ID` = 1 ORDER BY f.added_date ASC;

# Delete from favourites example
DELETE FROM favourites WHERE `User ID` = 1 AND `Plant ID` = 2;

####################################################################################
