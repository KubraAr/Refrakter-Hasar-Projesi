import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Modeli yükle (VotingRegressor)
with open("models/erozyon_model.pkl", "rb") as f:
    model = pickle.load(f)
    
st.title("Konverterdeki Refrakter Hasar (Korozyon) Tahmini ve Karbon Ayak İzi Hesaplama")

# Kullanıcıdan veri girişi
st.sidebar.header("Veri Girişi")

yorgunluk = st.sidebar.slider("Yorgunluk Süresi (dk)", 2, 4320, 10) # Ne kadar kullanıldı.
sicaklik = st.sidebar.slider("Cüruf Sıcaklığı (°C)", 1600, 1750, 1650)  # 1650 ile 1680 arası durabilir, 1700 üstüne çıkması durumunda büyük hasar alır.
karakter = st.sidebar.selectbox("Cüruf Karakteri", ["Asidik", "Bazik"])  # Asidik olması daha çok zarar verir.
bekleme = st.sidebar.slider("Bekleme Süresi (dk)", 2, 360, 10) ## 10 dk ya kadar makine kendine gelebilir, bundan dolayı 10dk sonrasında verim daha fazladır.
islem = st.sidebar.slider("İşlem Süresi (dk)", 1, 10, 3)  # 2-5 dakika arasında taşınım yapılabilir. 5 ten sonrası büyük ölçüde zarar verir.
agirlik = st.sidebar.slider("Malzeme Ağırlığı (kg)", 1000, 17000, 10000)


def hasar_orani_hesapla(yorgunluk, sicaklik, karakter, bekleme, islem, agirlik):
    karakter_kod = 0 if karakter == "Asidik" else 1

    sicaklik_katki = (sicaklik - 1600) / 80 if sicaklik < 1680 else ((sicaklik - 1680) * 2 / 70 + 1)

    # Bekleme süresi: 10 dk altı olumlu, 60 dk üzeri negatif katkı
    if bekleme <= 10:
        bekleme_katki = 0.05
    elif bekleme <= 60:
        bekleme_katki = (bekleme / 100)
    else:
        bekleme_katki = (bekleme / 60) * 0.2

    # Ağırlık: 10.000 kg üstü hasar artırır
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



def karbon_ayak_izi_hesapla(yorgunluk, sicaklik, islem):
    sicaklik_katki = sicaklik * islem * 0.00042
    yorgunluk_katki = yorgunluk * 0.0003
    toplam_karbon = (sicaklik_katki + yorgunluk_katki) / 1000  # kg cinsinden
    return toplam_karbon

# Tekil tahmin
if st.sidebar.button("Tahmin Et"):
    hasar = hasar_orani_hesapla(yorgunluk, sicaklik, karakter, bekleme, islem, agirlik)
    emisyon = karbon_ayak_izi_hesapla(yorgunluk, sicaklik, islem)

   
    if hasar < 0.75:
        st.success(f"🟢 Tahmini Hasar Oranı: {hasar:.2f} (Güvenli)")
    elif hasar < 1.0:
        st.warning(f"🟡 Tahmini Hasar Oranı: {hasar:.2f} (Kritik Sınır)")
    else:
        st.error(f"🔴 Tahmini Hasar Oranı: {hasar:.2f} (Tehlikeli)")

    st.info(f"🌱 Tahmini Karbon Ayak İzi: {emisyon:.4f} ton CO2")
    

# Toplu Tahmin
st.subheader("📁 Toplu Tahmin için CSV Yükle")

csv_dosya = st.file_uploader("CSV dosyanızı yükleyin", type=["csv"])
if csv_dosya is not None:
    try:
        veri = pd.read_csv(csv_dosya, sep=";")

        gerekli = ["Yorgunluk_Suresi", "Curuf_Sicakligi", "Curuf_Karakteri",
                   "Bekleme_Suresi", "Islem_Suresi", "Agirlik"]
        eksik = [sutun for sutun in gerekli if sutun not in veri.columns]

        if eksik:
            st.error(f"CSV dosyanızda şu sütun(lar) eksik: {eksik}")
        else:
            # Fonksiyon ile satır satır hasar oranı hesapla
            def hesapla_satir(satir):
                return hasar_orani_hesapla(
                    yorgunluk=satir["Yorgunluk_Suresi"],
                    sicaklik=satir["Curuf_Sicakligi"],
                    karakter=satir["Curuf_Karakteri"],
                    bekleme=satir["Bekleme_Suresi"],
                    islem=satir["Islem_Suresi"],
                    agirlik=satir["Agirlik"]
                )

            veri["Hasar_Orani"] = veri.apply(hesapla_satir, axis=1)

            # Karbon Ayak İzi hesapla
            veri["Karbon_Ayak_İzi"] = (
                (veri["Curuf_Sicakligi"] * veri["Islem_Suresi"] * 0.00042 +
                 veri["Yorgunluk_Suresi"] * 0.0003) / 1000
            )

            st.success("✅ Tahmin başarıyla yapıldı.")
            st.dataframe(veri[["Hasar_Orani", "Karbon_Ayak_İzi"]].head())

            # CSV indirme
            csv = veri.to_csv(index=False, sep=";").encode("utf-8")
            st.download_button(
                label="Sonuçları İndir (CSV)",
                data=csv,
                file_name="tahmin_sonuclari.csv",
                mime="text/csv"
            )

    except Exception as e:
        st.error(f"Hata oluştu: {e}")




