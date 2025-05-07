# allsafe-otp

## Project Overview

`allsafe-otp` is a simple Python package for generating Time-Based One-Time Passwords (TOTP) and QR codes for two-factor authentication (2FA). It allows you to easily create secure OTPs and generate QR codes that can be scanned with Google Authenticator or other 2FA apps.

## Features

* Generate secure TOTP codes using the HMAC-SHA1 algorithm.
* Create scannable QR codes for Google Authenticator or any 2FA app.
* Easy to integrate into your Python projects.

## Installation

```bash
pip install allsafe-otp
```

## Usage

### 1. Generate a TOTP Code

```python
from allsafe_otp.totp import generate_otp

secret = "JBSWY3DPEHPK3PXP"  # Your base32 secret
otp = generate_otp(secret)
print(f"Generated OTP: {otp}")
```

### 2. Generate a QR Code for Google Authenticator

```python
from allsafe_otp.generate_qr import generate_qr_code

otp_url = "otpauth://totp/MyApp:daniel@allsafe.com?secret=JBSWY3DPEHPK3PXP&issuer=MyApp"
generate_qr_code(otp_url)
```

## Testing

To test the package:

1. Install the package (if not already installed):

```bash
pip install allsafe-otp
```

2. Create a test script (`test.py`):

```python
from allsafe_otp.totp import generate_otp
from allsafe_otp.generate_qr import generate_qr_code

secret = "JBSWY3DPEHPK3PXP"
print("Generated OTP from Python:", generate_otp(secret))

otp_url = "otpauth://totp/MyApp:daniel@allsafe.com?secret=JBSWY3DPEHPK3PXP&issuer=MyApp"
generate_qr_code(otp_url)
```

## Project Structure

```
allsafe-otp/
├── allsafe_otp/
│   ├── __init__.py
│   ├── generate_qr.py
│   └── totp.py
├── setup.py
└── README.md
```

## Contributing

Feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
