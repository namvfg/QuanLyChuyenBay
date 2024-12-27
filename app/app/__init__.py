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

#số kết quả trong 1 trang tìm kiếm
app.config["PAGE_SIZE"] = 2

#key cho session chứa email_target và verify_code
app.config["KEY_VERIFY_EMAIL"] = "verify_email"

#key cho session để lập lịch chuyến bay
app.config["KEY_SCHEDULING"] = "scheduling"

#key để đặt vé
app.config["KEY_CART"] = "cart"

#key để lưu flight_id
app.config["FLIGHT_ID"] = "flight_id"

#key để lưu customer_id
app.config["CUSTOMER_ID"] = "customer_id"

#key để lưu thông tin hành khách
app.config["KEY_PASSENGER"] = "passenger"

#email để gửi mail xác nhận
app.config["EMAIL"] = "duakhongchau1234@gmail.com"
#password 2 lớp
app.config["PASSWORD_EMAIL"] = "prnksqarnigvvjkq"
#key cho api hunter.io
app.config["KEY_HUNTER.IO"] = "32b4507da8872ff43ad7ef9122de8bee777c1db5"

#số lượng sân bay trung gian tối đa
app.config["MAX_INTERMEDIATE_AIRPORT_QUANTITY"] = 2

cloudinary.config(cloud_name="dnpodiilj",
                  api_key="874131819545712",
                  api_secret="xHDsHPIIbwKkoT6qfPYTAvn4pmA")


#====qui định======

#thời gian bay tối thiểu
app.config["MIN_FLYING_DURATION"] = "min_flying_duration"

#thời gian chờ tối thiểu
app.config["MIN_WAITING_DURATION"] = "min_waiting_duration"

#thời gian chờ tối đa
app.config["MAX_WAITING_DURATION"] = "max_waiting_duration"

#số lượng số lượng sân bay trung gian tối đa
app.config["MAX_INTERMEDIATE_AIRPORT"] = "max_intermediate_airport"

#thời gian bán vé
app.config["TIME_TO_SELLING"] = "time_to_selling"

#thời gian đặt vé
app.config["TIME_TO_BOOKING"] = "time_to_booking"


db = SQLAlchemy(app=app)

login = LoginManager(app=app)

