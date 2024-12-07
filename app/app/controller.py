import math

from flask import render_template
from app import app, db, dao

#trang chu
def index():
    reviews = dao.load_reviews()
    return render_template("index.html", reviews=reviews)