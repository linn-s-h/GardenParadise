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
    
# add timestamp column
ALTER TABLE favourites
ADD COLUMN added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

####################################################################################
