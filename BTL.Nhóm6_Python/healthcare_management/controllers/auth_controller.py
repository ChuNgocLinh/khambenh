from models.user_model import UserModel  # pyright: ignore[reportImplicitRelativeImport]

class AuthController:

    @staticmethod
    def login(username, password):
        user = UserModel.login(username, password)

        if user:
            role = UserModel.resolve_login_role(user.get("role"), user.get("username") or "")
            user["role"] = role
            return {
                "status": True,
                "user": user,
                "role": role
            }
        return {
            "status": False,
            "message": "Sai tài khoản hoặc mật khẩu"
        }

    @staticmethod
    def register(username, password, name, phone, email):
        success, message = UserModel.register_patient(username, password, name, phone, email)
        return {
            "status": success,
            "message": message
        }
