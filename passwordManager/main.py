# Project Title : Password Manager
# Programming Language : Python
# Programmer / Author : Keith Ralph Poncardas
# Date Launched : February 16, 2023

import sqlite3
import csv
import os
from prettytable import PrettyTable
x = PrettyTable()

# ASCII ART DISPLAY
ascii_art = r'''

__________                                             .___    _____                                            
\______   _____    ______ _______  _  _____________  __| _/   /     \ _____    ____ _____    ____   ___________ 
 |     ___\__  \  /  ___//  ___\ \/ \/ /  _ \_  __ \/ __ |   /  \ /  \\__  \  /    \\__  \  / ___\_/ __ \_  __ \
 |    |    / __ \_\___ \ \___ \ \     (  <_> |  | \/ /_/ |  /    Y    \/ __ \|   |  \/ __ \/ /_/  \  ___/|  | \/
 |____|   (____  /____  /____  > \/\_/ \____/|__|  \____ |  \____|__  (____  |___|  (____  \___  / \___  |__|   
               \/     \/     \/                         \/          \/     \/     \/     \/_____/      \/       
     
'''

print(ascii_art)
print("Developer : Keith Ralph Poncardas (⌐■_■)")
print("Visit My Website : https://keithponcardas.netlify.app (*′☉.̫☉)")
print("")

# DISPLAY MENU
def display_menu():
    print("=== SELECTION ===")
    print("[1] Log In")
    print("[2] Terminate Program")

# GET USER CHOICE
def get_user_choice():
    while True:
        choice = input(">>> Enter Your Choice: ").strip()
        if choice.isdigit():
            choice = int(choice)
            if choice in [1, 2]:
                return choice
            else:
                print("Invalid Choice, Please Enter 1 Or 2.")
        elif choice == '':
            print("No Input Detected, Try Again.")
        else:
            print("Invalid Input, Try Again.")

# CREATE DATABASE FILE
def create_connection(db_file):
    """Create a database connection to the SQLite database specified by the db_file."""
    conn = None
    try:
        documents_folder = os.path.expanduser("D:\Default Folder\Documents")

        database_folder = os.path.join(documents_folder, "Credentials Folder")
        if not os.path.exists(database_folder):
            os.makedirs(database_folder)

        db_path = os.path.join(database_folder, db_file)

        conn = sqlite3.connect(db_path)
        print(f"Connected to database: {db_path}")
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

# CREATE TABLE FOR DATABASE
def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
        """)
        # print("Table 'users' created successfully.")
    except sqlite3.Error as e:
        print(e)

# ADD CREDENTIALS TO DATABASE
def add_user(conn, username, password):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        print(f"User '{username}' added successfully.")
    except sqlite3.Error as e:
        print(e)

# REMOVE CREDENTIAL(S) TO DATABASE
def remove_user(conn, username):
    try:
        cursor = conn.cursor()

        # Check if the username exists
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        existing_user = cursor.fetchone()

        if not existing_user:
            print(f"User '{username}' does not exist in the database.")
            return

        # Remove the user
        cursor.execute("DELETE FROM users WHERE username=?", (username,))
        conn.commit()
        print(f"User '{username}' removed successfully.")
    except sqlite3.Error as e:
        print(e)


# SHOW THE LIST OF CREDENTIALS FROM DATABASE
def show_users(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        if len(rows) == 0:
            print("No users available.")
        else:
            table = PrettyTable()
            table.field_names = ["Username", "Password"]
            for row in rows:
                table.add_row([row[1], row[2]])
            print("User List:")
            print(table)
    except sqlite3.Error as e:
        print(e)

# EXPORT CREDENTIALS TO CSV FORMAT
def export_to_csv(conn, filename, directory):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        if len(rows) == 0:
            print("No users available to export.")
            return
        filepath = os.path.join(directory, filename)
        with open(filepath, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['ID', 'Username', 'Password'])
            csv_writer.writerows(rows)
        print(f"User data exported to '{filepath}' successfully!")
    except sqlite3.Error as e:
        print(e)

# ADD USER INPUT USN & PASS TO DATABASE
def add_credentials(conn):
    while True:
        username = input("Enter Username: ").strip()
        password = input("Enter Password: ").strip()

        if not username or not password:
            print("Username Or Password Cannot Be Empty, Please Try Again.")
            continue

        return add_user(conn, username, password)

# REMOVE CREDENTIALS BY INDICATING USERNAME
def remove_credentials(conn):
    while True:
        username = input(">>> Enter Username You Want To Remove: ").strip()

        if not username:
            print("Username Or Password Cannot Be Empty, Please Try Again.")
            continue

        return remove_user(conn, username)

# MAIN SELECTION PROCESS
def main_selection_process():
    database = "users.db"
    conn = create_connection(database)
    if conn is not None:
        create_table(conn)
        while True:
            print("\nSELECTION")
            print("[1] Add User")
            print("[2] Remove User")
            print("[3] Show User List")
            print("[4] Export User Data to CSV")
            print("[5] Exit")
            choice = input(">>> Enter your choice: ").strip()
            if choice == '1':
                add_credentials(conn)
            elif choice == '2':
                remove_credentials(conn)
            elif choice == '3':
                show_users(conn)
            elif choice == '4':
                filename = input(">>> Enter filename to export: ").strip()
                directory = "E:\Default Folder\Downloads"
                if not directory:
                    directory = os.getcwd()
                filename = f"{filename}.csv"
                export_to_csv(conn, filename, directory)
            elif choice == '5':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please enter a valid option.")

        conn.close()
        print("Connection to database closed.")

# AUTHENTICATE USER
def authenticate_user():

    valid_username = "keith"
    valid_password = "keith123"

    while True:
        username = input(">>> Enter Username: ").strip()
        password = input(">>> Enter Password: ").strip()

        if not username or not password:
            print("Username Or Password Cannot Be Empty, Please Try Again.")
            continue

        if username == valid_username and password == valid_password:
            print("Logged In Successfuly!")
            main_selection_process()
            return
        else:
            print("Invalid Username Or Password, Please Try Again")

# MAIN
def main():
    display_menu()
    choice = get_user_choice()

    if choice == 1:
        authenticate_user()
    elif choice == 2:
        print("Program Terminated . . .")

# INITIATING MAIN FUNCTION
if __name__ == "__main__":
    main()