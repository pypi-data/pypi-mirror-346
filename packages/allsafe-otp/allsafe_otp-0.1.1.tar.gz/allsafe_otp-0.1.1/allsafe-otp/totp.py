# totp.py
import hmac
import hashlib
import time
import base64
import struct
from generate_qr import generate_qr_code  # Import the QR code generation function

# Step 1: Define your TOTP secret, account, and issuer
secret = "JBSWY3DPEHPK3PXP"  # Your base32 secret (change this for each user)
account_name = "daniel@allsafe.com"  # Your account name
issuer = "MyApp"  # Issuer name, e.g., the app or service name

# Step 2: Generate OTP using the TOTP algorithm (HMAC-SHA1)
def generate_otp(secret):
    # Decode the base32 secret
    key = base64.b32decode(secret.upper())
    # Time step is typically 30 seconds
    time_step = 30
    # Current timestamp in seconds
    timestamp = int(time.time() / time_step)
    # Convert timestamp into bytes
    msg = struct.pack(">Q", timestamp)
    
    # HMAC-SHA1 generation
    hmac_result = hmac.new(key, msg, hashlib.sha1).digest()
    
    # Dynamic truncation: extract 4 bytes and apply modulo to get a 6-digit code
    offset = hmac_result[19] & 0xf
    otp = struct.unpack(">I", hmac_result[offset:offset+4])[0] & 0x7fffffff
    otp = otp % 1000000  # Ensure OTP is 6 digits
    return otp

# Generate OTP from the secret
otp = generate_otp(secret)
print(f"Generated OTP from Python: {otp}")

# Step 3: Generate the provisioning URI (URL) for Google Authenticator
otp_url = f"otpauth://totp/{issuer}:{account_name}?secret={secret}&issuer={issuer}"
print(f"Provisioning URI: {otp_url}")

# Step 4: Generate the QR Code for the provisioning URI
generate_qr_code(otp_url)  # This will save the QR code as a PNG image
