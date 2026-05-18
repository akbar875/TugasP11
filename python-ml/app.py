from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
import joblib
import numpy as np

app = Flask(__name__)

# Konfigurasi JWT
app.config["JWT_SECRET_KEY"] = "79e99a937cbf66eca5371ca5e9b3f81618306d1d5873f85fc6831e3168bb37b4"
jwt = JWTManager(app)

# Memuat model dan normalisasi saat service dijalankan
model = joblib.load("model.pkl")
normalisasi = joblib.load("normalisasi.pkl")

# Simulasi database user (disimpan di memori)
users_db = {}

# Melabel kelas wine dengan angka
label_wine = {
    0: "Kelas 1 (Wine A)",
    1: "Kelas 2 (Wine B)",
    2: "Kelas 3 (Wine C)"
}

# Membuat fungsi untuk melakukan prediksi single
def prediksi_single(fitur):
    arr = np.array(fitur).reshape(1, -1)
    arr = normalisasi.transform(arr)
    hasil = model.predict(arr)
    prob = model.predict_proba(arr)
    return {
        "prediksi": int(hasil[0]),
        "label":label_wine[int(hasil[0])],
        "keyakinan": float(prob.max()),
        "layanan": "python-ml-flask"
    }

# Route untuk memeriksa service apakah bisa berjalan
@app.route("/health", methods=["GET"])
def kesehatan():
    return jsonify({
        "status": "aktif",
        "layanan": "python-ml-flask",
        "model": "Regresi Logistik",
        "dataset": "Wine"
    }), 200

# Route untuk melakukan registrasi
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    # Validasi input username dan password wajib ada
    if not data or "username" not in data or "password" not in data:
        return jsonify({"pesan": "Username dan password wajib diisi"}), 400

    # Validasi username dan password tidak boleh kosong
    if not data["username"].strip() or not data["password"].strip():
        return jsonify({"pesan": "Username dan password tidak boleh kosong"}), 400

    # Validasi username sudah terdaftar
    if data["username"] in users_db:
        return jsonify({"pesan": "Username sudah terdaftar"}), 409

    # Simpan user ke database simulasi
    users_db[data["username"]] = data["password"]
    return jsonify({"pesan": "Registrasi berhasil, silakan login"}), 201

# Route untuk melakukan login
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    # Validasi input username dan password wajib ada
    if not data or "username" not in data or "password" not in data:
        return jsonify({"pesan": "Username dan password wajib diisi"}), 400

    # Validasi username terdaftar
    if data["username"] not in users_db:
        return jsonify({"pesan": "Username tidak ditemukan, silakan register terlebih dahulu"}), 401

    # Validasi password 
    if users_db[data["username"]] != data["password"]:
        return jsonify({"pesan": "Password salah"}), 401

    token = create_access_token(identity=data["username"])
    return jsonify({"token": token}), 200

# Route untuk melakukan prediksi
@app.route("/prediksi", methods=["POST"])
def prediksi():
    data = request.get_json()

    # Validasi input fitur wajib ada
    if not data or "fitur" not in data:
        return jsonify({ "pesan": "Field 'fitur' wajib ada" }), 400

    # Validasi jumlah fitur
    if len(data["fitur"]) != 13:
        return jsonify({ "pesan": "Jumlah fitur harus 13" }), 400

    try:
        hasil = prediksi_single(data["fitur"])
        return jsonify(hasil)

    except Exception as e:
        return jsonify({"pesan": str(e)}), 500

# Route untuk melakukan prediksi batch
@app.route("/batch-prediksi", methods=["POST"])
@jwt_required()

# Membuat fungsi untuk melakukan prediksi batch
def batch_prediksi():
    data = request.get_json()

    # Validasi input data wajib ada
    if not data or "data" not in data:
        return jsonify({"pesan": "Field data wajib diisi"}), 400

    # Validasi data berupa array
    if not isinstance(data["data"], list) or len(data["data"]) == 0:
        return jsonify({"pesan": "Field data harus berupa array dan tidak boleh kosong"}), 400

    hasil_semua = []
    for i, fitur in enumerate(data["data"]):
        if len(fitur) != 13:
            hasil_semua.append({
                "index": i,
                "error": "Fitur harus berjumlah 13"
            })
            continue
        try:
            hasil = prediksi_single(fitur)
            hasil["index"] = i
            hasil_semua.append(hasil)
        except Exception as e:
            hasil_semua.append({
                "index": i,
                "error": str(e)
            })

    return jsonify({
        "total": len(data["data"]),
        "hasil": hasil_semua
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7070, debug=True)