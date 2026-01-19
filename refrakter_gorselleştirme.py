import pandas as pd
import matplotlib.pyplot as plt
import os

os.makedirs("visuals", exist_ok=True)

# Veriyi oku (noktalı virgül ile ayrılmış)
df = pd.read_csv("data/refrakter_verisi.csv", sep=";")

df = df.sort_values("Yorgunluk_Suresi")

# Çizgi grafiği
plt.figure(figsize=(10, 6))
plt.plot(df["Yorgunluk_Suresi"], df["Hasar_Orani"], color="blue", linewidth=2)
plt.xlabel("Yorgunluk Süresi (dk)")
plt.ylabel("Hasar Oranı")
plt.title("Yorgunluk Süresine Göre Hasar Oranı")
plt.grid(True)
plt.tight_layout()
plt.savefig("visuals/grafik.png")  # PNG olarak kaydet
plt.show()
