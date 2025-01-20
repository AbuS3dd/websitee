import random
import string
from flask import Flask, request, jsonify
import re
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# قائمة أكواد التفعيل العشوائية
activation_codes = [''.join(random.choices(string.ascii_letters + string.digits, k=8)) for _ in range(5)]

# التحقق من صحة البريد الإلكتروني
def is_valid_email(email):
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email)

# إرسال رسالة تحقق إلى البريد الإلكتروني
def send_verification_email(email):
    sender_email = "your_email@example.com"  # بريدك الإلكتروني
    sender_password = "your_password"       # كلمة مرور بريدك الإلكتروني
    subject = "Email Verification"
    body = "Your email has been verified successfully."

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, msg.as_string())
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    activation_code = data.get("activationCode")

    if activation_code not in activation_codes:
        return jsonify({"message": "Invalid activation code."}), 400

    if not is_valid_email(email):
        return jsonify({"message": "Invalid email address."}), 400

    if send_verification_email(email):
        return jsonify({"message": "Account created successfully. Verification email sent."}), 200
    else:
        return jsonify({"message": "Failed to send verification email."}), 500

if __name__ == "__main__":
    print("Allowed activation codes:", activation_codes)
    app.run(debug=True)
import random
import string
from flask import Flask, jsonify

app = Flask(__name__)

# توليد الأكواد العشوائية
activation_codes = ['12'.join(random.choices(string.ascii_letters + string.digits, k=8)) for _ in range(5)]

@app.route('/activation-codes', methods=['GET'])
def get_activation_codes():
    # إرجاع الأكواد في صيغة JSON
    return jsonify({"activation_codes": activation_codes})

if __name__ == "__main__":
    print("Allowed activation codes:", activation_codes)
    app.run(debug=True)
from flask import Flask, jsonify, request
import random
import string

app = Flask(__name__)

# قائمة الأكواد العشوائية
activation_codes = [''.join(random.choices(string.ascii_letters + string.digits, k=8)) for _ in range(5)]

# مسار لإرجاع الأكواد
@app.route('/activation-codes', methods=['GET'])
def get_activation_codes():
    return jsonify({"activation_codes": activation_codes})

# مسار للتحقق من الأكواد
@app.route('/verify-code', methods=['POST'])
def verify_code():
    data = request.json  # استقبال البيانات
    user_code = data.get("code")  # الحصول على الرمز
    
    # التحقق من الرمز
    if user_code in activation_codes:
        return jsonify({"status": "success", "message": "Activation code is valid!"})
    else:
        return jsonify({"status": "failure", "message": "Invalid activation code."}), 400

# تشغيل التطبيق
if __name__ == "__main__":
    print("Allowed activation codes:", activation_codes)
    app.run(debug=True)
