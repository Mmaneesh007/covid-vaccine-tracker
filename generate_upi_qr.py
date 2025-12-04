import qrcode

# UPI payment URL
upi_id = "manish7044436272@okaxis"
name = "Manish Sau"
upi_url = f"upi://pay?pa={upi_id}&pn={name}&cu=INR"

# Generate QR code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(upi_url)
qr.make(fit=True)

# Create QR code image
img = qr.make_image(fill_color="black", back_color="white")

# Save to assets directory
img.save("assets/upi_qr.png")
print("UPI QR Code generated successfully at assets/upi_qr.png")
