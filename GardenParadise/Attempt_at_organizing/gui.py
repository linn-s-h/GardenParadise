from tkinter import *
from tkinter import messagebox
import GardenParadise.Attempt_at_organizing.db_methods as db_methods # import db_methods for database interactions
import user_auth # user auth functions

# Global variables to keep track of login status
logged_in = False
logged_in_user = ""
user_first_name = ""
user_last_name = ""

window = Tk()
window.geometry("1000x800")
window.title("Garden Paradise")

# Configure rows and columns for proportional resizing
window.grid_columnconfigure(0, weight=1) #1/5
window.grid_columnconfigure(1, weight=15) #4/5
window.grid_rowconfigure(0, weight=1) #1/4
window.grid_rowconfigure(1, weight=100) #3/4

# Menu frame
menu_frame = Frame(window, bg="#06402B")
menu_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

# Search frame
search_frame = Frame(window, bg="#F2F0EF")
search_frame.grid(row=1, column=0, sticky="nsew")

search_frame.grid_columnconfigure(0, weight=1)  # Left padding
search_frame.grid_columnconfigure(1, weight=2)  # Content
search_frame.grid_columnconfigure(2, weight=1)  # Right padding

# Result frame
result_frame = Frame(window, bg="white")
result_frame.grid(row=1, column=1, sticky="nsew")

# Menu frame content
title_label = Label(menu_frame, text="Garden Paradise", font=("Helvetica", 28, "bold"), bg="#06402B", fg="white")
title_label.pack(padx=20, pady=20, side="left")

buttons_frame = Frame(menu_frame, bg="#06402B")
buttons_frame.pack(side="right", fill="y", padx=20)

logged_in = False

# Function that changes login status
def change_login_status(status):
    global logged_in 
    logged_in = False
    update_menu_buttons()

# Function to handle user signup
def sign_up_user(username, first_name, last_name, password, confirm_password, sign_up_window):
    if not username or not password or not confirm_password:
        messagebox.showerror("Error", "All fields are required")
        return
    
    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match!")
        return
    
    try:
        mydb, cursor = db_methods.connectDB()

        # Check if username already exists
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            messagebox.showerror("Error", "Username already exists")
            return

        query = "INSERT INTO users (username, first_name, last_name, `password`) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (username, first_name, last_name, password))
        mydb.commit()

        messagebox.showinfo("Success", "Account created successfully!")
        sign_up_window.destroy()
    except Exception as e:
        print(f"Error: {e}")
        messagebox.showerror("Database Error", f"An error occurred: {e}")
    finally:
        if mydb:
            mydb.close()

# Function that opens the sign-up screen
def open_sign_up_screen():
    sign_up_window = Toplevel()
    sign_up_window.geometry("400x400")
    sign_up_window.title("Signing up")

    title_frame = Frame(sign_up_window, bg="#F2F0EF")
    title_frame.place(relx=0, rely=0, relheight=0.25, relwidth=1, anchor="nw")

    main_frame = Frame(sign_up_window, bg="#F2F0EF")
    main_frame.place(relx=0, rely=0.25, relheight=0.65, relwidth=1, anchor="nw")

    bottom_frame = Frame(sign_up_window, bg="#06402B")
    bottom_frame.place(relx=0, rely=0.9, relheight=0.1, relwidth=1, anchor="nw")

    title_container = Frame(title_frame, bg="#F2F0EF")
    title_container.pack(expand=True)

    main_container = Frame(main_frame, bg="#F2F0EF")
    main_container.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    app_title = Label(title_container, text="Garden Paradise", font=("Helvetica", 24, "bold"), fg="#06402B")
    app_title.pack(padx=10, pady=10)

    sign_up_title = Label(title_container, text="Create an account", font=("Arial", 12, "bold"))
    sign_up_title.pack(padx=10, pady=10)

    username_label = Label(main_container, text="Username:", font=("Arial", 10))
    username_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    username_entry = Entry(main_container)
    username_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

    first_name_label = Label(main_container, text="First Name:", font=("Arial", 10))
    first_name_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
    first_name_entry = Entry(main_container)
    first_name_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

    last_name_label = Label(main_container, text="Last Name:", font=("Arial", 10))
    last_name_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
    last_name_entry = Entry(main_container)
    last_name_entry.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

    password_label = Label(main_container, text="Password:", font=("Arial", 10))
    password_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
    password_entry = Entry(main_container, show="*")
    password_entry.grid(row=5, column=1, padx=10, pady=5, sticky="ew")

    confirm_password_label = Label(main_container, text="Confirm Password:", font=("Arial", 10))
    confirm_password_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")
    confirm_password_entry = Entry(main_container, show="*")
    confirm_password_entry.grid(row=6, column=1, padx=10, pady=5, sticky="ew")

    sign_up_button = Button(main_container, text="Sign up", font=("Arial", 10, "bold"),
                                fg="white", bg="#06402B", command=lambda: sign_up_user(
                                    username_entry.get(),
                                    first_name_entry.get(),
                                    last_name_entry.get(),
                                    password_entry.get(),
                                    confirm_password_entry.get(),
                                    sign_up_window
                                ))
    sign_up_button.grid(row=7, column=0, columnspan=2, padx=10, pady=20)

    # Bind the Enter key to trigger the sign-up function
    sign_up_window.bind('<Return>', lambda event: sign_up_user(
        username_entry.get(), first_name_entry.get(), last_name_entry.get(), password_entry.get(), confirm_password_entry.get(),
        sign_up_window))

    sign_up_container = Frame(bottom_frame, bg="#06402B")
    sign_up_container.pack(expand=True)
    
    sign_up_text = Label(sign_up_container, text="Already have an account?", font=("Arial", 10, "bold"), fg="white", bg="#06402B")
    sign_up_text.pack(padx=10, pady=10, side="left")

    login_button = Button(sign_up_container, text="Login", font=("Arial", 10, "bold"), fg="#06402B", bg="white", command=open_login_screen)
    login_button.pack(padx=10, pady=10, side="left")

# Function to check if login credentials match a registered user in the database
def validate_login(username, password, login_window):
    global logged_in, logged_in_user, user_first_name, user_last_name
    try:
        mydb, cursor = db_methods.connectDB()

        query = "SELECT * FROM users WHERE username = %s and password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:
            logged_in = True
            logged_in_user = user[1]  # Assuming the username is in the second column
            user_first_name = user[2]  # First name in third column
            user_last_name = user[3]   # Last name in fourth column
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

# Function that opens the login screen
def open_login_screen():
    login_window = Toplevel()
    login_window.geometry("600x500")
    login_window.title("Logging in") 

    # Content of the screen
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

    # Initializes user and password entry boxes
    username_entry = Entry(main_container, text="Username")
    username_entry.delete(0, END)  # Clear the username field
    username_entry.insert(0, "Username")
    username_entry.pack(padx=10, pady=10, side="top")

    password_entry = Entry(main_container, show="*", text="Password")
    password_entry.delete(0, END)  # Clear the password field
    password_entry.insert(0, "Password")
    password_entry.pack(padx=10, pady=10, side="top")

    # Event handlers to clear text when clicked
    def on_username_click(event):
        if username_entry.get() == "Username":
            username_entry.delete(0, END)

    def on_password_click(event):
        if password_entry.get() == "Password":
            password_entry.delete(0, END)

    # Bind the focus event to the entries
    username_entry.bind("<FocusIn>", on_username_click)
    password_entry.bind("<FocusIn>", on_password_click)

    # Event handlers to reset text when focus is lost
    def on_username_blur(event):
        if username_entry.get() == "":
            username_entry.insert(0, "Username")

    def on_password_blur(event):
        if password_entry.get() == "":
            password_entry.insert(0, "Password")

    # Bind focus-out event to entries
    username_entry.bind("<FocusOut>", on_username_blur)
    password_entry.bind("<FocusOut>", on_password_blur)

    # Login button
    login_button = Button(main_container, text="Login", font=("Arial", 10, "bold"), fg="white", bg="#06402B", 
                             command=lambda: validate_login(username_entry.get(), password_entry.get(), login_window))
    login_button.pack(padx=10, pady=10, side="top")

    # Sign-up prompt
    sign_up_text = Label(sign_up_container, text="Don't have an account yet?", font=("Arial", 10, "bold"), fg="white", bg="#06402B")
    sign_up_text.pack(padx=10, pady=10, side="left")

    sign_up_button = Button(sign_up_container, text="Sign up", font=("Arial", 10, "bold"), fg="#06402B", bg="white", command=open_sign_up_screen)
    sign_up_button.pack(padx=10, pady=10, side="left")

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
        
        welcome_label = Label(buttons_frame, text="Welcome to your new paradise!", font=("Arial", 14), bg="#06402B", fg="white")
        welcome_label.pack(padx=10, pady=10, side="right")

    else:
        log_out_button = Button(buttons_frame, text="Log out", font=("Arial", 12), command=log_out)
        log_out_button.pack(padx=10, pady=20, side="right")
        favorites_button = Button(buttons_frame, text="Your favorites", font=("Arial", 12), command=open_favorites_screen)
        favorites_button.pack(padx=10, pady=20, side="right")

        welcome_label = Label(buttons_frame, text=f"Welcome, {user_first_name} {user_last_name}", font=("Arial", 14), bg="#06402B", fg="white")
        welcome_label.pack(padx=10, pady=10, side="right")

