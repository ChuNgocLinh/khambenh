Dưới đây là mô tả rất chi tiết giao diện **CarePlus Admin – Quản lý thuốc**, đủ để đưa cho designer/dev làm lại gần giống và suy đoán thêm chức năng cần có.

---

# 1. Tổng quan màn hình

Đây là giao diện quản trị dành cho hệ thống y tế/phòng khám/nhà thuốc, module hiện tại là **Quản lý thuốc**. Màn hình dùng để xem danh sách thuốc, theo dõi tồn kho, trạng thái thuốc, thêm/sửa/xóa thuốc, xuất Excel và lọc dữ liệu.

Giao diện chia thành 2 phần lớn:

1. **Sidebar bên trái**: menu điều hướng các module quản trị.
2. **Khu nội dung chính bên phải**: tiêu đề trang, breadcrumb, thống kê nhanh, bộ lọc, bảng danh sách thuốc và phân trang.

Phong cách thiết kế hiện đại, nền sáng, nhiều khoảng trắng, bo góc lớn, màu chủ đạo xanh lá của thương hiệu CarePlus.

---

# 2. Sidebar bên trái

Sidebar nằm cố định bên trái, chiều rộng khoảng **260–300px**, nền trắng hoặc gần trắng.

## 2.1 Logo / thương hiệu

Ở góc trên trái có logo:

* Icon hình dấu cộng y tế màu xanh lá trong vòng tròn.
* Text thương hiệu: **CarePlus Admin**
* Chữ “CarePlus” màu xanh lá, “Admin” cùng màu hoặc đậm hơn.
* Font sans-serif hiện đại, cỡ khoảng 22–26px, đậm.

Mục đích: nhận diện đây là hệ thống admin của CarePlus.

## 2.2 Danh sách menu

Menu gồm các mục sau, mỗi mục có icon bên trái và text bên phải:

1. **Dashboard**

   * Icon ngôi nhà.
   * Dẫn đến trang tổng quan hệ thống.

2. **Quản lý tài khoản**

   * Icon người dùng.
   * Dùng để quản lý tài khoản đăng nhập của admin, bác sĩ, nhân viên, bệnh nhân.

3. **Quản lý bác sĩ**

   * Icon bác sĩ / người có ống nghe.
   * Dùng để thêm, sửa, xóa, xem thông tin bác sĩ.

4. **Quản lý bệnh nhân**

   * Icon nhóm người.
   * Dùng để quản lý hồ sơ bệnh nhân.

5. **Quản lý thuốc**

   * Icon viên thuốc màu xanh.
   * Đây là menu đang được chọn.
   * Nền menu active là xanh nhạt.
   * Text màu xanh lá.
   * Có bo góc khoảng 8–12px.
   * Cho thấy người dùng đang ở module quản lý thuốc.

6. **Quản lý dịch vụ**

   * Icon ống nghe.
   * Quản lý các dịch vụ khám/chữa bệnh, xét nghiệm, tư vấn.

7. **Quản lý thanh toán**

   * Icon thẻ thanh toán.
   * Quản lý hóa đơn, giao dịch, thanh toán.

8. **Xem báo cáo thống kê**

   * Icon biểu đồ cột.
   * Dùng để xem doanh thu, số lượt khám, thống kê thuốc, bệnh nhân.

9. **Phân quyền hệ thống**

   * Icon khiên bảo mật.
   * Quản lý vai trò, quyền truy cập của từng nhóm người dùng.

10. **Sao lưu dữ liệu**

* Icon đám mây / tải xuống.
* Dùng để backup dữ liệu hệ thống.

## 2.3 Nút đăng xuất

Ở cuối sidebar có nút **Đăng xuất**.

* Nền đỏ rất nhạt.
* Icon logout màu đỏ.
* Text “Đăng xuất” màu đỏ.
* Bo góc lớn.
* Khi bấm sẽ đăng xuất khỏi tài khoản admin.

Nút này nên cố định ở gần đáy sidebar để người dùng dễ tìm.

---

# 3. Header khu nội dung chính

Phần nội dung chính nằm bên phải sidebar, nền tổng thể màu trắng ngà hoặc xám rất nhạt.

## 3.1 Tiêu đề trang

Ở góc trên bên trái khu nội dung có tiêu đề lớn:

**Quản lý thuốc**

* Font lớn khoảng 28–34px.
* Màu xanh navy đậm.
* In đậm.

Bên dưới là breadcrumb:

**Dashboard / Quản lý thuốc**

* “Dashboard” là trang cha.
* “Quản lý thuốc” là trang hiện tại.
* Text nhỏ hơn, màu xanh xám.
* Dấu `/` phân cách.

## 3.2 Khu tài khoản góc phải

Góc trên bên phải có:

1. **Icon chuông thông báo**

   * Màu xanh navy.
   * Có badge đỏ số **3** ở góc trên phải.
   * Suy đoán: có 3 thông báo chưa đọc, ví dụ thuốc sắp hết, thuốc hết hàng, yêu cầu nhập kho.

2. **Avatar admin**

   * Hình đại diện dạng minh họa.
   * Nằm cạnh tên tài khoản.

3. **Tên người dùng**

   * Text: **Admin (Quản trị viên)**
   * Có icon mũi tên xuống.
   * Khi bấm có thể mở menu:

     * Hồ sơ cá nhân
     * Đổi mật khẩu
     * Cài đặt tài khoản
     * Đăng xuất

---

# 4. Khu thống kê nhanh

Ngay dưới tiêu đề có 4 thẻ thống kê nằm ngang. Mỗi thẻ có bo góc lớn, nền trắng, bóng nhẹ, viền mờ. Khoảng cách giữa các thẻ đều nhau.

Các thẻ này dùng để tóm tắt nhanh tình trạng kho thuốc.

---

## 4.1 Thẻ “Tổng số thuốc”

Nội dung:

* Icon viên thuốc màu trắng trên nền xanh dương gradient.
* Tiêu đề: **Tổng số thuốc**
* Số liệu lớn: **256**
* Dòng so sánh: mũi tên tăng màu xanh, **12% so với tháng trước**

Ý nghĩa:

* Hệ thống hiện có tổng cộng 256 loại thuốc.
* Số lượng thuốc tăng 12% so với tháng trước.

Chức năng suy đoán:

* Bấm vào thẻ có thể lọc bảng về tất cả thuốc.
* Có thể dẫn đến báo cáo tổng hợp thuốc.

---

## 4.2 Thẻ “Thuốc còn hàng”

Nội dung:

* Icon hộp thuốc / túi y tế màu trắng trên nền xanh lá.
* Tiêu đề: **Thuốc còn hàng**
* Số liệu lớn: **186**
* Dòng so sánh: mũi tên tăng màu xanh, **8% so với tháng trước**

Ý nghĩa:

* Có 186 thuốc đang còn hàng.
* Tồn kho ổn định hoặc tăng so với tháng trước.

Chức năng suy đoán:

* Bấm vào thẻ sẽ lọc bảng theo trạng thái **Còn hàng**.
* Có thể hiển thị danh sách thuốc có số lượng lớn hơn ngưỡng an toàn.

---

## 4.3 Thẻ “Thuốc sắp hết”

Nội dung:

* Icon cảnh báo màu trắng trên nền cam.
* Tiêu đề: **Thuốc sắp hết**
* Số liệu lớn: **28**
* Dòng so sánh: mũi tên giảm màu đỏ, **5% so với tháng trước**

Ý nghĩa:

* Có 28 thuốc đang ở mức tồn kho thấp.
* Cần nhập thêm hàng sớm.
* Mũi tên giảm 5% có thể hiểu là số thuốc sắp hết đã giảm so với tháng trước, đây là tín hiệu tích cực.

Chức năng suy đoán:

* Bấm vào thẻ sẽ lọc bảng theo trạng thái **Sắp hết**.
* Có thể mở danh sách cảnh báo nhập kho.
* Có thể gửi thông báo cho quản lý kho.

---

## 4.4 Thẻ “Thuốc hết hàng”

Nội dung:

* Icon vòng cấm màu trắng trên nền tím.
* Tiêu đề: **Thuốc hết hàng**
* Số liệu lớn: **12**
* Dòng so sánh: mũi tên giảm màu đỏ, **3% so với tháng trước**

Ý nghĩa:

* Có 12 thuốc đã hết hàng.
* Cần nhập kho hoặc tạm ngưng kê đơn/bán thuốc.

Chức năng suy đoán:

* Bấm vào thẻ sẽ lọc bảng theo trạng thái **Hết hàng**.
* Có thể hiển thị cảnh báo nghiêm trọng.
* Có thể tự động đánh dấu thuốc không khả dụng trong hệ thống kê đơn.

---

# 5. Khu tìm kiếm, lọc và thao tác

Bên dưới các thẻ thống kê là khu thao tác với bảng dữ liệu.

Khu này nằm trong một khung trắng lớn, có bo góc, bóng nhẹ.

## 5.1 Ô tìm kiếm

Ở bên trái có ô tìm kiếm lớn.

Placeholder:

**Tìm kiếm thuốc (Tên thuốc, hoạt chất, mã thuốc...)**

Thành phần:

* Icon kính lúp bên trái.
* Input bo góc.
* Text placeholder màu xám.
* Chiều rộng khoảng 35–40% khu bảng.

Chức năng:

Người dùng có thể tìm thuốc theo:

* Tên thuốc
* Hoạt chất
* Mã thuốc
* Có thể mở rộng thêm tìm theo nhà cung cấp, danh mục, trạng thái

Hành vi nên có:

* Gõ từ khóa và tự động lọc sau 300–500ms.
* Hỗ trợ không phân biệt hoa thường.
* Hỗ trợ tiếng Việt có dấu và không dấu.
* Có nút clear khi nhập nội dung.
* Khi không có kết quả, hiển thị trạng thái rỗng: “Không tìm thấy thuốc phù hợp”.

---

## 5.2 Bộ lọc “Danh mục”

Label: **Danh mục**

Dropdown mặc định: **Tất cả**

Chức năng:

Lọc thuốc theo nhóm/danh mục, ví dụ:

* Giảm đau - Hạ sốt
* Kháng sinh
* Vitamin - Khoáng chất
* Dạ dày - Tiêu hóa
* Kháng dị ứng
* Tim mạch
* Hô hấp
* Giảm đau - Viêm

Hành vi:

* Khi chọn danh mục, bảng chỉ hiển thị thuốc thuộc danh mục đó.
* Có thể kết hợp với tìm kiếm và các bộ lọc khác.

---

## 5.3 Bộ lọc “Nhà cung cấp”

Label: **Nhà cung cấp**

Dropdown mặc định: **Tất cả**

Dữ liệu đang có trong bảng:

* Dược Hà Giang
* Traphaco
* Imexpharm
* Stella

Chức năng:

* Lọc thuốc theo nhà cung cấp.
* Hữu ích khi muốn kiểm tra tồn kho hoặc giá nhập của từng nhà cung cấp.

---

## 5.4 Bộ lọc “Trạng thái”

Label: **Trạng thái**

Dropdown mặc định: **Tất cả**

Các trạng thái có thể có:

* Còn hàng
* Sắp hết
* Hết hàng

Chức năng:

* Lọc nhanh theo tình trạng kho.
* Kết hợp với thống kê để quản lý nhập hàng.

---

## 5.5 Nút “Thêm thuốc”

Ở góc phải phía trên bảng có nút màu xanh lá:

**+ Thêm thuốc**

Thiết kế:

* Nền xanh lá.
* Icon dấu cộng.
* Text trắng.
* Bo góc.
* Kích thước nổi bật nhất trong khu thao tác.

Chức năng:

Mở form thêm thuốc mới.

Form thêm thuốc nên có các trường:

* Mã thuốc
* Tên thuốc
* Hoạt chất
* Danh mục
* Đơn vị tính
* Nhà cung cấp
* Số lượng tồn kho
* Ngưỡng cảnh báo sắp hết
* Giá nhập
* Giá bán
* Ngày sản xuất
* Hạn sử dụng
* Số lô
* Mô tả thuốc
* Cách dùng
* Chống chỉ định
* Ảnh thuốc nếu cần
* Trạng thái tự động hoặc chọn tay

Validation nên có:

* Tên thuốc bắt buộc.
* Số lượng phải là số không âm.
* Giá nhập và giá bán phải là số không âm.
* Giá bán nên lớn hơn hoặc bằng giá nhập.
* Hạn sử dụng phải sau ngày sản xuất.
* Không cho trùng mã thuốc.
* Cảnh báo nếu thuốc đã tồn tại tên hoặc hoạt chất giống.

---

## 5.6 Nút “Xuất Excel”

Bên dưới nút “Thêm thuốc” có nút:

**Xuất Excel**

Thiết kế:

* Nền trắng.
* Viền xám nhạt.
* Icon Excel màu xanh lá.
* Text màu xanh navy hoặc đen.

Chức năng:

Xuất danh sách thuốc ra file Excel.

Có thể xuất:

* Toàn bộ danh sách thuốc.
* Danh sách sau khi đã lọc.
* Các cột đang hiển thị.
* Có thể thêm ngày xuất báo cáo, người xuất, tổng số thuốc.

Nên có tùy chọn:

* Xuất tất cả
* Xuất theo bộ lọc hiện tại
* Xuất thuốc sắp hết
* Xuất thuốc hết hàng

---

# 6. Bảng danh sách thuốc

Bảng nằm bên dưới khu tìm kiếm/lọc. Bảng có nền trắng, đường kẻ hàng rất nhẹ, font nhỏ gọn nhưng rõ ràng.

## 6.1 Header bảng

Cột đầu tiên là checkbox chọn tất cả.

Các cột gồm:

1. Checkbox
2. **STT**
3. **Tên thuốc**
4. **Hoạt chất**
5. **Danh mục**
6. **Đơn vị tính**
7. **Nhà cung cấp**
8. **Số lượng**
9. **Giá nhập**
10. **Giá bán**
11. **Trạng thái**
12. **Thao tác**

Header có chữ màu xanh navy đậm, font 13–15px, in đậm.

## 6.2 Checkbox

Mỗi dòng có checkbox ở đầu.

Chức năng:

* Chọn một hoặc nhiều thuốc.
* Checkbox trên header dùng để chọn tất cả thuốc trên trang hiện tại.
* Khi có thuốc được chọn, nên hiện thanh thao tác hàng loạt:

  * Xóa nhiều thuốc
  * Cập nhật trạng thái
  * Xuất Excel các thuốc đã chọn
  * In danh sách
  * Gán danh mục
  * Cập nhật nhà cung cấp

---

# 7. Dữ liệu mẫu trong bảng

Bảng đang hiển thị 10 bản ghi trên trang đầu.

---

## Dòng 1

* STT: **1**
* Tên thuốc: **Paracetamol 500mg**
* Hoạt chất: **Paracetamol**
* Danh mục: **Giảm đau - Hạ sốt**
* Đơn vị tính: **Viên**
* Nhà cung cấp: **Dược Hà Giang**
* Số lượng: **1.250**
* Giá nhập: **850 đ**
* Giá bán: **1.200 đ**
* Trạng thái: **Còn hàng**
* Badge trạng thái: xanh lá nhạt, chữ xanh lá.

Ý nghĩa:

* Thuốc còn tồn kho nhiều.
* Có thể bán/kê đơn bình thường.

---

## Dòng 2

* STT: **2**
* Tên thuốc: **Amoxicillin 500mg**
* Hoạt chất: **Amoxicillin**
* Danh mục: **Kháng sinh**
* Đơn vị tính: **Viên**
* Nhà cung cấp: **Traphaco**
* Số lượng: **950**
* Giá nhập: **1.200 đ**
* Giá bán: **1.800 đ**
* Trạng thái: **Còn hàng**

---

## Dòng 3

* STT: **3**
* Tên thuốc: **Vitamin C 500mg**
* Hoạt chất: **Vitamin C**
* Danh mục: **Vitamin - Khoáng chất**
* Đơn vị tính: **Viên**
* Nhà cung cấp: **Imexpharm**
* Số lượng: **2.300**
* Giá nhập: **650 đ**
* Giá bán: **1.000 đ**
* Trạng thái: **Còn hàng**

---

## Dòng 4

* STT: **4**
* Tên thuốc: **Omeprazole 20mg**
* Hoạt chất: **Omeprazole**
* Danh mục: **Dạ dày - Tiêu hóa**
* Đơn vị tính: **Viên**
* Nhà cung cấp: **Dược Hà Giang**
* Số lượng: **320**
* Giá nhập: **1.100 đ**
* Giá bán: **1.600 đ**
* Trạng thái: **Sắp hết**
* Badge trạng thái: cam nhạt, chữ cam.

Ý nghĩa:

* Số lượng thuốc đã gần ngưỡng cảnh báo.
* Cần cân nhắc nhập thêm.

---

## Dòng 5

* STT: **5**
* Tên thuốc: **Loratadin 10mg**
* Hoạt chất: **Loratadin**
* Danh mục: **Kháng dị ứng**
* Đơn vị tính: **Viên**
* Nhà cung cấp: **Traphaco**
* Số lượng: **180**
* Giá nhập: **900 đ**
* Giá bán: **1.400 đ**
* Trạng thái: **Sắp hết**

---

## Dòng 6

* STT: **6**
* Tên thuốc: **Cetirizin 10mg**
* Hoạt chất: **Cetirizin**
* Danh mục: **Kháng dị ứng**
* Đơn vị tính: **Viên**
* Nhà cung cấp: **Imexpharm**
* Số lượng: **0**
* Giá nhập: **850 đ**
* Giá bán: **1.300 đ**
* Trạng thái: **Hết hàng**
* Badge trạng thái: đỏ nhạt, chữ đỏ.

Ý nghĩa:

* Thuốc không còn tồn kho.
* Không nên cho phép bán/kê đơn nếu hệ thống có liên kết với đơn thuốc.

---

## Dòng 7

* STT: **7**
* Tên thuốc: **Ibuprofen 400mg**
* Hoạt chất: **Ibuprofen**
* Danh mục: **Giảm đau - Viêm**
* Đơn vị tính: **Viên**
* Nhà cung cấp: **Stella**
* Số lượng: **760**
* Giá nhập: **950 đ**
* Giá bán: **1.500 đ**
* Trạng thái: **Còn hàng**

---

## Dòng 8

* STT: **8**
* Tên thuốc: **Aspirin 81 mg**
* Hoạt chất: **Aspirin**
* Danh mục: **Tim mạch**
* Đơn vị tính: **Viên**
* Nhà cung cấp: **Dược Hà Giang**
* Số lượng: **1.100**
* Giá nhập: **700 đ**
* Giá bán: **1.100 đ**
* Trạng thái: **Còn hàng**

---

## Dòng 9

* STT: **9**
* Tên thuốc: **Multivitamin**
* Hoạt chất: **Vitamin tổng hợp**
* Danh mục: **Vitamin - Khoáng chất**
* Đơn vị tính: **Viên**
* Nhà cung cấp: **Traphaco**
* Số lượng: **540**
* Giá nhập: **1.500 đ**
* Giá bán: **2.200 đ**
* Trạng thái: **Còn hàng**

---

## Dòng 10

* STT: **10**
* Tên thuốc: **Salbutamol 2mg**
* Hoạt chất: **Salbutamol**
* Danh mục: **Hô hấp**
* Đơn vị tính: **Viên**
* Nhà cung cấp: **Imexpharm**
* Số lượng: **150**
* Giá nhập: **1.000 đ**
* Giá bán: **1.600 đ**
* Trạng thái: **Sắp hết**

---

# 8. Cột trạng thái

Trạng thái được hiển thị dưới dạng badge nhỏ, bo góc, màu nền nhạt.

## 8.1 Còn hàng

* Nền xanh lá nhạt.
* Chữ xanh lá.
* Dùng cho thuốc có tồn kho ổn định.

Logic gợi ý:

```text
Nếu số lượng > ngưỡng sắp hết => Còn hàng
```

Ví dụ: số lượng trên 300 hoặc trên ngưỡng cấu hình.

## 8.2 Sắp hết

* Nền cam nhạt.
* Chữ cam.
* Dùng cho thuốc có số lượng thấp nhưng chưa bằng 0.

Logic gợi ý:

```text
Nếu 0 < số lượng <= ngưỡng sắp hết => Sắp hết
```

Ví dụ: số lượng còn dưới 300 viên.

## 8.3 Hết hàng

* Nền đỏ nhạt.
* Chữ đỏ.
* Dùng cho thuốc có số lượng bằng 0.

Logic gợi ý:

```text
Nếu số lượng = 0 => Hết hàng
```

---

# 9. Cột thao tác

Mỗi dòng có 3 icon thao tác nằm bên phải.

## 9.1 Icon xem chi tiết

Icon hình con mắt, màu xanh dương.

Chức năng:

* Mở modal hoặc trang chi tiết thuốc.
* Hiển thị toàn bộ thông tin thuốc:

  * Tên thuốc
  * Hoạt chất
  * Mã thuốc
  * Danh mục
  * Nhà cung cấp
  * Giá nhập
  * Giá bán
  * Tồn kho
  * Lịch sử nhập/xuất
  * Hạn sử dụng
  * Mô tả
  * Cảnh báo
  * Người tạo
  * Ngày cập nhật gần nhất

## 9.2 Icon chỉnh sửa

Icon cây bút, màu xanh dương.

Chức năng:

* Mở form sửa thuốc.
* Cho phép cập nhật:

  * Tên thuốc
  * Hoạt chất
  * Danh mục
  * Đơn vị tính
  * Nhà cung cấp
  * Giá nhập
  * Giá bán
  * Số lượng
  * Trạng thái
  * Hạn sử dụng
  * Mô tả

Nên ghi log thay đổi:

* Ai sửa
* Sửa lúc nào
* Trường nào thay đổi
* Giá trị cũ và mới

## 9.3 Icon xóa

Icon thùng rác, màu đỏ.

Chức năng:

* Xóa thuốc khỏi danh sách.
* Khi bấm cần hiện popup xác nhận:

```text
Bạn có chắc chắn muốn xóa thuốc này không?
Hành động này có thể ảnh hưởng đến lịch sử đơn thuốc và báo cáo kho.
```

Nên dùng xóa mềm thay vì xóa thật:

* Thuốc bị chuyển sang trạng thái “Ngừng sử dụng” hoặc “Đã xóa”.
* Vẫn giữ dữ liệu để phục vụ báo cáo, đơn thuốc cũ, lịch sử bán hàng.

---

# 10. Phân trang

Ở cuối bảng có khu phân trang.

Bên trái:

**Hiển thị [10 ▼] bản ghi**

Ý nghĩa:

* Người dùng đang xem 10 bản ghi mỗi trang.
* Dropdown có thể chọn:

  * 10
  * 20
  * 50
  * 100

Bên phải:

Các nút phân trang:

* Nút lùi
* Trang **1** đang active, nền xanh lá.
* Trang 2
* Trang 3
* Trang 4
* Trang 5
* Dấu …
* Trang 26
* Nút tiến

Ý nghĩa:

* Có tổng cộng 26 trang dữ liệu.
* Nếu mỗi trang hiển thị 10 bản ghi thì có khoảng 256 thuốc, trùng với thẻ “Tổng số thuốc”.

Hành vi:

* Click số trang để chuyển trang.
* Click mũi tên phải để sang trang tiếp.
* Click mũi tên trái để quay lại trang trước.
* Khi ở trang 1, nút lùi nên bị disable hoặc mờ.

---

# 11. Chức năng chính cần có trong màn hình này

## 11.1 Xem danh sách thuốc

Hiển thị danh sách thuốc theo dạng bảng với các thông tin quan trọng:

* Tên thuốc
* Hoạt chất
* Danh mục
* Đơn vị tính
* Nhà cung cấp
* Số lượng tồn
* Giá nhập
* Giá bán
* Trạng thái
* Thao tác

Mục tiêu là giúp admin kiểm soát kho thuốc nhanh chóng.

---

## 11.2 Tìm kiếm thuốc

Người dùng có thể nhập từ khóa để tìm nhanh.

Nên hỗ trợ tìm theo:

* Tên thuốc
* Hoạt chất
* Mã thuốc
* Danh mục
* Nhà cung cấp

Ví dụ:

* Gõ “para” → hiện Paracetamol.
* Gõ “kháng sinh” → hiện thuốc thuộc danh mục kháng sinh.
* Gõ “traphaco” → hiện thuốc của nhà cung cấp Traphaco.

---

## 11.3 Lọc thuốc

Có 3 bộ lọc chính:

* Lọc theo danh mục.
* Lọc theo nhà cung cấp.
* Lọc theo trạng thái.

Bộ lọc nên kết hợp được với nhau.

Ví dụ:

```text
Danh mục: Kháng dị ứng
Nhà cung cấp: Traphaco
Trạng thái: Sắp hết
```

Kết quả sẽ chỉ hiển thị thuốc kháng dị ứng của Traphaco đang sắp hết.

---

## 11.4 Thêm thuốc mới

Nút **Thêm thuốc** dùng để tạo mới thuốc.

Luồng xử lý:

1. Admin bấm “Thêm thuốc”.
2. Hệ thống mở modal hoặc trang form.
3. Admin nhập thông tin thuốc.
4. Bấm “Lưu”.
5. Hệ thống validate dữ liệu.
6. Nếu hợp lệ, lưu vào database.
7. Bảng cập nhật lại.
8. Thẻ thống kê cập nhật lại số liệu.

---

## 11.5 Xem chi tiết thuốc

Icon mắt dùng để xem thông tin đầy đủ của thuốc.

Nên có thêm các tab trong trang chi tiết:

* Thông tin chung
* Tồn kho
* Lịch sử nhập hàng
* Lịch sử xuất/bán
* Hạn sử dụng
* Nhà cung cấp
* Ghi chú

---

## 11.6 Chỉnh sửa thuốc

Icon bút dùng để sửa thông tin thuốc.

Các trường thường được sửa:

* Giá nhập
* Giá bán
* Số lượng
* Nhà cung cấp
* Danh mục
* Trạng thái
* Hạn sử dụng

Nên có xác nhận khi thay đổi thông tin quan trọng như giá bán hoặc số lượng tồn.

---

## 11.7 Xóa thuốc

Icon thùng rác dùng để xóa thuốc.

Nên có:

* Popup xác nhận.
* Không cho xóa thuốc đã từng nằm trong đơn thuốc/hóa đơn.
* Thay vào đó chuyển sang trạng thái “Ngừng kinh doanh” hoặc “Không hoạt động”.

---

## 11.8 Xuất Excel

Chức năng xuất danh sách thuốc.

File Excel nên có các cột:

* STT
* Mã thuốc
* Tên thuốc
* Hoạt chất
* Danh mục
* Đơn vị tính
* Nhà cung cấp
* Số lượng
* Giá nhập
* Giá bán
* Lợi nhuận dự kiến
* Trạng thái
* Ngày tạo
* Ngày cập nhật
* Hạn sử dụng

---

## 11.9 Cảnh báo tồn kho

Hệ thống nên tự động cảnh báo:

* Thuốc sắp hết.
* Thuốc hết hàng.
* Thuốc gần hết hạn.
* Thuốc đã hết hạn.
* Thuốc có giá bán thấp hơn giá nhập.
* Thuốc tồn kho quá lâu không xuất.

Các cảnh báo có thể hiển thị ở icon chuông góc phải.

---

## 11.10 Quản lý nhập/xuất kho

Mặc dù màn hình này chưa hiển thị trực tiếp, nhưng nên có chức năng liên quan:

* Nhập thêm thuốc.
* Xuất thuốc.
* Điều chỉnh tồn kho.
* Ghi nhận lý do điều chỉnh.
* Theo dõi số lô.
* Theo dõi hạn sử dụng.
* Lịch sử nhập xuất theo từng thuốc.

---

# 12. Gợi ý cấu trúc dữ liệu thuốc

Một đối tượng thuốc có thể gồm:

```json
{
  "id": 1,
  "maThuoc": "TH001",
  "tenThuoc": "Paracetamol 500mg",
  "hoatChat": "Paracetamol",
  "danhMuc": "Giảm đau - Hạ sốt",
  "donViTinh": "Viên",
  "nhaCungCap": "Dược Hà Giang",
  "soLuong": 1250,
  "nguongCanhBao": 300,
  "giaNhap": 850,
  "giaBan": 1200,
  "trangThai": "Còn hàng",
  "ngaySanXuat": "2025-01-15",
  "hanSuDung": "2027-01-15",
  "soLo": "LO20250115",
  "moTa": "Thuốc giảm đau, hạ sốt",
  "createdAt": "2026-05-01",
  "updatedAt": "2026-05-11"
}
```

---

# 13. Quy tắc tính trạng thái thuốc

Có thể tự động tính trạng thái theo số lượng:

```text
Nếu số lượng = 0:
    Hết hàng

Nếu số lượng > 0 và số lượng <= ngưỡng cảnh báo:
    Sắp hết

Nếu số lượng > ngưỡng cảnh báo:
    Còn hàng
```

Ví dụ:

```text
Ngưỡng cảnh báo = 300

Cetirizin 10mg có số lượng 0 → Hết hàng
Loratadin 10mg có số lượng 180 → Sắp hết
Paracetamol 500mg có số lượng 1.250 → Còn hàng
```

---

# 14. Màu sắc giao diện

## Màu chủ đạo

* Xanh lá thương hiệu: dùng cho logo, menu active, nút thêm thuốc, trang active.
* Xanh navy đậm: dùng cho tiêu đề, text chính.
* Xám xanh: dùng cho text phụ, breadcrumb, label.
* Nền trắng/xám rất nhạt.

## Màu trạng thái

* **Còn hàng**: xanh lá.
* **Sắp hết**: cam.
* **Hết hàng**: đỏ.
* **Tổng số thuốc**: xanh dương.
* **Thuốc hết hàng**: tím.

---

# 15. Style UI chi tiết

## 15.1 Card thống kê

Mỗi card có:

* Nền trắng.
* Bo góc khoảng 16–20px.
* Shadow nhẹ.
* Padding khoảng 24px.
* Icon bên trái.
* Nội dung bên phải hoặc căn trong card.
* Số liệu lớn, nổi bật.
* Dòng phần trăm nhỏ bên dưới.

## 15.2 Bảng

Bảng có:

* Header rõ ràng.
* Hàng cao khoảng 48–56px.
* Đường kẻ ngang mờ.
* Text căn trái cho tên thuốc, hoạt chất, danh mục.
* Text căn phải hoặc giữa cho số lượng, giá nhập, giá bán.
* Badge trạng thái nằm giữa cột trạng thái.
* Icon thao tác nhỏ, đặt trong button nền nhạt.

## 15.3 Button

Nút chính:

* Nền xanh lá.
* Chữ trắng.
* Icon trắng.
* Hover đậm hơn.

Nút phụ:

* Nền trắng.
* Viền xám.
* Icon xanh.
* Hover nền xám nhạt.

Nút nguy hiểm:

* Màu đỏ.
* Dùng cho xóa thuốc hoặc đăng xuất.

---

# 16. Responsive

Khi màn hình nhỏ hơn:

## Tablet

* Sidebar có thể thu gọn chỉ còn icon.
* Card thống kê chuyển thành 2 cột.
* Bộ lọc có thể xuống dòng.
* Bảng có scroll ngang.

## Mobile

* Sidebar ẩn sau nút hamburger.
* Card thống kê xếp 1 cột.
* Tìm kiếm và filter xếp dọc.
* Bảng có thể chuyển sang dạng card list:

  * Tên thuốc
  * Hoạt chất
  * Số lượng
  * Trạng thái
  * Nút xem/sửa/xóa

---

# 17. Các trạng thái màn hình cần thiết

## 17.1 Loading

Khi đang tải dữ liệu:

* Hiển thị skeleton cho card thống kê.
* Skeleton row cho bảng.
* Disable các nút thao tác.

## 17.2 Không có dữ liệu

Khi chưa có thuốc:

```text
Chưa có thuốc nào trong hệ thống.
Bấm “Thêm thuốc” để tạo thuốc mới.
```

## 17.3 Không tìm thấy kết quả

Khi search/filter không có kết quả:

```text
Không tìm thấy thuốc phù hợp với bộ lọc hiện tại.
```

Có nút:

```text
Xóa bộ lọc
```

## 17.4 Lỗi tải dữ liệu

Khi API lỗi:

```text
Không thể tải danh sách thuốc. Vui lòng thử lại.
```

Có nút:

```text
Thử lại
```

---

# 18. API cần có

Một dev backend có thể cần các API sau:

```text
GET /api/medicines
```

Lấy danh sách thuốc, hỗ trợ query:

```text
?page=1
&limit=10
&search=para
&category=Kháng sinh
&supplier=Traphaco
&status=Còn hàng
```

```text
GET /api/medicines/stats
```

Lấy thống kê:

* tổng số thuốc
* thuốc còn hàng
* thuốc sắp hết
* thuốc hết hàng
* phần trăm tăng/giảm so với tháng trước

```text
POST /api/medicines
```

Thêm thuốc.

```text
GET /api/medicines/:id
```

Xem chi tiết thuốc.

```text
PUT /api/medicines/:id
```

Cập nhật thuốc.

```text
DELETE /api/medicines/:id
```

Xóa hoặc vô hiệu hóa thuốc.

```text
GET /api/medicines/export
```

Xuất Excel.

```text
GET /api/categories
```

Lấy danh mục thuốc.

```text
GET /api/suppliers
```

Lấy nhà cung cấp.

---

# 19. Quyền người dùng

Vì đây là trang admin, nên nên có phân quyền.

## Admin

Có toàn quyền:

* Xem thuốc
* Thêm thuốc
* Sửa thuốc
* Xóa thuốc
* Xuất Excel
* Xem báo cáo
* Quản lý nhà cung cấp

## Nhân viên kho

Có thể:

* Xem thuốc
* Cập nhật số lượng
* Nhập/xuất kho
* Xuất Excel

Không nên được:

* Xóa thuốc
* Phân quyền hệ thống

## Bác sĩ

Có thể:

* Xem thuốc còn hàng
* Tìm thuốc khi kê đơn

Không nên được:

* Sửa giá
* Xóa thuốc
* Thay đổi tồn kho

---

# 20. Mô tả ngắn để đưa vào tài liệu thiết kế

Giao diện “Quản lý thuốc” của CarePlus Admin là màn hình quản trị kho thuốc, cho phép admin theo dõi tổng số thuốc, thuốc còn hàng, thuốc sắp hết và thuốc hết hàng thông qua các thẻ thống kê nhanh. Bên dưới là khu tìm kiếm và lọc theo danh mục, nhà cung cấp, trạng thái. Danh sách thuốc được hiển thị dưới dạng bảng gồm tên thuốc, hoạt chất, danh mục, đơn vị tính, nhà cung cấp, số lượng, giá nhập, giá bán, trạng thái và các thao tác xem, sửa, xóa. Màn hình hỗ trợ thêm thuốc mới, xuất Excel, chọn nhiều bản ghi, phân trang và cảnh báo tồn kho. Giao diện sử dụng màu xanh lá làm màu chủ đạo, nền sáng, card bo góc, icon rõ ràng, phù hợp cho hệ thống quản trị y tế/phòng khám.
