import random

def generate_otp():
    """Generate a 6-digit OTP code."""
    return f"{random.randint(100000, 999999)}"

