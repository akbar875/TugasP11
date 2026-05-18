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
│   └── normalisasi.pkl       
│   
├── service-express/
│   ├── routes/
│   │   └── prediksi.js      
│   ├── index.js              
│   └── package.json
|
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
- POST /register
- POST /login
- POST /prediksi
- POST /batch-prediksi

### Express (port 8000)
- GET /health
- GET /api/prediksi/health
- POST /api/prediksi
- POST /api/prediksi/batch

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

Kirim GET ke http://localhost:7070/health untuk cek layanan Flask:
```json
{
  "status": "aktif",
  "layanan": "python-ml-flask",
  "model": "Regresi Logistik",
  "dataset": "Wine"
}
```

Kirim GET ke http://localhost:8000/api/prediksi/health untuk cek koneksi antar layanan:
```json
{
  "layanan_express": "aktif",
  "layanan_ml": {
    "status": "aktif",
    "layanan": "python-ml-flask",
    "model": "Regresi Logistik",
    "dataset": "Wine"
  }
}
```

Kirim POST ke http://localhost:7070/register dengan body:
```json
{
  "username": "akbar",
  "password": "rahasia123"
}
```

Responsnya:
```json
{
  "pesan": "Registrasi berhasil, silakan login"
}
```

Kirim POST ke http://localhost:7070/login dengan body:
```json
{
  "username": "akbar",
  "password": "rahasia123"
}
```

Responsnya:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

Kirim POST ke http://localhost:7070/batch-prediksi dengan header Authorization: Bearer <token> dan body:
```json
{
  "data": [
    [14.13, 1.71, 2.43, 15.16, 127.0, 2.80, 3.06, 0.28, 2.29, 5.64, 1.04, 3.92, 1065.0],
    [13.20, 1.78, 2.14, 11.20, 100.0, 2.65, 2.76, 0.26, 1.28, 4.38, 1.05, 3.40, 1050.0]
  ]
}
```

Responsnya:
```json
{
  "total": 2,
  "hasil": [
    {
      "index": 0,
      "prediksi": 0,
      "label": "Kelas 1 (Wine A)",
      "keyakinan": 0.9998,
      "layanan": "python-ml-flask"
    },
    {
      "index": 1,
      "prediksi": 0,
      "label": "Kelas 1 (Wine A)",
      "keyakinan": 0.9954,
      "layanan": "python-ml-flask"
    }
  ]
}
```