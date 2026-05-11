# 📄 MÔ TẢ CHI TIẾT MÀN HÌNH "THANH TOÁN & HÓA ĐƠN" — STAFF VIEW
## Hệ thống: CarePlus — Phần mềm quản lý phòng khám

---

## 1. TỔNG QUAN BỐ CỤC (LAYOUT OVERVIEW)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  SIDEBAR (220px, cố định bên trái)  │  NỘI DUNG CHÍNH (flex-grow)          │
│                                      │  ┌──────────────────────────────────┐│
│  Logo + Nav items                    │  │ HEADER: Title + Breadcrumb       ││
│                                      │  ├──────────────────────────────────┤│
│                                      │  │ STAT CARDS (4 ô ngang)           ││
│                                      │  ├──────────────────────────────────┤│
│                                      │  │ TAB FILTER + SEARCH + DATE       ││
│                                      │  ├────────────────────┬─────────────┤│
│                                      │  │ DANH SÁCH HÓA ĐƠN  │ PANEL CHI  ││
│                                      │  │ (bảng, ~60% width) │ TIẾT HĐ    ││
│                                      │  │                    │ (~40% width)││
│                                      │  └────────────────────┴─────────────┘│
└─────────────────────────────────────────────────────────────────────────────┘
```

**Màu nền tổng thể:** `#F8F9FA` (xám nhạt)
**Font chữ:** Hệ thống sans-serif (ví dụ: `Be Vietnam Pro`, `Nunito`, hoặc `system-ui`)
**Ngôn ngữ giao diện:** Tiếng Việt

---

## 2. SIDEBAR (THANH ĐIỀU HƯỚNG TRÁI)

### Kích thước
- **Width:** 220px
- **Height:** 100vh (full chiều cao màn hình)
- **Background:** `#1A1A2E` (navy đậm, gần đen)
- **Position:** Fixed, bên trái

### Logo (phần trên cùng)
- Icon tròn màu xanh lá `#00C897` với dấu `+` trắng bên trong
- Text **"CarePlus"** màu trắng, font bold, cỡ ~20px
- Padding: 20px 16px

### Navigation Items (danh sách menu)
Mỗi item có: icon + label, padding 12px 16px, bo góc 8px khi hover/active.

| Icon | Label | Trạng thái |
|------|-------|-----------|
| 🏠 | Dashboard | Bình thường |
| 👤 | Tiếp nhận bệnh nhân | Bình thường |
| 📅 | Quản lý lịch hẹn | Bình thường |
| 👥 | Danh sách bệnh nhân | Bình thường |
| 💳 | **Thanh toán & Hóa đơn** | **ACTIVE** (nền vàng cam `#F59E0B`, text trắng) |
| 🩺 | Dịch vụ & Gói khám | Bình thường |
| 🔔 | Thông báo | Bình thường |
| 📊 | Báo cáo | Bình thường |
| ⚙️ | Cài đặt | Bình thường |

**Nav item bình thường:** text `#9CA3AF` (xám nhạt)
**Nav item hover:** background `rgba(255,255,255,0.08)`, text trắng
**Nav item active:** background `#F59E0B` (cam vàng), text trắng, icon trắng

### Nút Đăng xuất (dưới cùng sidebar)
- Màu text: `#EF4444` (đỏ)
- Icon: mũi tên ra ngoài (logout icon)
- Label: "Đăng xuất"
- Padding bottom: 24px

---

## 3. HEADER TOPBAR (Thanh trên cùng nội dung chính)

### Bố cục: flex, space-between, align-center

**Bên trái:**
- Text lớn `"Thanh toán & Hóa đơn"` — font bold, ~24px, màu `#111827`
- Breadcrumb bên dưới: `Trang chủ > Thanh toán & Hóa đơn` — font nhỏ ~13px, màu `#9CA3AF`

**Bên phải:**
- Icon chuông 🔔 với badge đỏ số `3` (notification badge, absolute top-right trên icon)
- Avatar tròn (ảnh người dùng ~36px)
- Text tên: `"Nguyễn Thị Lan"` — font medium, ~14px
- Mũi tên dropdown `▼` màu xám

---

## 4. KHU VỰC STAT CARDS (4 ô thống kê)

Bố cục: 4 card ngang hàng nhau, cách đều, mỗi card `flex: 1`.

### Card 1 — Hóa đơn chờ thanh toán
- Background: `#FFFFFF`, border-radius: 12px, box-shadow nhẹ
- Icon hình vuông bo góc màu cam nhạt `#FEF3C7`, icon bên trong màu `#F59E0B` (document icon)
- Label: `"Hóa đơn chờ thanh toán"` — font 13px, màu `#6B7280`
- Số lớn: **`6`** — font bold 28px, màu `#F59E0B` (cam)
- Dòng phụ: `"Tổng tiền: 12.450.000 đ"` — font 12px, màu `#F59E0B`

### Card 2 — Đã thanh toán hôm nay
- Icon nền xanh lá nhạt `#D1FAE5`, icon màu `#10B981` (camera/check icon)
- Label: `"Đã thanh toán hôm nay"` — font 13px, màu `#6B7280`
- Số lớn: **`9`** — font bold 28px, màu `#10B981` (xanh lá)
- Dòng phụ: `"Tổng tiền: 18.750.000 đ"` — font 12px, màu `#10B981`

### Card 3 — Hoàn tiền hôm nay
- Icon nền xanh dương nhạt `#DBEAFE`, icon màu `#3B82F6` (refresh/refund icon)
- Label: `"Hoàn tiền hôm nay"` — font 13px, màu `#6B7280`
- Số lớn: **`1`** — font bold 28px, màu `#3B82F6` (xanh dương)
- Dòng phụ: `"Tổng tiền: 450.000 đ"` — font 12px, màu `#3B82F6`

### Card 4 — Doanh thu hôm nay
- Icon nền tím nhạt `#EDE9FE`, icon màu `#8B5CF6` (chart/currency icon)
- Label: `"Doanh thu hôm nay"` — font 13px, màu `#6B7280`
- Số lớn: **`18.300.000 đ`** — font bold 22px, màu `#8B5CF6` (tím)
- Dòng phụ: `"12 hóa đơn"` — font 12px, màu `#6B7280`

---

## 5. KHU VỰC TAB + TÌM KIẾM + BỘ LỌC

### Tab trạng thái (5 tab ngang hàng)

Dạng pill/tab, border-bottom highlight khi active:

| Tab | Badge | Trạng thái |
|-----|-------|-----------|
| Tất cả | (không có) | **ACTIVE** — viền xanh dưới, text `#10B981` |
| Chờ thanh toán | Badge cam `6` | Bình thường |
| Đã thanh toán | (không có) | Bình thường |
| Đã hủy | (không có) | Bình thường |
| Hoàn tiền | (không có) | Bình thường |

- Tab active: font bold, màu xanh lá `#10B981`, border-bottom 2px solid `#10B981`
- Tab bình thường: màu `#6B7280`
- Badge: pill tròn nhỏ, background `#F59E0B`, text trắng, font 11px, hiện số lượng

### Thanh tìm kiếm
- Input dạng `search`, placeholder: `"Tìm kiếm bệnh nhân, mã hóa đơn..."`
- Chiều rộng: ~300px
- Border: 1px solid `#E5E7EB`, border-radius: 8px
- Icon kính lúp 🔍 bên trái input
- Background: `#FFFFFF`

### Bộ lọc ngày
- Hai input date: `"Từ ngày"` và `"Đến ngày"` nối nhau bằng dấu `—`
- Mỗi input có icon calendar 📅 bên phải
- Border: 1px solid `#E5E7EB`, border-radius: 8px
- Nút `"Bộ lọc"` có icon funnel (lọc), border outline, màu `#6B7280`

---

## 6. BẢNG "DANH SÁCH HÓA ĐƠN" (Trái, ~60% width)

### Tiêu đề bảng
- Text: `"Danh sách hóa đơn (28)"` — font bold 15px, màu `#111827`

### Header bảng
Background header: `#F9FAFB`, border-bottom: `1px solid #E5E7EB`

| Cột | Nội dung | Width gợi ý |
|-----|---------|-------------|
| Mã hóa đơn | Mã dạng `HDxxxxxx` | 110px |
| Bệnh nhân | Avatar tròn + tên | flex |
| Ngày tạo | Ngày giờ | 160px |
| Tổng tiền | Số tiền VND | 120px |
| Trạng thái | Badge màu | 140px |
| Thao tác | Icon buttons | 80px |

Font header: 13px, màu `#6B7280`, font-weight: 600, text-transform: uppercase

### Dữ liệu mẫu (10 hàng hiển thị)

| Mã HĐ | Bệnh nhân | Avatar | Ngày tạo | Tổng tiền | Trạng thái |
|-------|-----------|--------|----------|-----------|-----------|
| HD000128 | Nguyễn Văn Hùng | Nam, tóc đen | 23/05/2026 08:15 | 850.000 đ | 🟠 Chờ thanh toán |
| HD000127 | Trần Thị Mai | Nữ | 23/05/2026 08:20 | 650.000 đ | 🟠 Chờ thanh toán |
| HD000126 | Lê Văn Nam | Nam | 23/05/2026 08:45 | 1.200.000 đ | 🟠 Chờ thanh toán |
| HD000125 | Phạm Thị Lan | Nữ | 23/05/2026 09:00 | 1.500.000 đ | 🟢 Đã thanh toán |
| HD000124 | Hoàng Anh Tuấn | Nam | 23/05/2026 09:15 | 700.000 đ | 🟢 Đã thanh toán |
| HD000123 | Vũ Thị Hương | Nữ | 23/05/2026 09:30 | 1.350.000 đ | 🟠 Chờ thanh toán |
| HD000122 | Đỗ Minh Quân | Nam | 23/05/2026 10:00 | 950.000 đ | 🟢 Đã thanh toán |
| HD000121 | Nguyễn Thị Hoa | Nữ | 23/05/2026 10:15 | 600.000 đ | 🔴 Đã hủy |
| HD000120 | Bùi Văn Dũng | Nam | 23/05/2026 10:30 | 1.100.000 đ | 🟠 Chờ thanh toán |
| HD000119 | Trương Thị Kiều | Nữ | 23/05/2026 10:45 | 800.000 đ | 🟠 Chờ thanh toán |

### Styling từng hàng
- Mỗi hàng: padding 14px 16px, border-bottom `1px solid #F3F4F6`
- **Hàng được chọn (HD000128):** background `#F0FDF4` (xanh lá rất nhạt), border-left `3px solid #10B981`
- Hover hàng: background `#F9FAFB`

### Avatar bệnh nhân
- Hình tròn 32px × 32px
- Nam: màu nền `#DBEAFE` (xanh nhạt), icon người màu `#3B82F6`
- Nữ: màu nền `#FCE7F3` (hồng nhạt), icon người màu `#EC4899`
- Text tên: font 14px, màu `#111827`

### Badge trạng thái
- **Chờ thanh toán:** background `#FEF3C7`, text `#D97706`, font 12px, border-radius: 20px, padding: 3px 10px
- **Đã thanh toán:** background `#D1FAE5`, text `#059669`, cùng style
- **Đã hủy:** background `#FEE2E2`, text `#DC2626`, cùng style
- **Hoàn tiền:** background `#DBEAFE`, text `#2563EB`, cùng style

### Cột Thao tác
- Icon mắt 👁 (xem chi tiết): button tròn nhỏ, màu `#3B82F6`
- Icon ba chấm ⋮ (more options): button tròn nhỏ, màu `#6B7280`
- Khoảng cách giữa 2 icon: 8px

### Phân trang (Pagination)
- Nằm dưới bảng, căn giữa
- `"Hiển thị 10 ▼ bản ghi"` — dropdown chọn số hàng/trang
- Nút trang: `< 1 2 3 >`, trang 1 active: background `#10B981`, text trắng, border-radius: 6px

---

## 7. PANEL "THÔNG TIN HÓA ĐƠN" (Phải, ~40% width)

**Background:** `#FFFFFF`
**Border-left:** `1px solid #E5E7EB`
**Padding:** 20px
**Overflow-y:** auto (có thể scroll)

### 7.1 Header Panel

```
[Thông tin hóa đơn]                    [🖨 In hóa đơn]
```

- Text "Thông tin hóa đơn": font bold 15px, màu `#111827`
- Nút "In hóa đơn": icon printer + text, màu `#3B82F6`, có border outline xanh, border-radius: 8px, padding: 6px 14px

### 7.2 Thông tin cơ bản hóa đơn

3 dòng, mỗi dòng: label (xám) + value (đen), flexbox space-between

```
Mã hóa đơn:    HD000128    [Chờ thanh toán] ← badge cam
Ngày tạo:      23/05/2026 08:15
Nhân viên:     Nguyễn Thị Lan
```

- Badge trạng thái nằm cùng dòng với Mã hóa đơn, căn phải
- Font label: 13px, màu `#6B7280`
- Font value: 13px, màu `#111827`, font-weight 500

### 7.3 Thông tin bệnh nhân

Khu vực có divider phía trên `border-top: 1px solid #F3F4F6`

Bố cục:
```
[Avatar 48px]  Nguyễn Văn Hùng  [Nam badge xanh]
               15/02/1990 (35 tuổi) - 0987 654 321
               Địa chỉ: 123 Đường Lê Lợi, P.1, Q.1, TP.HCM
```

- Avatar: hình tròn 48px, nền xanh dương nhạt, icon người
- Tên: font bold 15px, màu `#111827`
- Badge giới tính "Nam": background `#DBEAFE`, text `#2563EB`, font 11px, border-radius 4px, padding 2px 8px
- Dòng thứ 2: font 12px, màu `#6B7280`
- Dòng địa chỉ: font 12px, màu `#6B7280`

### 7.4 Chi tiết dịch vụ

Header: `"Chi tiết dịch vụ"` — font bold 14px, màu `#111827`

Bảng mini có 4 cột:

| Dịch vụ | Số lượng | Đơn giá | Thành tiền |
|---------|---------|---------|-----------|
| Khám tổng quát | 1 | 300.000 đ | 300.000 đ |
| Xét nghiệm máu | 1 | 250.000 đ | 250.000 đ |
| Siêu âm ổ bụng | 1 | 300.000 đ | 300.000 đ |

- Font: 13px
- Header bảng: màu `#6B7280`
- Data: màu `#111827`
- Padding mỗi hàng: 8px 0
- Border-bottom mỗi hàng: `1px dashed #F3F4F6`

### 7.5 Tổng tiền

```
Tổng tiền dịch vụ:              850.000 đ
Giảm giá:                             0 đ
────────────────────────────────────────
Tổng cần thanh toán:           850.000 đ  ← màu cam đậm
```

- Dòng "Tổng tiền dịch vụ" và "Giảm giá": font 13px, màu `#6B7280` / `#111827`
- Divider: `border-top: 1px solid #E5E7EB`, margin 8px 0
- Dòng "Tổng cần thanh toán": font bold 15px
  - Label: màu `#111827`
  - Số tiền: màu `#F59E0B` (cam vàng), font bold

### 7.6 Khu vực Thanh toán

Header: `"Thanh toán"` — font bold 14px, màu `#111827`
Sub-label: `"Phương thức thanh toán"` — font 13px, màu `#6B7280`

#### 3 nút phương thức thanh toán (flex row, gap 8px)

```
[✓ Tiền mặt]    [Thẻ ATM/Visa]    [Chuyển khoản]
```

- Mỗi nút: border-radius 8px, padding 10px 16px, font 13px
- **Tiền mặt (SELECTED):** background `#10B981` (xanh lá), text trắng, icon ✓ + emoji 💵
- **Thẻ ATM/Visa:** background `#FFFFFF`, border `1px solid #E5E7EB`, text `#6B7280`, icon 💳
- **Chuyển khoản:** background `#FFFFFF`, border `1px solid #E5E7EB`, text `#6B7280`, icon 🏦

#### Ô nhập số tiền nhận

Label: `"Số tiền nhận"` — font 13px, màu `#6B7280`

Input:
```
[ 850.000                    đ ]
```
- Input text, align-right cho số
- Suffix text `"đ"` bên phải, màu `#6B7280`
- Border: `1px solid #E5E7EB`, border-radius: 8px, padding: 10px 12px
- Font: 14px, màu `#111827`

#### Dòng Tiền thừa

```
Tiền thừa:    0 đ
```
- Label: font 13px, màu `#6B7280`
- Value: font 13px bold, màu `#111827`

### 7.7 Nút CTA "Xác nhận thanh toán"

```
[  ✓  Xác nhận thanh toán  ]
```

- **Background:** gradient xanh lá `#10B981` → `#059669` (hoặc solid `#10B981`)
- **Text:** trắng, font bold 15px
- **Border-radius:** 10px
- **Width:** 100%
- **Padding:** 14px
- **Icon:** ✓ (checkmark) trước text
- **Hover:** background đậm hơn `#059669`, box-shadow nhẹ

---

## 8. RESPONSIVE VÀ CÁC LƯU Ý KỸ THUẬT

### Kích thước màn hình chuẩn
- Desktop: 1440px × 900px (full-screen desktop app)
- Layout cố định, không cần mobile-first

### Màu sắc tổng hợp (CSS Variables)

```css
:root {
  --color-bg: #F8F9FA;
  --color-sidebar: #1A1A2E;
  --color-white: #FFFFFF;
  --color-border: #E5E7EB;
  --color-text-primary: #111827;
  --color-text-secondary: #6B7280;
  --color-text-muted: #9CA3AF;

  /* Trạng thái */
  --color-warning: #F59E0B;        /* Chờ thanh toán / Active nav */
  --color-warning-light: #FEF3C7;
  --color-success: #10B981;        /* Đã thanh toán / CTA button */
  --color-success-light: #D1FAE5;
  --color-danger: #EF4444;         /* Đã hủy */
  --color-danger-light: #FEE2E2;
  --color-info: #3B82F6;           /* Hoàn tiền / link */
  --color-info-light: #DBEAFE;
  --color-purple: #8B5CF6;         /* Doanh thu */
  --color-purple-light: #EDE9FE;
}
```

### Shadows

```css
.card {
  box-shadow: 0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.04);
}
.panel {
  box-shadow: -2px 0 8px rgba(0,0,0,0.04);
}
```

### Typography Scale

```css
/* Title lớn */        font-size: 24px; font-weight: 700;
/* Section header */   font-size: 15px; font-weight: 600;
/* Body */             font-size: 14px; font-weight: 400;
/* Small/label */      font-size: 13px; font-weight: 400;
/* Micro/badge */      font-size: 11px; font-weight: 500;
/* Stat number */      font-size: 28px; font-weight: 700;
```

---

## 9. STATES & INTERACTIONS

### Hành động click vào hàng hóa đơn
1. Hàng được highlight: `background: #F0FDF4`, `border-left: 3px solid #10B981`
2. Panel bên phải cập nhật toàn bộ thông tin của hóa đơn được chọn

### Chọn phương thức thanh toán
- Nút được chọn: background `#10B981`, text trắng
- Các nút còn lại: trở về trạng thái outline

### Nhập số tiền nhận
- Hệ thống tự tính `Tiền thừa = Số tiền nhận - Tổng cần thanh toán`
- Nếu tiền nhận < tổng tiền: hiện cảnh báo đỏ nhẹ dưới input

### Xác nhận thanh toán
- Loading state: button disabled + spinner
- Success: badge "Chờ thanh toán" đổi thành "Đã thanh toán", hàng đổi màu badge

---

## 10. COMPONENT CHECKLIST ĐẦY ĐỦ

- [ ] Sidebar với nav items và active state
- [ ] Topbar với notification bell + avatar dropdown
- [ ] 4 Stat Cards (cam, xanh lá, xanh dương, tím)
- [ ] Tab bar 5 tab với badge counter
- [ ] Search input + date range picker + filter button
- [ ] Table với 10 dòng dữ liệu mẫu
- [ ] Row selection highlight
- [ ] Avatar (nam/nữ phân biệt bằng màu)
- [ ] Status badges (4 loại: chờ, đã TT, hủy, hoàn tiền)
- [ ] Pagination controls
- [ ] Panel chi tiết (header + thông tin HĐ + thông tin BN + bảng dịch vụ)
- [ ] Tổng tiền + giảm giá + tổng cuối
- [ ] 3 nút phương thức thanh toán
- [ ] Input số tiền nhận + tiền thừa
- [ ] CTA button "Xác nhận thanh toán"
- [ ] Nút "In hóa đơn"
