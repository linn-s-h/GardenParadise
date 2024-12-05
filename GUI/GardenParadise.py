import mysql.connector
from tkinter import *
from tkinter import PhotoImage
from PIL import Image, ImageTk

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "Clownpokemon8"
DB_DATABASE = "mydb"

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
    cursor.execute(query, (f"%{column_name}%",))
    values = [row[0] for row in cursor.fetchall()]
    mydb.close()
    return values

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

    query += " LIMIT 16;"
    
    cursor.execute(query, (tuple(results)))
    values = cursor.fetchall()
    mydb.close()
    return values

#Getting plant results from search bar entry
def get_plants_by_search(plant_name):
    mydb, cursor = connectDB()
    query = """
    SELECT `Common Name`, `Botanical Name`
    FROM plants
    WHERE `Common Name` LIKE %s OR `Botanical Name` LIKE %s
    ORDER BY `Common Name` ASC
    LIMIT 16;
    """
    cursor.execute(query, (f"%{plant_name}%", f"%{plant_name}%",))
    values = cursor.fetchall()
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

search_frame.grid_columnconfigure(0, weight=1)  # Left padding
search_frame.grid_columnconfigure(1, weight=2)  # Content
search_frame.grid_columnconfigure(2, weight=1)  # Right padding

#Result frame
result_frame = Frame(window, bg= "white")
result_frame.grid(row=1, column=1, sticky="nsew")

#Menu frame content
title_label = Label(menu_frame, text="Garden Paradise", font=("Helvetica", 28, "bold"), bg="#06402B", fg="white")
title_label.pack(padx=20, pady=20, side="left")

#Search frame content
search_entry = Entry(search_frame)
search_entry.grid(row=0, column=0, padx=(10, 10), pady=10, sticky="ew")  # Place in grid

#Scrollbar
scrollbar_frame = Frame(result_frame)
scrollbar_frame.pack(fill=BOTH, expand=1)

scrollbar_canvas = Canvas(scrollbar_frame, bg="white")
scrollbar_canvas.pack( side=LEFT, fill=BOTH, expand=1)

scrollbar = Scrollbar(scrollbar_frame, orient=VERTICAL, command=scrollbar_canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)

scrollbar_canvas.configure(yscrollcommand=scrollbar.set)
scrollable_frame = Frame(scrollbar_canvas, bg="white") #Creating a frame inside the canvas

scrollable_frame.place(relx=1, rely=1, relwidth=1, relheight=1)
scrollbar_canvas.create_window((0,0), window=scrollable_frame, anchor=NW) #Adding the scrollable frame to the canvas

def update_scrollregion(event=None): #Update the scrollregion whenever the content of scrollable_frame changes
    scrollbar_canvas.configure(scrollregion=scrollbar_canvas.bbox("all"))

scrollable_frame.bind('<Configure>', update_scrollregion)

#Advanced setting label
advanced_search_label = Label(search_frame, text="Advanced search", font=("Arial", 16, "bold"))
advanced_search_label.grid(padx=10, pady=(20, 10), row=2, column=0)

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
    title_label = Label(search_frame, text=dropdown_labels[i], font=("Arial", 10, "bold"), bg="#F2F0EF")
    title_label.grid(row=3 + (2 * i), column=0, padx=10, sticky="ew")

    dropdown = OptionMenu(search_frame, dropdown_options[i], *items[i]) 
    dropdown.config(width=20, bg="white")
    dropdown.grid(row=4 + (2 * i), column=0, padx=10, pady=(0, 20), sticky="ew")

#Getting results from advanced search
def fetch_plant_results():

    mydb, cursor = connectDB()
    results = []
    query = """
        SELECT `Common Name`, `Botanical Name`, `plant_id`
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
        query += f" AND `{dropdown_options[3].get()}` != 'Unknown'" #Tolerance dropdown #Can be Yes, Light, Medium, High
    if dropdown_options[4].get():
        query += f" AND `{dropdown_options[4].get()}` = 'Yes'" #Attracting dropdown

    query += " LIMIT 16;"
    
    cursor.execute(query, (tuple(results)))
    result = cursor.fetchall()
    mydb.close()

    return result

# Joaquin do this
def show_selected_plant(plant_id):
    # Connect to the database and fetch details for the selected plant
    mydb, cursor = connectDB()
    
    query = """
    SELECT `Common Name`, `Botanical Name`, `Plant Type`, `Climate Zones`, `Flower Colour`
    FROM plants
    WHERE `plant_id` = %s
    """
    cursor.execute(query, (plant_id,))
    plant_details = cursor.fetchone()  # Fetch the details of the selected plant
    
    mydb.close()   

    if plant_details:# plant_details:
        plant_window = Toplevel()
        plant_window.title("")
        plant_window.geometry("600x500")
       
       # Display the details in the new window
        common_name_label = Label(plant_window, text=f"Common Name: {plant_details[0]}", font=("Arial", 14))
        common_name_label.pack(pady=10)

        botanical_name_label = Label(plant_window, text=f"Botanical Name: {plant_details[1]}", font=("Arial", 14))
        botanical_name_label.pack(pady=10)
    else:
        print("No details found for this plant.")


#GUI function that displays the plants after search in scrollable_frame
def show_plants(plants):

    if not plants:
        label = Label(scrollable_frame, text="No products were found matching your selection.", font=("Arial", 12), bg="white")
        label.place(relx=0.5, rely=0.2, anchor="center")
        return
    else:
        for row_idx, (common_name, botanical_name, plant_id) in enumerate(plants):
            column_count = row_idx % 3
            plant_frame = Frame(scrollable_frame, bg="lightgray", relief=SOLID, borderwidth=1)
            plant_frame.grid(row=row_idx // 3, column=column_count, padx=10, pady=10, sticky="nsew")

            # Image
            image = Image.open(r"/Users/joaquingarcia/Documents/31305 Relational Databases/GardenParadise/Data/cute-pot.png")
            resize_image = image.resize((80, 80))  # Resize to a larger size if 10x10 is too small
            img = ImageTk.PhotoImage(resize_image)  # Use ImageTk.PhotoImage, not PhotoImage

            # Add the image to a Label
            image_label = Label(plant_frame, image=img, bg="lightgray")
            image_label.image = img  #Keep a reference to prevent garbage collection
            image_label.pack(anchor="center", padx=5, pady=5)
                
            # Display common name
            common_label = Label(plant_frame, text=f"{common_name}", font=("Arial", 12, "bold"), bg="lightgray")
            common_label.pack(anchor="center", padx=5, pady=2)

            # Display botanical name
            botanical_label = Label(plant_frame, text=f"{botanical_name}", font=("Arial", 12, "italic"), bg="lightgray")
            botanical_label.pack(anchor="center", padx=5, pady=2)

            # More info Button
            more_info_button = Button(plant_frame, text="More info", font=("Arial", 8), command=lambda plant_id=plant_id: show_selected_plant(plant_id))
            more_info_button.pack(anchor="center", padx=5, pady=10)


#Clear existing widgets in the scrollable frame and entry
def clear_entry_and_frame():
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
    search_entry.delete(0, 'end')

def clear_frame():
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
    for i in range(len(dropdown_labels)):
        dropdown_options[i].set("")

def clear_all_search(): 
    clear_entry_and_frame() 
    for i in range(len(dropdown_labels)):
        dropdown_options[i].set("")

#Showing advanced search results
def show_advanced_search():

    clear_entry_and_frame()
    plants = fetch_plant_results()
    show_plants(plants)

def show_entry_search(event=None):

    clear_frame()
    plant_name = search_entry.get().strip()
    plants = get_plants_by_search(plant_name)
    show_plants(plants)

#Find plant search button
find_plant_button = Button(search_frame, text="Find plant", font=("Arial", 12), command=show_advanced_search)
find_plant_button.grid(padx=10, pady=10)

clear_button = Button(search_frame, text="Clear all", font=("Arial", 12, "bold"), bg="#06402B", fg="white", command=clear_all_search)
clear_button.place(relx=0.5, rely=0.95, anchor="s")

#Search plant button
search_button = Button(search_frame, text="Search", font=("Arial", 12), command=show_entry_search)
search_button.grid(row=1, column=0, padx=(10, 10), pady=10)  # Place next to entry
search_entry.bind('<Return>', show_entry_search)



window.mainloop()














