import math
import re
from datetime import datetime
from re import search

from flask_login import login_user,current_user, logout_user
from flask import render_template, request, jsonify, session, url_for, flash
from flask import request, redirect, render_template
from app import app, db, dao
from app.decorators import annonymous_user
import cloudinary.uploader

#trang chủ
def index():
    # if request.method.__eq__("POST"):
    #     start_point = request.form["start_point"]
    #     end_point = request.form["end_point"]
    #     flight_date = request.form["flight_date"]
    #     query = {
    #         "start_point": start_point,
    #         "end_point": end_point,
    #         "flight_date": flight_date
    #     }
    #     print(query)
    #     return redirect(url_for("search_result", **query))
    reviews = dao.load_reviews()
    notifications = dao.load_notifications()
    return render_template("index.html", reviews=reviews, notifications=notifications)

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
        if not valid:
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
            flash("Tạo tài khoản thành công.", "success")
            return jsonify({"status": "success", "redirect": "/login"})
        except Exception as e:
            flash(f"Lỗi không xác định: {str(e)}", "error")
            return jsonify({"status": "error", "message": {str(e)}})
    return render_template("register.html")


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



