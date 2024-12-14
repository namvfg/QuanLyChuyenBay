import math
import re
from datetime import datetime
from re import search
from app import mail
from flask_login import login_user,current_user, logout_user
from flask import render_template, request, jsonify, session, url_for, flash
from flask import request, redirect, render_template
from app import app, db, dao
from app.dao import load_popular_routes
from app.decorators import annonymous_user
import cloudinary.uploader


#trang chủ
def index():
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
            return jsonify({"status": "success", "redirect": "/"})
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
        valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)
        if not valid or not mail.verify_email(email)["status"].__eq__("valid"):
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

        key = app.config["VERIFY_EMAIL"]
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
    key = app.config["VERIFY_EMAIL"]
    data = request.json
    session[key] = data
    email_target = data["email_target"]
    verify_code = data["verify_code"]
    print(verify_code)
    valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email_target)
    if not valid or not mail.verify_email(email_target)["status"].__eq__("valid"):
        return jsonify({"status": "error", "message": "Email không hợp lệ"})
    else:
        mail.send_authenticate_mail(email_target, subject="Verify Code", body=str(verify_code))
        return jsonify({"status": "success", "message": "Gửi mã thành công. Bạn có thể ấn vào nút Đổi thông tin để nhập lại"})

#xóa mã xác nhận
def clear_verify_code():
    key = app.config["VERIFY_EMAIL"]
    session[key] = {}
    return jsonify({"status": "success", "message": "Mã xác nhận đã xóa, bạn có thể nhập lại thông tin"})

#dang xuat
def logout_my_user():
    logout_user()
    return redirect("/login")

#kết quả tìm kiếm
def search_result():
    start_point = request.args.get("start_point")
    end_point = request.args.get("end_point")
    flight_date = request.args.get("flight_date")
    if flight_date:
        flight_date = datetime.strptime(flight_date, "%Y-%m-%d")
    print(type(flight_date))
    return render_template("search_result.html", start_point=start_point, end_point=end_point, flight_date=flight_date)

#trang đặt vé
def booking():
    return render_template("booking.html")

#trang chu admin
def admin_login():
    user_name = request.form['username']
    password = request.form['password']
    user = dao.auth_user(user_name=user_name, password=password)

    if user:
        login_user(user)
        print(current_user)
    return redirect('/admin')






