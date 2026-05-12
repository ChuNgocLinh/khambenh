Dưới đây là mô tả thật kỹ giao diện **CarePlus Admin – Quản lý bác sĩ**, đủ để đưa cho designer/dev làm lại gần giống và có thể suy ra chức năng cần có.

---

# Mô tả giao diện: CarePlus Admin – Quản lý bác sĩ

Đây là màn hình quản trị dành cho admin của hệ thống y tế **CarePlus Admin**, dùng để quản lý danh sách bác sĩ trong hệ thống. Giao diện có bố cục dạng **dashboard admin hiện đại**, nền sáng, nhiều khoảng trắng, bo góc mềm, màu chủ đạo xanh lá và xanh dương.

Màn hình được chia thành 2 khu vực chính:

1. **Sidebar bên trái**: dùng để điều hướng giữa các module quản trị.
2. **Khu vực nội dung chính bên phải**: hiển thị tiêu đề trang, thống kê nhanh, bộ lọc, bảng danh sách bác sĩ và phân trang.

---

# 1. Sidebar bên trái

Sidebar nằm cố định ở cạnh trái màn hình, chiều rộng khoảng **270–290px**, nền trắng. Bên trong có logo, menu điều hướng và nút đăng xuất.

## 1.1 Logo

Ở góc trên cùng bên trái có logo:

* Icon dấu cộng y tế màu xanh lá.
* Text: **CarePlus Admin**
* Chữ “CarePlus” và “Admin” màu xanh lá, font đậm.
* Logo nằm ngang, căn giữa theo chiều dọc với icon.

Gợi ý style:

* Icon tròn hoặc dạng medical plus.
* Màu xanh chủ đạo: `#16A34A` hoặc gần tương tự.
* Font chữ đậm, kích thước khoảng `22–24px`.

---

## 1.2 Danh sách menu

Các menu được xếp dọc, mỗi item có icon bên trái và text bên phải. Khoảng cách giữa các item khá thoáng.

Danh sách menu gồm:

1. **Dashboard**
2. **Quản lý tài khoản**
3. **Quản lý bác sĩ**
4. **Quản lý bệnh nhân**
5. **Quản lý thuốc**
6. **Quản lý dịch vụ**
7. **Quản lý thanh toán**
8. **Xem báo cáo thống kê**
9. **Phân quyền hệ thống**
10. **Sao lưu dữ liệu**

Menu đang được chọn là **Quản lý bác sĩ**.

### Trạng thái menu đang active

Item “Quản lý bác sĩ” có:

* Nền xanh lá nhạt.
* Text màu xanh lá.
* Icon màu xanh lá.
* Bo góc khoảng `8–12px`.
* Padding trái/phải rộng.
* Tạo cảm giác đang ở đúng module hiện tại.

Các menu khác:

* Icon màu xanh đen/xám đậm.
* Text màu xanh đen.
* Không có background.

---

## 1.3 Nút đăng xuất

Ở cuối sidebar có nút **Đăng xuất**.

Đặc điểm:

* Nền đỏ rất nhạt.
* Text màu đỏ.
* Icon logout màu đỏ.
* Bo góc mềm.
* Nút chiếm gần hết chiều rộng sidebar.
* Nằm sát cuối màn hình, tạo cảm giác cố định.

Chức năng suy đoán:

* Khi bấm vào sẽ hiển thị popup xác nhận:

  * “Bạn có chắc chắn muốn đăng xuất không?”
  * Nút “Hủy”
  * Nút “Đăng xuất”
* Sau khi xác nhận thì xóa token/session và chuyển về màn hình đăng nhập.

---

# 2. Khu vực nội dung chính

Khu vực bên phải chiếm phần lớn màn hình. Nền tổng thể là màu trắng hơi xám nhạt, tạo sự phân tách với các card và bảng.

Padding chính khoảng `32px`.

---

# 3. Header của trang

Ở đầu khu vực nội dung có tiêu đề:

## 3.1 Tiêu đề trang

Text lớn: **Quản lý bác sĩ**

* Font đậm.
* Màu xanh đen.
* Kích thước khoảng `26–30px`.
* Nằm phía trên bên trái.

Bên dưới có breadcrumb:

**Dashboard / Quản lý bác sĩ**

* Text nhỏ hơn.
* Màu xám xanh.
* Dùng để cho biết người dùng đang ở module nào.

---

## 3.2 Khu vực tài khoản admin

Ở góc trên bên phải có cụm thông tin admin gồm:

1. Icon chuông thông báo.
2. Badge đỏ hiển thị số lượng thông báo: **3**
3. Avatar admin.
4. Text: **Admin (Quản trị viên)**
5. Icon mũi tên xổ xuống.

### Chức năng suy đoán

#### Icon chuông

Khi bấm vào chuông:

* Mở dropdown danh sách thông báo.
* Hiển thị các thông báo gần đây như:

  * Bác sĩ mới được thêm.
  * Có yêu cầu nghỉ phép.
  * Có tài khoản cần duyệt.
  * Có cảnh báo hệ thống.
* Badge đỏ thể hiện số thông báo chưa đọc.
* Khi mở/xem thông báo thì có thể đánh dấu đã đọc.

#### Avatar / tên admin

Khi bấm vào tên admin hoặc mũi tên:

* Mở menu tài khoản.
* Các lựa chọn có thể gồm:

  * Thông tin cá nhân
  * Đổi mật khẩu
  * Cài đặt tài khoản
  * Đăng xuất

---

# 4. Khu vực thống kê nhanh

Ngay dưới header có 4 card thống kê nằm ngang, chia đều chiều rộng.

Các card có nền trắng, bo góc, viền mỏng, bóng rất nhẹ. Mỗi card gồm:

* Icon bên trái.
* Tiêu đề chỉ số.
* Số liệu lớn.
* Dòng so sánh với tháng trước.

---

## 4.1 Card “Tổng bác sĩ”

Nội dung:

* Icon bác sĩ màu trắng trên nền xanh dương.
* Tiêu đề: **Tổng bác sĩ**
* Số liệu: **42**
* Dòng tăng trưởng: **↑ 8% so với tháng trước**

Màu sắc:

* Icon card xanh dương.
* Số liệu màu xanh dương.
* Mũi tên tăng màu xanh lá.
* Text phụ màu xám xanh.

Chức năng suy đoán:

* Hiển thị tổng số bác sĩ trong hệ thống, bao gồm cả đang hoạt động, tạm nghỉ và nghỉ việc.
* Khi bấm vào card có thể lọc bảng về tất cả bác sĩ.

---

## 4.2 Card “Đang hoạt động”

Nội dung:

* Icon bác sĩ màu trắng trên nền xanh lá.
* Tiêu đề: **Đang hoạt động**
* Số liệu: **38**
* Dòng tăng trưởng: **↑ 7% so với tháng trước**

Ý nghĩa:

* Số bác sĩ có trạng thái tài khoản là “Hoạt động”.
* Có thể là bác sĩ đang được phép đăng nhập, đặt lịch, tư vấn hoặc khám bệnh.

Chức năng suy đoán:

* Bấm vào card sẽ tự động set filter “Trạng thái = Hoạt động”.

---

## 4.3 Card “Tạm nghỉ”

Nội dung:

* Icon người màu trắng trên nền cam.
* Tiêu đề: **Tạm nghỉ**
* Số liệu: **3**
* Dòng so sánh: **↓ 2% so với tháng trước**

Ý nghĩa:

* Số bác sĩ tạm thời không làm việc.
* Có thể do nghỉ phép, nghỉ bệnh, nghỉ thai sản hoặc tạm khóa lịch khám.

Chức năng suy đoán:

* Bấm vào card sẽ lọc danh sách bác sĩ có tình trạng “Nghỉ phép” hoặc trạng thái “Tạm nghỉ”.

---

## 4.4 Card “Nghỉ việc”

Nội dung:

* Icon người màu trắng trên nền tím.
* Tiêu đề: **Nghỉ việc**
* Số liệu: **1**
* Dòng so sánh: **↓ 1% so với tháng trước**

Ý nghĩa:

* Số bác sĩ đã nghỉ việc hoặc ngừng hợp tác.
* Có thể vẫn lưu hồ sơ trong hệ thống nhưng không còn hoạt động.

Chức năng suy đoán:

* Bấm vào card sẽ lọc danh sách bác sĩ có trạng thái “Nghỉ việc”.

---

# 5. Khu vực bộ lọc và thao tác

Phía dưới các card thống kê là một khung lớn chứa bộ lọc, nút thao tác và bảng dữ liệu.

Khung này có:

* Nền trắng.
* Bo góc lớn.
* Viền nhẹ.
* Padding khoảng `20–24px`.

---

## 5.1 Thanh tìm kiếm

Nằm bên trái, chiếm chiều rộng lớn nhất trong hàng filter.

Placeholder:

**Tìm kiếm bác sĩ (Tên, chuyên khoa, SĐT...)**

Có icon kính lúp ở bên trái.

Chức năng:

* Cho phép tìm bác sĩ theo:

  * Họ tên
  * Chuyên khoa
  * Số điện thoại
  * Email
  * Mã bác sĩ nếu hệ thống có
* Có thể tìm gần đúng, không phân biệt hoa thường.
* Nên có debounce khoảng 300–500ms để tránh gọi API liên tục.
* Khi nhập text, bảng bên dưới tự động cập nhật kết quả.

---

## 5.2 Bộ lọc “Chuyên khoa”

Dropdown có label **Chuyên khoa**.

Giá trị hiện tại: **Tất cả**

Các lựa chọn có thể gồm:

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

Chức năng:

* Lọc danh sách bác sĩ theo chuyên khoa.
* Khi chọn một chuyên khoa, bảng chỉ hiển thị bác sĩ thuộc chuyên khoa đó.

---

## 5.3 Bộ lọc “Trạng thái”

Dropdown có label **Trạng thái**.

Giá trị hiện tại: **Tất cả**

Các lựa chọn nên có:

* Tất cả
* Hoạt động
* Tạm nghỉ
* Nghỉ việc
* Bị khóa nếu hệ thống có quản lý tài khoản

Ý nghĩa:

* Đây có thể là trạng thái tài khoản/hồ sơ của bác sĩ.
* “Hoạt động” nghĩa là tài khoản còn sử dụng.
* “Tạm nghỉ” nghĩa là tạm ngưng làm việc nhưng chưa xóa.
* “Nghỉ việc” nghĩa là không còn làm việc.

---

## 5.4 Bộ lọc “Tình trạng”

Dropdown có label **Tình trạng**.

Giá trị hiện tại: **Tất cả**

Các lựa chọn nên có:

* Tất cả
* Đang làm việc
* Nghỉ phép
* Đã nghỉ việc
* Đang chờ duyệt
* Tạm khóa lịch

Điểm khác nhau giữa “Trạng thái” và “Tình trạng”:

* **Trạng thái** có thể nói về tài khoản/hồ sơ trong hệ thống.
* **Tình trạng** có thể nói về tình hình làm việc thực tế của bác sĩ.

Ví dụ:

* Một bác sĩ có trạng thái **Hoạt động** nhưng tình trạng **Nghỉ phép**.
* Một bác sĩ có trạng thái **Nghỉ việc** và tình trạng **Đã nghỉ việc**.

---

## 5.5 Nút “Thêm bác sĩ”

Nằm phía bên phải, màu xanh lá, nổi bật nhất trong khu vực thao tác.

Text: **+ Thêm bác sĩ**

Style:

* Nền xanh lá.
* Text trắng.
* Icon dấu cộng.
* Bo góc `8–10px`.
* Padding ngang rộng.
* Chiều cao khoảng `44–48px`.

Chức năng:

* Mở form thêm bác sĩ mới.
* Có thể mở dưới dạng modal, drawer hoặc chuyển sang trang riêng.

Form thêm bác sĩ nên có các trường:

### Thông tin cá nhân

* Họ và tên
* Giới tính
* Ngày sinh
* Ảnh đại diện
* Số điện thoại
* Email
* Địa chỉ

### Thông tin chuyên môn

* Chuyên khoa
* Học vị / chức danh
* Số năm kinh nghiệm
* Bằng cấp
* Chứng chỉ hành nghề
* Mô tả chuyên môn
* Dịch vụ phụ trách

### Thông tin làm việc

* Trạng thái
* Tình trạng
* Lịch làm việc
* Phòng khám / cơ sở làm việc
* Giá khám nếu hệ thống có đặt lịch
* Thời lượng mỗi lượt khám

### Thông tin tài khoản

* Username hoặc email đăng nhập
* Mật khẩu tạm thời
* Vai trò
* Quyền truy cập
* Gửi email kích hoạt tài khoản

Validation nên có:

* Họ tên không được trống.
* Email đúng định dạng và không trùng.
* Số điện thoại đúng định dạng và không trùng.
* Chuyên khoa bắt buộc chọn.
* Ảnh đại diện đúng định dạng.
* Chứng chỉ hành nghề có thể bắt buộc nếu là hệ thống y tế thật.

---

## 5.6 Nút “Xuất Excel”

Nằm bên dưới hoặc gần nút “Thêm bác sĩ”, màu trắng, viền nhẹ.

Text: **Xuất Excel**

Có icon Excel màu xanh lá.

Chức năng:

* Xuất danh sách bác sĩ ra file `.xlsx`.
* Dữ liệu xuất nên phụ thuộc vào bộ lọc hiện tại.
* Nếu đang tìm kiếm/lọc, file Excel chỉ nên xuất các kết quả đang hiển thị hoặc toàn bộ kết quả phù hợp filter.
* Nên có popup hỏi:

  * “Xuất toàn bộ danh sách”
  * “Xuất theo bộ lọc hiện tại”
  * “Xuất các dòng đã chọn”

Các cột Excel nên gồm:

* STT
* Họ và tên
* Chuyên khoa
* Số điện thoại
* Email
* Trạng thái
* Tình trạng
* Ngày tạo
* Ngày cập nhật
* Ghi chú nếu có

---

# 6. Bảng danh sách bác sĩ

Bảng nằm bên dưới bộ lọc. Đây là phần chính của màn hình.

Bảng có nền trắng, đường kẻ ngang mảnh, header nền trắng/xám rất nhạt.

## 6.1 Các cột trong bảng

Bảng gồm các cột:

1. Checkbox chọn dòng
2. **STT**
3. **Họ và tên**
4. **Chuyên khoa**
5. **SĐT**
6. **Email**
7. **Trạng thái**
8. **Tình trạng**
9. **Ngày tạo**
10. **Thao tác**

---

## 6.2 Checkbox chọn nhiều dòng

Ở header có checkbox tổng.

Chức năng:

* Tick checkbox ở header để chọn tất cả bác sĩ đang hiển thị trên trang hiện tại.
* Tick từng dòng để chọn riêng từng bác sĩ.
* Khi chọn một hoặc nhiều dòng, nên hiện thanh thao tác hàng loạt.

Các thao tác hàng loạt có thể có:

* Xóa nhiều bác sĩ
* Chuyển trạng thái sang “Tạm nghỉ”
* Chuyển trạng thái sang “Hoạt động”
* Xuất Excel các dòng đã chọn
* Gửi thông báo/email cho các bác sĩ đã chọn

---

## 6.3 Cột STT

Hiển thị số thứ tự từ 1 đến 10 trên trang hiện tại.

Nếu phân trang, STT nên tính theo công thức:

`STT = (trang hiện tại - 1) * số dòng mỗi trang + index + 1`

Ví dụ:

* Trang 1: 1–10
* Trang 2: 11–20
* Trang 3: 21–30

---

## 6.4 Cột “Họ và tên”

Cột này gồm:

* Ảnh avatar nhỏ hình tròn.
* Tên bác sĩ nằm bên phải avatar.

Danh sách trong ảnh:

1. Nguyễn Văn Nam
2. Trần Thị Mai
3. Lê Văn Cường
4. Phạm Thị Lan
5. Hoàng Anh Tuấn
6. Vũ Thị Hương
7. Đỗ Minh Quân
8. Bùi Văn Dũng
9. Nguyễn Thị Hoa
10. Trương Văn Kiên

Avatar:

* Kích thước khoảng `28–36px`.
* Hình tròn.
* Có thể dùng ảnh thật hoặc ảnh mặc định theo giới tính.
* Nên có fallback nếu không có ảnh: hiển thị chữ cái đầu tên hoặc icon người dùng.

Chức năng suy đoán:

* Bấm vào tên hoặc avatar có thể mở trang chi tiết hồ sơ bác sĩ.
* Có thể hover để hiện tooltip nhanh: tên, chuyên khoa, email.

---

## 6.5 Cột “Chuyên khoa”

Hiển thị chuyên khoa của bác sĩ.

Các chuyên khoa trong bảng:

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

Chức năng:

* Có thể lọc theo chuyên khoa.
* Có thể dùng chuyên khoa để phân quyền lịch khám/dịch vụ.

---

## 6.6 Cột “SĐT”

Hiển thị số điện thoại bác sĩ, ví dụ:

* 0987 654 321
* 0912 346 678
* 0933 456 789
* 0909 876 543
* 0988 765 432
* 0977 654 321
* 0966 543 210
* 0982 333 444
* 0908 111 222
* 0933 999 000

Chức năng suy đoán:

* Có thể click để gọi nếu dùng trên mobile.
* Có thể copy nhanh số điện thoại.
* Nên validate số điện thoại khi thêm/sửa.

---

## 6.7 Cột “Email”

Hiển thị email bác sĩ, ví dụ:

* [nam.nguyen@gmail.com](mailto:nam.nguyen@gmail.com)
* [mai.tran@gmail.com](mailto:mai.tran@gmail.com)
* [cuong.le@gmail.com](mailto:cuong.le@gmail.com)
* [lan.pham@gmail.com](mailto:lan.pham@gmail.com)
* [tuan.hoang@gmail.com](mailto:tuan.hoang@gmail.com)
* [huong.vu@gmail.com](mailto:huong.vu@gmail.com)
* [quan.do@gmail.com](mailto:quan.do@gmail.com)
* [dung.bui@gmail.com](mailto:dung.bui@gmail.com)
* [hoa.nguyen@gmail.com](mailto:hoa.nguyen@gmail.com)
* [kien.truong@gmail.com](mailto:kien.truong@gmail.com)

Chức năng suy đoán:

* Có thể click để gửi email.
* Có thể copy nhanh email.
* Email có thể dùng làm tài khoản đăng nhập.

---

## 6.8 Cột “Trạng thái”

Hiển thị badge màu.

Các trạng thái xuất hiện:

### Hoạt động

* Badge xanh lá nhạt.
* Text xanh lá.
* Ý nghĩa: bác sĩ đang hoạt động bình thường.

### Tạm nghỉ

* Badge cam nhạt.
* Text cam.
* Ý nghĩa: bác sĩ tạm nghỉ, có thể nghỉ phép hoặc tạm không nhận lịch.

### Nghỉ việc

* Badge đỏ nhạt.
* Text đỏ.
* Ý nghĩa: bác sĩ đã nghỉ việc/ngừng hoạt động.

Chức năng:

* Có thể chỉnh trạng thái khi sửa hồ sơ bác sĩ.
* Có thể ảnh hưởng đến khả năng hiển thị bác sĩ trên app bệnh nhân.
* Nếu trạng thái “Nghỉ việc”, bác sĩ không nên xuất hiện trong lịch đặt khám mới.

---

## 6.9 Cột “Tình trạng”

Hiển thị badge tương tự trạng thái nhưng mô tả tình hình làm việc cụ thể hơn.

Các tình trạng xuất hiện:

### Đang làm việc

* Badge xanh lá nhạt.
* Text xanh lá.

### Nghỉ phép

* Badge cam nhạt.
* Text cam.

### Đã nghỉ việc

* Badge đỏ nhạt.
* Text đỏ.

Chức năng:

* Cho biết bác sĩ hiện có đang nhận lịch không.
* Nếu “Nghỉ phép”, hệ thống có thể tạm ẩn lịch làm việc trong thời gian nghỉ.
* Nếu “Đã nghỉ việc”, hệ thống có thể khóa tài khoản và không cho tạo lịch mới.

---

## 6.10 Cột “Ngày tạo”

Tất cả dòng trong ảnh đều có ngày tạo: **24/05/2026**

Ý nghĩa:

* Ngày hồ sơ bác sĩ được tạo trong hệ thống.
* Nên lưu thêm ngày cập nhật ở database, dù không hiển thị.

Định dạng:

* `dd/mm/yyyy`

---

## 6.11 Cột “Thao tác”

Mỗi dòng có 3 nút thao tác ở bên phải:

1. Icon mắt màu xanh dương
2. Icon bút chỉnh sửa màu xanh dương
3. Icon thùng rác màu đỏ

### Nút xem chi tiết

Icon: mắt.

Chức năng:

* Mở trang hoặc modal xem chi tiết bác sĩ.
* Không cho chỉnh sửa trực tiếp.
* Thông tin nên gồm:

  * Ảnh đại diện
  * Họ tên
  * Chuyên khoa
  * SĐT
  * Email
  * Trạng thái
  * Tình trạng
  * Lịch làm việc
  * Bằng cấp/chứng chỉ
  * Số lượt khám
  * Đánh giá trung bình nếu có
  * Lịch sử thay đổi trạng thái

### Nút chỉnh sửa

Icon: bút.

Chức năng:

* Mở form sửa thông tin bác sĩ.
* Form có dữ liệu hiện tại được điền sẵn.
* Cho phép cập nhật:

  * Thông tin cá nhân
  * Chuyên khoa
  * SĐT
  * Email
  * Trạng thái
  * Tình trạng
  * Lịch làm việc
  * Avatar
  * Quyền truy cập

Nên có nút:

* Lưu thay đổi
* Hủy
* Đặt lại dữ liệu

### Nút xóa

Icon: thùng rác màu đỏ.

Chức năng:

* Xóa bác sĩ khỏi danh sách.
* Nên hiện popup xác nhận trước khi xóa.

Popup gợi ý:

> Bạn có chắc chắn muốn xóa bác sĩ này không?
> Hành động này có thể ảnh hưởng đến lịch khám và dữ liệu liên quan.

Nút:

* Hủy
* Xóa

Lưu ý nghiệp vụ:

* Không nên xóa cứng nếu bác sĩ đã có lịch khám, bệnh án hoặc giao dịch.
* Nên dùng soft delete hoặc chuyển trạng thái sang “Nghỉ việc”.
* Nếu bắt buộc xóa, cần kiểm tra ràng buộc dữ liệu trước.

---

# 7. Dữ liệu mẫu đang hiển thị trong bảng

Có 10 bác sĩ trên trang hiện tại:

| STT | Họ và tên       | Chuyên khoa   | SĐT          | Email                                                 | Trạng thái | Tình trạng    | Ngày tạo   |
| --- | --------------- | ------------- | ------------ | ----------------------------------------------------- | ---------- | ------------- | ---------- |
| 1   | Nguyễn Văn Nam  | Nội tổng quát | 0987 654 321 | [nam.nguyen@gmail.com](mailto:nam.nguyen@gmail.com)   | Hoạt động  | Đang làm việc | 24/05/2026 |
| 2   | Trần Thị Mai    | Nhi khoa      | 0912 346 678 | [mai.tran@gmail.com](mailto:mai.tran@gmail.com)       | Hoạt động  | Đang làm việc | 24/05/2026 |
| 3   | Lê Văn Cường    | Tim mạch      | 0933 456 789 | [cuong.le@gmail.com](mailto:cuong.le@gmail.com)       | Hoạt động  | Đang làm việc | 24/05/2026 |
| 4   | Phạm Thị Lan    | Sản phụ khoa  | 0909 876 543 | [lan.pham@gmail.com](mailto:lan.pham@gmail.com)       | Tạm nghỉ   | Nghỉ phép     | 24/05/2026 |
| 5   | Hoàng Anh Tuấn  | Ngoại khoa    | 0988 765 432 | [tuan.hoang@gmail.com](mailto:tuan.hoang@gmail.com)   | Hoạt động  | Đang làm việc | 24/05/2026 |
| 6   | Vũ Thị Hương    | Da liễu       | 0977 654 321 | [huong.vu@gmail.com](mailto:huong.vu@gmail.com)       | Hoạt động  | Đang làm việc | 24/05/2026 |
| 7   | Đỗ Minh Quân    | Răng hàm mặt  | 0966 543 210 | [quan.do@gmail.com](mailto:quan.do@gmail.com)         | Hoạt động  | Đang làm việc | 24/05/2026 |
| 8   | Bùi Văn Dũng    | Thần kinh     | 0982 333 444 | [dung.bui@gmail.com](mailto:dung.bui@gmail.com)       | Nghỉ việc  | Đã nghỉ việc  | 24/05/2026 |
| 9   | Nguyễn Thị Hoa  | Mắt           | 0908 111 222 | [hoa.nguyen@gmail.com](mailto:hoa.nguyen@gmail.com)   | Hoạt động  | Đang làm việc | 24/05/2026 |
| 10  | Trương Văn Kiên | Tai mũi họng  | 0933 999 000 | [kien.truong@gmail.com](mailto:kien.truong@gmail.com) | Hoạt động  | Đang làm việc | 24/05/2026 |

---

# 8. Phân trang

Bên dưới bảng có phần phân trang.

Bên trái:

* Text: **Hiển thị**
* Dropdown: **10**
* Text: **bản ghi**

Ý nghĩa:

* Người dùng có thể chọn số bản ghi mỗi trang.
* Các lựa chọn nên có:

  * 10
  * 20
  * 50
  * 100

Bên phải:

* Nút quay lại trang trước.
* Các số trang: **1, 2, 3, 4, 5, ...**
* Nút sang trang tiếp theo.

Trang hiện tại là **1**, được tô nền xanh lá, text trắng.

Chức năng:

* Chuyển trang danh sách bác sĩ.
* Khi đổi trang, giữ nguyên bộ lọc hiện tại.
* Khi tìm kiếm hoặc đổi bộ lọc, nên quay về trang 1.
* Nút previous bị disable nếu đang ở trang đầu.
* Nút next bị disable nếu đang ở trang cuối.

Lưu ý nhỏ: trong ảnh phần phân trang có vẻ hiển thị `1 2 3 4 5 ... 5`, hơi giống bị lặp số 5. Khi làm thật nên sửa thành dạng hợp lý hơn, ví dụ:

`1 2 3 4 5 ... 10`

hoặc nếu chỉ có 5 trang thì chỉ cần:

`1 2 3 4 5`

---

# 9. Luồng chức năng chính cần có

## 9.1 Xem danh sách bác sĩ

Khi vào trang, hệ thống gọi API lấy danh sách bác sĩ.

Dữ liệu cần trả về:

* Tổng số bác sĩ
* Danh sách bác sĩ theo trang
* Tổng số trang
* Số bản ghi mỗi trang
* Bộ lọc đang áp dụng
* Thống kê nhanh ở các card

---

## 9.2 Tìm kiếm bác sĩ

Người dùng nhập vào ô tìm kiếm.

Hệ thống tìm theo:

* Tên bác sĩ
* Chuyên khoa
* Số điện thoại
* Email

Kết quả bảng cập nhật theo từ khóa.

Nếu không có dữ liệu, hiển thị empty state:

> Không tìm thấy bác sĩ phù hợp.

---

## 9.3 Lọc bác sĩ

Người dùng có thể lọc theo:

* Chuyên khoa
* Trạng thái
* Tình trạng

Các filter có thể kết hợp với nhau.

Ví dụ:

* Chuyên khoa: Tim mạch
* Trạng thái: Hoạt động
* Tình trạng: Đang làm việc

Kết quả chỉ hiển thị bác sĩ tim mạch đang hoạt động và đang làm việc.

---

## 9.4 Thêm bác sĩ

Khi bấm “Thêm bác sĩ”:

* Mở form thêm mới.
* Admin nhập thông tin.
* Hệ thống validate dữ liệu.
* Nếu hợp lệ, tạo bác sĩ mới.
* Sau khi tạo thành công:

  * Đóng modal/form.
  * Refresh bảng.
  * Cập nhật thống kê.
  * Hiện toast: “Thêm bác sĩ thành công.”

---

## 9.5 Xem chi tiết bác sĩ

Khi bấm icon mắt:

* Mở chi tiết hồ sơ bác sĩ.
* Có thể hiển thị dạng modal lớn hoặc trang riêng.

Thông tin nên có:

* Thông tin cá nhân
* Thông tin liên hệ
* Chuyên khoa
* Học vị
* Chứng chỉ
* Lịch làm việc
* Trạng thái hiện tại
* Lịch sử lịch khám
* Đánh giá từ bệnh nhân nếu có

---

## 9.6 Chỉnh sửa bác sĩ

Khi bấm icon bút:

* Mở form chỉnh sửa.
* Dữ liệu cũ được load sẵn.
* Admin chỉnh sửa và lưu.
* Sau khi lưu:

  * Cập nhật bảng.
  * Cập nhật thống kê nếu trạng thái thay đổi.
  * Hiện toast: “Cập nhật bác sĩ thành công.”

---

## 9.7 Xóa hoặc ngừng hoạt động bác sĩ

Khi bấm icon thùng rác:

* Hiển thị popup xác nhận.
* Nếu bác sĩ chưa có dữ liệu liên quan, có thể xóa.
* Nếu bác sĩ đã có lịch khám/bệnh án, nên không xóa cứng mà chuyển trạng thái sang “Nghỉ việc”.

Thông báo gợi ý:

> Không thể xóa bác sĩ vì đã có dữ liệu lịch khám. Bạn có thể chuyển trạng thái sang “Nghỉ việc”.

---

## 9.8 Xuất Excel

Khi bấm “Xuất Excel”:

* Xuất danh sách theo bộ lọc hiện tại.
* File tải về có tên dạng:

`danh_sach_bac_si_2026_05_24.xlsx`

Nên có loading khi xuất file.

---

# 10. Các trạng thái giao diện cần xử lý

## Loading

Khi đang tải dữ liệu:

* Card thống kê hiển thị skeleton.
* Bảng hiển thị skeleton rows.
* Nút bị disable nếu cần.

## Empty

Khi không có bác sĩ:

* Hiển thị icon rỗng.
* Text: “Chưa có bác sĩ nào.”
* Nút: “Thêm bác sĩ”

## Không tìm thấy kết quả

Khi tìm kiếm/lọc không ra kết quả:

* Text: “Không tìm thấy bác sĩ phù hợp.”
* Có nút “Xóa bộ lọc”.

## Error

Khi lỗi API:

* Hiển thị thông báo:

  * “Không thể tải danh sách bác sĩ. Vui lòng thử lại.”
* Có nút “Tải lại”.

## Success toast

Các thao tác thành công nên hiện toast:

* “Thêm bác sĩ thành công.”
* “Cập nhật thông tin bác sĩ thành công.”
* “Xóa bác sĩ thành công.”
* “Xuất Excel thành công.”

## Warning/Error toast

Ví dụ:

* “Email đã tồn tại.”
* “Số điện thoại đã tồn tại.”
* “Không thể xóa bác sĩ vì đã có lịch khám.”
* “Vui lòng điền đầy đủ thông tin bắt buộc.”

---

# 11. Gợi ý thiết kế UI chi tiết

## Màu sắc

Màu chủ đạo:

* Xanh lá chính: `#16A34A`
* Xanh lá nhạt nền active: `#EAF7EE`
* Xanh dương: `#2563EB`
* Cam: `#F97316`
* Đỏ: `#EF4444`
* Tím: `#7E22CE`
* Text chính: `#0F172A`
* Text phụ: `#64748B`
* Border: `#E5E7EB`
* Background tổng: `#F8FAFC`

## Font

Có thể dùng:

* Inter
* Be Vietnam Pro
* Roboto
* SF Pro Display

Font size gợi ý:

* Logo: `22–24px`
* Tiêu đề trang: `28px`
* Breadcrumb: `14px`
* Card title: `15–16px`
* Số thống kê: `28–32px`
* Table header: `13–14px`
* Table body: `14px`
* Button: `14–15px`

## Bo góc

* Card thống kê: `16px`
* Khung bảng: `16px`
* Button: `8–10px`
* Badge: `8–12px`
* Input/dropdown: `8–10px`

## Shadow

Dùng shadow nhẹ:

* Card: shadow rất mờ.
* Không nên dùng shadow quá đậm vì giao diện đang theo phong cách clean admin.

Ví dụ:

```css
box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04);
```

---

# 12. Responsive

## Desktop

Layout như ảnh:

* Sidebar cố định bên trái.
* Main content bên phải.
* 4 card thống kê nằm ngang.
* Filter nằm một hàng.
* Bảng full width.

## Tablet

Có thể chuyển thành:

* Sidebar thu gọn chỉ còn icon.
* 4 card thành 2 cột.
* Filter chia thành 2 hàng.
* Bảng có horizontal scroll.

## Mobile

Nên làm:

* Sidebar chuyển thành drawer mở bằng hamburger.
* Card thống kê thành 1 cột hoặc 2 cột.
* Filter xếp dọc.
* Bảng chuyển thành card list hoặc cho scroll ngang.
* Các nút thao tác nên lớn hơn để dễ bấm.

---

# 13. Cấu trúc dữ liệu bác sĩ gợi ý

Một object bác sĩ có thể gồm:

```json
{
  "id": "doctor_001",
  "fullName": "Nguyễn Văn Nam",
  "avatarUrl": "/avatars/nguyen-van-nam.png",
  "specialty": "Nội tổng quát",
  "phone": "0987654321",
  "email": "nam.nguyen@gmail.com",
  "status": "ACTIVE",
  "workStatus": "WORKING",
  "createdAt": "2026-05-24",
  "updatedAt": "2026-05-24",
  "degree": "Bác sĩ chuyên khoa I",
  "experienceYears": 8,
  "licenseNumber": "CCHN-000001",
  "description": "Bác sĩ chuyên điều trị các bệnh nội khoa tổng quát.",
  "schedule": []
}
```

Enum trạng thái:

```ts
status: "ACTIVE" | "TEMPORARILY_INACTIVE" | "RESIGNED"
workStatus: "WORKING" | "ON_LEAVE" | "LEFT"
```

Map sang tiếng Việt:

```ts
ACTIVE = "Hoạt động"
TEMPORARILY_INACTIVE = "Tạm nghỉ"
RESIGNED = "Nghỉ việc"

WORKING = "Đang làm việc"
ON_LEAVE = "Nghỉ phép"
LEFT = "Đã nghỉ việc"
```

---

# 14. API gợi ý cho dev

Các API nên có:

```http
GET /api/admin/doctors
```

Query params:

```txt
keyword=
specialty=
status=
workStatus=
page=
limit=
sortBy=
sortOrder=
```

---

```http
GET /api/admin/doctors/:id
```

Lấy chi tiết bác sĩ.

---

```http
POST /api/admin/doctors
```

Thêm bác sĩ.

---

```http
PUT /api/admin/doctors/:id
```

Cập nhật bác sĩ.

---

```http
DELETE /api/admin/doctors/:id
```

Xóa hoặc soft delete bác sĩ.

---

```http
GET /api/admin/doctors/statistics
```

Lấy thống kê:

```json
{
  "totalDoctors": 42,
  "activeDoctors": 38,
  "temporaryLeaveDoctors": 3,
  "resignedDoctors": 1,
  "totalDoctorsGrowth": 8,
  "activeDoctorsGrowth": 7,
  "temporaryLeaveGrowth": -2,
  "resignedGrowth": -1
}
```

---

```http
GET /api/admin/doctors/export
```

Xuất Excel theo filter.

---

# 15. Quyền hạn nên có

Vì đây là màn admin, nên cần phân quyền rõ:

## Admin toàn quyền

* Xem danh sách bác sĩ
* Thêm bác sĩ
* Sửa bác sĩ
* Xóa/ngừng hoạt động bác sĩ
* Xuất Excel
* Quản lý lịch làm việc
* Quản lý tài khoản bác sĩ

## Nhân viên quản lý

* Xem danh sách
* Sửa một số thông tin cơ bản
* Không được xóa
* Có thể xuất Excel nếu được cấp quyền

## Viewer

* Chỉ được xem danh sách và chi tiết
* Không có quyền thêm/sửa/xóa

---

# 16. Mô tả ngắn gọn để đưa vào yêu cầu thiết kế

Màn hình “Quản lý bác sĩ” là một trang dashboard admin của hệ thống CarePlus, cho phép quản trị viên theo dõi, tìm kiếm, lọc, thêm, sửa, xem chi tiết, xóa và xuất danh sách bác sĩ. Giao diện gồm sidebar điều hướng bên trái, header tài khoản admin bên trên, 4 card thống kê nhanh và bảng dữ liệu bác sĩ có phân trang. Tông màu chủ đạo là xanh lá y tế, kết hợp xanh dương, cam, đỏ và tím để thể hiện các trạng thái khác nhau. Giao diện cần sạch, hiện đại, dễ nhìn, có khoảng trắng rộng, bo góc mềm, badge trạng thái rõ ràng và thao tác trực quan.

---

# 17. Prompt mô tả để đưa cho AI/dev dựng lại giao diện

Có thể dùng prompt này:

> Thiết kế giao diện web admin cho hệ thống y tế tên “CarePlus Admin”, màn hình “Quản lý bác sĩ”. Layout gồm sidebar bên trái nền trắng, logo CarePlus Admin màu xanh lá ở trên cùng, menu điều hướng gồm Dashboard, Quản lý tài khoản, Quản lý bác sĩ, Quản lý bệnh nhân, Quản lý thuốc, Quản lý dịch vụ, Quản lý thanh toán, Xem báo cáo thống kê, Phân quyền hệ thống, Sao lưu dữ liệu, và nút Đăng xuất ở cuối. Menu “Quản lý bác sĩ” đang active với nền xanh lá nhạt và icon/text màu xanh lá.
>
> Khu vực nội dung bên phải có tiêu đề “Quản lý bác sĩ”, breadcrumb “Dashboard / Quản lý bác sĩ”, góc phải có chuông thông báo với badge đỏ số 3, avatar admin, text “Admin (Quản trị viên)” và mũi tên dropdown. Bên dưới là 4 card thống kê nằm ngang: Tổng bác sĩ 42 tăng 8%, Đang hoạt động 38 tăng 7%, Tạm nghỉ 3 giảm 2%, Nghỉ việc 1 giảm 1%. Mỗi card có icon màu riêng, bo góc, viền mỏng, shadow nhẹ.
>
> Bên dưới là khung bảng quản lý bác sĩ. Trên bảng có ô tìm kiếm placeholder “Tìm kiếm bác sĩ (Tên, chuyên khoa, SĐT...)”, ba dropdown lọc gồm Chuyên khoa, Trạng thái, Tình trạng đều mặc định “Tất cả”, bên phải có nút xanh “+ Thêm bác sĩ” và nút trắng “Xuất Excel” kèm icon Excel.
>
> Bảng gồm các cột checkbox, STT, Họ và tên kèm avatar, Chuyên khoa, SĐT, Email, Trạng thái, Tình trạng, Ngày tạo, Thao tác. Badge trạng thái màu xanh cho Hoạt động/Đang làm việc, màu cam cho Tạm nghỉ/Nghỉ phép, màu đỏ cho Nghỉ việc/Đã nghỉ việc. Mỗi dòng có 3 nút thao tác: xem chi tiết, chỉnh sửa, xóa. Dưới bảng có chọn số bản ghi mỗi trang và phân trang. Phong cách thiết kế hiện đại, sạch, nền sáng, màu chủ đạo xanh lá y tế, font sans-serif, bo góc mềm, responsive cho desktop/tablet/mobile.

