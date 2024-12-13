import smtplib
import requests

from app import app

#send mail xác thực
def send_authenticate_mail(email_target, subject, body):
    email = app.config["EMAIL"]
    password = app.config["PASSWORD_EMAIL"]

    mail_session = smtplib.SMTP('smtp.gmail.com', 587)
    mail_session.starttls() #bảo mật
    mail_session.login(email, password)
    try:
        #Nội dung
        mail_content = f"Subject: {subject}\n\n{body}"
        mail_session.sendmail(email, email_target, mail_content)
        print("Email sent successfully!")

    except smtplib.SMTPRecipientsRefused as e:
        print(f"Recipient refused: {e.recipients}")
    except smtplib.SMTPResponseException as e:
        print(f"SMTP error: {e.smtp_code} - {e.smtp_error.decode()}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        mail_session.quit()

#verify email
def verify_email(email_target):
    api_key = app.config["KEY_HUNTER.IO"]
    url = f"https://api.hunter.io/v2/email-verifier?email={email_target}&api_key={api_key}"
    try:
        api_response = requests.get(url)
        api_response.raise_for_status() #kiểm tra lỗi http
        data = api_response.json()
        return {
            "status": data["data"]["status"]
            # valid: Email hợp lệ, có thể sử dụng
            # invalid: Email không hợp lệ (không tồn tại hoặc không thể nhận email).
            # webmail: Email sử dụng dịch vụ email công cộng (như Gmail, Yahoo).
            # unknown: Không thể xác định trạng thái email (do nhà cung cấp không phản hồi hoặc lỗi khác).
        }
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    with app.app_context():
        result = verify_email("2251052022dun@ou.edu.vn")
        if result["status"] == "valid":
            print("email có thể dùng được")
        else:
            print("hên xui")