################################# CREATING USERS TABLE #####################################

# Create USER table
CREATE TABLE IF NOT EXISTS users (
	user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    `password` VARCHAR(255) NOT NULL
    );
    
# Alter users table add first_name
ALTER TABLE users ADD COLUMN `first_name` VARCHAR(50) NOT NULL AFTER username;

# Alter users table add last_name
ALTER TABLE users ADD COLUMN `last_name` VARCHAR(50) NOT NULL AFTER first_name;

# Sample "new user" insert query
INSERT INTO users (username, first_name, last_name, `password`)
	VALUES ('joaquinbgarcia', 'Joaquin', 'Garcia', 'testing');
    
UPDATE users SET first_name = "Joaquin" WHERE username = "joaquinbgarcia" AND `password` = "testing";
UPDATE users SET last_name = "Garcia" WHERE username = "joaquinbgarcia" AND `password` = "testing";

ALTER TABLE users
RENAME COLUMN user_id to `User ID`;
    
# Sample user retrieval
SELECT * FROM users WHERE username = "joaquinbgarcia";
SELECT * FROM users;
