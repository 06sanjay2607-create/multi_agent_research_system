import os
import random
import resend

resend.api_key = os.getenv("RESEND_API_KEY")

otp_storage = {}


def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp(email):

    otp = generate_otp()

    otp_storage[email] = otp

    resend.Emails.send({
        "from": "onboarding@resend.dev",
        "to": email,
        "subject": "Your OTP - AI Research Assistant",
        "html": f"""
        <h2>AI Research Assistant</h2>

        <p>Your verification OTP is:</p>

        <h1>{otp}</h1>

        <p>Please enter this OTP to complete your registration.</p>
        """
    })

    return True


def verify_otp(email, entered_otp):

    return otp_storage.get(email) == entered_otp