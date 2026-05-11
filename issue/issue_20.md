Dưới đây là tài liệu đặc tả kỹ thuật (Technical Specification/Prompt) bằng Markdown, được thiết kế cực kỳ chi tiết về mặt kiến trúc, dữ liệu, bố cục UI/UX để AI Coding (các model xử lý text) có thể đọc hiểu và lập trình chính xác giao diện **Dịch vụ & Gói khám (Staff Mode)** bằng **Python (PyQt6)** mà không cần nhìn ảnh.

---

# ĐẶC TẢ GIAO DIỆN MÀN HÌNH "DỊCH VỤ & GÓI KHÁM" (STAFF MODE) - PyQt6

## 1. Tổng quan & Kiến trúc Layout (Layout Architecture)

Giao diện ứng dụng được chia làm 3 khu vực chính (Sử dụng `QHBoxLayout` làm layout tổng của toàn bộ cửa sổ):

1. **Left Sidebar (Bên trái):** Chiếm khoảng `15% - 20%` chiều rộng (Menu điều hướng).
2. **Main Content (Ở giữa):** Chiếm khoảng `50% - 55%` chiều rộng (Chứa thống kê, tab, bộ lọc và bảng danh sách).
3. **Right Detail Panel (Bên phải):** Chiếm khoảng `30%` chiều rộng (Hiển thị chi tiết dịch vụ/gói khám đang được select).

**Màu sắc chủ đạo (Theme):**

* Nền tổng thể: Trắng/Xám nhạt (`#F8F9FA`).
* Màu Primary (Thương hiệu): Xanh lá (`#00A86B` hoặc `#10B981`).
* Màu Text chính: Đen/Xám đậm (`#1F2937`).
* Màu Thống kê & Card: Sử dụng các tone màu pastel (Xanh lá nhạt, Xanh dương nhạt, Tím nhạt, Đỏ nhạt).

---

## 2. Chi tiết các thành phần (UI Components)

### 2.1. Left Sidebar (Menu Điều hướng)

Sử dụng `QVBoxLayout`, nền màu trắng `#FFFFFF`, có border-right mỏng màu xám.

* **Logo/Header:** Text **"+ CarePlus"** (chữ đậm, icon dấu cộng màu xanh lá, text màu xanh lá).
* **Danh sách Menu Items** (Sử dụng `QListWidget` hoặc các custom `QPushButton` dạng flat, text align left, icon bên trái):
* Dashboard
* Tiếp nhận bệnh nhân
* Quản lý lịch hẹn
* Danh sách bệnh nhân
* Thanh toán & Hóa đơn
* **Dịch vụ & Gói khám** (Trạng thái **Active**: Nền được highlight màu xanh lá nhạt `#E6F4EA`, text màu xanh lá đậm).
* Thông báo
* Báo cáo
* Cài đặt


* **Spacer:** Dùng `QSpacerItem` để đẩy nút Đăng xuất xuống dưới cùng.
* **Footer:** Nút **"Đăng xuất"** (Icon cửa thoát, text màu đỏ `#DC3545`).

---

### 2.2. Main Content (Khu vực Giữa - Quản lý Danh sách)

Sử dụng `QVBoxLayout` chứa các phần tử tuần tự từ trên xuống dưới:

#### a. Header

* **Title:** Label `"Dịch vụ & Gói khám"` (Font size to, Bold).
* **Breadcrumb:** Label `"Trang chủ > Dịch vụ & Gói khám"` (Màu xám nhạt).
* *(Góc phải trên cùng có thanh Topbar nhỏ chứa Icon Chuông thông báo (có badge 3) và Avatar + Tên nhân viên "Nguyễn Thị Lan").*

#### b. Các ô thống kê phía trên (Stats Overview Cards)

Sử dụng `QHBoxLayout` chứa 4 Card (Custom `QFrame` bo góc, nền trắng, border mỏng, có shadow nhẹ). Mỗi card dùng `QHBoxLayout` hoặc `QGridLayout` để chia icon bên trái, text bên phải:

1. **Tổng dịch vụ:** Icon màu tím nhạt. Label số: `"32"` (Bold, to, màu xanh dương đậm). Sub-label: `"Đang áp dụng"`.
2. **Gói khám:** Icon màu xanh dương nhạt. Label số: `"12"` (Bold, to, màu xanh dương đậm). Sub-label: `"Đang áp dụng"`.
3. **Dịch vụ nổi bật:** Icon màu đỏ/hồng nhạt. Label số: `"6"` (Bold, to, màu đỏ/hồng). Sub-label: `"Được quan tâm"`.
4. **Tổng doanh thu dịch vụ:** Icon hình giọt nước/tiền màu xanh dương. Label số: `"185.450.000 đ"` (Bold, to, màu tím đậm). Sub-label: `"Trong tháng 05"`.

#### c. Tabs Phân loại

Sử dụng `QHBoxLayout` (hoặc `QTabBar` flat) đặt sát lề trái:

* **Tab "Dịch vụ"** (Active): Text màu xanh lá, có đường underline màu xanh lá đậm bên dưới.
* **Tab "Gói khám"** (Inactive): Text màu xám.

#### d. Thanh tìm kiếm & Bộ lọc (Search & Filter Bar)

Sử dụng `QHBoxLayout`:

* **Search Input:** `QLineEdit` có placeholder *"Tìm kiếm dịch vụ..."*. Có icon kính lúp bên trong. Chiếm khoảng 40% chiều rộng.
* **Bộ lọc "Danh mục":** `QComboBox` với các options: *Tất cả danh mục (Default) / Khám bệnh / Xét nghiệm / Chẩn đoán hình ảnh*.
* **Bộ lọc "Trạng thái":** `QComboBox` với các options: *Tất cả (Default) / Đang áp dụng / Tạm ngưng*.
* **Spacer:** Thêm `QSpacerItem` nhỏ nếu cần.
* **Nút "Thêm dịch vụ":** `QPushButton` đặt ở góc phải, nền màu xanh lá `#10B981`, text trắng, icon dấu `+`. Mở ra Form nhập: Tên, Giá, Thời gian, Mô tả, Danh mục.

#### e. Bảng Danh sách dịch vụ (Data Table)

* **Header bảng:** Label `"Danh sách dịch vụ (32)"` (Hiển thị tổng số record hiện có).
* **Table:** Sử dụng `QTableWidget` hoặc `QTableView` (chế độ chỉ đọc/read-only, chọn nguyên dòng `SelectRows`).
* **Các cột (Columns):**
1. `STT` (Số thứ tự - Integer)
2. `Tên dịch vụ` (String, VD: `Khám tổng quát`, `Siêu âm tim`)
3. `Danh mục` (String, VD: `Khám bệnh`, `Khám chuyên khoa`, `Chẩn đoán hình ảnh`)
4. `Giá (đ)` (String/Integer format tiền tệ, VD: `300.000`)
5. `Thời gian` (String, VD: `30 phút`, `15 phút`)
6. `Trạng thái` (Custom Widget hiển thị dạng Badge/Pill bo góc):
* **Đang áp dụng:** Nền xanh lá nhạt, text xanh lá.
* **Ngưng áp dụng:** Nền đỏ/hồng nhạt, text đỏ.


7. `Thao tác` (Chứa 3 nút icon nhỏ dùng `QHBoxLayout` trong cell):
* Nút **Xem** (Icon mắt `👁️` màu xanh).
* Nút **Sửa** (Icon cây bút `✏️` màu xanh).
* Nút **Menu** (Icon 3 chấm dọc `⋮` màu xám).




* **Tính năng Table:** Khi click/select vào 1 dòng, trigger event để load toàn bộ thông tin chi tiết của dịch vụ đó sang **Right Detail Panel** bên phải.

#### f. Phân trang (Pagination)

Sử dụng `QHBoxLayout` ở dưới cùng bảng:

* Bên trái: Label + `QComboBox` `"Hiển thị [ 10 ] bản ghi"`.
* Bên phải: Các nút phân trang `<` `1` `2` `3` `4` `>`. Nút active (1) có nền xanh lá, text trắng.

---

### 2.3. Right Detail Panel (Khung Thông Tin Chi Tiết Dịch Vụ)

Sử dụng `QVBoxLayout`, nền trắng, có border bo góc mềm mại, hiển thị thông tin của dòng đang được chọn trong bảng. Dùng `QScrollArea` nếu nội dung quá dài.

#### a. Header Card (Thông tin cơ bản)

Dùng `QHBoxLayout` chứa Icon lớn và các Label:

* **Icon:** Một `QLabel` box vuông nền xanh lá nhạt, chứa icon bảng y tế màu xanh lá đậm.
* **Khung Text (Bên cạnh icon):**
* Sub-label: `"Tên dịch vụ"` (Màu xám nhỏ).
* Title: `"Khám tổng quát"` (Bold, size to).


* **Các thông tin dạng Form (Dưới Header):** Dùng `QVBoxLayout` chứa các cặp Label (Màu xám) - Value (Màu đen):
* `Danh mục:` Khám bệnh
* `Giá dịch vụ:` 300.000 đ
* `Thời gian:` 30 phút
* `Trạng thái:` Badge `"Đang áp dụng"` (Nền xanh lá nhạt).



#### b. Các vùng thông tin văn bản (Text Sections)

Sử dụng các `QVBoxLayout` nối tiếp nhau, các đoạn text dài dùng `QLabel` với thuộc tính `setWordWrap(True)`:

* **Mô tả:**
* Label Header: `"Mô tả"` (Bold).
* Content: *"Khám tổng quát toàn diện, kiểm tra sức khỏe tổng thể."*


* **Quy trình thực hiện:**
* Label Header: `"Quy trình thực hiện"` (Bold).
* Content (Dạng danh sách):
*"1. Đăng ký thông tin\n2. Khám lâm sàng\n3. Chỉ định cận lâm sàng (nếu cần)\n4. Bác sĩ tư vấn kết quả"*


* **Lưu ý:**
* Label Header: `"Lưu ý"` (Bold).
* Content: *"- Nhịn ăn sáng trước khi xét nghiệm (nếu có)\n- Mang theo giấy tờ tùy thân"*



#### c. Nhóm nút Hành động (Action Buttons)

Sử dụng `QHBoxLayout` chứa 2 nút:

* **Nút "Sửa dịch vụ":** `QPushButton`, nền trắng, border xanh dương mỏng, text xanh dương, icon cây bút.
* **Nút "Ngưng áp dụng":** `QPushButton`, nền trắng/đỏ nhạt, border đỏ, text đỏ, icon thùng rác hoặc nút pause.

#### d. Gợi ý Upsell ("Dịch vụ thường được chọn kèm")

Sử dụng `QVBoxLayout` ở dưới cùng:

* Label Header: `"Dịch vụ thường được chọn kèm"` (Bold).
* **Danh sách gợi ý:** Chứa các row (Dùng `QHBoxLayout`), mỗi row gồm:
* Checkbox (`QCheckBox`) đã checked mặc định màu xanh lá + Tên dịch vụ (VD: `"Xét nghiệm máu tổng quát"`).
* Label Giá ở sát lề phải (VD: `"180.000 đ"`).
*(Khu vực này hỗ trợ nhân viên tư vấn combo cho bệnh nhân).*



---

## 3. Workflow & Logic nghiệp vụ (Dành cho Coder)

* **Quyền hạn (Permissions):** Đây là màn hình dành cho **STAFF (Nhân viên)**. Nhân viên chỉ có quyền xem giá, tư vấn, thêm mới dịch vụ, sửa thông tin mô tả/giá, hoặc tạm ngưng dịch vụ. Các chức năng mang tính chuyên môn của Bác sĩ (Khám bệnh, Kê thuốc, Sửa kết quả khám) **KHÔNG** thuộc phạm vi màn hình này.
* **Data Binding Logic:**
* Cần chuẩn bị mock data khoảng 10-32 records mẫu cho dịch vụ trong Python (`List[Dict]`).
* Bắt buộc kết nối signal `itemSelectionChanged` của `QTableWidget` để cập nhật động toàn bộ text/giá/trạng thái/quy trình ở **Right Detail Panel** theo đúng dữ liệu của dịch vụ đang được click.


* **Responsive Layout:** Thiết lập `stretch factor` cho `QHBoxLayout` chính của ứng dụng. Ví dụ: `sidebar` (stretch 1), `main_content` (stretch 4), `detail_panel` (stretch 2) để đảm bảo khi co giãn cửa sổ, các ô thống kê và bảng không bị ép lún hoặc vỡ layout.