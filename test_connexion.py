import mariadb
import pandas as pd

try:
    conn = mariadb.connect(
        host="localhost",
        user="root",
        password="root123",
        database="orl_ia"
    )

    cur = conn.cursor()
    cur.execute("SELECT * FROM patients")
    rows = cur.fetchall()

    df = pd.DataFrame(rows, columns=["id", "nom", "age", "diagnostic"])
    print("CONNEXION OK ✔")
    print(df)

    conn.close()

except Exception as e:
    print("ERREUR :", e)