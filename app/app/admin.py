from app import app, db, dao
from app.models import Manufacturer, SeatClass, Seat, Airplane, Airport, Route, IntermediateAirport, Flight, SubFlight, TicketPrice, User, AdminWebsite, Customer, Staff, StaffRole, Receipt, Passenger, Ticket, Review, Notification, Rule
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

#hãng sản xuất
class ManufacturerView(ModelView):
    column_list = ["id", "name", "airplanes"]

#máy bay
class AirplaneView(ModelView):
    column_list = ["id", "name", "mfg_date", "manufacturer", "seats", "flights"]

#hạng ghế
class SeatClassView(ModelView):
    column_list = ["id", "name", "seats", "ticket_prices"]

#ghế
class SeatView(ModelView):
    column_list = ["id", "name", "active",  "seats_seat_class", "seats_airplane", "tickets"]

#sân bay
class AirportView(ModelView):
    column_list = ["id", "name", "address", "start_routes", "end_routes", "intermediate_airports"]

#tuyến bay
class RouteView(ModelView):
    column_list = ["id", "note", "departure_airport", "intermediate_airports", "arrival_airport", "flights"]

#sân bay trung gian
class IntermediateAirportView(ModelView):
    column_list = ["id", "order", "note", "intermediate_airport", "intermediate_airports_route"]

#chuyến bay
class FlightView(ModelView):
    column_list = ["id", "name", "flight_date", "flights_airplane", "flights_route", "flights_planner",
                   "ticket_prices", "tickets", "sub_flights"]

#chuyến bay nhỏ
class SubFlightView(ModelView):
    column_list = ["id", "order", "flight_time", "flying_duration", "waiting_duration", "sub_flights_flight"]

#gia ve
class TicketPriceView(ModelView):
    column_list = ["id", "price", "ticket_prices_seat_class", "ticket_prices_flight", "tickets"]

#user
class UserView(ModelView):
    column_list = ["id", "first_name", "last_name", "username", "password"]

#admin
class AdminWebsiteView(UserView):
    column_list = ["id", "first_name", "last_name", "username", "password"] + ["active", "rules"]

#khách hàng
class CustomerView(UserView):
    column_list = ["id", "first_name", "last_name", "username", "password"] + ["id_card_number", "phone_number", "email", "avatar", "receipts"]

#nhân viên
class StaffView(UserView):
    column_list = ["id", "first_name", "last_name", "username", "password"] + ["active", "staff_role", "flights", "receipts"]

#hóa đơn
class ReceiptView(ModelView):
    column_list = ["id", "pay_date", "receipts_customer", "receipts_seller", "tickets"]

#người đi
class PassengerView(ModelView):
    column_list = ["id", "first_name", "last_name", "id_card_number", "phone_number", "ticket"]

#vé máy bay
class TicketView(ModelView):
    column_list = ["id", "tickets_seat", "tickets_flight", "ticket_passenger", "tickets_ticket_price", "tickets_receipt"]

#review
class ReviewView(ModelView):
    column_list = ["id", "reviewer_name", "vote", "content", "image", "review_date"]

#thong bao
class NotificationView(ModelView):
    column_list = ["id", "title", "content", "image", "posting_date"]

#qui định
class RuleView(ModelView):
    column_list = ["id", "name", "value", "rules_admin"]


admin = Admin(app=app, name="Trang quản trị", template_mode="bootstrap4")

admin.add_view(ManufacturerView(Manufacturer, db.session))
admin.add_view(AirplaneView(Airplane, db.session))
admin.add_view(SeatClassView(SeatClass, db.session))
admin.add_view(SeatView(Seat, db.session))
admin.add_view(AirportView(Airport, db.session))
admin.add_view(RouteView(Route, db.session))
admin.add_view(IntermediateAirportView(IntermediateAirport, db.session))
admin.add_view(FlightView(Flight, db.session))
admin.add_view(SubFlightView(SubFlight, db.session))
admin.add_view(TicketPriceView(TicketPrice, db.session))
admin.add_view(AdminWebsiteView(AdminWebsite, db.session))
admin.add_view(CustomerView(Customer, db.session))
admin.add_view(StaffView(Staff, db.session))
admin.add_view(ReceiptView(Receipt, db.session))
admin.add_view(PassengerView(Passenger, db.session))
admin.add_view(TicketView(Ticket, db.session))
admin.add_view(ReviewView(Review, db.session))
admin.add_view(NotificationView(Notification, db.session))
admin.add_view(RuleView(Rule, db.session))