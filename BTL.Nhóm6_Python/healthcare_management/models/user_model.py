from database.db import fetch_one


class UserModel:

    @staticmethod
    def login(username, password):
        # 🔥 CHỈ LẤY CÁC CỘT CẦN THIẾT (KHÔNG DÙNG *)
        query = "SELECT username, password, role FROM Users WHERE username=? AND password=?"

        row = fetch_one(query, (username, password))

        if not row:
            return None

        # 🔥 TRƯỜNG HỢP 1: fetch_one trả về tuple
        if isinstance(row, tuple):
            return {
                "username": row[0],
                "password": row[1],
                "role": row[2]
            }

        # 🔥 TRƯỜNG HỢP 2: fetch_one trả về dict
        if isinstance(row, dict):
            return {
                "username": row.get("username"),
                "password": row.get("password"),
                "role": row.get("role")
            }

        return None