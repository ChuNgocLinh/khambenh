Dưới đây là mô tả chi tiết theo kiểu **tài liệu spec UI + suy đoán chức năng** để designer/dev/BA có thể dựa vào làm lại gần như y chang.

---

# 1. Tổng quan toàn bộ hệ thống

Đây là bộ giao diện **CarePlus Admin**, một hệ thống quản trị phòng khám / cơ sở y tế. Giao diện dành cho **Admin / quản trị viên** để quản lý toàn bộ dữ liệu vận hành gồm:

* Dashboard tổng quan
* Tài khoản người dùng
* Bác sĩ
* Bệnh nhân
* Thuốc
* Dịch vụ khám/chữa bệnh
* Thanh toán
* Báo cáo thống kê
* Phân quyền hệ thống
* Sao lưu dữ liệu

Tất cả màn hình có cùng một layout:

```text
Sidebar bên trái + Header trên cùng + Nội dung chính bên phải
```

Phong cách thiết kế:

* Nền sáng, sạch, hiện đại
* Màu chủ đạo: xanh lá
* Dùng card bo góc lớn
* Bảng dữ liệu rộng, thoáng
* Icon nhiều màu để phân biệt loại dữ liệu
* Giao diện giống admin dashboard chuyên nghiệp

---

# 2. Layout chung của tất cả màn hình

## 2.1 Sidebar bên trái

Sidebar cố định bên trái, nền trắng, cao toàn màn hình.

Chiều rộng khoảng **280–300px**.

Ở trên cùng là logo:

```text
[icon dấu cộng y tế màu xanh] CarePlus Admin
```

* Icon dấu cộng nằm trong vòng tròn xanh lá
* Chữ **CarePlus Admin** màu xanh lá
* Font đậm, kích thước lớn
* Padding trên khoảng 24–32px
* Padding trái khoảng 28–32px

## 2.2 Menu sidebar

Danh sách menu gồm:

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

* Icon bên trái
* Text bên phải
* Chiều cao khoảng 48–56px
* Bo góc khoảng 10–12px
* Khi không active: icon và chữ màu xanh đen/xám đậm
* Khi active: nền xanh lá nhạt, icon và chữ màu xanh lá

Ví dụ ở màn **Quản lý tài khoản**, item “Quản lý tài khoản” có nền xanh nhạt và icon màu xanh. Các item còn lại màu tối.

## 2.3 Nút đăng xuất

Ở cuối sidebar có nút **Đăng xuất**:

* Nền đỏ nhạt
* Text đỏ
* Icon logout đỏ
* Bo góc 10–12px
* Chiều rộng gần full sidebar
* Nằm sát đáy màn hình

Chức năng nên có:

* Click mở modal xác nhận:

  * “Bạn có chắc chắn muốn đăng xuất?”
  * Nút “Huỷ”
  * Nút “Đăng xuất”
* Sau khi đăng xuất:

  * Xoá token
  * Xoá session
  * Chuyển về màn login

---

# 3. Header chung

Mỗi màn có header nằm phía trên khu vực nội dung chính.

## 3.1 Bên trái header

Gồm tiêu đề màn hình lớn và breadcrumb bên dưới.

Ví dụ:

```text
Quản lý tài khoản
Dashboard / Quản lý tài khoản
```

Hoặc:

```text
Quản lý bác sĩ
Dashboard / Quản lý bác sĩ
```

Hoặc ở dashboard:

```text
Dashboard Admin
Tổng quan hệ thống quản trị
```

Đặc điểm:

* Tiêu đề font lớn, đậm, màu xanh đen
* Breadcrumb nhỏ hơn, màu xám xanh
* Chữ “Dashboard” trong breadcrumb có thể click để quay về dashboard

## 3.2 Bên phải header

Gồm:

1. Icon chuông thông báo

   * Có badge đỏ số **3**
   * Click để mở dropdown thông báo

2. Avatar admin

   * Hình tròn
   * Kích thước khoảng 44–50px

3. Tên người dùng:

   * **Admin (Quản trị viên)**

4. Icon mũi tên xuống

   * Mở menu tài khoản

Dropdown tài khoản nên có:

* Hồ sơ cá nhân
* Đổi mật khẩu
* Cài đặt
* Đăng xuất

---

# 4. Cấu trúc chung các màn quản lý danh sách

Các màn **Quản lý tài khoản, Quản lý bác sĩ, Quản lý bệnh nhân, Quản lý thuốc, Quản lý dịch vụ** có cùng cấu trúc:

```text
Header
↓
4 card thống kê nhanh
↓
Khu vực tìm kiếm + bộ lọc + nút thêm + xuất Excel
↓
Bảng dữ liệu
↓
Phân trang
```

## 4.1 Card thống kê

Mỗi màn có 4 card KPI nằm ngang.

Mỗi card gồm:

* Icon màu nằm bên trái
* Tiêu đề
* Số lớn
* Dòng mô tả tăng/giảm hoặc tỷ lệ
* Viền xám nhạt
* Nền trắng
* Bo góc lớn
* Shadow rất nhẹ

Màu icon/card:

* Xanh dương: tổng số
* Xanh lá: đang hoạt động / còn hàng / mới
* Cam: tạm nghỉ / sắp hết / nam / tạm ngưng
* Tím: vai trò / nữ / hết hàng / ngừng cung cấp
* Đỏ dùng cho chỉ số giảm hoặc trạng thái xấu

## 4.2 Thanh tìm kiếm và bộ lọc

Có một khối filter nằm dưới card KPI.

Gồm:

* Ô search lớn bên trái
* Các dropdown filter ở giữa
* Cụm nút bên phải:

  * Nút xanh **+ Thêm ...**
  * Nút trắng viền xám **Xuất Excel**

Search input có icon kính lúp.

Dropdown có label phía trên, ví dụ:

```text
Vai trò
[Tất cả ▼]
```

hoặc:

```text
Trạng thái
[Tất cả ▼]
```

## 4.3 Bảng dữ liệu

Bảng có:

* Checkbox chọn từng dòng
* Checkbox chọn tất cả ở header
* Cột STT
* Các cột dữ liệu chính
* Cột trạng thái dạng badge
* Cột thao tác gồm icon:

  * Mắt: xem chi tiết
  * Bút: chỉnh sửa
  * Thùng rác: xoá

Đặc điểm:

* Header bảng nền xám rất nhạt
* Text header đậm
* Dòng dữ liệu cao khoảng 56–64px
* Có border-bottom mảnh
* Avatar người dùng/bác sĩ/bệnh nhân hiển thị cạnh tên
* Badge có nền nhạt, chữ màu tương ứng

## 4.4 Phân trang

Ở cuối bảng:

Bên trái:

```text
Hiển thị [10 ▼] bản ghi
```

Bên phải:

```text
< 1 2 3 4 5 ... 26 >
```

Trang hiện tại có nền xanh lá, chữ trắng.

Chức năng nên có:

* Chọn số bản ghi mỗi trang: 10, 20, 50, 100
* Chuyển trang
* Search/filter vẫn giữ khi đổi trang
* Query URL có thể lưu page, limit, search, filter

---

# 5. Màn Dashboard Admin

Màn dashboard là trang tổng quan hệ thống.

## 5.1 Header dashboard

Tiêu đề:

```text
Dashboard Admin
Tổng quan hệ thống quản trị
```

Bên phải vẫn là chuông thông báo, avatar admin, tên admin.

## 5.2 Card thống kê trên dashboard

Có 4 card KPI:

### Card 1: Tổng bệnh nhân

```text
Tổng bệnh nhân
3.256
↑ 12% so với tháng trước
```

* Icon nhóm người
* Màu xanh dương
* Click nên dẫn tới trang Quản lý bệnh nhân

### Card 2: Tổng bác sĩ

```text
Tổng bác sĩ
42
↑ 8% so với tháng trước
```

* Icon bác sĩ
* Màu xanh lá
* Click dẫn tới Quản lý bác sĩ

### Card 3: Tổng lịch hẹn

```text
Tổng lịch hẹn
58
↑ 15% so với hôm qua
```

* Icon lịch
* Màu cam
* Click dẫn tới danh sách lịch hẹn

### Card 4: Đơn thuốc hôm nay

```text
Đơn thuốc hôm nay
136
↓ 5% so với hôm qua
```

* Icon đơn thuốc
* Màu tím
* Chỉ số giảm màu đỏ

## 5.3 Biểu đồ lượt khám bệnh hằng tuần

Card lớn bên trái.

Tiêu đề:

```text
Biểu đồ lượt khám bệnh hằng tuần
```

Có dropdown:

```text
7 ngày qua
```

Biểu đồ dạng line chart + area chart.

Dữ liệu:

| Ngày  | Lượt khám |
| ----- | --------: |
| Thứ 2 |        12 |
| Thứ 3 |        25 |
| Thứ 4 |        20 |
| Thứ 5 |        32 |
| Thứ 6 |        45 |
| Thứ 7 |        30 |
| CN    |        42 |

Đặc điểm:

* Đường màu xanh lá
* Điểm tròn trắng viền xanh
* Vùng dưới đường tô xanh rất nhạt
* Trục Y từ 0 đến 100
* Có số trên từng điểm

Chức năng nên có:

* Hover hiện tooltip
* Dropdown chọn:

  * 7 ngày qua
  * 30 ngày qua
  * Tháng này
  * Quý này
  * Năm nay
* Có thể lọc theo chuyên khoa, bác sĩ, cơ sở
* Dữ liệu lấy từ lịch hẹn đã hoàn thành hoặc phiếu khám đã hoàn tất

## 5.4 Card Tổng quan doanh thu

Card bên phải biểu đồ.

Tiêu đề:

```text
Tổng quan doanh thu
```

Dropdown:

```text
Tháng này
```

Tổng doanh thu:

```text
152.450.000 đ
↑ 18% so với tháng trước
```

Danh mục doanh thu:

| Danh mục     |    Doanh thu | Tỷ lệ |
| ------------ | -----------: | ----: |
| Khám bệnh    | 62.450.000 đ |   41% |
| Xét nghiệm   | 38.200.000 đ |   25% |
| Thuốc        | 31.800.000 đ |   21% |
| Dịch vụ khác | 20.000.000 đ |   13% |

Chức năng nên có:

* Click từng dòng để xem chi tiết doanh thu
* Dropdown đổi khoảng thời gian
* Chỉ tính hoá đơn đã thanh toán
* Không tính hoá đơn huỷ
* Có thể xuất báo cáo doanh thu

## 5.5 Card Lịch hẹn sắp tới

Danh sách lịch hẹn gần nhất:

1. Nguyễn Văn Nam

   * Khám tổng quát
   * 09:00
   * 24/05/2026

2. Trần Thị Mai

   * Khám da liễu
   * 09:30
   * 24/05/2026

3. Lê Văn Cường

   * Khám tim mạch
   * 10:00
   * 24/05/2026

4. Phạm Thị Lan

   * Khám sản phụ khoa
   * 10:30
   * 24/05/2026

Có link:

```text
Xem tất cả
```

Và nút:

```text
Xem tất cả lịch hẹn
```

Chức năng nên có:

* Click từng lịch để xem chi tiết
* Xem bệnh nhân, bác sĩ phụ trách, phòng khám, trạng thái
* Có thể xác nhận, đổi lịch, huỷ lịch
* Danh sách ưu tiên lịch gần hiện tại nhất

## 5.6 Card Thông báo hệ thống

Có 4 thông báo:

### Sao lưu dữ liệu thành công

```text
Dữ liệu hệ thống đã được sao lưu lúc 02:00 AM
2h trước
```

### Hết hạn một số thuốc

```text
Kiểm tra danh sách thuốc sắp hết hạn
5h trước
```

### Cập nhật phiên bản mới

```text
Hệ thống đã cập nhật phiên bản 1.2.1
1 ngày trước
```

### Bác sĩ mới đăng ký

```text
Bác sĩ Hoàng Văn Anh đã tham gia hệ thống
1 ngày trước
```

Chức năng nên có:

* Click thông báo để xem chi tiết
* Đánh dấu đã đọc
* Badge chuông trên header đếm thông báo chưa đọc
* Cảnh báo thuốc sắp hết hạn dẫn sang Quản lý thuốc
* Backup dẫn sang Sao lưu dữ liệu
* Bác sĩ mới đăng ký dẫn sang Quản lý bác sĩ

## 5.7 Card Thống kê nhanh

Gồm 4 ô nhỏ:

### Bệnh nhân mới

```text
128
Tháng này
```

### Bác sĩ hoạt động

```text
38
Hiện tại
```

### Lịch hẹn hoàn thành

```text
342
Tháng này
```

### Đơn thuốc đã phát

```text
1.245
Tháng này
```

Chức năng nên có:

* Click từng ô để mở danh sách tương ứng
* Có thể cập nhật realtime hoặc theo ngày
* Số liệu nên lấy từ API tổng hợp dashboard

---

# 6. Màn Quản lý tài khoản

## 6.1 Mục đích màn hình

Màn này dùng để quản lý toàn bộ tài khoản trong hệ thống, gồm admin, bác sĩ, lễ tân, kế toán, điều dưỡng, nhân viên, khách hàng/bệnh nhân.

Các chức năng chính:

* Xem danh sách tài khoản
* Tìm kiếm tài khoản
* Lọc theo vai trò
* Lọc theo trạng thái
* Thêm tài khoản
* Xem chi tiết
* Sửa tài khoản
* Xoá hoặc khoá tài khoản
* Xuất Excel
* Phân quyền theo vai trò

## 6.2 Header

Tiêu đề:

```text
Quản lý tài khoản
```

Breadcrumb:

```text
Dashboard / Quản lý tài khoản
```

Sidebar active ở mục **Quản lý tài khoản**.

## 6.3 Card thống kê

Có 4 card:

### Tổng tài khoản

```text
Tổng tài khoản
56
↑ 12% so với tháng trước
```

* Icon nhóm người
* Màu xanh dương

### Tài khoản hoạt động

```text
Tài khoản hoạt động
48
↑ 9% so với tháng trước
```

* Icon người
* Màu xanh lá

### Tài khoản bị khóa

```text
Tài khoản bị khóa
5
↓ 3% so với tháng trước
```

* Icon khoá
* Màu cam
* Chỉ số giảm màu đỏ

### Vai trò hệ thống

```text
Vai trò hệ thống
6
Quản lý vai trò
```

* Icon khiên
* Màu tím
* Có thể click sang trang phân quyền/vai trò

## 6.4 Bộ lọc

Có các thành phần:

### Search input

Placeholder:

```text
Tìm kiếm tài khoản (Tên, email, SĐT...)
```

Có thể tìm theo:

* Họ tên
* Email
* Số điện thoại
* Mã tài khoản nếu có

### Dropdown Vai trò

Label:

```text
Vai trò
```

Giá trị mặc định:

```text
Tất cả
```

Các option nên có:

* Tất cả
* Quản trị viên
* Bác sĩ
* Lễ tân
* Kế toán
* Điều dưỡng
* Nhân viên
* Khách hàng

### Dropdown Trạng thái

Label:

```text
Trạng thái
```

Giá trị mặc định:

```text
Tất cả
```

Các option:

* Tất cả
* Hoạt động
* Bị khóa
* Chờ kích hoạt
* Tạm ngưng

### Nút Thêm tài khoản

```text
+ Thêm tài khoản
```

* Nền xanh lá
* Chữ trắng
* Icon dấu cộng

Click mở form thêm tài khoản.

### Nút Xuất Excel

```text
Xuất Excel
```

* Nền trắng
* Viền xám
* Icon Excel xanh

Chức năng:

* Xuất danh sách theo bộ lọc hiện tại
* Hoặc xuất toàn bộ nếu không có filter
* File nên có tên dạng `danh_sach_tai_khoan_2026_05_24.xlsx`

## 6.5 Bảng tài khoản

Các cột:

| Cột           | Ý nghĩa                 |
| ------------- | ----------------------- |
| Checkbox      | Chọn nhiều tài khoản    |
| STT           | Số thứ tự               |
| Họ và tên     | Avatar + tên người dùng |
| Email         | Email đăng nhập         |
| Số điện thoại | SĐT                     |
| Vai trò       | Badge vai trò           |
| Trạng thái    | Badge hoạt động/bị khóa |
| Ngày tạo      | Ngày giờ tạo tài khoản  |
| Thao tác      | Xem, sửa, xoá           |

Dữ liệu mẫu:

| STT | Họ tên          | Email                                                 | SĐT          | Vai trò       | Trạng thái | Ngày tạo         |
| --: | --------------- | ----------------------------------------------------- | ------------ | ------------- | ---------- | ---------------- |
|   1 | Nguyễn Văn Nam  | [nam.nguyen@gmail.com](mailto:nam.nguyen@gmail.com)   | 0987 654 321 | Quản trị viên | Hoạt động  | 24/05/2026 09:15 |
|   2 | Trần Thị Mai    | [mai.tran@gmail.com](mailto:mai.tran@gmail.com)       | 0912 345 678 | Bác sĩ        | Hoạt động  | 24/05/2026 09:30 |
|   3 | Lê Văn Cường    | [cuong.le@gmail.com](mailto:cuong.le@gmail.com)       | 0933 456 789 | Bác sĩ        | Hoạt động  | 24/05/2026 10:00 |
|   4 | Phạm Thị Lan    | [lan.pham@gmail.com](mailto:lan.pham@gmail.com)       | 0909 876 543 | Lễ tân        | Hoạt động  | 24/05/2026 10:30 |
|   5 | Hoàng Anh Tuấn  | [tuan.hoang@gmail.com](mailto:tuan.hoang@gmail.com)   | 0988 765 432 | Kế toán       | Hoạt động  | 24/05/2026 11:00 |
|   6 | Vũ Thị Hương    | [huong.vu@gmail.com](mailto:huong.vu@gmail.com)       | 0977 654 321 | Điều dưỡng    | Bị khóa    | 24/05/2026 11:30 |
|   7 | Đỗ Minh Quân    | [quan.do@gmail.com](mailto:quan.do@gmail.com)         | 0966 543 210 | Nhân viên     | Hoạt động  | 24/05/2026 12:00 |
|   8 | Nguyễn Thị Hoa  | [hoa.nguyen@gmail.com](mailto:hoa.nguyen@gmail.com)   | 0908 111 222 | Nhân viên     | Bị khóa    | 24/05/2026 12:30 |
|   9 | Bùi Văn Dũng    | [dung.bui@gmail.com](mailto:dung.bui@gmail.com)       | 0982 333 444 | Nhân viên     | Hoạt động  | 24/05/2026 13:00 |
|  10 | Trương Văn Kiên | [kien.truong@gmail.com](mailto:kien.truong@gmail.com) | 0933 999 000 | Khách hàng    | Hoạt động  | 24/05/2026 13:30 |

## 6.6 Badge vai trò

Mỗi vai trò có màu riêng:

* Quản trị viên: xanh lá
* Bác sĩ: xanh dương
* Lễ tân: cam
* Kế toán: tím
* Điều dưỡng: xanh cyan
* Nhân viên: xám
* Khách hàng: vàng/cam nhạt

## 6.7 Thao tác từng dòng

Có 3 icon:

### Xem chi tiết

Icon mắt màu xanh.

Click mở modal/trang chi tiết tài khoản:

* Họ tên
* Email
* SĐT
* Vai trò
* Trạng thái
* Ngày tạo
* Lần đăng nhập cuối
* Lịch sử hoạt động
* Quyền được cấp

### Sửa

Icon bút màu xanh.

Cho sửa:

* Họ tên
* Email
* SĐT
* Vai trò
* Trạng thái
* Avatar
* Mật khẩu nếu admin reset

### Xoá

Icon thùng rác màu đỏ.

Nên là xoá mềm hoặc khoá tài khoản, không xoá vật lý ngay.

Click cần confirm:

```text
Bạn có chắc muốn xoá tài khoản này không?
```

Nếu tài khoản có dữ liệu liên quan như lịch sử khám, thanh toán, đơn thuốc thì nên không xoá cứng.

## 6.8 Form thêm tài khoản nên có

Các field:

* Họ và tên
* Email
* Số điện thoại
* Mật khẩu
* Nhập lại mật khẩu
* Vai trò
* Trạng thái
* Avatar
* Ghi chú

Validation:

* Email đúng định dạng
* Email không trùng
* SĐT không trùng
* Mật khẩu tối thiểu 8 ký tự
* Vai trò bắt buộc
* Họ tên bắt buộc

---

# 7. Màn Quản lý bác sĩ

## 7.1 Mục đích

Màn này dùng để quản lý danh sách bác sĩ trong hệ thống.

Chức năng chính:

* Xem danh sách bác sĩ
* Tìm kiếm bác sĩ
* Lọc theo chuyên khoa
* Lọc theo trạng thái tài khoản
* Lọc theo tình trạng làm việc
* Thêm bác sĩ
* Sửa thông tin bác sĩ
* Xoá/ngưng hoạt động bác sĩ
* Xuất Excel
* Quản lý hồ sơ chuyên môn

## 7.2 Header

```text
Quản lý bác sĩ
Dashboard / Quản lý bác sĩ
```

Sidebar active mục **Quản lý bác sĩ**.

## 7.3 Card thống kê

### Tổng bác sĩ

```text
Tổng bác sĩ
42
↑ 8% so với tháng trước
```

### Đang hoạt động

```text
Đang hoạt động
38
↑ 7% so với tháng trước
```

### Tạm nghỉ

```text
Tạm nghỉ
3
↓ 2% so với tháng trước
```

### Nghỉ việc

```text
Nghỉ việc
1
↓ 1% so với tháng trước
```

## 7.4 Bộ lọc

### Search

Placeholder:

```text
Tìm kiếm bác sĩ (Tên, chuyên khoa, SĐT...)
```

Tìm theo:

* Tên bác sĩ
* Chuyên khoa
* Số điện thoại
* Email
* Mã bác sĩ nếu có

### Dropdown Chuyên khoa

Option nên có:

* Tất cả
* Nội tổng quát
* Nhi khoa
* Tim mạch
* Sản phụ khoa
* Ngoại khoa
* Da liễu
* Răng hàm mặt
* Thần kinh
* Mắt
* Tai mũi họng

### Dropdown Trạng thái

Option:

* Tất cả
* Hoạt động
* Bị khóa
* Chờ duyệt

### Dropdown Tình trạng

Option:

* Tất cả
* Đang làm việc
* Nghỉ phép
* Tạm nghỉ
* Đã nghỉ việc

### Nút Thêm bác sĩ

```text
+ Thêm bác sĩ
```

### Nút Xuất Excel

```text
Xuất Excel
```

## 7.5 Bảng bác sĩ

Các cột:

| Cột         | Ý nghĩa                 |
| ----------- | ----------------------- |
| Checkbox    | Chọn nhiều              |
| STT         | Số thứ tự               |
| Họ và tên   | Avatar + tên bác sĩ     |
| Chuyên khoa | Chuyên ngành            |
| SĐT         | Số điện thoại           |
| Email       | Email                   |
| Trạng thái  | Hoạt động/Nghỉ việc     |
| Tình trạng  | Đang làm việc/Nghỉ phép |
| Ngày tạo    | Ngày tạo hồ sơ          |
| Thao tác    | Xem/Sửa/Xoá             |

Dữ liệu mẫu:

| STT | Họ tên          | Chuyên khoa   | SĐT          | Email                                                 | Trạng thái | Tình trạng    |
| --: | --------------- | ------------- | ------------ | ----------------------------------------------------- | ---------- | ------------- |
|   1 | Nguyễn Văn Nam  | Nội tổng quát | 0987 654 321 | [nam.nguyen@gmail.com](mailto:nam.nguyen@gmail.com)   | Hoạt động  | Đang làm việc |
|   2 | Trần Thị Mai    | Nhi khoa      | 0912 345 678 | [mai.tran@gmail.com](mailto:mai.tran@gmail.com)       | Hoạt động  | Đang làm việc |
|   3 | Lê Văn Cường    | Tim mạch      | 0933 456 789 | [cuong.le@gmail.com](mailto:cuong.le@gmail.com)       | Hoạt động  | Đang làm việc |
|   4 | Phạm Thị Lan    | Sản phụ khoa  | 0909 876 543 | [lan.pham@gmail.com](mailto:lan.pham@gmail.com)       | Tạm nghỉ   | Nghỉ phép     |
|   5 | Hoàng Anh Tuấn  | Ngoại khoa    | 0988 765 432 | [tuan.hoang@gmail.com](mailto:tuan.hoang@gmail.com)   | Hoạt động  | Đang làm việc |
|   6 | Vũ Thị Hương    | Da liễu       | 0977 654 321 | [huong.vu@gmail.com](mailto:huong.vu@gmail.com)       | Hoạt động  | Đang làm việc |
|   7 | Đỗ Minh Quân    | Răng hàm mặt  | 0966 543 210 | [quan.do@gmail.com](mailto:quan.do@gmail.com)         | Hoạt động  | Đang làm việc |
|   8 | Bùi Văn Dũng    | Thần kinh     | 0982 333 444 | [dung.bui@gmail.com](mailto:dung.bui@gmail.com)       | Nghỉ việc  | Đã nghỉ việc  |
|   9 | Nguyễn Thị Hoa  | Mắt           | 0908 111 222 | [hoa.nguyen@gmail.com](mailto:hoa.nguyen@gmail.com)   | Hoạt động  | Đang làm việc |
|  10 | Trương Văn Kiên | Tai mũi họng  | 0933 999 000 | [kien.truong@gmail.com](mailto:kien.truong@gmail.com) | Hoạt động  | Đang làm việc |

## 7.6 Badge trạng thái

* Hoạt động: xanh lá
* Tạm nghỉ: cam
* Nghỉ việc: đỏ

## 7.7 Badge tình trạng

* Đang làm việc: xanh lá
* Nghỉ phép: cam
* Đã nghỉ việc: đỏ

## 7.8 Form thêm/sửa bác sĩ nên có

Thông tin cá nhân:

* Họ tên
* Ngày sinh
* Giới tính
* Số điện thoại
* Email
* Địa chỉ
* Avatar

Thông tin chuyên môn:

* Mã bác sĩ
* Chuyên khoa
* Học vị
* Chức danh
* Số năm kinh nghiệm
* Số chứng chỉ hành nghề
* Ngày cấp chứng chỉ
* Nơi cấp
* Mô tả chuyên môn
* Dịch vụ phụ trách

Thông tin làm việc:

* Trạng thái tài khoản
* Tình trạng làm việc
* Lịch làm việc
* Phòng khám/phòng ban
* Ca làm việc
* Ghi chú

Chức năng nâng cao:

* Quản lý lịch trực
* Gán bác sĩ vào dịch vụ
* Xem lịch hẹn của bác sĩ
* Xem doanh thu/lượt khám theo bác sĩ
* Tạm ngưng nhận lịch
* Duyệt bác sĩ mới đăng ký

---

# 8. Màn Quản lý bệnh nhân

## 8.1 Mục đích

Màn này dùng để quản lý hồ sơ bệnh nhân.

Chức năng chính:

* Xem danh sách bệnh nhân
* Tìm kiếm theo tên/SĐT/CCCD/email
* Lọc giới tính
* Lọc nhóm tuổi
* Lọc trạng thái
* Thêm bệnh nhân
* Xem hồ sơ bệnh án
* Chỉnh sửa thông tin cá nhân
* Tạm khoá/ngưng hoạt động hồ sơ
* Xuất Excel

## 8.2 Header

```text
Quản lý bệnh nhân
Dashboard / Quản lý bệnh nhân
```

Sidebar active mục **Quản lý bệnh nhân**.

## 8.3 Card thống kê

### Tổng bệnh nhân

```text
Tổng bệnh nhân
3.256
↑ 12% so với tháng trước
```

### Bệnh nhân mới

```text
Bệnh nhân mới
128
↑ 8% so với tháng trước
```

### Bệnh nhân nam

```text
Bệnh nhân nam
1.582
48,6% tổng số
```

### Bệnh nhân nữ

```text
Bệnh nhân nữ
1.674
51,4% tổng số
```

## 8.4 Bộ lọc

### Search

Placeholder:

```text
Tìm kiếm bệnh nhân (Tên, SĐT, CCCD, Email...)
```

Tìm theo:

* Họ tên
* Số điện thoại
* CCCD/CMND
* Email
* Mã bệnh nhân nếu có

### Dropdown Giới tính

Option:

* Tất cả
* Nam
* Nữ
* Khác

### Dropdown Nhóm tuổi

Option nên có:

* Tất cả
* Dưới 18
* 18–30
* 31–45
* 46–60
* Trên 60

### Dropdown Trạng thái

Option:

* Tất cả
* Hoạt động
* Tạm khóa
* Ngưng hoạt động

### Nút Thêm bệnh nhân

```text
+ Thêm bệnh nhân
```

### Nút Xuất Excel

```text
Xuất Excel
```

## 8.5 Bảng bệnh nhân

Các cột:

| Cột        | Ý nghĩa                  |
| ---------- | ------------------------ |
| Checkbox   | Chọn bệnh nhân           |
| STT        | Số thứ tự                |
| Họ và tên  | Avatar + họ tên          |
| Giới tính  | Icon nam/nữ              |
| Ngày sinh  | DOB                      |
| SĐT        | Số điện thoại            |
| CCCD/CMND  | Mã định danh             |
| Email      | Email                    |
| Địa chỉ    | Tỉnh/thành               |
| Trạng thái | Hoạt động/Tạm khoá/Ngưng |
| Thao tác   | Xem/Sửa/Xoá              |

Dữ liệu mẫu:

| STT | Họ tên          | Giới tính | Ngày sinh  | SĐT          | CCCD/CMND    | Email                                                 | Địa chỉ         | Trạng thái      |
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

## 8.6 Icon giới tính

* Nam: icon nam màu xanh dương
* Nữ: icon nữ màu hồng

## 8.7 Trạng thái bệnh nhân

* Hoạt động: xanh lá
* Tạm khóa: cam
* Ngưng hoạt động: đỏ

## 8.8 Xem chi tiết bệnh nhân nên có

Khi click icon mắt, nên mở hồ sơ bệnh nhân gồm:

Thông tin cá nhân:

* Mã bệnh nhân
* Họ tên
* Ngày sinh
* Giới tính
* SĐT
* Email
* CCCD/CMND
* Địa chỉ
* Người liên hệ khẩn cấp
* Bảo hiểm y tế nếu có

Thông tin y tế:

* Nhóm máu
* Dị ứng thuốc
* Bệnh nền
* Tiền sử bệnh
* Ghi chú y tế

Lịch sử:

* Lịch sử khám
* Lịch hẹn sắp tới
* Đơn thuốc đã kê
* Kết quả xét nghiệm
* Hoá đơn thanh toán

## 8.9 Form thêm bệnh nhân nên có

Field bắt buộc:

* Họ tên
* Ngày sinh
* Giới tính
* SĐT
* CCCD/CMND

Field không bắt buộc:

* Email
* Địa chỉ
* Avatar
* Nghề nghiệp
* Người liên hệ khẩn cấp
* SĐT người liên hệ
* Tiền sử bệnh
* Dị ứng
* Ghi chú

Validation:

* SĐT đúng định dạng
* CCCD không trùng
* Email đúng định dạng nếu nhập
* Ngày sinh không được lớn hơn ngày hiện tại

---

# 9. Màn Quản lý thuốc

## 9.1 Mục đích

Màn này dùng để quản lý danh mục thuốc và tồn kho thuốc.

Chức năng chính:

* Xem danh sách thuốc
* Tìm kiếm thuốc
* Lọc theo danh mục
* Lọc theo nhà cung cấp
* Lọc theo trạng thái tồn kho
* Thêm thuốc
* Sửa thông tin thuốc
* Xem chi tiết thuốc
* Xoá thuốc
* Xuất Excel
* Cảnh báo thuốc sắp hết/hết hàng/sắp hết hạn

## 9.2 Header

```text
Quản lý thuốc
Dashboard / Quản lý thuốc
```

Sidebar active mục **Quản lý thuốc**.

## 9.3 Card thống kê

### Tổng số thuốc

```text
Tổng số thuốc
256
↑ 12% so với tháng trước
```

### Thuốc còn hàng

```text
Thuốc còn hàng
186
↑ 8% so với tháng trước
```

### Thuốc sắp hết

```text
Thuốc sắp hết
28
↓ 5% so với tháng trước
```

### Thuốc hết hàng

```text
Thuốc hết hàng
12
↓ 3% so với tháng trước
```

## 9.4 Bộ lọc

### Search

Placeholder:

```text
Tìm kiếm thuốc (Tên thuốc, hoạt chất, mã thuốc...)
```

Tìm theo:

* Tên thuốc
* Hoạt chất
* Mã thuốc
* Nhà cung cấp
* Danh mục

### Dropdown Danh mục

Option:

* Tất cả
* Giảm đau - Hạ sốt
* Kháng sinh
* Vitamin - Khoáng chất
* Dạ dày - Tiêu hóa
* Kháng dị ứng
* Giảm đau - Viêm
* Tim mạch
* Hô hấp

### Dropdown Nhà cung cấp

Option mẫu:

* Tất cả
* Dược Hậu Giang
* Traphaco
* Imexpharm
* Stella

### Dropdown Trạng thái

Option:

* Tất cả
* Còn hàng
* Sắp hết
* Hết hàng
* Sắp hết hạn
* Đã ngừng bán

### Nút Thêm thuốc

```text
+ Thêm thuốc
```

### Nút Xuất Excel

```text
Xuất Excel
```

## 9.5 Bảng thuốc

Các cột:

| Cột          | Ý nghĩa                    |
| ------------ | -------------------------- |
| Checkbox     | Chọn thuốc                 |
| STT          | Số thứ tự                  |
| Tên thuốc    | Tên thương mại + hàm lượng |
| Hoạt chất    | Hoạt chất chính            |
| Danh mục     | Nhóm thuốc                 |
| Đơn vị tính  | Viên/hộp/chai/vỉ           |
| Nhà cung cấp | Supplier                   |
| Số lượng     | Tồn kho                    |
| Giá nhập     | Giá nhập                   |
| Giá bán      | Giá bán                    |
| Trạng thái   | Còn hàng/Sắp hết/Hết hàng  |
| Thao tác     | Xem/Sửa/Xoá                |

Dữ liệu mẫu:

| STT | Tên thuốc         | Hoạt chất        | Danh mục              | ĐVT  | Nhà cung cấp   |    SL | Giá nhập | Giá bán | Trạng thái |
| --: | ----------------- | ---------------- | --------------------- | ---- | -------------- | ----: | -------: | ------: | ---------- |
|   1 | Paracetamol 500mg | Paracetamol      | Giảm đau - Hạ sốt     | Viên | Dược Hậu Giang | 1.250 |    850 đ | 1.200 đ | Còn hàng   |
|   2 | Amoxicillin 500mg | Amoxicillin      | Kháng sinh            | Viên | Traphaco       |   950 |  1.200 đ | 1.800 đ | Còn hàng   |
|   3 | Vitamin C 500mg   | Vitamin C        | Vitamin - Khoáng chất | Viên | Imexpharm      | 2.300 |    650 đ | 1.000 đ | Còn hàng   |
|   4 | Omeprazole 20mg   | Omeprazole       | Dạ dày - Tiêu hóa     | Viên | Dược Hậu Giang |   320 |  1.100 đ | 1.600 đ | Sắp hết    |
|   5 | Loratadin 10mg    | Loratadin        | Kháng dị ứng          | Viên | Traphaco       |   180 |    900 đ | 1.400 đ | Sắp hết    |
|   6 | Cetirizin 10mg    | Cetirizin        | Kháng dị ứng          | Viên | Imexpharm      |     0 |    850 đ | 1.300 đ | Hết hàng   |
|   7 | Ibuprofen 400mg   | Ibuprofen        | Giảm đau - Viêm       | Viên | Stella         |   760 |    950 đ | 1.500 đ | Còn hàng   |
|   8 | Aspirin 81mg      | Aspirin          | Tim mạch              | Viên | Dược Hậu Giang | 1.100 |    700 đ | 1.100 đ | Còn hàng   |
|   9 | Multivitamin      | Vitamin tổng hợp | Vitamin - Khoáng chất | Viên | Traphaco       |   540 |  1.500 đ | 2.200 đ | Còn hàng   |
|  10 | Salbutamol 2mg    | Salbutamol       | Hô hấp                | Viên | Imexpharm      |   150 |  1.000 đ | 1.600 đ | Sắp hết    |

## 9.6 Trạng thái thuốc

* Còn hàng: badge xanh
* Sắp hết: badge cam
* Hết hàng: badge đỏ

Ngưỡng suy đoán:

* Còn hàng: số lượng > mức cảnh báo
* Sắp hết: số lượng > 0 và <= ngưỡng cảnh báo
* Hết hàng: số lượng = 0

Ví dụ:

```text
if quantity == 0 => Hết hàng
if quantity <= min_stock => Sắp hết
else => Còn hàng
```

## 9.7 Form thêm thuốc nên có

Thông tin cơ bản:

* Mã thuốc
* Tên thuốc
* Hoạt chất
* Hàm lượng
* Danh mục
* Đơn vị tính
* Nhà cung cấp
* Mô tả
* Hướng dẫn sử dụng
* Chống chỉ định
* Ghi chú

Thông tin kho:

* Số lượng tồn
* Tồn tối thiểu
* Giá nhập
* Giá bán
* Số lô
* Ngày sản xuất
* Ngày hết hạn
* Vị trí lưu kho

Thông tin trạng thái:

* Còn bán
* Tạm ngừng
* Hết hàng
* Thuốc kê đơn / không kê đơn

## 9.8 Chức năng nâng cao nên có

* Nhập kho
* Xuất kho
* Lịch sử tồn kho
* Cảnh báo sắp hết hạn
* Cảnh báo tồn kho thấp
* Quản lý theo lô thuốc
* Không cho xoá thuốc nếu đã từng xuất hiện trong đơn thuốc
* Chỉ cho ngừng kinh doanh hoặc ẩn khỏi danh sách kê đơn
* Xuất danh sách thuốc sắp hết
* Xuất danh sách thuốc hết hạn

---

# 10. Màn Quản lý dịch vụ

## 10.1 Mục đích

Màn này dùng để quản lý các dịch vụ y tế/phòng khám cung cấp.

Ví dụ:

* Khám tổng quát
* Khám chuyên khoa
* Xét nghiệm
* Chẩn đoán hình ảnh
* Thăm dò chức năng
* Điều trị
* Vật lý trị liệu

Chức năng chính:

* Xem danh sách dịch vụ
* Tìm kiếm dịch vụ
* Lọc danh mục dịch vụ
* Lọc trạng thái
* Lọc hiển thị
* Thêm dịch vụ
* Sửa dịch vụ
* Xoá/ngừng cung cấp
* Xuất Excel

## 10.2 Header

```text
Quản lý dịch vụ
Dashboard / Quản lý dịch vụ
```

Sidebar active mục **Quản lý dịch vụ**.

## 10.3 Card thống kê

### Tổng dịch vụ

```text
Tổng dịch vụ
132
↑ 12% so với tháng trước
```

### Dịch vụ đang hoạt động

```text
Dịch vụ đang hoạt động
118
↑ 8% so với tháng trước
```

### Dịch vụ tạm ngừng

```text
Dịch vụ tạm ngừng
8
↓ 3% so với tháng trước
```

### Dịch vụ ngừng cung cấp

```text
Dịch vụ ngừng cung cấp
6
↓ 1% so với tháng trước
```

## 10.4 Bộ lọc

### Search

Placeholder:

```text
Tìm kiếm dịch vụ (Tên dịch vụ, mã dịch vụ, mô tả...)
```

Tìm theo:

* Mã dịch vụ
* Tên dịch vụ
* Mô tả
* Danh mục

### Dropdown Danh mục dịch vụ

Option:

* Tất cả
* Khám bệnh
* Xét nghiệm
* Chẩn đoán hình ảnh
* Thăm dò chức năng
* Điều trị

### Dropdown Trạng thái

Option:

* Tất cả
* Đang hoạt động
* Tạm ngừng
* Ngừng cung cấp

### Dropdown Hiển thị

Option:

* Tất cả
* Hiển thị
* Ẩn

### Nút Thêm dịch vụ

```text
+ Thêm dịch vụ
```

### Nút Xuất Excel

```text
Xuất Excel
```

## 10.5 Bảng dịch vụ

Các cột:

| Cột              | Ý nghĩa                  |
| ---------------- | ------------------------ |
| Checkbox         | Chọn dịch vụ             |
| STT              | Số thứ tự                |
| Mã dịch vụ       | Code                     |
| Tên dịch vụ      | Tên dịch vụ              |
| Danh mục         | Nhóm dịch vụ             |
| Giá dịch vụ      | Giá tiền                 |
| Thời gian (phút) | Thời lượng ước tính      |
| Trạng thái       | Đang hoạt động/Tạm ngừng |
| Thao tác         | Xem/Sửa/Xoá              |

Dữ liệu mẫu:

| STT | Mã dịch vụ | Tên dịch vụ               | Danh mục           |       Giá | Thời gian | Trạng thái     |
| --: | ---------- | ------------------------- | ------------------ | --------: | --------: | -------------- |
|   1 | DV001      | Khám tổng quát            | Khám bệnh          | 150.000 đ |        30 | Đang hoạt động |
|   2 | DV002      | Khám chuyên khoa Tim mạch | Khám bệnh          | 200.000 đ |        45 | Đang hoạt động |
|   3 | DV003      | Khám chuyên khoa Nội tiết | Khám bệnh          | 200.000 đ |        45 | Đang hoạt động |
|   4 | DV004      | Xét nghiệm máu tổng quát  | Xét nghiệm         | 120.000 đ |        15 | Đang hoạt động |
|   5 | DV005      | Xét nghiệm đường huyết    | Xét nghiệm         |  80.000 đ |        10 | Đang hoạt động |
|   6 | DV006      | Xét nghiệm mỡ máu         | Xét nghiệm         | 150.000 đ |        15 | Đang hoạt động |
|   7 | DV007      | Siêu âm ổ bụng tổng quát  | Chẩn đoán hình ảnh | 250.000 đ |        30 | Tạm ngừng      |
|   8 | DV008      | Chụp X-quang phổi         | Chẩn đoán hình ảnh | 200.000 đ |        20 | Đang hoạt động |
|   9 | DV009      | Điện tâm đồ (ECG)         | Thăm dò chức năng  | 120.000 đ |        15 | Tạm ngừng      |
|  10 | DV010      | Vật lý trị liệu           | Điều trị           | 180.000 đ |        30 | Đang hoạt động |

## 10.6 Trạng thái dịch vụ

* Đang hoạt động: xanh lá
* Tạm ngừng: cam
* Ngừng cung cấp: đỏ

## 10.7 Form thêm dịch vụ nên có

Field:

* Mã dịch vụ
* Tên dịch vụ
* Danh mục
* Giá dịch vụ
* Thời gian thực hiện
* Mô tả
* Trạng thái
* Hiển thị trên hệ thống đặt lịch hay không
* Bác sĩ/chuyên khoa phụ trách
* Ghi chú

Validation:

* Mã dịch vụ không trùng
* Tên dịch vụ bắt buộc
* Giá phải >= 0
* Thời gian phải > 0
* Danh mục bắt buộc

## 10.8 Chức năng nâng cao nên có

* Cho phép ẩn dịch vụ khỏi màn đặt lịch nhưng vẫn giữ trong hệ thống
* Không xoá cứng dịch vụ đã từng có lịch hẹn/thanh toán
* Cho phép cập nhật giá theo thời gian
* Lưu lịch sử thay đổi giá
* Gắn dịch vụ với bác sĩ hoặc chuyên khoa
* Gắn dịch vụ với phòng thực hiện
* Xuất bảng giá dịch vụ

---

# 11. Các màn chưa hiện trong ảnh nhưng sidebar có

## 11.1 Quản lý thanh toán

Nên có:

* Danh sách hoá đơn
* Tạo hoá đơn
* Xem chi tiết hoá đơn
* Thanh toán dịch vụ
* Thanh toán thuốc
* Trạng thái:

  * Chưa thanh toán
  * Đã thanh toán
  * Thanh toán một phần
  * Đã hoàn tiền
  * Đã huỷ
* Phương thức thanh toán:

  * Tiền mặt
  * Chuyển khoản
  * Thẻ
  * Ví điện tử
* In hoá đơn
* Xuất PDF
* Xuất Excel
* Thống kê doanh thu

## 11.2 Xem báo cáo thống kê

Nên có:

* Báo cáo doanh thu
* Báo cáo lượt khám
* Báo cáo bệnh nhân mới
* Báo cáo bác sĩ hoạt động
* Báo cáo thuốc
* Báo cáo dịch vụ
* Báo cáo thanh toán
* Bộ lọc theo:

  * Ngày
  * Tuần
  * Tháng
  * Quý
  * Năm
  * Khoảng ngày tuỳ chọn
* Biểu đồ:

  * Line chart
  * Bar chart
  * Donut chart
  * Table summary
* Xuất PDF/Excel

## 11.3 Phân quyền hệ thống

Nên có:

* Danh sách vai trò
* Danh sách quyền
* Tạo vai trò mới
* Sửa vai trò
* Phân quyền theo module
* Ma trận quyền:

```text
Module | Xem | Thêm | Sửa | Xoá | Xuất dữ liệu | Duyệt
```

Vai trò mẫu:

* Quản trị viên
* Bác sĩ
* Lễ tân
* Kế toán
* Điều dưỡng
* Nhân viên
* Khách hàng

## 11.4 Sao lưu dữ liệu

Nên có:

* Danh sách bản sao lưu
* Sao lưu thủ công
* Sao lưu tự động
* Khôi phục dữ liệu
* Tải file backup
* Xoá bản backup cũ
* Trạng thái:

  * Thành công
  * Thất bại
  * Đang xử lý
* Lịch backup tự động:

  * Hằng ngày lúc 02:00 AM
  * Hằng tuần
  * Hằng tháng

---

# 12. Thiết kế component nên chuẩn hoá

## 12.1 Button

### Primary button

Dùng cho nút thêm:

```text
+ Thêm tài khoản
+ Thêm bác sĩ
+ Thêm bệnh nhân
+ Thêm thuốc
+ Thêm dịch vụ
```

Style:

* Nền xanh lá
* Chữ trắng
* Bo góc 8–10px
* Có icon cộng

### Secondary button

Dùng cho Xuất Excel:

* Nền trắng
* Viền xám
* Chữ xanh/xám
* Icon Excel xanh

### Danger button

Dùng cho xoá:

* Nền đỏ hoặc đỏ nhạt
* Chữ đỏ/trắng
* Có confirm modal

## 12.2 Badge

Dùng cho trạng thái.

Ví dụ:

```text
Hoạt động
Bị khóa
Tạm nghỉ
Nghỉ việc
Còn hàng
Sắp hết
Hết hàng
Đang hoạt động
Tạm ngừng
```

Style:

* Bo tròn dạng pill
* Padding ngang 10–14px
* Padding dọc 4–6px
* Font nhỏ, medium

Màu:

* Xanh: trạng thái tốt
* Cam: cảnh báo/tạm
* Đỏ: lỗi/ngưng/khoá
* Tím/xanh dương/xám: phân loại vai trò

## 12.3 Table action icons

Mỗi dòng có 3 action:

* Eye: xem
* Edit: sửa
* Trash: xoá

Style:

* Icon nằm trong ô vuông nhỏ
* Nền xanh nhạt cho view/edit
* Nền đỏ nhạt cho delete
* Hover đổi màu đậm hơn

## 12.4 Modal xác nhận xoá

Nội dung nên có:

```text
Xác nhận xoá
Bạn có chắc chắn muốn xoá bản ghi này không? Hành động này có thể không khôi phục được.
[Huỷ] [Xoá]
```

Với dữ liệu quan trọng như bệnh nhân, bác sĩ, thuốc, dịch vụ thì nên dùng **xoá mềm**.

---

# 13. Quy tắc dữ liệu và trạng thái

## 13.1 Không nên xoá cứng dữ liệu y tế

Các dữ liệu sau không nên xoá vĩnh viễn:

* Bệnh nhân
* Bác sĩ
* Đơn thuốc
* Lịch hẹn
* Hoá đơn
* Thuốc đã từng kê
* Dịch vụ đã từng thanh toán

Thay vào đó nên có:

```text
deleted_at
status
is_active
```

## 13.2 Audit log

Vì đây là hệ thống admin y tế, nên ghi log:

* Ai tạo
* Ai sửa
* Ai xoá
* Sửa lúc nào
* Dữ liệu trước/sau
* IP/device nếu cần

Ví dụ:

```text
Admin A sửa giá dịch vụ DV001 từ 120.000đ lên 150.000đ lúc 24/05/2026 09:20
```

## 13.3 Quyền truy cập

Không phải vai trò nào cũng được làm mọi thứ.

Ví dụ:

* Admin: toàn quyền
* Kế toán: xem thanh toán, xuất báo cáo doanh thu
* Bác sĩ: xem bệnh nhân/lịch hẹn/đơn thuốc liên quan
* Lễ tân: tạo lịch hẹn, thêm bệnh nhân
* Dược sĩ/điều dưỡng: quản lý thuốc/đơn thuốc
* Khách hàng: chỉ xem thông tin của chính mình

---

# 14. Gợi ý database

Các bảng chính:

```text
users
roles
permissions
role_permissions

doctors
doctor_specialties
doctor_schedules

patients
medical_records
appointments

services
service_categories

medicines
medicine_categories
medicine_suppliers
medicine_batches
medicine_stock_logs

prescriptions
prescription_items

payments
payment_items

notifications
backups
audit_logs
```

## 14.1 Bảng users

```text
id
full_name
email
phone
password_hash
avatar_url
role_id
status
last_login_at
created_at
updated_at
deleted_at
```

## 14.2 Bảng doctors

```text
id
user_id
doctor_code
specialty_id
degree
license_number
experience_years
status
working_status
created_at
updated_at
deleted_at
```

## 14.3 Bảng patients

```text
id
patient_code
full_name
gender
date_of_birth
phone
email
citizen_id
address
status
blood_type
allergy_note
medical_history
created_at
updated_at
deleted_at
```

## 14.4 Bảng medicines

```text
id
medicine_code
name
active_ingredient
category_id
unit
supplier_id
quantity
min_stock
import_price
sale_price
status
description
created_at
updated_at
deleted_at
```

## 14.5 Bảng services

```text
id
service_code
name
category_id
price
duration_minutes
description
status
is_visible
created_at
updated_at
deleted_at
```

---

# 15. Gợi ý API cho các màn danh sách

## 15.1 API lấy danh sách tài khoản

```http
GET /api/admin/users?search=&role=&status=&page=1&limit=10
```

Response:

```json
{
  "data": [],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 56,
    "totalPages": 6
  },
  "summary": {
    "totalAccounts": 56,
    "activeAccounts": 48,
    "lockedAccounts": 5,
    "totalRoles": 6
  }
}
```

## 15.2 API lấy danh sách bác sĩ

```http
GET /api/admin/doctors?search=&specialty=&status=&workingStatus=&page=1&limit=10
```

## 15.3 API lấy danh sách bệnh nhân

```http
GET /api/admin/patients?search=&gender=&ageGroup=&status=&page=1&limit=10
```

## 15.4 API lấy danh sách thuốc

```http
GET /api/admin/medicines?search=&category=&supplier=&status=&page=1&limit=10
```

## 15.5 API lấy danh sách dịch vụ

```http
GET /api/admin/services?search=&category=&status=&visible=&page=1&limit=10
```

## 15.6 API dashboard

```http
GET /api/admin/dashboard?range=this_month
```

Nên trả về:

* KPI tổng quan
* Biểu đồ lượt khám
* Doanh thu
* Lịch hẹn sắp tới
* Thông báo
* Thống kê nhanh

---

# 16. Luồng thao tác chuẩn

## 16.1 Thêm mới

Ví dụ thêm bệnh nhân:

1. Admin click **+ Thêm bệnh nhân**
2. Mở modal hoặc trang form
3. Nhập thông tin
4. Validate
5. Submit
6. Hiển thị loading
7. Thành công:

   * Toast: “Thêm bệnh nhân thành công”
   * Reload table
8. Thất bại:

   * Hiển thị lỗi cụ thể

## 16.2 Sửa

1. Click icon bút
2. Load dữ liệu bản ghi
3. Mở form sửa
4. Admin cập nhật
5. Submit
6. Toast thành công
7. Reload dòng hoặc reload table

## 16.3 Xoá

1. Click icon thùng rác
2. Modal xác nhận
3. Nếu xác nhận:

   * Gọi API xoá mềm
   * Toast thành công
   * Reload table

## 16.4 Xem chi tiết

1. Click icon mắt
2. Mở modal/trang chi tiết
3. Hiển thị đầy đủ thông tin
4. Có thể có tab:

   * Thông tin chung
   * Lịch sử
   * Ghi chú
   * Nhật ký hoạt động

---

# 17. Responsive

## Desktop

Giống ảnh:

* Sidebar luôn mở
* 4 card KPI trên 1 hàng
* Bảng full width
* Filter nằm ngang

## Tablet

* Sidebar thu gọn hoặc thành drawer
* KPI thành 2 cột x 2 hàng
* Filter có thể xuống dòng
* Bảng có scroll ngang

## Mobile

* Sidebar thành menu hamburger
* KPI xếp 1 cột
* Search full width
* Filter xếp dọc
* Bảng chuyển thành card list hoặc scroll ngang
* Action icon vẫn giữ ở cuối mỗi dòng/card

---

# 18. Mô tả ngắn cho dev làm theo

Hệ thống là admin dashboard cho phòng khám CarePlus. Tất cả màn hình dùng layout chung gồm sidebar trái, header trên cùng và nội dung chính. Sidebar có menu quản trị, item active nền xanh nhạt. Header có tiêu đề, breadcrumb, chuông thông báo có badge, avatar admin và dropdown tài khoản.

Các màn quản lý danh sách có 4 card thống kê ở đầu trang, bên dưới là thanh tìm kiếm + filter + nút thêm + xuất Excel, tiếp theo là bảng dữ liệu có checkbox, trạng thái dạng badge, action xem/sửa/xoá và phân trang. Màu chủ đạo là xanh lá, dùng xanh dương cho tổng số, xanh lá cho hoạt động, cam cho cảnh báo/tạm ngưng, tím cho nhóm phụ và đỏ cho trạng thái xấu.

Các module chính gồm quản lý tài khoản, bác sĩ, bệnh nhân, thuốc, dịch vụ. Mỗi module cần hỗ trợ CRUD, tìm kiếm, lọc, phân trang, xuất Excel, xem chi tiết, xác nhận xoá và phân quyền theo vai trò. Dashboard cần hiển thị KPI tổng quan, biểu đồ lượt khám, doanh thu, lịch hẹn sắp tới, thông báo hệ thống và thống kê nhanh.
