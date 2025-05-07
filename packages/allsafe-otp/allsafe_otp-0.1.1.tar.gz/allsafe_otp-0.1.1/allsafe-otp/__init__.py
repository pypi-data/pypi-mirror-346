# allsafe_otp/__init__.py

from .totp import generate_otp
from .generate_qr import generate_qr_code

__all__ = ["generate_otp", "generate_qr_code"]
