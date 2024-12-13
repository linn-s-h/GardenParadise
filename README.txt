i) Create the DB, tables and populate them. See (DB AND TABLES CREATION) at the bottom of this file for instructions

ii) Create a virtual environment by loading all the required packages contained in the file requirements.txt
	pip install -r requirements-txt / py -m pip install -r requirements.txt

iii) Update config.py in the GUI folder by changing the following values: 
	DB_HOST
	DB_USER
	DB_PASSWORD
	BASE_IMAGE_DIR

iiii) Execute group1-main.py to start the GUI


DB AND TABLES CREATION

1. Open plants_table.sql in MySQL Workbench from DB/tables and execute the file
2. Use Table Data Import Wizards in MySQL Workbench to import the waterwise-plants.csv file from DB/datasets
3. When selecting destination, select 'Use existing table garden_paradise.plants' (4654 records should be imported)
4. Open images_table.sql in MySQL Workbench from DB/tables and execute the file
5. Open users_table.sql in MySQL Workbench from DB/tables and execute the file
6. Open favourites_table.sql in MySQL Workbench from DB/tables and execute the file

