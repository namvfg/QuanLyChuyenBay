
import hashlib

from flask import request, jsonify

from app import app, db
from app.models import User, Customer
from app.models import Review, Notification

#xác nhận user
def auth_user(user_name, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).digest())
    return User.query.filter(User.user_name.__eq__(user_name.strip()),
                             User.password.__eq__(password)).first()

#=================================Validate đăng ký======================================#
#check đã tồn tại user_name hay chưa
def get_user_by_user_name(user_name):
    return User.query.filter_by(user_name=user_name).first()

def get_customer_by_phone_number(phone_number):
    return Customer.query.filter_by(phone_number=phone_number).first()

def get_customer_by_email(email):
    return Customer.query.filter_by(email=email).first()

def register(user_name, password, first_name, last_name, phone_number, email, avatar):
    password = str(hashlib.md5(password.strip().encode("utf-8")).digest())
    customer = Customer(user_name=user_name, password=password, first_name=first_name, last_name=last_name,
                        phone_number=phone_number, email=email, avatar=avatar)
    db.session.add(customer)
    db.session.commit()

#end==============================Validate đăng ký======================================#

#xác nhận customer
def auth_customer(user_name, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).digest())
    return Customer.query.filter(Customer.user_name.__eq__(user_name.strip()),
                             Customer.password.__eq__(password)).first()


#lấy khách hàng theo id
def get_customer_by_id(customer_id):
    return Customer.query.get(customer_id)


def get_user_by_id(user_id):
    return User.query.get(user_id)


#đọc lấy review từ bảng Review
def load_reviews():
    return Review.query


#đọc lấy notification từ bảng Notification
def load_notifications():
    return Notification.query


#đếm số notifications
def count_notifications():
    return Notification.query.count()
