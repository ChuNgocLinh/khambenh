Dưới đây là mô tả chi tiết giao diện **CarePlus Admin – Quản lý thanh toán**, đủ để đưa cho designer/dev làm lại theo.

---

# 1. Tổng quan màn hình

Đây là màn hình quản trị dành cho admin hệ thống y tế/phòng khám, nằm trong module **Quản lý thanh toán**. Giao diện dùng để theo dõi, lọc, thêm mới, xuất Excel và thao tác với các giao dịch thanh toán của bệnh nhân.

Phong cách thiết kế: **dashboard quản trị hiện đại**, nền sáng, nhiều khoảng trắng, bo góc mềm, màu chủ đạo là **xanh lá CarePlus**, kết hợp với xanh dương, cam, tím, đỏ để biểu thị trạng thái thanh toán.

Màn hình chia thành 2 phần chính:

* **Sidebar bên trái**: menu điều hướng toàn hệ thống.
* **Khu vực nội dung bên phải**: tiêu đề trang, thẻ thống kê, bộ lọc, bảng danh sách thanh toán.

---

# 2. Sidebar bên trái

Sidebar nằm cố định bên trái, nền trắng, rộng khoảng **250–280px**, cao full màn hình.

## Logo

Phía trên cùng là logo:

* Icon dấu cộng màu xanh trong hình tròn.
* Text: **CarePlus Admin**
* Chữ “CarePlus” màu xanh lá, “Admin” màu xanh đậm hoặc xanh lá đậm.
* Font đậm, cỡ khoảng 20–22px.

## Menu điều hướng

Các mục menu được xếp dọc, mỗi dòng gồm:

* Icon bên trái.
* Tên chức năng bên phải.
* Khoảng cách giữa các mục khá thoáng.
* Icon màu xanh đen/xám đậm khi chưa active.

Các mục menu gồm:

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

Mục đang được chọn là **Quản lý thanh toán**.

## Trạng thái active của menu

Mục **Quản lý thanh toán** có:

* Nền xanh lá nhạt.
* Bo góc khoảng 8–12px.
* Icon và chữ màu xanh lá đậm.
* Tạo cảm giác đang ở module hiện tại.

## Nút đăng xuất

Ở cuối sidebar có nút **Đăng xuất**:

* Nền đỏ rất nhạt.
* Icon logout màu đỏ.
* Text “Đăng xuất” màu đỏ.
* Bo góc mềm.
* Nằm sát đáy sidebar, tách biệt khỏi nhóm menu chính.

Chức năng suy đoán: khi bấm sẽ mở popup xác nhận đăng xuất, ví dụ: “Bạn có chắc chắn muốn đăng xuất không?”

---

# 3. Header khu vực nội dung

Bên phải sidebar là vùng nội dung chính, nền gần trắng/xám rất nhạt.

Ở góc trên trái của vùng nội dung có tiêu đề:

## Tiêu đề trang

Text lớn:

**Quản lý thanh toán**

* Font đậm.
* Màu xanh navy đậm.
* Cỡ chữ khoảng 28–32px.

Bên dưới là breadcrumb:

**Dashboard / Quản lý thanh toán**

* “Dashboard” màu xanh xám.
* Dấu `/`.
* “Quản lý thanh toán” màu xanh xám hoặc đậm hơn một chút.

## Góc trên phải

Có cụm thông tin admin gồm:

### Icon chuông thông báo

* Icon chuông outline.
* Có badge đỏ nhỏ ở góc trên phải.
* Badge hiển thị số **3**.
* Suy đoán chức năng: bấm vào để xem thông báo như giao dịch mới, thanh toán thất bại, khoản chờ xác nhận.

### Avatar admin

* Avatar hình người dạng minh họa.
* Bên phải avatar là text: **Admin (Quản trị viên)**
* Có icon mũi tên xuống.
* Suy đoán chức năng: mở dropdown gồm Hồ sơ cá nhân, Đổi mật khẩu, Cài đặt, Đăng xuất.

---

# 4. Khu thẻ thống kê thanh toán

Ngay dưới tiêu đề là 4 thẻ thống kê nằm ngang, mỗi thẻ chiếm khoảng 1/4 chiều rộng vùng nội dung.

Các thẻ có:

* Nền trắng.
* Border xám nhạt.
* Bo góc khoảng 14–18px.
* Padding rộng.
* Có icon lớn bên trái.
* Bên phải là label và số tiền.
* Bên dưới có phần so sánh với tháng trước.

## Thẻ 1: Tổng thanh toán

Nội dung:

* Icon ví tiền màu xanh dương, nằm trong ô vuông bo góc.
* Label: **Tổng thanh toán**
* Số tiền: **152.450.000 đ**
* Dòng tăng trưởng: mũi tên lên màu xanh, **18% so với tháng trước**

Ý nghĩa: tổng số tiền phát sinh trong khoảng thời gian đang lọc hoặc trong tháng hiện tại.

## Thẻ 2: Thanh toán thành công

Nội dung:

* Icon dấu check màu trắng trên nền xanh lá.
* Label: **Thanh toán thành công**
* Số tiền: **128.650.000 đ**
* Dòng tăng trưởng: mũi tên lên màu xanh, **16% so với tháng trước**

Ý nghĩa: tổng tiền các giao dịch có trạng thái thành công.

## Thẻ 3: Đang chờ thanh toán

Nội dung:

* Icon đồng hồ màu trắng trên nền cam.
* Label: **Đang chờ thanh toán**
* Số tiền: **18.200.000 đ**
* Dòng so sánh: mũi tên xuống màu đỏ, **5% so với tháng trước**

Ý nghĩa: tổng tiền các giao dịch chưa hoàn tất, đang chờ bệnh nhân thanh toán hoặc chờ xác nhận.

## Thẻ 4: Thanh toán thất bại

Nội dung:

* Icon dấu X màu trắng trên nền tím.
* Label: **Thanh toán thất bại**
* Số tiền: **5.600.000 đ**
* Dòng so sánh: mũi tên xuống màu đỏ, **2% so với tháng trước**

Ý nghĩa: tổng tiền của các giao dịch thất bại.

---

# 5. Khu bộ lọc và hành động

Bên dưới thẻ thống kê là một khối card lớn chứa:

* Thanh tìm kiếm.
* Bộ lọc ngày.
* Bộ lọc phương thức.
* Bộ lọc trạng thái.
* Nút thêm thanh toán.
* Nút xuất Excel.
* Bảng dữ liệu.

Card này có nền trắng, bo góc mềm, border rất nhạt.

## Thanh tìm kiếm

Nằm bên trái, chiếm khoảng 30–35% chiều rộng.

Placeholder:

**Tìm kiếm (Mã giao dịch, tên bệnh nhân, dịch vụ...)**

Có icon kính lúp ở đầu input.

Chức năng suy đoán:

* Tìm theo mã giao dịch.
* Tìm theo tên bệnh nhân.
* Tìm theo mã bệnh nhân.
* Tìm theo tên dịch vụ hoặc thuốc.
* Có thể debounce khi nhập, ví dụ 300–500ms.
* Có thể hỗ trợ tìm không dấu tiếng Việt.

## Bộ lọc từ ngày

Label: **Từ ngày**

Input ngày hiển thị:

**01/05/2026**

Có icon lịch ở bên phải input.

Chức năng:

* Bấm vào mở date picker.
* Không cho chọn ngày bắt đầu lớn hơn ngày kết thúc.
* Định dạng ngày: `dd/mm/yyyy`.

## Bộ lọc đến ngày

Label: **Đến ngày**

Input ngày hiển thị:

**24/05/2026**

Có icon lịch.

Chức năng tương tự bộ lọc từ ngày.

## Bộ lọc phương thức

Label: **Phương thức**

Dropdown đang chọn:

**Tất cả**

Các giá trị có thể có:

* Tất cả
* Tiền mặt
* Chuyển khoản
* Thẻ ngân hàng
* Ví điện tử, nếu hệ thống có hỗ trợ

## Bộ lọc trạng thái

Label: **Trạng thái**

Dropdown đang chọn:

**Tất cả**

Các giá trị có thể có:

* Tất cả
* Thành công
* Đang chờ
* Thất bại
* Đã hoàn tiền
* Đã hủy, nếu có nghiệp vụ hủy thanh toán

## Nút “Thêm thanh toán”

Nằm bên phải, nút chính màu xanh lá.

Text:

**+ Thêm thanh toán**

Thiết kế:

* Nền xanh lá đậm.
* Chữ trắng.
* Icon dấu cộng.
* Bo góc 8–10px.
* Cao khoảng 40–44px.

Chức năng suy đoán:

Khi bấm mở modal hoặc chuyển sang trang tạo thanh toán mới. Form có thể gồm:

* Chọn bệnh nhân.
* Chọn dịch vụ/thuốc/hóa đơn.
* Số tiền.
* Phương thức thanh toán.
* Ngày thanh toán.
* Trạng thái.
* Ghi chú.
* Người thu tiền.
* Mã giao dịch tự sinh.

## Nút “Xuất Excel”

Nằm dưới hoặc cạnh nút thêm thanh toán, màu trắng.

Text:

**Xuất Excel**

Có icon Excel màu xanh.

Thiết kế:

* Nền trắng.
* Border xám nhạt.
* Chữ xanh đậm.
* Icon Excel bên trái.
* Bo góc nhẹ.

Chức năng suy đoán:

* Xuất danh sách đang lọc ra file Excel.
* Nếu có bộ lọc ngày/trạng thái/phương thức thì file Excel chỉ chứa dữ liệu theo bộ lọc hiện tại.
* File có thể đặt tên dạng: `danh-sach-thanh-toan-2026-05-24.xlsx`.

---

# 6. Bảng danh sách thanh toán

Bảng nằm dưới bộ lọc, chiếm toàn bộ chiều rộng card.

## Header bảng

Header có nền trắng hoặc xám rất nhạt. Các cột gồm:

1. Checkbox chọn tất cả
2. **STT**
3. **Mã giao dịch**
4. **Bệnh nhân**
5. **Dịch vụ/Thuốc**
6. **Phương thức**
7. **Số tiền**
8. **Ngày thanh toán**
9. **Trạng thái**
10. **Thao tác**

Text header màu xanh navy đậm, font đậm.

Các hàng có đường kẻ ngang rất nhạt để phân tách.

## Checkbox

Mỗi dòng có checkbox ở cột đầu.

Chức năng suy đoán:

* Chọn từng giao dịch.
* Checkbox ở header chọn tất cả giao dịch trên trang hiện tại.
* Khi chọn nhiều dòng có thể hiện thanh thao tác hàng loạt như: xuất, xóa, cập nhật trạng thái, in hóa đơn.

---

# 7. Dữ liệu từng dòng trong bảng

## Cột STT

Hiển thị số thứ tự từ 1 đến 10 trên trang hiện tại.

## Cột mã giao dịch

Dạng mã:

* **GD250524-0001**
* **GD250524-0002**
* …
* **GD250524-0010**

Quy luật có thể hiểu là:

`GD + ngày tháng năm + số thứ tự`

Ví dụ:

`GD250524-0001` có thể là giao dịch ngày 25/05/2024 hoặc hệ thống đang dùng format nội bộ. Tuy nhiên trong bảng ngày thanh toán là 24/05/2026, nên mã có thể chỉ là dữ liệu mẫu.

Chức năng: bấm vào mã giao dịch có thể mở chi tiết giao dịch.

## Cột bệnh nhân

Mỗi bệnh nhân hiển thị gồm:

* Avatar nhỏ hình người.
* Tên bệnh nhân.
* Mã bệnh nhân bên dưới.

Ví dụ:

1. **Nguyễn Văn Nam**
   BN001

2. **Trần Thị Mai**
   BN002

3. **Lê Văn Cường**
   BN003

4. **Phạm Thị Lan**
   BN004

5. **Hoàng Anh Tuấn**
   BN005

6. **Vũ Thị Hương**
   BN006

7. **Đỗ Minh Quân**
   BN007

8. **Nguyễn Thị Hoa**
   BN008

9. **Bùi Văn Dũng**
   BN009

10. **Trương Thị Kiều**
    BN010

Tên bệnh nhân dùng màu xanh navy, mã bệnh nhân nhỏ hơn, màu xanh xám.

## Cột dịch vụ/thuốc

Hiển thị tên dịch vụ hoặc thuốc được thanh toán.

Các ví dụ trong ảnh:

* Khám tổng quát
* Khám tim mạch
* Xét nghiệm máu
* Siêu âm ổ bụng
* Thuốc điều trị
* Vật lý trị liệu
* Chụp X-Quang
* Khám sản phụ khoa
* Điện tâm đồ ECG
* Xét nghiệm nước tiểu

Chức năng suy đoán:

* Một giao dịch có thể liên kết với một dịch vụ, một đơn thuốc hoặc một hóa đơn tổng hợp.
* Nếu có nhiều dịch vụ, có thể hiển thị “3 dịch vụ” và bấm xem chi tiết.

## Cột phương thức

Hiển thị bằng badge nhỏ, bo góc.

Có 3 loại trong ảnh:

### Tiền mặt

* Nền xanh lá rất nhạt.
* Chữ xanh lá.

### Chuyển khoản

* Nền xanh dương rất nhạt.
* Chữ xanh dương.

### Thẻ ngân hàng

* Nền tím rất nhạt.
* Chữ tím.

Chức năng suy đoán:

* Dùng để phân biệt nguồn tiền.
* Có thể dùng trong báo cáo doanh thu theo phương thức thanh toán.

## Cột số tiền

Hiển thị định dạng tiền Việt Nam:

* 150.000 đ
* 200.000 đ
* 350.000 đ
* 250.000 đ
* 320.000 đ
* 180.000 đ
* 200.000 đ
* 300.000 đ
* 120.000 đ
* 100.000 đ

Quy chuẩn hiển thị:

* Dùng dấu chấm phân tách hàng nghìn.
* Ký hiệu tiền tệ là `đ`.
* Căn trái hoặc căn gần giữa tùy thiết kế, trong ảnh đang căn trái theo cột.

## Cột ngày thanh toán

Định dạng:

`dd/mm/yyyy hh:mm`

Ví dụ:

* 24/05/2026 09:15
* 24/05/2026 09:30
* 24/05/2026 10:00
* 24/05/2026 10:30
* 24/05/2026 11:00
* 24/05/2026 11:30
* 24/05/2026 12:00
* 24/05/2026 12:30
* 24/05/2026 13:00
* 24/05/2026 13:30

## Cột trạng thái

Hiển thị badge màu theo trạng thái.

### Thành công

* Nền xanh lá nhạt.
* Chữ xanh lá.
* Text: **Thành công**

### Đang chờ

* Nền cam nhạt.
* Chữ cam.
* Text: **Đang chờ**

### Thất bại

* Nền đỏ nhạt.
* Chữ đỏ.
* Text: **Thất bại**

Chức năng suy đoán:

* Thành công: đã ghi nhận tiền.
* Đang chờ: chưa hoàn tất, cần xác nhận hoặc bệnh nhân chưa thanh toán.
* Thất bại: giao dịch lỗi, chuyển khoản không thành công, thẻ bị từ chối, hoặc giao dịch bị hủy.

## Cột thao tác

Mỗi dòng có 3 nút icon:

### Icon mắt

Chức năng: xem chi tiết giao dịch.

Khi bấm có thể mở modal gồm:

* Mã giao dịch.
* Thông tin bệnh nhân.
* Dịch vụ/thuốc.
* Số tiền.
* Phương thức.
* Trạng thái.
* Ngày thanh toán.
* Người tạo.
* Ghi chú.
* Lịch sử cập nhật.

### Icon máy in

Chức năng: in hóa đơn hoặc phiếu thu.

Có thể mở bản preview hóa đơn trước khi in.

### Icon ba chấm

Chức năng: mở menu thao tác phụ.

Menu có thể gồm:

* Chỉnh sửa thanh toán.
* Cập nhật trạng thái.
* Hoàn tiền.
* Gửi hóa đơn qua email.
* Tải hóa đơn PDF.
* Xóa giao dịch.
* Xem lịch sử thay đổi.

---

# 8. Phân trang

Cuối bảng có khu phân trang.

Bên trái:

**Hiển thị [10 ▼] bản ghi**

Dropdown cho phép chọn số dòng mỗi trang.

Các lựa chọn có thể có:

* 10
* 20
* 50
* 100

Ở giữa/phải có pagination:

* Nút quay lại.
* Trang **1** đang active, nền xanh lá.
* Các trang 2, 3, 4, 5.
* Dấu `...`
* Trang 32.
* Nút tiếp theo.

Chức năng:

* Chuyển trang danh sách thanh toán.
* Khi thay đổi bộ lọc, nên reset về trang 1.
* Nếu đang ở trang đầu thì nút quay lại có thể disabled.
* Nếu ở trang cuối thì nút tiếp theo disabled.

---

# 9. Luồng chức năng chính nên có

## Xem danh sách thanh toán

Admin vào màn hình sẽ thấy danh sách giao dịch mới nhất, mặc định có thể lọc theo tháng hiện tại.

Thông tin cần hiển thị:

* Mã giao dịch.
* Bệnh nhân.
* Dịch vụ/thuốc.
* Phương thức thanh toán.
* Số tiền.
* Ngày thanh toán.
* Trạng thái.
* Các thao tác.

## Tìm kiếm giao dịch

Admin có thể nhập:

* Mã giao dịch.
* Tên bệnh nhân.
* Mã bệnh nhân.
* Tên dịch vụ.
* Tên thuốc.

Kết quả cập nhật theo từ khóa.

Nên hỗ trợ:

* Tìm không phân biệt hoa thường.
* Tìm tiếng Việt có dấu hoặc không dấu.
* Hiển thị trạng thái “Không tìm thấy giao dịch phù hợp” nếu không có kết quả.

## Lọc giao dịch

Có thể lọc theo:

* Từ ngày.
* Đến ngày.
* Phương thức thanh toán.
* Trạng thái.

Nên có thêm nút “Đặt lại” nếu làm thực tế, để xóa toàn bộ bộ lọc.

## Thêm thanh toán

Khi bấm **Thêm thanh toán**, mở form.

Các trường nên có:

* Bệnh nhân.
* Dịch vụ hoặc hóa đơn cần thanh toán.
* Số tiền.
* Phương thức thanh toán.
* Trạng thái.
* Ngày thanh toán.
* Mã giao dịch.
* Ghi chú.
* File đính kèm chứng từ, nếu là chuyển khoản.

Validation:

* Không được bỏ trống bệnh nhân.
* Số tiền phải lớn hơn 0.
* Ngày thanh toán không được sai định dạng.
* Phương thức thanh toán bắt buộc chọn.
* Nếu phương thức là chuyển khoản/thẻ ngân hàng, có thể yêu cầu mã tham chiếu giao dịch.

## Xem chi tiết thanh toán

Khi bấm icon mắt, hiển thị đầy đủ thông tin giao dịch.

Có thể chia modal thành các nhóm:

* Thông tin giao dịch.
* Thông tin bệnh nhân.
* Chi tiết dịch vụ/thuốc.
* Thanh toán.
* Lịch sử xử lý.

## In hóa đơn

Khi bấm icon máy in:

* Mở hóa đơn dạng preview.
* Có nút In.
* Có nút Tải PDF.
* Hóa đơn nên có mã QR hoặc mã giao dịch.
* Có thông tin phòng khám, bệnh nhân, dịch vụ, tổng tiền, ngày thanh toán.

## Xuất Excel

Khi bấm **Xuất Excel**:

* Xuất dữ liệu theo bộ lọc hiện tại.
* Có thể xuất các cột giống bảng.
* Có thêm tổng tiền cuối file.
* Có thể thêm sheet thống kê theo phương thức hoặc trạng thái.

## Cập nhật trạng thái

Từ menu ba chấm có thể cập nhật:

* Đang chờ → Thành công.
* Đang chờ → Thất bại.
* Thành công → Hoàn tiền.
* Thất bại → Tạo lại thanh toán.

Nên có xác nhận trước khi đổi trạng thái quan trọng.

---

# 10. Các trạng thái giao diện nên thiết kế thêm

## Loading

Khi tải dữ liệu:

* Hiển thị skeleton table.
* Các card thống kê cũng có skeleton.
* Không để màn hình trắng.

## Empty state

Khi không có giao dịch:

Text gợi ý:

**Chưa có thanh toán nào**

Mô tả:

**Không tìm thấy giao dịch phù hợp với bộ lọc hiện tại.**

Có thể có nút:

**Thêm thanh toán**

## Error state

Khi lỗi API:

Text:

**Không thể tải danh sách thanh toán**

Có nút:

**Thử lại**

## Không có quyền

Nếu tài khoản không có quyền quản lý thanh toán:

Text:

**Bạn không có quyền truy cập chức năng này.**

---

# 11. Quy tắc màu sắc gợi ý

Có thể dùng bảng màu gần như sau:

* Xanh lá thương hiệu: `#16A34A` hoặc `#18A957`
* Xanh lá nhạt active menu: `#E8F7EE`
* Xanh navy text chính: `#111B45`
* Xám phụ: `#6B7280`
* Border nhạt: `#E5EAF2`
* Nền trang: `#F8FAFC`
* Xanh dương thống kê: `#2563EB`
* Cam cảnh báo: `#F97316`
* Đỏ lỗi: `#EF4444`
* Tím thất bại/card: `#6D28D9`

---

# 12. Quy tắc typography

Gợi ý font:

* Inter
* Roboto
* SF Pro
* Be Vietnam Pro

Cỡ chữ:

* Tiêu đề trang: 28–32px, bold.
* Breadcrumb: 14–15px.
* Label card: 15–16px, semibold.
* Số tiền card: 24–28px, bold.
* Header bảng: 13–14px, semibold.
* Nội dung bảng: 13–14px.
* Mã bệnh nhân: 12px.
* Badge: 12px, semibold.

---

# 13. Cấu trúc dữ liệu gợi ý

Một bản ghi thanh toán có thể có dạng:

```json
{
  "id": "payment_001",
  "transactionCode": "GD250524-0001",
  "patient": {
    "id": "BN001",
    "name": "Nguyễn Văn Nam",
    "avatar": "/avatars/patient-1.png"
  },
  "itemName": "Khám tổng quát",
  "itemType": "service",
  "paymentMethod": "cash",
  "amount": 150000,
  "paidAt": "2026-05-24T09:15:00",
  "status": "success",
  "createdBy": "Admin",
  "note": ""
}
```

Các enum nên có:

```json
{
  "paymentMethod": ["cash", "bank_transfer", "bank_card"],
  "status": ["success", "pending", "failed", "refunded", "cancelled"]
}
```

---

# 14. Mô tả ngắn gọn để đưa cho dev/designer

Thiết kế một màn hình admin tên **Quản lý thanh toán** cho hệ thống CarePlus. Bên trái là sidebar cố định gồm logo CarePlus Admin, các mục quản trị như Dashboard, tài khoản, bác sĩ, bệnh nhân, thuốc, dịch vụ, thanh toán, báo cáo, phân quyền, sao lưu, và nút đăng xuất ở cuối. Mục **Quản lý thanh toán** đang active với nền xanh lá nhạt.

Khu vực chính có tiêu đề **Quản lý thanh toán**, breadcrumb **Dashboard / Quản lý thanh toán**, góc phải có chuông thông báo badge số 3, avatar và dropdown admin. Bên dưới là 4 card thống kê: tổng thanh toán, thanh toán thành công, đang chờ thanh toán, thanh toán thất bại. Mỗi card có icon màu riêng, số tiền lớn và phần trăm so với tháng trước.

Phần nội dung chính là card bảng dữ liệu. Trên bảng có ô tìm kiếm, bộ lọc từ ngày, đến ngày, phương thức, trạng thái, nút **Thêm thanh toán** màu xanh và nút **Xuất Excel**. Bảng gồm checkbox, STT, mã giao dịch, bệnh nhân, dịch vụ/thuốc, phương thức, số tiền, ngày thanh toán, trạng thái, thao tác. Mỗi dòng có avatar bệnh nhân, badge phương thức, badge trạng thái, và các nút xem chi tiết, in hóa đơn, menu mở rộng. Cuối bảng có chọn số bản ghi mỗi trang và phân trang.

Giao diện cần sạch, hiện đại, bo góc mềm, màu chủ đạo xanh lá, nền sáng, phù hợp hệ thống quản trị y tế.
