from GardenParadise.Attempt_at_organizing.db_methods import connectDB
from tkinter import messagebox
from gui import update_menu_buttons

logged_in = False
user_first_name = ""
user_last_name = ""

# Function that registers the user into the user table
def sign_up_user(username, first_name, last_name, password, confirm_password, sign_up_window):
    if not username or not password or not confirm_password:
        messagebox.showerror("Error", "All fields are required")
        return
    
    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match!")
        return
    
    try:
        mydb, cursor = connectDB()

        # Check if username already exists
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        existing_user=cursor.fetchone()

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

def log_out():
    global logged_in
    logged_in = False
    messagebox.showinfo("Logged Out", "You have successfully logged out.")
    update_menu_buttons()

