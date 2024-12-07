import hashlib
from app.models import User
def auth_user(user_name,password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).digest())

    return User.query.filter(User.user_name.__eq__(user_name.strip()),
                             User.password.__eq__(password)).first()


def get_user_by_id(user_id):
    return User.query.get(user_id)
