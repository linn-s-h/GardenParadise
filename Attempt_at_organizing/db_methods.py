import mysql.connector
import config

#Connection code 
def connectDB():
    mydb = mysql.connector.connect(

        host = config.DB_HOST,
        user = config.DB_USER,
        passwd = config.DB_PASSWORD,
        database = config.DB_DATABASE
    )
    mycursor = mydb.cursor()
    return mydb, mycursor

#Function to fetch distinct values from specified column in the plants table
def get_distinct_values(column_name):
    mydb, cursor = connectDB()
    cursor.execute(f"SELECT DISTINCT {column_name} FROM plants GROUP BY {column_name} ORDER BY {column_name} ASC")
    values = [row[0] for row in cursor.fetchall()]
    mydb.close()
    return values

#Function to fetch the count of each distinct value
def get_distinct_values_count(column_name):
    mydb, cursor = connectDB()
    cursor.execute(f"SELECT COUNT({column_name}), (SELECT DISTINCT {column_name}) FROM plants GROUP BY {column_name};")
    values = [row[0] for row in cursor.fetchall()]
    mydb.close()
    return values

#Function to fetch column names that have a keyword in it
def get_column_values(column_name):
    mydb, cursor = connectDB()
    query = """
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = 'plants' AND COLUMN_NAME LIKE %s
    """
    cursor.execute(query, (f"%{column_name}%",))
    values = [row[0] for row in cursor.fetchall()]
    mydb.close()
    return values

#Getting plant results from search bar entry
def get_plants_by_search(plant_name):
    mydb, cursor = connectDB()
    query = """
    SELECT `Common Name`, `Botanical Name`, `Plant ID`
    FROM plants
    WHERE `Common Name` LIKE %s OR `Botanical Name` LIKE %s
    ORDER BY `Common Name` ASC
    LIMIT 16;
    """
    cursor.execute(query, (f"%{plant_name}%", f"%{plant_name}%",))
    values = cursor.fetchall()
    mydb.close()
    return values

def get_image_path(plant_id):
    mydb, cursor = connectDB()
    query = """
    SELECT img.`Image Location`
    FROM images img
    JOIN plants p ON p.`Image ID` = img.`Image ID`
    WHERE p.`Plant ID` LIKE %s
    """
    cursor.execute(query, (f"{plant_id}",))
    value = cursor.fetchone()
    try:
        if value:
            relative_path = value[0].strip()  # Get the relative path from the database
            full_path = os.path.join(BASE_IMAGE_DIR, relative_path)  # Combine base directory with relative path
            return full_path
        else:
            return None
    finally:
        mydb.close()