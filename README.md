Nama: Akbar Fitri Andhika
NIM: 2410511011

# Tugas Pertemuan 11 - Python ML Service + Express.js
Tugas ini membuat sistem microservice yang terdiri dari dua service,
yaitu Python Flask untuk ML dan Express.js sebagai penghubungnya.

## Dataset dan Model yang Dipakai
- Dataset Wine dari scikit-learn (178 data, 13 fitur)
- Model Logistic Regression, akurasi 100% di data uji
- Hasil prediksi berupa 3 kelas wine (Kelas 1, 2, 3)

## Struktur Folder
TugasP11/
├── python-ml/
│   ├── train_model.py
│   ├── app.py
│   ├── model.pkl
│   └── scaler.pkl
├── express-service/
│   ├── index.js
│   ├── routes/
│   │   └── prediksi.js
│   └── package.json
└── README.md

## Cara Install dan Jalankan

### Python ML Service
Buka CMD, masuk ke folder python-ml lalu install dulu:

py -m pip install flask scikit-learn joblib numpy

Latih modelnya:

python train_model.py

Lalu jalankan servicenya:

python app.py

Jalan di http://localhost:7070

### Express Service
Buka CMD baru, masuk ke folder express-service:

npm install
node index.js

Jalan di http://localhost:8000

> Pastikan Flask sudah jalan dulu sebelum menjalankan Express

## Endpoint yang Tersedia

### Flask (port 7070)
- GET /health
- POST /prediksi

### Express (port 8000)
- GET /health
- GET /api/prediksi/health
- POST /api/prediksi

## Contoh Pemakaian
Kirim POST ke http://localhost:8000/api/prediksi dengan body:
```json
{
  "fitur": [14.13, 1.71, 2.43, 15.16, 127.10, 2.28, 3.46, 1.28, 2.39, 5.65, 1.14, 3.62, 1062.0]
}
```

Kalau fitur kurang dari 13 akan muncul:
```json
{
  "pesan": "Fitur harus berjumlah 13"
}
```