import json

from flask import request, redirect, render_template, jsonify, session
from flask_login import login_user, current_user
from datetime import datetime, timedelta
import hashlib
from app import app, controller, login, dao, admin, db
from app.dao import add_ticket_price
from app.models import User, Customer, SubFlight, Airplane

# gọi tới file html của staff
@app.route('/staff')
def staff_page():
    return render_template('staff/index.html')

# gọi.qual tới file html của thong tin tai khoan
@app.route("/info_page", methods=["GET","POST"])
def info_page():
    if request.method == "POST":
        oldPassword = request.form["oldPassword"]
        newPassword = request.form["newPassword"]
        confirmPassword = request.form["confirmPassword"]

        # Kiểm tra mật khẩu xác nhận
        if newPassword != confirmPassword:
            return jsonify({"status": "error", "message": "Mật khẩu xác nhận không khớp."})

        # Hash mật khẩu cũ
        oldPassword_hashed = str(hashlib.md5(oldPassword.encode('utf-8')).digest())

        # Kiểm tra mật khẩu cũ
        if oldPassword_hashed != current_user.password:
            return jsonify({"status": "error", "message": "Mật khẩu cũ không chính xác."})

        # Cập nhật mật khẩu mới
        dao.change_password(newPassword)
        return jsonify({"status": "success", "message": "Đổi mật khẩu thành công!"})

    return render_template('info.html')

#nhap id máy bay, tuyến bay, ngày giow
@app.route('/staff/scheduling1', methods=["POST", "GET"])
def staff_scheduling1():
    if request.method.__eq__("POST"):
        key = app.config["KEY_SCHEDULING"]
        data = request.json
        name = data["name"]

        existing_flight = dao.load_flight_by_name(name)
        if existing_flight:
            return jsonify({"status": "error", "message": "Tên chuyến bay đã tồn tại"})

        airplane_id = int(data["airplane_id"])
        flight_date = data["flight_date"]
        route_id = data["route_id"]
        departure_airport_id = data["departure_airport_id"]
        arrival_airport_id = data["arrival_airport_id"]


        session[key] = {
            "name": name,
            "airplane_id": airplane_id,
            "route_id": route_id,
            "departure_airport_id": departure_airport_id,
            "arrival_airport_id": arrival_airport_id,
            "flight_date": flight_date,
        }
        print(session[key])
        return jsonify({"status": "success", "redirect": "/staff/scheduling2"})

    airplanes = dao.load_airplanes()
    airports = dao.load_airports()
    routes = dao.load_route()
    return render_template('staff/scheduling1.html',
                           airplanes=airplanes, airports=airports, routes=routes)

@app.route('/staff/scheduling2',  methods=["POST", "GET"])
def staff_scheduling2():
    #lấy dữ liệu từ session
    key = app.config["KEY_SCHEDULING"]
    flight_info = session[key]
    name = flight_info["name"]
    airplane_id = flight_info["airplane_id"]
    route_id = flight_info["route_id"]
    departure_airport_id = flight_info["departure_airport_id"]
    arrival_airport_id = flight_info["arrival_airport_id"]
    flight_date = datetime.fromisoformat(flight_info["flight_date"])

    #xếp airport vào 1 mảng theo thứ tự
    airport_array = []

    departure_airport = dao.load_airport_by_id(departure_airport_id)
    arrival_airport = dao.load_airport_by_id(arrival_airport_id)


    airport_array.append(departure_airport)

    intermediate_airports = dao.load_intermediate_airports_by_route_id(route_id)
    for intermediate_airport in intermediate_airports:
        airport = dao.load_airport_by_id(intermediate_airport.airport_id)
        airport_array.append(airport)

    airport_array.append(arrival_airport)
    print(airport_array, len(airport_array))

    #lấy seat_class có trong máy bay đó
    seat_classes = dao.count_seats_in_seat_classes_by_airplane_id(airplane_id)

    if request.method.__eq__("POST"):
        try:
            data = request.json
            ticket_prices = data["ticket_prices"]
            waiting_durations = data["waiting_durations"]
            flying_durations = data["flying_duration"]

            total_time = 0
            for i in range(1, len(airport_array)):
                waiting_duration = waiting_durations[str(i)]
                flying_duration = flying_durations[str(i)]
                total_time += waiting_duration
                total_time += flying_duration

            dao.add_flight(name=name, flight_date=flight_date, airplane_id=airplane_id,
                           route_id=route_id, planner_id=current_user.id, total_time=total_time)
            flight = dao.load_flight_by_name(name=name)



            for i in range(1, len(seat_classes) + 1):
                seat_class_id = seat_classes[i - 1].id
                price = ticket_prices[str(i)]
                add_ticket_price(price=price, seat_class_id=seat_class_id, flight_id=flight.id)


            flight_time = flight.flight_date
            for i in range(1, len(airport_array)):
                waiting_duration = waiting_durations[str(i)]
                flying_duration = flying_durations[str(i)]
                flight_time = flight_time + timedelta(minutes=waiting_duration)
                dao.add_sub_flight(order=i, flight_time=flight_time,
                                   waiting_duration=waiting_duration,
                                   flying_duration=flying_duration,
                                   flight_id=flight.id)
                flight_time = flight_time + timedelta(minutes=flying_duration)
            return jsonify({"status": "success", "redirect": "/staff/scheduling1"})
        except Exception as e:
            return jsonify({"status": "error", "message": {str(e)}})

    return render_template('staff/scheduling2.html',
                           seat_classes=seat_classes,
                           airport_array=airport_array)

@app.route('/staff/selling.html')
def staff_selling():
    return render_template('staff/selling.html')

# load trang chủ
app.add_url_rule("/", "index", controller.index, methods=["GET", "POST"])

#load trang đăng nhập
app.add_url_rule("/login", "login", controller.login_my_user, methods=["POST", "GET"])

#load trang đăng ký
app.add_url_rule("/register", "register", controller.register, methods=["POST", "GET"])

#api mã xác nhận
app.add_url_rule("/api/verify_code", "verify_code", controller.type_verify_code, methods=["POST"])

#api xóa mã xác nhận
app.add_url_rule("/api/clear_verify_code", "clear_verify_code", controller.clear_verify_code, methods=["POST"])

#api thêm vé
app.add_url_rule("/api/cart", "add_seat", controller.add_seat, methods=["POST"])

#api xóa vé
app.add_url_rule("/api/cart/<seat_id>", "api_cart_seatId_delete", controller.delete_seat, methods=["DELETE"])

#log out
app.add_url_rule("/logout", "logout", controller.logout_my_user)

#tìm user theo user_id
@login.user_loader
def load_user(id):
    #nếu là customer
    if dao.get_customer_by_id(id):
        return dao.get_customer_by_id(id)
    elif dao.get_staff_by_id(id):
        return dao.get_staff_by_id(id)
    elif dao.get_admin_by_id(id):
        return dao.get_admin_by_id(id)
    else:
    # nếu là user
        return dao.get_user_by_id(id)

#load trang kết quả tìm kiếm
app.add_url_rule("/search_result", "search_result", controller.search_result, methods=["GET", "POST"])

#load trang đặt vé
app.add_url_rule("/booking/<int:flight_id>", "booking", controller.booking, methods=["GET", "POST"])

#load trang nhập thông tin hành khách
app.add_url_rule("/passenger_information", "passenger_information", controller.passenger_information, methods=["GET", "POST"])

#load trang thanh toán
app.add_url_rule("/pay", "pay", controller.pay, methods=["GET", "POST"])

#load trang kết quả thanh toán
app.add_url_rule("/payment_return", "payment_return", controller.payment_return, methods=["GET", "POST"])

#load trang chu admin
app.add_url_rule("/login-admin", "login_admin", controller.admin_login, methods=['POST', 'GET'])



if __name__ == "__main__":
    app.run(debug=True)



