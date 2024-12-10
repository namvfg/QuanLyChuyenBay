import math
from flask_login import login_user,current_user, logout_user
from flask import render_template, request, jsonify, session
from flask import request, redirect, render_template
from app import app, db, dao

#trang chu
def index():
    reviews = dao.load_reviews()
    notifications = dao.load_notifications()
    return render_template("index.html", reviews=reviews, notifications=notifications)

#dang nhap
def login_my_user():
    if request.method.__eq__("POST"):
        user_name = request.form["user_name"]
        password = request.form["password"]
        user = dao.auth_customer(user_name.strip(), password)
        if user:
            login_user(user=user)
            next = request.args.get("next")
            return redirect(next if next else "/")
        else:
            return redirect("/")
    return render_template("login.html")

#dang nhap
def register():
    return render_template("register.html")

#dang xuat
def logout_my_user():
    logout_user()
    return redirect("/login")

#trang chu admin
def admin_login():
    user_name = request.form['username']
    password = request.form['password']

    user = dao.auth_user(user_name=user_name, password=password)
    if user:
        login_user(user)
        print(current_user)
    return redirect('/admin')

