# generate_qr.py
import qrcode

def generate_qr_code(uri, filename="totp_qrcode.png"):
    """
    Generate a QR code from the URI and save it as an image file.
    """
    qr = qrcode.QRCode(
        version=1,  # Size of the QR code
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level
        box_size=10,  # Size of each box
        border=4,  # Border size
    )
    qr.add_data(uri)  # Add the URI data
    qr.make(fit=True)  # Fit the QR code to the data

    # Save the QR code as an image file
    img = qr.make_image(fill='black', back_color='white')
    img.save(filename)
    print(f"QR code saved as {filename}")
