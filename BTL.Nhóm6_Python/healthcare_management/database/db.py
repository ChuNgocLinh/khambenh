import logging
from config import DB_TYPE, get_connection_string

# Nếu dùng mysql, import thư viện tương ứng
if DB_TYPE == "mysql":
    try:
        import mysql.connector
    except ImportError:
        logging.error("❌ Thư viện mysql-connector-python chưa được cài đặt!")
else:
    import pyodbc

logging.basicConfig(level=logging.INFO)

# ================================
# 🔌 CONNECT DATABASE
# ================================
def connect():
    try:
        if DB_TYPE == "mysql":
            conn_config = get_connection_string()
            conn = mysql.connector.connect(**conn_config)
            return conn
        else:
            # SQL Server connection
            conn = pyodbc.connect(
                get_connection_string(),
                timeout=5
            )
            return conn
    except Exception as e:
        logging.error(f"❌ Lỗi kết nối {DB_TYPE}: {e}")
        return None

# ================================
# 📌 GET CURSOR
# ================================
def get_cursor():
    conn = connect()
    if conn:
        return conn.cursor(), conn
    raise Exception(f"❌ Không thể kết nối database {DB_TYPE}")

# ================================
# 📥 SELECT DATA (LIST)
# ================================
def fetch_all(query, params=()):
    cursor, conn = get_cursor()
    try:
        # MySQL dùng %s, SQL Server dùng ?
        formatted_query = query.replace('?', '%s') if DB_TYPE == "mysql" else query
        cursor.execute(formatted_query, params)
        
        # MySQL connector trả về cursor.description khác với pyodbc
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return result
    except Exception as e:
        logging.error(f"❌ Lỗi fetch_all: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

# ================================
# 📥 SELECT ONE DATA
# ================================
def fetch_one(query, params=()):
    cursor, conn = get_cursor()
    try:
        formatted_query = query.replace('?', '%s') if DB_TYPE == "mysql" else query
        cursor.execute(formatted_query, params)
        
        row = cursor.fetchone()
        if row:
            columns = [col[0] for col in cursor.description]
            return dict(zip(columns, row))
        return None
    except Exception as e:
        logging.error(f"❌ Lỗi fetch_one: {e}")
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
        formatted_query = query.replace('?', '%s') if DB_TYPE == "mysql" else query
        cursor.execute(formatted_query, params)
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        logging.error(f"❌ Lỗi execute: {e}")
        return False
    finally:
        cursor.close()
        conn.close()
