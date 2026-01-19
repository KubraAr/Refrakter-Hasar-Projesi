def karbon_ayak_izi_hesapla(yorgunluk_suresi, curuf_sicakligi, islem_suresi):
    """
    Karbon ayak izi hesaplama formulu:
    - Sicaklik × Islem Suresi × 0.00042
    - Yorgunluk Suresi × 0.0003
    Toplam CO2 salinimi (kg)
    """
    sicaklik_katki = curuf_sicakligi * islem_suresi * 0.00042
    yorgunluk_katki = yorgunluk_suresi * 0.0003
    toplam_karbon = (sicaklik_katki + yorgunluk_katki) / 1000  # gramdan kilograma
    return toplam_karbon

# Örnek kullanım
yorgunluk = 60          #dakika olarak
sicaklik = 1300         #derece olarak
islem_suresi = 50      #dakika olarak

emisyon = karbon_ayak_izi_hesapla(yorgunluk, sicaklik, islem_suresi)
print(f"⚠️ Kayıp nedeniyle tahmini CO2 salımı: {emisyon:.2f} ton")
