from app.models import Review


#đọc lấy review từ bảng review
def load_reviews():
    return Review.query