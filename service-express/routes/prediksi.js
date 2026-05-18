const express = require('express');
const axios = require('axios');
const router = express.Router();

const URL_ML = 'http://localhost:7070';

// Metode untuk melakukan prediksi
router.post('/', async (req, res) => {
    const { fitur } = req.body;

    // Validasi input fitur wajib di isi
    if (!fitur || !Array.isArray(fitur)) {
        return res.status(400).json({ pesan: "Field 'fitur' wajib ada dan harus berupa array" });
    }

    try {
        // Panggil layanan Python ML melalui HTTP
        const responML = await axios.post( `${URL_ML}/prediksi`, { fitur }, { timeout: 5000 }
        );

        // Menggabungkan dan mengembalikan hasil prediksi
        return res.status(200).json({
            status: "berhasil",
            data: {
                fitur_masukan: fitur,
                hasil_prediksi: responML.data.hasil_prediksi,
                label: responML.data.label,
                tingkat_keyakinan: responML.data.tingkat_keyakinan,
                layanan_ml: responML.data.layanan
            },
            waktu: new Date().toISOString()
        });

    } catch (error) {
        // Circuit breaker jika layanan Python ML tidak tersedia
        if (error.code === 'ECONNREFUSED' || error.code === 'ETIMEDOUT') {
            return res.status(503).json({ pesan: "Layanan ML tidak tersedia, silakan coba beberapa saat lagi" });
        }

        // Circuit breaker jika layanan Python ML mengembalikan error
        if (error.response) {
            return res.status(error.response.status).json(error.response.data );
        }
        
        return res.status(500).json({ pesan: "Terjadi kesalahan: " + error.message });
    }
});

// Metode untuk memeriksa layanan apakah bisa berjalan
router.get('/health', async (req, res) => {
    try {
        const cek = await axios.get( `${URL_ML}/health`, { timeout: 3000 });
        
        return res.status(200).json({ layanan_express: "aktif", layanan_ml: cek.data });

    } catch (error) {
        return res.status(503).json({ layanan_express: "aktif", layanan_ml: "tidak tersedia" });
    }
});

module.exports = router;