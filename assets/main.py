from js import document, window
from pyodide.ffi import create_proxy, to_js
import qrcode
from io import BytesIO
import base64

# Store the current QR code data
current_qr_data = None
current_filename = "qr_code.png"

def generate_qr(event=None):
    global current_qr_data, current_filename
    try:
        url = document.getElementById("urlInput").value.strip()

        if not url:
            print("Please enter a URL")
            return

        # Use default filename
        current_filename = "qr_code.png"

        print(f"Generating QR code for: {url}")
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        buffer = BytesIO()
        img.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode()
        current_qr_data = img_str

        qr_image = document.getElementById("qrImage")
        qr_image.src = "data:image/png;base64," + img_str
        
        # Enable download button
        download_btn = document.getElementById("downloadBtn")
        download_btn.disabled = False
        
        print("QR code generated successfully!")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

def download_qr(event=None):
    global current_qr_data, current_filename
    try:
        if not current_qr_data:
            print("No QR code to download. Please generate one first.")
            return

        # Create a temporary anchor element and trigger download
        link = document.createElement("a")
        link.href = "data:image/png;base64," + current_qr_data
        link.download = current_filename
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        print(f"Downloaded {current_filename}")
    except Exception as e:
        print(f"Download error: {e}")
        import traceback
        traceback.print_exc()

# Expose functions to window for direct access
generate_proxy = create_proxy(generate_qr)
download_proxy = create_proxy(download_qr)
window.generateQR = generate_proxy
window.downloadQR = download_proxy

# Attach event listeners
def attach_listeners():
    try:
        generate_btn = document.getElementById("generateBtn")
        download_btn = document.getElementById("downloadBtn")
        
        if generate_btn:
            generate_btn.addEventListener("click", generate_proxy)
        if download_btn:
            download_btn.addEventListener("click", download_proxy)
        
        if generate_btn or download_btn:
            print("Event listeners attached!")
            return True
    except Exception as e:
        print(f"Error attaching listeners: {e}")
    return False

# Try attaching immediately and also set up a fallback
if not attach_listeners():
    def retry_attach():
        if attach_listeners():
            return
        window.setTimeout(retry_attach, 100)
    window.setTimeout(retry_attach, 200)

