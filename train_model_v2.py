import mariadb
import pandas as pd
import joblib

from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

# =========================
# DB CONNECTION
# =========================
conn = mariadb.connect(
    host="localhost",
    user="root",
    password="root123",
    database="orl_ia"
)

cur = conn.cursor()

cur.execute("""
    SELECT age, nom, diagnostic,
           obstruction_nasale,
           rhinorrhee,
           epistaxis,
           anosmie,
           tabac
    FROM patients
""")

rows = cur.fetchall()
conn.close()

df = pd.DataFrame(rows, columns=[
    "age", "nom", "diagnostic",
    "obstruction_nasale",
    "rhinorrhee",
    "epistaxis",
    "anosmie",
    "tabac"
])

# sexe
df["sexe"] = df["nom"].apply(lambda x: 1 if "-M" in x else 0)

X = df[
    ["age", "sexe",
     "obstruction_nasale",
     "rhinorrhee",
     "epistaxis",
     "anosmie",
     "tabac"]
]

encoder = LabelEncoder()
y = encoder.fit_transform(df["diagnostic"])

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=8,
    random_state=42
)

model.fit(X, y)

# SAVE MODEL
joblib.dump(model, "model_orl.pkl")
joblib.dump(encoder, "encoder_orl.pkl")

print("MODEL V2 SAUVEGARDE ✔")