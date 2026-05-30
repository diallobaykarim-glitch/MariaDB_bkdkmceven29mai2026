from fastapi import FastAPI
import oracledb

app = FastAPI(title="ORACLE IA API")

def get_conn():
    return oracledb.connect(
        user="system",
        password="oracle",
        dsn="oracle-db:1521/XEPDB1"
    )

@app.get("/patients")
def patients():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM patients")
    rows = cur.fetchall()
    conn.close()
    return rows