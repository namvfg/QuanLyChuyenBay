from functools import wraps
from app import dao
from app.models import StaffRole
from flask import redirect
from flask_login import current_user, logout_user

def anonymous_customer(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_func

def anonymous_staff(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect("/staff")
        return f(*args, **kwargs)
    return decorated_func

def anonymous_admin(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect("/admin")
        return f(*args, **kwargs)
    return decorated_func

def is_customer(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if current_user.is_authenticated and not dao.get_customer_by_id(current_user.id):
            logout_user()
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_func

def is_staff(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if current_user.is_authenticated and not dao.get_staff_by_id(current_user.id):
            logout_user()
            print("dang xuat")
            return redirect("/staff")
        return f(*args, **kwargs)
    return decorated_func

def is_admin(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if current_user.is_authenticated and not dao.get_admin_by_id(current_user.id):
            logout_user()
            return redirect("/admin")
        return f(*args, **kwargs)
    return decorated_func

def for_staff_seller(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if current_user.is_authenticated and not current_user.staff_role.__eq__(StaffRole.SELLER):
            return redirect("/staff")
        return f(*args, **kwargs)
    return decorated_func

def for_staff_planner(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if current_user.is_authenticated and not current_user.staff_role.__eq__(StaffRole.PLANNER):
            return redirect("/staff")
        return f(*args, **kwargs)
    return decorated_func