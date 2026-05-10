import json
import mysql.connector
from healthcare_management.config import get_connection_string

cfg = get_connection_string()
root = mysql.connector.connect(**cfg)
cur = root.cursor()
tmp_db = "HealthcareDB_task1_tmp"
cur.execute(f"DROP DATABASE IF EXISTS {tmp_db}")
cur.execute(f"CREATE DATABASE {tmp_db}")
root.commit()
cur.close()
root.close()

cfg2 = dict(cfg)
cfg2["database"] = tmp_db
conn = mysql.connector.connect(**cfg2)
cur = conn.cursor()

sql = open("BTL.Nhóm6_Python/healthcare_management/database/init_db.sql", encoding="utf-8").read()
parts = [p.strip() for p in sql.split(";") if p.strip() and not p.strip().startswith("--")]

ok = 0
fail = 0
errs = []
for p in parts:
    try:
        cur.execute(p)
        ok += 1
    except Exception as e:
        fail += 1
        errs.append(str(e))
conn.commit()

q = (
    "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS "
    "WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s "
    "AND COLUMN_NAME IN (%s,%s,%s,%s,%s)"
)
cur.execute(q, (tmp_db, "Patients", "cccd", "email", "occupation", "intake_notes", "patient_type"))
cols = [r[0] for r in cur.fetchall()]

cur.execute(
    "SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s",
    (tmp_db, "WaitingQueue"),
)
wq = cur.fetchone()[0]

print("TMP_DB=" + tmp_db)
print("STATEMENTS_OK=" + str(ok))
print("STATEMENTS_FAIL=" + str(fail))
print("FIRST_ERROR=" + (errs[0] if errs else "NONE"))
print("PATIENT_COLS=" + json.dumps(cols, ensure_ascii=False))
print("WAITINGQUEUE_EXISTS=" + str(wq))

cur.close()
conn.close()
