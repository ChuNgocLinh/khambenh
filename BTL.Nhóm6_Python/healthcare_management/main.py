# pyright: reportMissingImports=false
import sys
from pathlib import Path


def _bootstrap_import_paths():
    """Normalize sys.path so mixed absolute imports resolve from entry script."""
    current_dir = Path(__file__).resolve().parent
    package_root = current_dir.parent

    for path in (package_root, current_dir):
        path_str = str(path)
        if path_str not in sys.path:
            sys.path.insert(0, path_str)


_bootstrap_import_paths()

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QColor, QPalette
from views.login_view import LoginView  # pyright: ignore[reportImplicitRelativeImport]


def _apply_accessible_text_theme(app):
    """Apply a light-theme text palette to prevent low-contrast white text."""
    palette = app.palette()
    readable_text = QColor("#1f2937")
    muted_text = QColor("#64748b")
    white_background = QColor("#ffffff")

    palette.setColor(QPalette.ColorRole.Text, readable_text)
    palette.setColor(QPalette.ColorRole.WindowText, readable_text)
    palette.setColor(QPalette.ColorRole.ButtonText, readable_text)
    palette.setColor(QPalette.ColorRole.Base, white_background)
    palette.setColor(QPalette.ColorRole.PlaceholderText, muted_text)
    app.setPalette(palette)

    app.setStyleSheet(
        """
        QLineEdit, QComboBox, QDateEdit {
            color: #1f2937;
            background: #ffffff;
        }
        QLineEdit:disabled, QComboBox:disabled, QDateEdit:disabled {
            color: #64748b;
            background: #f8fafc;
            border-color: #e2e8f0;
        }
        QTableWidget {
            color: #1f2937;
            background: #ffffff;
        }
        QTableWidget::item:selected {
            background: #e2f3ee;
        }
        QHeaderView::section {
            color: #334155;
        }
        """
    )


def main():
    # 1. Khởi tạo ứng dụng PyQt6
    app = QApplication(sys.argv)
    _apply_accessible_text_theme(app)

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
