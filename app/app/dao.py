
import hashlib
from typing import TextIO
from flask import request, jsonify, session
from sqlalchemy import func
from sqlalchemy.orm import aliased
from app import app, db
from app.models import User, Customer
from app.models import Review, Notification, Ticket, TicketPrice, Passenger, SubFlight, Flight, Route, Airport
import json
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

#lấy thông tin người dùng
def get_user_by_id(user_id):
    return User.query.get(user_id)

#xác nhận customer
def auth_customer(user_name, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).digest())
    return Customer.query.filter(Customer.user_name.__eq__(user_name.strip()),
                             Customer.password.__eq__(password)).first()

#lấy thông tin vé đếm
def count_tickets():
    return Ticket.query.count()

#tính tổng doanh thu
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


#đếm số notifications
def count_notifications():
    return Notification.query.count()


#lấy các chuyến bay phổ biến cho trang chủ
def load_popular_routes():
    DepartureAirport = aliased(Airport)
    ArrivalAirport = aliased(Airport)
    average_price_query = (db.session.query(Route.id,
                            DepartureAirport.address.label("departure_airport"),
                            ArrivalAirport.address.label("arrival_airport"),
                            func.avg(TicketPrice.price).label("average_price"),
                            func.count(Flight.id).label("flight_amount")
                            ).join(Flight, Route.id.__eq__(Flight.route_id)
                            ).join(TicketPrice, Flight.id.__eq__(TicketPrice.flight_id)
                            ).join(DepartureAirport, Route.departure_airport_id.__eq__(DepartureAirport.id)
                            ).join(ArrivalAirport, Route.arrival_airport_id.__eq__(ArrivalAirport.id)
                            ).group_by(Route.id).limit(10)).subquery()

    flight_amount_query = (db.session.query(Route.id, func.count(Flight.id).label("flight_amount")
                            ).join(Flight, Route.id.__eq__(Flight.route_id)
                            ).group_by(Route.id)).subquery()

    return db.session.query(
        average_price_query.c.id,
        average_price_query.c.departure_airport,
        average_price_query.c.arrival_airport,
        average_price_query.c.average_price,
        flight_amount_query.c.flight_amount
    ).join(flight_amount_query, flight_amount_query.c.id.__eq__(average_price_query.c.id)
    ).order_by(flight_amount_query.c.flight_amount.desc()).all()


if __name__ == "__main__":
    with app.app_context():
        print(load_popular_routes())