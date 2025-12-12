from app.data.users import create_user
#Loading users
def load_users_from_file():
    with open("DATA/users.txt", "r") as file:
        for line in file:
            username, password, role = line.strip().split(",")
            create_user(username, password, role)
