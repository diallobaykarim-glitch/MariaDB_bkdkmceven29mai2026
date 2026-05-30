import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.set_page_config(page_title="ORL IA Platform", layout="wide")
st.title("🏥 IA Hospital Platform FULL PRO")

tab1, tab2, tab3 = st.tabs(["ORL Prediction", "Statistics", "Analytics"])

with tab1:
    st.header("ORL Prediction")
    
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input("Age", min_value=0, max_value=120, value=45, step=1)
        sexe = st.selectbox("Sexe", options=[0, 1], format_func=lambda x: "Femme" if x == 0 else "Homme")
        tabac = st.selectbox("Tabac", options=[0, 1], format_func=lambda x: "Non" if x == 0 else "Oui")
    
    with col2:
        alcool = st.selectbox("Alcool", options=[0, 1], format_func=lambda x: "Non" if x == 0 else "Oui")
        obstruction_nasale = st.selectbox("Obstruction nasale", options=[0, 1], format_func=lambda x: "Non" if x == 0 else "Oui")
        rhinorrhee = st.selectbox("Rhinorrhée", options=[0, 1], format_func=lambda x: "Non" if x == 0 else "Oui")
    
    col3, col4 = st.columns(2)
    
    with col3:
        epistaxis = st.selectbox("Épistaxis", options=[0, 1], format_func=lambda x: "Non" if x == 0 else "Oui")
        anosmie = st.selectbox("Anosmie", options=[0, 1], format_func=lambda x: "Non" if x == 0 else "Oui")
    
    with col4:
        polypose_nasale = st.selectbox("Polypose nasale", options=[0, 1], format_func=lambda x: "Non" if x == 0 else "Oui")
        douleur_faciale = st.selectbox("Douleur faciale", options=[0, 1], format_func=lambda x: "Non" if x == 0 else "Oui")

    if st.button("Predict ORL", key="predict_orl"):
        try:
            r = requests.post("http://api_orl:8000/predict", json={
                "age": int(age),
                "sexe": int(sexe),
                "tabac": int(tabac),
                "alcool": int(alcool),
                "obstruction_nasale": int(obstruction_nasale),
                "rhinorrhee": int(rhinorrhee),
                "epistaxis": int(epistaxis),
                "anosmie": int(anosmie),
                "polypose_nasale": int(polypose_nasale),
                "douleur_faciale": int(douleur_faciale)
            }, timeout=5)
            if r.status_code == 200:
                st.success(f"**Diagnostic:** {r.json()['prediction']}")
            else:
                st.error(f"Erreur: {r.status_code}")
        except Exception as e:
            st.error(f"Erreur API ORL: {str(e)}")

with tab2:
    st.header("📊 Statistiques ORL")
    
    try:
        r = requests.get("http://api_orl:8000/patients", timeout=5)
        if r.status_code == 200 and r.text:
            data = r.json()
            
            if len(data) > 0:
                # Convertir directement sans spécifier de colonnes
                df = pd.DataFrame(data)
                
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Total patients", len(df))
                col2.metric("Âge moyen", f"{df.iloc[:, 1].mean():.1f} ans")
                col3.metric("Hommes", int(df.iloc[:, 2].sum()))
                col4.metric("Femmes", len(df) - int(df.iloc[:, 2].sum()))
                
                st.divider()
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Distribution par âge")
                    fig, ax = plt.subplots(figsize=(8, 5))
                    ax.hist(df.iloc[:, 1], bins=10, color='skyblue', edgecolor='black')
                    ax.set_xlabel("Âge (ans)")
                    ax.set_ylabel("Nombre de patients")
                    ax.grid(alpha=0.3)
                    st.pyplot(fig)
                
                with col2:
                    st.subheader("Répartition Sexe")
                    sexe_counts = [len(df[df.iloc[:, 2] == 0]), len(df[df.iloc[:, 2] == 1])]
                    fig, ax = plt.subplots(figsize=(8, 5))
                    ax.pie(sexe_counts, labels=['Femme', 'Homme'], autopct='%1.1f%%', 
                           colors=['pink', 'lightblue'], startangle=90)
                    st.pyplot(fig)
                
                st.divider()
                st.subheader("Facteurs de risque")
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Tabac", f"{int(df.iloc[:, 3].sum())}/{len(df)} ({df.iloc[:, 3].mean()*100:.1f}%)")
                col2.metric("Alcool", f"{int(df.iloc[:, 4].sum())}/{len(df)} ({df.iloc[:, 4].mean()*100:.1f}%)")
                col3.metric("Polypose nasale", f"{int(df.iloc[:, 9].sum())}/{len(df)} ({df.iloc[:, 9].mean()*100:.1f}%)")
            else:
                st.info("Aucune donnée disponible")
        else:
            st.warning("Erreur lors de la récupération des données")
    except Exception as e:
        st.warning(f"Erreur API: {str(e)}")

with tab3:
    st.header("📈 Analytics avancés")
    
    try:
        r = requests.get("http://api_orl:8000/patients", timeout=5)
        if r.status_code == 200 and r.text:
            data = r.json()
            
            if len(data) > 0:
                df = pd.DataFrame(data)
                
                st.subheader("Corrélations signes cliniques")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    obs_rate = (df.iloc[:, 5].sum()) / len(df) * 100
                    st.metric("Obstruction nasale", f"{obs_rate:.1f}%")
                with col2:
                    rhin_rate = (df.iloc[:, 6].sum()) / len(df) * 100
                    st.metric("Rhinorrhée", f"{rhin_rate:.1f}%")
                with col3:
                    epis_rate = (df.iloc[:, 7].sum()) / len(df) * 100
                    st.metric("Épistaxis", f"{epis_rate:.1f}%")
                with col4:
                    anos_rate = (df.iloc[:, 8].sum()) / len(df) * 100
                    st.metric("Anosmie", f"{anos_rate:.1f}%")
                
                st.divider()
                
                st.subheader("Heatmap : Comorbidités")
                
                # Prendre les colonnes numériques (exclure la dernière qui est le diagnostic)
                df_numeric = df.iloc[:, 1:11].copy()
                df_numeric.columns = ['Age', 'Sexe', 'Tabac', 'Alcool', 'Obstruction', 
                                     'Rhinorrhée', 'Épistaxis', 'Anosmie', 'Polypose', 'Douleur']
                
                fig, ax = plt.subplots(figsize=(12, 8))
                
                corr_matrix = df_numeric.corr()
                sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', ax=ax, 
                           cbar_kws={'label': 'Corrélation'}, square=True)
                ax.set_title("Matrice de corrélation des facteurs ORL")
                st.pyplot(fig)
                
                st.divider()
                st.subheader("Diagnostics principaux")
                
                diagnostic_counts = df.iloc[:, -1].value_counts().head(10)
                fig, ax = plt.subplots(figsize=(10, 6))
                diagnostic_counts.plot(kind='barh', ax=ax, color='steelblue')
                ax.set_xlabel("Nombre de cas")
                ax.set_title("Top 10 des diagnostics")
                ax.grid(alpha=0.3)
                st.pyplot(fig)
            else:
                st.info("Aucune donnée disponible")
        else:
            st.warning("Erreur lors de la récupération des données")
    except Exception as e:
        st.warning(f"Erreur API: {str(e)}")
