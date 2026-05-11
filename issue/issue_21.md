# Màn Hình "Thông Báo" – CarePlus STAFF (PyQt6)

---

## 1. Tổng quan màn hình

| Thuộc tính | Giá trị |
|---|---|
| Tên màn hình | Thông báo |
| Đối tượng | Nhân viên (Staff) |
| Mục đích | Hiển thị & xử lý toàn bộ thông báo hệ thống |
| Layout chính | 3 vùng: Sidebar trái · Nội dung giữa · Panel chi tiết phải |
| Màu nền tổng thể | `#F5F6FA` (xám nhạt) |
| Font chữ chính | Sans-serif (ví dụ: Segoe UI hoặc Inter) |

---

## 2. Cấu trúc layout tổng thể

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  TITLE BAR  (CarePlus – STAFF (Nhân viên))         [─] [□] [✕]             │
├──────────────┬──────────────────────────────────────────┬───────────────────┤
│              │  HEADER: "Thông báo"  +  Breadcrumb      │  🔔(3)  Avatar    │
│   SIDEBAR    ├──────────────────────────────────────────┴───────────────────┤
│   (trái)     │  STAT CARDS (4 ô)                                            │
│              ├──────────────────────────────────────────────────────────────┤
│              │  TABS + SEARCH BAR + FILTERS                                 │
│              ├──────────────────────────────────────────┬───────────────────┤
│              │  DANH SÁCH THÔNG BÁO                     │  PANEL CHI TIẾT  │
│              │  (danh sách cuộn)                        │  (bên phải)      │
│              │                                          │                   │
│              │                                          │                   │
│              ├──────────────────────────────────────────┴───────────────────┤
│              │  PAGINATION                                                   │
└──────────────┴──────────────────────────────────────────────────────────────┘
```

---

## 3. Title Bar (Thanh tiêu đề cửa sổ)

- **Nền:** `#1A1A2E` (xanh đen đậm)
- **Text trái:** `CarePlus – STAFF (Nhân viên)` – màu trắng, font size 13px
- **Icon trái:** Logo CarePlus (chữ thập xanh lá `#00B14F` trong hình tròn xanh nhạt) + chữ "CarePlus" màu xanh lá
- **Nút phải (hệ thống):** `[–]` `[□]` `[✕]` – các nút thu nhỏ/phóng to/đóng cửa sổ, màu trắng trên nền tối

---

## 4. Sidebar (Thanh điều hướng trái)

- **Chiều rộng:** ~200px
- **Nền:** `#FFFFFF` (trắng)
- **Viền phải:** border `1px solid #E8E8E8`

### 4.1 Logo (trên cùng sidebar)

- Icon hình tròn xanh nhạt chứa dấu `+` màu xanh lá `#00B14F`
- Chữ **"CarePlus"** màu xanh lá `#00B14F`, font-weight bold, size 18px
- Padding top: 20px, căn giữa theo chiều ngang

### 4.2 Menu điều hướng

Danh sách các mục menu theo thứ tự từ trên xuống:

| STT | Icon | Nhãn | Trạng thái |
|---|---|---|---|
| 1 | 🏠 (house) | Dashboard | Bình thường |
| 2 | 👤 (người + dấu +) | Tiếp nhận bệnh nhân | Bình thường |
| 3 | 📋 (lịch có kẻ ô) | Quản lý lịch hẹn | Bình thường |
| 4 | 👥 (2 người) | Danh sách bệnh nhân | Bình thường |
| 5 | 💳 (thẻ thanh toán) | Thanh toán & Hóa đơn | Bình thường |
| 6 | 🟩 (hộp xanh lá) | Dịch vụ & Gói khám | Bình thường |
| 7 | 🔔 (chuông) | **Thông báo** | **ĐANG ACTIVE** |
| 8 | 📊 (biểu đồ cột) | Báo cáo | Bình thường |
| 9 | ⚙️ (bánh răng) | Cài đặt | Bình thường |

**Mục đang active (Thông báo):**
- Nền: `#E8F5E9` (xanh lá cực nhạt)
- Text & icon: `#00B14F` (xanh lá đậm)
- Không có border-left indicator

**Mục bình thường:**
- Nền: trong suốt
- Text: `#555555`
- Icon: màu xám tương ứng theo từng mục

**Dưới cùng sidebar:**
- Icon 🚪 (cửa thoát) màu đỏ `#E53935`
- Chữ **"Đăng xuất"** màu đỏ `#E53935`

---

## 5. Header khu vực nội dung chính

Nằm phía trên bên phải sidebar, chiều cao ~60px:

```
[Thông báo]                                    [🔔 badge đỏ "3"]  [Avatar]  [Nguyễn Thị Lan ▼]
Trang chủ > Thông báo
```

- **"Thông báo":** font-size 22px, font-weight bold, màu `#1A1A2E`
- **Breadcrumb:** `Trang chủ > Thông báo` – font-size 13px, màu `#888888`; chữ "Trang chủ" có thể click (màu xanh nhạt)
- **Icon chuông 🔔:** góc trên phải, có badge đỏ tròn số `3` (thông báo chưa đọc), font-size badge 10px, nền `#E53935`
- **Avatar:** hình tròn ~36px, ảnh đại diện mặc định (icon người màu xám nền xanh nhạt)
- **Tên người dùng:** `Nguyễn Thị Lan` + mũi tên dropdown `▼`, màu `#333333`

---

## 6. Khu vực Stat Cards (4 ô thống kê)

Nằm dưới header, layout 4 cột ngang bằng nhau, nền trắng, bo góc 10px, padding 16px, shadow nhẹ.

### Card 1 – Tất cả thông báo

| Thuộc tính | Giá trị |
|---|---|
| Icon | 🔔 chuông màu xanh lá `#00B14F` trong hình tròn nền `#E8F5E9` |
| Nhãn nhỏ trên | `Tất cả thông báo` – font 12px, màu `#888` |
| Số lớn | **18** – font 28px bold, màu `#1A1A2E` |
| Nhãn nhỏ dưới | `Tất cả` – font 12px, màu `#888` |

### Card 2 – Lịch hẹn

| Thuộc tính | Giá trị |
|---|---|
| Icon | 📅 lịch màu xanh dương `#1976D2` trong hình tròn nền `#E3F2FD` |
| Nhãn nhỏ trên | `Lịch hẹn` |
| Số lớn | **7** – màu `#1976D2` |
| Nhãn nhỏ dưới | `Lịch hẹn` |

### Card 3 – Thanh toán

| Thuộc tính | Giá trị |
|---|---|
| Icon | 📄 hóa đơn màu cam `#F57C00` trong hình tròn nền `#FFF3E0` |
| Nhãn nhỏ trên | `Thanh toán` |
| Số lớn | **5** – màu `#F57C00` |
| Nhãn nhỏ dưới | `Thanh toán` |

### Card 4 – Hệ thống

| Thuộc tính | Giá trị |
|---|---|
| Icon | 🔔 chuông màu tím `#7B1FA2` trong hình tròn nền `#F3E5F5` |
| Nhãn nhỏ trên | `Hệ thống` |
| Số lớn | **6** – màu `#7B1FA2` |
| Nhãn nhỏ dưới | `Hệ thống` |

> **Ghi chú PyQt6:** Dùng `QFrame` + `QVBoxLayout` cho mỗi card. Số lớn dùng `QLabel` với stylesheet font-size lớn. Xếp 4 card bằng `QHBoxLayout`.

---

## 7. Tab Bar (Thanh tab lọc thông báo)

Nằm dưới stat cards, các tab nằm ngang:

```
[Tất cả]  [Chưa đọc (3)]  [Lịch hẹn]  [Thanh toán]  [Hệ thống]
```

| Tab | Nhãn hiển thị | Ghi chú |
|---|---|---|
| Tab 1 | `Tất cả` | Tab mặc định, **đang active** |
| Tab 2 | `Chưa đọc (3)` | Số trong ngoặc là số chưa đọc |
| Tab 3 | `Lịch hẹn` | |
| Tab 4 | `Thanh toán` | |
| Tab 5 | `Hệ thống` | |

**Tab đang active:**
- Chữ: `#00B14F` (xanh lá)
- Underline: border-bottom `2px solid #00B14F`
- Nền tab: trong suốt

**Tab bình thường:**
- Chữ: `#555555`
- Không có underline

> **PyQt6:** Dùng `QTabBar` tùy chỉnh hoặc `QPushButton` toggle group với stylesheet.

---

## 8. Thanh tìm kiếm & Bộ lọc

Nằm ngay dưới tab bar, layout ngang:

```
[🔍 Tìm kiếm thông báo...]  [Tất cả loại ▼]  [Tất cả thời gian 📅]  [✔ Đánh dấu đã đọc]
```

### 8.1 Ô tìm kiếm

- **Loại:** `QLineEdit`
- **Placeholder:** `Tìm kiếm thông báo...`
- **Icon:** 🔍 kính lúp bên trái trong ô input
- **Bo góc:** 6px
- **Viền:** `1px solid #E0E0E0`
- **Chiều rộng:** ~250px

### 8.2 Dropdown "Tất cả loại"

- **Loại:** `QComboBox`
- **Giá trị mặc định:** `Tất cả loại`
- **Các tùy chọn:** Tất cả loại / Lịch hẹn / Thanh toán / Hệ thống / Bệnh nhân
- **Bo góc:** 6px
- **Chiều rộng:** ~140px

### 8.3 Bộ lọc thời gian

- **Loại:** `QPushButton` hoặc `QDateEdit`
- **Nhãn:** `Tất cả thời gian`
- **Icon:** 📅 lịch bên phải
- **Bo góc:** 6px
- **Viền:** `1px solid #E0E0E0`

### 8.4 Nút "Đánh dấu đã đọc"

- **Loại:** `QPushButton`
- **Nhãn:** `✔ Đánh dấu đã đọc`
- **Màu chữ:** `#00B14F`
- **Nền:** trắng
- **Viền:** `1px solid #00B14F`
- **Bo góc:** 6px
- **Hover:** nền `#E8F5E9`

---

## 9. Khu vực nội dung chính (Danh sách + Chi tiết)

Chia làm 2 cột:

```
┌─────────────────────────────────┬──────────────────────┐
│  DANH SÁCH THÔNG BÁO (~65%)     │  CHI TIẾT (~35%)     │
└─────────────────────────────────┴──────────────────────┘
```

---

## 10. Danh Sách Thông Báo

### 10.1 Tiêu đề vùng danh sách

- Text: **`Danh sách thông báo (18)`** – font 14px bold, màu `#1A1A2E`

### 10.2 Mỗi dòng thông báo (Notification Item)

Mỗi item là một `QFrame` nằm trong `QScrollArea`, layout như sau:

```
┌──────────────────────────────────────────────────────────────────────┐
│  [ICON]   [TIÊU ĐỀ IN ĐẬM]                          [GIỜ/NGÀY]  [●] │
│           [Nội dung mô tả ngắn, màu xám]                             │
└──────────────────────────────────────────────────────────────────────┘
```

**Chi tiết từng phần:**

| Phần | Mô tả |
|---|---|
| **Icon trái** | Hình tròn ~36px, màu nền khác nhau theo loại (xem bảng bên dưới), chứa icon tương ứng |
| **Tiêu đề** | Font 13px bold, màu `#1A1A2E` |
| **Nội dung** | Font 12px, màu `#888888`, tối đa 1 dòng, truncate nếu dài |
| **Thời gian** | Căn phải, font 12px, màu `#AAAAAA`. Nếu hôm nay: hiển thị `HH:MM`. Nếu ngày khác: `DD/MM/YYYY` |
| **Chấm xanh** | Hình tròn `●` đường kính 8px, màu `#00B14F` – hiển thị khi **chưa đọc**. Ẩn đi khi đã đọc |

**Màu icon theo loại thông báo:**

| Loại | Màu nền icon | Màu icon | Icon |
|---|---|---|---|
| Lịch hẹn mới | `#E3F2FD` | `#1976D2` | 📅 lịch |
| Hóa đơn / Thanh toán | `#FFF3E0` | `#F57C00` | 📄 hóa đơn |
| Bệnh nhân | `#E8F5E9` | `#388E3C` | 👤 người |
| Hệ thống | `#F3E5F5` | `#7B1FA2` | ⚙️ / 🔔 |
| Kết quả xét nghiệm | `#E8F5E9` | `#388E3C` | 👤 người |

**Trạng thái item:**
- **Chưa đọc:** nền `#FFFFFF`, có chấm xanh `●`
- **Đang chọn:** nền `#F0FBF4` (xanh lá cực nhạt), viền trái `3px solid #00B14F`
- **Đã đọc:** nền `#FAFAFA`, không có chấm

**Hover:** nền `#F5F5F5`

### 10.3 Danh sách thông báo mẫu (dữ liệu demo)

| # | Icon | Tiêu đề | Nội dung | Thời gian | Trạng thái |
|---|---|---|---|---|---|
| 1 | 📅 xanh dương | Lịch hẹn mới | Bệnh nhân Trần Văn Nam đã đặt lịch khám vào 24/05/2026 08:30 với BS. Minh. | 09:15 | Chưa đọc ● |
| 2 | 📄 cam | Hóa đơn chờ thanh toán | Hóa đơn #HD000128 của bệnh nhân Nguyễn Văn Hùng trị giá 850.000đ đang chờ thanh toán. | 08:45 | Chưa đọc ● |
| 3 | 👤 xanh lá | Bệnh nhân đến sớm | Bệnh nhân Lê Thị Mai đã đến phòng khám lúc 07:50, sớm hơn lịch hẹn 10 phút. | 07:50 | Chưa đọc ● |
| 4 | 🔔 tím | Cập nhật hệ thống | Hệ thống sẽ bảo trì vào 25/05/2026 từ 22:00 đến 23:00. Vui lòng lưu ý! | 23/05/2026 | Chưa đọc ● |
| 5 | 📅 xanh dương | Nhắc lịch hẹn | Nhắc nhở: Bệnh nhân Phạm Minh Đức có lịch khám vào 23/05/2026 10:00. | 23/05/2026 | Chưa đọc ● |
| 6 | 👤 xanh lá | Kết quả xét nghiệm đã có | Kết quả xét nghiệm của bệnh nhân Hoàng Anh Tuấn đã có. Vui lòng kiểm tra. | 23/05/2026 | Chưa đọc ● |
| 7 | 📄 cam | Thanh toán thành công | Hóa đơn #HD000126 của bệnh nhân Lê Văn Nam đã được thanh toán thành công. | 23/05/2026 | Chưa đọc ● |
| 8 | 📅 xanh dương | Lịch hẹn đã được xác nhận | Lịch hẹn khám của bệnh nhân Vũ Thị Hương vào 24/05/2026 09:00 đã được xác nhận. | 22/05/2026 | Chưa đọc ● |

---

## 11. Pagination (Phân trang)

Nằm dưới danh sách, layout ngang:

```
Hiển thị [10 ▼] bản ghi          [<]  [1]  [2]  [>]
```

- **Dropdown số bản ghi:** `QComboBox` với các giá trị: 10, 20, 50
- **Nút trang:** `QPushButton` bo góc 6px
  - Trang hiện tại: nền `#00B14F`, chữ trắng
  - Trang khác: nền trắng, chữ `#555`
  - Nút `[<]` `[>]`: viền `1px solid #E0E0E0`

---

## 12. Panel Chi Tiết Thông Báo (Bên phải)

- **Chiều rộng:** ~320px
- **Nền:** `#FFFFFF`
- **Bo góc:** 10px
- **Shadow:** nhẹ `0 2px 8px rgba(0,0,0,0.08)`
- **Padding:** 20px

### 12.1 Tiêu đề Panel

```
Chi tiết thông báo
```
Font 15px bold, màu `#1A1A2E`, border-bottom `1px solid #F0F0F0`

### 12.2 Loại thông báo (badge + icon lớn)

```
        [ICON LỚN 48px]
         Lịch hẹn mới
        [badge: Lịch hẹn]
```

- **Icon lớn:** hình tròn ~60px nền `#E3F2FD`, icon 📅 màu `#1976D2`, size 28px
- **Tiêu đề loại:** `Lịch hẹn mới` – font 16px bold, màu `#1A1A2E`
- **Badge loại:** `Lịch hẹn` – pill badge, nền `#E3F2FD`, chữ `#1976D2`, bo góc 12px, padding 4px 10px

### 12.3 Thông tin trạng thái & thời gian

```
📅 23/05/2026 09:15        ● Chưa đọc
```

- Icon 📅 nhỏ + ngày giờ: font 12px, màu `#555`
- Chấm `●` màu `#00B14F` + chữ `Chưa đọc`: font 12px, màu `#00B14F`
- Layout: 2 item nằm ngang, justify-content: space-between

### 12.4 Mô tả thông báo

```
Bệnh nhân Trần Văn Nam đã đặt lịch khám mới.
```

- Font 13px, màu `#555555`
- Padding top/bottom 12px
- Border-bottom `1px solid #F0F0F0`

### 12.5 Thông tin chi tiết (dạng bảng 2 cột)

Tiêu đề: **`Thông tin chi tiết`** – font 13px bold, màu `#1A1A2E`

| Nhãn (trái) | Giá trị (phải) |
|---|---|
| Bệnh nhân | Trần Văn Nam |
| Ngày hẹn | 24/05/2026 |
| Giờ hẹn | 08:30 |
| Bác sĩ | BS. Nguyễn Minh |
| Dịch vụ | Khám tổng quát |
| Số điện thoại | 0987 654 321 |

**Style bảng:**
- Nhãn (trái): font 12px, màu `#888888`
- Giá trị (phải): font 12px bold, màu `#1A1A2E`, căn phải
- Mỗi dòng cách nhau 10px
- Dùng `QGridLayout` hoặc 2 `QLabel` trong `QHBoxLayout`

### 12.6 Khu vực Hành Động

Tiêu đề: **`Hành động`** – font 13px bold, màu `#1A1A2E`

**Nút 1: Xem lịch hẹn**
- **Loại:** `QPushButton`
- **Icon:** 📅 lịch (trắng)
- **Nhãn:** `Xem lịch hẹn`
- **Nền:** `#00B14F` (xanh lá đậm)
- **Chữ:** trắng `#FFFFFF`, font 13px bold
- **Bo góc:** 8px
- **Chiều rộng:** ~50% nửa panel
- **Hover:** `#00963F` (xanh lá đậm hơn)
- **Padding:** 10px 16px

**Nút 2: Gọi cho bệnh nhân**
- **Loại:** `QPushButton`
- **Icon:** 📞 điện thoại (xanh lá)
- **Nhãn:** `Gọi cho bệnh nhân`
- **Nền:** `#FFFFFF`
- **Chữ:** `#555555`
- **Viền:** `1px solid #E0E0E0`
- **Bo góc:** 8px
- **Hover:** nền `#F5F5F5`

> Hai nút trên nằm ngang cạnh nhau trong `QHBoxLayout`

**Nút 3: Đánh dấu đã đọc**
- **Loại:** `QPushButton`
- **Icon:** ✔ checkmark
- **Nhãn:** `Đánh dấu đã đọc`
- **Nền:** `#FFFFFF`
- **Chữ:** `#555555`
- **Viền:** `1px solid #E0E0E0`
- **Bo góc:** 8px
- **Chiều rộng:** 100% (full width)
- **Hover:** nền `#F5F5F5`

### 12.7 Thông báo liên quan

Tiêu đề: **`Các thông báo liên quan`** – font 13px bold, màu `#1A1A2E`

Danh sách các link liên quan (dạng text link màu xanh dương `#1976D2`, underline khi hover):

```
• Nhắc lịch hẹn – 22/05/2026 15:30
• Bệnh nhân đến sớm – 23/05/2026 07:50
```

- Font 12px
- Mỗi item cách nhau 8px
- Click vào sẽ chuyển focus sang thông báo đó trong danh sách

---

## 13. Màu sắc & Design Tokens

```python
# Color palette (dùng cho stylesheet PyQt6)
COLOR_PRIMARY     = "#00B14F"   # Xanh lá chính
COLOR_PRIMARY_DARK= "#00963F"   # Hover xanh lá
COLOR_PRIMARY_LIGHT= "#E8F5E9"  # Nền xanh lá nhạt

COLOR_BLUE        = "#1976D2"
COLOR_BLUE_LIGHT  = "#E3F2FD"

COLOR_ORANGE      = "#F57C00"
COLOR_ORANGE_LIGHT= "#FFF3E0"

COLOR_PURPLE      = "#7B1FA2"
COLOR_PURPLE_LIGHT= "#F3E5F5"

COLOR_RED         = "#E53935"

COLOR_BG_MAIN     = "#F5F6FA"   # Nền tổng thể
COLOR_WHITE       = "#FFFFFF"
COLOR_TEXT_DARK   = "#1A1A2E"   # Chữ tiêu đề
COLOR_TEXT_MEDIUM = "#555555"   # Chữ thường
COLOR_TEXT_LIGHT  = "#888888"   # Chữ phụ / placeholder
COLOR_BORDER      = "#E0E0E0"   # Viền

COLOR_UNREAD_DOT  = "#00B14F"   # Chấm chưa đọc
```

---

## 14. Kích thước & Spacing

| Thành phần | Kích thước |
|---|---|
| Cửa sổ tối thiểu | 1280 × 800px |
| Sidebar width | 200px |
| Panel chi tiết width | 320px |
| Khu vực danh sách | chiều rộng còn lại (~760px) |
| Stat card height | ~90px |
| Notification item height | ~70px |
| Border radius card | 10px |
| Border radius button | 8px |
| Border radius input | 6px |
| Padding nội dung | 24px |

---

## 15. Workflow & Logic xử lý

```
[Hệ thống tạo thông báo]
        ↓
[Thông báo xuất hiện trong danh sách]
[Badge số trên icon 🔔 header tăng lên]
        ↓
[Nhân viên click vào một thông báo]
        ↓
[Panel chi tiết bên phải cập nhật nội dung]
[Item được highlight (viền trái xanh lá)]
        ↓
[Nhân viên chọn hành động:]
    ├─ Click "Xem lịch hẹn"     → Chuyển sang màn Quản lý lịch hẹn
    ├─ Click "Gọi cho bệnh nhân" → Hiện dialog gọi / copy SĐT
    └─ Click "Đánh dấu đã đọc"  → Ẩn chấm ●, giảm số badge
```

---

## 16. Ghi chú triển khai PyQt6

```python
# Cấu trúc class đề xuất

class ThongBaoScreen(QWidget):
    """Màn hình Thông báo"""

    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. Sidebar
        sidebar = SidebarWidget()
        main_layout.addWidget(sidebar)

        # 2. Content area
        content = QWidget()
        content.setStyleSheet("background: #F5F6FA;")
        content_layout = QVBoxLayout(content)

        # 2a. Header
        header = HeaderWidget(title="Thông báo", breadcrumb="Trang chủ > Thông báo")
        content_layout.addWidget(header)

        # 2b. Stat cards
        stat_cards = StatCardsRow()
        content_layout.addWidget(stat_cards)

        # 2c. Tab bar
        tab_bar = NotificationTabBar()
        content_layout.addWidget(tab_bar)

        # 2d. Search & Filters
        filters = SearchFilterBar()
        content_layout.addWidget(filters)

        # 2e. Main area (list + detail panel)
        main_area = QHBoxLayout()
        self.notification_list = NotificationListWidget()
        self.detail_panel = NotificationDetailPanel()
        main_area.addWidget(self.notification_list, 65)
        main_area.addWidget(self.detail_panel, 35)
        content_layout.addLayout(main_area)

        # 2f. Pagination
        pagination = PaginationWidget()
        content_layout.addWidget(pagination)

        main_layout.addWidget(content)

    def on_notification_clicked(self, notification_data):
        """Khi click vào thông báo → cập nhật panel chi tiết"""
        self.detail_panel.load(notification_data)
```

> **Lưu ý quan trọng:**
> - Dùng `QScrollArea` cho danh sách thông báo để hỗ trợ cuộn.
> - Dùng `QStackedWidget` nếu cần chuyển tab nội dung.
> - Emit signal khi click item để cập nhật panel chi tiết (tránh coupling chặt).
> - Chấm `●` chưa đọc: dùng `QLabel` với stylesheet `border-radius: 4px; background: #00B14F; min-width: 8px; max-width: 8px; min-height: 8px; max-height: 8px;`
> - Stylesheet toàn cục nên đặt ở `QApplication.setStyleSheet()` cho nhất quán.