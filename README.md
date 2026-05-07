# Hệ thống Quản lý Khám bệnh (Healthcare Management System)

Dự án quản lý chăm sóc sức khỏe sử dụng kiến trúc MVC bằng Python (PyQt6) và cơ sở dữ liệu MySQL.

## 📋 Yêu cầu hệ thống
- Python 3.x
- Docker & Docker Compose (để chạy cơ sở dữ liệu MySQL)
- Cài đặt các thư viện Python (được cấu hình trong `requirements.txt`)

## 🚀 Cách chạy dự án

### 1. Khởi tạo Cơ sở dữ liệu (Database)
Dự án hiện tại sử dụng MySQL làm hệ quản trị cơ sở dữ liệu. Bạn có thể nhanh chóng thiết lập database bằng Docker thông qua lệnh sau ở thư mục gốc:

```bash
docker compose up -d
```

*Lưu ý: Lệnh này sẽ tự động tải MySQL 8.0, cấu hình chạy trên cổng **3307**, tự động khởi tạo các bảng và nạp sẵn dữ liệu mẫu từ tệp `BTL.Nhóm6_Python/healthcare_management/database/init_db.sql`.*

### 2. Thiết lập Môi trường (.env)
File `.env` nằm ở thư mục gốc chứa các thông số kết nối Database. Mặc định dự án đã được cấu hình chuẩn xác để kết nối với container Docker phía trên:

```env
DB_TYPE=mysql
DB_SERVER=localhost
DB_NAME=HealthcareDB
DB_PORT=3307
DB_USER=root
DB_PASSWORD=your_password
```

*(Bạn cũng có thể thay đổi các thông số này và kết nối dự án vào Database MySQL trên máy cục bộ của bạn bằng MySQL Workbench nếu muốn).*

### 3. Cài đặt Thư viện Python
Từ thư mục gốc (chứa file `requirements.txt`), tiến hành cài đặt các thư viện cần thiết:

```bash
pip install -r requirements.txt
```

*(Các thư viện chính bao gồm: `PyQt6` cho giao diện Desktop, `mysql-connector-python` để kết nối DB và `python-dotenv` để đọc cấu hình).*

### 4. Chạy Ứng dụng
Để chạy ứng dụng, bạn cần di chuyển vào thư mục mã nguồn chính và chạy file `main.py`:

```bash
cd BTL.Nhóm6_Python/healthcare_management
python3 main.py
```

## 🔐 Tài khoản mẫu để Đăng nhập
Sau khi giao diện CarePlus hiện lên, bạn có thể kiểm tra với các tài khoản được seed mặc định sau (mật khẩu chung cho tất cả là: `123456`):

- **Quản trị viên (Admin)**: `admin`
- **Bác sĩ (Doctor)**: `doctor1`
- **Bệnh nhân (Patient)**: `staff1`

## 📁 Cấu trúc nổi bật
- `BTL.Nhóm6_Python/healthcare_management/`: Chứa mã nguồn giao diện (Views), xử lý (Controllers), mô hình dữ liệu (Models) và thiết lập cơ sở dữ liệu.
- `docker-compose.yml`: Hỗ trợ tự động hóa việc khởi tạo database MySQL.
- `requirements.txt`: Chứa danh sách các gói thư viện Python cần thiết.
