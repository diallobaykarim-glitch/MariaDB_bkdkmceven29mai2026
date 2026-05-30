import os
from fastapi import FastAPI
from pydantic import BaseModel
import mariadb
import joblib
import pandas as pd

app = FastAPI(title="ORL IA API")

model = joblib.load("model_orl.pkl")
encoder = joblib.load("encoder_orl.pkl")

def get_connection():
    return mariadb.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

class PatientInput(BaseModel):
    age: int
    sexe: int
    tabac: int
    alcool: int
    obstruction_nasale: int
    rhinorrhee: int
    epistaxis: int
    anosmie: int
    polypose_nasale: int
    douleur_faciale: int

@app.get("/patients")
def patients():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM patients")
    data = cur.fetchall()
    conn.close()
    return data

@app.post("/predict")
def predict(p: PatientInput):
    df = pd.DataFrame([[p.age, p.sexe, p.tabac, p.alcool, p.obstruction_nasale,
                        p.rhinorrhee, p.epistaxis, p.anosmie, p.polypose_nasale,
                        p.douleur_faciale]])

    pred = model.predict(df)
    return {"prediction": encoder.inverse_transform(pred)[0]}
