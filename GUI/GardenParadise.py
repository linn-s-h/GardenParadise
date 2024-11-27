
from tkinter import *
import sys
import queries

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
search_entry = Entry(search_frame, text="Search common name or botanical name", font=("Arial", 12))
search_entry.grid(row=0, column=0, padx=(5, 10), pady=10, sticky="ew")  # Place in grid

search_button = Button(search_frame, text="Search", font=("Arial", 12))
search_button.grid(row=1, column=0, padx=(5, 10), pady=10)  # Place next to entry


#Dropdown manues in result frame
items_plant_type =  queries.get_distinct_values(f"`Plant Type`")
items_climate_zones = queries.get_distinct_values(f"`Climate Zones`")
items_flower_colour = queries.get_distinct_values(f"`Flower Colour`")
items_tolerance = queries.get_column_values(f"tolerance")
items_attracting = queries.get_column_values(f"attracting")

#Option selected
option_plant_type = StringVar()
option_plant_type.set("")
option_climate_zones = StringVar()
option_climate_zones.set("")
option_flower_colour = StringVar()
option_flower_colour.set("")
option_tolerance = StringVar()
option_tolerance.set("")
option_attracting = StringVar()
option_attracting.set("")


#Plant Type Dropmenu
dropmenu_plant_type = OptionMenu(search_frame, option_plant_type, *items_plant_type, command=lambda _: update_dropdown())
dropmenu_plant_type.config(width=20, bg="white")
dropmenu_plant_type.grid(padx=10, pady=10, row=3, column=0)

#Climate Zones Dropmenu
dropmenu_climate_zones = OptionMenu(search_frame, option_climate_zones, *items_climate_zones, command=lambda _: update_dropdown())
dropmenu_climate_zones.config(width=20, bg="white")
dropmenu_climate_zones.grid(padx=10, pady=10, row=4, column=0)

#Flower Colour Dropmenu
dropmenu_flower_colour = OptionMenu(search_frame, option_flower_colour, *items_flower_colour, command=lambda _: update_dropdown())
dropmenu_flower_colour.config(width=20, bg="white")
dropmenu_flower_colour.grid(padx=10, pady=10, row=5, column=0)

#Tolerance Dropmenu
dropmenu_tolerance = OptionMenu(search_frame, option_tolerance, *items_tolerance, command=lambda _: update_dropdown())
dropmenu_tolerance.config(width=20, bg="white")
dropmenu_tolerance.grid(padx=10, pady=10, row=6, column=0)

#Attracting Dropmenu
dropmenu_attracting = OptionMenu(search_frame, option_attracting, *items_attracting, command=lambda _: update_dropdown())
dropmenu_attracting.config(width=20, bg="white")
dropmenu_attracting.grid(padx=10, pady=10, row=7, column=0)


def show_plants():
    Label(result_frame, text=option_plant_type.get()).pack()
    option_plant_type.set("")
    option_climate_zones.set("")
    option_flower_colour.set("")
    option_tolerance.set("")
    option_attracting.set("")

find_plant_button = Button(search_frame, text="Find plant", font=("Arial", 12), command=show_plants)
find_plant_button.grid(padx=10, pady=10)

window.mainloop()