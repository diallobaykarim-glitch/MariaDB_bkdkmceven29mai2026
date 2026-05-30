from fastapi import FastAPI
from pydantic import BaseModel
import mariadb
import joblib
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="ORL IA API DOCKER")

# =========================
# MODELE ML
# =========================
model = joblib.load("model_orl.pkl")
encoder = joblib.load("encoder_orl.pkl")

# =========================
# CONNEXION DB
# =========================
def get_connection():
    return mariadb.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

# =========================
# INPUT API
# =========================
class PatientInput(BaseModel):
    age: int
    sexe: int
    obstruction_nasale: int
    rhinorrhee: int
    epistaxis: int
    anosmie: int
    tabac: int

# =========================
# GET PATIENTS
# =========================
@app.get("/patients")
def get_patients():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM patients")
    rows = cur.fetchall()

    conn.close()
    return rows

# =========================
# PREDICTION
# =========================
@app.post("/predict")
def predict(p: PatientInput):

    sample = [[
        p.age,
        p.sexe,
        p.obstruction_nasale,
        p.rhinorrhee,
        p.epistaxis,
        p.anosmie,
        p.tabac
    ]]

    pred = model.predict(sample)
    result = encoder.inverse_transform(pred)

    return {"prediction": result[0]}

# =========================
# SCORE RISQUE
# =========================
@app.post("/risk")
def risk(p: PatientInput):

    score = (
        p.obstruction_nasale +
        p.rhinorrhee +
        p.epistaxis +
        p.anosmie +
        p.tabac
    ) * 20

    niveau = "Faible"
    if score > 60:
        niveau = "Élevé"
    elif score > 30:
        niveau = "Modéré"

    return {
        "score": score,
        "niveau_risque": niveau
    }