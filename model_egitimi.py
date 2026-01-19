# model_egitimi.py

import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, VotingRegressor
from sklearn.model_selection import train_test_split, cross_val_score
import pickle

# Veri setini oku
df = pd.read_csv("data/refrakter_verisi.csv", sep=";")
df["Curuf_Karakteri"] = df["Curuf_Karakteri"].map({"Asidik": 0, "Bazik": 1})

X = df[["Yorgunluk_Suresi", "Curuf_Sicakligi", "Curuf_Karakteri", "Bekleme_Suresi", "Islem_Suresi"]]
y = df["Hasar_Orani"]

df["Curuf_Karakteri"] = df["Curuf_Karakteri"].map({"Asidik": 0, "Bazik": 1})

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# MODELLER
rf = RandomForestRegressor(n_estimators=100, random_state=42)
gb = GradientBoostingRegressor(n_estimators=100, random_state=42)

# test skorları
def evaluate_model(name, model):
    model.fit(X_train, y_train)
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    cv_score = cross_val_score(model, X, y, cv=5).mean()
    print(f"{name.upper()} -> Eğitim R² = {train_score:.3f} | Test R² = {test_score:.3f} | CV Ort = {cv_score:.3f}")
    return model

# Değerlendirme
rf_model = evaluate_model("Random Forest", rf)
gb_model = evaluate_model("Gradient Boosting", gb)

voting = VotingRegressor(estimators=[
    ("rf", rf_model),
    ("gb", gb_model)
])
voting.fit(X_train, y_train)
print(f"\nVotingRegressor (RF + GB): Eğitim R² = {voting.score(X_train, y_train):.3f} | Test R² = {voting.score(X_test, y_test):.3f}")
print("VotingRegressor modeli başarıyla eğitildi ve kaydedildi.")

with open("models/erozyon_model.pkl", "wb") as f:
    pickle.dump(voting, f)



