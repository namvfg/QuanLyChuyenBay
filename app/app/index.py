import json

from flask import request, redirect, render_template, jsonify, session
from flask_login import login_user, current_user
from datetime import datetime, timedelta
import hashlib
from app import app, controller, login, dao, admin, db
from app.dao import add_ticket_price
from app.models import User, Customer, SubFlight, Airplane


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

# gọi.qual tới file html của thong tin tai khoan
app.add_url_rule("/info_page", "info_page", controller.info_page, methods=["POST", "GET"])

#api thêm vé
app.add_url_rule("/api/cart", "add_seat", controller.add_seat, methods=["POST"])

#api xóa vé
app.add_url_rule("/api/cart/<seat_id>", "api_cart_seatId_delete", controller.delete_seat, methods=["DELETE"])

#log out
app.add_url_rule("/logout", "logout", controller.logout_my_user)

#load trang kết quả tìm kiếm
app.add_url_rule("/search_result", "search_result", controller.search_result, methods=["GET"])

#load trang đặt vé
app.add_url_rule("/booking/<int:flight_id>", "booking", controller.booking, methods=["GET"])

#load trang nhập thông tin hành khách
app.add_url_rule("/passenger_information", "passenger_information", controller.passenger_information, methods=["GET", "POST"])

#load trang thanh toán
app.add_url_rule("/pay", "pay", controller.pay, methods=["GET", "POST"])

#load trang kết quả thanh toán
app.add_url_rule("/payment_return", "payment_return", controller.payment_return, methods=["GET", "POST"])


#==========staff=========#
# gọi tới file html của staff
app.add_url_rule("/staff", "staff", controller.staff_page, methods=["POST", "GET"])

#load trang chu staff
app.add_url_rule("/login-staff", "login_staff", controller.staff_login, methods=['POST', 'GET'])

#dat lich1
app.add_url_rule("/staff/scheduling1", "scheduling1", controller.staff_scheduling1, methods=["POST", "GET"])

#dat lich2
app.add_url_rule("/staff/scheduling2", "scheduling2", controller.staff_scheduling2, methods=["POST", "GET"])

#ket qua tim kiem
app.add_url_rule("/staff/search_result_staff", "search_result_staff", controller.search_result_staff, methods=["GET"])

#ban ve
app.add_url_rule("/staff/selling/<int:flight_id>", "selling", controller.staff_selling, methods=["GET"])

#nhap thong tin hanh khach
app.add_url_rule("/staff/passenger_information", "passenger_information_staff", controller.passenger_information_staff, methods=["GET", "POST"])

#nhập thông tin khách hàng
app.add_url_rule("/staff/customer_information", "customer_information_staff", controller.customer_information, methods=["GET", "POST"])

#api check số điện thoại
app.add_url_rule("/api/check_phone_number", "api_check_phone_number", controller.check_phone_number, methods=["POST"])

#trang thanh toán
app.add_url_rule("/staff/pay", "staff_pay", controller.pay_staff, methods=["GET", "POST"])

#load trang kết quả thanh toán
app.add_url_rule("/staff/payment_return", "payment_return_staff", controller.payment_return_staff, methods=["GET", "POST"])

#load trang xuất vé
app.add_url_rule("/staff/export_ticket", "export_ticket_staff", controller.export_ticket, methods=["GET", "POST"])

#end=======staff=========#


#load trang chu admin
app.add_url_rule("/login-admin", "login_admin", controller.admin_login, methods=['POST', 'GET'])



#tìm user theo user_id
@login.user_loader
def load_user(id):
    #nếu là customer
    if dao.get_customer_by_id(id):
        return dao.get_customer_by_id(id)
    #nếu là staff
    elif dao.get_staff_by_id(id):
        return dao.get_staff_by_id(id)
    #nếu là admin
    elif dao.get_admin_by_id(id):
        return dao.get_admin_by_id(id)
    else:
    # nếu là user
        return dao.get_user_by_id(id)


if __name__ == "__main__":
    app.run(debug=True)



