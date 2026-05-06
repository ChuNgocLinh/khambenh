import pyodbc
import logging
from config import get_connection_string

logging.basicConfig(level=logging.INFO)


# ================================
# 🔌 CONNECT DATABASE
# ================================
def connect():
    try:
        conn = pyodbc.connect(
            get_connection_string(),
            timeout=5  # 🔥 tránh treo khi deploy
        )
        return conn
    except Exception as e:
        logging.error(f"❌ Lỗi kết nối SQL Server: {e}")
        return None


# ================================
# 📌 GET CURSOR
# ================================
def get_cursor():
    conn = connect()
    if conn:
        return conn.cursor(), conn
    raise Exception("❌ Không thể kết nối database")


# ================================
# 📥 SELECT DATA (LIST)
# ================================
def fetch_all(query, params=()):
    cursor, conn = get_cursor()
    try:
        cursor.execute(query, params)

        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return result

    except Exception as e:
        logging.error(f"❌ Lỗi fetch_all: {e} | Query: {query}")
        return []

    finally:
        cursor.close()
        conn.close()


# ================================
# 📥 SELECT 1 ROW
# ================================
def fetch_one(query, params=()):
    cursor, conn = get_cursor()
    try:
        cursor.execute(query, params)

        row = cursor.fetchone()
        if row:
            columns = [col[0] for col in cursor.description]
            return dict(zip(columns, row))

        return None

    except Exception as e:
        logging.error(f"❌ Lỗi fetch_one: {e} | Query: {query}")
        return None

    finally:
        cursor.close()
        conn.close()


# ================================
# 📤 INSERT / UPDATE / DELETE
# ================================
def execute(query, params=()):
    cursor, conn = get_cursor()
    try:
        cursor.execute(query, params)
        conn.commit()
        return True

    except Exception as e:
        conn.rollback()
        logging.error(f"❌ Lỗi execute: {e} | Query: {query}")
        return False

    finally:
        cursor.close()
        conn.close()


# ================================
# 📦 EXECUTE MANY (BATCH INSERT)
# ================================
def execute_many(query, data_list):
    cursor, conn = get_cursor()
    try:
        cursor.fast_executemany = True
        cursor.executemany(query, data_list)
        conn.commit()
        return True

    except Exception as e:
        conn.rollback()
        logging.error(f"❌ Lỗi batch insert: {e}")
        return False

    finally:
        cursor.close()
        conn.close()


# ================================
# 🔍 TEST CONNECTION
# ================================
if __name__ == "__main__":
    conn = connect()
    if conn:
        print("✅ Kết nối DB thành công!")
        conn.close()