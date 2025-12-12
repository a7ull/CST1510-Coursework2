from multi_domain_platform.database.users import UserDB

class User:
    def __init__(self, username: str, role: str, id=None):
        self.id = id
        self.username = username
        self.role = role

    def save(self, password: str):
        # create in DB
        UserDB.create_user(self.username, password, self.role)

    @classmethod
    def authenticate(cls, username: str, password: str):
        row = UserDB.check_login(username, password)
        if row:
            return cls(username=row["username"], role=row["role"], id=row["id"])
        return None

    @classmethod
    def exists(cls, username: str):
        return UserDB.get_by_username(username) is not None