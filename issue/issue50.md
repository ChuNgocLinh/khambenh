Dưới đây là mô tả chi tiết màn hình **“Sao lưu dữ liệu”** của hệ thống **CarePlus Admin**, theo kiểu đặc tả để designer/dev có thể dựng lại giao diện và suy luận chức năng.

---

# 1. Tổng quan màn hình

Đây là trang quản trị dành cho **sao lưu và khôi phục dữ liệu hệ thống** trong dashboard admin của CarePlus. Mục tiêu chính của màn hình là:

* Hiển thị tình trạng sao lưu dữ liệu hiện tại.
* Cho phép admin tạo bản sao lưu thủ công.
* Theo dõi lịch sử các bản sao lưu.
* Cấu hình các tùy chọn sao lưu tự động.
* Tải xuống, xóa hoặc chọn bản sao lưu để khôi phục.
* Cho admin biết hệ thống có đang an toàn hay không.

Giao diện có phong cách **dashboard y tế / admin hiện đại**, nền sáng, nhiều khoảng trắng, màu chủ đạo là **xanh lá CarePlus**, kết hợp xanh dương, cam và tím cho từng loại thông tin.

---

# 2. Bố cục tổng thể

Màn hình chia thành 2 vùng lớn:

## 2.1 Sidebar bên trái

Sidebar cố định bên trái, rộng khoảng **250–270px**, chiếm toàn bộ chiều cao màn hình.

Nền sidebar: trắng hoặc trắng ngà.
Có đường phân cách nhẹ với phần nội dung chính.

## 2.2 Khu vực nội dung chính

Phần nội dung nằm bên phải sidebar, có padding lớn khoảng **28–36px**.

Bên trong nội dung chính gồm:

1. Header trang.
2. Hàng 4 thẻ thống kê.
3. Khu vực chính chia làm 2 cột:

   * Cột trái lớn: sao lưu ngay + lịch sử sao lưu.
   * Cột phải nhỏ: thông tin sao lưu + tùy chọn sao lưu + khôi phục dữ liệu.

Tỷ lệ cột gần đúng:

* Cột trái: khoảng **65%**
* Cột phải: khoảng **35%**

Khoảng cách giữa các khối khoảng **16–24px**.

---

# 3. Sidebar chi tiết

## 3.1 Logo

Góc trên trái có logo:

* Icon dấu cộng màu xanh lá trong hình tròn.
* Text: **CarePlus Admin**
* “CarePlus” và “Admin” đều màu xanh lá, font đậm.

Logo nằm cách mép trái khoảng 24px, cách trên khoảng 24px.

## 3.2 Menu điều hướng

Danh sách menu nằm dọc, mỗi item gồm:

* Icon bên trái.
* Text bên phải.
* Khoảng cách giữa icon và text khoảng 14–16px.
* Chiều cao mỗi item khoảng 48–56px.
* Font màu xanh navy đậm.

Các mục trong sidebar:

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

Mục đang được chọn là **“Sao lưu dữ liệu”**.

## 3.3 Trạng thái active menu

Item active có:

* Nền xanh lá rất nhạt.
* Text màu xanh lá.
* Icon màu xanh lá.
* Bo góc khoảng 8–10px.
* Có cảm giác đang được highlight nhưng không quá đậm.

Item active nằm gần cuối sidebar.

## 3.4 Nút Đăng xuất

Ở đáy sidebar có nút **Đăng xuất**.

Đặc điểm:

* Nền đỏ rất nhạt.
* Icon logout màu đỏ.
* Text đỏ.
* Bo góc nhẹ.
* Chiều rộng gần bằng sidebar, chừa margin hai bên.
* Vị trí cố định gần đáy màn hình.

Chức năng suy đoán:

* Khi click, hiện modal xác nhận:

  * “Bạn có chắc muốn đăng xuất?”
  * Nút Hủy
  * Nút Đăng xuất
* Sau khi xác nhận thì clear token/session và chuyển về trang đăng nhập.

---

# 4. Header trang

Phần header nằm phía trên nội dung chính.

## 4.1 Tiêu đề

Text lớn: **Sao lưu dữ liệu**

* Font size khoảng 28–32px.
* Font weight 700.
* Màu xanh navy rất đậm.
* Nằm góc trên trái phần content.

## 4.2 Breadcrumb

Dưới tiêu đề có breadcrumb:

**Dashboard / Sao lưu dữ liệu**

Trong đó:

* “Dashboard” màu xanh xám.
* Dấu “/” màu xám nhạt.
* “Sao lưu dữ liệu” màu xanh xám hoặc navy nhạt.

Chức năng:

* Click “Dashboard” có thể quay về trang dashboard chính.
* Breadcrumb giúp admin biết vị trí hiện tại.

## 4.3 Khu vực user góc phải

Góc trên phải có:

1. Icon chuông thông báo.
2. Badge đỏ nhỏ hiển thị số **3**.
3. Avatar người dùng dạng minh họa.
4. Text: **Admin (Quản trị viên)**
5. Mũi tên dropdown.

Chức năng suy đoán:

### Chuông thông báo

Click mở dropdown danh sách thông báo, ví dụ:

* “Sao lưu dữ liệu hoàn tất”
* “Bản sao lưu lúc 02:00 đã tạo thành công”
* “Dung lượng sao lưu tăng 0.2GB”
* “Cảnh báo: bản sao lưu cũ sắp hết hạn”

Badge đỏ thể hiện số thông báo chưa đọc.

### Avatar / Admin dropdown

Click mở menu:

* Hồ sơ cá nhân
* Đổi mật khẩu
* Cài đặt tài khoản
* Đăng xuất

---

# 5. Hàng thẻ thống kê phía trên

Ngay dưới header là 4 card thống kê nằm ngang.

Mỗi card có:

* Nền trắng.
* Border xám rất nhạt.
* Bo góc khoảng 12–16px.
* Padding trong khoảng 20–24px.
* Icon lớn bên trái nằm trong ô vuông màu gradient.
* Text mô tả nhỏ phía trên.
* Số liệu chính nổi bật.
* Text phụ bên dưới.

Chiều cao card khoảng 100–120px.

---

## 5.1 Card 1 — Tổng dung lượng dữ liệu

Nội dung:

* Icon: database / ổ dữ liệu.
* Icon nền xanh dương gradient.
* Label: **Tổng dung lượng dữ liệu**
* Giá trị chính: **24.8 GB**
* Text phụ: **Dung lượng hiện tại**

Ý nghĩa:

* Tổng dung lượng dữ liệu cần được sao lưu tại thời điểm hiện tại.
* Có thể bao gồm:

  * Cơ sở dữ liệu
  * File đính kèm
  * Hình ảnh
  * Tài liệu
  * Log hệ thống tùy cấu hình

Chức năng suy đoán:

* Dữ liệu lấy từ API thống kê hệ thống.
* Có thể cập nhật realtime hoặc khi reload trang.
* Nên có tooltip giải thích “Tính trên toàn bộ dữ liệu được bật sao lưu”.

---

## 5.2 Card 2 — Bản sao lưu gần nhất

Nội dung:

* Icon: cloud upload / cloud backup.
* Icon nền xanh lá gradient.
* Label: **Bản sao lưu gần nhất**
* Giá trị chính: **24/05/2026 02:00**
* Text phụ: **2 giờ trước**

Ý nghĩa:

* Thời điểm bản sao lưu thành công gần nhất.
* Text “2 giờ trước” là thời gian tương đối.

Chức năng suy đoán:

* Nếu chưa từng sao lưu, hiển thị:

  * “Chưa có”
  * “Chưa tạo bản sao lưu nào”
* Nếu bản sao lưu gần nhất thất bại, card có thể chuyển sang màu đỏ/cam.

---

## 5.3 Card 3 — Lịch sao lưu tự động

Nội dung:

* Icon: đồng hồ.
* Icon nền cam gradient.
* Label: **Lịch sao lưu tự động**
* Giá trị chính: **02:00 AM**
* Text phụ: **Hàng ngày**

Ý nghĩa:

* Cho biết lịch sao lưu tự động đang được thiết lập.
* Hiện tại là sao lưu mỗi ngày lúc 02:00 sáng.

Chức năng suy đoán:

* Có thể click vào card hoặc nút “Tùy chọn nâng cao” để chỉnh lịch:

  * Hàng ngày
  * Hàng tuần
  * Hàng tháng
  * Chọn giờ chạy
  * Chọn ngày trong tuần
  * Chọn múi giờ

---

## 5.4 Card 4 — Trạng thái hệ thống

Nội dung:

* Icon: khiên bảo vệ.
* Icon nền tím gradient.
* Label: **Trạng thái hệ thống**
* Giá trị chính: **An toàn**
* Text phụ: **Dữ liệu được bảo vệ**

Ý nghĩa:

* Hệ thống đang có bản sao lưu hợp lệ.
* Không có lỗi sao lưu gần đây.
* Dữ liệu đang được bảo vệ đúng cấu hình.

Trạng thái có thể có:

* **An toàn**: sao lưu thành công, bản gần nhất còn mới.
* **Cảnh báo**: bản sao lưu gần nhất quá cũ hoặc có lỗi nhỏ.
* **Nguy hiểm**: sao lưu thất bại nhiều lần hoặc không có bản backup.
* **Đang sao lưu**: hệ thống đang chạy backup.
* **Đang khôi phục**: hệ thống đang restore dữ liệu.

---

# 6. Khối “Sao lưu dữ liệu ngay”

Đây là card lớn nằm ở cột trái, phía trên bảng lịch sử.

## 6.1 Header khối

Tiêu đề: **Sao lưu dữ liệu ngay**

* Font đậm.
* Màu xanh navy.

Mô tả bên dưới:

**Tạo bản sao lưu mới cho toàn bộ hệ thống. Quá trình sao lưu có thể mất vài phút tùy theo dung lượng dữ liệu.**

Ý nghĩa:

* Giải thích cho admin rằng thao tác backup không phải tức thời.
* Cần chuẩn bị trạng thái loading/progress.

---

## 6.2 Box trạng thái sẵn sàng

Bên trong card có một box màu xanh lá rất nhạt.

Nội dung:

* Icon cloud upload màu xanh lá.
* Text chính: **Hệ thống sẵn sàng để sao lưu**
* Text phụ: **Tất cả dữ liệu sẽ được sao lưu an toàn.**

Box này thể hiện hệ thống đủ điều kiện backup.

Các trạng thái khác có thể cần:

### Khi đang sao lưu

* Text chính: “Đang sao lưu dữ liệu”
* Text phụ: “Vui lòng không tắt hệ thống trong quá trình này.”
* Có progress bar.
* Có phần trăm hoàn thành.
* Nút “Sao lưu ngay” bị disable.

### Khi lỗi

* Box chuyển màu đỏ nhạt.
* Text: “Không thể sao lưu”
* Hiển thị lý do:

  * Không đủ dung lượng
  * Mất kết nối máy chủ
  * Lỗi quyền truy cập thư mục backup
  * Database đang bận

### Khi cảnh báo

* Box màu vàng/cam nhạt.
* Text: “Dung lượng sao lưu lớn”
* Gợi ý bật nén dữ liệu hoặc xóa bản cũ.

---

## 6.3 Nút “Sao lưu ngay”

Nút nằm dưới box trạng thái, bên trái.

Đặc điểm:

* Nền xanh lá.
* Text trắng.
* Icon nhỏ bên trái.
* Bo góc khoảng 8px.
* Padding ngang rộng.
* Label: **Sao lưu ngay**

Chức năng:

Khi admin bấm:

1. Hiện hộp xác nhận:

   * “Bạn có chắc muốn tạo bản sao lưu mới?”
   * “Quá trình này có thể mất vài phút.”
2. Nếu xác nhận:

   * Gọi API tạo backup.
   * Chuyển trạng thái sang “Đang sao lưu”.
   * Disable nút.
   * Hiển thị tiến trình.
3. Khi xong:

   * Hiện toast thành công.
   * Thêm bản ghi mới vào bảng lịch sử.
   * Cập nhật card “Bản sao lưu gần nhất”.
   * Cập nhật tổng số bản sao lưu.
4. Nếu lỗi:

   * Hiện toast lỗi.
   * Ghi lại log lỗi.
   * Có thể thêm bản ghi trạng thái “Thất bại” vào lịch sử.

Nên có debounce hoặc chống spam click để tránh tạo nhiều job backup cùng lúc.

---

## 6.4 Nút “Tùy chọn nâng cao”

Nằm cùng hàng với nút “Sao lưu ngay” nhưng ở bên phải card.

Đặc điểm:

* Nền trắng.
* Border xám nhạt.
* Icon bánh răng.
* Text: **Tùy chọn nâng cao**

Chức năng suy đoán:

Click mở modal hoặc drawer cấu hình nâng cao:

* Chọn loại dữ liệu cần backup:

  * Cơ sở dữ liệu
  * File upload
  * Hình ảnh
  * Log
  * Cấu hình hệ thống
* Bật/tắt nén dữ liệu.
* Mã hóa bản sao lưu.
* Chọn nơi lưu:

  * Máy chủ nội bộ
  * Cloud storage
  * Google Drive / S3 / FTP
* Chọn giữ lại bao nhiêu ngày.
* Chọn giới hạn số bản backup.
* Chọn lịch tự động.
* Bật gửi email thông báo.
* Kiểm tra dung lượng còn trống.

---

# 7. Bảng “Lịch sử sao lưu”

Bảng nằm ở cột trái, bên dưới khối “Sao lưu dữ liệu ngay”.

## 7.1 Header bảng

Tiêu đề: **Lịch sử sao lưu**

Bên phải có link/nút nhỏ: **Xem tất cả**

Chức năng:

* “Xem tất cả” có thể mở trang danh sách backup đầy đủ.
* Hoặc mở modal/table có filter, search, export.

---

## 7.2 Cấu trúc bảng

Bảng có các cột:

1. **Thời gian**
2. **Loại sao lưu**
3. **Dung lượng**
4. **Người tạo**
5. **Trạng thái**
6. **Thao tác**

Các dòng hiển thị:

| Thời gian        | Loại sao lưu | Dung lượng | Người tạo | Trạng thái |
| ---------------- | ------------ | ---------: | --------- | ---------- |
| 24/05/2026 02:00 | Tự động      |    24.8 GB | Hệ thống  | Thành công |
| 23/05/2026 02:00 | Tự động      |    24.6 GB | Hệ thống  | Thành công |
| 22/05/2026 02:00 | Tự động      |    24.1 GB | Hệ thống  | Thành công |
| 21/05/2026 02:00 | Tự động      |    23.7 GB | Hệ thống  | Thành công |
| 20/05/2026 02:00 | Tự động      |    23.5 GB | Hệ thống  | Thành công |
| 19/05/2026 02:00 | Tự động      |    23.2 GB | Hệ thống  | Thành công |
| 18/05/2026 02:00 | Tự động      |    22.9 GB | Hệ thống  | Thành công |

## 7.3 Style bảng

* Header bảng nền trắng hoặc xám cực nhạt.
* Text header đậm.
* Row có border-bottom rất nhẹ.
* Font size khoảng 13–14px.
* Chiều cao mỗi row khoảng 44–52px.
* Dữ liệu căn trái, riêng dung lượng có thể căn trái hoặc phải tùy design.

## 7.4 Badge trạng thái

Trạng thái “Thành công” hiển thị dạng pill:

* Nền xanh lá nhạt.
* Text xanh lá.
* Bo tròn mạnh.
* Font nhỏ, đậm vừa.

Các trạng thái cần có thêm:

### Thành công

* Màu xanh lá.
* Có thể cho phép tải xuống/khôi phục.

### Đang xử lý

* Màu xanh dương hoặc vàng.
* Icon loading.
* Không cho xóa.
* Không cho tải xuống cho đến khi hoàn tất.

### Thất bại

* Màu đỏ.
* Có nút xem lỗi.
* Không cho khôi phục.
* Có thể cho chạy lại.

### Đã hết hạn

* Màu xám.
* File backup có thể đã bị xóa theo chính sách retention.

---

## 7.5 Cột thao tác

Mỗi dòng có 2 icon:

1. Icon tải xuống màu xanh dương.
2. Icon thùng rác màu đỏ.

### Nút tải xuống

Chức năng:

* Tải file backup về máy.
* Có thể cần xác nhận hoặc yêu cầu quyền admin cao.
* File tải xuống có thể là `.zip`, `.sql`, `.tar.gz`, hoặc định dạng nội bộ.
* Nên hiển thị loading riêng trên icon khi đang tải.

### Nút xóa

Chức năng:

* Xóa bản sao lưu.
* Nên mở modal xác nhận:

  * “Bạn có chắc muốn xóa bản sao lưu ngày 24/05/2026 02:00?”
  * “Thao tác này không thể hoàn tác.”
* Không nên cho xóa bản backup duy nhất hoặc bản backup gần nhất nếu chưa có bản thay thế, trừ khi admin xác nhận quyền cao.

Có thể bổ sung thêm thao tác:

* Khôi phục bản này.
* Xem chi tiết.
* Kiểm tra tính toàn vẹn.
* Sao chép đường dẫn lưu trữ.
* Tải log backup.

---

## 7.6 Phân trang bảng

Dưới bảng có:

Bên trái:

* Text: **Hiển thị**
* Dropdown: **10**
* Text: **bản ghi**

Bên phải:

* Nút previous.
* Trang **1** đang active màu xanh lá.
* Trang 2.
* Trang 3.
* Dấu …
* Trang 8.
* Nút next.

Chức năng:

* Admin chọn số dòng hiển thị: 10, 20, 50, 100.
* Click số trang để chuyển trang.
* Previous/Next disable khi ở trang đầu/cuối.
* Khi thay đổi số dòng hoặc trang, gọi API lấy dữ liệu mới.

---

# 8. Cột phải — “Thông tin sao lưu”

Khối đầu tiên bên phải là card **Thông tin sao lưu**.

## 8.1 Nội dung hiển thị

Card có tiêu đề: **Thông tin sao lưu**

Bên dưới là danh sách key-value, mỗi dòng có icon nhỏ bên trái.

Các dòng:

1. **Vị trí lưu trữ:** Máy chủ nội bộ
2. **Đường dẫn:** `/backup/careplus/`
3. **Tổng số bản sao lưu:** 28 bản
4. **Bản sao lưu gần nhất:** 24/05/2026 02:00
5. **Bản sao lưu tiếp theo:** 25/05/2026 02:00
6. **Phương thức:** Tự động hằng ngày
7. **Giữ lại bản sao lưu:** 30 ngày

## 8.2 Ý nghĩa chức năng

Card này đóng vai trò tóm tắt cấu hình backup hiện tại.

Cần có API trả về:

* Nơi lưu trữ.
* Đường dẫn thư mục.
* Tổng số backup.
* Backup gần nhất.
* Backup tiếp theo.
* Chu kỳ backup.
* Chính sách lưu giữ.

## 8.3 Các trường hợp cần xử lý

Nếu chưa cấu hình backup:

* Vị trí lưu trữ: “Chưa thiết lập”
* Đường dẫn: “—”
* Bản sao lưu tiếp theo: “Chưa có lịch”
* Trạng thái hệ thống có thể là “Cảnh báo”

Nếu không lấy được thông tin:

* Hiển thị skeleton loading.
* Hoặc text lỗi: “Không thể tải thông tin sao lưu”.

---

# 9. Cột phải — “Tùy chọn sao lưu”

Card thứ hai bên phải là **Tùy chọn sao lưu**.

Đây là khu vực cấu hình nhanh bằng toggle.

## 9.1 Các option đang bật/tắt

Có 5 tùy chọn:

### 1. Sao lưu tự động

Text phụ: **Tự động sao lưu dữ liệu theo lịch**

Trạng thái: bật.

Ý nghĩa:

* Khi bật, hệ thống tự chạy backup theo lịch.
* Khi tắt, chỉ có backup thủ công.

Khi tắt nên hiện cảnh báo:

* “Tắt sao lưu tự động có thể làm tăng rủi ro mất dữ liệu.”

---

### 2. Sao lưu cơ sở dữ liệu

Text phụ: **Sao lưu riêng cơ sở dữ liệu**

Trạng thái: bật.

Ý nghĩa:

* Backup database chính:

  * users
  * doctors
  * patients
  * appointments
  * medicines
  * payments
  * permissions
  * services

Đây là tùy chọn quan trọng, có thể không nên cho tắt nếu không có quyền cao.

---

### 3. Sao lưu tệp đính kèm

Text phụ: **Bao gồm tệp đính kèm và hình ảnh**

Trạng thái: bật.

Ý nghĩa:

* Backup các file upload:

  * ảnh đại diện
  * hồ sơ bệnh án
  * file xét nghiệm
  * hóa đơn
  * đơn thuốc dạng file
  * ảnh y tế

Vì đây là hệ thống y tế, dữ liệu file đính kèm có thể quan trọng.

---

### 4. Nén dữ liệu

Text phụ: **Nén dữ liệu để tiết kiệm dung lượng**

Trạng thái: bật.

Ý nghĩa:

* Backup được nén thành file nhỏ hơn.
* Có thể làm thời gian backup lâu hơn.
* Có thể dùng `.zip`, `.gzip`, `.tar.gz`.

---

### 5. Gửi email thông báo

Text phụ: **Gửi thông báo sau khi sao lưu hoàn tất**

Trạng thái: tắt.

Ý nghĩa:

* Khi bật, hệ thống gửi email sau mỗi lần backup.
* Email có thể gửi khi:

  * Backup thành công.
  * Backup thất bại.
  * Dung lượng vượt ngưỡng.
  * Không đủ dung lượng lưu trữ.

Khi bật nên mở thêm cấu hình:

* Email người nhận.
* Chỉ gửi khi lỗi hay gửi mọi lần.
* Gửi báo cáo định kỳ.

---

## 9.2 Style toggle

Toggle bật:

* Nền xanh lá.
* Nút tròn trắng nằm bên phải.

Toggle tắt:

* Nền xám nhạt.
* Nút tròn trắng nằm bên trái.

Khi click:

* Cập nhật ngay hoặc mở xác nhận với tùy chọn quan trọng.
* Có trạng thái loading nhỏ.
* Nếu lỗi thì rollback về trạng thái cũ và hiển thị toast.

---

# 10. Cột phải — “Khôi phục dữ liệu”

Card cuối bên phải là **Khôi phục dữ liệu**.

## 10.1 Nội dung

Tiêu đề: **Khôi phục dữ liệu**

Mô tả: **Khôi phục dữ liệu từ bản sao lưu đã chọn.**

Có một nút lớn full-width:

**Chọn bản sao lưu để khôi phục**

Icon bên trái giống refresh/restore.

## 10.2 Chức năng suy đoán

Khi click nút, hệ thống nên mở modal hoặc màn hình chọn bản backup.

Flow hợp lý:

1. Admin click “Chọn bản sao lưu để khôi phục”.
2. Mở modal danh sách backup.
3. Admin chọn một bản sao lưu.
4. Hệ thống hiển thị chi tiết:

   * Thời gian tạo.
   * Dung lượng.
   * Loại sao lưu.
   * Người tạo.
   * Dữ liệu bao gồm.
   * Checksum/tình trạng file.
5. Admin bấm “Khôi phục”.
6. Hiện cảnh báo nghiêm trọng:

   * “Khôi phục dữ liệu sẽ ghi đè dữ liệu hiện tại.”
   * “Hệ thống có thể tạm thời không khả dụng.”
   * “Bạn nên tạo bản sao lưu hiện tại trước khi khôi phục.”
7. Có thể yêu cầu nhập:

   * Mật khẩu admin.
   * Mã OTP.
   * Text xác nhận: `RESTORE`
8. Tiến hành restore.
9. Hiển thị tiến trình.
10. Ghi log audit.

## 10.3 Trạng thái cần có

### Chưa chọn bản backup

Nút: “Chọn bản sao lưu để khôi phục”

### Đã chọn bản backup

Hiển thị:

* “Đã chọn: Backup 24/05/2026 02:00”
* Nút “Khôi phục ngay”
* Nút “Đổi bản sao lưu”

### Đang khôi phục

* Disable toàn bộ thao tác quan trọng.
* Hiển thị progress bar.
* Text: “Đang khôi phục dữ liệu…”

### Khôi phục thành công

* Toast thành công.
* Có thể yêu cầu đăng nhập lại.
* Reload dữ liệu.

### Khôi phục thất bại

* Hiển thị lỗi.
* Có tùy chọn tải log.
* Có thể rollback nếu hệ thống hỗ trợ.

---

# 11. Màu sắc đề xuất

Giao diện dùng bảng màu rất nhẹ, chuyên nghiệp.

## Màu chính

* Xanh lá CarePlus: `#16A34A` hoặc `#12A150`
* Xanh lá nhạt nền active: `#EAF8EF`
* Xanh navy text chính: `#11183C` hoặc `#121A3D`
* Text phụ: `#667085`
* Border: `#E5E7EB`
* Nền trang: `#F8FAFC`
* Nền card: `#FFFFFF`

## Màu trạng thái

* Thành công:

  * Text: `#16A34A`
  * Background: `#DCFCE7`

* Lỗi:

  * Text: `#DC2626`
  * Background: `#FEE2E2`

* Cảnh báo:

  * Text: `#F97316`
  * Background: `#FFEDD5`

* Thông tin:

  * Text: `#2563EB`
  * Background: `#DBEAFE`

## Màu icon card

* Database: xanh dương gradient.
* Cloud backup: xanh lá gradient.
* Clock: cam gradient.
* Shield: tím gradient.

---

# 12. Typography

Font nên dùng loại sans-serif hiện đại:

* Inter
* Roboto
* Manrope
* SF Pro Display

Cỡ chữ gợi ý:

* Tiêu đề trang: 28–32px, weight 700.
* Tiêu đề card: 18px, weight 600–700.
* Label thống kê: 14px, weight 600.
* Giá trị chính card: 22–26px, weight 700.
* Text phụ: 13–14px.
* Table header: 13px, weight 600.
* Table content: 13–14px.
* Button: 14px, weight 600.

---

# 13. Khoảng cách và bo góc

## Layout

* Sidebar width: 260px.
* Content padding: 32px.
* Gap giữa các card: 18–24px.
* Gap giữa cột trái/phải: 16–20px.

## Card

* Border radius: 12–16px.
* Border: 1px solid `#E5E7EB`.
* Padding: 20–24px.
* Box shadow rất nhẹ hoặc không có.

## Button

* Height: 40–44px.
* Border radius: 8px.
* Padding ngang: 16–20px.

---

# 14. Các chức năng backend cần có

Để màn hình này hoạt động đầy đủ, backend nên có các nhóm API sau.

## 14.1 API lấy tổng quan backup

Ví dụ:

`GET /admin/backups/summary`

Trả về:

```json
{
  "totalDataSize": "24.8 GB",
  "lastBackupAt": "2026-05-24T02:00:00",
  "nextBackupAt": "2026-05-25T02:00:00",
  "scheduleTime": "02:00 AM",
  "scheduleFrequency": "daily",
  "systemStatus": "safe",
  "storageLocation": "Máy chủ nội bộ",
  "storagePath": "/backup/careplus/",
  "totalBackups": 28,
  "retentionDays": 30
}
```

## 14.2 API lấy danh sách backup

`GET /admin/backups?page=1&limit=10`

Trả về:

```json
{
  "items": [
    {
      "id": "backup_001",
      "createdAt": "2026-05-24T02:00:00",
      "type": "automatic",
      "size": "24.8 GB",
      "createdBy": "system",
      "status": "success",
      "downloadUrl": "/admin/backups/backup_001/download"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 78,
    "totalPages": 8
  }
}
```

## 14.3 API tạo backup thủ công

`POST /admin/backups`

Body:

```json
{
  "includeDatabase": true,
  "includeAttachments": true,
  "compress": true,
  "encrypt": true
}
```

Trả về job:

```json
{
  "jobId": "backup_job_123",
  "status": "processing"
}
```

## 14.4 API kiểm tra tiến trình backup

`GET /admin/backups/jobs/backup_job_123`

Trả về:

```json
{
  "jobId": "backup_job_123",
  "status": "processing",
  "progress": 65,
  "message": "Đang nén dữ liệu..."
}
```

## 14.5 API tải backup

`GET /admin/backups/{id}/download`

Chức năng:

* Trả file backup.
* Cần kiểm tra quyền.
* Ghi log người tải xuống.

## 14.6 API xóa backup

`DELETE /admin/backups/{id}`

Chức năng:

* Xóa file backup.
* Xóa metadata hoặc đánh dấu deleted.
* Ghi audit log.

## 14.7 API cập nhật cấu hình backup

`PATCH /admin/backups/settings`

Body:

```json
{
  "autoBackup": true,
  "backupDatabase": true,
  "backupAttachments": true,
  "compressData": true,
  "emailNotification": false,
  "retentionDays": 30,
  "scheduleTime": "02:00",
  "scheduleFrequency": "daily"
}
```

## 14.8 API khôi phục dữ liệu

`POST /admin/backups/{id}/restore`

Body:

```json
{
  "confirmText": "RESTORE",
  "createBackupBeforeRestore": true
}
```

Trả về:

```json
{
  "jobId": "restore_job_456",
  "status": "processing"
}
```

---

# 15. Phân quyền cần có

Vì đây là chức năng nhạy cảm, nên không phải admin nào cũng nên có toàn quyền.

Nên chia quyền:

## Quyền xem

* Xem danh sách backup.
* Xem cấu hình backup.
* Xem trạng thái hệ thống.

## Quyền tạo backup

* Cho phép bấm “Sao lưu ngay”.

## Quyền tải backup

* Cho phép download file backup.

## Quyền xóa backup

* Cho phép xóa bản backup cũ.

## Quyền cấu hình backup

* Bật/tắt backup tự động.
* Đổi lịch backup.
* Đổi retention.
* Đổi nơi lưu trữ.

## Quyền khôi phục dữ liệu

* Quyền cao nhất.
* Nên yêu cầu xác thực lại.

---

# 16. Các trạng thái giao diện cần thiết

## 16.1 Loading ban đầu

Khi mới vào trang:

* Card thống kê hiển thị skeleton.
* Bảng lịch sử hiển thị skeleton rows.
* Toggle bị disable tạm thời.
* Không hiển thị dữ liệu cũ sai lệch.

## 16.2 Empty state

Nếu chưa có backup:

* Bảng hiển thị:

  * “Chưa có bản sao lưu nào”
  * Nút “Tạo bản sao lưu đầu tiên”
* Card “Bản sao lưu gần nhất”: “Chưa có”
* Trạng thái hệ thống: “Cảnh báo”

## 16.3 Error state

Nếu API lỗi:

* Toast: “Không thể tải dữ liệu sao lưu”
* Card có nút “Thử lại”
* Không crash toàn bộ trang.

## 16.4 Processing state

Khi backup/restore đang chạy:

* Hiển thị progress.
* Disable các thao tác nguy hiểm:

  * Xóa backup
  * Restore backup khác
  * Thay đổi cấu hình backup
* Có thể cho admin rời trang nhưng job vẫn chạy nền.

## 16.5 Success state

Sau khi backup thành công:

* Toast xanh: “Sao lưu dữ liệu thành công”
* Bảng thêm dòng mới.
* Card cập nhật thời gian.
* Tổng số bản sao lưu tăng thêm 1.

## 16.6 Failed state

Sau khi backup thất bại:

* Toast đỏ.
* Bảng có dòng trạng thái “Thất bại”.
* Có nút “Xem chi tiết lỗi”.
* Có nút “Thử lại”.

---

# 17. Những chi tiết UX nên bổ sung

## Xác nhận trước thao tác nguy hiểm

Các thao tác cần confirm:

* Xóa backup.
* Restore backup.
* Tắt sao lưu tự động.
* Tắt sao lưu cơ sở dữ liệu.
* Đổi nơi lưu trữ.
* Giảm thời gian giữ backup.

## Toast thông báo

Nên có toast góc phải trên:

* Thành công: xanh.
* Cảnh báo: cam.
* Lỗi: đỏ.
* Đang xử lý: xanh dương.

## Audit log

Mỗi thao tác quan trọng cần lưu:

* Ai thực hiện.
* Thời gian.
* IP hoặc thiết bị.
* Hành động.
* Kết quả.
* Backup ID liên quan.

Ví dụ:

* Admin A tạo backup thủ công.
* Admin B tải backup ngày 24/05.
* Admin C xóa backup ngày 18/05.
* Admin A khôi phục dữ liệu từ backup ngày 23/05.

## Tooltip

Nên có tooltip cho:

* Tổng dung lượng dữ liệu.
* Retention 30 ngày.
* Nén dữ liệu.
* Sao lưu tệp đính kèm.
* Gửi email thông báo.
* Trạng thái hệ thống.

---

# 18. Responsive

## Desktop lớn

Giống ảnh hiện tại:

* Sidebar trái cố định.
* 4 card thống kê nằm ngang.
* Nội dung chia 2 cột.

## Laptop nhỏ

* 4 card có thể thành 2 hàng, mỗi hàng 2 card.
* Cột phải có thể vẫn nằm bên phải nếu đủ rộng.

## Tablet

* Sidebar thu gọn thành icon-only hoặc drawer.
* Cards xếp 2 cột.
* Cột phải xuống dưới cột trái.

## Mobile

* Sidebar thành menu hamburger.
* Cards xếp 1 cột.
* Bảng lịch sử cần scroll ngang.
* Các thao tác trong bảng có thể đưa vào menu ba chấm.
* Nút “Sao lưu ngay” full-width.

---

# 19. Mô tả từng khu vực theo thứ tự dựng UI

Có thể dựng giao diện theo thứ tự này:

1. Tạo layout chính gồm sidebar và main content.
2. Sidebar có logo, menu, active item, logout.
3. Main content có header: title, breadcrumb, notification, user dropdown.
4. Dựng grid 4 card thống kê.
5. Dựng card “Sao lưu dữ liệu ngay”.
6. Dựng bảng “Lịch sử sao lưu”.
7. Dựng card “Thông tin sao lưu”.
8. Dựng card “Tùy chọn sao lưu”.
9. Dựng card “Khôi phục dữ liệu”.
10. Thêm modal:

    * Xác nhận backup.
    * Tùy chọn nâng cao.
    * Xác nhận xóa.
    * Chọn backup để restore.
    * Xác nhận restore.
11. Thêm toast.
12. Thêm loading/skeleton/error/empty states.
13. Kết nối API.
14. Thêm phân quyền.

---

# 20. Tóm tắt chức năng chính cần có

Màn hình này nên có các chức năng sau:

| Nhóm chức năng    | Mô tả                                                             |
| ----------------- | ----------------------------------------------------------------- |
| Xem tổng quan     | Xem dung lượng, backup gần nhất, lịch backup, trạng thái hệ thống |
| Backup thủ công   | Admin bấm “Sao lưu ngay” để tạo bản backup mới                    |
| Backup tự động    | Hệ thống tự backup theo lịch 02:00 AM hằng ngày                   |
| Lịch sử backup    | Xem danh sách các bản sao lưu theo ngày                           |
| Download backup   | Tải bản sao lưu về máy                                            |
| Xóa backup        | Xóa bản sao lưu không cần nữa                                     |
| Cấu hình backup   | Bật/tắt tự động, database, file đính kèm, nén, email              |
| Khôi phục dữ liệu | Chọn một bản backup để restore hệ thống                           |
| Phân trang        | Xem nhiều bản ghi backup                                          |
| Thông báo         | Badge, toast, email notification                                  |
| Bảo mật           | Phân quyền, xác nhận, audit log                                   |

---

# 21. Nhận xét thiết kế

Giao diện này khá rõ ràng và hợp lý cho admin vì:

* Thông tin quan trọng được đưa lên đầu.
* Nút thao tác chính “Sao lưu ngay” nổi bật bằng màu xanh.
* Lịch sử backup dễ theo dõi.
* Cột phải gom các thông tin cấu hình và hành động phụ.
* Màu sắc phân cấp tốt:

  * Xanh lá cho an toàn/thành công.
  * Cam cho lịch/thời gian.
  * Tím cho bảo mật.
  * Đỏ cho xóa/đăng xuất/cảnh báo.

Điểm nên bổ sung khi triển khai thật:

* Progress bar khi backup/restore.
* Modal xác nhận restore thật kỹ.
* Audit log.
* Phân quyền riêng cho restore và delete.
* Cảnh báo khi bản backup gần nhất quá cũ.
* Kiểm tra dung lượng còn trống.
* Cơ chế mã hóa backup.
* Thông báo khi backup tự động thất bại.
