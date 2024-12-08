from GardenParadise.Attempt_at_organizing.db_methods import connectDB
from tkinter import *

# Getting results from advanced search
def fetch_plant_results(dropdown_options):
    mydb, cursor = connectDB()
    results = []
    query = """
        SELECT `Common Name`, `Botanical Name`, `Plant ID`
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
    
    cursor.execute(query, tuple(results))
    result = cursor.fetchall()
    mydb.close()
    return result

# function that shows more details of a selected plant
def show_selected_plant(plant_id):
    mydb, cursor = connectDB()
    query = """
    SELECT `Common Name`, `Botanical Name`, `Plant Type`, `Climate Zones`, `Flower Colour`, `Water Needs`, `Light Needs`, `Soil Type`, `Maintenance`, `Foliage Colour`, `Perfume`, `Aromatic`, `Edible`, `Notes`
    FROM plants
    WHERE `Plant ID` = %s
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
        path = get_image_path(plant_id)
        image = Image.open(path)
        #print(f"Retrieved path for Plant ID {plant_id}: {path}")
        resize_image = image.resize((100, 100)) 
        img = ImageTk.PhotoImage(resize_image) 

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