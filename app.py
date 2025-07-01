from flask import Flask, render_template, request, redirect, url_for, session
import unicodedata
import os
from crypto.caesar import caesar_decrypt
from crypto.vigenere import vigenere_decrypt, vigenere_encrypt
from crypto.rsa import rsa_decrypt
from crypto.aes import aes_decrypt
from Crypto.Util.Padding import unpad
from Crypto.Cipher import AES
import base64

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Trang bắt đầu nhập tên
@app.route('/', methods=['GET', 'POST'])
def index():
    session.clear()  # ✅ reset
    if request.method == 'POST':
        name = request.form.get('player_name')
        if name:
            session['player_name'] = name
            session['score'] = 0
            return redirect(url_for('level1'))
    return render_template('index.html')


# ---------- LEVEL 1: Caesar Cipher ----------
LEVEL1_CIPHER = "Wklv lv d whvw"
LEVEL1_PLAINTEXT = "This is a test"

@app.route('/level1', methods=['GET', 'POST'])
def level1():
    error = None
    result = None
    is_correct = False

    if request.method == 'POST':
        shift = request.form.get('shift')
        if not shift:
            error = "⚠️ Bạn chưa nhập số dịch chuyển."
        else:
            try:
                shift = int(shift)
                result = caesar_decrypt(LEVEL1_CIPHER, shift)
                if result.lower() == LEVEL1_PLAINTEXT.lower():
                    is_correct = True
                    session['score'] = session.get('score', 0) + 10
                else:
                    error = "❌ Sai rồi! Thử lại nhé."
            except ValueError:
                error = "⚠️ Hãy nhập một số nguyên."

    return render_template("level1.html",
                           message=LEVEL1_CIPHER,
                           result=result,
                           error=error,
                           is_correct=is_correct)


# ---------- LEVEL 2: Vigenère Cipher ----------
@app.route('/level2', methods=['GET', 'POST'])
def level2():
    keyword = "CHIAKHOA"
    correct_answer = "HELLOVIGENERE"
    ciphertext = vigenere_encrypt(correct_answer, keyword)

    result = ""
    feedback = ""
    is_correct = False

    if request.method == 'POST':
        user_key = request.form.get('keyword', '').strip().upper().replace(" ", "")
        if user_key == keyword:
            result = vigenere_decrypt(ciphertext, user_key)
            if result.upper() == correct_answer:
                is_correct = True
                session['score'] = session.get('score', 0) + 10
            else:
                feedback = "❌ Đúng từ khóa nhưng sai nội dung giải mã."
        else:
            feedback = "🔑 Sai từ khóa. Gợi ý: Đây là vật dùng để mở kho báu."

    return render_template('level2.html',
                           ciphertext=ciphertext,
                           result=result,
                           feedback=feedback,
                           is_correct=is_correct)


# ---------- LEVEL 3: RSA ----------
@app.route('/level3', methods=['GET', 'POST'])
def level3():
    ciphertext = [2159, 1307, 2790, 1759, 1307, 2906, 538, 368]
    correct_d = 2753
    correct_n = 3233
    result = ''
    feedback = ''
    is_correct = False
    show_hint = False

    if request.method == 'POST':
        try:
            d = int(request.form.get('d'))
            n = int(request.form.get('n'))

            result = ''.join([chr(pow(c, d, n)) for c in ciphertext])

            if d == correct_d and n == correct_n:
                if result.upper() == "TOADO123":
                    session['score'] += 20
                    is_correct = True  # ✅ Gán đúng tại đây
                else:
                    feedback = "🔓 Sai thông điệp! Có vẻ bạn nhập đúng d và n nhưng thông điệp giải mã không đúng."
            else:
                feedback = "❌ Không đúng! Bạn nên tìm quanh phòng xem có manh mối nào không..."
                show_hint = True

        except Exception:
            feedback = "⚠️ Hãy nhập đúng định dạng số nguyên cho d và n."
            show_hint = True

    return render_template("level3.html",
                           ciphertext=ciphertext,
                           result=result,
                           feedback=feedback,
                           is_correct=is_correct,
                           show_hint=show_hint)


# ---------- LEVEL 4: AES ----------
CIPHERTEXT_B64 = "EGy/mFNijfQHXihkI5fnAAHOv1205qZzaiUKdsCwEfo="

@app.route('/level4', methods=['GET', 'POST'])
def level4():
    result = ""
    feedback = ""
    if request.method == 'POST':
        user_key = request.form['key']
        try:
            if len(user_key) != 16:
                raise ValueError("Khóa phải có đúng 16 ký tự.")

            key = user_key.encode()
            data = base64.b64decode(CIPHERTEXT_B64)
            iv = data[:16]
            ciphertext = data[16:]

            cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size).decode('utf-8')

            if decrypted.strip().lower() == "bao mat":
                return render_template('victory.html')
            else:
                feedback = "❌ Giải mã sai! Hãy thử lại."
        except Exception:
            feedback = "⚠️ Lỗi giải mã! Kiểm tra khóa và thử lại."

    return render_template('level4.html',
                           ciphertext=CIPHERTEXT_B64,
                           result=result,
                           feedback=feedback)

# ---------- KHỞI ĐỘNG ỨNG DỤNG ----------
if __name__ == '__main__':
    app.run(debug=True)
