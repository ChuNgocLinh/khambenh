Dưới đây là mô tả chi tiết giao diện **CarePlus Admin – Quản lý bệnh nhân**, đủ để designer/dev có thể dựng lại gần như y hệt và suy luận các chức năng cần có.

---

# 1. Tổng quan màn hình

Đây là giao diện quản trị dành cho hệ thống y tế/phòng khám/bệnh viện tên **CarePlus Admin**. Màn hình hiện tại là trang **Quản lý bệnh nhân**, dùng để quản trị danh sách bệnh nhân, xem thống kê tổng quan, tìm kiếm, lọc, thêm mới, xuất Excel và thao tác từng hồ sơ bệnh nhân.

Giao diện có bố cục dạng **admin dashboard hiện đại**, nền sáng, nhiều khoảng trắng, bo góc mềm, màu chủ đạo là **xanh lá CarePlus** kết hợp xanh dương, cam, tím và đỏ cho các trạng thái.

Bố cục chính gồm 2 phần lớn:

1. **Sidebar bên trái**
   Chứa logo, menu điều hướng và nút đăng xuất.

2. **Khu vực nội dung bên phải**
   Chứa tiêu đề trang, breadcrumb, thanh người dùng, các thẻ thống kê, bộ lọc, bảng danh sách bệnh nhân và phân trang.

---

# 2. Kích thước và bố cục tổng thể

Màn hình đang hiển thị ở tỉ lệ desktop rộng.

## Layout tổng

* Toàn bộ trang chia thành:

  * Sidebar trái: khoảng **260–280px** chiều rộng.
  * Main content bên phải: chiếm phần còn lại.
* Nền tổng thể:

  * Sidebar: trắng hoặc gần trắng.
  * Main content: trắng ngà/xám rất nhạt `#F8FAFC` hoặc `#FAFBFF`.
* Các khối nội dung chính có nền trắng, bo góc, viền mờ.

## Sidebar

Sidebar chiếm toàn bộ chiều cao màn hình, cố định bên trái.

* Nền: trắng.
* Có đường phân cách nhẹ bên phải, màu xám rất nhạt.
* Padding ngang khoảng 16–24px.
* Logo nằm trên cùng.
* Menu nằm bên dưới logo.
* Nút **Đăng xuất** nằm cố định phía dưới cùng sidebar.

## Main content

Khu vực chính có padding lớn:

* Padding trái/phải khoảng 24–32px.
* Padding top khoảng 28–36px.
* Nội dung được chia thành các block:

  1. Header trang.
  2. Cards thống kê.
  3. Bộ lọc và nút thao tác.
  4. Bảng danh sách.
  5. Phân trang.

---

# 3. Sidebar chi tiết

## 3.1 Logo

Trên cùng bên trái là logo:

* Icon dấu cộng y tế màu xanh lá trong hình tròn.
* Text: **CarePlus Admin**
* Màu chữ:

  * “CarePlus”: xanh lá đậm.
  * “Admin”: xanh lá cùng tông.
* Font chữ đậm, kích thước khoảng 24–28px.
* Logo căn trái, cách mép trên khoảng 32px.

Có thể triển khai:

```text
[icon dấu cộng xanh] CarePlus Admin
```

## 3.2 Menu điều hướng

Menu gồm các mục sau, theo thứ tự từ trên xuống:

1. Dashboard
2. Quản lý tài khoản
3. Quản lý bác sĩ
4. Quản lý bệnh nhân
5. Quản lý thuốc
6. Quản lý dịch vụ
7. Quản lý thanh toán
8. Xem báo cáo thống kê
9. Phân quyền hệ thống
10. Sao lưu dữ liệu

Mỗi menu item gồm:

* Icon bên trái.
* Text bên phải.
* Chiều cao item khoảng 48–56px.
* Bo góc khoảng 8–12px.
* Khoảng cách giữa các item khoảng 6–10px.
* Icon màu xanh navy/xám đậm khi không active.
* Text màu xanh navy đậm.

## 3.3 Menu đang active

Mục đang active là:

```text
Quản lý bệnh nhân
```

Đặc điểm:

* Nền xanh lá rất nhạt, kiểu `#EAF8EF`.
* Text màu xanh lá.
* Icon màu xanh lá.
* Có cảm giác được highlight rõ nhưng nhẹ.
* Item bo góc khoảng 10–12px.
* Icon là biểu tượng nhóm người.

## 3.4 Nút Đăng xuất

Nằm cuối sidebar.

* Nền đỏ nhạt `#FFF1F1` hoặc hồng nhạt.
* Text đỏ.
* Icon logout đỏ.
* Kích thước gần bằng một menu item nhưng rộng hơn.
* Bo góc khoảng 8–10px.
* Text: **Đăng xuất**
* Khi hover có thể đậm màu hơn.

Chức năng suy đoán:

* Khi nhấn mở modal xác nhận:

  * “Bạn có chắc chắn muốn đăng xuất?”
  * Nút “Hủy”
  * Nút “Đăng xuất”
* Sau khi xác nhận thì xóa token/session và chuyển về trang đăng nhập.

---

# 4. Header khu vực nội dung

Phía trên cùng của main content có:

## 4.1 Tiêu đề trang

Bên trái:

```text
Quản lý bệnh nhân
```

* Font lớn, đậm.
* Kích thước khoảng 28–32px.
* Màu xanh navy rất đậm `#11152E`.
* Nằm gần góc trên trái của main content.

Bên dưới tiêu đề là breadcrumb:

```text
Dashboard / Quản lý bệnh nhân
```

* Font nhỏ hơn, khoảng 14–16px.
* Màu xám xanh.
* “Dashboard” có thể là link.
* Dấu `/` phân cách.
* “Quản lý bệnh nhân” là trang hiện tại.

## 4.2 Khu vực tài khoản admin

Góc trên phải có:

1. Icon chuông thông báo.
2. Badge đỏ số **3**.
3. Avatar admin.
4. Text: **Admin (Quản trị viên)**
5. Icon mũi tên xuống.

### Chuông thông báo

* Icon chuông màu xanh navy.
* Có badge đỏ nhỏ ở góc trên phải.
* Badge hiển thị số `3`.
* Khi click có thể mở dropdown thông báo.

Chức năng suy đoán:

* Hiển thị thông báo mới:

  * Bệnh nhân mới đăng ký.
  * Hồ sơ cần xác minh.
  * Cảnh báo hệ thống.
  * Lịch hẹn sắp tới.
* Có trạng thái đã đọc/chưa đọc.
* Có nút “Xem tất cả”.

### Avatar admin

* Avatar dạng hình tròn.
* Có thể dùng ảnh hoặc icon người mặc vest.
* Bên cạnh là tên quyền:

```text
Admin (Quản trị viên)
```

* Có mũi tên dropdown.
* Khi click mở menu:

  * Hồ sơ cá nhân.
  * Đổi mật khẩu.
  * Cài đặt tài khoản.
  * Đăng xuất.

---

# 5. Khối thống kê tổng quan

Ngay dưới header là 4 card thống kê nằm ngang.

Các card có cùng phong cách:

* Nền trắng.
* Bo góc khoảng 14–18px.
* Viền rất nhạt.
* Shadow nhẹ hoặc border xám.
* Padding khoảng 20–24px.
* Chiều cao khoảng 130–150px.
* Mỗi card có icon lớn bên trái và nội dung bên phải.
* Icon đặt trong hình chữ nhật bo góc, màu nền gradient hoặc màu đậm.
* Text tiêu đề nhỏ, giá trị lớn.

## 5.1 Card 1: Tổng bệnh nhân

Nội dung:

```text
Tổng bệnh nhân
3.256
↑ 12% so với tháng trước
```

Chi tiết visual:

* Icon nhóm người màu trắng nằm trong ô xanh dương.
* Nền icon: xanh dương gradient.
* Số `3.256` màu xanh dương.
* Dòng tăng trưởng có mũi tên lên màu xanh lá.
* `12%` màu xanh lá, phần “so với tháng trước” màu xám.

Chức năng suy đoán:

* Thể hiện tổng số bệnh nhân hiện có trong hệ thống.
* So sánh với tháng trước.
* Có thể lấy từ API thống kê:

  * `totalPatients`
  * `growthPercent`
  * `growthPeriod`

## 5.2 Card 2: Bệnh nhân mới

Nội dung:

```text
Bệnh nhân mới
128
↑ 8% so với tháng trước
```

Visual:

* Icon trái tim/y tế màu trắng trong ô xanh lá.
* Số `128` màu xanh lá.
* Dòng tăng trưởng xanh lá.

Chức năng suy đoán:

* Đếm bệnh nhân mới trong tháng hiện tại.
* So sánh số bệnh nhân mới với tháng trước.
* Có thể dùng để theo dõi tăng trưởng người dùng/bệnh nhân.

## 5.3 Card 3: Bệnh nhân nam

Nội dung:

```text
Bệnh nhân nam
1.582
48,6% tổng số
```

Visual:

* Icon người màu trắng trong ô cam.
* Số `1.582` màu cam.
* Dòng phụ: `48,6% tổng số`.

Chức năng suy đoán:

* Đếm số bệnh nhân giới tính nam.
* Tính phần trăm trên tổng bệnh nhân.
* Dữ liệu cần đồng bộ với filter giới tính trong bảng.

## 5.4 Card 4: Bệnh nhân nữ

Nội dung:

```text
Bệnh nhân nữ
1.674
51,4% tổng số
```

Visual:

* Icon người màu trắng trong ô tím.
* Số `1.674` màu tím.
* Dòng phụ: `51,4% tổng số`.

Chức năng suy đoán:

* Đếm số bệnh nhân giới tính nữ.
* Tính phần trăm nữ trên tổng bệnh nhân.

---

# 6. Khu vực bộ lọc và thao tác

Bên dưới các card thống kê là một khối lớn chứa bộ lọc, nút thao tác và bảng.

Khối này:

* Nền trắng.
* Bo góc lớn khoảng 16px.
* Viền mờ.
* Padding trên khoảng 20px.
* Có thể coi là `PatientListCard`.

## 6.1 Thanh tìm kiếm

Nằm bên trái hàng filter.

Placeholder:

```text
Tìm kiếm bệnh nhân (Tên, SDT, CCCD, Email...)
```

Đặc điểm:

* Input rộng nhất trong hàng filter.
* Có icon kính lúp bên trái.
* Nền trắng.
* Border xám nhạt.
* Bo góc 8–10px.
* Chiều cao khoảng 44–48px.
* Padding trái đủ để icon và text không dính nhau.
* Text placeholder màu xám xanh.

Chức năng suy đoán:

Tìm kiếm bệnh nhân theo:

* Họ và tên.
* Số điện thoại.
* CCCD/CMND.
* Email.
* Có thể thêm mã bệnh nhân nếu hệ thống có.

Nên hỗ trợ:

* Debounce khoảng 300–500ms.
* Tìm kiếm không phân biệt hoa thường.
* Tìm kiếm tiếng Việt có dấu/không dấu.
* Khi nhập text, bảng tự reload về trang 1.
* Có nút clear `x` khi input có giá trị.

## 6.2 Filter giới tính

Label:

```text
Giới tính
```

Dropdown mặc định:

```text
Tất cả
```

Option nên có:

* Tất cả
* Nam
* Nữ
* Khác / Không xác định

Visual:

* Label nằm trên dropdown.
* Dropdown bo góc.
* Có icon mũi tên xuống bên phải.
* Chiều rộng khoảng 140–160px.

Chức năng:

* Lọc danh sách theo giới tính.
* Khi chọn, gọi API hoặc lọc client-side.
* Reset về page 1.

## 6.3 Filter nhóm tuổi

Label:

```text
Nhóm tuổi
```

Dropdown mặc định:

```text
Tất cả
```

Option gợi ý:

* Tất cả
* Dưới 18
* 18–30
* 31–45
* 46–60
* Trên 60

Hoặc theo nghiệp vụ y tế:

* Trẻ em
* Thanh thiếu niên
* Người trưởng thành
* Trung niên
* Người cao tuổi

Chức năng:

* Lọc theo ngày sinh.
* Backend có thể nhận `ageGroup`.
* Frontend có thể tính tuổi từ `dateOfBirth`.

## 6.4 Filter trạng thái

Label:

```text
Trạng thái
```

Dropdown mặc định:

```text
Tất cả
```

Option nên có:

* Tất cả
* Hoạt động
* Tạm khóa
* Ngưng hoạt động

Chức năng:

* Lọc theo trạng thái tài khoản/hồ sơ bệnh nhân.
* Có thể dùng để tìm bệnh nhân bị khóa, ngưng dùng dịch vụ.

## 6.5 Nút Thêm bệnh nhân

Nằm bên phải hàng filter, phía trên nút Xuất Excel.

Text:

```text
+ Thêm bệnh nhân
```

Visual:

* Nút màu xanh lá đậm.
* Icon dấu cộng màu trắng.
* Text trắng.
* Bo góc 8–10px.
* Chiều cao khoảng 44–48px.
* Padding ngang rộng.
* Font medium/semibold.

Chức năng:

* Mở form/modal thêm bệnh nhân.
* Hoặc điều hướng sang trang `/patients/create`.

Thông tin form thêm bệnh nhân nên có:

* Họ và tên.
* Giới tính.
* Ngày sinh.
* Số điện thoại.
* CCCD/CMND.
* Email.
* Địa chỉ.
* Trạng thái.
* Ảnh đại diện.
* Thông tin bảo hiểm y tế nếu có.
* Người liên hệ khẩn cấp nếu có.
* Ghi chú y tế nếu có.

Validation:

* Họ tên bắt buộc.
* Số điện thoại đúng định dạng.
* Email đúng định dạng.
* CCCD/CMND không trùng.
* Ngày sinh không được lớn hơn ngày hiện tại.
* Trạng thái mặc định là Hoạt động.

## 6.6 Nút Xuất Excel

Nằm dưới nút Thêm bệnh nhân hoặc cùng cột bên phải.

Text:

```text
Xuất Excel
```

Visual:

* Nút nền trắng.
* Border xám nhạt.
* Icon Excel màu xanh lá.
* Text màu xanh navy/xám đậm.
* Bo góc 8–10px.
* Chiều cao khoảng 44px.

Chức năng:

* Xuất danh sách bệnh nhân ra file Excel.
* Có thể xuất:

  * Toàn bộ danh sách.
  * Danh sách theo bộ lọc hiện tại.
  * Các dòng đã tick checkbox.
* File có thể tên dạng:

  * `danh-sach-benh-nhan.xlsx`
  * `patients_YYYYMMDD.xlsx`

Cột Excel nên gồm:

* STT.
* Họ và tên.
* Giới tính.
* Ngày sinh.
* Số điện thoại.
* CCCD/CMND.
* Email.
* Địa chỉ.
* Trạng thái.
* Ngày tạo hồ sơ.
* Ngày cập nhật gần nhất.

---

# 7. Bảng danh sách bệnh nhân

Bảng là phần chính của màn hình.

## 7.1 Cấu trúc bảng

Các cột hiển thị:

1. Checkbox chọn dòng
2. STT
3. Họ và tên
4. Giới tính
5. Ngày sinh
6. SĐT
7. CCCD/CMND
8. Email
9. Địa chỉ
10. Trạng thái
11. Thao tác

Header bảng có nền trắng, chữ đậm, màu xanh navy.

Mỗi dòng:

* Chiều cao khoảng 58–64px.
* Border-bottom rất mờ.
* Text màu xanh navy đậm.
* Có hover state màu xám xanh rất nhạt.
* Checkbox ở đầu dòng.
* Cột họ tên có avatar nhỏ.

## 7.2 Checkbox

Có checkbox ở header và từng dòng.

Chức năng:

* Checkbox header chọn tất cả dòng trong trang hiện tại.
* Checkbox từng dòng chọn một bệnh nhân.
* Khi có dòng được chọn có thể hiện thanh thao tác hàng loạt:

  * Xóa nhiều.
  * Khóa nhiều.
  * Kích hoạt nhiều.
  * Xuất Excel các dòng đã chọn.
  * Gán nhãn/nhóm nếu hệ thống có.

## 7.3 Cột STT

Hiển thị số thứ tự từ 1 đến 10 ở trang hiện tại.

Ví dụ:

```text
1
2
3
...
10
```

Khi qua trang mới, STT nên tính theo phân trang:

```text
STT = (currentPage - 1) * pageSize + rowIndex + 1
```

## 7.4 Cột Họ và tên

Mỗi bệnh nhân có:

* Avatar nhỏ bên trái.
* Tên bệnh nhân bên phải.

Avatar trong ảnh là icon minh họa nam/nữ:

* Nam: avatar nam mặc áo.
* Nữ: avatar nữ tóc dài.

Tên bệnh nhân được in đậm vừa.

Danh sách đang hiển thị:

1. Nguyễn Văn Nam
2. Trần Thị Mai
3. Lê Văn Cường
4. Phạm Thị Lan
5. Hoàng Anh Tuấn
6. Vũ Thị Hương
7. Đỗ Minh Quân
8. Nguyễn Thị Hoa
9. Bùi Văn Dũng
10. Trương Thị Kiều

Chức năng suy đoán:

* Click vào tên hoặc avatar có thể mở trang chi tiết bệnh nhân.
* Avatar mặc định theo giới tính nếu chưa có ảnh upload.
* Có thể hiển thị mã bệnh nhân phụ bên dưới tên nếu cần.

## 7.5 Cột Giới tính

Hiển thị bằng icon:

* Nam: ký hiệu nam màu xanh dương.
* Nữ: ký hiệu nữ màu hồng.

Không hiển thị chữ, chỉ dùng icon.

Nên có tooltip khi hover:

```text
Nam
```

hoặc

```text
Nữ
```

Để dễ tiếp cận, icon nên có `aria-label`.

## 7.6 Cột Ngày sinh

Format:

```text
DD/MM/YYYY
```

Ví dụ:

```text
15/05/1990
22/08/1988
03/06/1975
12/11/1992
30/09/1985
05/09/1991
18/01/2000
25/12/1970
02/03/1982
09/07/1995
```

Chức năng suy đoán:

* Có thể sort theo tuổi/ngày sinh.
* Có thể dùng để tính nhóm tuổi.
* Khi xem chi tiết, hiển thị thêm tuổi.

## 7.7 Cột SĐT

Hiển thị số điện thoại dạng nhóm 3 chữ số:

Ví dụ:

```text
0987 654 321
0912 345 678
0933 456 789
0909 876 543
0988 765 432
0977 654 321
0966 543 210
0908 111 222
0982 333 444
0933 999 000
```

Chức năng suy đoán:

* Click có thể gọi điện nếu thiết bị hỗ trợ.
* Có thể copy nhanh số điện thoại.
* Số điện thoại cần unique hoặc ít nhất được kiểm tra trùng.

## 7.8 Cột CCCD/CMND

Hiển thị số giấy tờ tùy thân.

Ví dụ:

```text
123456789012
234567890123
345678901234
456789012345
567890123456
678901234567
789012345678
890123456789
901234567890
012345678901
```

Chức năng suy đoán:

* Dùng để định danh bệnh nhân.
* Nên kiểm tra trùng khi thêm/sửa.
* Có thể bị ẩn một phần theo quyền hạn, ví dụ `1234******12`, nhưng giao diện này đang hiển thị đầy đủ.

## 7.9 Cột Email

Hiển thị email bệnh nhân.

Ví dụ:

```text
nam.nguyen@gmail.com
mai.tran@gmail.com
cuong.le@gmail.com
lan.pham@gmail.com
tuan.hoang@gmail.com
huong.vu@gmail.com
quan.do@gmail.com
hoa.nguyen@gmail.com
dung.bui@gmail.com
kieu.truong@gmail.com
```

Chức năng suy đoán:

* Click có thể mở mail client.
* Email dùng cho đăng nhập/tài khoản bệnh nhân.
* Có thể dùng gửi thông báo lịch hẹn, kết quả khám, nhắc tái khám.

## 7.10 Cột Địa chỉ

Hiển thị tỉnh/thành phố hoặc địa chỉ rút gọn.

Ví dụ:

```text
TP. Hồ Chí Minh
Hà Nội
Đà Nẵng
Hải Phòng
Cần Thơ
Bình Dương
Đồng Nai
Nghệ An
Thanh Hóa
TP. Hồ Chí Minh
```

Chức năng suy đoán:

* Có thể chỉ hiển thị tỉnh/thành ở bảng để tránh quá dài.
* Trang chi tiết sẽ có địa chỉ đầy đủ:

  * Số nhà.
  * Đường.
  * Phường/xã.
  * Quận/huyện.
  * Tỉnh/thành.

## 7.11 Cột Trạng thái

Hiển thị badge màu theo trạng thái.

Các trạng thái trong ảnh:

### Hoạt động

```text
Hoạt động
```

* Nền xanh lá nhạt.
* Text xanh lá.
* Bo tròn pill.
* Phần lớn bệnh nhân đang ở trạng thái này.

### Tạm khóa

```text
Tạm khóa
```

* Nền cam/vàng nhạt.
* Text cam.
* Xuất hiện ở dòng Đỗ Minh Quân.

### Ngưng hoạt động

```text
Ngưng hoạt động
```

* Nền đỏ/hồng nhạt.
* Text đỏ.
* Xuất hiện ở dòng Bùi Văn Dũng.

Chức năng suy đoán:

* Hoạt động: bệnh nhân có thể đăng nhập/đặt lịch/sử dụng dịch vụ.
* Tạm khóa: tài khoản bị khóa tạm, có thể mở lại.
* Ngưng hoạt động: hồ sơ không còn dùng nữa, không nên xóa hoàn toàn để giữ lịch sử y tế.

## 7.12 Cột Thao tác

Mỗi dòng có 3 icon thao tác:

1. Xem chi tiết
2. Chỉnh sửa
3. Xóa

### Icon xem

* Icon hình con mắt.
* Màu xanh dương.
* Nằm trong button nhỏ nền xanh rất nhạt.
* Khi click mở chi tiết bệnh nhân.

Chức năng trang chi tiết nên có:

* Thông tin cá nhân.
* Hồ sơ bệnh án.
* Lịch sử khám.
* Lịch hẹn.
* Đơn thuốc.
* Thanh toán.
* Ghi chú bác sĩ.
* Tệp đính kèm nếu có.

### Icon sửa

* Icon bút chì.
* Màu xanh dương.
* Button nhỏ nền xanh rất nhạt.
* Khi click mở form chỉnh sửa.

Chức năng:

* Sửa thông tin bệnh nhân.
* Cập nhật trạng thái.
* Thay avatar.
* Cập nhật địa chỉ, email, số điện thoại.
* Lưu lịch sử chỉnh sửa.

### Icon xóa

* Icon thùng rác.
* Màu đỏ.
* Button nhỏ nền đỏ rất nhạt.
* Khi click mở modal xác nhận.

Nên dùng soft delete thay vì xóa thật:

* Đổi trạng thái thành “Ngưng hoạt động”.
* Hoặc đánh dấu `deleted_at`.
* Giữ lại lịch sử khám, thanh toán, đơn thuốc.

Modal xác nhận:

```text
Xóa bệnh nhân?
Bạn có chắc chắn muốn xóa hồ sơ bệnh nhân này không? Hành động này có thể ảnh hưởng đến dữ liệu liên quan.

[Hủy] [Xóa]
```

---

# 8. Dữ liệu mẫu đang hiển thị trong bảng

Có thể mô phỏng bảng bằng dữ liệu sau:

| STT | Họ và tên       | Giới tính | Ngày sinh  | SĐT          | CCCD/CMND    | Email                                                 | Địa chỉ         | Trạng thái      |
| --: | --------------- | --------- | ---------- | ------------ | ------------ | ----------------------------------------------------- | --------------- | --------------- |
|   1 | Nguyễn Văn Nam  | Nam       | 15/05/1990 | 0987 654 321 | 123456789012 | [nam.nguyen@gmail.com](mailto:nam.nguyen@gmail.com)   | TP. Hồ Chí Minh | Hoạt động       |
|   2 | Trần Thị Mai    | Nữ        | 22/08/1988 | 0912 345 678 | 234567890123 | [mai.tran@gmail.com](mailto:mai.tran@gmail.com)       | Hà Nội          | Hoạt động       |
|   3 | Lê Văn Cường    | Nam       | 03/06/1975 | 0933 456 789 | 345678901234 | [cuong.le@gmail.com](mailto:cuong.le@gmail.com)       | Đà Nẵng         | Hoạt động       |
|   4 | Phạm Thị Lan    | Nữ        | 12/11/1992 | 0909 876 543 | 456789012345 | [lan.pham@gmail.com](mailto:lan.pham@gmail.com)       | Hải Phòng       | Hoạt động       |
|   5 | Hoàng Anh Tuấn  | Nam       | 30/09/1985 | 0988 765 432 | 567890123456 | [tuan.hoang@gmail.com](mailto:tuan.hoang@gmail.com)   | Cần Thơ         | Hoạt động       |
|   6 | Vũ Thị Hương    | Nữ        | 05/09/1991 | 0977 654 321 | 678901234567 | [huong.vu@gmail.com](mailto:huong.vu@gmail.com)       | Bình Dương      | Hoạt động       |
|   7 | Đỗ Minh Quân    | Nam       | 18/01/2000 | 0966 543 210 | 789012345678 | [quan.do@gmail.com](mailto:quan.do@gmail.com)         | Đồng Nai        | Tạm khóa        |
|   8 | Nguyễn Thị Hoa  | Nữ        | 25/12/1970 | 0908 111 222 | 890123456789 | [hoa.nguyen@gmail.com](mailto:hoa.nguyen@gmail.com)   | Nghệ An         | Hoạt động       |
|   9 | Bùi Văn Dũng    | Nam       | 02/03/1982 | 0982 333 444 | 901234567890 | [dung.bui@gmail.com](mailto:dung.bui@gmail.com)       | Thanh Hóa       | Ngưng hoạt động |
|  10 | Trương Thị Kiều | Nữ        | 09/07/1995 | 0933 999 000 | 012345678901 | [kieu.truong@gmail.com](mailto:kieu.truong@gmail.com) | TP. Hồ Chí Minh | Hoạt động       |

---

# 9. Phân trang

Phía dưới bảng có phần phân trang.

Bên trái:

```text
Hiển thị [10 ▼] bản ghi
```

Trong đó dropdown `10` cho biết số bản ghi mỗi trang.

Option nên có:

* 10
* 20
* 50
* 100

Ở giữa/phải là pagination:

```text
<  1  2  3  4  5  ...  326  >
```

Chi tiết:

* Trang hiện tại là `1`, nền xanh lá, chữ trắng.
* Các trang khác nền trắng, border xám nhạt.
* Có nút previous `<`.
* Có nút next `>`.
* Có dấu `...` trước trang cuối.
* Trang cuối là `326`.

Suy luận:

* Tổng bệnh nhân là 3.256.
* Mỗi trang 10 bản ghi.
* Số trang là khoảng 326.
* Điều này khớp với card tổng bệnh nhân `3.256`.

Chức năng:

* Click số trang để chuyển trang.
* Click next/previous.
* Khi đổi filter/search, reset về trang 1.
* Khi đổi page size, tính lại tổng số trang.
* URL có thể lưu query:

  * `/patients?page=1&pageSize=10&gender=all&status=all`

---

# 10. Màu sắc chủ đạo

Có thể dùng bảng màu sau để dựng lại:

## Màu chính

```css
--primary-green: #00A651;
--primary-green-dark: #008C44;
--primary-green-light: #EAF8EF;
```

## Màu chữ

```css
--text-primary: #11152E;
--text-secondary: #5B6478;
--text-muted: #8A94A6;
```

## Màu nền

```css
--page-bg: #F8FAFC;
--card-bg: #FFFFFF;
--border-color: #E7EAF0;
```

## Màu trạng thái

```css
--success-bg: #E8F8EF;
--success-text: #009B50;

--warning-bg: #FFF4E5;
--warning-text: #F59E0B;

--danger-bg: #FFEAEA;
--danger-text: #EF4444;
```

## Màu card thống kê

```css
--blue: #2563EB;
--green: #00A651;
--orange: #F97316;
--purple: #7E22CE;
```

---

# 11. Typography

Giao diện dùng font sans-serif hiện đại, có thể dùng:

* Inter
* Roboto
* Open Sans
* SF Pro Display
* Arial nếu đơn giản

Gợi ý kích thước:

```css
Title page: 28px - 32px, font-weight: 700
Breadcrumb: 14px - 15px, font-weight: 400
Card label: 15px - 16px, font-weight: 600
Card number: 28px - 32px, font-weight: 700
Table header: 13px - 14px, font-weight: 700
Table body: 13px - 14px, font-weight: 500
Button: 14px - 15px, font-weight: 600
Sidebar item: 15px - 16px, font-weight: 500
```

---

# 12. Spacing và bo góc

Gợi ý CSS:

```css
Sidebar width: 280px
Main padding: 28px 32px
Card border-radius: 16px
Button border-radius: 8px
Input border-radius: 8px
Table container border-radius: 16px
Card padding: 22px
Table row height: 60px
Gap giữa statistic cards: 20px
Gap giữa filter controls: 20px
```

---

# 13. Chức năng backend/API cần có

Trang này nên có các API sau.

## 13.1 Lấy thống kê bệnh nhân

```http
GET /api/admin/patients/statistics
```

Response gợi ý:

```json
{
  "totalPatients": 3256,
  "totalGrowthPercent": 12,
  "newPatients": 128,
  "newPatientsGrowthPercent": 8,
  "malePatients": 1582,
  "malePercent": 48.6,
  "femalePatients": 1674,
  "femalePercent": 51.4
}
```

## 13.2 Lấy danh sách bệnh nhân

```http
GET /api/admin/patients
```

Query params:

```text
page=1
limit=10
keyword=
gender=all
ageGroup=all
status=all
sortBy=createdAt
sortOrder=desc
```

Response gợi ý:

```json
{
  "data": [
    {
      "id": "patient_001",
      "fullName": "Nguyễn Văn Nam",
      "gender": "male",
      "dateOfBirth": "1990-05-15",
      "phone": "0987654321",
      "identityNumber": "123456789012",
      "email": "nam.nguyen@gmail.com",
      "address": "TP. Hồ Chí Minh",
      "status": "active",
      "avatarUrl": null
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "totalItems": 3256,
    "totalPages": 326
  }
}
```

## 13.3 Thêm bệnh nhân

```http
POST /api/admin/patients
```

## 13.4 Xem chi tiết bệnh nhân

```http
GET /api/admin/patients/{id}
```

## 13.5 Cập nhật bệnh nhân

```http
PUT /api/admin/patients/{id}
```

## 13.6 Xóa hoặc ngưng hoạt động bệnh nhân

```http
DELETE /api/admin/patients/{id}
```

Hoặc nên dùng:

```http
PATCH /api/admin/patients/{id}/status
```

với body:

```json
{
  "status": "inactive"
}
```

## 13.7 Xuất Excel

```http
GET /api/admin/patients/export
```

Query params giống bộ lọc hiện tại.

---

# 14. Các màn hình/modal nên có liên quan

## 14.1 Modal thêm bệnh nhân

Nên là modal lớn hoặc trang riêng.

Các section:

1. Thông tin cá nhân
2. Thông tin liên hệ
3. Thông tin định danh
4. Địa chỉ
5. Trạng thái tài khoản
6. Ghi chú

Các nút:

```text
[Hủy] [Lưu bệnh nhân]
```

## 14.2 Modal sửa bệnh nhân

Tương tự modal thêm, nhưng dữ liệu được fill sẵn.

Nút:

```text
[Hủy] [Cập nhật]
```

## 14.3 Modal xem chi tiết

Có thể là drawer trượt từ phải sang hoặc trang chi tiết.

Nên hiển thị:

* Avatar.
* Họ tên.
* Trạng thái.
* Tuổi.
* Giới tính.
* SĐT.
* Email.
* CCCD/CMND.
* Địa chỉ.
* Lịch sử khám.
* Lịch hẹn.
* Đơn thuốc.
* Thanh toán.
* Ghi chú.

## 14.4 Modal xác nhận xóa

Nội dung nên rõ ràng, tránh xóa nhầm.

Có thể ghi:

```text
Bạn có chắc chắn muốn xóa bệnh nhân “Nguyễn Văn Nam”?
Dữ liệu bệnh án liên quan sẽ được giữ lại để phục vụ tra cứu.
```

Nút:

```text
[Hủy] [Xóa]
```

---

# 15. Trạng thái giao diện cần xử lý

## Loading

Khi tải dữ liệu:

* Card thống kê hiển thị skeleton.
* Bảng hiển thị skeleton rows.
* Nút bị disabled nếu đang export hoặc submit.

## Empty state

Nếu không có bệnh nhân:

```text
Không tìm thấy bệnh nhân nào
Hãy thử thay đổi bộ lọc hoặc thêm bệnh nhân mới.
```

Có thể có nút:

```text
+ Thêm bệnh nhân
```

## Error state

Nếu API lỗi:

```text
Không thể tải danh sách bệnh nhân
Vui lòng thử lại.
```

Có nút:

```text
Thử lại
```

## No search result

Khi search không có kết quả:

```text
Không tìm thấy bệnh nhân phù hợp với từ khóa “...”
```

## Permission denied

Nếu admin không có quyền:

* Ẩn nút thêm/sửa/xóa.
* Chỉ cho xem danh sách.
* Hoặc hiện thông báo:

```text
Bạn không có quyền thực hiện thao tác này.
```

---

# 16. Phân quyền suy đoán

Vì sidebar có mục **Phân quyền hệ thống**, trang này nên hỗ trợ role-based access control.

Các quyền có thể có:

```text
patient.view
patient.create
patient.update
patient.delete
patient.export
patient.lock
patient.unlock
```

Ví dụ:

* Quản trị viên: toàn quyền.
* Nhân viên lễ tân: xem, thêm, sửa thông tin cơ bản.
* Bác sĩ: xem hồ sơ và lịch sử khám, không được xóa.
* Kế toán: chỉ xem thông tin liên quan thanh toán.
* Nhân viên thường: quyền giới hạn.

---

# 17. Tương tác chi tiết nên có

## Search

* Người dùng nhập từ khóa.
* Sau 300ms tự gọi API.
* Hiển thị loading trong bảng.
* Reset page về 1.

## Filter

* Chọn giới tính, nhóm tuổi, trạng thái.
* Có thể kết hợp nhiều filter.
* URL nên cập nhật query params để reload vẫn giữ filter.

## Add patient

* Click **Thêm bệnh nhân**.
* Mở modal/form.
* Submit thành công:

  * Đóng modal.
  * Toast: “Thêm bệnh nhân thành công”.
  * Reload bảng.
  * Cập nhật card thống kê nếu cần.

## Edit patient

* Click icon bút chì.
* Load thông tin chi tiết.
* Mở form sửa.
* Submit thành công:

  * Toast: “Cập nhật bệnh nhân thành công”.
  * Reload dòng tương ứng.

## Delete patient

* Click icon thùng rác.
* Mở modal xác nhận.
* Xác nhận:

  * Soft delete hoặc chuyển trạng thái.
  * Toast: “Xóa bệnh nhân thành công”.
  * Reload bảng.

## View patient

* Click icon mắt.
* Mở trang/modal chi tiết.
* Có thể có tab:

  * Tổng quan.
  * Lịch sử khám.
  * Đơn thuốc.
  * Thanh toán.
  * Tệp hồ sơ.

## Export Excel

* Click **Xuất Excel**.
* Button chuyển loading:

```text
Đang xuất...
```

* Sau khi export xong tải file về.
* Nếu lỗi:

```text
Xuất Excel thất bại. Vui lòng thử lại.
```

---

# 18. Gợi ý cấu trúc component frontend

Nếu làm bằng React/Vue/Angular, có thể tách như sau:

```text
AdminLayout
 ├── Sidebar
 │    ├── Logo
 │    ├── SidebarMenu
 │    └── LogoutButton
 │
 └── MainContent
      ├── Topbar
      │    ├── PageTitle
      │    ├── Breadcrumb
      │    ├── NotificationBell
      │    └── UserDropdown
      │
      ├── PatientStats
      │    ├── StatCard total
      │    ├── StatCard new
      │    ├── StatCard male
      │    └── StatCard female
      │
      └── PatientTableSection
           ├── PatientFilters
           │    ├── SearchInput
           │    ├── GenderSelect
           │    ├── AgeGroupSelect
           │    ├── StatusSelect
           │    ├── AddPatientButton
           │    └── ExportExcelButton
           │
           ├── PatientTable
           │    ├── TableHeader
           │    ├── PatientRow
           │    └── RowActions
           │
           └── Pagination
```

---

# 19. Gợi ý database cho bệnh nhân

Bảng `patients` có thể gồm:

```text
id
full_name
gender
date_of_birth
phone
email
identity_number
address_line
ward
district
province
avatar_url
status
created_at
updated_at
deleted_at
created_by
updated_by
```

Nếu liên kết với tài khoản đăng nhập:

```text
user_id
```

Nếu có nghiệp vụ y tế sâu hơn:

```text
blood_type
health_insurance_number
emergency_contact_name
emergency_contact_phone
medical_note
allergies
```

---

# 20. Những điểm cần chú ý về UX/UI

* Bảng khá nhiều cột, nên cần đảm bảo responsive.
* Ở màn hình nhỏ hơn, nên cho table scroll ngang.
* Cột “Họ và tên” và “Thao tác” có thể sticky để dễ thao tác.
* Không nên xóa bệnh nhân thật vì dữ liệu y tế cần lưu lịch sử.
* Trạng thái nên có màu rõ:

  * Hoạt động: xanh.
  * Tạm khóa: cam.
  * Ngưng hoạt động: đỏ.
* CCCD/CMND là dữ liệu nhạy cảm, nên cân nhắc che bớt nếu role không đủ quyền.
* Nút xóa nên có confirm modal.
* Nút export nên xuất đúng dữ liệu theo filter hiện tại.
* Tìm kiếm nên hỗ trợ tiếng Việt có dấu và không dấu.
* Bảng nên có sort theo:

  * Họ tên.
  * Ngày sinh.
  * Trạng thái.
  * Ngày tạo.
* Có thể thêm nút reset filter nếu filter phức tạp hơn.

---

# 21. Mô tả ngắn cho designer/dev

Giao diện là trang **Patient Management** trong admin dashboard. Sidebar trái cố định màu trắng, logo CarePlus Admin màu xanh lá, menu điều hướng có item “Quản lý bệnh nhân” đang active với nền xanh nhạt. Main content bên phải có tiêu đề “Quản lý bệnh nhân”, breadcrumb, chuông thông báo có badge đỏ số 3, avatar admin và dropdown tài khoản. Bên dưới là 4 card thống kê bệnh nhân: tổng bệnh nhân, bệnh nhân mới, bệnh nhân nam, bệnh nhân nữ. Tiếp theo là card bảng danh sách gồm thanh tìm kiếm, filter giới tính, nhóm tuổi, trạng thái, nút thêm bệnh nhân và xuất Excel. Bảng hiển thị danh sách bệnh nhân với checkbox, STT, avatar + họ tên, giới tính bằng icon, ngày sinh, số điện thoại, CCCD/CMND, email, địa chỉ, badge trạng thái và 3 nút thao tác xem/sửa/xóa. Cuối bảng có chọn số bản ghi mỗi trang và phân trang.

---

# 22. Prompt có thể đưa cho AI/dev để dựng lại UI

```text
Thiết kế giao diện admin dashboard cho hệ thống y tế CarePlus Admin, trang Quản lý bệnh nhân.

Bố cục gồm sidebar trái cố định rộng khoảng 280px, nền trắng, logo CarePlus Admin màu xanh lá ở trên cùng, menu điều hướng gồm Dashboard, Quản lý tài khoản, Quản lý bác sĩ, Quản lý bệnh nhân, Quản lý thuốc, Quản lý dịch vụ, Quản lý thanh toán, Xem báo cáo thống kê, Phân quyền hệ thống, Sao lưu dữ liệu. Mục Quản lý bệnh nhân đang active với nền xanh lá nhạt, icon và text màu xanh lá. Cuối sidebar có nút Đăng xuất nền đỏ nhạt.

Khu vực chính nền xám rất nhạt, padding 32px. Header có tiêu đề lớn “Quản lý bệnh nhân”, breadcrumb “Dashboard / Quản lý bệnh nhân”, góc phải có icon chuông thông báo với badge đỏ số 3, avatar admin, text “Admin (Quản trị viên)” và mũi tên dropdown.

Bên dưới header là 4 card thống kê nằm ngang, nền trắng, bo góc 16px, border nhẹ. Card 1: icon nhóm người nền xanh dương, tiêu đề “Tổng bệnh nhân”, số 3.256 màu xanh dương, dòng “↑ 12% so với tháng trước”. Card 2: icon trái tim y tế nền xanh lá, “Bệnh nhân mới”, số 128, “↑ 8% so với tháng trước”. Card 3: icon người nền cam, “Bệnh nhân nam”, số 1.582, “48,6% tổng số”. Card 4: icon người nền tím, “Bệnh nhân nữ”, số 1.674, “51,4% tổng số”.

Phần dưới là card danh sách bệnh nhân nền trắng bo góc 16px. Hàng filter gồm input tìm kiếm có icon kính lúp với placeholder “Tìm kiếm bệnh nhân (Tên, SDT, CCCD, Email...)”, dropdown Giới tính, dropdown Nhóm tuổi, dropdown Trạng thái, nút xanh “+ Thêm bệnh nhân”, nút viền “Xuất Excel” có icon Excel.

Bảng gồm các cột checkbox, STT, Họ và tên, Giới tính, Ngày sinh, SĐT, CCCD/CMND, Email, Địa chỉ, Trạng thái, Thao tác. Mỗi dòng có avatar nhỏ cạnh tên. Giới tính dùng icon nam xanh dương hoặc nữ hồng. Trạng thái dùng badge: Hoạt động xanh lá nhạt, Tạm khóa cam nhạt, Ngưng hoạt động đỏ nhạt. Cột thao tác có 3 icon button: xem chi tiết màu xanh, chỉnh sửa màu xanh, xóa màu đỏ.

Cuối bảng có text “Hiển thị 10 bản ghi”, dropdown số bản ghi, pagination gồm nút previous, các trang 1 2 3 4 5 ... 326, trang 1 active nền xanh lá, và nút next.

Phong cách hiện đại, sạch, nhiều khoảng trắng, font Inter hoặc Roboto, màu chủ đạo xanh lá #00A651, text xanh navy đậm, border xám nhạt, shadow rất nhẹ.
```
