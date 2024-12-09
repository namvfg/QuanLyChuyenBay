import hashlib
from app.models import User, Ticket, Passenger, TicketPrice
from app.models import Review,db

#xác thực người dùng
def auth_user(user_name,password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).digest())

    return User.query.filter(User.user_name.__eq__(user_name.strip()),
                             User.password.__eq__(password)).first()

#lấy thông tin người dùng
def get_user_by_id(user_id):
    return User.query.get(user_id)

#lấy thông tin vé đếm
def count_tickets():
    return Ticket.query.count()

def get_total_revenue():
    # Giả sử có cột price trong Ticket hoặc tính toán giá vé tổng
    return db.session.query(db.func.sum(TicketPrice.price)).scalar()

#lấy thông tin khách đếm
def count_passengers():
    return Passenger.query.count()

#đọc lấy review từ bảng review
def load_reviews():
    return Review.query
