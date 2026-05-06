import sys
from PyQt6.QtWidgets import QApplication
from views.login_view import LoginView

def main():
    # 1. Khởi tạo ứng dụng PyQt6
    app = QApplication(sys.argv)

    # 2. Tạo cửa sổ login
    # Lưu ý: LoginView cần được gán vào một biến để tránh bị giải phóng bộ nhớ
    window = LoginView()

    # 3. Thiết lập thuộc tính cửa sổ (Giống Tkinter geometry/resizable)
    window.setWindowTitle("CarePlus - Healthcare Management System")
    
    # Đặt kích thước tối thiểu
    window.setMinimumSize(800, 500)
    
    # Nếu muốn cố định kích thước hoàn toàn (disable resize), dùng dòng dưới:
    # window.setFixedSize(900, 600)

    # 4. Hiển thị cửa sổ
    window.show()

    # 5. Vòng lặp chạy ứng dụng
    sys.exit(app.exec())

if __name__ == "__main__":
    main()