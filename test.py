from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64

ciphertext_b64 = "mzwKJbLbZsD3ptw+OSgAe0EkMK7uVDAmEDlgllfr9zE="
cipher_bytes = base64.b64decode(ciphertext_b64)

iv = cipher_bytes[:16]
ciphertext = cipher_bytes[16:]

key = "nhập_khóa_ở_đây"  # <- Thử thay bằng các khóa 16 ký tự
cipher = AES.new(key, AES.MODE_CBC, iv)

try:
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size).decode()
    print("✅ Kết quả giải mã:", plaintext)
except Exception as e:
    print("❌ Sai khóa:", e)
