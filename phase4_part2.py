"""
Name :  N'din Assi 
Course: CIS 216 
Course name: Object Oriented Programming 1. 
Phase 4
"""

import os

class Login:
    """Class to manage user authentication and authorization."""
    
    def __init__(self, user_id, password, authorization):
        self.user_id = user_id
        self.password = password
        self.authorization = authorization

    def __str__(self):
        return f"User ID: {self.user_id}, Role: {self.authorization}"


def load_users():
    """Loads users from a file and returns a dictionary of users."""
    users = {}
    if os.path.exists("users.txt"):
        with open("users.txt", "r") as file:
            for line in file:
                user_id, password, auth = line.strip().split("|")
                users[user_id] = {"password": password, "authorization": auth}
    return users


def save_user(user_id, password, authorization):
    """Saves a new user to the file."""
    with open("users.txt", "a") as file:
        file.write(f"{user_id}|{password}|{authorization}\n")


def register_users():
    """Allows admins to register users until 'End' is entered."""
    users = load_users()
    
    while True:
        user_id = input("\nEnter new User ID (or type 'End' to stop): ").strip()
        if user_id.lower() == "end":
            break
        if user_id in users:
            print("Error: User ID already exists!")
            continue

        password = input("Enter Password: ").strip()
        authorization = input("Enter Authorization (Admin/User): ").strip().capitalize()
        
        if authorization not in ["Admin", "User"]:
            print("Error: Authorization must be 'Admin' or 'User'!")
            continue

        save_user(user_id, password, authorization)
        users[user_id] = {"password": password, "authorization": authorization}
        print("User successfully registered!")


def display_users():
    """Displays all registered users from the file."""
    users = load_users()
    print("\nRegistered Users:")
    for user_id, info in users.items():
        print(f"User ID: {user_id}, Password: {info['password']}, Role: {info['authorization']}")


def login():
    """Handles the login process and returns a Login object if successful."""
    users = load_users()
    
    user_id = input("Enter User ID: ").strip()
    if user_id not in users:
        print("Error: User ID not found. Exiting...")
        return None

    password = input("Enter Password: ").strip()
    if users[user_id]["password"] != password:
        print("Error: Incorrect password. Exiting...")
        return None

    print(f"\nLogin Successful! Welcome, {user_id} ({users[user_id]['authorization']}).\n")
    return Login(user_id, password, users[user_id]["authorization"])


def main():
    """Main function to control the application's flow."""
    print("Welcome to the Secure Application!\n")
    
    user = login()
    if not user:
        return  # Exit if login failed

    if user.authorization == "Admin":
        while True:
            print("\nAdmin Menu:")
            print("1. Register New Users")
            print("2. Display All Users")
            print("3. Logout")

            choice = input("Select an option: ").strip()
            if choice == "1":
                register_users()
            elif choice == "2":
                display_users()
            elif choice == "3":
                print("Logging out... Goodbye!")
                break
            else:
                print("Invalid choice! Try again.")

    elif user.authorization == "User":
        print("\nYou have 'User' access. You can only view users.")
        display_users()
        print("\nLogging out... Goodbye!")


if __name__ == "__main__":
    main()
