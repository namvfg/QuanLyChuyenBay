
import hashlib
from cProfile import label
from typing import TextIO
from flask import request, jsonify, session
from flask_admin import Admin
from sqlalchemy import func
from sqlalchemy.orm import aliased
from app import app, db
from app.models import User, Customer, Manufacturer, SeatClass, Seat, IntermediateAirport, Staff, AdminWebsite
from app.models import Review, Notification,Ticket,TicketPrice,Passenger,SubFlight, Airport, Airplane, Route, Flight
import json
from flask_login import current_user
from werkzeug.security import generate_password_hash
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

#xác nhận staff
def auth_staff(user_name, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).digest())
    return Staff.query.filter(Staff.user_name.__eq__(user_name.strip()),
                             Staff.password.__eq__(password)).first()

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

#lấy nhân viên theo id
def get_staff_by_id(staff_id):
    return Staff.query.get(staff_id)

#lấy admin theo id
def get_admin_by_id(admin_id):
    return AdminWebsite.query.get(admin_id)

#lấy thông tin khách đếm
def count_passengers():
    return Passenger.query.count()

def get_user_by_id(user_id):
    return User.query.get(user_id)


#đọc lấy review từ bảng Review
def load_reviews():
    return Review.query.all()


#đọc lấy notification từ bảng Notification
def load_notifications():
    return Notification.query.all()


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

def load_user():
    return db.session.query(User.first_name,User.last_name)

#truy xuat du lieu airplane
def load_airplanes():
    return db.session.query(Airplane.id,Airplane.name).all()

#truy xuat du lieu airport
def load_airports():
    return Airport.query.all()

#truy xuất dữ liệu manufacturer
def load_manufacturers():
    return Manufacturer.query.all()

#truy xuất dữ liệu hạng ghế
def load_seat_classes():
    return SeatClass.query.order_by("id").all()

#truy xuat du lieu routes
def load_route():
    DepartureAirport = aliased(Airport)
    ArrivalAirport = aliased(Airport)
    return db.session.query(
            Route.id,
            Route.name,
            DepartureAirport.id.label("departure_airport_id"),
            DepartureAirport.name.label("departure_airport"),
            ArrivalAirport.id.label("arrival_airport_id"),
            ArrivalAirport.name.label("arrival_airport")
        ).join(
            DepartureAirport, Route.departure_airport_id == DepartureAirport.id
        ).join(
            ArrivalAirport, Route.arrival_airport_id == ArrivalAirport.id
        ).all()

#lấy số lượng hạng ghế
def count_seat_classes():
    return SeatClass.query.count()

#tạo dữ liệu máy bay
def add_airplane(name, manufacturer_id, mfg_date, seat_quantity):
    airplane = Airplane(name=name, manufacturer_id=manufacturer_id, mfg_date=mfg_date, seat_quantity=seat_quantity)
    db.session.add(airplane)
    db.session.commit()

# tạo seat
def add_seats(airplane_id, seat_class_id, start_number, quantity):
    for i in range(start_number, start_number + quantity):
        seat = Seat(name=str(i), seat_class_id=seat_class_id, airplane_id=airplane_id)
        db.session.add(seat)
    db.session.commit()

# tạo tuyến bay
def add_route(name, departure_airport_id, arrival_airport_id):
    route = Route(name=name, departure_airport_id=departure_airport_id, arrival_airport_id=arrival_airport_id)
    db.session.add(route)
    db.session.commit()

#tạo sân bay trung gian
def add_intermediate_airport(order, airport_id, route_id):
    intermediate_airport = IntermediateAirport(order=order, airport_id=airport_id, route_id=route_id)
    db.session.add(intermediate_airport)
    db.session.commit()

#tạo flight
def add_flight(name, flight_date, airplane_id, route_id, planner_id, total_time):
    flight = Flight(name=name, flight_date=flight_date, airplane_id=airplane_id,
                    route_id=route_id, planner_id=planner_id, total_time=total_time)
    db.session.add(flight)
    db.session.commit()

#tạo subflight
def add_sub_flight(order, flight_time, flying_duration, waiting_duration, flight_id):
    sub_flight = SubFlight(order=order, flight_time=flight_time, flying_duration=flying_duration,
                           waiting_duration=waiting_duration, flight_id=flight_id)
    db.session.add(sub_flight)
    db.session.commit()

#tạo ticket price
def add_ticket_price(price, seat_class_id, flight_id):
    ticket_price = TicketPrice(price=price, seat_class_id=seat_class_id, flight_id=flight_id)
    db.session.add(ticket_price)
    db.session.commit()


#lấy airplane theo tên
def get_air_plane_by_name(name):
    return Airplane.query.filter_by(name=name).first()

#lấy đếm seat trong seat class theo id máy bay
def count_seats_in_seat_classes_by_airplane_id(airplane_id):
    query = db.session.query(
        SeatClass.id.label("id"),
        SeatClass.name.label("name"),
        db.func.count(Seat.id).label("total_seats")
    ).join(Seat, Seat.seat_class_id.__eq__(SeatClass.id)
    ).filter(
        Seat.airplane_id.__eq__(airplane_id)
    ).group_by(SeatClass.id).all()
    return query

#lấy seat class + ticket price theo flight id
def load_seat_classes_with_ticket_price_by_flight_id(flight_id):
    query = db.session.query(
        SeatClass.id,
        SeatClass.name,
        TicketPrice.price
    ).join(
        TicketPrice, TicketPrice.seat_class_id.__eq__(SeatClass.id)
    ).filter(
        TicketPrice.flight_id.__eq__(flight_id)
    ).all()
    return query

#lấy seat trên 1 máy bay
def load_seats_by_flight_id(flight_id):
    flight = Flight.query.get(flight_id)
    query = db.session.query(
        Seat.id,
        Seat.name,
        Seat.seat_class_id,
        Seat.active,
        SeatClass.name.label("seat_class_name"),
        Airplane.id.label("airplane_id"),
        TicketPrice.id.label("ticket_price_id"),
        TicketPrice.price.label("price")
    ).join(Airplane, Seat.airplane_id.__eq__(Airplane.id)
    ).join(SeatClass, SeatClass.id.__eq__(Seat.seat_class_id)
    ).join(TicketPrice, SeatClass.id.__eq__(TicketPrice.seat_class_id)
    ).filter(TicketPrice.flight_id.__eq__(flight_id)
    ).filter(Airplane.id.__eq__(flight.airplane_id)
    ).order_by(Seat.id).all()
    return query

#lấy flight theo tên
def load_flight_by_name(name):
    return Flight.query.filter_by(name=name).first()

#lấy flight theo id
def load_flight_by_id(flight_id):
    return Flight.query.get(flight_id)

#lấy flight cho search result
def load_flight_for_search_result(kw1=None, kw2=None, flight_date=None):
    DepartureAirport = aliased(Airport)
    ArrivalAirport = aliased(Airport)
    query = db.session.query(Flight.id, Flight.flight_date, Flight.total_time,
                             DepartureAirport.address.label("departure_airport_address"),
                             ArrivalAirport.address.label("arrival_airport_address"),
                             func.count(IntermediateAirport.id).label("intermediate_airport_quantity")
                             ).join(Route, Route.id.__eq__(Flight.route_id)
                             ).join(DepartureAirport, Route.departure_airport_id.__eq__(DepartureAirport.id)
                             ).join(ArrivalAirport, Route.arrival_airport_id.__eq__(ArrivalAirport.id)
                             ).join(IntermediateAirport, Route.id.__eq__(IntermediateAirport.route_id)
                             ).group_by(Flight.id)

    if kw1:
        query = query.filter(DepartureAirport.address.contains(kw1))

    if kw2:
        query = query.filter(ArrivalAirport.address.contains(kw2))

    if flight_date:
        query = query.filter(Flight.flight_date.date().__eq__(flight_date))

    return query.all()


#lấy intermediate_airports theo route_id
def load_intermediate_airports_by_route_id(route_id):
    query = db.session.query(
        IntermediateAirport.id,
        IntermediateAirport.order,
        IntermediateAirport.airport_id
    ).filter(
        IntermediateAirport.route_id.__eq__(route_id)
    ).order_by(IntermediateAirport.order).all()
    return query

#lấy departure_airport theo id
def load_airport_by_id(airport_id):
    return Airport.query.get(airport_id)

#lấy route theo tên
def get_route_by_name(name):
    return Route.query.filter_by(name=name).first()

#doi mat khau
def change_password(new_password):
    user = User.query.get(current_user.id)
    password =str(hashlib.md5(new_password.encode('utf-8')).digest())
    user.password = password

    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        print(load_flight_for_search_result())

