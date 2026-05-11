# Mô tả chi tiết màn hình “Cài đặt” – CarePlus STAFF

Tài liệu này mô tả lại màn hình **Cài đặt** dành cho **nhân viên/staff** dựa trên ảnh giao diện. Mục tiêu là để AI hoặc lập trình viên **không đọc được ảnh vẫn có thể dựng lại giao diện bằng Python PyQt6**.

---

## 1. Tổng quan màn hình

Đây là màn hình **Cài đặt hệ thống cho nhân viên** trong phần mềm desktop **CarePlus - STAFF (Nhân viên)**.

Màn hình dùng để:

- Xem và chỉnh sửa thông tin cá nhân của nhân viên.
- Đổi mật khẩu đăng nhập.
- Cấu hình một số tùy chọn hệ thống cơ bản.
- Xem hoặc đổi logo phòng khám.
- Sao lưu và khôi phục dữ liệu.
- Xem thông tin hệ thống.
- Kiểm tra cập nhật phần mềm.

Phạm vi quyền của nhân viên:

- Nhân viên được chỉnh thông tin cá nhân của chính mình.
- Nhân viên được đổi mật khẩu của chính mình.
- Nhân viên được thay đổi một số tùy chọn hiển thị cá nhân như ngôn ngữ, giao diện, định dạng ngày giờ, số bản ghi mỗi trang.
- Nhân viên không được chỉnh database lõi, phân quyền admin hoặc các cấu hình hệ thống nhạy cảm.

---

## 2. Kích thước và bố cục tổng thể

Giao diện là ứng dụng desktop PyQt6, phong cách hiện đại, nền sáng.

Kích thước cửa sổ trong ảnh khoảng:

- Rộng: 1600 px.
- Cao: 900 px.

Có thể thiết kế theo dạng responsive nhưng bố cục chính nên giữ như sau:

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ Thanh tiêu đề app: CarePlus - STAFF (Nhân viên)                              │
├───────────────┬──────────────────────────────────────────────────────────────┤
│ Sidebar trái  │ Nội dung chính                                               │
│ menu chính    │                                                              │
│               │ Header nội dung: Cài đặt + breadcrumb + user topbar          │
│               │                                                              │
│               │ ┌───────────────┬──────────────────────────────────────────┐ │
│               │ │ Menu setting  │ Các khối cài đặt                         │ │
│               │ │ bên trong     │                                          │ │
│               │ └───────────────┴──────────────────────────────────────────┘ │
└───────────────┴──────────────────────────────────────────────────────────────┘
```

Có 4 vùng chính:

1. **Thanh tiêu đề hệ điều hành/app** ở trên cùng.
2. **Sidebar menu chính** bên trái.
3. **Header nội dung** phía trên vùng main.
4. **Vùng cài đặt** gồm menu cài đặt phụ bên trái và các card nội dung bên phải.

---

## 3. Màu sắc và phong cách giao diện

### 3.1. Màu nền

- Nền toàn bộ nội dung chính: `#FFFFFF` hoặc gần trắng.
- Nền sidebar trái: `#FFFFFF`.
- Nền item đang chọn trong sidebar: xanh nhạt `#EAF7F0` hoặc `#E9F8F1`.
- Nền item đang chọn trong menu cài đặt phụ: xanh nhạt tương tự.
- Nền card: trắng `#FFFFFF`.

### 3.2. Màu thương hiệu

Màu chính của CarePlus là xanh lá:

- Xanh chính: `#00A86B` hoặc `#00A65A`.
- Xanh hover: `#00995F`.
- Xanh nhạt dùng cho background active: `#EAF7F0`.

### 3.3. Màu chữ

- Tiêu đề chính: `#1F2937`.
- Chữ thường: `#374151`.
- Chữ phụ/label: `#6B7280`.
- Chữ disable hoặc mô tả nhỏ: `#8A94A6`.
- Màu cảnh báo/xóa/khôi phục: đỏ `#EF4444`.

### 3.4. Border và bo góc

- Card có border mảnh: `#E5E7EB`.
- Input có border: `#DDE3EA`.
- Bo góc card: 10–12 px.
- Bo góc input/button: 6–8 px.

### 3.5. Font

Có thể dùng:

- `Inter`, `Segoe UI`, `Arial`, hoặc font mặc định hệ thống.

Kích thước chữ tham khảo:

- Tiêu đề trang: 22–24 px, bold.
- Tiêu đề card: 16–17 px, bold.
- Label input: 12–13 px.
- Nội dung input/menu: 14 px.
- Sidebar menu: 15 px.

---

## 4. Thanh tiêu đề cửa sổ

Trên cùng là thanh title bar nền xanh đậm/đen xanh.

Nội dung bên trái:

```text
CarePlus - STAFF (Nhân viên)
```

Phía phải có các nút điều khiển cửa sổ:

- Thu nhỏ.
- Phóng to/khôi phục.
- Đóng.

Trong PyQt6 có thể dùng title bar mặc định của hệ điều hành hoặc custom title bar. Nếu custom title bar thì nền nên là xanh navy rất đậm, gần `#07152A`.

---

## 5. Sidebar menu chính bên trái

Sidebar nằm sát trái, rộng khoảng **300 px**. Nền trắng, có đường viền phải rất nhạt.

### 5.1. Logo CarePlus

Ở đầu sidebar có logo:

- Icon dấu cộng trong vòng tròn xanh.
- Text “CarePlus” màu xanh.
- Cỡ chữ logo khoảng 24–26 px, bold.
- Căn trái, cách mép trái khoảng 40 px, cách trên khoảng 35 px.

Bố cục:

```text
[icon +] CarePlus
```

### 5.2. Danh sách menu chính

Các item menu chính xếp dọc, mỗi item cao khoảng 55–60 px.

Mỗi item gồm:

- Icon bên trái.
- Text bên phải.
- Căn giữa theo chiều dọc.
- Khoảng cách icon đến text khoảng 18 px.
- Padding trái khoảng 40 px.

Danh sách menu theo đúng thứ tự:

1. Dashboard
2. Tiếp nhận bệnh nhân
3. Quản lý lịch hẹn
4. Danh sách bệnh nhân
5. Thanh toán & Hóa đơn
6. Dịch vụ & Gói khám
7. Thông báo
8. Báo cáo
9. Cài đặt

Item **Cài đặt** đang được chọn:

- Nền xanh nhạt.
- Text màu xanh.
- Icon màu tím/xanh hoặc xanh.
- Bo góc khoảng 8 px.
- Item active kéo dài gần hết chiều rộng sidebar, còn chừa lề trái/phải.

Các item khác:

- Nền trắng.
- Text màu đậm `#111827`.
- Icon nhiều màu khác nhau theo từng chức năng.

### 5.3. Nút đăng xuất

Nằm cuối sidebar, gần góc dưới trái.

Hiển thị:

```text
[icon logout đỏ] Đăng xuất
```

Đặc điểm:

- Text màu đỏ `#EF4444`.
- Icon đỏ.
- Căn trái giống các menu khác.

---

## 6. Header vùng nội dung chính

Vùng main bắt đầu bên phải sidebar.

### 6.1. Tiêu đề trang

Ở góc trên trái của vùng main:

```text
Cài đặt
```

- Font khoảng 22–24 px.
- Bold.
- Màu chữ `#1F2937`.

Bên dưới là breadcrumb:

```text
Trang chủ  >  Cài đặt
```

- Font khoảng 13–14 px.
- “Trang chủ” màu xanh/xám.
- Dấu `>` nhỏ.
- “Cài đặt” màu xám đậm.

### 6.2. Khu vực người dùng bên phải

Góc trên phải của vùng main có:

1. Icon chuông thông báo.
2. Badge đỏ số `3` ở góc trên icon chuông.
3. Avatar người dùng hình tròn nhỏ.
4. Tên người dùng: `Nguyễn Thị Lan`.
5. Icon mũi tên xổ xuống.

Bố cục ngang:

```text
[bell icon] [badge 3]   [avatar]  Nguyễn Thị Lan  [chevron down]
```

Kích thước:

- Avatar khoảng 34–40 px.
- Badge đỏ khoảng 16–18 px, chữ trắng.
- Text tên khoảng 14 px, bold nhẹ.

---

## 7. Khu vực nội dung cài đặt

Bên dưới header là khu vực cài đặt chính.

Bố cục gồm 2 cột:

```text
┌────────────────────┬──────────────────────────────────────────────────────┐
│ Menu cài đặt phụ   │ Nội dung chi tiết                                    │
│ rộng khoảng 270 px │ rộng phần còn lại                                    │
└────────────────────┴──────────────────────────────────────────────────────┘
```

Cả menu cài đặt phụ và các card nội dung đều nằm trong vùng main, cách mép trái/phải khoảng 25 px.

---

## 8. Menu cài đặt phụ bên trái

Menu này nằm trong một card trắng, border nhạt, bo góc 10–12 px.

Kích thước card khoảng:

- Rộng: 270 px.
- Cao: khoảng 455 px.

Các item xếp dọc, mỗi item cao khoảng 55–58 px.

Danh sách theo đúng thứ tự:

1. Thông tin cá nhân
2. Thông tin phòng khám
3. Quản lý người dùng
4. Phân quyền
5. Cài đặt lịch hẹn
6. Cài đặt thông báo
7. Cài đặt hóa đơn
8. Sao lưu & Khôi phục
9. Nhật ký hệ thống

Item đang active là **Thông tin cá nhân**.

### 8.1. Item active “Thông tin cá nhân”

- Nền xanh nhạt.
- Icon user màu xanh.
- Text màu xanh.
- Text bold.
- Bo góc 8 px.
- Có padding trái khoảng 22 px.

### 8.2. Các item còn lại

- Nền trắng.
- Icon màu xám xanh.
- Text màu `#374151`.
- Khi hover có thể đổi nền sang `#F3F4F6`.

---

## 9. Card “Thông tin cá nhân”

Card này nằm bên phải menu cài đặt phụ, ở hàng đầu tiên.

Kích thước khoảng:

- Rộng: phần còn lại, khoảng 940 px.
- Cao: khoảng 250 px.

Card có:

- Nền trắng.
- Border nhạt.
- Bo góc 10–12 px.
- Padding trong khoảng 24 px.

### 9.1. Tiêu đề card

Góc trên trái card:

```text
Thông tin cá nhân
```

- Font 16–17 px.
- Bold.

### 9.2. Nút “Lưu thay đổi”

Góc trên phải card có button xanh:

```text
[icon edit/save] Lưu thay đổi
```

Đặc điểm:

- Nền xanh `#00A86B`.
- Text trắng.
- Bo góc 7–8 px.
- Kích thước khoảng 125 x 38 px.
- Icon nhỏ màu trắng ở bên trái text.

### 9.3. Avatar cá nhân

Bên trái nội dung card có avatar lớn:

- Hình tròn.
- Kích thước khoảng 100 x 100 px.
- Hình minh họa nữ.
- Bên dưới/góc phải avatar có nút camera nhỏ.

Nút camera:

- Kích thước khoảng 30 x 30 px.
- Nền trắng.
- Border/đổ bóng nhẹ.
- Icon camera màu xanh/xám.
- Nằm đè lên mép dưới bên phải của avatar.

### 9.4. Các trường nhập thông tin

Các input được chia thành 3 cột chính ở bên phải avatar.

Hàng 1 gồm:

1. Họ và tên
2. Chức vụ
3. Email

Hàng 2 gồm:

1. Số điện thoại
2. Ngày sinh
3. Giới tính

Khoảng cách giữa các cột khoảng 20 px.

#### Trường “Họ và tên”

Label:

```text
Họ và tên
```

Input text:

```text
Nguyễn Thị Lan
```

Loại widget PyQt6 gợi ý: `QLineEdit`.

#### Trường “Chức vụ”

Label:

```text
Chức vụ
```

Combo box:

```text
Nhân viên lễ tân
```

Loại widget: `QComboBox`.

Có icon mũi tên xuống ở bên phải.

#### Trường “Email”

Label:

```text
Email
```

Input text:

```text
lan.nguyen@careplus.vn
```

Loại widget: `QLineEdit`.

#### Trường “Số điện thoại”

Label:

```text
Số điện thoại
```

Input text:

```text
0987 654 321
```

Loại widget: `QLineEdit`.

#### Trường “Ngày sinh”

Label:

```text
Ngày sinh
```

Input/date field:

```text
15/04/1995
```

Bên phải input có icon lịch.

Loại widget có thể dùng:

- `QDateEdit` với display format `dd/MM/yyyy`, hoặc
- `QLineEdit` + button icon calendar.

#### Trường “Giới tính”

Label:

```text
Giới tính
```

Combo box:

```text
Nữ
```

Loại widget: `QComboBox`.

### 9.5. Style input chung

Input/combo có:

- Cao khoảng 38–42 px.
- Border `#DDE3EA`.
- Bo góc 6 px.
- Padding trái 12 px.
- Nền trắng.
- Text màu `#374151`.
- Label nằm phía trên input, font nhỏ 12–13 px.

---

## 10. Card “Đổi mật khẩu”

Nằm ngay dưới card “Thông tin cá nhân”.

Kích thước:

- Rộng bằng card thông tin cá nhân.
- Cao khoảng 130 px.

### 10.1. Tiêu đề

Góc trên trái:

```text
Đổi mật khẩu
```

Font 16–17 px, bold.

### 10.2. Các trường mật khẩu

Có 3 input nằm ngang:

1. Mật khẩu hiện tại
2. Mật khẩu mới
3. Xác nhận mật khẩu mới

Mỗi input có label phía trên.

#### Input “Mật khẩu hiện tại”

Placeholder:

```text
Nhập mật khẩu hiện tại
```

Bên phải có icon con mắt để hiện/ẩn mật khẩu.

#### Input “Mật khẩu mới”

Placeholder:

```text
Nhập mật khẩu mới
```

Bên phải có icon con mắt.

#### Input “Xác nhận mật khẩu mới”

Placeholder:

```text
Nhập lại mật khẩu mới
```

Bên phải có icon con mắt.

Loại widget gợi ý:

- `QLineEdit`
- `setEchoMode(QLineEdit.Password)`
- Custom action icon eye ở bên phải.

### 10.3. Button “Đổi mật khẩu”

Nằm bên phải hàng input.

Text:

```text
Đổi mật khẩu
```

Đặc điểm:

- Nền xanh.
- Text trắng.
- Cao bằng input.
- Rộng khoảng 120–130 px.
- Bo góc 7–8 px.

---

## 11. Khu vực “Tùy chọn hệ thống” và “Logo phòng khám”

Hai phần này nằm trên cùng một hàng, ngay dưới card đổi mật khẩu.

Bố cục:

```text
┌──────────────────────────────────────┬──────────────────────────────┐
│ Tùy chọn hệ thống                    │ Logo phòng khám              │
└──────────────────────────────────────┴──────────────────────────────┘
```

Card tổng có border nhạt và bo góc. Có một đường chia dọc ở giữa.

---

## 12. Card “Tùy chọn hệ thống”

Nằm bên trái trong hàng này.

Kích thước khoảng:

- Rộng: 60–65% vùng nội dung.
- Cao: khoảng 270 px.

### 12.1. Tiêu đề

```text
Tùy chọn hệ thống
```

Font 16–17 px, bold.

### 12.2. Checkbox bên trái

Có 3 checkbox, đang đều được check màu xanh.

Danh sách:

1. `Tự động xác nhận lịch hẹn sau khi tạo`
2. `Hiển thị thông báo trên màn hình`
3. `Âm thanh khi có thông báo mới`

Widget gợi ý: `QCheckBox`.

Checkbox:

- Ô check nhỏ khoảng 14–16 px.
- Khi check có nền xanh và dấu tick trắng.
- Text font 13–14 px.

### 12.3. Combo box “Ngôn ngữ”

Label:

```text
Ngôn ngữ
```

Giá trị hiện tại:

```text
Tiếng Việt
```

Loại widget: `QComboBox`.

Có thể có options:

- Tiếng Việt
- English

### 12.4. Combo box “Giao diện”

Label:

```text
Giao diện
```

Giá trị hiện tại:

```text
Sáng
```

Options có thể gồm:

- Sáng
- Tối
- Theo hệ thống

### 12.5. Cột tùy chọn bên phải

Bên phải card có 3 combo box xếp dọc.

#### Định dạng ngày

Label:

```text
Định dạng ngày
```

Giá trị:

```text
dd/mm/yyyy
```

Options có thể gồm:

- dd/mm/yyyy
- mm/dd/yyyy
- yyyy-mm-dd

#### Định dạng giờ

Label:

```text
Định dạng giờ
```

Giá trị:

```text
24 giờ
```

Options:

- 24 giờ
- 12 giờ

#### Số bản ghi trên trang

Label:

```text
Số bản ghi trên trang
```

Giá trị:

```text
10 bản ghi
```

Options:

- 10 bản ghi
- 20 bản ghi
- 50 bản ghi
- 100 bản ghi

---

## 13. Card “Logo phòng khám”

Nằm bên phải card “Tùy chọn hệ thống”.

Kích thước khoảng:

- Rộng: 35–40% vùng nội dung.
- Cao bằng card tùy chọn hệ thống.

### 13.1. Tiêu đề

```text
Logo phòng khám
```

Font 16–17 px, bold.

### 13.2. Vùng preview logo

Ở giữa card có khung preview logo.

Đặc điểm:

- Khung vuông khoảng 135 x 135 px.
- Border xanh `#00A86B`.
- Bo góc 6–8 px.
- Bên trong hiển thị icon dấu cộng xanh và chữ `CarePlus` màu xanh.
- Nội dung căn giữa cả ngang và dọc.

Bố cục bên trong:

```text
   [+]
CarePlus
```

### 13.3. Button “Thay đổi logo”

Nằm dưới khung preview, bên trái.

Text:

```text
[icon upload] Thay đổi logo
```

Đặc điểm:

- Nền trắng.
- Border nhạt.
- Text màu xám xanh.
- Bo góc 6–8 px.
- Rộng khoảng 150 px.
- Cao khoảng 38 px.

Khi click:

- Mở `QFileDialog.getOpenFileName`.
- Chỉ cho chọn ảnh: `.png`, `.jpg`, `.jpeg`, `.webp`.
- Sau khi chọn thì cập nhật preview logo.

### 13.4. Button “Xóa”

Nằm dưới khung preview, bên phải button thay đổi logo.

Text:

```text
[icon trash] Xóa
```

Đặc điểm:

- Nền trắng hoặc hồng rất nhạt.
- Border đỏ nhạt.
- Text đỏ `#EF4444`.
- Bo góc 6–8 px.
- Rộng khoảng 80 px.
- Cao khoảng 38 px.

Khi click:

- Hỏi xác nhận trước khi xóa logo.
- Nếu xác nhận thì đưa logo về mặc định.

---

## 14. Card “Sao lưu dữ liệu”

Nằm bên dưới card “Tùy chọn hệ thống”, ở bên trái của hàng kế tiếp.

Kích thước:

- Rộng khoảng 50% vùng nội dung.
- Cao khoảng 160 px.

### 14.1. Tiêu đề

```text
Sao lưu dữ liệu
```

Font 16–17 px, bold.

### 14.2. Mô tả

Text mô tả:

```text
Sao lưu dữ liệu để bảo vệ thông tin phòng khám của bạn.
```

Font nhỏ, màu xám.

### 14.3. Dòng thời gian backup gần nhất

```text
Lần sao lưu gần nhất: 23/05/2026 10:15
```

Trong đó ngày giờ là ví dụ dữ liệu hiện tại trên ảnh.

### 14.4. Button “Sao lưu ngay”

Text:

```text
[icon database/backup] Sao lưu ngay
```

Đặc điểm:

- Nền xanh.
- Text trắng.
- Icon trắng.
- Rộng khoảng 135 px.
- Cao khoảng 40 px.
- Bo góc 7–8 px.

Khi click:

- Tạo file backup database.
- Có thể hiện progress/loading.
- Sau khi hoàn tất thông báo thành công.

### 14.5. Button “Xem lịch sử sao lưu”

Text:

```text
[icon clock] Xem lịch sử sao lưu
```

Đặc điểm:

- Nền trắng.
- Border nhạt.
- Text màu xám xanh.
- Rộng khoảng 185 px.
- Cao khoảng 40 px.
- Bo góc 7–8 px.

Khi click:

- Mở popup/table lịch sử backup.
- Hiển thị ngày giờ backup, tên file, dung lượng, người thao tác.

---

## 15. Card “Khôi phục dữ liệu”

Nằm bên phải card “Sao lưu dữ liệu”, cùng hàng.

Kích thước:

- Rộng khoảng 50% vùng nội dung.
- Cao bằng card sao lưu.

### 15.1. Tiêu đề

```text
Khôi phục dữ liệu
```

Font 16–17 px, bold.

### 15.2. Mô tả

```text
Khôi phục dữ liệu từ tệp sao lưu khi cần thiết.
```

Font nhỏ, màu xám.

### 15.3. Button “Chọn tệp sao lưu”

Text:

```text
[icon upload/file] Chọn tệp sao lưu
```

Đặc điểm:

- Nền trắng.
- Border nhạt.
- Text màu xám xanh.
- Rộng khoảng 160 px.
- Cao khoảng 40 px.
- Bo góc 7–8 px.

Khi click:

- Mở `QFileDialog.getOpenFileName`.
- Cho chọn file backup, ví dụ `.sql`, `.db`, `.zip`, `.bak` tùy hệ thống.

### 15.4. Button “Khôi phục”

Text:

```text
[icon trash/restore] Khôi phục
```

Đặc điểm:

- Nền đỏ nhạt hoặc trắng.
- Border đỏ nhạt.
- Text đỏ.
- Rộng khoảng 120 px.
- Cao khoảng 40 px.
- Bo góc 7–8 px.

Hành vi:

- Đây là thao tác nguy hiểm.
- Khi click phải hiện hộp thoại xác nhận.
- Nội dung cảnh báo nên nói rõ dữ liệu hiện tại có thể bị ghi đè.
- Chỉ tiếp tục restore nếu người dùng xác nhận.

---

## 16. Card “Thông tin hệ thống”

Nằm cuối vùng nội dung, kéo ngang gần hết chiều rộng vùng bên phải.

Kích thước:

- Rộng bằng vùng content bên phải.
- Cao khoảng 85–95 px.

### 16.1. Tiêu đề

Bên trái:

```text
Thông tin hệ thống
```

Font 16–17 px, bold.

### 16.2. Các thông tin hiển thị

Dạng các cột ngang, mỗi cột gồm label nhỏ phía trên và giá trị phía dưới.

Các cột theo thứ tự:

1. Phiên bản phần mềm
2. Cơ sở dữ liệu
3. Máy chủ
4. Dung lượng dữ liệu

Nội dung trong ảnh:

```text
Phiên bản phần mềm: 1.2.0
Cơ sở dữ liệu: careplus_db
Máy chủ: localhost
Dung lượng dữ liệu: 256.8 MB
```

### 16.3. Button “Kiểm tra cập nhật”

Nằm phía phải card.

Text:

```text
[icon refresh] Kiểm tra cập nhật
```

Đặc điểm:

- Nền trắng.
- Border nhạt.
- Text màu xám xanh.
- Rộng khoảng 165 px.
- Cao khoảng 40 px.
- Bo góc 7–8 px.

Khi click:

- Kiểm tra phiên bản mới.
- Hiển thị thông báo nếu đã là bản mới nhất hoặc có bản cập nhật.

---

## 17. Luồng thao tác thực tế

### 17.1. Chỉnh thông tin cá nhân

```text
Nhân viên đăng nhập
    ↓
Vào Cài đặt
    ↓
Chọn tab Thông tin cá nhân
    ↓
Sửa họ tên / email / số điện thoại / ngày sinh / giới tính / avatar
    ↓
Bấm Lưu thay đổi
    ↓
Validate dữ liệu
    ↓
Lưu vào database
    ↓
Cập nhật thông tin hiển thị ở topbar nếu tên/avatar thay đổi
```

Validate đề xuất:

- Họ tên không được rỗng.
- Email phải đúng định dạng.
- Số điện thoại chỉ nên gồm số, dấu cách, `+`, `-`.
- Ngày sinh phải hợp lệ.

### 17.2. Đổi mật khẩu

```text
Nhập mật khẩu hiện tại
    ↓
Nhập mật khẩu mới
    ↓
Nhập lại mật khẩu mới
    ↓
Bấm Đổi mật khẩu
    ↓
Kiểm tra mật khẩu hiện tại
    ↓
Kiểm tra mật khẩu mới và xác nhận có trùng nhau không
    ↓
Cập nhật password
    ↓
Thông báo thành công
```

Validate đề xuất:

- Mật khẩu hiện tại không được rỗng.
- Mật khẩu mới tối thiểu 8 ký tự.
- Mật khẩu mới và xác nhận mật khẩu phải giống nhau.
- Mật khẩu mới không được trùng mật khẩu cũ.

### 17.3. Thay đổi tùy chọn hệ thống

```text
Người dùng bật/tắt checkbox hoặc đổi combo box
    ↓
Bấm Lưu thay đổi hoặc tự động lưu tùy thiết kế
    ↓
Lưu config vào database/local settings
    ↓
Áp dụng lại giao diện/ngôn ngữ/format
```

### 17.4. Sao lưu dữ liệu

```text
Bấm Sao lưu ngay
    ↓
Hiện trạng thái đang sao lưu
    ↓
Tạo file backup
    ↓
Cập nhật “Lần sao lưu gần nhất”
    ↓
Thông báo thành công
```

### 17.5. Khôi phục dữ liệu

```text
Bấm Chọn tệp sao lưu
    ↓
Chọn file backup
    ↓
Bấm Khôi phục
    ↓
Hiện cảnh báo xác nhận
    ↓
Nếu đồng ý, tiến hành restore
    ↓
Thông báo kết quả
    ↓
Có thể yêu cầu khởi động lại app
```

---

## 18. Gợi ý cấu trúc PyQt6

### 18.1. Widget tổng

Có thể tổ chức class như sau:

```python
class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.connect_signals()
```

Layout tổng:

```text
QVBoxLayout window_layout
    └── QHBoxLayout app_layout
            ├── SidebarWidget
            └── MainSettingsWidget
```

Nếu đã có MainWindow chung thì `SettingsPage` chỉ là page nội dung, còn sidebar nằm ở layout cha.

### 18.2. Các component nên tách riêng

Nên chia thành các widget nhỏ:

```python
SidebarWidget
SettingsSubMenuWidget
PersonalInfoCard
ChangePasswordCard
SystemOptionsCard
ClinicLogoCard
BackupCard
RestoreCard
SystemInfoCard
```

### 18.3. Layout gợi ý

```python
main_layout = QVBoxLayout()
header_layout = QHBoxLayout()
content_layout = QHBoxLayout()

settings_menu = SettingsSubMenuWidget()
right_content = QVBoxLayout()

row_top = PersonalInfoCard()
row_password = ChangePasswordCard()
row_options_logo = QHBoxLayout()
row_backup_restore = QHBoxLayout()
row_system_info = SystemInfoCard()
```

### 18.4. Widget tương ứng

| Thành phần giao diện | Widget PyQt6 gợi ý |
|---|---|
| Sidebar | `QFrame` + `QVBoxLayout` |
| Menu item | `QPushButton` hoặc custom `QFrame` |
| Card | `QFrame` |
| Input text | `QLineEdit` |
| Combo box | `QComboBox` |
| Checkbox | `QCheckBox` |
| Date input | `QDateEdit` |
| Button | `QPushButton` |
| Avatar/logo | `QLabel` với `QPixmap` |
| Icon | `QIcon` hoặc FontAwesome/icon SVG |
| Badge thông báo | `QLabel` đặt absolute hoặc overlay layout |

---

## 19. Style QSS tham khảo

```css
QWidget {
    background-color: #FFFFFF;
    color: #1F2937;
    font-family: "Segoe UI";
    font-size: 14px;
}

QFrame#Card {
    background-color: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 12px;
}

QLineEdit, QComboBox, QDateEdit {
    height: 38px;
    border: 1px solid #DDE3EA;
    border-radius: 6px;
    padding-left: 10px;
    background-color: #FFFFFF;
    color: #374151;
}

QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
    border: 1px solid #00A86B;
}

QPushButton#PrimaryButton {
    background-color: #00A86B;
    color: white;
    border: none;
    border-radius: 7px;
    padding: 8px 16px;
    font-weight: 600;
}

QPushButton#PrimaryButton:hover {
    background-color: #00995F;
}

QPushButton#SecondaryButton {
    background-color: #FFFFFF;
    color: #4B5563;
    border: 1px solid #DDE3EA;
    border-radius: 7px;
    padding: 8px 16px;
    font-weight: 500;
}

QPushButton#DangerButton {
    background-color: #FFFFFF;
    color: #EF4444;
    border: 1px solid #FCA5A5;
    border-radius: 7px;
    padding: 8px 16px;
    font-weight: 600;
}

QPushButton#MenuActive {
    background-color: #EAF7F0;
    color: #00A86B;
    border: none;
    border-radius: 8px;
    text-align: left;
    padding-left: 18px;
    font-weight: 600;
}

QPushButton#MenuNormal {
    background-color: transparent;
    color: #374151;
    border: none;
    border-radius: 8px;
    text-align: left;
    padding-left: 18px;
}

QPushButton#MenuNormal:hover {
    background-color: #F3F4F6;
}

QCheckBox {
    spacing: 8px;
    color: #374151;
}

QCheckBox::indicator {
    width: 14px;
    height: 14px;
}
```

---

## 20. Dữ liệu mẫu cần hiển thị giống ảnh

Thông tin nhân viên:

```text
Họ và tên: Nguyễn Thị Lan
Chức vụ: Nhân viên lễ tân
Email: lan.nguyen@careplus.vn
Số điện thoại: 0987 654 321
Ngày sinh: 15/04/1995
Giới tính: Nữ
```

Tùy chọn hệ thống:

```text
Tự động xác nhận lịch hẹn sau khi tạo: bật
Hiển thị thông báo trên màn hình: bật
Âm thanh khi có thông báo mới: bật
Ngôn ngữ: Tiếng Việt
Giao diện: Sáng
Định dạng ngày: dd/mm/yyyy
Định dạng giờ: 24 giờ
Số bản ghi trên trang: 10 bản ghi
```

Sao lưu:

```text
Lần sao lưu gần nhất: 23/05/2026 10:15
```

Thông tin hệ thống:

```text
Phiên bản phần mềm: 1.2.0
Cơ sở dữ liệu: careplus_db
Máy chủ: localhost
Dung lượng dữ liệu: 256.8 MB
```

Thông báo topbar:

```text
Số thông báo chưa đọc: 3
Người dùng hiện tại: Nguyễn Thị Lan
```

---

## 21. Yêu cầu hành vi theo quyền staff

Vì đây là màn hình nhân viên, cần giới hạn quyền như sau:

### Staff được phép

- Chỉnh họ tên, số điện thoại, avatar cá nhân.
- Chỉnh email nếu hệ thống cho phép.
- Đổi mật khẩu.
- Đổi ngôn ngữ, giao diện, định dạng ngày giờ.
- Xem thông tin hệ thống cơ bản.
- Có thể sao lưu nếu nghiệp vụ cho phép.

### Staff không nên được phép

- Chỉnh phân quyền người dùng.
- Cấp quyền admin.
- Sửa database name/server trực tiếp.
- Restore dữ liệu nếu không có xác nhận/quyền nâng cao.
- Sửa cấu hình phòng khám lõi nếu không được cấp quyền.

Các item như “Thông tin phòng khám”, “Quản lý người dùng”, “Phân quyền”, “Cài đặt hóa đơn” có thể:

- Chỉ cho xem.
- Disable nút chỉnh sửa.
- Hoặc khi click báo “Bạn không có quyền thực hiện thao tác này”.

---

## 22. Checklist để dựng giao diện bằng PyQt6

Khi code màn hình này, cần đảm bảo có đủ các thành phần sau:

- [ ] Sidebar trái có logo CarePlus.
- [ ] Sidebar có đầy đủ 9 menu chính.
- [ ] Item “Cài đặt” trong sidebar đang active.
- [ ] Header có tiêu đề “Cài đặt”.
- [ ] Header có breadcrumb “Trang chủ > Cài đặt”.
- [ ] Header phải có chuông thông báo, badge số 3, avatar, tên user.
- [ ] Menu cài đặt phụ có đủ 9 mục.
- [ ] Mục “Thông tin cá nhân” đang active.
- [ ] Card “Thông tin cá nhân” có avatar, nút camera, 6 trường thông tin và nút lưu.
- [ ] Card “Đổi mật khẩu” có 3 input password và nút đổi mật khẩu.
- [ ] Card “Tùy chọn hệ thống” có 3 checkbox và 5 combo box.
- [ ] Card “Logo phòng khám” có preview logo, nút thay đổi logo, nút xóa.
- [ ] Card “Sao lưu dữ liệu” có mô tả, thời gian backup, 2 button.
- [ ] Card “Khôi phục dữ liệu” có mô tả, nút chọn tệp và nút khôi phục.
- [ ] Card “Thông tin hệ thống” có 4 thông tin và nút kiểm tra cập nhật.
- [ ] Button chính màu xanh, button nguy hiểm màu đỏ.
- [ ] Card có border nhạt, bo góc đều.
- [ ] Input có label rõ ràng, chiều cao đồng nhất.
- [ ] Layout không bị chen chúc khi resize cửa sổ.

---

## 23. Mô tả ngắn cho AI coding

Hãy dựng một màn hình desktop PyQt6 tên **SettingsPage** cho app **CarePlus STAFF**. Giao diện nền sáng, phong cách medical SaaS hiện đại. Bên trái là sidebar menu chính rộng khoảng 300px, có logo CarePlus ở trên và menu “Cài đặt” đang active màu xanh nhạt. Bên phải là vùng main có tiêu đề “Cài đặt”, breadcrumb “Trang chủ > Cài đặt”, topbar user gồm chuông thông báo badge 3, avatar và tên Nguyễn Thị Lan.

Trong vùng main, tạo layout 2 cột: menu cài đặt phụ rộng khoảng 270px bên trái và nội dung card bên phải. Menu phụ có 9 item, active là “Thông tin cá nhân”. Nội dung bên phải gồm các card trắng border nhạt bo góc 12px: card thông tin cá nhân có avatar, 6 field và nút “Lưu thay đổi”; card đổi mật khẩu có 3 password input và nút “Đổi mật khẩu”; card tùy chọn hệ thống có checkbox và combobox; card logo phòng khám có preview logo và nút thay/xóa; hàng sao lưu/khôi phục dữ liệu; cuối cùng là card thông tin hệ thống với phiên bản, database, máy chủ, dung lượng và nút kiểm tra cập nhật.