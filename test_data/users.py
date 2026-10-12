from datetime import datetime


STANDARD_USER = {
    "username": "standard_user",
    "password": "standard123",
    "type": "standard",
}

LOCKED_USER = {
    "username": "locked_user",
    "password": "locked123",
    "type": "locked",
}


def get_admin_user():
    return {
        "username": "admin_user",
        "password": f"$Admin{datetime.now():%d%m%Y}",
        "type": "admin",
    }