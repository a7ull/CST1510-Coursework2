# small helper for auth-related operations
from multi_domain_platform.database.users import check_login, create_user, user_exists

def register_user(username, password, role):
    if user_exists(username):
        raise ValueError("username exists")
    create_user(username, password, role)
def login_user(username, password):
    return check_login(username, password)