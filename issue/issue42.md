Dưới đây là mô tả chi tiết giao diện **CarePlus Admin – Quản lý tài khoản**, viết theo kiểu đặc tả để người khác nhìn mô tả cũng có thể dựng lại giao diện và suy luận chức năng.

---

## 1. Tổng quan màn hình

Đây là màn hình quản trị của hệ thống **CarePlus Admin**, dùng để **quản lý tài khoản người dùng** trong hệ thống y tế/phòng khám/bệnh viện.

Màn hình có bố cục dashboard admin gồm:

* Thanh menu dọc bên trái.
* Khu vực nội dung chính bên phải.
* Header phía trên nội dung.
* Các thẻ thống kê nhanh.
* Khu vực tìm kiếm, lọc và thao tác.
* Bảng danh sách tài khoản.
* Phân trang và chọn số bản ghi hiển thị.

Tông màu chủ đạo là **trắng – xanh lá – xanh dương**, tạo cảm giác sạch sẽ, hiện đại, phù hợp với hệ thống y tế. Các trạng thái dùng màu rõ ràng: xanh lá cho hoạt động, đỏ cho bị khóa, cam/tím/xanh cho từng loại vai trò.

---

## 2. Thanh sidebar bên trái

Sidebar nằm cố định bên trái, chiều rộng khoảng **280–300px**, nền trắng hoặc xanh rất nhạt. Phía trên cùng là logo hệ thống.

### Logo

Ở góc trên bên trái có biểu tượng dấu cộng màu xanh lá trong hình tròn, bên cạnh là chữ:

**CarePlus Admin**

Chữ “CarePlus” màu xanh lá, “Admin” cũng cùng tông xanh, font đậm, tạo cảm giác thương hiệu y tế.

### Danh sách menu

Các menu được xếp dọc, mỗi mục có icon bên trái và nhãn bên phải. Khoảng cách giữa các item rộng, dễ bấm.

Các mục gồm:

1. **Dashboard**

   * Icon hình ngôi nhà.
   * Dẫn về trang tổng quan.

2. **Quản lý tài khoản**

   * Icon hình người.
   * Đây là mục đang được chọn.
   * Nền item được tô xanh lá rất nhạt.
   * Chữ và icon màu xanh lá.
   * Có thể hiểu đây là trang hiện tại.

3. **Quản lý bác sĩ**

   * Icon bác sĩ/ống nghe.
   * Quản lý hồ sơ bác sĩ.

4. **Quản lý bệnh nhân**

   * Icon nhóm người.
   * Quản lý bệnh nhân trong hệ thống.

5. **Quản lý thuốc**

   * Icon viên thuốc.
   * Quản lý danh mục thuốc, tồn kho, giá thuốc.

6. **Quản lý dịch vụ**

   * Icon ống nghe/dịch vụ.
   * Quản lý dịch vụ khám, xét nghiệm, điều trị.

7. **Quản lý thanh toán**

   * Icon thẻ ngân hàng.
   * Quản lý hóa đơn, giao dịch, thanh toán.

8. **Xem báo cáo thống kê**

   * Icon biểu đồ cột.
   * Xem báo cáo doanh thu, bệnh nhân, lịch khám, tài khoản.

9. **Phân quyền hệ thống**

   * Icon khiên.
   * Quản lý vai trò, quyền truy cập.

10. **Sao lưu dữ liệu**

* Icon đám mây/tải xuống.
* Sao lưu hoặc khôi phục dữ liệu.

### Nút đăng xuất

Ở cuối sidebar có nút **Đăng xuất**.

* Nền đỏ rất nhạt.
* Icon đăng xuất màu đỏ.
* Chữ màu đỏ.
* Bo góc lớn.
* Nằm tách biệt với menu chính, sát phía dưới.

Chức năng suy đoán: khi bấm vào sẽ hiển thị popup xác nhận “Bạn có chắc muốn đăng xuất không?” rồi chuyển về màn hình đăng nhập.

---

## 3. Header khu vực nội dung

Bên phải sidebar là phần nội dung chính. Trên cùng có tiêu đề và khu vực tài khoản admin.

### Tiêu đề trang

Góc trên bên trái của nội dung có tiêu đề lớn:

**Quản lý tài khoản**

Bên dưới là breadcrumb:

**Dashboard / Quản lý tài khoản**

Breadcrumb giúp người dùng biết đang ở đâu trong hệ thống.

### Góc trên bên phải

Có 3 thành phần:

1. **Icon chuông thông báo**

   * Có badge đỏ nhỏ hiển thị số **3**.
   * Nghĩa là có 3 thông báo chưa đọc.
   * Có thể bấm để mở dropdown thông báo.

2. **Avatar admin**

   * Avatar hình người mặc vest.
   * Nằm trong hình tròn hoặc khung bo tròn.

3. **Thông tin tài khoản**

   * Hiển thị: **Admin (Quản trị viên)**
   * Có mũi tên dropdown bên phải.
   * Khi bấm có thể mở menu: thông tin cá nhân, đổi mật khẩu, cài đặt, đăng xuất.

---

## 4. Khu vực thẻ thống kê nhanh

Bên dưới header là 4 thẻ thống kê nằm ngang. Mỗi thẻ có nền trắng, bo góc, viền mảnh màu xám nhạt, bóng nhẹ.

### Thẻ 1: Tổng tài khoản

* Icon: nhóm người màu trắng nằm trong ô vuông xanh dương.
* Tiêu đề: **Tổng tài khoản**
* Số lớn: **56**
* Dòng phụ: mũi tên lên màu xanh, **12% so với tháng trước**

Ý nghĩa: toàn hệ thống hiện có 56 tài khoản, tăng 12% so với tháng trước.

Chức năng suy đoán: bấm vào thẻ này có thể lọc bảng về tất cả tài khoản.

---

### Thẻ 2: Tài khoản hoạt động

* Icon: người dùng màu trắng trong ô vuông xanh lá.
* Tiêu đề: **Tài khoản hoạt động**
* Số lớn: **48**
* Dòng phụ: mũi tên lên màu xanh, **9% so với tháng trước**

Ý nghĩa: có 48 tài khoản đang hoạt động.

Chức năng suy đoán: bấm vào thẻ sẽ lọc trạng thái “Hoạt động”.

---

### Thẻ 3: Tài khoản bị khóa

* Icon: ổ khóa màu trắng trong ô vuông cam.
* Tiêu đề: **Tài khoản bị khóa**
* Số lớn: **5**
* Dòng phụ: mũi tên xuống màu đỏ, **3% so với tháng trước**

Ý nghĩa: có 5 tài khoản đang bị khóa. Số tài khoản bị khóa giảm 3% so với tháng trước, đây có thể là tín hiệu tốt.

Chức năng suy đoán: bấm vào thẻ sẽ lọc trạng thái “Bị khóa”.

---

### Thẻ 4: Vai trò hệ thống

* Icon: khiên màu trắng trong ô vuông tím.
* Tiêu đề: **Vai trò hệ thống**
* Số lớn: **6**
* Dòng phụ: **Quản lý vai trò**

Ý nghĩa: hệ thống hiện có 6 vai trò chính.

Chức năng suy đoán: bấm vào thẻ sẽ chuyển sang trang **Phân quyền hệ thống** hoặc mở danh sách vai trò.

---

## 5. Khu vực tìm kiếm, lọc và thao tác

Bên dưới các thẻ thống kê là một khối lớn chứa bộ lọc và bảng dữ liệu. Khối này có nền trắng, bo góc, viền mảnh.

### Ô tìm kiếm

Nằm bên trái hàng điều khiển.

Placeholder:

**Tìm kiếm tài khoản (Tên, email, SĐT...)**

Có icon kính lúp ở đầu ô input.

Chức năng:

* Tìm theo họ tên.
* Tìm theo email.
* Tìm theo số điện thoại.
* Có thể tìm không dấu hoặc có dấu.
* Nên hỗ trợ debounce khoảng 300–500ms để không gọi API quá nhiều.

Ví dụ tìm:

* “Nam”
* “nam.nguyen”
* “0987”
* “Nguyễn Văn”

---

### Bộ lọc vai trò

Có label: **Vai trò**

Dropdown mặc định: **Tất cả**

Các lựa chọn suy đoán:

* Tất cả
* Quản trị viên
* Bác sĩ
* Lễ tân
* Kế toán
* Điều dưỡng
* Nhân viên
* Khách hàng

Khi chọn một vai trò, bảng chỉ hiển thị tài khoản thuộc vai trò đó.

---

### Bộ lọc trạng thái

Có label: **Trạng thái**

Dropdown mặc định: **Tất cả**

Các lựa chọn:

* Tất cả
* Hoạt động
* Bị khóa

Có thể mở rộng thêm:

* Chờ xác thực
* Tạm ngưng
* Đã xóa mềm

---

### Nút Thêm tài khoản

Nằm bên phải, màu xanh lá nổi bật.

Nội dung:

**+ Thêm tài khoản**

Chức năng suy đoán:

Khi bấm sẽ mở modal hoặc chuyển sang trang tạo tài khoản mới.

Form thêm tài khoản nên có:

* Họ và tên
* Email
* Số điện thoại
* Vai trò
* Trạng thái mặc định
* Mật khẩu tạm thời
* Xác nhận mật khẩu
* Ảnh đại diện
* Ghi chú
* Tùy chọn gửi email kích hoạt tài khoản

Cần validate:

* Email đúng định dạng.
* Email không được trùng.
* Số điện thoại đúng định dạng.
* Vai trò bắt buộc chọn.
* Mật khẩu đủ mạnh nếu nhập thủ công.

---

### Nút Xuất Excel

Nằm dưới hoặc gần nút thêm tài khoản.

Nội dung:

**Xuất Excel**

Có icon Excel màu xanh.

Chức năng:

* Xuất danh sách tài khoản ra file `.xlsx`.
* Có thể xuất theo bộ lọc hiện tại.
* Ví dụ: nếu đang lọc “Bác sĩ” thì chỉ xuất danh sách bác sĩ.
* File nên có các cột: STT, Họ tên, Email, SĐT, Vai trò, Trạng thái, Ngày tạo.

---

## 6. Bảng danh sách tài khoản

Bảng chiếm phần lớn màn hình. Thiết kế sạch, nhiều khoảng trắng, đường kẻ ngang mảnh.

### Các cột trong bảng

Từ trái sang phải:

1. Checkbox chọn dòng
2. **STT**
3. **Họ và tên**
4. **Email**
5. **Số điện thoại**
6. **Vai trò**
7. **Trạng thái**
8. **Ngày tạo**
9. **Thao tác**

### Checkbox

Ở đầu bảng có checkbox tổng.

Chức năng:

* Chọn tất cả tài khoản trên trang hiện tại.
* Khi chọn nhiều tài khoản, có thể hiện thanh thao tác hàng loạt.

Chức năng hàng loạt nên có:

* Khóa tài khoản
* Mở khóa tài khoản
* Xóa tài khoản
* Gán vai trò
* Xuất Excel các dòng đã chọn

---

## 7. Dữ liệu hiển thị trong bảng

Bảng hiện 10 dòng dữ liệu.

### Dòng 1

* STT: **1**
* Họ tên: **Nguyễn Văn Nam**
* Email: **[nam.nguyen@gmail.com](mailto:nam.nguyen@gmail.com)**
* Số điện thoại: **0987 654 321**
* Vai trò: **Quản trị viên**
* Trạng thái: **Hoạt động**
* Ngày tạo: **24/05/2026 09:15**

Vai trò “Quản trị viên” dùng badge màu xanh lá.

---

### Dòng 2

* STT: **2**
* Họ tên: **Trần Thị Mai**
* Email: **[mai.tran@gmail.com](mailto:mai.tran@gmail.com)**
* Số điện thoại: **0912 345 678**
* Vai trò: **Bác sĩ**
* Trạng thái: **Hoạt động**
* Ngày tạo: **24/05/2026 09:30**

Vai trò “Bác sĩ” dùng badge xanh dương nhạt.

---

### Dòng 3

* STT: **3**
* Họ tên: **Lê Văn Cường**
* Email: **[cuong.le@gmail.com](mailto:cuong.le@gmail.com)**
* Số điện thoại: **0933 456 789**
* Vai trò: **Bác sĩ**
* Trạng thái: **Hoạt động**
* Ngày tạo: **24/05/2026 10:00**

---

### Dòng 4

* STT: **4**
* Họ tên: **Phạm Thị Lan**
* Email: **[lan.pham@gmail.com](mailto:lan.pham@gmail.com)**
* Số điện thoại: **0909 876 543**
* Vai trò: **Lễ tân**
* Trạng thái: **Hoạt động**
* Ngày tạo: **24/05/2026 10:30**

Vai trò “Lễ tân” dùng badge màu cam nhạt.

---

### Dòng 5

* STT: **5**
* Họ tên: **Hoàng Anh Tuấn**
* Email: **[tuan.hoang@gmail.com](mailto:tuan.hoang@gmail.com)**
* Số điện thoại: **0988 765 432**
* Vai trò: **Kế toán**
* Trạng thái: **Hoạt động**
* Ngày tạo: **24/05/2026 11:00**

Vai trò “Kế toán” dùng badge tím nhạt.

---

### Dòng 6

* STT: **6**
* Họ tên: **Vũ Thị Hương**
* Email: **[huong.vu@gmail.com](mailto:huong.vu@gmail.com)**
* Số điện thoại: **0977 654 321**
* Vai trò: **Điều dưỡng**
* Trạng thái: **Bị khóa**
* Ngày tạo: **24/05/2026 11:30**

Trạng thái “Bị khóa” dùng badge đỏ nhạt.

---

### Dòng 7

* STT: **7**
* Họ tên: **Đỗ Minh Quân**
* Email: **[quan.do@gmail.com](mailto:quan.do@gmail.com)**
* Số điện thoại: **0966 543 210**
* Vai trò: **Nhân viên**
* Trạng thái: **Hoạt động**
* Ngày tạo: **24/05/2026 12:00**

Vai trò “Nhân viên” dùng badge xám nhạt.

---

### Dòng 8

* STT: **8**
* Họ tên: **Nguyễn Thị Hoa**
* Email: **[hoa.nguyen@gmail.com](mailto:hoa.nguyen@gmail.com)**
* Số điện thoại: **0908 111 222**
* Vai trò: **Nhân viên**
* Trạng thái: **Bị khóa**
* Ngày tạo: **24/05/2026 12:30**

---

### Dòng 9

* STT: **9**
* Họ tên: **Bùi Văn Dũng**
* Email: **[dung.bui@gmail.com](mailto:dung.bui@gmail.com)**
* Số điện thoại: **0982 333 444**
* Vai trò: **Nhân viên**
* Trạng thái: **Hoạt động**
* Ngày tạo: **24/05/2026 13:00**

---

### Dòng 10

* STT: **10**
* Họ tên: **Trương Văn Kiên**
* Email: **[kien.truong@gmail.com](mailto:kien.truong@gmail.com)**
* Số điện thoại: **0933 999 000**
* Vai trò: **Khách hàng**
* Trạng thái: **Hoạt động**
* Ngày tạo: **24/05/2026 13:30**

Vai trò “Khách hàng” dùng badge màu cam nhạt.

---

## 8. Avatar người dùng trong bảng

Mỗi tài khoản có avatar nhỏ nằm trước tên.

Avatar dạng minh họa hoạt hình, kích thước khoảng **28–32px**, hình tròn hoặc bo tròn nhẹ. Có sự khác nhau giữa nam/nữ.

Chức năng suy đoán:

* Nếu người dùng có ảnh đại diện thì hiển thị ảnh thật.
* Nếu không có ảnh thì dùng avatar mặc định theo giới tính hoặc chữ cái đầu tên.
* Có thể bấm vào avatar hoặc tên để xem hồ sơ tài khoản.

---

## 9. Badge vai trò

Vai trò được hiển thị bằng nhãn nhỏ bo tròn, mỗi vai trò có màu riêng để dễ phân biệt.

Gợi ý màu:

* **Quản trị viên**: xanh lá.
* **Bác sĩ**: xanh dương.
* **Lễ tân**: cam.
* **Kế toán**: tím.
* **Điều dưỡng**: xanh cyan.
* **Nhân viên**: xám.
* **Khách hàng**: cam/vàng nhạt.

Mỗi badge có nền nhạt, chữ đậm hơn màu nền, padding ngang vừa phải, bo tròn.

---

## 10. Badge trạng thái

Trạng thái hiện có 2 loại:

### Hoạt động

* Nền xanh lá nhạt.
* Chữ xanh lá.
* Cho biết tài khoản có thể đăng nhập và sử dụng hệ thống.

### Bị khóa

* Nền đỏ nhạt.
* Chữ đỏ.
* Cho biết tài khoản không thể đăng nhập hoặc đã bị admin khóa.

Chức năng suy đoán:

* Tài khoản bị khóa có thể được mở khóa từ màn hình chi tiết hoặc nút thao tác.
* Khi khóa tài khoản nên yêu cầu nhập lý do khóa.
* Khi mở khóa nên ghi log thao tác.

---

## 11. Cột thao tác

Cột cuối cùng có 3 nút icon nằm ngang:

1. **Xem chi tiết**

   * Icon con mắt.
   * Màu xanh dương.
   * Nền xanh rất nhạt.
   * Khi bấm mở màn hình hoặc modal chi tiết tài khoản.

2. **Chỉnh sửa**

   * Icon cây bút.
   * Màu xanh dương.
   * Khi bấm mở form chỉnh sửa thông tin tài khoản.

3. **Xóa**

   * Icon thùng rác.
   * Màu đỏ.
   * Nền đỏ nhạt.
   * Khi bấm cần hiện popup xác nhận.

Chức năng nên có thêm:

* Không cho admin tự xóa chính mình.
* Không cho xóa quản trị viên cuối cùng.
* Xóa nên là “xóa mềm” để có thể khôi phục.
* Ghi log người thao tác, thời gian thao tác.

---

## 12. Phân trang

Phía dưới bảng có khu vực phân trang.

Bên trái:

**Hiển thị [10] bản ghi**

Dropdown đang chọn **10**.

Có thể có các lựa chọn:

* 10
* 20
* 50
* 100

Bên phải là phân trang:

* Nút quay lại.
* Trang **1** đang được chọn, nền xanh lá.
* Các trang: 2, 3, 4, 5.
* Dấu `...`.
* Trang 6.
* Nút đi tới.

Chức năng:

* Khi đổi trang, dữ liệu bảng thay đổi.
* Khi đổi số bản ghi, bảng reload lại từ trang 1.
* Nên giữ lại trạng thái tìm kiếm/lọc khi chuyển trang.

---

## 13. Các chức năng chính cần có

Màn hình này nên có các chức năng sau:

### Quản lý danh sách tài khoản

* Xem danh sách tài khoản.
* Tìm kiếm theo tên, email, số điện thoại.
* Lọc theo vai trò.
* Lọc theo trạng thái.
* Phân trang.
* Chọn số lượng bản ghi hiển thị.
* Xuất Excel.

### Thêm tài khoản

Admin có thể tạo tài khoản mới.

Thông tin nên gồm:

* Họ tên.
* Email.
* Số điện thoại.
* Vai trò.
* Trạng thái.
* Mật khẩu tạm thời.
* Ảnh đại diện.
* Ghi chú.
* Tùy chọn gửi email kích hoạt.

### Xem chi tiết tài khoản

Modal hoặc trang chi tiết nên hiển thị:

* Ảnh đại diện.
* Họ tên.
* Email.
* Số điện thoại.
* Vai trò.
* Trạng thái.
* Ngày tạo.
* Lần đăng nhập gần nhất.
* Người tạo tài khoản.
* Lịch sử thay đổi.
* Các quyền đang có.

### Chỉnh sửa tài khoản

Admin có thể sửa:

* Họ tên.
* Số điện thoại.
* Vai trò.
* Trạng thái.
* Ảnh đại diện.
* Ghi chú.

Nên hạn chế sửa email nếu email là định danh đăng nhập chính.

### Khóa / mở khóa tài khoản

Với tài khoản hoạt động:

* Có thể khóa tài khoản.
* Khi khóa cần xác nhận.
* Có thể yêu cầu nhập lý do khóa.

Với tài khoản bị khóa:

* Có thể mở khóa.
* Có thể gửi lại email kích hoạt hoặc reset mật khẩu.

### Xóa tài khoản

Nên dùng xóa mềm.

Khi bấm xóa:

* Hiện popup: “Bạn có chắc chắn muốn xóa tài khoản này không?”
* Có nút Hủy và Xóa.
* Sau khi xóa hiển thị toast thành công.
* Không xóa vĩnh viễn ngay để tránh mất dữ liệu.

### Xuất Excel

Có thể xuất:

* Toàn bộ danh sách.
* Danh sách theo bộ lọc.
* Các dòng đang chọn.

File Excel nên có tên dạng:

`danh-sach-tai-khoan-24-05-2026.xlsx`

---

## 14. Các trạng thái giao diện cần thiết

Để làm hoàn chỉnh, màn hình nên xử lý đủ các trạng thái sau:

### Loading

Khi đang tải dữ liệu:

* Hiển thị skeleton table hoặc spinner.
* Các nút thao tác có thể disable.

### Không có dữ liệu

Khi không tìm thấy tài khoản:

* Hiển thị icon rỗng.
* Text: “Không tìm thấy tài khoản phù hợp.”
* Có nút “Xóa bộ lọc” nếu đang lọc.

### Lỗi tải dữ liệu

Khi API lỗi:

* Hiển thị thông báo lỗi.
* Có nút “Thử lại”.

### Thành công

Sau khi thêm/sửa/xóa:

* Hiển thị toast góc phải:

  * “Thêm tài khoản thành công”
  * “Cập nhật tài khoản thành công”
  * “Xóa tài khoản thành công”
  * “Khóa tài khoản thành công”

---

## 15. Phân quyền thao tác

Vì đây là màn hình quản lý tài khoản, cần kiểm soát quyền rất kỹ.

Ví dụ:

### Quản trị viên

Có quyền:

* Xem tất cả tài khoản.
* Thêm tài khoản.
* Sửa tài khoản.
* Xóa tài khoản.
* Khóa/mở khóa tài khoản.
* Gán vai trò.
* Xuất Excel.

### Nhân viên thường

Có thể chỉ được:

* Xem danh sách giới hạn.
* Không được xóa.
* Không được thay đổi vai trò.

### Bác sĩ

Có thể không được truy cập màn hình này, hoặc chỉ xem thông tin bệnh nhân/liên quan.

### Kế toán

Có thể chỉ xem tài khoản liên quan thanh toán, không được sửa quyền.

---

## 16. Gợi ý API cho màn hình này

Có thể thiết kế các API như sau:

```txt
GET    /api/admin/accounts
GET    /api/admin/accounts/:id
POST   /api/admin/accounts
PUT    /api/admin/accounts/:id
DELETE /api/admin/accounts/:id
PATCH  /api/admin/accounts/:id/lock
PATCH  /api/admin/accounts/:id/unlock
POST   /api/admin/accounts/:id/reset-password
GET    /api/admin/accounts/export
GET    /api/admin/roles
```

Query cho danh sách:

```txt
/api/admin/accounts?page=1&limit=10&search=nam&role=doctor&status=active
```

Response danh sách nên có:

```json
{
  "data": [],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 56,
    "totalPages": 6
  },
  "stats": {
    "totalAccounts": 56,
    "activeAccounts": 48,
    "lockedAccounts": 5,
    "totalRoles": 6
  }
}
```

---

## 17. Gợi ý cấu trúc dữ liệu tài khoản

Một tài khoản có thể có cấu trúc:

```json
{
  "id": "acc_001",
  "fullName": "Nguyễn Văn Nam",
  "email": "nam.nguyen@gmail.com",
  "phone": "0987654321",
  "avatar": "/avatars/nam.png",
  "role": {
    "id": "admin",
    "name": "Quản trị viên"
  },
  "status": "active",
  "createdAt": "2026-05-24T09:15:00",
  "lastLoginAt": "2026-05-25T08:30:00"
}
```

---

## 18. Gợi ý thiết kế form thêm/sửa tài khoản

Form nên có layout 2 cột trên desktop.

### Nhóm thông tin cá nhân

* Họ và tên
* Email
* Số điện thoại
* Ảnh đại diện

### Nhóm thông tin hệ thống

* Vai trò
* Trạng thái
* Mật khẩu tạm thời
* Xác nhận mật khẩu
* Gửi email kích hoạt

### Nút hành động

* Hủy
* Lưu thay đổi
* Tạo tài khoản

Nếu là chỉnh sửa thì không cần nhập mật khẩu, thay vào đó có nút **Đặt lại mật khẩu**.

---

## 19. Gợi ý modal xem chi tiết

Khi bấm icon con mắt, modal có thể hiển thị:

* Avatar lớn.
* Tên tài khoản.
* Vai trò.
* Trạng thái.
* Email.
* Số điện thoại.
* Ngày tạo.
* Lần đăng nhập gần nhất.
* Danh sách quyền.
* Lịch sử hoạt động gần đây.

Các nút trong modal:

* Chỉnh sửa
* Khóa tài khoản / Mở khóa
* Đặt lại mật khẩu
* Đóng

---

## 20. Giao diện tổng thể nên được hiểu như sau

Đây là một màn hình admin hoàn chỉnh để quản trị viên theo dõi và xử lý tài khoản trong hệ thống CarePlus. Người dùng chính của màn hình là **admin/quản trị viên**, cần thao tác nhanh với nhiều tài khoản.

Luồng sử dụng chính:

1. Admin vào trang **Quản lý tài khoản**.
2. Nhìn nhanh số lượng tài khoản qua 4 thẻ thống kê.
3. Tìm kiếm hoặc lọc tài khoản theo vai trò/trạng thái.
4. Xem danh sách trong bảng.
5. Bấm xem chi tiết, chỉnh sửa hoặc xóa từng tài khoản.
6. Có thể thêm tài khoản mới bằng nút xanh.
7. Có thể xuất danh sách ra Excel.
8. Có thể chuyển trang nếu dữ liệu nhiều.

Giao diện này nên ưu tiên: **rõ ràng, dễ tìm kiếm, dễ thao tác, kiểm soát quyền chặt chẽ và tránh thao tác nhầm khi xóa/khóa tài khoản.**
