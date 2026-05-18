const express = require('express');
const app = express();
const PORT = 8000;

app.use(express.json());

// Rute untuk melakukan prediksi
const rutePrediksi = require('./routes/prediksi');
app.use('/api/prediksi', rutePrediksi);

// Cek layanan Express
app.get('/health', (req, res) => {
    res.status(200).json({ status: "aktif", layanan: "express-service" });
});

// Menjalankan layanan Express
app.listen(PORT, () => {
    console.log(`Layanan Express berjalan di http://localhost:${PORT}`);
});