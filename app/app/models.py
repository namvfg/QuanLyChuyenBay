from pickle import FALSE

from sqlalchemy import Column, Integer, String, Float, Text, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from app import app, db
from flask_login import UserMixin
from enum import Enum as UserEnum
from datetime import datetime
import json


# base model
class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


# hang san xuat
class Manufacturer(BaseModel):
    name = Column(String(100), nullable=False, unique=True)

    airplanes = relationship("Airplane", backref="manufacturer", lazy=True)

    def __str__(self):
        return self.name


# may bay
class Airplane(BaseModel):
    name = Column(String(100), nullable=False)
    mfg_date = Column(DateTime, nullable=False)

    manufacturer_id = Column(Integer, ForeignKey(Manufacturer.id), nullable=False)

    seats = relationship("Seat", backref="seats_airplane", lazy=True)
    flights = relationship("Flight", backref="flights_airplane", lazy=True)

    def __str__(self):
        return self.name


# hang ghe
class SeatClass(BaseModel):
    name = Column(String(30), nullable=False, unique=True)

    seats = relationship("Seat", backref="seats_seat_class", lazy=True)
    ticket_prices = relationship("TicketPrice", backref="ticket_prices_seat_class", lazy=True)

    def __str__(self):
        return self.name


# cho ngoi
class Seat(BaseModel):
    name = Column(String(10), nullable=False, unique=True)
    active = Column(Boolean, default=False)

    seat_class_id = Column(Integer, ForeignKey(SeatClass.id), nullable=False)
    airplane_id = Column(Integer, ForeignKey(Airplane.id), nullable=False)

    tickets = relationship("Ticket", backref="tickets_seat", lazy=True)

    def __str__(self):
        return self.name


# san bay
class Airport(BaseModel):
    name = Column(String(50), nullable=False, unique=True)
    address = Column(String(100), nullable=False, unique=True)

    start_routes = relationship("Route", foreign_keys="Route.departure_airport_id", backref="departure_airport",
                                lazy=True)
    end_routes = relationship("Route", foreign_keys="Route.arrival_airport_id", backref="arrival_airport", lazy=True)
    intermediate_airports = relationship("IntermediateAirport", backref="intermediate_airport", lazy=True)

    def __str__(self):
        return self.name


# Tuyen bay
class Route(BaseModel):
    note = Column(Text)

    departure_airport_id = Column(Integer, ForeignKey(Airport.id), nullable=False)
    arrival_airport_id = Column(Integer, ForeignKey(Airport.id), nullable=False)

    intermediate_airports = relationship("IntermediateAirport", backref="intermediate_airports_route", lazy=True)
    flights = relationship("Flight", backref="flights_route", lazy=True)


# san bay trung gian
class IntermediateAirport(BaseModel):
    order = Column(Integer, nullable=False)
    note = Column(Text)

    airport_id = Column(Integer, ForeignKey(Airport.id), nullable=False)
    route_id = Column(Integer, ForeignKey(Route.id), nullable=False)


# chuyen bay
class Flight(BaseModel):
    name = Column(String(20), nullable=False, unique=True)
    flight_date = Column(DateTime, nullable=False)

    airplane_id = Column(Integer, ForeignKey(Airplane.id), nullable=False)
    route_id = Column(Integer, ForeignKey(Route.id), nullable=False)
    planner_id = Column(Integer, ForeignKey("staff.staff_id"), nullable=False)

    ticket_prices = relationship("TicketPrice", backref="ticket_prices_flight", lazy=True)
    tickets = relationship("Ticket", backref="tickets_flight", lazy=True)
    sub_flights = relationship("SubFlight", backref=" sub_flights_flight", lazy=True)

    def __str__(self):
        return self.name


# chuyen bay nho
class SubFlight(BaseModel):
    order = Column(Integer, nullable=False)
    flight_time = Column(Integer, nullable=False)
    flying_duration = Column(Integer, nullable=False)
    waiting_duration = Column(Integer, nullable=False, default=0)

    flight_id = Column(Integer, ForeignKey(Flight.id), nullable=False)


# gia ve
class TicketPrice(BaseModel):
    price = Column(Float, nullable=False)

    seat_class_id = Column(Integer, ForeignKey(SeatClass.id), nullable=False)
    flight_id = Column(Integer, ForeignKey(Flight.id), nullable=False)

    tickets = relationship("Ticket", backref="tickets_ticket_price", lazy=True)


# user
class User(BaseModel, UserMixin):
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(100))
    user_name = Column(String(20), unique=True, nullable=False)
    password = Column(String(50), nullable=False)

    def __str__(self):
        return self.first_name


# admin
class AdminWebsite(User):
    admin_id = Column(Integer, ForeignKey(User.id), primary_key=True)
    active = Column(Boolean, default=True)

    rules = relationship("Rule", backref="rules_admin", lazy=False)


# customer
class Customer(User):
    customer_id = Column(Integer, ForeignKey(User.id), primary_key=True)
    id_card_number = Column(String(20), nullable=False, unique=True)
    phone_number = Column(String(15), nullable=False)
    email = Column(String(50), nullable=False)
    avatar = Column(String(100))

    receipts = relationship("Receipt", backref="receipts_customer", lazy=True)


# staff role
class StaffRole(UserEnum):
    PLANNER = 1
    SELLER = 2


# staff
class Staff(User):
    staff_id = Column(Integer, ForeignKey(User.id), primary_key=True)
    active = Column(Boolean, default=True)
    staff_role = Column(Enum(StaffRole), default=StaffRole.SELLER)

    flights = relationship("Flight", backref="flights_planner", lazy=True)
    receipts = relationship("Receipt", backref="receipts_seller", lazy=True)


# hoa don
class Receipt(BaseModel):
    pay_date = Column(DateTime, default=datetime.now())

    customer_id = Column(Integer, ForeignKey(Customer.customer_id), nullable=False)
    seller_id = Column(Integer, ForeignKey(Staff.staff_id), nullable=False)

    tickets = relationship("Ticket", backref="tickets_receipt", lazy=True)


# nguoi di
class Passenger(BaseModel):
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(100), nullable=False)
    id_card_number = Column(String(20), nullable=False)
    phone_number = Column(String(15), nullable=False)

    ticket = relationship("Ticket", backref="ticket_passenger", lazy=False)

    def __str__(self):
        return self.first_name


# ve may bay
class Ticket(BaseModel):
    seat_id = Column(Integer, ForeignKey(Seat.id), nullable=False)
    flight_id = Column(Integer, ForeignKey(Flight.id), nullable=False)
    passenger_id = Column(Integer, ForeignKey(Passenger.id), nullable=False, unique=True)
    ticket_price_id = Column(Integer, ForeignKey(TicketPrice.id), nullable=False)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)


# review
class Review(BaseModel):
    reviewer_name = Column(String(150), nullable=False)
    vote = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    image = Column(String(150), nullable=False)
    review_date = Column(DateTime, nullable=False)


# thong bao
class Notification(BaseModel):
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    image = Column(String(100), nullable=False)
    posting_date = Column(DateTime, default=datetime.now())


# qui dinh
class Rule(BaseModel):
    name = Column(String(100), nullable=False)
    value = Column(String(100), nullable=False)

    admin_id = Column(Integer, ForeignKey(AdminWebsite.admin_id), nullable=False)


if __name__ == "__main__":
    with app.app_context():

        # db.create_all()
        # with open("%s/data/review.json" %app.root_path, encoding="utf-8") as f1:
        #     data = json.load(f1)
        #     for x in data:
        #         date = x["review_date"]
        #         date = datetime.fromisoformat(date)
        #         x["review_date"] = date
        #         x = Review(**x)
        #         db.session.add(x)
        #     db.session.commit()
        # with open("%s/data/notification.json" %app.root_path, encoding="utf-8") as f2:
        #      data = json.load(f2)
        #      for x in data:
        #         date = datetime.now()
        #         x = Notification(**x)
        #         x.posting_date = date
        #         db.session.add(x)
        #      db.session.commit()
            
        import hashlib
        password = str(hashlib.md5('123456'.encode('utf-8')).digest())
        # u = AdminWebsite(first_name='Dat', last_name='Nguyen', user_name='admin', password=password)
        # db.session.add(u)
        customer = Customer(first_name='Dun', last_name='Nguyen', user_name='customer', password=password,
                     avatar="https://res.cloudinary.com/dcee16rsp/image/upload/v1732182639/My%20Brand/deadlock_rz3for.jpg",
                     id_card_number="123456", phone_number="123456", email="123@gmail.com")
        db.session.add(customer)
        db.session.commit()
           

       


