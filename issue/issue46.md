Dưới đây là mô tả chi tiết giao diện **CarePlus Admin – Quản lý dịch vụ** để một người khác có thể thiết kế hoặc code lại gần giống, đồng thời suy đoán các chức năng cần có.

---

# 1. Tổng quan màn hình

Đây là màn hình quản trị trong hệ thống phòng khám/bệnh viện **CarePlus Admin**, dùng để **quản lý danh sách dịch vụ y tế** như khám tổng quát, xét nghiệm, chụp X-quang, siêu âm, vật lý trị liệu…

Tên trang hiện tại là:

**Quản lý dịch vụ**

Breadcrumb bên dưới:

**Dashboard / Quản lý dịch vụ**

Giao diện có phong cách hiện đại, nền sáng, màu chủ đạo xanh lá và xanh dương. Layout gồm 2 phần chính:

1. **Sidebar bên trái**: menu điều hướng toàn hệ thống.
2. **Khu vực nội dung bên phải**: dashboard thống kê, bộ lọc, bảng danh sách dịch vụ, phân trang.

---

# 2. Sidebar bên trái

Sidebar nằm cố định bên trái, chiếm khoảng **250px – 270px** chiều ngang. Nền trắng, có viền hoặc bóng đổ rất nhẹ tách khỏi nội dung chính.

## 2.1 Logo

Ở góc trên sidebar có logo:

* Icon dấu cộng màu xanh lá trong hình tròn.
* Text: **CarePlus Admin**
* Màu chữ: xanh lá.
* Font đậm, kích thước khoảng 22–24px.
* Dòng logo căn ngang giữa icon và chữ.

## 2.2 Menu điều hướng

Danh sách menu nằm dọc, mỗi mục gồm icon bên trái và text bên phải.

Các mục gồm:

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

Mục đang được chọn là:

**Quản lý dịch vụ**

Mục này có:

* Nền xanh lá nhạt.
* Text màu xanh lá đậm.
* Icon màu xanh lá.
* Bo góc khoảng 8–12px.
* Có cảm giác nổi bật hơn các mục còn lại.

Các mục còn lại:

* Text màu xanh đen.
* Icon màu xanh đen/xám đậm.
* Khi hover nên đổi nền sang xanh nhạt hoặc xám nhạt.

## 2.3 Nút đăng xuất

Ở cuối sidebar có nút:

**Đăng xuất**

Đặc điểm:

* Nền đỏ rất nhạt.
* Text màu đỏ.
* Icon logout màu đỏ.
* Bo góc khoảng 8–10px.
* Căn gần đáy sidebar.
* Khi hover có thể đậm nền hơn.

Chức năng suy đoán:

* Khi bấm mở modal xác nhận: “Bạn có chắc muốn đăng xuất không?”
* Nếu xác nhận thì xóa token/session và chuyển về trang đăng nhập.

---

# 3. Header khu vực nội dung

Khu vực nội dung nằm bên phải sidebar, nền tổng thể trắng/xám rất nhạt.

Phần trên cùng có:

## 3.1 Tiêu đề trang

Bên trái:

**Quản lý dịch vụ**

* Font lớn, khoảng 26–32px.
* Màu xanh đen.
* Đậm.

Bên dưới là breadcrumb:

**Dashboard / Quản lý dịch vụ**

* Font nhỏ hơn, khoảng 14–16px.
* Màu xanh xám.
* Chữ “Dashboard” có thể là link.

## 3.2 Khu vực tài khoản admin

Góc phải trên có:

1. Icon chuông thông báo.
2. Badge đỏ hiển thị số **3**.
3. Avatar admin.
4. Text: **Admin (Quản trị viên)**
5. Icon mũi tên xổ xuống.

Chức năng suy đoán:

* Bấm icon chuông mở dropdown danh sách thông báo.
* Badge hiển thị số thông báo chưa đọc.
* Bấm avatar hoặc tên admin mở menu:

  * Thông tin cá nhân.
  * Đổi mật khẩu.
  * Cài đặt tài khoản.
  * Đăng xuất.

---

# 4. Khu vực thẻ thống kê

Ngay bên dưới tiêu đề là 4 card thống kê nằm ngang.

Mỗi card có:

* Nền trắng.
* Bo góc lớn khoảng 12–16px.
* Viền xám nhạt.
* Bóng đổ rất nhẹ.
* Padding rộng.
* Icon màu nổi bật bên trái.
* Tiêu đề, số liệu lớn, phần trăm thay đổi so với tháng trước.

## 4.1 Card 1 — Tổng dịch vụ

Nội dung:

* Icon dạng lưới 4 ô, nền xanh dương.
* Tiêu đề: **Tổng dịch vụ**
* Số: **132**
* Dòng phụ: mũi tên xanh đi lên, **12% so với tháng trước**

Ý nghĩa:

* Tổng số dịch vụ đang có trong hệ thống, bao gồm đang hoạt động, tạm ngưng và ngừng cung cấp.

## 4.2 Card 2 — Dịch vụ đang hoạt động

Nội dung:

* Icon tim/nhịp tim, nền xanh lá.
* Tiêu đề: **Dịch vụ đang hoạt động**
* Số: **118**
* Dòng phụ: mũi tên xanh đi lên, **8% so với tháng trước**

Ý nghĩa:

* Số dịch vụ hiện còn hoạt động, có thể hiển thị cho người dùng/nhân viên đặt lịch.

## 4.3 Card 3 — Dịch vụ tạm ngưng

Nội dung:

* Icon pause, nền cam.
* Tiêu đề: **Dịch vụ tạm ngưng**
* Số: **8**
* Dòng phụ: mũi tên đỏ đi xuống, **3% so với tháng trước**

Ý nghĩa:

* Dịch vụ chưa bị xóa hẳn nhưng tạm thời không nhận đặt lịch.

## 4.4 Card 4 — Dịch vụ ngừng cung cấp

Nội dung:

* Icon thùng rác, nền tím.
* Tiêu đề: **Dịch vụ ngừng cung cấp**
* Số: **6**
* Dòng phụ: mũi tên đỏ đi xuống, **1% so với tháng trước**

Ý nghĩa:

* Các dịch vụ đã dừng hẳn, không còn cung cấp nữa. Có thể vẫn lưu để tra cứu lịch sử hóa đơn hoặc hồ sơ cũ.

---

# 5. Khu vực bộ lọc và thao tác

Bên dưới các card là một khối lớn chứa thanh tìm kiếm, bộ lọc, nút thêm dịch vụ, nút xuất Excel và bảng dữ liệu.

Khối này có:

* Nền trắng.
* Bo góc 12–16px.
* Viền xám nhạt.
* Padding khoảng 20px.
* Chiều rộng gần full nội dung.

## 5.1 Ô tìm kiếm

Nằm bên trái, chiếm khoảng 35–40% chiều ngang.

Placeholder:

**Tìm kiếm dịch vụ (Tên dịch vụ, mã dịch vụ, mô tả...)**

Có icon kính lúp ở bên trái trong input.

Chức năng nên có:

* Tìm theo:

  * Mã dịch vụ.
  * Tên dịch vụ.
  * Mô tả.
  * Danh mục.
* Có debounce khoảng 300–500ms nếu search realtime.
* Hoặc bấm Enter để tìm.
* Không phân biệt hoa thường.
* Có thể hỗ trợ tìm tiếng Việt không dấu.

Ví dụ:

* Gõ “tim mạch” → hiện dịch vụ “Khám chuyên khoa Tim mạch”.
* Gõ “DV001” → hiện dịch vụ có mã DV001.
* Gõ “xet nghiem” → vẫn tìm ra “Xét nghiệm”.

## 5.2 Bộ lọc danh mục dịch vụ

Label:

**Danh mục dịch vụ**

Dropdown mặc định:

**Tất cả**

Các option suy đoán:

* Tất cả
* Khám bệnh
* Xét nghiệm
* Chẩn đoán hình ảnh
* Thăm dò chức năng
* Điều trị
* Vật lý trị liệu
* Tiêm chủng
* Cấp cứu
* Dịch vụ khác

Chức năng:

* Lọc bảng theo danh mục.
* Khi chọn danh mục, bảng cập nhật lại và phân trang quay về trang 1.

## 5.3 Bộ lọc trạng thái

Label:

**Trạng thái**

Dropdown mặc định:

**Tất cả**

Các option nên có:

* Tất cả
* Đang hoạt động
* Tạm ngưng
* Ngừng cung cấp

Chức năng:

* Lọc dịch vụ theo trạng thái hoạt động.

## 5.4 Bộ lọc hiển thị

Label:

**Hiển thị**

Dropdown mặc định:

**Tất cả**

Suy đoán ý nghĩa:

* Dịch vụ có được hiển thị trên hệ thống đặt lịch/app/web bệnh nhân hay không.

Option nên có:

* Tất cả
* Đang hiển thị
* Đang ẩn

Chức năng:

* Lọc dịch vụ theo trạng thái public/private.
* Một dịch vụ có thể “Đang hoạt động” nhưng bị ẩn tạm thời khỏi app bệnh nhân.

## 5.5 Nút Thêm dịch vụ

Nút màu xanh lá, nằm bên phải.

Text:

**+ Thêm dịch vụ**

Đặc điểm:

* Nền xanh lá.
* Text trắng.
* Icon dấu cộng.
* Bo góc khoảng 8px.
* Padding ngang rộng.
* Khi hover nền xanh đậm hơn.

Chức năng:

* Mở modal hoặc chuyển sang trang thêm mới dịch vụ.
* Form thêm mới nên gồm:

  * Mã dịch vụ.
  * Tên dịch vụ.
  * Danh mục.
  * Giá dịch vụ.
  * Thời gian thực hiện.
  * Mô tả.
  * Trạng thái.
  * Có hiển thị hay không.
  * Ghi chú nội bộ nếu cần.

## 5.6 Nút Xuất Excel

Nằm dưới hoặc gần nút thêm dịch vụ, bên phải.

Text:

**Xuất Excel**

Icon Excel màu xanh.

Đặc điểm:

* Nền trắng.
* Viền xám nhạt.
* Text xanh đen.
* Icon Excel màu xanh lá.
* Bo góc 8px.

Chức năng:

* Xuất danh sách dịch vụ ra file Excel.
* Nên xuất theo bộ lọc hiện tại.
* File nên có các cột:

  * STT
  * Mã dịch vụ
  * Tên dịch vụ
  * Danh mục
  * Giá dịch vụ
  * Thời gian
  * Trạng thái
  * Hiển thị
  * Ngày tạo
  * Ngày cập nhật
* Tên file gợi ý: `danh-sach-dich-vu_YYYY-MM-DD.xlsx`.

---

# 6. Bảng danh sách dịch vụ

Bảng nằm dưới khu vực filter.

## 6.1 Header bảng

Các cột lần lượt:

1. Checkbox chọn tất cả
2. **STT**
3. **Mã dịch vụ**
4. **Tên dịch vụ**
5. **Danh mục**
6. **Giá dịch vụ**
7. **Thời gian (phút)**
8. **Trạng thái**
9. **Thao tác**

Header có:

* Nền trắng.
* Text màu xanh đen.
* Font đậm.
* Dòng kẻ ngang xám nhạt phía dưới.
* Checkbox ở đầu bảng.

Chức năng checkbox:

* Checkbox header chọn tất cả dịch vụ trên trang hiện tại.
* Checkbox từng dòng chọn riêng dịch vụ.
* Khi chọn một hoặc nhiều dòng, có thể hiện thanh bulk action:

  * Xóa hàng loạt.
  * Tạm ngưng hàng loạt.
  * Kích hoạt hàng loạt.
  * Xuất các dòng đã chọn.

## 6.2 Dữ liệu đang hiển thị

Có 10 dòng trên trang hiện tại.

### Dòng 1

* STT: 1
* Mã dịch vụ: **DV001**
* Tên dịch vụ: **Khám tổng quát**
* Danh mục: **Khám bệnh**
* Giá dịch vụ: **150.000 ₫**
* Thời gian: **30**
* Trạng thái: **Đang hoạt động**
* Thao tác: xem, sửa, xóa

### Dòng 2

* STT: 2
* Mã dịch vụ: **DV002**
* Tên dịch vụ: **Khám chuyên khoa Tim mạch**
* Danh mục: **Khám bệnh**
* Giá dịch vụ: **200.000 ₫**
* Thời gian: **45**
* Trạng thái: **Đang hoạt động**

### Dòng 3

* STT: 3
* Mã dịch vụ: **DV003**
* Tên dịch vụ: **Khám chuyên khoa Nội tiết**
* Danh mục: **Khám bệnh**
* Giá dịch vụ: **200.000 ₫**
* Thời gian: **45**
* Trạng thái: **Đang hoạt động**

### Dòng 4

* STT: 4
* Mã dịch vụ: **DV004**
* Tên dịch vụ: **Xét nghiệm máu tổng quát**
* Danh mục: **Xét nghiệm**
* Giá dịch vụ: **120.000 ₫**
* Thời gian: **15**
* Trạng thái: **Đang hoạt động**

### Dòng 5

* STT: 5
* Mã dịch vụ: **DV005**
* Tên dịch vụ: **Xét nghiệm đường huyết**
* Danh mục: **Xét nghiệm**
* Giá dịch vụ: **80.000 ₫**
* Thời gian: **10**
* Trạng thái: **Đang hoạt động**

### Dòng 6

* STT: 6
* Mã dịch vụ: **DV006**
* Tên dịch vụ: **Xét nghiệm mỡ máu**
* Danh mục: **Xét nghiệm**
* Giá dịch vụ: **150.000 ₫**
* Thời gian: **15**
* Trạng thái: **Đang hoạt động**

### Dòng 7

* STT: 7
* Mã dịch vụ: **DV007**
* Tên dịch vụ: **Siêu âm ổ bụng tổng quát**
* Danh mục: **Chẩn đoán hình ảnh**
* Giá dịch vụ: **250.000 ₫**
* Thời gian: **30**
* Trạng thái: **Tạm ngưng**

### Dòng 8

* STT: 8
* Mã dịch vụ: **DV008**
* Tên dịch vụ: **Chụp X-quang phổi**
* Danh mục: **Chẩn đoán hình ảnh**
* Giá dịch vụ: **200.000 ₫**
* Thời gian: **20**
* Trạng thái: **Đang hoạt động**

### Dòng 9

* STT: 9
* Mã dịch vụ: **DV009**
* Tên dịch vụ: **Điện tâm đồ (ECG)**
* Danh mục: **Thăm dò chức năng**
* Giá dịch vụ: **120.000 ₫**
* Thời gian: **15**
* Trạng thái: **Tạm ngưng**

### Dòng 10

* STT: 10
* Mã dịch vụ: **DV010**
* Tên dịch vụ: **Vật lý trị liệu**
* Danh mục: **Điều trị**
* Giá dịch vụ: **180.000 ₫**
* Thời gian: **30**
* Trạng thái: **Đang hoạt động**

---

# 7. Hiển thị trạng thái

Cột trạng thái dùng badge màu.

## 7.1 Đang hoạt động

Badge:

* Text: **Đang hoạt động**
* Nền xanh lá nhạt.
* Text xanh lá đậm.
* Bo tròn.
* Padding nhỏ.

Ý nghĩa:

* Dịch vụ đang được sử dụng.
* Có thể đặt lịch.
* Có thể hiển thị cho bệnh nhân nếu trạng thái hiển thị bật.

## 7.2 Tạm ngưng

Badge:

* Text: **Tạm ngưng**
* Nền cam nhạt.
* Text cam đậm.
* Bo tròn.

Ý nghĩa:

* Dịch vụ tạm thời không cho đặt lịch.
* Có thể bật lại sau.

## 7.3 Ngừng cung cấp

Không thấy trong bảng hiện tại nhưng có card thống kê, nên cần hỗ trợ.

Badge đề xuất:

* Text: **Ngừng cung cấp**
* Nền đỏ hoặc tím nhạt.
* Text đỏ/tím đậm.

Ý nghĩa:

* Dịch vụ đã dừng vĩnh viễn.
* Không nên cho đặt lịch mới.
* Không nên xóa cứng nếu đã có lịch sử hóa đơn/hồ sơ liên quan.

---

# 8. Cột thao tác

Mỗi dòng có 3 nút icon nhỏ:

1. Icon mắt: xem chi tiết.
2. Icon bút: chỉnh sửa.
3. Icon thùng rác: xóa.

## 8.1 Nút xem chi tiết

Icon mắt màu xanh dương.

Chức năng:

* Mở modal hoặc trang chi tiết dịch vụ.
* Hiển thị:

  * Mã dịch vụ.
  * Tên dịch vụ.
  * Danh mục.
  * Giá.
  * Thời gian.
  * Mô tả.
  * Trạng thái.
  * Hiển thị/ẩn.
  * Ngày tạo.
  * Người tạo.
  * Ngày cập nhật.
  * Người cập nhật.
  * Số lượt sử dụng nếu có.

## 8.2 Nút chỉnh sửa

Icon bút màu xanh dương.

Chức năng:

* Mở form chỉnh sửa dịch vụ.
* Cho phép sửa:

  * Tên dịch vụ.
  * Danh mục.
  * Giá.
  * Thời gian.
  * Mô tả.
  * Trạng thái.
  * Hiển thị.
* Có thể không cho sửa mã dịch vụ nếu mã đã dùng làm khóa hệ thống.

## 8.3 Nút xóa

Icon thùng rác màu đỏ.

Chức năng:

* Mở popup xác nhận.
* Nội dung gợi ý:

“Bạn có chắc chắn muốn xóa dịch vụ này không? Hành động này có thể ảnh hưởng đến dữ liệu lịch hẹn, hóa đơn hoặc hồ sơ bệnh án liên quan.”

Nên xử lý theo 2 trường hợp:

* Nếu dịch vụ chưa từng được sử dụng → cho phép xóa.
* Nếu dịch vụ đã từng xuất hiện trong lịch hẹn/hóa đơn → không xóa cứng, chỉ chuyển sang **Ngừng cung cấp**.

---

# 9. Phân trang

Dưới bảng có khu vực phân trang.

Bên trái:

**Hiển thị [10 ▼] bản ghi**

Ý nghĩa:

* Người dùng có thể chọn số bản ghi mỗi trang.
* Option nên có:

  * 10
  * 20
  * 50
  * 100

Bên phải là pagination:

* Nút quay lại.
* Trang **1** đang active, nền xanh lá.
* Các trang 2, 3, 4, 5.
* Dấu `...`
* Trang 14.
* Nút đi tiếp.

Chức năng:

* Tổng dữ liệu khoảng 132 bản ghi.
* Nếu mỗi trang 10 bản ghi thì có khoảng 14 trang.
* Khi đổi số bản ghi/trang thì tính lại tổng trang.
* Khi filter/search thay đổi thì reset về trang 1.

---

# 10. Chức năng chính cần có trong màn hình

Màn hình này nên có các chức năng sau:

## 10.1 Xem danh sách dịch vụ

Hiển thị danh sách dịch vụ theo dạng bảng, có phân trang.

Dữ liệu cần có tối thiểu:

* ID nội bộ.
* Mã dịch vụ.
* Tên dịch vụ.
* Danh mục.
* Giá dịch vụ.
* Thời gian thực hiện.
* Trạng thái.
* Trạng thái hiển thị.
* Mô tả.
* Ngày tạo.
* Ngày cập nhật.

## 10.2 Tìm kiếm dịch vụ

Tìm theo:

* Mã dịch vụ.
* Tên dịch vụ.
* Mô tả.
* Danh mục.

Nên hỗ trợ:

* Không phân biệt hoa thường.
* Không dấu tiếng Việt.
* Tìm gần đúng.

## 10.3 Lọc dịch vụ

Lọc theo:

* Danh mục.
* Trạng thái.
* Trạng thái hiển thị.

Có thể mở rộng thêm:

* Khoảng giá.
* Khoảng thời gian thực hiện.
* Ngày tạo.
* Người tạo.
* Dịch vụ được sử dụng nhiều/ít.

## 10.4 Thêm dịch vụ

Form thêm mới nên có validation:

* Mã dịch vụ bắt buộc, không trùng.
* Tên dịch vụ bắt buộc.
* Danh mục bắt buộc.
* Giá phải là số, lớn hơn hoặc bằng 0.
* Thời gian phải là số phút, lớn hơn 0.
* Trạng thái mặc định là **Đang hoạt động**.
* Hiển thị mặc định là **Có**.

## 10.5 Sửa dịch vụ

Khi sửa dịch vụ cần:

* Load dữ liệu cũ vào form.
* Validate giống form thêm.
* Ghi nhận người sửa và thời gian sửa.
* Có thể lưu lịch sử thay đổi giá nếu hệ thống có thanh toán.

## 10.6 Xóa hoặc ngừng cung cấp dịch vụ

Không nên xóa cứng dịch vụ đã phát sinh dữ liệu.

Luồng hợp lý:

* Nếu chưa có lịch hẹn/hóa đơn liên quan → cho xóa.
* Nếu đã có dữ liệu liên quan → chuyển trạng thái sang **Ngừng cung cấp**.
* Hiển thị thông báo rõ ràng cho admin.

## 10.7 Tạm ngưng/kích hoạt lại dịch vụ

Nên có chức năng đổi trạng thái nhanh:

* Đang hoạt động → Tạm ngưng.
* Tạm ngưng → Đang hoạt động.
* Ngừng cung cấp → có thể không cho kích hoạt lại, hoặc cần quyền cao hơn.

## 10.8 Xuất Excel

Xuất danh sách dịch vụ hiện tại ra Excel.

Nên hỗ trợ:

* Xuất toàn bộ.
* Xuất theo bộ lọc.
* Xuất các dòng đã chọn.
* File có định dạng tiền tệ, thời gian, trạng thái dễ đọc.

## 10.9 Thống kê nhanh

4 card phía trên nên lấy dữ liệu realtime hoặc gần realtime:

* Tổng dịch vụ.
* Dịch vụ đang hoạt động.
* Dịch vụ tạm ngưng.
* Dịch vụ ngừng cung cấp.

Phần trăm so với tháng trước cần tính dựa trên dữ liệu tháng hiện tại và tháng trước.

---

# 11. Gợi ý cấu trúc dữ liệu dịch vụ

Một service record có thể như sau:

```json
{
  "id": 1,
  "code": "DV001",
  "name": "Khám tổng quát",
  "category": "Khám bệnh",
  "price": 150000,
  "durationMinutes": 30,
  "status": "ACTIVE",
  "visibility": "VISIBLE",
  "description": "Dịch vụ khám sức khỏe tổng quát",
  "createdAt": "2026-05-01T08:00:00",
  "updatedAt": "2026-05-10T09:30:00",
  "createdBy": "Admin",
  "updatedBy": "Admin"
}
```

Status nên dùng enum:

```txt
ACTIVE = Đang hoạt động
PAUSED = Tạm ngưng
DISCONTINUED = Ngừng cung cấp
```

Visibility nên dùng enum:

```txt
VISIBLE = Đang hiển thị
HIDDEN = Đang ẩn
```

---

# 12. Gợi ý API cần có

Các API backend hợp lý cho màn hình này:

```txt
GET /admin/services
```

Lấy danh sách dịch vụ, hỗ trợ query:

```txt
?page=1
&limit=10
&keyword=tim mach
&category=Kham benh
&status=ACTIVE
&visibility=VISIBLE
```

```txt
GET /admin/services/statistics
```

Lấy dữ liệu 4 card thống kê.

```txt
GET /admin/services/:id
```

Xem chi tiết dịch vụ.

```txt
POST /admin/services
```

Thêm dịch vụ.

```txt
PUT /admin/services/:id
```

Cập nhật dịch vụ.

```txt
DELETE /admin/services/:id
```

Xóa dịch vụ nếu được phép.

```txt
PATCH /admin/services/:id/status
```

Đổi trạng thái dịch vụ.

```txt
GET /admin/services/export
```

Xuất Excel theo bộ lọc.

---

# 13. Quy tắc nghiệp vụ nên có

Một số quy tắc quan trọng:

1. **Mã dịch vụ không được trùng.**
2. **Không cho giá âm.**
3. **Thời gian thực hiện phải lớn hơn 0.**
4. **Dịch vụ ngừng cung cấp không được đặt lịch mới.**
5. **Dịch vụ tạm ngưng không được đặt lịch mới nhưng vẫn giữ dữ liệu cũ.**
6. **Không xóa cứng dịch vụ đã có hóa đơn, lịch hẹn hoặc hồ sơ liên quan.**
7. **Chỉ admin có quyền mới được thêm, sửa, xóa dịch vụ.**
8. **Nhân viên thường có thể chỉ được xem.**
9. **Mọi thao tác thêm/sửa/xóa nên ghi log.**
10. **Khi thay đổi giá dịch vụ, hóa đơn cũ không được bị thay đổi theo.**

---

# 14. Trạng thái giao diện cần xử lý

Khi implement, không chỉ làm trạng thái bình thường như ảnh, mà cần thêm:

## Loading

Khi đang tải dữ liệu:

* Hiển thị skeleton table.
* Disable nút filter/xuất Excel nếu cần.

## Empty state

Khi không có dịch vụ nào:

Text gợi ý:

**Không tìm thấy dịch vụ phù hợp**

Có thể kèm nút:

**Thêm dịch vụ mới**

## Error state

Khi lỗi API:

Text:

**Không thể tải danh sách dịch vụ. Vui lòng thử lại.**

Có nút:

**Tải lại**

## No permission

Nếu tài khoản không có quyền:

* Ẩn nút thêm/sửa/xóa.
* Hoặc disable và hiển thị tooltip “Bạn không có quyền thực hiện thao tác này.”

---

# 15. Gợi ý responsive

Trên desktop, layout như ảnh:

* Sidebar bên trái.
* Nội dung bên phải.
* 4 card nằm ngang.
* Filter nằm một hàng.
* Table full width.

Trên tablet:

* Sidebar có thể thu gọn còn icon.
* 4 card chuyển thành 2 cột.
* Filter xuống 2 hàng.

Trên mobile:

* Sidebar chuyển thành drawer.
* 4 card thành 1 cột.
* Bảng có scroll ngang.
* Nút “Thêm dịch vụ” và “Xuất Excel” xếp dọc hoặc nằm trong menu hành động.

---

# 16. Màu sắc gợi ý

Có thể dùng palette gần giống ảnh:

```txt
Màu nền chính: #F8FAFC
Màu card: #FFFFFF
Màu chữ chính: #0F172A
Màu chữ phụ: #64748B
Màu xanh lá chính: #16A34A
Màu xanh lá nhạt: #DCFCE7
Màu xanh dương: #2563EB
Màu cam: #F97316
Màu cam nhạt: #FFEDD5
Màu đỏ: #EF4444
Màu đỏ nhạt: #FEE2E2
Màu tím: #7E22CE
Màu viền: #E2E8F0
```

---

# 17. Tóm tắt yêu cầu để đưa cho dev/UI designer

Màn hình cần xây dựng là trang **Quản lý dịch vụ** trong hệ thống **CarePlus Admin**. Trang có sidebar quản trị, header admin, 4 thẻ thống kê dịch vụ, khu vực tìm kiếm/lọc, nút thêm dịch vụ, nút xuất Excel, bảng danh sách dịch vụ có checkbox chọn dòng, badge trạng thái, các nút xem/sửa/xóa và phân trang. Chức năng chính gồm CRUD dịch vụ, tìm kiếm, lọc, phân trang, xuất Excel, đổi trạng thái dịch vụ, quản lý hiển thị, kiểm tra quyền và xử lý không xóa cứng dữ liệu đã phát sinh lịch sử.
