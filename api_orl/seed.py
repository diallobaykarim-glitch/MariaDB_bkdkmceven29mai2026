import mariadb
import random

conn = mariadb.connect(
    host="localhost",
    port=3307,
    user="root",
    password="root123",
    database="orl_ia"
)

cur = conn.cursor()

cur.execute("DELETE FROM patients")

pathologies = [
    ("Cancer du cavum", 7),
    ("Cancer du sinus maxillaire", 5),
    ("Sinusite chronique", 53),
    ("Allergie naso-sinusienne", 55),
    ("Autre pathologie rhinologique", 9)
]

def generate_sex():
    return random.choice(["-M", "-F"])

def generate_age():
    return random.randint(5, 85)

data = []

for diag, count in pathologies:
    for _ in range(count):
        nom = f"Patient{random.randint(1000,9999)}{generate_sex()}"
        age = generate_age()

        data.append((nom, age, diag, 0, 0, 0, 0, 0))

cur.executemany("""
INSERT INTO patients
(nom, age, diagnostic,
obstruction_nasale, rhinorrhee, epistaxis, anosmie, tabac)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", data)

conn.commit()
conn.close()

print("129 patients ORL générés ✔")