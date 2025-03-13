from pickle import FALSE
from sqlalchemy import Column, Integer, String, Float, Text, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from app import app,db
from flask_login import UserMixin
from enum import Enum as PythonEnum
from datetime import datetime
import json
from werkzeug.security import generate_password_hash, check_password_hash

# base model
class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)

    def as_dict(self):
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, datetime):
                value = value.strftime("%Y-%m-%d %H:%M:%S")
            result[column.name] = value
        return result


# hang san xuat
class Manufacturer(BaseModel):
    name = Column(String(100), nullable=False, unique=True)

    airplanes = relationship("Airplane", backref="manufacturer", lazy=True)

    def __str__(self):
        return self.name

    def as_dict(self):
        # Gọi phương thức của lớp cha
        result = super().as_dict()
        result['airplanes'] = [airplane.as_dict() for airplane in self.airplanes]
        return result


# may bay
class Airplane(BaseModel):
    name = Column(String(100), nullable=False, unique=True)
    mfg_date = Column(DateTime, nullable=False)
    seat_quantity = Column(Integer, nullable=False)

    manufacturer_id = Column(Integer, ForeignKey(Manufacturer.id), nullable=False)

    seats = relationship("Seat", backref="seats_airplane", lazy=True)
    flights = relationship("Flight", backref="flights_airplane", lazy=True)

    def __str__(self):
        return self.name

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            # Chuyển đổi mfg_date thành chuỗi nếu không phải None
            "seat_quantity": self.seat_quantity,
            "mfg_date": self.mfg_date.strftime("%Y-%m-%d %H:%M:%S") if self.mfg_date else None,
            "manufacturer_id": self.manufacturer_id
        }


# hang ghe
class SeatClass(BaseModel):
    name = Column(String(30), nullable=False, unique=True)

    seats = relationship("Seat", backref="seats_seat_class", lazy=True)
    ticket_prices = relationship("TicketPrice", backref="ticket_prices_seat_class", lazy=True)

    def __str__(self):
        return self.name

    def as_dict(self):
        result = super().as_dict()
        result['seats'] = [seat.as_dict() for seat in self.seats]
        result['ticket_prices'] = [ticket_price.as_dict() for ticket_price in self.ticket_prices]
        return result


# cho ngoi
class Seat(BaseModel):
    name = Column(String(10), nullable=False)
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
    image = Column(String(150))

    start_routes = relationship("Route", foreign_keys="Route.departure_airport_id", backref="departure_airport",
                                lazy=True)
    end_routes = relationship("Route", foreign_keys="Route.arrival_airport_id", backref="arrival_airport", lazy=True)
    intermediate_airports = relationship("IntermediateAirport", backref="intermediate_airport", lazy=True)

    def __str__(self):
        return self.name


    def as_dict(self):
        result = super().as_dict()
        result['start_routes'] = [route.as_dict() for route in self.start_routes]
        result['end_routes'] = [route.as_dict() for route in self.end_routes]
        result['intermediate_airports'] = [airport.as_dict() for airport in self.intermediate_airports]
        return result


# Tuyen bay
class Route(BaseModel):
    name = Column(String(10), nullable=False, unique=True)

    departure_airport_id = Column(Integer, ForeignKey(Airport.id), nullable=False)
    arrival_airport_id = Column(Integer, ForeignKey(Airport.id), nullable=False)

    intermediate_airports = relationship("IntermediateAirport", backref="intermediate_airports_route", lazy=True)
    flights = relationship("Flight", backref="flights_route", lazy=True)

    def as_dict(self):
        result = super().as_dict()
        result['departure_airport_id'] = self.departure_airport_id
        result['arrival_airport_id'] = self.arrival_airport_id
        result['intermediate_airports'] = [airport.as_dict() for airport in self.intermediate_airports]
        result['flights'] = [flight.as_dict() for flight in self.flights]
        return result


# san bay trung gian
class IntermediateAirport(BaseModel):
    order = Column(Integer, nullable=False)

    airport_id = Column(Integer, ForeignKey(Airport.id), nullable=False)
    route_id = Column(Integer, ForeignKey(Route.id), nullable=False)

    def as_dict(self):
        result = super().as_dict()
        result['airport_id'] = self.airport_id
        result['route_id'] = self.route_id
        return result


# chuyen bay
class Flight(BaseModel):
    name = Column(String(20), nullable=False, unique=True)
    flight_date = Column(DateTime, nullable=False)
    total_time = Column(Integer, nullable=False)

    airplane_id = Column(Integer, ForeignKey(Airplane.id), nullable=False)
    route_id = Column(Integer, ForeignKey(Route.id), nullable=False)
    planner_id = Column(Integer, ForeignKey("staff.staff_id"), nullable=False)

    ticket_prices = relationship("TicketPrice", backref="ticket_prices_flight", lazy=True)
    tickets = relationship("Ticket", backref="tickets_flight", lazy=True)
    sub_flights = relationship("SubFlight", backref=" sub_flights_flight", lazy=True)

    def __str__(self):
        return self.name

    def as_dict(self):
        # Khởi tạo từ lớp cha nếu có
        result = {
            "id": self.id,
            "name": self.name,
            # Xử lý datetime
            "flight_date": self.flight_date.strftime("%Y-%m-%d %H:%M:%S") if self.flight_date else None,
            "airplane_id": self.airplane_id,
            "route_id": self.route_id,
            "planner_id": self.planner_id,
            "total_time": self.total_time,
            # Chuyển đổi các quan hệ
            "ticket_prices": [ticket_price.as_dict() for ticket_price in
                              self.ticket_prices] if self.ticket_prices else [],
            "tickets": [ticket.as_dict() for ticket in self.tickets] if self.tickets else [],
            "sub_flights": [sub_flight.as_dict() for sub_flight in self.sub_flights] if self.sub_flights else []
        }
        return result


# chuyen bay nho
class SubFlight(BaseModel):
    order = Column(Integer, nullable=False)
    flight_time = Column(DateTime, nullable=False) #xóa
    flying_duration = Column(Integer, nullable=False)
    waiting_duration = Column(Integer, nullable=False, default=0)

    flight_id = Column(Integer, ForeignKey(Flight.id), nullable=False)

    def as_dict(self):
        result = super().as_dict()
        result['flight_time'] = self.flight_time.strftime("%Y-%m-%d %H:%M:%S") if self.flight_time else None
        result['flight_id'] = self.flight_id
        return result


# gia ve
class TicketPrice(BaseModel):
    price = Column(Float, nullable=False)

    seat_class_id = Column(Integer, ForeignKey(SeatClass.id), nullable=False)
    flight_id = Column(Integer, ForeignKey(Flight.id), nullable=False)

    tickets = relationship("Ticket", backref="tickets_ticket_price", lazy=True)

    def as_dict(self):
        result = super().as_dict()
        result['seat_class_id'] = self.seat_class_id
        result['flight_id'] = self.flight_id
        result['tickets'] = [ticket.as_dict() for ticket in self.tickets]
        return result

# user
class User(BaseModel, UserMixin):
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(100), nullable=False)
    user_name = Column(String(20), unique=True)
    password = Column(String(100))

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
    phone_number = Column(String(10), unique=True, nullable=False)
    email = Column(String(50), unique=True)
    avatar = Column(String(100))

    receipts = relationship("Receipt", backref="receipts_customer", lazy=True)


# staff role
class StaffRole(PythonEnum):
    PLANNER = 1
    SELLER = 2


# staff
class Staff(User):
    staff_id = Column(Integer, ForeignKey(User.id), primary_key=True)
    active = Column(Boolean, default=True)
    staff_role = Column(Enum(StaffRole), default=StaffRole.SELLER)

    flights = relationship("Flight", backref="flights_planner", lazy=True)
    receipts = relationship("Receipt", backref="receipts_seller", lazy=True)

    def as_dict(self):
        result = super().as_dict()  # Kế thừa logic từ User nếu có
        result.update({
            "staff_id": self.staff_id,
            "active": self.active,
            "staff_role": self.staff_role.name if isinstance(self.staff_role, Enum) else str(self.staff_role),
            # Chuyển Enum thành chuỗi
            "flights": [flight.as_dict() for flight in self.flights],  # Serialize các quan hệ
            "receipts": [receipt.as_dict() for receipt in self.receipts]  # Serialize các quan hệ
        })
        return result


class PaymentMethod(PythonEnum):
    BANKING = 1
    CASHING = 2

# hoa don
class Receipt(BaseModel):
    pay_date = Column(DateTime, default=datetime.now())
    order_id = Column(String(100), nullable=False)
    payment_method = Column(Enum(PaymentMethod), default=PaymentMethod.CASHING)

    customer_id = Column(Integer, ForeignKey(Customer.customer_id), nullable=False)
    seller_id = Column(Integer, ForeignKey(Staff.staff_id), default=1, nullable=False)

    tickets = relationship("Ticket", backref="tickets_receipt", lazy=True)

    def as_dict(self):
        return {
            "id": self.id,
            # Xử lý datetime
            "pay_date": self.pay_date.strftime("%Y-%m-%d %H:%M:%S") if self.pay_date else None,
            # Liên kết khóa ngoại
            "customer_id": self.customer_id,
            "order_id": self.order_id,
            "seller_id": self.seller_id,
            # Quan hệ (relationship)
            "tickets": [ticket.as_dict() for ticket in self.tickets] if self.tickets else []
        }

        # nguoi di
class Passenger(BaseModel):
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(100), nullable=False)
    id_card_number = Column(String(20), nullable=False)
    phone_number = Column(String(15), nullable=False)

    ticket = relationship("Ticket", backref="ticket_passenger", lazy=False)

    def __str__(self):
        return self.first_name

    def as_dict(self):
        result = super().as_dict()
        result['ticket'] = [ticket.as_dict() for ticket in self.ticket]
        return result


# ve may bay
class Ticket(BaseModel):
    seat_id = Column(Integer, ForeignKey(Seat.id), nullable=False)
    flight_id = Column(Integer, ForeignKey(Flight.id), nullable=False)
    passenger_id = Column(Integer, ForeignKey(Passenger.id), nullable=False, unique=True)
    ticket_price_id = Column(Integer, ForeignKey(TicketPrice.id), nullable=False)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)

    def as_dict(self):
        result = super().as_dict()
        result['seat_id'] = self.seat_id
        result['flight_id'] = self.flight_id
        result['passenger_id'] = self.passenger_id
        result['ticket_price_id'] = self.ticket_price_id
        result['receipt_id'] = self.receipt_id
        return result


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

        db.create_all()
        # #load review vao csdl
        with open("%s/data/reviews.json" % app.root_path, encoding="utf-8") as f:
            data = json.load(f)
            for x in data:
                date = x["review_date"]
                date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
                x["review_date"] = date
                x = Review(**x)
                db.session.add(x)
            db.session.commit()

        # #load notification vao csdl
        with open("%s/data/notifications.json" % app.root_path, encoding="utf-8") as f:
            data = json.load(f)
            for x in data:
                date = datetime.now()
                x = Notification(**x)
                x.posting_date = date
                db.session.add(x)
            db.session.commit()

        #load manufacturer vao csdl
        with open("%s/data/manufacturers.json" % app.root_path, encoding="utf-8") as f:
            data = json.load(f)
            for x in data:
                x = Manufacturer(**x)
                db.session.add(x)
            db.session.commit()

        # #load airplane vào csdl
        with open("%s/data/airplanes.json" % app.root_path, encoding="utf-8") as f:
            data = json.load(f)
            for x in data:
                date = x["mfg_date"]
                date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
                x["mfg_date"] = date
                x = Airplane(**x)
                db.session.add(x)
            db.session.commit()

        # #load airport vào csdl
        with open("%s/data/airports.json" % app.root_path, encoding="utf-8") as f:
            data = json.load(f)
            for x in data:
                x = Airport(**x)
                db.session.add(x)
            db.session.commit()


        # #load route vào csdl
        with open("%s/data/routes.json" % app.root_path, encoding="utf-8") as f:
            data = json.load(f)
            for x in data:
                x = Route(**x)
                db.session.add(x)
            db.session.commit()

        # #load intermediate_airport vào csdl
        with open("%s/data/intermediate_airports.json" % app.root_path, encoding="utf-8") as f:
            data = json.load(f)
            for x in data:
                x = IntermediateAirport(**x)
                db.session.add(x)
            db.session.commit()

        # #load seat_class vào csdl
        with open("%s/data/seat_classes.json" % app.root_path, encoding="utf-8") as f:
            data = json.load(f)
            for x in data:
                x = SeatClass(**x)
                db.session.add(x)
            db.session.commit()


        # #load seat vào csdl
        with open("%s/data/seats.json" % app.root_path, encoding="utf-8") as f:
            data = json.load(f)
            for x in data:
                x = Seat(**x)
                db.session.add(x)
            db.session.commit()

        # #load user vào csdl
        # with open("%s/data/users.json" % app.root_path, encoding="utf-8") as f:
        #     data = json.load(f)
        #     for x in data:
        #         x = User(**x)
        #         db.session.add(x)
        #     db.session.commit()

        # #load staff vào csdl
        with open("%s/data/staffs.json" % app.root_path, encoding="utf-8") as f:
            data = json.load(f)
            for x in data:
                x = Staff(**x)
                db.session.add(x)
            db.session.commit()

        # #load admin vào csdl
        with open("%s/data/admin_websites.json" % app.root_path, encoding="utf-8") as f:
            data = json.load(f)
            for x in data:
                x = AdminWebsite(**x)
                db.session.add(x)
            db.session.commit()

        # #load customer vào csdl
        with open("%s/data/customers.json" % app.root_path, encoding="utf-8") as f:
            data = json.load(f)
            for x in data:
                x = Customer(**x)
                db.session.add(x)
            db.session.commit()

        # #load receipt vào csdl
        with open("%s/data/receipts.json" % app.root_path, encoding="utf-8") as f:
            data = json.load(f)
            for x in data:
                date = x["pay_date"]
                date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
                x["pay_date"] = date
                x = Receipt(**x)
                db.session.add(x)
            db.session.commit()

        # # load flight vào csdl
        with open("%s/data/flights.json" % app.root_path, encoding="utf-8") as f:
            data = json.load(f)
            for x in data:
                date = x["flight_date"]
                date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
                x["flight_date"] = date
                x = Flight(**x)
                db.session.add(x)
            db.session.commit()

        # #load subflights vào csdl
        with open("%s/data/sub_flights.json" % app.root_path, encoding="utf-8") as f:
            data = json.load(f)
            for x in data:
                date = x["flight_time"]
                date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
                x["flight_time"] = date
                x = SubFlight(**x)
                db.session.add(x)
            db.session.commit()

        # #load ticket_price vào csdl
        with open("%s/data/ticket_prices.json" % app.root_path, encoding="utf-8") as f:
            data = json.load(f)
            for x in data:
                x = TicketPrice(**x)
                db.session.add(x)
            db.session.commit()

        # #load passenger vào csdl
        with open("%s/data/passengers.json" % app.root_path, encoding="utf-8") as f:
            data = json.load(f)
            for x in data:
                x = Passenger(**x)
                db.session.add(x)
            db.session.commit()

        # #load ticket vào csdl
        with open("%s/data/tickets.json" % app.root_path, encoding="utf-8") as f:
            data = json.load(f)
            for x in data:
                x = Ticket(**x)
                db.session.add(x)
            db.session.commit()

        # #load ticket vào csdl
        with open("%s/data/rules.json" % app.root_path, encoding="utf-8") as f:
            data = json.load(f)
            for x in data:
                x = Rule(**x)
                db.session.add(x)
            db.session.commit()


