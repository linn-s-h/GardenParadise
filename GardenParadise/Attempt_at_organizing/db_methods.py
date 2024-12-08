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