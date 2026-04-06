import streamlit as st
import smtplib
from email.mime.text import MIMEText
import random

# ------------------- SEND OTP FUNCTION -------------------
def send_otp(receiver_email):
    otp = str(random.randint(100000, 999999))

    sender_email = "your_email@gmail.com"
    password = "your_app_password"   # Use Gmail App Password

    msg = MIMEText(f"Your OTP is {otp}")
    msg['Subject'] = "OTP Verification"
    msg['From'] = sender_email
    msg['To'] = receiver_email

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        st.error("Error sending email: " + str(e))

    return otp

# ------------------- UI -------------------
st.title("🔐 Two-Factor Authentication (2FA)")

# Step 1: Email input
email = st.text_input("Enter your Email")

# Step 2: Send OTP
if st.button("Send OTP"):
    if email:
        otp = send_otp(email)
        st.session_state['otp'] = otp
        st.success("✅ OTP sent to your email!")
    else:
        st.warning("⚠️ Please enter email")

# Step 3: Enter OTP
user_otp = st.text_input("Enter OTP")

# Step 4: Verify OTP
if st.button("Verify OTP"):
    if 'otp' in st.session_state:
        if user_otp == st.session_state['otp']:
            st.success("🎉 Login Successful!")
            st.subheader("📊 Dashboard")
            st.write("Welcome! You are securely logged in using 2FA.")
        else:
            st.error("❌ Invalid OTP")
    else:
        st.warning("⚠️ Please generate OTP first")