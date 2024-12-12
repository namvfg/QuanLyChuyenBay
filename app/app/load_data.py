from app import app, db
from datetime import datetime
from models import *
import json

#load review vào csdl
def load_reviews():

    with open("%s/data/reviews.json" % app.root_path, encoding="utf-8") as f:
        data = json.load(f)
        for x in data:
            date = x["review_date"]
            date = datetime.fromisoformat(date)
            x["review_date"] = date
            x = Review(**x)
            db.session.add(x)
        db.session.commit()

#load notification vào csdl
def load_notifications():
    with open("%s/data/notifications.json" % app.root_path, encoding="utf-8") as f:
        data = json.load(f)
        for x in data:
            date = datetime.now()
            x = Notification(**x)
            x.posting_date = date
            db.session.add(x)
        db.session.commit()

#load manufacture vào csdl
def load_manufacturers():
    with open("%s/data/manufacturers.json" % app.root_path, encoding="utf-8") as f:
        data = json.load(f)
        for x in data:
            x = Manufacturer(**x)
            db.session.add(x)
        db.session.commit()

#load airplane vào csdl
def load_airplanes():
    with open("%s/data/airplanes.json" % app.root_path, encoding="utf-8") as f:
        data = json.load(f)
        for x in data:
            date = x["mfg_date"]
            date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            x["mfg_date"] = date
            x = Airplane(**x)
            db.session.add(x)
        db.session.commit()

#load airport vào csdl
def load_airports():
    with open("%s/data/airports.json" % app.root_path, encoding="utf-8") as f:
        data = json.load(f)
        for x in data:
            x = Airport(**x)
            db.session.add(x)
        db.session.commit()

#load flight vào csdl
def load_flights():
    with open("%s/data/flights.json" % app.root_path, encoding="utf-8") as f:
        data = json.load(f)
        for x in data:
            date = x["flight_date"]
            date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            x["flight_date"] = date
            x = Flight(**x)
            db.session.add(x)
        db.session.commit()

#load intermediate_airport vào csdl
def load_intermediate_airports():
    with open("%s/data/intermediate_airports.json" % app.root_path, encoding="utf-8") as f:
        data = json.load(f)
        for x in data:
            x = IntermediateAirport(**x)
            db.session.add(x)
        db.session.commit()

#load receipt vào csdl
def load_receipts():
    with open("%s/data/receipts.json" % app.root_path, encoding="utf-8") as f:
        data = json.load(f)
        for x in data:
            date = x["pay_date"]
            date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            x["pay_date"] = date
            x = Receipt(**x)
            db.session.add(x)
        db.session.commit()

#load route vào csdl
def load_routes():
    with open("%s/data/routes.json" % app.root_path, encoding="utf-8") as f:
        data = json.load(f)
        for x in data:
            x = Route(**x)
            db.session.add(x)
        db.session.commit()

#load seat_class vào csdl
def load_seat_classes():
    with open("%s/data/seat_classes.json" % app.root_path, encoding="utf-8") as f:
        data = json.load(f)
        for x in data:
            x = SeatClass(**x)
            db.session.add(x)
        db.session.commit()

#load seat vào csdl
def load_seats():
    with open("%s/data/seats.json" % app.root_path, encoding="utf-8") as f:
        data = json.load(f)
        for x in data:
            x = Seat(**x)
            db.session.add(x)
        db.session.commit()

#load ticket_price vào csdl
def load_ticket_prices():
    with open("%s/data/ticket_prices.json" % app.root_path, encoding="utf-8") as f:
        data = json.load(f)
        for x in data:
            x = TicketPrice(**x)
            db.session.add(x)
        db.session.commit()

#load ticket vào csdl
def load_tickets():
    with open("%s/data/tickets.json" % app.root_path, encoding="utf-8") as f:
        data = json.load(f)
        for x in data:
            x = Ticket(**x)
            db.session.add(x)
        db.session.commit()

#load user vào csdl
def load_users():
    with open("%s/data/users.json" % app.root_path, encoding="utf-8") as f:
        data = json.load(f)
        for x in data:
            x = User(**x)
            db.session.add(x)
        db.session.commit()

#load customer vào csdl
def load_customers():
    with open("%s/data/customers.json" % app.root_path, encoding="utf-8") as f:
        data = json.load(f)
        for x in data:
            x = Customer(**x)
            db.session.add(x)
        db.session.commit()

#load admin vào csdl
def load_admin_websites():
    with open("%s/data/admin_websites.json" % app.root_path, encoding="utf-8") as f:
        data = json.load(f)
        for x in data:
            x = AdminWebsite(**x)
            db.session.add(x)
        db.session.commit()

#load staff vào csdl
def load_staffs():
    with open("%s/data/staffs.json" % app.root_path, encoding="utf-8") as f:
        data = json.load(f)
        for x in data:
            x = Staff(**x)
            db.session.add(x)
        db.session.commit()

#load subflight vào csdl
def load_sub_flights():
    with open("%s/data/sub_flights.json" % app.root_path, encoding="utf-8") as f:
        data = json.load(f)
        for x in data:
            x = SubFlight(**x)
            db.session.add(x)
        db.session.commit()

#load passenger vào csdl
def load_passengers():
    with open("%s/data/passengers.json" % app.root_path, encoding="utf-8") as f:
        data = json.load(f)
        for x in data:
            x = Passenger(**x)
            db.session.add(x)
        db.session.commit()