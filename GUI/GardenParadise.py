import mysql.connector
from tkinter import *
from tkinter import PhotoImage
#from PIL import Image, ImageTk

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
    # Execute the query with parameterized input
    cursor.execute(query, (f"%{column_name}%",))
    values = [row[0] for row in cursor.fetchall()]
    mydb.close()
    return values


###############################################################

#GUI
window = Tk()
window.geometry("1000x800")
window.title("Garden Paradise")

#Configurate the rows and columns for proportional resizing
window.grid_columnconfigure(0, weight=1) #1/5
window.grid_columnconfigure(1, weight=15) #4/5
window.grid_rowconfigure(0, weight=1) #1/4
window.grid_rowconfigure(1, weight=100) #3/4

#Menu frame
menu_frame = Frame(window, bg="#06402B")
menu_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

#Search frame
search_frame = Frame(window, bg="#F2F0EF")
search_frame.grid(row=1, column=0, sticky="nsew")

#Result frame
result_frame = Frame(window, bg= "white")
result_frame.grid(row=1, column=1, sticky="nsew")

#Menu frame content
title_label = Label(menu_frame, text="Garden Paradise", font=("Helvetica", 24, "bold"), bg="#06402B", fg="white")
title_label.pack(padx=20, pady=20, side="left")

#Search frame content
search_entry = Entry(search_frame)
search_entry.insert(0, "Search by common name or botanical name")
search_entry.grid(row=0, column=0, padx=(5, 10), pady=10, sticky="ew")  # Place in grid

search_button = Button(search_frame, text="Search", font=("Arial", 12))
search_button.grid(row=1, column=0, padx=(5, 10), pady=10)  # Place next to entry

#Scrollbar
scrollbar_frame = Frame(result_frame)
scrollbar_frame.pack(fill=BOTH, expand=1)

scrollbar_canvas = Canvas(scrollbar_frame, bg="white")
scrollbar_canvas.pack( side=LEFT, fill=BOTH, expand=1)

scrollbar = Scrollbar(scrollbar_frame, orient=VERTICAL, command=scrollbar_canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)

scrollbar_canvas.configure(yscrollcommand=scrollbar.set)
scrollbar_canvas.bind('<Configure>', lambda e: scrollbar_canvas.configure(scrollregion=scrollbar_canvas.bbox("all")))

scrollable_frame = Frame(scrollbar_canvas)
scrollbar_canvas.create_window((0,0), window=scrollable_frame, anchor=NW)

#Advanced setting label
advanced_search_label = Label(search_frame, text="Advanced search", font=("Arial", 16, "bold"))
advanced_search_label.grid(padx=10, pady=10, row=2, column=0)

dropdown_labels = ["Plant Type", "Climate Zones", "Flower Colour", "Tolerance", "Attracting"]

#Putting results from dropdown menu selection in a list
items = [
    get_distinct_values(f"`Plant Type`") , 
    get_distinct_values(f"`Climate Zones`"), 
    get_distinct_values(f"`Flower Colour`"),
    get_column_values(f"tolerance"),
    get_column_values(f"attracting")]  

#Creating a list of StringVar instances, one for each dropdown menu
dropdown_options = [StringVar(value="") for _ in dropdown_labels]

#Creating dropdown menus
for i in range(len(dropdown_labels)):

    dropdown = OptionMenu(search_frame, dropdown_options[i], *items[i], command=lambda _: update_dropdown())
    dropdown.config(width=20, bg="white")
    dropdown.grid(row=3+i, column=0, padx=10, pady=10)

#Getting results from advanced search
def fetch_plant_results():

    mydb, cursor = connectDB()
    results = []
    query = """
        SELECT `Common Name`, `Botanical Name`
        FROM plants
        WHERE 1+1
    """

    if dropdown_options[0].get():
        query += " AND `Plant Type` = %s"
        results.append(dropdown_options[0].get()) #Plant type dropdown
    if dropdown_options[1].get():
        query += " AND `Climate Zones` = %s"
        results.append(dropdown_options[1].get()) #Climate zones dropdown
    if dropdown_options[2].get():
        query += " AND `Flower Colour` = %s"
        results.append(dropdown_options[2].get()) #Flower colour dropdown
    if dropdown_options[3].get():
        query += f" AND `{dropdown_options[3].get()}` = 'Yes'" #Tolerance dropdown
    if dropdown_options[4].get():
        query += f" AND `{dropdown_options[4].get()}` = 'Yes'" #Attracting dropdown
 
    cursor.execute(query, (tuple(results)))
    result = cursor.fetchall()
    mydb.close()

    return result

#Showing advanced search results
def show_plants():

    #Clear existing widgets in the scrollable frame
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    plants = fetch_plant_results()

    for idx, (common_name, botanical_name) in enumerate(plants):
            plant_frame = Frame(scrollable_frame, bg="lightgray", relief=SOLID, borderwidth=1, width=100, height=150)
            plant_frame.grid(row=idx, column=0, padx=10, pady=5, sticky="ew")
            plant_frame.grid_propagate(False)  # Prevent resizing

            # Image
            #image = Image.open(r"C:\Users\linns\OneDrive\Desktop\Relational Database\GardenParadise\Data\cute-pot.png")
            #resize_image = image.resize((30, 30))  # Resize to a larger size if 10x10 is too small
            #img = ImageTk.PhotoImage(resize_image)  # Use ImageTk.PhotoImage, not PhotoImage

            # Add the image to a Label
            #image_label = Label(plant_frame, image=img, bg="lightgray")
            #image_label.image = img  # Keep a reference to prevent garbage collection
            #image_label.pack(anchor="center", padx=5, pady=5)
            

            # Display common name
            common_label = Label(plant_frame, text=f"{common_name}", font=("Arial", 12, "bold"), bg="lightgray")
            common_label.pack(anchor="center", padx=5, pady=2)

            # Display botanical name
            botanical_label = Label(plant_frame, text=f"{botanical_name}", font=("Arial", 12, "italic"), bg="lightgray")
            botanical_label.pack(anchor="center", padx=5, pady=2)

            # More info Button
            more_info_button = Button(plant_frame, text="More info", font=("Arial", 10))
            more_info_button.pack(anchor="center", padx=5, pady=2)


    for i in range(len(dropdown_labels)):
        dropdown_options[i].set("")

#Find plant search button
find_plant_button = Button(search_frame, text="Find plant", font=("Arial", 12), command=show_plants)
find_plant_button.grid(padx=10, pady=10)


window.mainloop()














