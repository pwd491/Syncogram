import base64
import qrcode
from io import BytesIO


def generate_qrcode(url):
    qr = qrcode.make(url)
    buffered = BytesIO()
    # SAVE IMAGE QRCODE TO JPEG OR WHATEVER
    qr.save(buffered,format="JPEG")
    s1 = base64.b64encode(buffered.getvalue())
    return s1.decode("utf-8")