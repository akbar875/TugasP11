from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Memuat model dan normalisasi saat service dijalankan
model = joblib.load("model.pkl")
normalisasi = joblib.load("normalisasi.pkl")

# Melabel kelas wine dengan angka
label_wine = {
    0: "Kelas 1 (Wine A)",
    1: "Kelas 2 (Wine B)",
    2: "Kelas 3 (Wine C)"
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
        # Normalisasi input fitur
        fitur = np.array(data["fitur"]).reshape(1, -1)
        fitur_normal = normalisasi.transform(fitur)

        # Melakukan prediksi dengan model
        hasil_prediksi = model.predict(fitur_normal)
        probabilitas = model.predict_proba(fitur_normal)

        return jsonify({
            "hasil_prediksi": int(hasil_prediksi[0]),
            "label": label_wine[int(hasil_prediksi[0])],
            "tingkat_keyakinan": float(probabilitas.max()),
            "layanan": "python-ml-flask"
        }), 200

    except Exception as e:
        return jsonify({ "pesan_error": str(e) }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7070, debug=True)