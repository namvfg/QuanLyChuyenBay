import hmac
import urllib.parse
import hashlib
from datetime import datetime, timedelta
from app import mail, vnpay
from app.models import PaymentMethod
from flask_login import login_user,current_user, logout_user, login_required
from flask import jsonify, session, url_for
from flask import request, redirect, render_template
from app import app, db, dao, utils
from app.dao import load_popular_routes, load_seat_classes_with_ticket_price_by_flight_id, add_ticket_price
from app.decorators import annonymous_user
import hashlib
import cloudinary.uploader


#trang chủ
def index():
    key = app.config["KEY_CART"]
    session[key] = {}

    reviews = dao.load_reviews()
    notifications = dao.load_notifications()
    popular_routes = load_popular_routes()

    return render_template("index.html", reviews=reviews, notifications=notifications, popular_routes=popular_routes)

#đăng nhập
@annonymous_user
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

#đăng ký
def register():
    if request.method.__eq__('POST'):

        #user_name đã tồn tại
        user_name = request.form.get("user_name").strip()
        existing_user = dao.get_user_by_user_name(user_name=user_name)
        if existing_user:
            return jsonify({"status": "error", "message": "Tên đăng nhập đã tồn tại."})


        phone_number = request.form.get("phone_number").strip()
        # số điện thoại khác 10
        if len(phone_number) != app.config["PHONE_NUMBER_LENGTH"]:
            return jsonify({"status": "error", "message": f"Số điện thoại không hợp lệ ({app.config["PHONE_NUMBER_LENGTH"]} số)."})
        # số điện thoại đã tồn tại
        existing_customer = dao.get_customer_by_phone_number(phone_number=phone_number)
        if existing_customer:
            return jsonify({"status": "error", "message": "Số điện thoại đã tồn tại."})

        email = request.form.get("email").strip()
        #email không hợp lệ
        if utils.verify_email(email):
            return jsonify({"status": "error", "message": "Email không hợp lệ"})
        #email đã tồn tại
        existing_customer = dao.get_customer_by_email(email=email)
        if existing_customer:
            return jsonify({"status": "error", "message": "Email đã tồn tại."})

        #mật khẩu quá ngắn
        password = request.form.get("password").strip()
        if len(password) < app.config["PASSWORD_LENGTH"]:
            return jsonify({"status": "error", "message": f"Mật khẩu quá ngắn (lớn hơn {app.config["PASSWORD_LENGTH"]} ký tự.)"})
        #mật khẩu không khớp
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

#nhập mã xác nhận
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
        return jsonify({"status": "success", "message": "Gửi mã thành công. Bạn có thể ấn vào nút Đổi thông tin để nhập lại"})

#xóa mã xác nhận
def clear_verify_code():
    data = request.json
    key = app.config["KEY_VERIFY_EMAIL"]
    session[key] = data
    return jsonify({"status": "success", "message": "Mã xác nhận đã xóa, bạn có thể nhập lại thông tin"})

#dang xuat
@login_required
def logout_my_user():
    logout_user()
    return redirect("/")

#ban ve
@login_required
def staff_selling():
    return render_template('staff/selling.html')

#kết quả tìm kiếm
def search_result():
    key = app.config["KEY_CART"]
    session[key] = {}

    start_point = request.args.get("start_point")
    end_point = request.args.get("end_point")
    flight_date = request.args.get("flight_date")
    if flight_date:
        flight_date = datetime.strptime(flight_date, "%Y-%m-%d")
    flights = dao.load_flight_for_search_result(start_point, end_point, flight_date)
    return render_template("search_result.html", flights=flights, start_point=start_point, end_point=end_point, flight_date=flight_date)

#trang đặt vé
def booking(flight_id):
    app.config["FLIGHT_ID"] = flight_id
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

#api thêm vé
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

#xóa vé
def delete_seat(seat_id):
    key = app.config["KEY_CART"]
    cart = session.get(key)

    if cart and seat_id in cart:
        del cart[seat_id]

    session[key] = cart
    return jsonify(utils.cart_stats(cart=cart))

#trang nhập thông tin khách hàng
@login_required
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

#thanh toán
@login_required
def pay():
    key_cart = app.config["KEY_CART"]
    cart = session[key_cart]

    total_amount = 0
    total_quantity = 0
    for c in cart.values():
        total_quantity += 1
        total_amount += c["ticket_price"]
    if request.method.__eq__("POST"):
        order_id = str(current_user.id) + str(datetime.now())
        vnpay_payment_url = vnpay.generate_payment_url(order_id=order_id, amount=total_amount)
        return jsonify({"status": "success", "redirect": vnpay_payment_url})


    return render_template("pay.html",
                           total_amount=total_amount,
                           total_quantity=total_quantity)

#kết quả thanh toán
@login_required
def payment_return():
    query_params = request.args.to_dict()
    vnp_secure_hash = query_params.pop("vnp_SecureHash", None)

    sorted_params = sorted(query_params.items())
    query_string = "&".join(f"{k}={urllib.parse.quote_plus(str(v))}" for k, v in sorted_params)
    hmac_obj = hmac.new(vnpay.VNP_HASH_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha512)
    expected_hash = hmac_obj.hexdigest()

    is_success = True

    if vnp_secure_hash == expected_hash and query_params.get("vnp_ResponseCode") == "00":
        order_id = query_params.get("vnp_TxnRef")
        amount = int(query_params.get("vnp_Amount")) // 100
        payment_method = PaymentMethod.BANKING
        cart = session[app.config["KEY_CART"]]
        passenger_infos = session[app.config["KEY_PASSENGER"]]
        dao.add_receipt(cart=cart, passenger_infos=passenger_infos, order_id=order_id, payment_method=payment_method)
        return render_template("payment_return.html", is_success=True)
    else:
        return render_template("payment_return.html", is_success=False)

#dat lich1
@login_required
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

#dat lich2
@login_required
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

# gọi.qual tới file html của thong tin tai khoan
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

# gọi tới file html của staff
def staff_page():
    return render_template('/staff/index.html')

#dang xuat staff
def staff_logout():
    session.clear()
    return redirect(url_for('staff_page'))
#=========admin========#

#trang chu admin
def admin_login():
    user_name = request.form['username']
    password = request.form['password']
    user = dao.auth_user(user_name=user_name, password=password)

    if user:
        login_user(user)
        print(current_user)
    return redirect('/admin')


def draw_monthly_chart():
    # Lấy dữ liệu JSON từ request
    data = request.json
    month = data.get("month")
    year = data.get("year")

    # Lấy dữ liệu doanh thu theo tuyến bay cho tháng đã chọn
    raw_data_by_month = dao.revenue_stats_by_month(year=year, month=month)
    raw_data_by_turn = dao.count_flights_by_route(year=year, month=month)

    # Chuyển dữ liệu thành định dạng phù hợp với Chart.js
    data_to_draw_chart_bar = [{"route_name": row.name, "total_revenue": row.total_revenue} for row in raw_data_by_month]
    data_to_draw_chart_pie = [{"route_name": row.name, "flight_count": row.flight_count} for row in raw_data_by_turn]
    print("Data for bar chart:", data_to_draw_chart_bar)
    print("Data for pie chart:", data_to_draw_chart_pie)
    # Tạo dữ liệu report dựa trên raw_data_by_month
    report_data = [
        {
            "id": idx + 1,  # Đánh số thứ tự
            "route_name": row.name,
            "total_revenue": row.total_revenue,
            "flight_count": next(
                (item.flight_count for item in raw_data_by_turn if item.name == row.name),
                0  # Mặc định là 0 nếu không tìm thấy
            )
        }
        for idx, row in enumerate(raw_data_by_month)
    ]

    # Trả về dữ liệu dưới dạng JSON với các khóa riêng biệt
    return jsonify({ "data_bar": data_to_draw_chart_bar, "data_pie": data_to_draw_chart_pie,"report_data": report_data,
    "total_flights": sum(row.flight_count for row in raw_data_by_turn) })


#trang chu staff
def staff_login():
    user_name = request.form['username']
    password = request.form['password']
    user = dao.auth_staff(user_name=user_name, password=password)

    if user:
        login_user(user)
        print(current_user)
    return redirect('/staff')



#end======admin========#

#======staff=======#







