from app import app
import hashlib
import hmac
import datetime
import urllib.parse
from flask import request

# Cấu hình VNPAY
VNP_TMN_CODE = "C0BGWBNK"  # Mã website tích hợp (do VNPAY cấp)
VNP_HASH_SECRET = "KW06TMWD7PXSRZ3UW8RWTHOYCO48181B"  # Chuỗi bí mật (do VNPAY cấp)
VNP_URL = "https://sandbox.vnpayment.vn/paymentv2/vpcpay.html"  # URL sandbox
VNP_RETURN_URL = "http://127.0.0.1:5000/payment_return"  # URL nhận callback

def generate_payment_url(order_id, amount):
    vnp_IpAddr = request.remote_addr  # Lấy IP thực của người dùng
    params = {
        "vnp_Version": "2.1.0",
        "vnp_Command": "pay",
        "vnp_TmnCode": VNP_TMN_CODE,
        "vnp_Amount": amount * 100,
        "vnp_CreateDate": datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
        "vnp_CurrCode": "VND",
        "vnp_IpAddr": vnp_IpAddr,
        "vnp_Locale": "vn",
        "vnp_OrderInfo": f"Thanh toan don hang {order_id}",
        "vnp_OrderType": "billpayment",
        "vnp_ReturnUrl": VNP_RETURN_URL,
        "vnp_TxnRef": order_id,
    }

    sorted_params = sorted(params.items())
    query_string = "&".join(f"{k}={urllib.parse.quote_plus(str(v))}" for k, v in sorted_params)

    hmac_obj = hmac.new(VNP_HASH_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha512)
    signature = hmac_obj.hexdigest()

    return f"{VNP_URL}?{query_string}&vnp_SecureHash={signature}"