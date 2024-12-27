import re
from app import mail

def cart_stats(cart):
    total_amount = 0
    total_quantity = 0
    chosen_seats = ""
    chosen_id_seats = []
    if cart:
        for c in cart.values():
            total_quantity += 1
            total_amount += c["ticket_price"]
            chosen_seats += c["seat_name"] + " "
            chosen_id_seats.append(c["seat_id"])

    return {
        "status": "success",
        "total_amount": total_amount,
        "total_quantity": total_quantity,
        "chosen_seats": chosen_seats,
        "chosen_id_seats": chosen_id_seats
    }

def verify_email(email):
    valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)
    status = mail.verify_email(email)["status"]
    if not valid or (status != "valid" and status != "webmail" and status != "accept_all"):
        return False
    else:
        return True

def parse_to_valid_file_name(order_id):
    order_id = order_id.replace(".", "d")
    order_id = order_id.replace(":", "-")
    order_id = order_id.replace(" ", "_")
    return order_id