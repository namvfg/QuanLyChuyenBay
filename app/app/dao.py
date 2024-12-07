from app.models import Review, Notification
from app import app

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