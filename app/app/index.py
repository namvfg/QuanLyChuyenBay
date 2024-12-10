
from flask import request, redirect, render_template
from flask_login import login_user,current_user
from app import app, controller, login, dao
from app import admin

# load trang chủ
app.add_url_rule("/", "index", controller.index)

#load trang đăng nhập
app.add_url_rule("/login", "login", controller.login_my_user, methods=["POST", "GET"])

#load trang đăng ký
app.add_url_rule("/register", "register", controller.register, methods=["POST", "GET"])

# #api đăng ký
# app.add_url_rule("/api/validate_register", "validate_register", controller.validate_register, methods=[ "POST"])

#load out
app.add_url_rule("/logout", "logout", controller.logout_my_user)

@login.user_loader
def load_user(id):
    #nếu là customer
    if dao.get_customer_by_id(id):
        return dao.get_customer_by_id(id)
    else:
    # nếu là user
        return dao.get_user_by_id(id)



#load trang chu admin
app.add_url_rule("/login-admin", "login_admin", controller.admin_login, methods=['post'])



#notification


if __name__ == "__main__":
    app.run(debug=True)
