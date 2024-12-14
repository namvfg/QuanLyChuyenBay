import json

from flask import request, redirect, render_template,jsonify
from flask_login import login_user
from app import app, controller, login, dao,admin,db
from app.dao import load_airplane, load_airport, load_route
from app.models import User, Customer, SubFlight, Airplane

# load trang chủ
app.add_url_rule("/", "index", controller.index, methods=["GET", "POST"])


# gọi tới file html của staff
@app.route('/staff')
def staff_page():
    return render_template('staff/index.html')

@app.route('/staff/scheduling')
def staff_scheduling():
    airplane_info = load_airplane()
    airport_info = load_airport()
    route_info = load_route()
    return render_template('staff/scheduling.html',airplane_info = airplane_info,airport_info = airport_info,route_info = route_info)

#load trang đăng nhập
app.add_url_rule("/login", "login", controller.login_my_user, methods=["POST", "GET"])

#load trang đăng ký
app.add_url_rule("/register", "register", controller.register, methods=["POST", "GET"])

#load trang nhập mã xác nhận
app.add_url_rule("/api/verify_code", "verify_code", controller.type_verify_code, methods=["POST"])

#log out
app.add_url_rule("/logout", "logout", controller.logout_my_user)

#tìm user theo user_id
@login.user_loader
def load_user(id):
    #nếu là customer
    if dao.get_customer_by_id(id):
        return dao.get_customer_by_id(id)
    else:
    # nếu là user
        return dao.get_user_by_id(id)

#load trang kết quả tìm kiếm
app.add_url_rule("/search_result", "search_result", controller.search_result, methods=["GET", "POST"])

#load trang đặt vé
app.add_url_rule("/booking", "booking", controller.booking, methods=["GET", "POST"])

#load trang chu admin
app.add_url_rule("/login-admin", "login_admin", controller.admin_login, methods=['POST'])




if __name__ == "__main__":
    app.run(debug=True)



