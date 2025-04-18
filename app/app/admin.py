from app import app, db, dao
from flask import request, jsonify, session

from app.decorators import is_admin
from app.models import Manufacturer, SeatClass, Seat, Airplane, Airport, Route, IntermediateAirport, Flight, SubFlight, TicketPrice, User, AdminWebsite, Customer, Staff, StaffRole, Receipt, Passenger, Ticket, Review, Notification, Rule
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from datetime import datetime
from flask_login import current_user

#hãng sản xuất
class ManufacturerView(ModelView):
    column_list = ["id", "name", "airplanes"]

    def is_accessible(self):
        return current_user.is_authenticated

    @is_admin  # Decorator kiểm soát quyền admin
    @expose('/')  # Trang chính của view
    def index_view(self):
        return super().index_view()

#máy bay
class AirplaneView(ModelView):
    column_list = ["id", "name", "mfg_date", "seat_quantity","manufacturer", "seats", "flights"]

    def is_accessible(self):
        return current_user.is_authenticated

    @is_admin  # Decorator kiểm soát quyền admin
    @expose('/')  # Trang chính của view
    def index_view(self):
        return super().index_view()

#hạng ghế
class SeatClassView(ModelView):
    column_list = ["id", "name", "seats", "ticket_prices"]

    def is_accessible(self):
        return current_user.is_authenticated

    @is_admin  # Decorator kiểm soát quyền admin
    @expose('/')  # Trang chính của view
    def index_view(self):
        return super().index_view()

#ghế
class SeatView(ModelView):
    column_list = ["id", "name", "active",  "seats_seat_class", "seats_airplane", "tickets"]

    def is_accessible(self):
        return current_user.is_authenticated

    @is_admin  # Decorator kiểm soát quyền admin
    @expose('/')  # Trang chính của view
    def index_view(self):
        return super().index_view()

#sân bay
class AirportView(ModelView):
    column_list = ["id", "name", "address", "start_routes", "end_routes", "intermediate_airports"]

    def is_accessible(self):
        return current_user.is_authenticated

    @is_admin  # Decorator kiểm soát quyền admin
    @expose('/')  # Trang chính của view
    def index_view(self):
        return super().index_view()

#tuyến bay
class RouteView(ModelView):
    column_list = ["id", "name", "departure_airport", "intermediate_airports", "arrival_airport", "flights"]

    def is_accessible(self):
        return current_user.is_authenticated

    @is_admin  # Decorator kiểm soát quyền admin
    @expose('/')  # Trang chính của view
    def index_view(self):
        return super().index_view()

#sân bay trung gian
class IntermediateAirportView(ModelView):
    column_list = ["id", "order", "intermediate_airport", "intermediate_airports_route"]

    def is_accessible(self):
        return current_user.is_authenticated

    @is_admin  # Decorator kiểm soát quyền admin
    @expose('/')  # Trang chính của view
    def index_view(self):
        return super().index_view()

#chuyến bay
class FlightView(ModelView):
    column_list = ["id", "name", "flight_date", "flights_airplane", "flights_route", "flights_planner",
                   "ticket_prices", "tickets", "sub_flights"]

    def is_accessible(self):
        return current_user.is_authenticated

    @is_admin  # Decorator kiểm soát quyền admin
    @expose('/')  # Trang chính của view
    def index_view(self):
        return super().index_view()

#chuyến bay nhỏ
class SubFlightView(ModelView):
    column_list = ["id", "order", "flight_time", "flying_duration", "waiting_duration", "sub_flights_flight"]

    def is_accessible(self):
        return current_user.is_authenticated

    @is_admin  # Decorator kiểm soát quyền admin
    @expose('/')  # Trang chính của view
    def index_view(self):
        return super().index_view()

#gia ve
class TicketPriceView(ModelView):
    column_list = ["id", "price", "ticket_prices_seat_class", "ticket_prices_flight", "tickets"]

    def is_accessible(self):
        return current_user.is_authenticated

    @is_admin  # Decorator kiểm soát quyền admin
    @expose('/')  # Trang chính của view
    def index_view(self):
        return super().index_view()

#user
class UserView(ModelView):
    column_list = ["id", "first_name", "last_name", "username", "password"]

    def is_accessible(self):
        return current_user.is_authenticated

    @is_admin  # Decorator kiểm soát quyền admin
    @expose('/')  # Trang chính của view
    def index_view(self):
        return super().index_view()

#admin
class AdminWebsiteView(UserView):
    column_list = ["id", "first_name", "last_name", "username", "password"] + ["active", "rules"]

    def is_accessible(self):
        return current_user.is_authenticated

    @is_admin  # Decorator kiểm soát quyền admin
    @expose('/')  # Trang chính của view
    def index_view(self):
        return super().index_view()

#khách hàng
class CustomerView(UserView):
    column_list = ["id", "first_name", "last_name", "username", "password"] + ["phone_number", "email", "avatar", "receipts"]

    def is_accessible(self):
        return current_user.is_authenticated

    @is_admin  # Decorator kiểm soát quyền admin
    @expose('/')  # Trang chính của view
    def index_view(self):
        return super().index_view()

#nhân viên
class StaffView(UserView):
    column_list = ["id", "first_name", "last_name", "username", "password"] + ["active", "staff_role", "flights", "receipts"]

    def is_accessible(self):
        return current_user.is_authenticated

    @is_admin  # Decorator kiểm soát quyền admin
    @expose('/')  # Trang chính của view
    def index_view(self):
        return super().index_view()

#hóa đơn
class ReceiptView(ModelView):
    column_list = ["id", "pay_date", "receipts_customer", "receipts_seller", "tickets"]

    def is_accessible(self):
        return current_user.is_authenticated

    @is_admin  # Decorator kiểm soát quyền admin
    @expose('/')  # Trang chính của view
    def index_view(self):
        return super().index_view()

#người đi
class PassengerView(ModelView):
    column_list = ["id", "first_name", "last_name", "id_card_number", "phone_number", "ticket"]

    def is_accessible(self):
        return current_user.is_authenticated

    @is_admin  # Decorator kiểm soát quyền admin
    @expose('/')  # Trang chính của view
    def index_view(self):
        return super().index_view()

#vé máy bay
class TicketView(ModelView):
    column_list = ["id", "tickets_seat", "tickets_flight", "ticket_passenger", "tickets_ticket_price", "tickets_receipt"]

    def is_accessible(self):
        return current_user.is_authenticated

    @is_admin  # Decorator kiểm soát quyền admin
    @expose('/')  # Trang chính của view
    def index_view(self):
        return super().index_view()

#review
class ReviewView(ModelView):
    column_list = ["id", "reviewer_name", "vote", "content", "image", "review_date"]

    def is_accessible(self):
        return current_user.is_authenticated

    @is_admin  # Decorator kiểm soát quyền admin
    @expose('/')  # Trang chính của view
    def index_view(self):
        return super().index_view()

#thong bao
class NotificationView(ModelView):
    column_list = ["id", "title", "content", "image", "posting_date"]

    def is_accessible(self):
        return current_user.is_authenticated

    @is_admin  # Decorator kiểm soát quyền admin
    @expose('/')  # Trang chính của view
    def index_view(self):
        return super().index_view()

#qui định
class RuleView(ModelView):
    column_list = ["id", "name", "value", "rules_admin"]

    def is_accessible(self):
        return current_user.is_authenticated

    @is_admin  # Decorator kiểm soát quyền admin
    @expose('/')  # Trang chính của view
    def index_view(self):
        return super().index_view()

#đếm số lượng vé

class MyAdminView(AdminIndexView):
    @expose("/")
    @is_admin
    def index(self):
        tickets = dao.count_tickets()
        passengers = dao.count_passengers()
        total_revenue = dao.get_total_revenue()
        print(f"Tickets: {tickets}, Passengers: {passengers}, Total Revenue: {total_revenue}")
        return self.render("admin/index.html", tickets=tickets, passengers = passengers,total_revenue = total_revenue)


from flask import request


class StatsView(BaseView):
    @expose("/", methods=["GET", "POST"])
    @is_admin
    def index(self):
        year = datetime.now().year

        # Thống kê doanh thu theo tuyến bay trong năm hiện tại
        stats = dao.revenue_stats_by_routes()
        stats2 = dao.revenue_stats_by_time(year)

        return self.render('admin/stats.html',
                           stats=stats,
                           stats2=stats2,

                           # tickets=dao.count_tickets(),
                           passengers=dao.count_passengers(),
                           total_revenue=dao.get_total_revenue(),
                           )

    def is_accessible(self):
        return current_user.is_authenticated

#thêm máy bay
class AddAirplaneView(BaseView):
    @expose('/', methods=["GET", "POST"]) #chỉ định đường dẫn để map vào admin
    @is_admin
    def index(self):
        if request.method.__eq__('POST'):
            data = request.json
            name = data["name"]
            existing_airplane = dao.get_route_by_name(name=name)
            if existing_airplane:
                return jsonify({"status": "error", "message": "Đã tồn tại tên máy bay này"})
            manufacturer_id = int(data["manufacturer_id"])
            mfg_date = datetime.fromisoformat(data["mfg_date"])
            seat_quantity = int(data["seat_quantity"])
            seat_inputs = data["seat_inputs"]
            seat_class_id = 1
            start_number = 1
            seat_class_quantity = dao.count_seat_classes()
            try:
                airplane = dao.add_airplane_no_commit(name=name, manufacturer_id=manufacturer_id, mfg_date=mfg_date, seat_quantity=seat_quantity)
                for i in range(1, seat_class_quantity + 1):
                    seat_quantity = seat_inputs[str(i)]
                    dao.add_seats_no_commit(airplane=airplane, seat_class_id=seat_class_id,
                              start_number=start_number, quantity=seat_quantity)
                    start_number += seat_quantity
                    seat_class_id += 1
                db.session.commit()
                return jsonify({"status": "success", "message": "Thành công"})
            except Exception as e:
                return jsonify({"status": "error", "message": {str(e)}})
        manufacturers = dao.load_manufacturers()
        seat_classes = dao.load_seat_classes()
        return self.render('admin/add_airplane.html', manufacturers=manufacturers, seat_classes=seat_classes)

    def is_accessible(self):
        return current_user.is_authenticated


#thêm tuyến bay
class AddRouteView(BaseView):
    @expose('/', methods=["GET", "POST"])
    @is_admin
    def index(self):
        if request.method.__eq__("POST"):
            data = request.json
            name = data["name"]
            existing_route = dao.get_route_by_name(name=name)
            if existing_route:
                return jsonify({"status": "error", "message": "Đã tồn tại tên tuyến bay này"})

            departure_airport_id = int(data["departure_airport_id"])
            arrival_airport_id = int(data["arrival_airport_id"])
            intermediate_airport_quantity = int(data["intermediate_airport_quantity"])
            intermediate_airports = data["intermediate_airports"]
            try:
                route = dao.add_route_no_commit(name=name, departure_airport_id=departure_airport_id, arrival_airport_id=arrival_airport_id)
                for i in range(1, intermediate_airport_quantity + 1):
                    airport_id = intermediate_airports[str(i)]
                    dao.add_intermediate_airport_no_commit(order=i, airport_id=airport_id, route=route)
                return jsonify({"status": "success", "message": "Thành công"})
            except Exception as e:
                return jsonify({"status": "error", "message": {str(e)}})
        airports = dao.load_airports()
        max_intermediate_airport_quantity = app.config["MAX_INTERMEDIATE_AIRPORT_QUANTITY"]
        return self.render("admin/add_route.html", airports=airports,
                           max_intermediate_airport_quantity=max_intermediate_airport_quantity)

    def is_accessible(self):
        return current_user.is_authenticated



admin = Admin(app=app, name="Trang quản trị", template_mode="bootstrap4", index_view=MyAdminView())

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


#=========View=========#
admin.add_view(AddAirplaneView(name="Add Airplane", endpoint='add_airplane'))
admin.add_view(AddRouteView(name="Add Route", endpoint="add_route"))
admin.add_view(StatsView(name='Stats'))
#end======View=========#

