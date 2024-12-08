
from flask import request, redirect, render_template
from flask_login import login_user,current_user
from app import app, controller, login, dao
from app import admin

# load trang chu
app.add_url_rule("/", "index", controller.index)


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


@app.route('/login-admin', methods=['post'])
def admin_login():
    user_name = request.form['username']
    password = request.form['password']

    user = dao.auth_user(user_name=user_name, password=password)
    if user:
        login_user(user)
    return redirect('/admin')

if __name__ == "__main__":
    app.run(debug=True)
