import hmac
import math
import urllib.parse
import hashlib
from datetime import datetime, timedelta

from sqlalchemy.testing.suite.test_reflection import users

from app import mail, vnpay, login, table_class
from app.models import PaymentMethod
from flask_login import login_user, current_user, logout_user, login_required
from flask import jsonify, session, url_for
from flask import request, redirect, render_template
from app import app, db, dao, utils
from app.dao import load_popular_routes, load_seat_classes_with_ticket_price_by_flight_id, \
    count_remaining_seats_per_seat_class_by_airplane_id
from app.decorators import anonymous_customer, anonymous_staff, anonymous_admin, is_customer, is_staff, is_admin, \
    for_staff_seller, for_staff_planner
import hashlib
import cloudinary.uploader


# trang chủ
@is_customer
def index():
    key = app.config["KEY_CART"]
    session[key] = {}

    session[app.config["TIME_TO_BOOKING"]] = int(dao.get_rule_by_name(app.config["TIME_TO_BOOKING"]).value)

    reviews = dao.load_reviews()
    notifications = dao.load_notifications()
    popular_routes = load_popular_routes()

    return render_template("index.html", reviews=reviews, notifications=notifications, popular_routes=popular_routes)


# đăng nhập
@anonymous_customer
@is_customer
def login_my_user():
    if request.method.__eq__("POST"):
        user_name = request.form["user_name"]
        password = request.form["password"]
        user = dao.auth_customer(user_name.strip(), password)
        if user:
            login_user(user=user)
            next = request.form["next"]
            return jsonify({"status": "success", "redirect": next})
        else:
            return jsonify({"status": "error", "message": "Tài khoản không tồn tại."})
    return render_template("login.html")


# dang xuat
@login_required
def logout_my_user():
    logout_user()
    return redirect("/")


# đăng ký
@is_customer
def register():
    if request.method.__eq__('POST'):

        # user_name đã tồn tại
        user_name = request.form.get("user_name").strip()
        existing_user = dao.get_user_by_user_name(user_name=user_name)
        if existing_user :
            return jsonify({"status": "error", "message": "Tên đăng nhập đã tồn tại."})

        phone_number = request.form.get("phone_number").strip()
        # số điện thoại khác 10
        if len(phone_number) != app.config["PHONE_NUMBER_LENGTH"]:
            return jsonify(
                {"status": "error", "message": f"Số điện thoại không hợp lệ ({app.config["PHONE_NUMBER_LENGTH"]} số)."})
        # số điện thoại đã tồn tại
        existing_customer = dao.get_customer_by_phone_number(phone_number=phone_number)
        if existing_customer and existing_customer.user_name and existing_customer.password:
            return jsonify({"status": "error", "message": "Số điện thoại đã tồn tại."})

        email = request.form.get("email").strip()
        # email không hợp lệ
        if utils.verify_email(email):
            return jsonify({"status": "error", "message": "Email không hợp lệ"})
        # email đã tồn tại
        existing_customer = dao.get_customer_by_email(email=email)
        if existing_customer:
            return jsonify({"status": "error", "message": "Email đã tồn tại."})

        # mật khẩu quá ngắn
        password = request.form.get("password").strip()
        if len(password) < app.config["PASSWORD_LENGTH"]:
            return jsonify(
                {"status": "error", "message": f"Mật khẩu quá ngắn (lớn hơn {app.config["PASSWORD_LENGTH"]} ký tự.)"})
        # mật khẩu không khớp
        confirm_password = request.form.get("confirm_password").strip()
        if not password.__eq__(confirm_password):
            return jsonify({"status": "error", "message": "Mật khẩu không khớp"})

        key = app.config["KEY_VERIFY_EMAIL"]
        verify_code = session[key]["verify_code"]
        code = int(request.form.get("verify_code").strip())
        if verify_code and code and code != verify_code:
            return jsonify({"status": "error", "message": "Sai mã xác nhận"})

        first_name = request.form.get("first_name").strip()
        last_name = request.form.get("last_name").strip()
        avatar = request.files.get("avatar")
        res = cloudinary.uploader.upload(avatar)
        avatar = res["secure_url"]
        # save user
        try:
            dao.register(first_name=first_name,
                         last_name=last_name,
                         user_name=user_name,
                         password=password,
                         phone_number=phone_number,
                         email=email,
                         avatar=avatar)
            return jsonify({"status": "success", "redirect": "/login"})
        except Exception as e:
            return jsonify({"status": "error", "message": {str(e)}})
    return render_template("register.html")


# nhập mã xác nhận
@is_customer
def type_verify_code():
    key = app.config["KEY_VERIFY_EMAIL"]
    data = request.json
    session[key] = data

    import random
    verify_code = random.randint(1000, 9999)
    email_target = data["email_target"]
    data["verify_code"] = verify_code

    if utils.verify_email(email_target):
        return jsonify({"status": "error", "message": "Email không hợp lệ"})
    else:
        mail.send_authenticate_mail(email_target, subject="Verify Code", body=str(verify_code))
        return jsonify(
            {"status": "success", "message": "Gửi mã thành công. Bạn có thể ấn vào nút Đổi thông tin để nhập lại"})


# xóa mã xác nhận
def clear_verify_code():
    data = request.json
    key = app.config["KEY_VERIFY_EMAIL"]
    session[key] = data
    return jsonify({"status": "success", "message": "Mã xác nhận đã xóa, bạn có thể nhập lại thông tin"})


# kết quả tìm kiếm
@is_customer
def search_result():
    key = app.config["KEY_CART"]
    session[key] = {}

    start_point = request.args.get("start_point")
    end_point = request.args.get("end_point")
    flight_date = request.args.get("flight_date")
    if flight_date:
        flight_date = datetime.strptime(flight_date, "%Y-%m-%d")

    page = int(request.args.get("page", 1))
    page_size = app.config["PAGE_SIZE"]

    flights = dao.load_flight_for_search_result(start_point, end_point, flight_date, time=session[app.config["TIME_TO_BOOKING"]])
    page_count = len(flights)

    start = (page - 1) * page_size
    flights = flights[start:start + page_size]

    seat_classes_array = []
    remaining_seat_array = []
    for flight in flights:
        seat_classes_array.append(load_seat_classes_with_ticket_price_by_flight_id(flight.id))
        remaining_seat_array.append(count_remaining_seats_per_seat_class_by_airplane_id(flight.airplane_id))
    return render_template("search_result.html",
                           flights=flights,
                           start_point=start_point,
                           end_point=end_point,
                           flight_date=flight_date,
                           pages=math.ceil(math.ceil(page_count / page_size)),
                           seat_classes_array=seat_classes_array,
                           remaining_seat_array=remaining_seat_array)


# trang đặt vé
@is_customer
def booking(flight_id):
    flight_id_session = app.config["FLIGHT_ID"]
    if flight_id_session in session and session[flight_id_session] != flight_id:
        key = app.config["KEY_CART"]
        session[key] = {}
    session[flight_id_session] = flight_id

    seat_classes = load_seat_classes_with_ticket_price_by_flight_id(flight_id)
    seats = dao.load_seats_by_flight_id(flight_id)
    cart = session[app.config["KEY_CART"]]
    total_amount = 0
    total_quantity = 0
    chosen_seats = ""
    for c in cart.values():
        chosen_seats += c["seat_name"] + " "
        total_quantity += 1
        total_amount += c["ticket_price"]
    return render_template("booking.html",
                           seat_classes=seat_classes,
                           seats=seats,
                           flight_id=flight_id,
                           total_amount=total_amount,
                           total_quantity=total_quantity,
                           chosen_seats=chosen_seats)


# api thêm vé
def add_seat():
    key = app.config["KEY_CART"]
    cart = session[key] if key in session else {}
    data = request.json
    seat_id = data["seat_id"]

    seat = dao.get_seat_by_id(seat_id)
    if seat.active:
        return jsonify({"status": "error", "message": "Ghế đã được đặt rồi"})

    seat_id = str(seat_id)
    if seat_id in cart:
        return jsonify({"status": "error", "message": "Bạn đã chọn ghế này rồi"})
    else:
        seat_name = data["seat_name"]
        seat_class_name = data["seat_class_name"]
        ticket_price = data["ticket_price"]
        ticket_price_id = data["ticket_price_id"]
        cart[seat_id] = {
            "seat_id": seat_id,
            "seat_name": seat_name,
            "seat_class_name": seat_class_name,
            "ticket_price": ticket_price,
            "ticket_price_id": ticket_price_id
        }
        session[key] = cart
        return jsonify(utils.cart_stats(cart))


# api xóa vé
def delete_seat(seat_id):
    key = app.config["KEY_CART"]
    cart = session.get(key)

    if cart and seat_id in cart:
        del cart[seat_id]

    session[key] = cart
    return jsonify(utils.cart_stats(cart=cart))


# trang nhập thông tin khách hàng
@login_required
@is_customer
def passenger_information():
    key = app.config["KEY_CART"]
    cart = session[key]
    session[app.config["KEY_PASSENGER"]] = {}

    seat_name_array = []
    seat_id_array = []
    total_amount = 0
    total_quantity = 0
    for c in cart.values():
        total_quantity += 1
        total_amount += c["ticket_price"]
        seat_id_array.append(c["seat_id"])
        seat_name_array.append(c["seat_name"])
    if request.method.__eq__("POST"):
        data = request.json
        session[app.config["KEY_PASSENGER"]] = data
        # print(session[app.config["KEY_PASSENGER"]])
        # print(cart)

        return jsonify({"status": "success", "redirect": "/pay"})

    return render_template("passenger_information.html",
                           seat_name_array=seat_name_array)


# thanh toán
@login_required
@is_customer
def pay():
    key_cart = app.config["KEY_CART"]
    cart = session[key_cart]
    passengers = session[app.config["KEY_PASSENGER"]]
    total_amount = 0
    total_quantity = 0
    for c in cart.values():
        total_quantity += 1
        total_amount += c["ticket_price"]
    if request.method.__eq__("POST"):
        order_id = "{:010}".format(current_user.id) + str(datetime.now())
        vnpay_payment_url = vnpay.generate_payment_url(order_id=order_id, amount=total_amount, end_point="payment_return")
        return jsonify({"status": "success", "redirect": vnpay_payment_url})

    flight = dao.get_flight_by_id(session[app.config["FLIGHT_ID"]])
    airplane = dao.get_air_plane_by_id(flight.airplane_id)
    route = dao.get_route_by_id(flight.route_id)
    # xếp airport vào 1 mảng theo thứ tự
    airport_array = []

    departure_airport = dao.get_airport_by_id(route.departure_airport_id)
    arrival_airport = dao.get_airport_by_id(route.arrival_airport_id)

    airport_array.append(departure_airport)

    intermediate_airports = dao.load_intermediate_airports_by_route_id(route.id)
    for intermediate_airport in intermediate_airports:
        airport = dao.get_airport_by_id(intermediate_airport.airport_id)
        airport_array.append(airport)

    airport_array.append(arrival_airport)

    sub_flights = dao.load_sub_flight_by_flight_id(flight.id)

    return render_template("pay.html",
                           total_amount=total_amount,
                           total_quantity=total_quantity,
                           tickets=list(cart.values()),
                           passengers=list(passengers.values()),
                           airplane_name=airplane.name,
                           sub_flights=sub_flights,
                           airport_array=airport_array,
                           flight_date=flight.flight_date)


# kết quả thanh toán
@login_required
@is_customer
def payment_return():
    query_params = request.args.to_dict()
    vnp_secure_hash = query_params.pop("vnp_SecureHash", None)

    sorted_params = sorted(query_params.items())
    query_string = "&".join(f"{k}={urllib.parse.quote_plus(str(v))}" for k, v in sorted_params)
    hmac_obj = hmac.new(vnpay.VNP_HASH_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha512)
    expected_hash = hmac_obj.hexdigest()

    if vnp_secure_hash == expected_hash and query_params.get("vnp_ResponseCode") == "00":
        order_id = query_params.get("vnp_TxnRef")
        amount = int(query_params.get("vnp_Amount")) // 100
        payment_method = PaymentMethod.BANKING
        cart = session[app.config["KEY_CART"]]
        passenger_infos = session[app.config["KEY_PASSENGER"]]
        dao.add_receipt(cart=cart,
                        passenger_infos=passenger_infos,
                        order_id=order_id,
                        payment_method=payment_method,
                        customer_id=current_user.id)

        ticket_infos = []
        seat_ids = []
        flight_name = dao.get_flight_by_id(session[app.config["FLIGHT_ID"]]).name
        cart_data = list(cart.values())
        passenger_data = list(passenger_infos.values())
        content = ""
        for i in range(len(cart_data)):
            order_id_tmp = utils.parse_to_valid_file_name(order_id)
            send_code = f"{order_id_tmp}{'{:010}'.format(cart_data[i]["seat_id"])}"
            ticket_content = f'''
                       Mã vé: {send_code}
                       Chuyến bay: {flight_name}
                       Hành khách: {passenger_data[i]["last_name"]} {passenger_data[i]["first_name"]}
                       CMND/CCCD: {passenger_data[i]["id_card_number"]}
                       SĐT: {passenger_data[i]["phone_number"]}
                       Hạng ghế: {cart_data[i]["seat_class_name"]}
                       Giá vé: {"{:,.0f}".format(cart_data[i]["ticket_price"])}
                       ========================================================
                       '''
            content += ticket_content

        mail.send_authenticate_mail(current_user.email, "Xác nhận mua vé", body=content)



        return render_template("payment_return.html", is_success=True, amount=amount)
    else:
        return render_template("payment_return.html", is_success=False)


# gọi.qual tới file html của thong tin tai khoan
@login_required
@is_customer
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


# ======staff=======#

# gọi tới file html của staff
@app.route('/staff/index.html')
@is_staff
def staff_page():
    session[app.config["TIME_TO_SELLING"]] = int(dao.get_rule_by_name(app.config["TIME_TO_SELLING"]).value)
    session[app.config["MIN_FLYING_DURATION"]] = int(dao.get_rule_by_name(app.config["MIN_FLYING_DURATION"]).value)
    session[app.config["MIN_WAITING_DURATION"]] = int(dao.get_rule_by_name(app.config["MIN_WAITING_DURATION"]).value)
    session[app.config["MAX_WAITING_DURATION"]] = int(dao.get_rule_by_name(app.config["MAX_WAITING_DURATION"]).value)

    return render_template('/staff/index.html')


# trang chu staff
@anonymous_staff
def staff_login():
    user_name = request.form['username']
    password = request.form['password']
    staff = dao.auth_staff(user_name=user_name, password=password)
    print(staff.staff_role)
    print(type(staff.staff_role))
    print(str(staff.staff_role))
    if staff:
        login_user(staff)
    return redirect('/staff')


# dat lich1
@login_required
@is_staff
@for_staff_planner
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
                           airplanes=airplanes,
                           airports=airports,
                           routes=routes)


# dat lich2
@login_required
@is_staff
@for_staff_planner
def staff_scheduling2():
    # lấy dữ liệu từ session
    key = app.config["KEY_SCHEDULING"]
    flight_info = session[key]
    name = flight_info["name"]
    airplane_id = flight_info["airplane_id"]
    route_id = flight_info["route_id"]
    departure_airport_id = flight_info["departure_airport_id"]
    arrival_airport_id = flight_info["arrival_airport_id"]
    flight_date = datetime.fromisoformat(flight_info["flight_date"])

    # xếp airport vào 1 mảng theo thứ tự
    airport_array = []

    departure_airport = dao.get_airport_by_id(departure_airport_id)
    arrival_airport = dao.get_airport_by_id(arrival_airport_id)

    airport_array.append(departure_airport)

    intermediate_airports = dao.load_intermediate_airports_by_route_id(route_id)
    for intermediate_airport in intermediate_airports:
        airport = dao.get_airport_by_id(intermediate_airport.airport_id)
        airport_array.append(airport)

    airport_array.append(arrival_airport)

    # lấy seat_class có trong máy bay đó
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
                dao.add_ticket_price(price=price, seat_class_id=seat_class_id, flight_id=flight.id)

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
                           airport_array=airport_array,
                           min_flying_duration=session[app.config["MIN_FLYING_DURATION"]],
                           min_waiting_duration=session[app.config["MIN_WAITING_DURATION"]],
                           max_waiting_duration=session[app.config["MAX_WAITING_DURATION"]])


# tìm kiếm chuyến bay cho nhân viên
@login_required
@is_staff
@for_staff_seller
def search_result_staff():
    key = app.config["KEY_CART"]
    session[key] = {}

    start_point = request.args.get("start_point")
    end_point = request.args.get("end_point")
    flight_date = request.args.get("flight_date")
    if flight_date:
        flight_date = datetime.strptime(flight_date, "%Y-%m-%d")

    page = int(request.args.get("page", 1))
    page_size = app.config["PAGE_SIZE"]

    flights = dao.load_flight_for_search_result(start_point, end_point, flight_date)
    page_count = len(flights)

    start = (page - 1) * page_size
    flights = flights[start:start + page_size]

    seat_classes_array = []
    remaining_seat_array = []
    for flight in flights:
        seat_classes_array.append(load_seat_classes_with_ticket_price_by_flight_id(flight.id))
        remaining_seat_array.append(count_remaining_seats_per_seat_class_by_airplane_id(flight.airplane_id))
    return render_template('staff/search_result_staff.html',
                           flights=flights,
                           start_point=start_point,
                           end_point=end_point,
                           pages=math.ceil(math.ceil(page_count / page_size)),
                           flight_date=flight_date,
                           seat_classes_array=seat_classes_array,
                           remaining_seat_array=remaining_seat_array)


# ban ve
@login_required
@is_staff
@for_staff_seller
def staff_selling(flight_id):
    flight_id_session = app.config["FLIGHT_ID"]
    if flight_id_session in session and session[flight_id_session] != flight_id:
        key = app.config["KEY_CART"]
        session[key] = {}
    session[flight_id_session] = flight_id

    seat_classes = load_seat_classes_with_ticket_price_by_flight_id(flight_id)
    seats = dao.load_seats_by_flight_id(flight_id)
    cart = session[app.config["KEY_CART"]]
    total_amount = 0
    total_quantity = 0
    chosen_seats = ""
    for c in cart.values():
        chosen_seats += c["seat_name"] + " "
        total_quantity += 1
        total_amount += c["ticket_price"]
    return render_template("staff/selling.html",
                           seat_classes=seat_classes,
                           seats=seats,
                           flight_id=flight_id,
                           total_amount=total_amount,
                           total_quantity=total_quantity,
                           chosen_seats=chosen_seats)


# nhap thong tin hang khach
@login_required
@is_staff
@for_staff_seller
def passenger_information_staff():
    key = app.config["KEY_CART"]
    cart = session[key]
    session[app.config["KEY_PASSENGER"]] = {}

    seat_name_array = []
    seat_id_array = []
    total_amount = 0
    total_quantity = 0
    for c in cart.values():
        total_quantity += 1
        total_amount += c["ticket_price"]
        seat_id_array.append(c["seat_id"])
        seat_name_array.append(c["seat_name"])
    if request.method.__eq__("POST"):
        data = request.json
        session[app.config["KEY_PASSENGER"]] = data
        # print(session[app.config["KEY_PASSENGER"]])
        # print(cart)

        return jsonify({"status": "success", "redirect": "/staff/customer_information"})

    return render_template("staff/passenger_information.html",
                           seat_name_array=seat_name_array)


# nhập thông tin khách hàng
@login_required
@is_staff
@for_staff_seller
def customer_information():
    if request.method.__eq__("POST"):
        data = request.json
        phone_number = data["phone_number"]
        print(phone_number)
        if len(phone_number) != app.config["PHONE_NUMBER_LENGTH"]:
            return jsonify({
                "status": "error",
                "message": "Số điện thoại phải có 10 số"
            })
        customer = dao.get_customer_by_phone_number(phone_number)
        if not customer:
            last_name = data["last_name"]
            first_name = data["first_name"]
            print(last_name)
            print(first_name)
            dao.add_unregisted_customer(phone_number=phone_number, last_name=last_name, first_name=first_name, user_name=first_name)
            customer = dao.get_customer_by_phone_number(phone_number)
        session[app.config["CUSTOMER_ID"]] = customer.customer_id
        return jsonify({"status": "success", "redirect": "/staff/pay"})

    return render_template("staff/customer_information.html")


# api check số điện thoại
def check_phone_number():
    data = request.json
    phone_number = data["phone_number"]
    if len(phone_number) != app.config["PHONE_NUMBER_LENGTH"]:
        return jsonify({
            "status": "error",
            "message": "Số điện thoại phải có 10 số"
        })
    customer = dao.get_customer_by_phone_number(phone_number)
    if customer:
        return jsonify({
            "status": "exist",
            "first_name": customer.first_name,
            "last_name": customer.last_name})
    else:
        return jsonify({
            "status": "not_exist"
        })

@login_required
@is_staff
@for_staff_seller
def pay_staff():
    key_cart = app.config["KEY_CART"]
    cart = session[key_cart]
    passengers = session[app.config["KEY_PASSENGER"]]
    total_amount = 0
    total_quantity = 0
    order_id = "{:010}".format(current_user.id) + str(datetime.now())
    for c in cart.values():
        total_quantity += 1
        total_amount += c["ticket_price"]
    if request.method.__eq__("POST"):
        payment_method = request.json["payment_method"]
        if PaymentMethod[payment_method] == PaymentMethod.CASHING:
            return jsonify({"status": "success", "redirect": str(url_for("payment_return_staff",
                                                                     payment_method=payment_method,
                                                                     order_id=order_id,
                                                                     amount=total_amount))})
        elif PaymentMethod[payment_method] == PaymentMethod.BANKING:
            vnpay_payment_url = vnpay.generate_payment_url(order_id=order_id, amount=total_amount, end_point="staff/payment_return")
            return jsonify({"status": "success", "redirect": vnpay_payment_url})

    flight = dao.get_flight_by_id(session[app.config["FLIGHT_ID"]])
    airplane = dao.get_air_plane_by_id(flight.airplane_id)
    route = dao.get_route_by_id(flight.route_id)
    # xếp airport vào 1 mảng theo thứ tự
    airport_array = []

    departure_airport = dao.get_airport_by_id(route.departure_airport_id)
    arrival_airport = dao.get_airport_by_id(route.arrival_airport_id)

    airport_array.append(departure_airport)

    intermediate_airports = dao.load_intermediate_airports_by_route_id(route.id)
    for intermediate_airport in intermediate_airports:
        airport = dao.get_airport_by_id(intermediate_airport.airport_id)
        airport_array.append(airport)

    airport_array.append(arrival_airport)

    sub_flights = dao.load_sub_flight_by_flight_id(flight.id)

    payment_methods = {payment_method.name: payment_method.value for payment_method in PaymentMethod}

    customer = dao.get_customer_by_id(session[app.config["CUSTOMER_ID"]])
    return render_template("staff/pay.html",
                           total_amount=total_amount,
                           total_quantity=total_quantity,
                           tickets=list(cart.values()),
                           passengers=list(passengers.values()),
                           airplane_name=airplane.name,
                           sub_flights=sub_flights,
                           airport_array=airport_array,
                           customer=customer,
                           flight_date=flight.flight_date,
                           payment_methods=payment_methods)

@login_required
@is_staff
@for_staff_seller
def payment_return_staff():
    payment_method = request.args.get("payment_method")
    cart = session[app.config["KEY_CART"]]
    passenger_infos = session[app.config["KEY_PASSENGER"]]

    ticket_infos = []
    seat_ids = []
    flight_name = dao.get_flight_by_id(session[app.config["FLIGHT_ID"]]).name
    cart_data = list(cart.values())
    passenger_data = list(passenger_infos.values())
    for i in range(len(cart_data)):
        ticket_info = {
            "flight": flight_name,
            "passenger": f"{passenger_data[i]["last_name"]} {passenger_data[i]["first_name"]}",
            "id_card_number": passenger_data[i]["id_card_number"],
            "phone_number": passenger_data[i]["phone_number"],
            "seat_class": cart_data[i]["seat_class_name"],
            "ticket_price": "{:,.0f}".format(cart_data[i]["ticket_price"])
        }
        ticket_infos.append(ticket_info)
        seat_ids.append(cart_data[i]["seat_id"])

    if payment_method and payment_method == "CASHING":
        amount = float(request.args.get("amount"))
        order_id = request.args.get("order_id")
        payment_method = PaymentMethod[payment_method]
        dao.add_receipt(cart=cart,
                        passenger_infos=passenger_infos,
                        order_id=order_id,
                        payment_method=payment_method,
                        customer_id=session[app.config["CUSTOMER_ID"]])
        for i in range(len(ticket_infos)):
            order_id_tmp = utils.parse_to_valid_file_name(order_id)

            pdf_path = f"pdf/{order_id_tmp}{'{:010}'.format(seat_ids[i])}.pdf"
            table_class.export_ticket(ticket_data=ticket_infos[i], pdf_path=pdf_path)
        return render_template("staff/payment_return.html", is_success=True, amount=amount)
    else:
        query_params = request.args.to_dict()
        vnp_secure_hash = query_params.pop("vnp_SecureHash", None)

        sorted_params = sorted(query_params.items())
        query_string = "&".join(f"{k}={urllib.parse.quote_plus(str(v))}" for k, v in sorted_params)
        hmac_obj = hmac.new(vnpay.VNP_HASH_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha512)
        expected_hash = hmac_obj.hexdigest()

        if vnp_secure_hash == expected_hash and query_params.get("vnp_ResponseCode") == "00":
            order_id = query_params.get("vnp_TxnRef")
            amount = int(query_params.get("vnp_Amount")) // 100
            payment_method = PaymentMethod.BANKING
            dao.add_receipt(cart=cart,
                            passenger_infos=passenger_infos,
                            order_id=order_id,
                            payment_method=payment_method,
                            customer_id=session[app.config["CUSTOMER_ID"]])

            for i in range(len(ticket_infos)):
                order_id_tmp = utils.parse_to_valid_file_name(order_id)
                pdf_path = f"pdf/{order_id_tmp}{'{:010}'.format(seat_ids[i])}.pdf"
                table_class.export_ticket(ticket_data=ticket_infos[i], pdf_path=pdf_path)

            return render_template("staff/payment_return.html", is_success=True, amount=amount)
        else:
            return render_template("staff/payment_return.html", is_success=False)

@login_required
@is_staff
@for_staff_seller
def export_ticket():
    if request.method.__eq__("POST"):
        data = request.json
        ticket_code = data["ticket_code"]
        seat_id = (ticket_code[-10:0])
        order_id = ticket_code[0: -10]
        order_id = order_id.replace("d", ".")
        order_id = order_id.replace("_", " ")

        order_id1 = order_id[:21]
        order_id2 = order_id[21:].replace("-", ":")
        order_id = order_id1 + order_id2

        print(order_id)
        print(dao.get_receipt_by_order_id(order_id))

    return render_template("staff/export_ticket.html")

#api kiểm tra ticket code
def check_ticket_code():
    pass



# end=======staff========#

# =========admin========#

# trang chu admin
@anonymous_admin
def admin_login():
    user_name = request.form['username']
    password = request.form['password']
    admin = dao.auth_admin(user_name=user_name, password=password)

    if admin:
        login_user(admin)
    return redirect('/admin')

# end======admin========#
