# 🏥 ORL IA Platform - Plateforme d'Intelligence Artificielle en ORL

Plateforme complète de diagnostic assisté par IA pour les pathologies ORL rhinologiques, utilisant Docker, MariaDB, Machine Learning et une interface web interactive.

## 📋 Table des matières

- [Vue d'ensemble](#vue-densemble)
- [Architecture](#architecture)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Structure du projet](#structure-du-projet)
- [API Endpoints](#api-endpoints)
- [Modèle ML](#modèle-ml)
- [Dashboard](#dashboard)
- [Données](#données)
- [Troubleshooting](#troubleshooting)
- [Auteur](#auteur)

---

## 🎯 Vue d'ensemble

**ORL IA Platform** est une application web qui fournit :

1. **Prédiction diagnostique** : Utilise un modèle RandomForest entraîné pour prédire les diagnostics ORL basés sur 10 paramètres cliniques
2. **Gestion des données** : Base de données MariaDB avec 33 patients et leurs caractéristiques
3. **Dashboard interactif** : Interface Streamlit pour la prédiction et l'analyse statistique
4. **API REST** : Backend FastAPI pour les prédictions et récupération des données

### Fonctionnalités principales

- ✅ Formulaire de saisie avec 10 paramètres cliniques
- ✅ Prédiction instantanée du diagnostic
- ✅ Statistiques complètes (âge, sexe, facteurs de risque)
- ✅ Visualisations graphiques (histogrammes, camemberts, heatmaps)
- ✅ Matrice de corrélation des comorbidités
- ✅ Entièrement containerisée avec Docker

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Navigateur Web                            │
│              http://localhost:8502                          │
└────────────────────┬────────────────────────────────────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
    ┌────▼────────┐      ┌──────▼──────┐
    │  Dashboard  │      │   API ORL   │
    │ (Streamlit) │      │  (FastAPI)  │
    │  :8502      │      │   :8000     │
    └────┬────────┘      └──────┬──────┘
         │                      │
         │         ┌────────────┴─────────────┐
         │         │                         │
    ┌────▼─────────▼───┐          ┌──────────▼─────┐
    │   MariaDB        │          │  RandomForest  │
    │   (3307)         │          │    Model       │
    │  33 patients     │          │  (model_orl.pkl)│
    │                  │          │  (encoder_orl.pkl)
    └──────────────────┘          └────────────────┘
```

### Conteneurs Docker

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `orl_mariadb` | `mariadb:11.4` | 3307 | Base de données patients |
| `api_orl` | Custom | 8002 | API FastAPI pour prédictions |
| `dashboard_global` | Custom | 8502 | Dashboard Streamlit |
| `oracle_db` | `gvenzl/oracle-xe:21-slim` | 1523 | Oracle (optionnel) |
| `api_oracle` | Custom | 8001 | API Oracle (optionnel) |

---

## 📦 Prérequis

- **Docker** (v20.10+) et **Docker Compose** (v1.29+)
- **Git**
- **Python** 3.11 (pour l'entraînement du modèle localement)
- **Ports disponibles** : 3307, 8000, 8001, 8002, 8501, 8502, 1522, 1523

### Vérification

```bash
docker --version
docker-compose --version
git --version
```

---

## 🚀 Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/diallobaykarim-glitch/MariaDB_bkdkmceven29mai2026.git
cd MariaDB_bkdkmceven29mai2026
```

### 2. Démarrer les conteneurs

```bash
docker-compose up -d --build
```

Cela va :
- Construire les images Docker
- Lancer les 5 conteneurs (MariaDB, API ORL, Dashboard, Oracle DB, API Oracle)
- Initialiser la base de données avec 33 patients
- Exposer les services sur les ports configurés

Vérifiez que tout fonctionne :

```bash
docker-compose ps
```

### 3. Accéder à l'application

- **Dashboard** : http://localhost:8502
- **API ORL Docs** : http://localhost:8002/docs
- **API Oracle Docs** : http://localhost:8001/docs
- **MariaDB** : localhost:3307 (user: root, password: root123)

---

## 📖 Utilisation

### Démarrage rapide

```bash
cd C:\Users\UTILISATEUR\Documents\MariaDB_bkdkmCeven29mai2026

# Démarrer
docker-compose up -d

# Accéder au dashboard
start http://localhost:8502

# Arrêter
docker-compose down
```

### Faire une prédiction

1. Accédez à http://localhost:8502
2. Allez à l'onglet **"ORL Prediction"**
3. Remplissez les 10 paramètres :
   - Âge (0-120)
   - Sexe (Femme/Homme)
   - Tabac (Oui/Non)
   - Alcool (Oui/Non)
   - Obstruction nasale (Oui/Non)
   - Rhinorrhée (Oui/Non)
   - Épistaxis (Oui/Non)
   - Anosmie (Oui/Non)
   - Polypose nasale (Oui/Non)
   - Douleur faciale (Oui/Non)
4. Cliquez **"Predict ORL"**
5. Consultez le diagnostic prédis

### Explorer les statistiques

- **Onglet "Statistics"** : Visualisation de la distribution des 33 patients
  - Nombre total, âge moyen, répartition sexe
  - Histogramme d'âge
  - Camembert sexe
  - Facteurs de risque (tabac, alcool, polypose)

- **Onglet "Analytics"** : Analyses avancées
  - Corrélations entre signes cliniques
  - Heatmap des comorbidités
  - Top 10 des diagnostics

---

## 📁 Structure du projet

```
MariaDB_bkdkmceven29mai2026/
├── docker-compose.yml              # Configuration Docker multi-conteneurs
├── requirements.txt                # Dépendances Python (host)
├── train_model.py                  # Script d'entraînement du modèle ML
├── model_orl.pkl                   # Modèle RandomForest sérialisé
├── encoder_orl.pkl                 # Encodeur LabelEncoder sérialisé
│
├── api_orl/                        # API FastAPI ORL
│   ├── Dockerfile                  # Image Docker pour l'API
│   ├── main.py                     # Code FastAPI
│   ├── requirements.txt            # Dépendances API
│   ├── model_orl.pkl              # Modèle (copie)
│   └── encoder_orl.pkl            # Encodeur (copie)
│
├── streamlit_app/                  # Dashboard Streamlit
│   ├── Dockerfile                  # Image Docker pour le dashboard
│   ├── app.py                      # Code Streamlit (3 onglets)
│   ├── requirements.txt            # Dépendances dashboard
│   └── .streamlit/
│       └── config.toml            # Configuration Streamlit
│
├── db_orl/                         # Initialisation MariaDB
│   └── init.sql                    # Schéma et 33 patients
│
├── api_oracle/                     # API FastAPI Oracle (optionnel)
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
│
└── .gitignore                      # Fichiers à ignorer dans Git
```

---

## 🔌 API Endpoints

### API ORL (http://localhost:8002)

#### GET /patients
Récupère tous les patients

```bash
curl http://localhost:8002/patients
```

**Réponse** (tuples) :
```
[[1, 45, 1, 1, 0, 1, 0, 1, 0, 0, 'Allergie naso-sinusienne', ...], ...]
```

#### POST /predict
Prédiction diagnostique

```bash
curl -X POST http://localhost:8002/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 45,
    "sexe": 1,
    "tabac": 1,
    "alcool": 0,
    "obstruction_nasale": 1,
    "rhinorrhee": 0,
    "epistaxis": 0,
    "anosmie": 1,
    "polypose_nasale": 0,
    "douleur_faciale": 0
  }'
```

**Réponse** :
```json
{"prediction": "Allergie naso-sinusienne"}
```

#### GET /docs
Documentation Swagger interactive

---

## 🤖 Modèle ML

### Caractéristiques du modèle

| Paramètre | Type | Ensemble d'entraînement |
|-----------|------|------------------------|
| Modèle | RandomForestClassifier | 100 arbres, max_depth=10 |
| Données | 33 patients | 10 features, 10 diagnostics |
| Accuracy | ~98% | Sur l'ensemble d'entraînement |
| Format | Joblib pickle | model_orl.pkl + encoder_orl.pkl |

### Entraînement du modèle

Pour réentraîner le modèle :

```bash
cd C:\Users\UTILISATEUR\Documents\MariaDB_bkdkmceven29mai2026
python train_model.py
```

Cela génère :
- `model_orl.pkl` : Modèle RandomForest
- `encoder_orl.pkl` : Encodeur LabelEncoder pour les diagnostics

Puis redémarrez l'API :

```bash
docker-compose restart api_orl
```

### Classes diagnostiques

```
['Allergie', 'Cancer etmoïde', 'Cancer nasal', 'Cancer sinusal', 
 'Déviation', 'Polyadénome', 'Polypose', 'Rhinite', 'Sinusite', 
 'Sinusite polypose']
```

---

## 💻 Dashboard

### Onglet 1 : ORL Prediction

- Formulaire interactif avec 10 paramètres cliniques
- Bouton "Predict ORL"
- Affichage du diagnostic prédis avec succès/erreur

### Onglet 2 : Statistics (Statistiques ORL)

Affiche :
- **4 métriques clés** : Total patients, Âge moyen, Hommes, Femmes
- **Histogramme** : Distribution d'âge
- **Camembert** : Répartition sexe (Femme/Homme)
- **Facteurs de risque** : Tabac, Alcool, Polypose nasale (en %)

### Onglet 3 : Analytics (Analyses avancées)

Affiche :
- **4 métriques** : Taux d'obstruction, rhinorrhée, épistaxis, anosmie
- **Heatmap de corrélation** : Matrice 10x10 des corrélations entre features
- **Top 10 diagnostics** : Graphique en barres horizontales des diagnostics les plus fréquents

---

## 📊 Données

### Base de données

**Schéma** (`db_orl/init.sql`) :

```sql
CREATE TABLE patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    age INT,
    sexe INT,                -- 0=Femme, 1=Homme
    tabac INT,               -- 0=Non, 1=Oui
    alcool INT,              -- 0=Non, 1=Oui
    obstruction_nasale INT,  -- 0=Non, 1=Oui
    rhinorrhee INT,          -- 0=Non, 1=Oui
    epistaxis INT,           -- 0=Non, 1=Oui
    anosmie INT,             -- 0=Non, 1=Oui
    polypose_nasale INT,     -- 0=Non, 1=Oui
    douleur_faciale INT,     -- 0=Non, 1=Oui
    cancer VARCHAR(255),     -- Diagnostic
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Accès à la base de données

```bash
# Via MariaDB CLI
docker exec -it orl_mariadb mysql -u root -proot123 orl_ia

# Requête exemple
SELECT id, age, sexe, cancer FROM patients LIMIT 10;
```

### Import/Export de données

```bash
# Export
docker exec orl_mariadb mysqldump -u root -proot123 orl_ia > backup.sql

# Import
docker exec -i orl_mariadb mysql -u root -proot123 orl_ia < backup.sql
```

---

## 🔧 Commandes Docker

### Démarrage/Arrêt

```bash
# Démarrer tous les conteneurs
docker-compose up -d

# Arrêter tous les conteneurs
docker-compose down

# Arrêter et supprimer les volumes
docker-compose down -v

# Reconstruire les images
docker-compose up -d --build
```

### Gestion des conteneurs

```bash
# Voir l'état
docker-compose ps

# Voir les logs
docker-compose logs -f api_orl
docker-compose logs -f dashboard_global

# Redémarrer un service
docker-compose restart api_orl

# Exécuter une commande dans un conteneur
docker exec -it orl_mariadb bash
```

### Nettoyage

```bash
# Supprimer les conteneurs arrêtés
docker container prune

# Supprimer les images non utilisées
docker image prune

# Supprimer les volumes non utilisés
docker volume prune

# Espace utilisé
docker system df
```

---

## 📱 Fichiers de configuration

### docker-compose.yml

Configure 5 services :
- **orl_mariadb** : Base de données (port 3307)
- **api_orl** : API FastAPI (port 8002)
- **dashboard_global** : Dashboard Streamlit (port 8502)
- **oracle_db** : Oracle XE (port 1523, optionnel)
- **api_oracle** : API Oracle (port 8001, optionnel)

Chaque service a :
- Build personnalisé (Dockerfile)
- Variables d'environnement (.env)
- Port bindings
- Volumes persistants
- Healthchecks

### .env

```
DB_USER=root
DB_PASSWORD=root123
DB_HOST=orl_mariadb
DB_PORT=3306
DB_NAME=orl_ia
```

### Dockerfile (API)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 🆘 Troubleshooting

### Erreur : "Port already in use"

```bash
# Identifier le processus
netstat -ano | findstr :8502

# Arrêter les conteneurs
docker-compose down

# Lancer sur un port différent (modifier docker-compose.yml)
# Puis relancer
docker-compose up -d
```

### Erreur : "Connection refused"

```bash
# Vérifier que tous les conteneurs tournent
docker-compose ps

# Vérifier les logs
docker-compose logs

# Attendre 10-15s au démarrage (temps d'initialisation MariaDB/Oracle)
```

### Erreur : "ModuleNotFoundError"

```bash
# Reconstruire
docker-compose down
docker-compose up -d --build
```

### Dashboard blanc ou erreur d'affichage

```bash
# Vider le cache navigateur (Ctrl+Shift+Delete)
# Ou accéder en mode incognito
# Ou relancer le dashboard
docker-compose restart dashboard_global
```

### Modèle : "JSONDecodeError" ou "500 Internal Server Error"

```bash
# Vérifier que model_orl.pkl existe
docker exec api_orl ls -la model_orl.pkl

# Relancer l'API
docker-compose restart api_orl

# Vérifier les logs
docker-compose logs api_orl
```

---

## 🚀 Déploiement

### Sur une machine de production

1. **Cloner le dépôt**
   ```bash
   git clone https://github.com/diallobaykarim-glitch/MariaDB_bkdkmceven29mai2026.git
   cd MariaDB_bkdkmceven29mai2026
   ```

2. **Configurer l'environnement**
   ```bash
   # Modifier .env avec les valeurs de production
   nano .env
   ```

3. **Lancer les conteneurs**
   ```bash
   docker-compose up -d --build
   ```

4. **Configurer un reverse proxy** (Nginx/Apache)
   ```nginx
   server {
       listen 80;
       server_name example.com;

       location / {
           proxy_pass http://localhost:8502;
       }
   }
   ```

5. **Sauvegarder les données**
   ```bash
   # Backup régulier
   docker exec orl_mariadb mysqldump -u root -proot123 orl_ia > /backup/orl_ia_$(date +%Y%m%d).sql
   ```

---

## 📈 Améliorations futures

- [ ] Augmenter le dataset à 1000+ patients
- [ ] Utiliser des algorithmes avancés (XGBoost, LightGBM)
- [ ] Ajouter la validation croisée et les métriques d'évaluation
- [ ] Intégrer des images médicales (CT, IRM)
- [ ] Système d'authentification utilisateur
- [ ] Export PDF des rapports diagnostiques
- [ ] API publique avec authentification OAuth2
- [ ] Monitoring et alertes (Prometheus/Grafana)
- [ ] Tests unitaires et intégration continue (CI/CD)
- [ ] Documentation OpenAPI complète

---

## 📝 License

Ce projet est fourni à titre éducatif.

---

## 👨‍💻 Auteur

**Diallo Bakarim**
- GitHub : https://github.com/diallobaykarim-glitch
- Projet : ORL IA Platform
- Date : 2026

---

## 🔗 Ressources

- **Docker** : https://docs.docker.com/
- **Streamlit** : https://streamlit.io/
- **FastAPI** : https://fastapi.tiangolo.com/
- **MariaDB** : https://mariadb.org/
- **Scikit-learn** : https://scikit-learn.org/
- **Pandas** : https://pandas.pydata.org/

---

## 📧 Support

Pour les questions ou problèmes, créez une issue sur GitHub : https://github.com/diallobaykarim-glitch/MariaDB_bkdkmceven29mai2026/issues

---

**Dernière mise à jour** : 30 mai 2026
