from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager
import cloudinary


app = Flask(__name__)
app.secret_key = "hkjgjjgfdjgoidu0iwuiregjgojp753498574357*(^&*^*&%&^"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/mydb?charset=utf8mb4" %quote("Admin@123")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

#số notification trên 1 trang ở file index.html
app.config["PAGE_SIZE_NOTIFICATION"] = 4

#độ dài số điện thoại
app.config["PHONE_NUMBER_LENGTH"] = 10

#độ dài mật khẩu tối thiểu
app.config["PASSWORD_LENGTH"] = 6

cloudinary.config(cloud_name="dnpodiilj",
                  api_key="874131819545712",
                  api_secret="xHDsHPIIbwKkoT6qfPYTAvn4pmA")

db = SQLAlchemy(app=app)

login = LoginManager(app=app)

