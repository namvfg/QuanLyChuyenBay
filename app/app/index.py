
from flask import request, redirect, render_template
from flask_login import login_user
from app import app, controller, login, dao,admin


# load trang chu
app.add_url_rule("/", "index", controller.index)

# gọi tới file html của staff
@app.route('/staff')
def staff_page():
    return render_template('staff/index.html')

@app.route('/staff/scheduling')
def staff_scheduling():
    return render_template('staff/scheduling.html')

#tìm user theo user_id
@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


#đăng nhập admin
@app.route('/login-admin', methods=['post'])
def admin_login():
    user_name = request.form['username']
    password = request.form['password']
    user = dao.auth_user(user_name=user_name, password=password)
    if user:
        login_user(user=user)
        return redirect('/admin')

if __name__ == "__main__":
    app.run(debug=True)



