from database.db import fetch_all, execute
from models.user_model import UserModel

def migrate_passwords():
    users = fetch_all("SELECT user_id, password FROM Users")
    for u in users:
        uid = u["user_id"] if isinstance(u, dict) else u[0]
        pwd = u["password"] if isinstance(u, dict) else u[1]
        
        # Check if already hashed (length 64)
        if len(str(pwd)) != 64:
            hashed = UserModel.hash_password(str(pwd))
            execute("UPDATE Users SET password=? WHERE user_id=?", (hashed, uid))
            print(f"Updated password for user_id: {uid}")

if __name__ == "__main__":
    migrate_passwords()
    print("Password migration complete.")
