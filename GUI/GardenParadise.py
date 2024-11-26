
from tkinter import *
import mysql.connector

#Backend

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "36Cc7919!"
DB_DATABASE = "garden_paradise"

#Connection code 
def connectDB():
    mydb = mysql.connector.connect(

        host = DB_HOST,
        user = DB_USER,
        passwd = DB_PASSWORD,
        database = DB_DATABASE
    )
    mycursor = mydb.cursor()
    return mydb, mycursor

#GUI

window = Tk()
window.geometry("1200x800")
window.title("Garden Paradise")

#Configurate the rows and columns for proportional resizing
window.grid_columnconfigure(0, weight=1) #1/5
window.grid_columnconfigure(1, weight=15) #4/5
window.grid_rowconfigure(0, weight=1) #1/4
window.grid_rowconfigure(1, weight=100) #3/4

#Menu frame
menu_frame = Frame(window, bg="black")
menu_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

#Search frame
search_frame = Frame(window, bg="beige")
search_frame.grid(row=1, column=0, sticky="nsew")

#Result frame
result_frame = Frame(window, bg= "white")
result_frame.grid(row=1, column=1, sticky="nsew")

#Menu frame content
title_label = Label(menu_frame, text="Garden Paradise", font=("Helvatica", 24, "bold"), bg="black", fg="white")
title_label.pack(padx=20, pady=20, side="left")

# Search frame content
search_entry = Entry(search_frame, font=("Arial", 24))
search_entry.grid(row=0, column=0, padx=(5, 1), pady=10, sticky="ew")  # Place in grid

search_button = Button(search_frame, text="Search", font=("Arial", 12))
search_button.grid(row=0, column=1, padx=(5, 10), pady=10)  # Place next to entry

# Configure columns in the search frame
search_frame.grid_columnconfigure(0, weight=1)  # Entry box wider
search_frame.grid_columnconfigure(1, weight=1)  # Button narrower





#Function to fetch distinct values from specified column in the plants table
def get_distinct_values(column_name):
    mydb, cursor = connectDB()
    cursor.execute(f"SELECT DISTINCT {column_name}, COUNT(*) FROM plants GROUP BY {column_name} ORDER BY {column_name} ASC")
    values = [row[0] for row in cursor.fetchall()]
    print(values)
    mydb.close()
    return values


#Dropdown manues in result frame
items =  get_distinct_values(f"`Plant Type`")

option = StringVar()
option.set("")

dropmenu = OptionMenu(search_frame, option, *items, command=lambda _: update_dropdown())
dropmenu.config(width=20)
dropmenu.grid(row=1, column=0)

def show_plants():
    Label(result_frame, text=option.get()).pack()
    option.set("")

find_plant_button = Button(search_frame, text="Find plant", font=("Arial", 12), command=show_plants)
find_plant_button.grid()

window.mainloop()