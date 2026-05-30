import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import numpy as np

# Créer dataset d'entraînement avec 33 patients
data = {
    'age': [45, 52, 38, 61, 48, 73, 42, 55, 36, 67, 44, 58, 39, 70, 46, 53, 41, 65, 37, 59, 47, 72, 43, 56, 40, 68, 50, 35, 62, 45, 54, 49, 69],
    'sexe': [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0],
    'tabac': [1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    'alcool': [0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1],
    'obstruction_nasale': [1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0],
    'rhinorrhee': [0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1],
    'epistaxis': [0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1],
    'anosmie': [1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    'polypose_nasale': [0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1],
    'douleur_faciale': [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1],
    'diagnostic': ['Allergie', 'Polypose', 'Rhinite', 'Cancer sinusal', 'Polyadénome', 'Cancer nasal', 'Rhinite', 'Sinusite', 'Déviation', 'Cancer etmoïde',
                   'Polypose', 'Sinusite', 'Allergie', 'Cancer sinusal', 'Rhinite', 'Polypose', 'Sinusite', 'Cancer nasal', 'Rhinite', 'Sinusite polypose',
                   'Déviation', 'Cancer etmoïde', 'Allergie', 'Polypose', 'Sinusite', 'Cancer sinusal', 'Rhinite', 'Polypose', 'Sinusite', 'Allergie',
                   'Cancer nasal', 'Rhinite', 'Cancer etmoïde']
}

df = pd.DataFrame(data)

# Features et target
X = df.drop('diagnostic', axis=1)
y = df['diagnostic']

# Encoder les labels
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)

# Entraîner le modèle
model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
model.fit(X, y_encoded)

# Sauvegarder
joblib.dump(model, 'model_orl.pkl')
joblib.dump(encoder, 'encoder_orl.pkl')

print("✓ Modèle entraîné et sauvegardé")
print(f"Features: {X.shape[1]}")
print(f"Diagnostics: {list(encoder.classes_)}")
