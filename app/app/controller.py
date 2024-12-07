import math

from flask import render_template, request
from app import app, db, dao

#trang chu
def index():
    reviews = dao.load_reviews()
    page_size = app.config["PAGE_SIZE_NOTIFICATION"] #4

    page_notification = request.args.get("page_notification", 1)

    notifications = dao.load_notifications(int(page_notification))
    page_notification_count = dao.count_notifications()
    return render_template("index.html", reviews=reviews,
                           notifications=notifications,
                           pages_notification=math.ceil(page_notification_count/page_size))