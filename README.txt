i) Create the DB and tables needed. See (DB AND TABLES CREATION) at the bottom of this file for instructions

ii) Create a virtual environment by loading all the required packages contained in the file requirements.txt
	pip install -r requirements-txt / py -m pip install -r requirements.txt

iii) Update config.py in the GUI folder by changing the following values: 
	DB_HOST
	DB_USER
	DB_PASSWORD
	BASE_IMAGE_DIR

iv) Execute group1-main.py to start the GUI

########################
DB AND TABLES CREATION
########################

i) Go to File in MySQL Workbench and select 'Open SQL Script'
ii) Select group1-db-dump.sql from DB/tables
iii) Execute the file to create the DB, tables and populate them 

=== OR ===

i) Open plants_table.sql in MySQL Workbench from DB/tables and execute the file
ii) Use Table Data Import Wizards in MySQL Workbench to import the waterwise-plants.csv file from DB/datasets
iii) When selecting destination, select 'Use existing table garden_paradise.plants' (4654 records should be imported)
iv) Open images_table.sql in MySQL Workbench from DB/tables and execute the file
v) Open users_table.sql in MySQL Workbench from DB/tables and execute the file
vi) Open favourites_table.sql in MySQL Workbench from DB/tables and execute the file

