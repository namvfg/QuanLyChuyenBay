import math

from flask import render_template
from app import app, db, dao

#trang chu
def index():
    return render_template("index.html")