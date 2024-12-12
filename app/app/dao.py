
import hashlib
from typing import TextIO
from sqlalchemy import func
from app import app, db
from app.models import User, Customer
from app.models import Review, Notification,Ticket,TicketPrice,Passenger,SubFlight
import json
#xác nhận user
def auth_user(user_name, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).digest())
    return User.query.filter(User.user_name.__eq__(user_name.strip()),
                             User.password.__eq__(password)).first()


#lấy thông tin người dùng
def get_user_by_id(user_id):
    return User.query.get(user_id)

def auth_customer(user_name, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).digest())

    return Customer.query.filter(Customer.user_name.__eq__(user_name.strip()),
                             Customer.password.__eq__(password)).first()

#lấy thông tin vé đếm
def count_tickets():
    return Ticket.query.count()


def get_total_revenue():
    # Giả sử có cột price trong Ticket hoặc tính toán giá vé tổng
    query = db.session.query(Ticket.id, TicketPrice.price)\
            .join(TicketPrice, Ticket.ticket_price_id.__eq__(TicketPrice.id))
    total = query.with_entities(func.sum(TicketPrice.price)).scalar()
    return total

#lấy khách hàng theo id
def get_customer_by_id(customer_id):
    return Customer.query.get(customer_id)

#lấy thông tin khách đếm
def count_passengers():
    return Passenger.query.count()

def get_user_by_id(user_id):
    return User.query.get(user_id)


#đọc lấy review từ bảng Review
def load_reviews():
    return Review.query


#đọc lấy notification từ bảng Notification
def load_notifications():
    return Notification.query


