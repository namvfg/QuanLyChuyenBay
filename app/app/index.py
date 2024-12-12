import json
from flask import request, redirect, render_template,jsonify
from flask_login import login_user
from app import app, controller, login, dao,admin,db
from app.models import User,Customer,SubFlight

# load trang chủ
app.add_url_rule("/", "index", controller.index)


# gọi tới file html của staff
@app.route('/staff')
def staff_page():
    return render_template('staff/index.html')

@app.route('/staff/scheduling')
def staff_scheduling():
    return render_template('staff/scheduling.html')

#load trang đăng nhập
app.add_url_rule("/login", "login", controller.login_my_user, methods=["POST", "GET"])

#load trang đăng ký
app.add_url_rule("/register", "register", controller.register, methods=["POST", "GET"])

#load out
app.add_url_rule("/logout", "logout", controller.logout_my_user)

#tìm user theo user_id
@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)

# @login.user_loader
# def load_user(customer_id):
#     # Tìm Customer trong cơ sở dữ liệu
#     return dao.get_customer_by_id(customer_id)

#load trang chu admin
app.add_url_rule("/login-admin", "login_admin", controller.admin_login, methods=['post'])


if __name__ == "__main__":
    app.run(debug=True)



