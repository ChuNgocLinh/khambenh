from models.user_model import UserModel

class AuthController:

    @staticmethod
    def login(username, password):
        user = UserModel.login(username, password)

        if user:
            return {
                "status": True,
                "user": user,
                "role": user["role"]
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