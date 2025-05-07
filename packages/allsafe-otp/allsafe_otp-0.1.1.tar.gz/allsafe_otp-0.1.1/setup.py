from setuptools import setup, find_packages
import os  # You forgot this

setup(
    name="allsafe_otp",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "qrcode",
        "Pillow",  # Needed by qrcode to handle image saving
    ],
    author="Daniel Destaw",
    author_email="daniel@allsafe.com",
    description="A simple TOTP + QR code generator package for 2FA",
    long_description=open("README.md").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
