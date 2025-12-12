#Importing modules
import bcrypt
import os
USER_DATA_FILE = "users.txt"  #User details are stored in users.txt
#Function definitions
def hash_password(plain_text_password):        #Function to hash the password
    password_bytes = plain_text_password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")
def verify_password(plain_text_password, hashed_password):
    password_bytes = plain_text_password.encode("utf-8")
    hashed_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hashed_bytes)
def user_exists(username):
    if not os.path.exists(USER_DATA_FILE):
        return False
    with open(USER_DATA_FILE, "r") as file:
        for line in file:
            stored_username = line.strip().split(",")[0]
            if stored_username == username:
                return True
    return False
def register_user(username, password):
    if user_exists(username):
        print(f"Error: Username '{username}' already exists.")
        return False
    hashed_pw = hash_password(password)
    with open(USER_DATA_FILE, "a") as file:
        file.write(f"{username},{hashed_pw}\n")
    print(f"Success: User '{username}' registered successfully!")
    return True
def login_user(username, password):
    if not os.path.exists(USER_DATA_FILE):
        print("Error: No users registered yet.")
        return False
    with open(USER_DATA_FILE, "r") as file:
        for line in file:
            stored_username, stored_hash = line.strip().split(",")
            if stored_username == username:
                if verify_password(password, stored_hash):
                    print(f"Success: Welcome, {username}!")
                    return True
                else:
                    print("Error: Invalid password.")
                    return False
    print("Error: Username not found.")
    return False
def validate_username(username):
    if not (3 <= len(username) <= 20):
        return False, "Username must be 3–20 characters."
    if not username.isalnum():
        return False, "Username must be alphanumeric only."
    return True, ""
def validate_password(password):
    if len(password) < 6:
        return False, "Password must be at least 6 characters."
    if len(password) > 50:
        return False, "Password too long (max 50)."
    return True, ""
def display_menu():            #Menu
    print("\n" + "=" * 50)
    print(" MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print(" Secure Authentication System")
    print("=" * 50)
    print("\n[1] Register a new user")
    print("[2] Login")
    print("[3] Exit")
    print("-" * 50)
def main():
    print("\nWelcome to the Week 7 Authentication System!")
    while True:
        display_menu()
        choice = input("\nPlease select an option (1-3): ").strip()
        if choice == '1':  # REGISTER
            print("\n--- USER REGISTRATION ---")
            username = input("Enter a username: ").strip()
            if user_exists(username):
                print(f"Error: Username '{username}' already exists.")
                continue
            # Validate username format
            is_valid, error_msg = validate_username(username)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue
            password = input("Enter a password: ").strip()
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue
            password_confirm = input("Confirm password: ").strip()
            if password != password_confirm:
                print("Error: Passwords do not match.")
                continue
            register_user(username, password)
        elif choice == '2':  # LOGIN
            print("\n--- USER LOGIN ---")
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()
            login_user(username, password)
            input("\nPress Enter to return to main menu...")
        elif choice == '3':  # EXIT
            print("\nThank you for using the authentication system.")
            print("Exiting...")
            break
        else:
            print("\nError: Invalid option. Please select 1, 2, or 3.")
if __name__ == "__main__":
    main()
