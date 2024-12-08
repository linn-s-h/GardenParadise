import mysql.connector
from tkinter import *
from tkinter import PhotoImage
from tkinter import messagebox
from PIL import Image, ImageTk

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "Clownpokemon8"
DB_DATABASE = "mydb"
logged_in_user = None
user_first_name = None
user_last_name = None

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


#Getting plant results from search bar entry
def get_plants_by_search(plant_name):
    mydb, cursor = connectDB()
    query = """
    SELECT `Common Name`, `Botanical Name`, `plant_id`
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
    cursor.execute(query, (f"{plant_id}"))
    value = mydb.close()
    return value



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

buttons_frame = Frame(menu_frame, bg="#06402B")
buttons_frame.pack(side="right", fill="y", padx=20)

logged_in = False

#Function that changes status of log in
def change_login_status(status):
    global logged_in 
    logged_in = False
    update_menu_buttons()

#Function that opens a sign up screen
def open_sign_up_screen():
    sign_up_window = Toplevel()
    sign_up_window.geometry("600x500")
    sign_up_window.title("Signing up")

# check if login credentials match a registered user in the database
def validate_login(username, password, login_window):
    global logged_in, logged_in_user, user_first_name, user_last_name
    try:
        mydb, cursor = connectDB()

        query = "SELECT * FROM users WHERE username = %s and password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:
            logged_in = True
            logged_in_user = user[1]
            user_first_name = user[2]
            user_last_name = user[3]
            messagebox.showinfo("Login Successful", f"Welcome, {user_first_name} {user_last_name}!")
            login_window.destroy()
            update_menu_buttons()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")
            return False

    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        if mydb:
            mydb.close()

#Function that opens a log in screen
def open_login_screen():
    login_window = Toplevel()
    login_window.geometry("600x500")
    login_window.title("Logging in") 

    #Content of screen
    main_frame = Frame(login_window, bg="#F2F0EF")
    main_frame.place(relx=0, rely=0, relheight=0.9, relwidth=1, anchor="nw")  # Top-left alignment for main frame

    bottom_frame = Frame(login_window, bg="#06402B")
    bottom_frame.place(relx=0, rely=0.9, relheight=0.1, relwidth=1, anchor="nw")

    main_container = Frame(main_frame, bg="#F2F0EF")
    main_container.pack(expand=True)

    sign_up_container = Frame(bottom_frame, bg="#06402B")
    sign_up_container.pack(expand=True)

    app_title = Label(main_container, text="Garden Paradise", font=("Helvetica", 24, "bold"), fg="#06402B")
    app_title.pack(padx=10, pady=10, side="top")
    login_title = Label(main_container, text="Login", font=("Arial", 12, "bold"))
    login_title.pack(padx=10, pady=10, side="top")
    username_entry = Entry(main_container)
    username_entry.pack(padx=10, pady=10, side="top")
    password_entry = Entry(main_container, show="*")
    password_entry.pack(padx=10, pady=10, side="top")

    login_button = Button(main_container, text="Login", font=("Arial", 10, "bold"), fg="white", bg="#06402B", command=lambda:validate_login(username_entry.get(),password_entry.get(), login_window))
    login_button.pack(padx=10, pady=10, side="top")

    sign_up_text = Label(sign_up_container, text="Don't have an account yet?", font=("Arial", 10, "bold"), fg="white", bg="#06402B")
    sign_up_text.pack(padx=10, pady=10, side="left")
    sign_up_button = Button(sign_up_container, text="Sign up", font=("Arial", 10, "bold"), fg="#06402B", bg="white", command=open_sign_up_screen)
    sign_up_button.pack(padx=10, pady=10, side="left")

    


#Function that alters staus when logging out   
def log_out():
    global logged_in
    logged_in = False
    messagebox.showinfo("Logged Out", "You have successfully logged out.")
    update_menu_buttons()

#Function that opens favorites screen
def open_favorites_screen():
    favorites_window = Toplevel()
    favorites_window.geometry("600x500")
    favorites_window.title("Your favorites")

#Function that updates the displayed menu buttons depending on the login status
def update_menu_buttons():
    """Update the buttons in the menu based on login status."""
    global buttons_frame
    for widget in buttons_frame.winfo_children(): 
        widget.destroy() #Delete existing widgets 

    if not logged_in:
        sign_up_button = Button(buttons_frame, text="Sign up", font=("Arial", 12), command=open_sign_up_screen)
        sign_up_button.pack(padx=10, pady=20, side="right")
        login_button = Button(buttons_frame, text="Login", font=("Arial", 12), command=open_login_screen)
        login_button.pack(padx=10, pady=20, side="right")
        
        welcome_label = Label(buttons_frame, text="Welcome", font=("Arial", 14), bg="#06402B", fg="white")
        welcome_label.pack(padx=10, pady=10, side="right")

    else:
        log_out_button = Button(buttons_frame, text="Log out", font=("Arial", 12), command=log_out)
        log_out_button.pack(padx=10, pady=20, side="right")
        favorites_button = Button(buttons_frame, text="Your favorites", font=("Arial", 12), command=open_favorites_screen)
        favorites_button.pack(padx=10, pady=20, side="right")

        welcome_label = Label(buttons_frame, text=f"Welcome, {user_first_name} {user_last_name}", font=("Arial", 14), bg="#06402B", fg="white")
        welcome_label.pack(padx=10, pady=10, side="right")

update_menu_buttons()

#Search frame content
search_entry = Entry(search_frame, font=("Arial", 12))
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

# function that shows more details of a selected plant
def show_selected_plant(plant_id):
    # Connect to the database and fetch details for the selected plant
    mydb, cursor = connectDB()
    
    query = """
    SELECT `Common Name`, `Botanical Name`, `Plant Type`, `Climate Zones`, `Flower Colour`, `Water Needs`, `Light Needs`, `Soil Type`, `Maintenance`, `Foliage Colour`, `Perfume`, `Aromatic`, `Edible`, `Notes`
    FROM plants
    WHERE `plant_id` = %s;
    """
    cursor.execute(query, (plant_id,))
    plant_details = cursor.fetchone()  # Fetch the details of the selected plant
    
    mydb.close()   

    if plant_details:# plant_details:
        plant_window = Toplevel()
        plant_window.title("")
        plant_window.geometry("700x500")

        # left frame
        left_frame = Frame(plant_window, bg="#06402B")
        left_frame.place(relx=0, rely=0, relwidth=0.3, relheight=1)

        # Display the details in the left frame
        # Add favourites button
        def add_to_favorites():
            # Add logic to save the current plant to favorites
            print("Plant added to favorites!")

        add_to_favorites_button = Button(
            left_frame,
            text="Add to Favorites",
            font=("Arial", 12, "bold"),
            bg="#FF6347",  # Tomato red background
            fg="white",  # White text
            activebackground="#FF4500",  # Slightly darker red when pressed
            activeforeground="white",
            relief="raised",  # Button effect
            borderwidth=2,  # Border thickness
            command=add_to_favorites  # Function to handle button click
        )
        add_to_favorites_button.pack(
            side="bottom",  # Pack at the bottom
            pady=20,  # Add vertical padding
            padx=10,  # Add horizontal padding
            fill="x"  # Make it stretch horizontally
        )


        # Image
        image = Image.open(r"/Users/joaquingarcia/Documents/31305 Relational Databases/GardenParadise/Data/cute-pot.png")
        resize_image = image.resize((100, 100))  # Resize to a larger size if 10x10 is too small
        img = ImageTk.PhotoImage(resize_image)  # Use ImageTk.PhotoImage, not PhotoImage

        # Add the image to a Label
        image_label = Label(left_frame, image=img, bg="white")
        image_label.image = img  #Keep a reference to prevent garbage collection
        image_label.pack(anchor="center", padx=5, pady=30)

        common_name = Label(left_frame, text=f"Common Name", font=("Arial", 13, "bold"), fg="white", bg=left_frame["bg"]) # so frame inherits bg colour
        common_name.pack(pady=5)

        common_name_label = Label(left_frame, text=f"{plant_details[0]}", font=("Arial", 12), fg="white", bg=left_frame["bg"])
        common_name_label.pack(pady=5)

        botanical_name = Label(left_frame, text=f"Botanical Name", font=("Arial", 13, "bold"), fg="white", bg=left_frame["bg"])
        botanical_name.pack(pady=5)
        
        botanical_name_label = Label(left_frame, text=f"{plant_details[1]}", font=("Arial", 12), fg="white", bg=left_frame["bg"])
        botanical_name_label.pack(pady=5)

        plant_type = Label(left_frame, text=f"Plant Type", font=("Arial", 13, "bold"), fg="white", bg=left_frame["bg"])
        plant_type.pack(pady=5)
        
        plant_type_label = Label(left_frame, text=f"{plant_details[2]}", font=("Arial", 12), fg="white", bg=left_frame["bg"])
        plant_type_label.pack(pady=5)

        # right frame
        right_frame = Frame(plant_window, bg="white")
        right_frame.place(relx=0.3, rely=0, relwidth=0.7, relheight=1)

        # Create the top frame for "Maintenance Information"
        top_frame = Frame(right_frame, bg="grey", bd=2, relief="solid")  # Border with grey background
        top_frame.pack(fill="x", padx=10, pady=10, expand=False)

        # Add the label to the top frame
        top_label = Label(top_frame, text="Maintenance Information", font=("Arial", 14, "bold"), bg="grey")
        top_label.pack(pady=5, padx=10)

        maintenance_info_frame = Frame(right_frame, bg=right_frame["bg"])
        maintenance_info_frame.pack(fill="x", padx=10, pady=10)

        # Create the labels and info pairs in a grid layout
        # Row 1 - "Climate Zone" title and info label
        climate_zone = Label(maintenance_info_frame, text="Climate Zone", font=("Arial", 13, "bold"), fg="black", bg=right_frame["bg"]) #make any commas separated with a space
        climate_zone.grid(row=0, column=0, padx=10, pady=5, sticky="w")  # Title in the first row

        climate_zone_label = Label(maintenance_info_frame, text=f"{plant_details[3].replace(',', ', ')}", font=("Arial", 12), fg="black", bg=right_frame["bg"], wraplength=180, justify="left")
        climate_zone_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")  # Info label underneath

        # Row 2 - "Water Needs" title and info label
        water_needs = Label(maintenance_info_frame, text="Water Needs", font=("Arial", 13, "bold"), fg="black", bg=right_frame["bg"])
        water_needs.grid(row=0, column=1, padx=10, pady=5, sticky="w")  # Title in the first row

        water_needs_label = Label(maintenance_info_frame, text=f"{plant_details[5]}", font=("Arial", 12), fg="black", bg=right_frame["bg"])
        water_needs_label.grid(row=1, column=1, padx=10, pady=5, sticky="w")  # Info label underneath

        # Row 3 - "Light Needs" title and info label
        light_needs = Label(maintenance_info_frame, text="Light Needs", font=("Arial", 13, "bold"), fg="black", bg=right_frame["bg"])
        light_needs.grid(row=0, column=2, padx=10, pady=5, sticky="w")  # Title in the first row

        light_needs_label = Label(maintenance_info_frame, text=f"{plant_details[6]}", font=("Arial", 12), fg="black", bg=right_frame["bg"])
        light_needs_label.grid(row=1, column=2, padx=10, pady=5, sticky="w")  # Info label underneath

        # Row 4 - "Soil Type" title and info label
        soil_type = Label(maintenance_info_frame, text="Soil Type", font=("Arial", 13, "bold"), fg="black", bg=right_frame["bg"])
        soil_type.grid(row=2, column=0, padx=10, pady=5, sticky="w")  # Title in the first row

        soil_type_label = Label(maintenance_info_frame, text=f"{plant_details[7].replace(',', ', ')}", font=("Arial", 12), fg="black", bg=right_frame["bg"])
        soil_type_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")  # Info label underneath

        # Row 5 - "Maintenance Level" title and info label
        maintenance = Label(maintenance_info_frame, text="Maintenance Level", font=("Arial", 13, "bold"), fg="black", bg=right_frame["bg"])
        maintenance.grid(row=2, column=1, padx=10, pady=5, sticky="w")  # Title in the first row

        maintenance_label = Label(maintenance_info_frame, text=f"{plant_details[8]}", font=("Arial", 12), fg="black", bg=right_frame["bg"])
        maintenance_label.grid(row=3, column=1, padx=10, pady=5, sticky="w")  # Info label underneath

        # Create the bottom frame for "Plant Characteristics"
        bottom_frame = Frame(right_frame, bg="grey", bd=2, relief="solid")  # Border with grey background
        bottom_frame.pack(fill="x", padx=10, pady=10, expand=False)

        # Add the label to the bottom frame
        bottom_label = Label(bottom_frame, text="Plant Characteristics", font=("Arial", 14, "bold"), bg="grey")
        bottom_label.pack(pady=5, padx=10)

        #plant characteristics frame
        pc_frame = Frame(right_frame, bg=right_frame["bg"])
        pc_frame.pack(fill="x", padx=10, pady=10)

        # Row 1 - "Flower Colour" Title and info label
        flower_color = Label(pc_frame, text=f"Flower Color", font=("Arial", 13, "bold"), fg="black", bg=right_frame["bg"])
        flower_color.grid(row=0, column=0, padx=10, pady=5, sticky="w")  # Title in the first row
        
        flower_color_label = Label(pc_frame, text=f"{plant_details[4]}", font=("Arial", 12), fg="black", bg=right_frame["bg"])
        flower_color_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")  # Info label underneath

        # Row 2 - "Foliage Color" title and info label
        foliage_color = Label(pc_frame, text="Foliage Color", font=("Arial", 13, "bold"), fg="black", bg=right_frame["bg"])
        foliage_color.grid(row=0, column=1, padx=10, pady=5, sticky="w")  # Title in the first row

        foliage_color_label = Label(pc_frame, text=f"{plant_details[9]}", font=("Arial", 12), fg="black", bg=right_frame["bg"])
        foliage_color_label.grid(row=1, column=1, padx=10, pady=5, sticky="w")  # Info label underneath

        # Row 3 - "Perfume" title and info label
        perfume = Label(pc_frame, text="Perfume", font=("Arial", 13, "bold"), fg="black", bg=right_frame["bg"])
        perfume.grid(row=0, column=2, padx=10, pady=5, sticky="w")  # Title in the first row

        perfume_label = Label(pc_frame, text=f"{plant_details[10]}", font=("Arial", 12), fg="black", bg=right_frame["bg"])
        perfume_label.grid(row=1, column=2, padx=10, pady=5, sticky="w")  # Info label underneath

        # Row 4 - "Aromatic" title and info label
        aromatic = Label(pc_frame, text="Aromatic", font=("Arial", 13, "bold"), fg="black", bg=right_frame["bg"])
        aromatic.grid(row=2, column=0, padx=10, pady=5, sticky="w")  # Title in the first row

        aromatic_label = Label(pc_frame, text=f"{plant_details[11].replace(',', ', ')}", font=("Arial", 12), fg="black", bg=right_frame["bg"])
        aromatic_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")  # Info label underneath

        # Row 5 - "Edible" title and info label
        edible = Label(pc_frame, text="Edible", font=("Arial", 13, "bold"), fg="black", bg=right_frame["bg"])
        edible.grid(row=2, column=1, padx=10, pady=5, sticky="w")  # Title in the first row

        edible_label = Label(pc_frame, text=f"{plant_details[12]}", font=("Arial", 12), fg="black", bg=right_frame["bg"])
        edible_label.grid(row=3, column=1, padx=10, pady=5, sticky="w")  # Info label underneath

        # Notes Frame
        notes = Frame(right_frame, bg="grey", bd=2, relief="solid")
        notes.pack(fill="x", padx=10, pady=10, expand=False)

        # Add the label to the top frame
        notes_label = Label(notes, text="Notes:", font=("Arial", 14, "bold"), bg="grey")
        notes_label.pack(pady=5, padx=(10, 0), side="left")

        if plant_details[13]:
            notes_text = plant_details[13]

            text_width = len(notes_text)
            max_width = 50

            if text_width > max_width:
                notes_info = Label(notes, text="Click to view full notes", font=("Arial", 14, "italic"), fg="blue", bg="grey", cursor="hand2")
                notes_info.pack(pady=5, padx=10, side="left")

                def show_full_notes():
                    full_notes_window = Toplevel()
                    full_notes_window.title(f"{plant_details[0]} Notes")

                    full_notes_window.resizable(True, True)
                    
                    full_notes_frame = Frame(full_notes_window, bg="grey")
                    full_notes_frame.pack(fill=BOTH, expand=TRUE)

                    notes_label = Label(full_notes_frame, text="Notes:", font=("Arial", 14, "bold"), anchor="w", bg="grey", justify="left")
                    notes_label.pack(padx=10, pady=(10, 0), fill="x")
                    
                    # Create the label with text wrapping and justification
                    full_notes_label = Label(full_notes_frame, 
                                            text=notes_text, 
                                            font=("Arial", 14), 
                                            wraplength=380, 
                                            justify="left", 
                                            bg="grey", 
                                            anchor="w")  # 'anchor="w"' aligns the text to the left
                    
                    # Add padding around the label
                    full_notes_label.pack(padx=10, pady=(0, 10), fill=BOTH, expand=True)
                
                notes_info.bind("<Button-1>", lambda e: show_full_notes())
            
            else:
                # If the text fits, just show it normally
                notes_info = Label(notes, text=notes_text, font=("Arial", 14), bg="grey")
                notes_info.pack(pady=5, padx=0, side="left")
        else:
            # If there are no notes, display a default message
            no_info = Label(notes, text="No extra notes", font=("Arial", 14), bg="grey")
            no_info.pack(pady=5, side="left")
       
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
            plant_frame.config(width=230, height=230)
            plant_frame.propagate(False)

            # Image
            image = Image.open(r"C:\Users\linns\OneDrive\Desktop\Relational Database\GardenParadise\Data\cute-pot.png")
            resize_image = image.resize((80, 80))  # Resize to a larger size if 10x10 is too small
            img = ImageTk.PhotoImage(resize_image)  # Use ImageTk.PhotoImage, not PhotoImage

            # Add the image to a Label
            image_label = Label(plant_frame, image=img, bg="lightgray")
            image_label.image = img  #Keep a reference to prevent garbage collection
            image_label.pack(anchor="center", padx=5, pady=5)
                
            # Display common name
            common_label = Label(plant_frame, text=f"{common_name}", font=("Arial", 11, "bold"), bg="lightgray")
            common_label.pack(anchor="center", padx=5, pady=2)

            # Display botanical name
            botanical_label = Label(plant_frame, text=f"{botanical_name}", font=("Arial", 11, "italic"), bg="lightgray")
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














