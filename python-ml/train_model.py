from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

import joblib

# 1. Memuat dataset wine dari scikit-learn
print("Memuat dataset wine...")
data_wine = load_wine()
X, y = data_wine.data, data_wine.target

# 2. Bagi data latih dan data uji 
X_latih, X_uji, y_latih, y_uji = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 3. Melakukan normalisasi data 
normalisasi = StandardScaler()
X_latih_normal = normalisasi.fit_transform(X_latih)
X_uji_normal = normalisasi.transform(X_uji)

# 4. Melatih model untuk regresi logistik
print("Melatih model Regresi Logistik...")
model = LogisticRegression(max_iter=200, random_state=42)
model.fit(X_latih_normal, y_latih)

# 5. Evaluasi model dengan data uji
y_prediksi = model.predict(X_uji_normal)
print(f"Akurasi Model: {accuracy_score(y_uji, y_prediksi):.4f}")
print(classification_report(y_uji, y_prediksi, target_names=data_wine.target_names))

# 6. Simpan model dan normalisasi dalam file pickle
joblib.dump(model, "model.pkl")
joblib.dump(normalisasi, "normalisasi.pkl")
print("Model dan normalisasi berhasil disimpan!")