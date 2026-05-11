# MÀN HÌNH BÁO CÁO – STAFF (Nhân viên) — Mô tả chi tiết cho AI coding (PyQt6)

> **Mục tiêu tài liệu:** Mô tả đầy đủ layout, màu sắc, font chữ, kích thước, widget PyQt6 và logic hiển thị của màn hình **Báo cáo – Tổng quan** trong ứng dụng **CarePlus – STAFF**. AI không đọc được ảnh nên mọi chi tiết trực quan đều được diễn giải thành văn bản kỹ thuật.

---

## 1. TỔNG THỂ CỬA SỔ ỨNG DỤNG

| Thuộc tính | Giá trị |
|---|---|
| Tiêu đề cửa sổ | `CarePlus - STAFF (Nhân viên)` |
| Kích thước tham khảo | ~1280 × 900 px |
| Nền toàn màn hình | `#F4F6FA` (xám nhạt) |
| Font chữ chính | Sans-serif (ví dụ: `Segoe UI`, `Be Vietnam Pro`, `Roboto`) |
| Màu chủ đạo (brand) | `#00A86B` (xanh lá – CarePlus green) |
| Màu text tiêu đề lớn | `#1A1A2E` (gần đen) |
| Màu text phụ | `#6B7280` (xám trung) |

---

## 2. THANH SIDEBAR TRÁI (Left Navigation)

### 2.1 Cấu trúc tổng thể

- **Widget:** `QWidget` cố định bên trái, chiều rộng ~210 px
- **Nền:** `#FFFFFF` (trắng)
- **Border-right:** 1px solid `#E5E7EB`
- **Layout:** `QVBoxLayout`, căn từ trên xuống

### 2.2 Logo CarePlus (trên cùng)

```
[Icon tròn màu xanh lá #00A86B, dấu "+" trắng bên trong]  CarePlus
```

- Icon: `QLabel` chứa `QPixmap` hình tròn màu `#00A86B`, bán kính ~18 px, có dấu `+` trắng cỡ 14px ở giữa
- Chữ `CarePlus`: `QLabel`, font bold ~18px, màu `#00A86B`
- Padding top: 20px, padding left: 16px
- Cả hai nằm trong `QHBoxLayout`

### 2.3 Danh sách menu (từ trên xuống)

Mỗi mục menu là một `QPushButton` hoặc `QLabel` dạng clickable, layout `QHBoxLayout`:

```
[Icon 20px]  [Tên menu]
```

| STT | Icon (mô tả) | Tên hiển thị | Ghi chú |
|---|---|---|---|
| 1 | Lưới 4 ô (dashboard icon) | Dashboard | |
| 2 | Người + dấu cộng | Tiếp nhận bệnh nhân | |
| 3 | Lịch có dấu tick | Quản lý lịch hẹn | |
| 4 | 2 người dùng | Danh sách bệnh nhân | |
| 5 | Tờ giấy + đô la | Thanh toán & Hóa đơn | |
| 6 | Hộp + kính lúp | Dịch vụ & Gói khám | |
| 7 | Chuông | Thông báo | |
| 8 | Biểu đồ cột | **Báo cáo** | ← **MỤC ĐANG ĐƯỢC CHỌN** |
| 9 | Bánh răng | Cài đặt | |

**Trạng thái menu được chọn (Báo cáo):**
- Nền: `#E6F7F1` (xanh lá rất nhạt)
- Chữ + icon: `#00A86B`
- Border-left: 3px solid `#00A86B`
- Border-radius: 8px (chỉ bên phải)

**Trạng thái menu thường:**
- Nền: transparent
- Chữ + icon: `#6B7280`

**Padding mỗi item:** 10px top/bottom, 16px left/right  
**Khoảng cách giữa các item:** 4px

### 2.4 Nút Đăng xuất (dưới cùng sidebar)

```
[Icon mũi tên ra khỏi cửa – màu đỏ #EF4444]  Đăng xuất
```

- `QPushButton`
- Chữ màu `#EF4444`
- Icon màu `#EF4444`
- Nằm ở cuối sidebar, `addStretch()` phía trên để đẩy xuống
- Padding: 10px 16px
- Hover: nền `#FEF2F2`

---

## 3. KHU VỰC HEADER TRÊN CÙNG (Top Header / Toolbar)

### 3.1 Layout

- `QHBoxLayout` nằm trong vùng nội dung chính (bên phải sidebar)
- Nền: `#FFFFFF`
- Height: ~64px
- Border-bottom: 1px solid `#E5E7EB`
- Padding: 0 24px

### 3.2 Phần bên trái (Tiêu đề trang)

```
Báo cáo                          ← QLabel, font bold 22px, màu #1A1A2E
Trang chủ  >  Báo cáo            ← QLabel breadcrumb, font 13px, màu #6B7280
```

- "Trang chủ": màu `#6B7280`
- ">": màu `#9CA3AF`
- "Báo cáo": màu `#1A1A2E`
- Hai label xếp theo `QVBoxLayout`

### 3.3 Phần bên phải (User info)

```
[Icon chuông]  [Badge đỏ số 3]     [Avatar tròn]  Nguyễn Thị Lan  [▼]
```

- **Icon chuông:** `QLabel` chứa icon SVG/PNG, 22px, màu `#6B7280`
- **Badge thông báo:** `QLabel` tròn nhỏ, nền `#EF4444`, chữ trắng 10px, hiển thị số `3`; đặt overlay góc trên phải của icon chuông (dùng `QFrame` + `setGeometry`)
- **Avatar:** `QLabel` hình tròn, diameter ~36px; nền `#E0F2FE` (xanh nhạt), có icon người dùng màu `#0284C7`
- **Tên:** `QLabel` "Nguyễn Thị Lan", font 14px medium, màu `#1A1A2E`
- **Mũi tên:** `QLabel` "▼", màu `#6B7280`, 12px

---

## 4. KHU VỰC NỘI DUNG CHÍNH (Main Content Area)

- Nền: `#F4F6FA`
- Padding: 24px
- Layout: `QVBoxLayout`

---

## 5. THANH TAB BÁO CÁO

### 5.1 Mô tả

Dòng tab nằm ngay dưới header, trước bộ lọc. Dùng `QTabBar` hoặc tự vẽ bằng `QPushButton` group.

### 5.2 Danh sách tab (trái → phải)

| Tab | Tên | Trạng thái |
|---|---|---|
| 1 | Tổng quan | **Đang chọn** |
| 2 | Bệnh nhân | Thường |
| 3 | Lịch hẹn | Thường |
| 4 | Doanh thu | Thường |
| 5 | Dịch vụ | Thường |
| 6 | Nhân viên | Thường |

**Tab đang chọn (Tổng quan):**
- Chữ: `#00A86B`, font bold 14px
- Border-bottom: 2px solid `#00A86B`
- Nền: transparent

**Tab thường:**
- Chữ: `#6B7280`, font 14px
- Không có border-bottom
- Hover: chữ `#374151`

- Khoảng cách giữa các tab: 24px
- Padding mỗi tab: 10px 4px
- Toàn bộ dòng tab nằm trên `QFrame` có border-bottom: 1px solid `#E5E7EB`

---

## 6. THANH BỘ LỌC (Filter Bar)

### 6.1 Layout

`QHBoxLayout`, spacing 12px, nằm dưới tab bar, padding top 16px bottom 16px.

### 6.2 Ô chọn khoảng thời gian (Date Range Picker)

```
[🔍 icon]  23/05/2026 - 23/05/2026  [📅 icon lịch]
```

- Widget: `QFrame` dạng input box
- Nền: `#FFFFFF`
- Border: 1px solid `#D1D5DB`, border-radius: 8px
- Padding: 8px 12px
- Icon kính lúp bên trái: 16px, màu `#9CA3AF`
- Text ngày: font 13px, màu `#374151`
- Icon lịch bên phải: 16px, màu `#9CA3AF`
- Width: ~200px
- Click: mở `QDateTimeEdit` hoặc custom calendar popup

### 6.3 Dropdown "Hôm nay"

```
Hôm nay  [▼]
```

- Widget: `QComboBox`
- Width: ~140px
- Nền: `#FFFFFF`
- Border: 1px solid `#D1D5DB`, border-radius: 8px
- Padding: 8px 12px
- Font: 13px, màu `#374151`
- Options: `Hôm nay`, `Tuần này`, `Tháng này`, `Tùy chỉnh`

### 6.4 Dropdown "Tất cả bác sĩ"

```
Tất cả bác sĩ  [▼]
```

- Widget: `QComboBox`
- Width: ~160px
- Style giống dropdown "Hôm nay"
- Options: `Tất cả bác sĩ`, `BS. Nguyễn Văn A`, `BS. Trần Thị B`, ...

### 6.5 Nút "Xuất báo cáo" (bên phải cùng, `addStretch()` đẩy sang phải)

```
[⬇ icon download]  Xuất báo cáo
```

- Widget: `QPushButton`
- Nền: `#00A86B`
- Chữ: `#FFFFFF`, font bold 13px
- Icon download: màu trắng, 16px, bên trái chữ
- Border-radius: 8px
- Padding: 10px 20px
- Hover: nền `#009960`
- Click: xuất file PDF hoặc Excel (mở dialog chọn định dạng)

---

## 7. KHUNG THỐNG KÊ TỔNG QUAN (Summary Cards)

### 7.1 Layout

`QHBoxLayout`, spacing 16px, 4 card ngang nhau, mỗi card chiếm 1/4 chiều rộng (dùng `QSizePolicy.Expanding`).

### 7.2 Card chung – Style

- `QFrame`
- Nền: `#FFFFFF`
- Border-radius: 12px
- Padding: 20px
- Box-shadow: giả lập bằng `QGraphicsDropShadowEffect` (blur 8px, offset 0 2px, màu `rgba(0,0,0,0.08)`)
- Layout bên trong: `QVBoxLayout`

---

### 7.3 Card 1 – Tổng bệnh nhân

```
[Icon 2 người – màu #00A86B, nền tròn #E6F7F1]   Tổng bệnh nhân   (phải trên)
24                                                              (số lớn)
↑ 20% so với hôm qua                                            (dưới)
```

| Thành phần | Chi tiết |
|---|---|
| Icon container | `QLabel` hình tròn, 44×44px, nền `#E6F7F1`, border-radius 22px |
| Icon bên trong | SVG 2 người, màu `#00A86B`, 24px |
| Label "Tổng bệnh nhân" | font 13px, màu `#6B7280` |
| Số `24` | `QLabel`, font bold 32px, màu `#1A1A2E` |
| Dòng tăng trưởng | `↑ 20% so với hôm qua`, font 12px, màu `#10B981` (xanh lá) |
| Icon mũi tên lên | `↑` hoặc SVG arrow-up màu `#10B981` |

---

### 7.4 Card 2 – Tổng lịch hẹn

```
[Icon lịch – màu #3B82F6, nền #EFF6FF]   Tổng lịch hẹn
15
↑ 7% so với hôm qua
```

| Thành phần | Chi tiết |
|---|---|
| Icon container | nền `#EFF6FF`, border-radius 22px |
| Icon lịch | màu `#3B82F6` (xanh dương) |
| Số `15` | font bold 32px, màu `#1A1A2E` |
| Tăng trưởng | `↑ 7% so với hôm qua`, màu `#10B981` |

---

### 7.5 Card 3 – Tổng hóa đơn

```
[Icon tờ giấy/hóa đơn – màu #F59E0B, nền #FFFBEB]   Tổng hóa đơn
16
↑ 14% so với hôm qua
```

| Thành phần | Chi tiết |
|---|---|
| Icon container | nền `#FFFBEB` |
| Icon hóa đơn | màu `#F59E0B` (vàng cam) |
| Số `16` | font bold 32px, màu `#F59E0B` |
| Tăng trưởng | màu `#10B981` |

---

### 7.6 Card 4 – Doanh thu

```
[Icon đô la/tiền – màu #8B5CF6, nền #F5F3FF]   Doanh thu
12.450.000 đ
↑ 18% so với hôm qua
```

| Thành phần | Chi tiết |
|---|---|
| Icon container | nền `#F5F3FF` |
| Icon tiền | màu `#8B5CF6` (tím) |
| Số `12.450.000 đ` | font bold 28px (nhỏ hơn một chút vì dài), màu `#8B5CF6` |
| Tăng trưởng | màu `#10B981` |

> **Lưu ý logic:** Nếu % âm (giảm), thay `↑` bằng `↓`, đổi màu thành `#EF4444` (đỏ).

---

## 8. HÀNG BIỂU ĐỒ THỨ NHẤT (Row 2 Charts)

`QHBoxLayout`, spacing 16px, hai biểu đồ song song.

---

### 8.1 Biểu đồ "Số bệnh nhân theo khung giờ" (bên trái, chiếm ~55% width)

**Container:**
- `QFrame`, nền `#FFFFFF`, border-radius 12px, padding 20px
- Drop shadow nhẹ

**Header của card:**
```
Số bệnh nhân theo khung giờ        [Theo giờ ▼]
```
- Tiêu đề: `QLabel`, font bold 15px, màu `#1A1A2E`
- Dropdown "Theo giờ": `QComboBox`, nền `#F9FAFB`, border: 1px solid `#E5E7EB`, nhỏ gọn

**Biểu đồ (Line Chart):**

Dùng thư viện `matplotlib` nhúng vào PyQt6 qua `FigureCanvasQTAgg`, hoặc vẽ tay bằng `QPainter`.

| Thuộc tính | Giá trị |
|---|---|
| Loại biểu đồ | Line chart (đường cong) + area fill phía dưới |
| Màu đường | `#00A86B` |
| Màu fill area | `rgba(0, 168, 107, 0.15)` (xanh lá rất nhạt) |
| Trục X | Thời gian: `07:00`, `08:00`, `09:00`, `10:00`, `11:00`, `12:00`, `13:00`, `14:00`, `15:00`, `16:00`, `17:00` |
| Trục Y | Số bệnh nhân: `0`, `3`, `6`, `9`, `12`, `15` |
| Data mẫu (giờ → số BN) | 07:00→3, 08:00→6, 09:00→9, 10:00→9, 11:00→12, 12:00→8, 13:00→10, 14:00→9, 15:00→7, 16:00→6, 17:00→7 |
| Điểm data | Hình tròn nhỏ `#00A86B`, filled, diameter ~7px |
| Gridlines ngang | `#F3F4F6` (xám rất nhạt), nét đứt |
| Nền chart area | `#FFFFFF` |
| Font trục | 11px, màu `#9CA3AF` |

---

### 8.2 Biểu đồ "Doanh thu theo ngày" (bên phải, chiếm ~45% width)

**Container:** giống card trái

**Header:**
```
Doanh thu theo ngày (7 ngày gần nhất)        [7 ngày ▼]
```

**Biểu đồ (Bar Chart):**

| Thuộc tính | Giá trị |
|---|---|
| Loại | Bar chart (cột đứng) |
| Màu cột | Gradient từ `#00A86B` (dưới) → `#4ADE80` (trên), hoặc solid `#00A86B` |
| Trục X | Ngày: `17/05`, `18/05`, `19/05`, `20/05`, `21/05`, `22/05`, `23/05` |
| Trục Y | Doanh thu (đ): nhãn `0`, `2M`, `4M`, `6M`, `8M`, `10M` |
| Label trục Y | Hiển thị "đ" và "10M" ở trên cùng |
| Data mẫu (ngày → doanh thu) | 17/05→2.5M, 18/05→5M, 19/05→5.5M, 20/05→6.5M, 21/05→6M, 22/05→8.5M, 23/05→7M |
| Border-radius cột | ~4px (cột bo tròn đầu trên) |
| Gridlines | `#F3F4F6`, ngang |

---

## 9. HÀNG BIỂU ĐỒ THỨ HAI (Row 3 – Donut + Bảng)

`QHBoxLayout`, spacing 16px.

---

### 9.1 Biểu đồ "Tỷ lệ dịch vụ" (bên trái, ~45% width)

**Container:** `QFrame`, nền `#FFFFFF`, border-radius 12px, padding 20px

**Header:**
```
Tỷ lệ dịch vụ
```
Font bold 15px, màu `#1A1A2E`

**Biểu đồ Donut:**

Vẽ bằng `matplotlib` (pie chart với `wedgeprops={'width': 0.5}`) hoặc `QPainter` vẽ arc.

| Phần | Màu | % |
|---|---|---|
| Khám tổng quát | `#00A86B` (xanh lá) | 45% |
| Tư vấn sức khỏe | `#3B82F6` (xanh dương) | 25% |
| Khám tim mạch | `#F59E0B` (vàng cam) | 15% |
| Khám nhi | `#8B5CF6` (tím) | 10% |
| Khác | `#9CA3AF` (xám) | 5% |

- Tâm donut: rỗng (vòng tròn ở giữa)
- Kích thước chart: ~200×200px
- Vị trí: bên trái trong card
- Bên phải chart là **legend dọc**:

```
● Khám tổng quát    45%
● Tư vấn sức khỏe   25%
● Khám tim mạch     15%
● Khám nhi          10%
● Khác               5%
```

Mỗi dòng legend:
- Chấm tròn màu tương ứng, ~10px
- Text: font 13px, màu `#374151`
- Số %: font 13px, màu `#6B7280`, căn phải

Layout bên trong card: `QHBoxLayout` (chart bên trái + legend bên phải)

---

### 9.2 Bảng "Doanh thu theo dịch vụ" (bên phải, ~55% width)

**Container:** `QFrame`, nền `#FFFFFF`, border-radius 12px, padding 20px

**Header:**
```
Doanh thu theo dịch vụ
```
Font bold 15px, màu `#1A1A2E`

**Bảng dữ liệu** (`QTableWidget` hoặc custom `QFrame` + labels):

| Dịch vụ | Số lượt | Doanh thu |
|---|---|---|
| Khám tổng quát | 18 | 5.625.000 đ |
| Tư vấn sức khỏe | 10 | 3.125.000 đ |
| Khám tim mạch | 6 | 1.875.000 đ |
| Khám nhi | 4 | 1.250.000 đ |
| Khác | 2 | 575.000 đ |
| **Tổng cộng** | **40** | **12.450.000 đ** |

**Style bảng:**

| Thuộc tính | Giá trị |
|---|---|
| Header row | Nền `#F9FAFB`, font bold 12px, màu `#6B7280`, chữ in hoa nhẹ |
| Border header bottom | 1px solid `#E5E7EB` |
| Mỗi row | padding 12px 8px, border-bottom 1px solid `#F3F4F6` |
| Chữ cột "Dịch vụ" | font 13px, màu `#374151` |
| Chữ cột "Số lượt" | font 13px, màu `#374151`, căn giữa |
| Chữ cột "Doanh thu" | font 13px, màu `#374151`, căn phải |
| Row cuối "Tổng cộng" | font bold 13px; Doanh thu tổng màu `#00A86B` |
| Row hover | nền `#F9FAFB` |
| Không có scrollbar ngang | `setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)` |

---

## 10. HÀNG THỨ TƯ (Row 4 – Tình trạng lịch hẹn + Báo cáo nhanh)

`QHBoxLayout`, spacing 16px.

---

### 10.1 Biểu đồ "Tình trạng lịch hẹn" (bên trái, ~45% width)

**Container:** `QFrame`, nền `#FFFFFF`, border-radius 12px, padding 20px

**Header:**
```
Tình trạng lịch hẹn
```
Font bold 15px, màu `#1A1A2E`

**Biểu đồ Donut (tương tự mục 9.1):**

| Phần | Màu | % | Số lịch |
|---|---|---|---|
| Đã xác nhận | `#00A86B` (xanh lá) | 60% | 9 |
| Đã hoàn tất | `#3B82F6` (xanh dương) | 20% | 3 |
| Đang chờ | `#F59E0B` (vàng) | 13% | 2 |
| Đã hủy | `#EF4444` (đỏ) | 7% | 1 |

**Legend (bên phải chart):**
```
● Đã xác nhận    60% (9)
● Đã hoàn tất    20% (3)
● Đang chờ       13% (2)
● Đã hủy          7% (1)
```

- Số trong ngoặc: số lịch thực tế

---

### 10.2 Khung "Báo cáo nhanh" (bên phải, ~55% width)

**Container:** `QFrame`, nền `#FFFFFF`, border-radius 12px, padding 20px

**Header:**
```
Báo cáo nhanh
```
Font bold 15px, màu `#1A1A2E`, padding-bottom 16px.

**Grid 5 nút shortcut** (1 hàng, 5 cột – `QHBoxLayout` spacing 12px):

Mỗi nút là `QFrame` hoặc `QPushButton` custom:

```
[Icon 32px]
 Tên báo cáo
```

| Nút | Icon (mô tả) | Màu nền icon | Tên |
|---|---|---|---|
| 1 | 2 người (bệnh nhân) | `#E6F7F1` (xanh nhạt), icon `#00A86B` | Báo cáo bệnh nhân |
| 2 | Lịch / calendar | `#EFF6FF` (xanh dương nhạt), icon `#3B82F6` | Báo cáo lịch hẹn |
| 3 | Tờ giấy có đường kẻ + dấu đô la | `#FFFBEB` (vàng nhạt), icon `#F59E0B` | Báo cáo doanh thu |
| 4 | Clipboard / dịch vụ | `#F5F3FF` (tím nhạt), icon `#8B5CF6` | Báo cáo dịch vụ |
| 5 | Người đeo ca-vat / nhân viên | `#EFF6FF`, icon `#3B82F6` | Báo cáo nhân viên |

**Style mỗi nút:**
- `QFrame` hoặc `QPushButton`, nền `#F9FAFB`, border: 1px solid `#E5E7EB`, border-radius 10px
- Padding: 16px
- Layout bên trong: `QVBoxLayout`, căn giữa
- Icon container: `QLabel` hình tròn 44×44px, màu nền như bảng trên
- Icon bên trong: 24px, màu tương ứng
- Text: `QLabel`, font 12px, màu `#374151`, `Qt.AlignCenter`
- Hover: nền `#F3F4F6`, border `#D1D5DB`
- Cursor: `Qt.PointingHandCursor`

---

## 11. FOOTER / DÒNG THÔNG TIN CUỐI

`QHBoxLayout`, nằm dưới cùng vùng nội dung, padding-top 12px.

**Bên trái:**
```
Dữ liệu cập nhật đến 23/05/2026 10:30
```
- Font 12px, màu `#9CA3AF`

**Bên phải:**
```
Ghi chú: Dữ liệu chỉ mang tính chất tham khảo tại thời điểm hiện tại.
```
- Font 12px, italic, màu `#9CA3AF`
- `addStretch()` giữa trái và phải để đẩy sang hai đầu

---

## 12. SCROLL AREA

Toàn bộ vùng nội dung chính (từ mục 5 đến mục 11) được đặt trong `QScrollArea`:

```python
scroll_area = QScrollArea()
scroll_area.setWidgetResizable(True)
scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
scroll_area.setFrameShape(QFrame.NoFrame)
```

---

## 13. STYLESHEET TOÀN CỤC (QSS Reference)

```css
/* Nền app */
QMainWindow, QWidget#main_content {
    background-color: #F4F6FA;
}

/* Sidebar */
QWidget#sidebar {
    background-color: #FFFFFF;
    border-right: 1px solid #E5E7EB;
}

/* Menu item thường */
QPushButton.nav_item {
    background: transparent;
    color: #6B7280;
    border: none;
    border-radius: 8px;
    padding: 10px 16px;
    text-align: left;
    font-size: 14px;
}
QPushButton.nav_item:hover {
    background: #F9FAFB;
    color: #374151;
}

/* Menu item được chọn */
QPushButton.nav_item_active {
    background: #E6F7F1;
    color: #00A86B;
    border-left: 3px solid #00A86B;
    font-weight: bold;
}

/* Card */
QFrame.card {
    background: #FFFFFF;
    border-radius: 12px;
    border: none;
}

/* Nút xuất báo cáo */
QPushButton#btn_export {
    background: #00A86B;
    color: #FFFFFF;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: bold;
    font-size: 13px;
}
QPushButton#btn_export:hover {
    background: #009960;
}

/* Dropdown filter */
QComboBox.filter_combo {
    background: #FFFFFF;
    border: 1px solid #D1D5DB;
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 13px;
    color: #374151;
}
QComboBox.filter_combo::drop-down {
    border: none;
}

/* Bảng doanh thu */
QTableWidget {
    border: none;
    gridline-color: #F3F4F6;
    font-size: 13px;
}
QTableWidget::item {
    padding: 12px 8px;
    color: #374151;
}
QHeaderView::section {
    background: #F9FAFB;
    color: #6B7280;
    font-weight: bold;
    font-size: 12px;
    border: none;
    border-bottom: 1px solid #E5E7EB;
    padding: 10px 8px;
}
```

---

## 14. CẤU TRÚC CLASS / MODULE GỢI Ý (PyQt6)

```
careplus/
├── main.py                   # QApplication entry point
├── windows/
│   └── staff_window.py       # QMainWindow chính
├── widgets/
│   ├── sidebar.py            # SidebarWidget(QWidget)
│   ├── header.py             # HeaderWidget(QWidget)
│   ├── report/
│   │   ├── report_screen.py  # ReportScreen(QWidget) – container chính
│   │   ├── report_tabs.py    # ReportTabBar(QWidget)
│   │   ├── filter_bar.py     # FilterBar(QWidget)
│   │   ├── summary_cards.py  # SummaryCards(QWidget) – 4 card
│   │   ├── chart_patients_hourly.py   # Biểu đồ line
│   │   ├── chart_revenue_daily.py     # Biểu đồ bar
│   │   ├── chart_service_ratio.py     # Donut chart
│   │   ├── table_revenue_service.py   # QTableWidget
│   │   ├── chart_appointment_status.py # Donut chart 2
│   │   └── quick_report_panel.py      # 5 nút shortcut
│   └── common/
│       ├── stat_card.py      # Widget card thống kê tái sử dụng
│       └── donut_chart.py    # QPainter donut chart tái sử dụng
└── styles/
    └── main.qss              # QSS toàn cục
```

---

## 15. LƯU Ý TRIỂN KHAI

1. **Thư viện biểu đồ:** Dùng `matplotlib` + `matplotlib.backends.backend_qtagg.FigureCanvasQTAgg` nhúng vào `QWidget`. Đây là cách phổ biến nhất với PyQt6.
2. **Font:** Đăng ký font qua `QFontDatabase.addApplicationFont()` nếu dùng font tùy chỉnh.
3. **Drop shadow:** `QGraphicsDropShadowEffect` áp lên `QFrame` card.
4. **Responsive:** Dùng `QSplitter` hoặc `QSizePolicy` để các cột tự co giãn khi resize cửa sổ.
5. **Dữ liệu:** Ban đầu dùng data mẫu hardcode; sau này kết nối API/database thực tế.
6. **Cập nhật real-time:** Dùng `QTimer` để refresh dữ liệu mỗi N phút, cập nhật label và biểu đồ không reload toàn màn hình.
7. **Định dạng số tiền:** Dùng hàm `format(12450000, ',').replace(',', '.')` + ` đ` để hiển thị `12.450.000 đ`.
8. **Icon:** Dùng SVG icons (Material Icons, Heroicons) load qua `QIcon` hoặc `QLabel` + `QPixmap`.