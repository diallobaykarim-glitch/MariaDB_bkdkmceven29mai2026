import streamlit as st
import requests

st.title("🏥 ORL IA Dashboard")

age = st.number_input("Âge", 0, 100, 40)
sexe = st.selectbox("Sexe", [0, 1])

obstruction = st.selectbox("Obstruction nasale", [0, 1])
rhinorrhee = st.selectbox("Rhinorrhée", [0, 1])
epistaxis = st.selectbox("Epistaxis", [0, 1])
anosmie = st.selectbox("Anosmie", [0, 1])
tabac = st.selectbox("Tabac", [0, 1])

if st.button("Prédire"):
    response = requests.post("http://127.0.0.1:8000/predict", json={
        "age": age,
        "sexe": sexe,
        "obstruction_nasale": obstruction,
        "rhinorrhee": rhinorrhee,
        "epistaxis": epistaxis,
        "anosmie": anosmie,
        "tabac": tabac
    })

    st.success(response.json()["prediction"])