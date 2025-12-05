import qrcode
import sys

# The Expo URL for your local network
# Format: exp://<IP_ADDRESS>:8081
expo_url = "exp://192.168.0.134:8081"

# Generate QR Code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(expo_url)
qr.make(fit=True)

# Create an image from the QR Code instance
img = qr.make_image(fill_color="black", back_color="white")

# Save it to the artifacts directory (or desktop for visibility)
output_path = "expo_qr_code.png"
img.save(output_path)
print(f"QR code generated at {output_path}")
