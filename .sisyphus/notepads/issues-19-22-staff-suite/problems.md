
## 2026-05-11 - Final review residual risks

- `login_view.py` vẫn nạp ảnh nền bằng đường dẫn tương đối `healthcare_management/assets/bg.jpg`; khi chạy từ repo root có thể tạo `QPixmap::scaled: Pixmap is a null pixmap`. Hiện chưa chặn login hay staff dashboard, nhưng là brittle asset-path cho manual desktop smoke.
- Repo vẫn phụ thuộc mạnh vào implicit imports (`from controllers...`, `from models...`) và runtime bootstrap path trong `main.py`; điều này đủ cho entry hiện tại nhưng còn mong manh nếu module bị import theo package path khác hoặc chạy từ tool/test harness khác.
