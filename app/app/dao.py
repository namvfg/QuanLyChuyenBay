
import hashlib
from app import app
from app.models import User
from app.models import Review, Notification
def auth_user(user_name,password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).digest())

    return User.query.filter(User.user_name.__eq__(user_name.strip()),
                             User.password.__eq__(password)).first()


def get_user_by_id(user_id):
    return User.query.get(user_id)


#đọc lấy review từ bảng Review
def load_reviews():
    return Review.query


#đọc lấy notification từ bảng Notification
def load_notifications(page=1):
    notifications = Notification.query
    page_size = app.config["PAGE_SIZE_NOTIFICATION"]  # 4
    start = (page - 1) * page_size
    notifications = notifications.slice(start, start + page_size)

    return notifications.all()


    return 0
#đếm số notifications
def count_notifications():
    return Notification.query.count()
