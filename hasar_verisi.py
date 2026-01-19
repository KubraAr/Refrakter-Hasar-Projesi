import pandas as pd
import numpy as np
import os

# Klasörü oluştur
os.makedirs("data", exist_ok=True)

# 2 yıllık veri -- toplam 730 tane

# Düşük Riskli Veriler (243 veri)
low_risk = {
    "Yorgunluk_Suresi": np.random.randint(2, 1000, 243),
    "Curuf_Sicakligi": np.random.randint(1600, 1680, 243),
    "Curuf_Karakteri": np.random.choice(["Bazik"], 243),
    "Bekleme_Suresi": np.random.randint(10, 60, 243),
    "Islem_Suresi": np.random.randint(1, 4, 243),
    "Agirlik": np.random.randint(1000, 9000, 243)
}

# Orta Riskli Veriler (243 veri)
medium_risk = {
    "Yorgunluk_Suresi": np.random.randint(1000, 2500, 243),
    "Curuf_Sicakligi": np.random.randint(1680, 1700, 243),
    "Curuf_Karakteri": np.random.choice(["Bazik", "Asidik"], 243),
    "Bekleme_Suresi": np.random.randint(60, 200, 243),
    "Islem_Suresi": np.random.randint(3, 7, 243),
    "Agirlik": np.random.randint(9000, 14000, 243)
}

# Yüksek Riskli Veriler (244 veri)
high_risk = {
    "Yorgunluk_Suresi": np.random.randint(2500, 4321, 244),
    "Curuf_Sicakligi": np.random.randint(1700, 1751, 244),
    "Curuf_Karakteri": np.random.choice(["Asidik"], 244),
    "Bekleme_Suresi": np.random.randint(200, 361, 244),
    "Islem_Suresi": np.random.randint(6, 11, 244),
    "Agirlik": np.random.randint(14000, 17001, 244)
}

# DataFrame'e dönüştür
df_low = pd.DataFrame(low_risk)
df_medium = pd.DataFrame(medium_risk)
df_high = pd.DataFrame(high_risk)


df = pd.concat([df_low, df_medium, df_high], ignore_index=True) # Birleştir

# Fonksiyon ile hasar oranı hesapla
def hasar_orani_hesapla(yorgunluk, sicaklik, karakter, bekleme, islem, agirlik):
    karakter_kod = 0 if karakter == "Asidik" else 1
    sicaklik_katki = (sicaklik - 1600) / 80 if sicaklik < 1680 else ((sicaklik - 1680) * 2 / 70 + 1)

    if bekleme <= 10:
        bekleme_katki = 0.05
    elif bekleme <= 60:
        bekleme_katki = (bekleme / 100)
    else:
        bekleme_katki = (bekleme / 60) * 0.2

    agirlik_katki = (agirlik / 10000) if agirlik <= 10000 else ((agirlik - 10000) / 7000) + 1

    oran = (
        0.3 * sicaklik_katki +
        0.2 * (yorgunluk / 400) +
        0.15 * bekleme_katki +
        0.1 * karakter_kod +
        0.1 * (islem / 60) +
        0.15 * agirlik_katki
    )
    return oran

# Her bir satır için hasar oranı hesapla
df["Hasar_Orani"] = df.apply(lambda row: hasar_orani_hesapla(
    row["Yorgunluk_Suresi"],
    row["Curuf_Sicakligi"],
    row["Curuf_Karakteri"],
    row["Bekleme_Suresi"],
    row["Islem_Suresi"],
    row["Agirlik"]
), axis=1)


# Data dosyasına kayıt.
df.to_csv("data/refrakter_verisi.csv", sep=";", index=False)

print(" Hasar verisi başarıyla oluşturuldu ve 'data/refrakter_verisi.csv' dosyasına kaydedildi.")






