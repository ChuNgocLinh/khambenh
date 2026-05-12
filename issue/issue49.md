Dưới đây là mô tả chi tiết để người khác có thể dựng lại giao diện này gần như đầy đủ.

# 1. Tổng quan màn hình

Đây là màn hình **Phân quyền hệ thống** trong trang quản trị **CarePlus Admin**, dùng để quản lý vai trò người dùng và các quyền truy cập trong hệ thống y tế/phòng khám.

Màn hình thuộc nhóm chức năng quản trị cấp cao, dành cho tài khoản **Admin / Quản trị viên**. Giao diện đang hiển thị tab **Quản lý vai trò**, trong đó người dùng có thể xem danh sách vai trò, chọn một vai trò cụ thể và xem toàn bộ quyền mà vai trò đó đang được cấp.

Bố cục tổng thể gồm:

1. **Sidebar bên trái**: menu điều hướng chính của hệ thống.
2. **Header khu vực nội dung**: tiêu đề trang, breadcrumb, chuông thông báo, thông tin tài khoản.
3. **Khu vực thống kê nhanh**: 4 thẻ số liệu tổng quan.
4. **Thanh tab và hành động**: chuyển giữa quản lý vai trò / người dùng, nút thêm vai trò, nút cấu hình quyền.
5. **Nội dung chính dạng 2 cột**:

   * Cột trái: danh sách vai trò.
   * Cột phải: danh sách quyền của vai trò đang được chọn.
6. **Phân trang và chọn số dòng hiển thị** ở cuối từng khối.

---

# 2. Sidebar bên trái

Sidebar cố định bên trái, rộng khoảng **270px**, nền trắng hoặc xám rất nhạt. Chiều cao full viewport.

## Logo

Phía trên cùng có logo:

* Icon dấu cộng màu xanh trong hình tròn.
* Text: **CarePlus Admin**
* Màu chữ xanh lá.
* Font đậm, kích thước khoảng 20–22px.

Logo đặt cách lề trái khoảng 24px, cách trên khoảng 28–32px.

## Menu điều hướng

Danh sách menu nằm dưới logo. Mỗi item gồm icon bên trái và text bên phải.

Các menu đang có:

1. **Dashboard**
2. **Quản lý tài khoản**
3. **Quản lý bác sĩ**
4. **Quản lý bệnh nhân**
5. **Quản lý thuốc**
6. **Quản lý dịch vụ**
7. **Quản lý thanh toán**
8. **Xem báo cáo thống kê**
9. **Phân quyền hệ thống**
10. Nút **Đăng xuất** ở cuối sidebar

Menu đang active là **Phân quyền hệ thống**.

## Trạng thái active

Item **Phân quyền hệ thống** có:

* Nền xanh lá rất nhạt.
* Text màu xanh lá.
* Icon khiên màu xanh lá.
* Bo góc khoảng 6–8px.
* Có cảm giác nổi bật hơn các item khác.

Các item còn lại:

* Icon màu xanh đen / slate.
* Text màu xanh đen.
* Không có nền hoặc nền trong suốt.
* Khi hover nên đổi nền xám nhạt hoặc xanh rất nhạt.

## Nút Đăng xuất

Nằm gần đáy sidebar, tách khỏi nhóm menu chính.

Thiết kế:

* Nền đỏ nhạt.
* Icon logout màu đỏ.
* Text **Đăng xuất** màu đỏ.
* Bo góc 8px.
* Padding ngang khoảng 18–24px, dọc 14px.

Chức năng suy đoán:

* Khi bấm sẽ hiển thị modal xác nhận:

  * “Bạn có chắc chắn muốn đăng xuất?”
  * Nút Hủy
  * Nút Đăng xuất
* Sau khi xác nhận thì xóa token/session và chuyển về màn hình đăng nhập.

---

# 3. Header nội dung chính

Khu vực nội dung bắt đầu từ bên phải sidebar, nền tổng thể màu xám trắng rất nhạt.

Phần trên cùng gồm tiêu đề bên trái và khu vực tài khoản bên phải.

## Tiêu đề trang

Text lớn:

**Phân quyền hệ thống**

Đặc điểm:

* Font đậm.
* Màu xanh đen.
* Kích thước khoảng 28–32px.
* Nằm cách mép trái khu vực content khoảng 30px.
* Cách trên khoảng 28px.

## Breadcrumb

Bên dưới tiêu đề có breadcrumb:

**Dashboard / Phân quyền hệ thống**

Trong đó:

* “Dashboard” màu xám xanh.
* Dấu “/” màu xám.
* “Phân quyền hệ thống” màu xám xanh hoặc đậm hơn chút.
* Kích thước khoảng 14–15px.

Chức năng:

* Bấm vào “Dashboard” có thể điều hướng về trang dashboard.
* Breadcrumb giúp người dùng biết đang ở module nào.

## Khu vực bên phải header

Có 3 phần:

1. Icon chuông thông báo.
2. Badge đỏ hiển thị số lượng thông báo.
3. Avatar + tên người dùng + dropdown.

### Chuông thông báo

* Icon chuông màu xanh đen.
* Có badge đỏ tròn ở góc trên phải.
* Badge hiển thị số **3**.
* Badge nền đỏ, chữ trắng, kích thước nhỏ.

Chức năng suy đoán:

* Bấm vào chuông mở dropdown thông báo.
* Danh sách có thể gồm:

  * Tài khoản mới chờ duyệt.
  * Vai trò vừa được cập nhật.
  * Cảnh báo bảo mật.
* Có thể có nút “Xem tất cả thông báo”.

### Avatar và tài khoản

Hiển thị:

* Avatar hình tròn.
* Text: **Admin (Quản trị viên)**
* Icon mũi tên xuống.

Chức năng suy đoán:

* Bấm mở menu tài khoản gồm:

  * Thông tin cá nhân.
  * Đổi mật khẩu.
  * Cài đặt tài khoản.
  * Đăng xuất.

---

# 4. Khu vực thống kê nhanh

Ngay dưới tiêu đề là 4 thẻ thống kê nằm ngang.

Mỗi thẻ có:

* Nền trắng.
* Viền mảnh màu xám nhạt.
* Bo góc 10–12px.
* Padding khoảng 20–24px.
* Icon lớn nằm bên trái trong một ô vuông bo góc.
* Nội dung nằm bên phải icon.
* Có hiệu ứng đổ bóng rất nhẹ hoặc chỉ viền.

Khoảng cách giữa các thẻ khoảng 24px.

## Thẻ 1: Tổng vai trò

Nội dung:

* Icon khiên màu trắng trên nền xanh lá.
* Label: **Tổng vai trò**
* Số lớn: **4**
* Mô tả nhỏ: **vai trò trong hệ thống**

Màu chính: xanh lá.

Chức năng dữ liệu:

* Đếm tổng số role đang tồn tại trong hệ thống.
* Có thể không tính role đã bị xóa mềm.

## Thẻ 2: Tổng người dùng

Nội dung:

* Icon nhóm người màu trắng trên nền xanh dương.
* Label: **Tổng người dùng**
* Số lớn: **18**
* Mô tả nhỏ: **người dùng đã phân quyền**

Màu chính: xanh dương.

Chức năng dữ liệu:

* Đếm số user đã được gán ít nhất một vai trò.
* Có thể bấm để chuyển sang tab “Quản lý người dùng”.

## Thẻ 3: Tổng quyền

Nội dung:

* Icon chìa khóa màu trắng trên nền cam.
* Label: **Tổng quyền**
* Số lớn: **68**
* Mô tả nhỏ: **quyền trong hệ thống**

Màu chính: cam.

Chức năng dữ liệu:

* Đếm toàn bộ permission/action trong hệ thống.

Ví dụ quyền:

* Xem danh sách bác sĩ.
* Thêm bác sĩ.
* Sửa bác sĩ.
* Xóa bác sĩ.
* Quản lý lịch làm việc.
* Sao lưu dữ liệu.

## Thẻ 4: Nhóm quyền

Nội dung:

* Icon biểu đồ tròn/pie màu trắng trên nền tím.
* Label: **Nhóm quyền**
* Số lớn: **10**
* Mô tả nhỏ: **nhóm quyền chức năng**

Màu chính: tím.

Chức năng dữ liệu:

* Đếm số nhóm quyền theo module/chức năng, ví dụ:

  * Quản lý hệ thống
  * Quản lý bác sĩ
  * Quản lý bệnh nhân
  * Quản lý thuốc
  * Quản lý dịch vụ
  * Quản lý thanh toán
  * Báo cáo thống kê
  * Sao lưu dữ liệu
  * Quản lý tài khoản
  * Quản lý phân quyền

---

# 5. Thanh tab và hành động

Bên dưới khu vực thống kê là một khối nằm ngang, nền trắng, bo góc.

## Tab

Có 2 tab:

1. **Quản lý vai trò**
2. **Quản lý người dùng**

Tab đang active là **Quản lý vai trò**.

### Tab active

* Text màu xanh lá.
* Có đường gạch dưới màu xanh lá.
* Font đậm hơn.
* Padding ngang khoảng 32px.
* Chiều cao tab khoảng 56px.

### Tab inactive

* Text màu xám xanh.
* Không có gạch dưới.
* Khi hover đổi sang xanh lá nhẹ.

## Nút hành động bên phải

Có 2 nút:

### Nút “Thêm vai trò”

* Nền xanh lá.
* Chữ trắng.
* Icon dấu cộng bên trái.
* Text: **Thêm vai trò**
* Bo góc 6–8px.
* Cao khoảng 38–42px.
* Padding ngang khoảng 18–20px.

Chức năng suy đoán:

Bấm mở modal tạo vai trò mới với các trường:

* Tên vai trò
* Mã vai trò
* Mô tả
* Trạng thái hoạt động
* Danh sách quyền được gán
* Nút Hủy
* Nút Tạo vai trò

Validation:

* Tên vai trò bắt buộc.
* Mã vai trò không trùng.
* Ít nhất có thể chọn một nhóm quyền hoặc cho phép tạo role chưa có quyền.
* Không cho tạo role trùng tên.

### Nút “Cấu hình quyền”

* Nền trắng.
* Viền xám nhạt.
* Icon bánh răng.
* Text: **Cấu hình quyền**
* Chữ màu xanh đen.
* Bo góc 6–8px.

Chức năng suy đoán:

Bấm mở màn hình hoặc modal cấu hình toàn bộ permission trong hệ thống.

Có thể gồm:

* Danh sách nhóm quyền.
* Danh sách quyền trong từng nhóm.
* Checkbox bật/tắt quyền theo từng vai trò.
* Ma trận Role x Permission.
* Nút lưu thay đổi.
* Nút khôi phục mặc định.
* Cảnh báo khi chỉnh quyền Admin.

---

# 6. Nội dung chính: bố cục 2 cột

Phần nội dung chính phía dưới được chia thành 2 card lớn.

## Cột trái: Danh sách vai trò

Chiếm khoảng 30% chiều rộng nội dung.

Card có:

* Nền trắng.
* Viền mảnh xám nhạt.
* Bo góc 8–10px.
* Chiều cao gần bằng card bên phải.
* Có header, ô tìm kiếm, danh sách role, footer phân trang.

### Header

Text:

**Danh sách vai trò**

Đặc điểm:

* Font đậm.
* Màu xanh đen.
* Kích thước khoảng 16–18px.
* Padding trên và trái khoảng 20px.

### Ô tìm kiếm

Bên dưới header có input tìm kiếm.

Placeholder:

**Tìm kiếm vai trò...**

Thiết kế:

* Icon kính lúp bên trái.
* Border xám nhạt.
* Bo góc 6–8px.
* Cao khoảng 42px.
* Padding trái đủ để chứa icon.
* Font 14px.

Chức năng:

* Tìm kiếm theo tên vai trò.
* Có thể tìm theo mã vai trò hoặc mô tả.
* Khi nhập text, danh sách role lọc realtime hoặc sau debounce 300ms.
* Nếu không tìm thấy, hiển thị empty state “Không tìm thấy vai trò”.

### Danh sách role

Danh sách hiện có 4 vai trò:

1. **Quản trị viên (Admin)**

   * Mô tả: **Toàn quyền hệ thống**
   * Badge: **2 người dùng**
   * Icon bánh răng/khiên nền xanh lá
   * Đang được chọn

2. **Bác sĩ (Doctor)**

   * Mô tả: **Quản lý chuyên môn**
   * Badge: **6 người dùng**
   * Icon người dùng nền xanh dương

3. **Lễ tân (receptionist)**

   * Mô tả: **Quản lý tiếp đón và lịch hẹn**
   * Badge: **8 người dùng**
   * Icon nhóm/người nền cam

4. **Kế toán (accountant)**

   * Mô tả: **Quản lý tài chính**
   * Badge: **2 người dùng**
   * Icon nhóm/người nền tím

### Role item active

Role **Quản trị viên (Admin)** đang active.

Thiết kế:

* Nền xanh lá rất nhạt.
* Có border trái màu xanh lá hoặc toàn bộ nền nhấn mạnh.
* Text title đậm.
* Badge người dùng nền xanh lá nhạt.
* Icon nền xanh lá.
* Cả item có thể click.

Chức năng:

* Khi click vào role, cập nhật phần bên phải để hiển thị quyền của role đó.
* URL có thể thay đổi dạng:

  * `/admin/permissions?role=admin`
  * hoặc `/admin/roles/admin`

### Role item inactive

Các role còn lại:

* Nền trắng.
* Hover đổi nền xám nhạt.
* Icon màu riêng theo role.
* Badge màu theo role hoặc màu xanh/tím/cam nhẹ.

### Footer cột trái

Cuối card có phần chọn số dòng hiển thị:

Text:

**Hiển thị [10 ▼] bản ghi**

Trong đó dropdown đang chọn **10**.

Chức năng:

* Cho phép chọn 10 / 20 / 50 bản ghi.
* Nếu danh sách role nhiều, cần có phân trang hoặc scroll nội bộ.
* Card hiện tại chưa có pagination số trang ở cột trái, nhưng có thể bổ sung khi role nhiều.

---

# 7. Cột phải: Danh sách quyền của vai trò

Cột phải chiếm khoảng 70% chiều rộng.

Card có:

* Nền trắng.
* Viền xám nhạt.
* Bo góc 8–10px.
* Padding nội bộ.
* Chứa header, subtitle, bảng quyền, footer phân trang.

## Header

Text chính:

**Danh sách quyền của vai trò: Quản trị viên (Admin)**

Bên dưới có mô tả nhỏ:

**Quản trị toàn bộ hệ thống**

Ý nghĩa:

* Header thay đổi theo role đang chọn.
* Subtitle lấy từ mô tả của role.

Ví dụ khi chọn Bác sĩ thì đổi thành:

**Danh sách quyền của vai trò: Bác sĩ (Doctor)**
**Quản lý chuyên môn**

---

# 8. Bảng quyền

Bảng có 4 cột chính:

1. **Nhóm quyền**
2. **Danh sách quyền**
3. **Mô tả**
4. **Trạng thái**

Header bảng nền trắng hoặc xám rất nhạt, border-bottom xám nhạt.

## Cột Nhóm quyền

Cột này hiển thị tên nhóm quyền theo module.

Mỗi nhóm có:

* Icon mũi tên nhỏ để expand/collapse.
* Icon nhóm quyền màu riêng.
* Tên nhóm quyền in đậm.
* Dòng phụ hiển thị số lượng quyền, ví dụ:

  * **6 quyền**
  * **5 quyền**
  * **4 quyền**

Nhóm quyền hiện đang hiển thị:

### 1. Quản lý hệ thống

* Icon khiên màu xanh lá.
* Số lượng: **6 quyền**

Các quyền:

1. Quản lý người dùng
2. Phân quyền người dùng
3. Quản lý vai trò
4. Cấu hình hệ thống
5. Sao lưu dữ liệu
6. Nhật ký hệ thống

Mô tả tương ứng:

1. Thêm, sửa, xóa người dùng
2. Phân quyền cho người dùng
3. Quản lý các vai trò hệ thống
4. Cấu hình thông số hệ thống
5. Sao lưu và phục hồi dữ liệu
6. Xem nhật ký hoạt động

Trạng thái: tất cả **Được phép**

### 2. Quản lý bác sĩ

* Icon người/bác sĩ màu xanh dương.
* Số lượng: **5 quyền**

Các quyền:

1. Xem danh sách bác sĩ
2. Thêm bác sĩ
3. Sửa thông tin bác sĩ
4. Xóa bác sĩ
5. Quản lý lịch làm việc

Mô tả tương ứng:

1. Xem thông tin bác sĩ
2. Thêm bác sĩ mới
3. Cập nhật thông tin bác sĩ
4. Xóa bác sĩ khỏi hệ thống
5. Quản lý lịch làm việc bác sĩ

Trạng thái: tất cả **Được phép**

### 3. Quản lý bệnh nhân

* Icon người màu cam.
* Số lượng: **5 quyền**

Các quyền:

1. Xem danh sách bệnh nhân
2. Thêm bệnh nhân
3. Sửa thông tin bệnh nhân
4. Xóa bệnh nhân
5. Xem lịch sử khám

Mô tả tương ứng:

1. Xem thông tin bệnh nhân
2. Thêm bệnh nhân mới
3. Cập nhật thông tin bệnh nhân
4. Xóa bệnh nhân khỏi hệ thống
5. Xem lịch sử khám bệnh

Trạng thái: tất cả **Được phép**

### 4. Quản lý thuốc

* Icon viên thuốc màu tím.
* Số lượng: **4 quyền**

Các quyền:

1. Xem danh sách thuốc
2. Thêm thuốc
3. Sửa thông tin thuốc
4. Xóa thuốc

Mô tả tương ứng:

1. Xem danh sách thuốc
2. Thêm thuốc mới
3. Cập nhật thông tin thuốc
4. Xóa thuốc khỏi hệ thống

Trạng thái: tất cả **Được phép**

## Cột Danh sách quyền

Hiển thị từng permission/action cụ thể.

Text màu xanh đen hoặc xám xanh, kích thước 13–14px.

Mỗi dòng tương ứng một quyền.

Không thấy checkbox trong ảnh, nhưng về chức năng nên có một trong hai cách:

### Cách 1: Chỉ xem quyền

Bảng chỉ hiển thị các quyền hiện tại của role. Muốn sửa thì bấm **Cấu hình quyền**.

### Cách 2: Cho chỉnh trực tiếp

Cột trạng thái hoặc mỗi dòng có thể click để bật/tắt quyền. Nếu làm cách này, nên có thêm:

* Checkbox ở đầu mỗi quyền.
* Nút “Lưu thay đổi”.
* Nút “Hủy”.
* Cảnh báo khi thay đổi quyền quan trọng.

Vì giao diện hiện tại chỉ có badge **Được phép**, có vẻ đây là chế độ xem, còn chỉnh sửa nằm trong nút **Cấu hình quyền**.

## Cột Mô tả

Mô tả ngắn giải thích quyền đó dùng để làm gì.

Cột này rất quan trọng để admin hiểu rõ quyền trước khi cấp.

Ví dụ:

* “Thêm bác sĩ mới”
* “Xóa bác sĩ khỏi hệ thống”
* “Cấu hình thông số hệ thống”
* “Sao lưu và phục hồi dữ liệu”

## Cột Trạng thái

Mỗi dòng hiển thị badge:

**Được phép**

Thiết kế:

* Nền xanh lá nhạt.
* Text xanh lá.
* Bo góc dạng pill.
* Font nhỏ, khoảng 12px.
* Padding ngang 8–10px, dọc 3–5px.

Chức năng suy đoán:

* Nếu role không có quyền, có thể hiển thị badge:

  * **Không được phép**
  * Nền đỏ nhạt
  * Text đỏ
* Hoặc nếu quyền bị khóa:

  * **Bị khóa**
  * Nền xám
  * Text xám
* Hoặc nếu quyền đang chờ duyệt:

  * **Chờ duyệt**
  * Nền vàng nhạt
  * Text vàng/cam

---

# 9. Hành vi expand/collapse nhóm quyền

Trong bảng, mỗi nhóm quyền có icon mũi tên nhỏ bên trái.

Chức năng nên có:

* Click vào nhóm quyền để thu gọn/mở rộng.
* Khi mở rộng, hiển thị danh sách quyền con.
* Khi thu gọn, chỉ còn dòng nhóm quyền và số lượng quyền.
* Mũi tên xoay:

  * Mở: mũi tên xuống.
  * Đóng: mũi tên sang phải.
* Trạng thái mở/đóng có thể lưu tạm trong state frontend.

Suy đoán từ ảnh: các nhóm đang được mở rộng.

---

# 10. Phân trang cột phải

Dưới bảng bên phải có footer gồm 2 phần.

## Bên trái

Text:

**Hiển thị [10 ▼] bản ghi**

Dropdown đang chọn **10**.

Chức năng:

* Chọn số bản ghi mỗi trang:

  * 10
  * 20
  * 50
  * 100
* Khi đổi số bản ghi, reset về trang 1.

## Bên phải

Pagination gồm:

* Nút previous `<`
* Trang **1** đang active
* Trang 2
* Trang 3
* Dấu `...`
* Trang 7
* Nút next `>`

Trang active:

* Nền xanh lá.
* Chữ trắng.
* Bo góc 6px.

Trang inactive:

* Nền trắng.
* Border xám nhạt.
* Chữ xanh đen.

Chức năng:

* Bấm trang để chuyển trang.
* Bấm previous/next.
* Disable previous khi ở trang đầu.
* Disable next khi ở trang cuối.
* Với nhiều quyền, phân trang theo permission row, không nhất thiết theo group.

---

# 11. Màu sắc đề xuất

Có thể dùng bộ màu như sau:

```txt
Primary green: #16A34A hoặc #10B981
Primary green dark: #15803D
Primary green light: #ECFDF5 hoặc #DCFCE7

Blue: #2563EB
Blue light: #EFF6FF

Orange: #F97316
Orange light: #FFF7ED

Purple: #7C3AED
Purple light: #F5F3FF

Text primary: #0F172A
Text secondary: #475569
Text muted: #64748B

Border: #E5E7EB
Background page: #F8FAFC
Card background: #FFFFFF

Danger: #EF4444
Danger light: #FEF2F2
```

---

# 12. Typography

Gợi ý font:

* Inter
* Roboto
* Nunito Sans
* SF Pro Display nếu làm giao diện giống macOS/iOS

Kích thước:

```txt
Page title: 28–32px, font-weight 700
Card title: 16–18px, font-weight 600
Body text: 14px
Small text: 12–13px
Stats number: 26–30px, font-weight 700
Sidebar item: 15–16px
Badge text: 12px, font-weight 500
```

---

# 13. Spacing và layout

Gợi ý kích thước:

```txt
Sidebar width: 270px
Main content padding: 28–32px
Card border-radius: 10–12px
Card padding: 20–24px
Gap between stats cards: 24px
Gap between main columns: 16–20px
Left role panel width: 30%
Right permission panel width: 70%
Input height: 42px
Button height: 38–42px
Table row min-height: 38–44px
```

---

# 14. Component nên tách khi code

Có thể chia thành các component:

```txt
AdminLayout
 ├── Sidebar
 ├── TopHeader
 ├── Breadcrumb
 └── PageContent

PermissionPage
 ├── StatsCards
 ├── PermissionTabs
 ├── RoleManagementTab
 │    ├── RoleListPanel
 │    │    ├── RoleSearchInput
 │    │    ├── RoleListItem
 │    │    └── PageSizeSelector
 │    └── RolePermissionPanel
 │         ├── RolePermissionHeader
 │         ├── PermissionTable
 │         │    ├── PermissionGroupRow
 │         │    └── PermissionRow
 │         └── Pagination
 ├── UserRoleManagementTab
 ├── AddRoleModal
 ├── ConfigurePermissionModal
 └── ConfirmDialog
```

---

# 15. Dữ liệu mẫu cho frontend

Có thể dựng data như sau:

```js
const roles = [
  {
    id: "admin",
    name: "Quản trị viên",
    code: "Admin",
    description: "Toàn quyền hệ thống",
    userCount: 2,
    color: "green"
  },
  {
    id: "doctor",
    name: "Bác sĩ",
    code: "Doctor",
    description: "Quản lý chuyên môn",
    userCount: 6,
    color: "blue"
  },
  {
    id: "receptionist",
    name: "Lễ tân",
    code: "receptionist",
    description: "Quản lý tiếp đón và lịch hẹn",
    userCount: 8,
    color: "orange"
  },
  {
    id: "accountant",
    name: "Kế toán",
    code: "accountant",
    description: "Quản lý tài chính",
    userCount: 2,
    color: "purple"
  }
];
```

Permission group mẫu:

```js
const permissionGroups = [
  {
    id: "system",
    name: "Quản lý hệ thống",
    icon: "shield",
    color: "green",
    permissions: [
      {
        id: "user.manage",
        name: "Quản lý người dùng",
        description: "Thêm, sửa, xóa người dùng",
        allowed: true
      },
      {
        id: "user.assign_permission",
        name: "Phân quyền người dùng",
        description: "Phân quyền cho người dùng",
        allowed: true
      },
      {
        id: "role.manage",
        name: "Quản lý vai trò",
        description: "Quản lý các vai trò hệ thống",
        allowed: true
      }
    ]
  }
];
```

---

# 16. Chức năng cần có trong màn này

## Quản lý vai trò

Các chức năng chính:

1. Xem danh sách vai trò.
2. Tìm kiếm vai trò.
3. Xem số người dùng đang thuộc từng vai trò.
4. Chọn vai trò để xem quyền.
5. Thêm vai trò mới.
6. Sửa thông tin vai trò.
7. Xóa vai trò.
8. Nhân bản vai trò.
9. Bật/tắt trạng thái vai trò.
10. Gán quyền cho vai trò.

Nên có thêm menu ba chấm ở mỗi role item:

* Chỉnh sửa
* Sao chép vai trò
* Xem người dùng thuộc vai trò
* Xóa vai trò

Role Admin nên có ràng buộc:

* Không cho xóa.
* Không cho tắt toàn bộ quyền.
* Không cho tự gỡ quyền quản trị của chính mình nếu chỉ còn một Admin.

## Cấu hình quyền

Các chức năng nên có:

1. Xem toàn bộ nhóm quyền.
2. Thêm nhóm quyền.
3. Sửa tên nhóm quyền.
4. Thêm permission mới.
5. Sửa mô tả permission.
6. Bật/tắt permission.
7. Cấp quyền cho role theo checkbox.
8. Cấp quyền theo nhóm.
9. Cấp toàn bộ quyền.
10. Gỡ toàn bộ quyền.
11. Lưu cấu hình quyền.
12. Xem lịch sử thay đổi quyền.

## Quản lý người dùng

Tab này chưa được mở trong ảnh, nhưng nên có chức năng:

1. Xem danh sách người dùng.
2. Tìm kiếm người dùng.
3. Lọc theo vai trò.
4. Lọc theo trạng thái tài khoản.
5. Gán vai trò cho người dùng.
6. Gỡ vai trò khỏi người dùng.
7. Xem quyền thực tế của người dùng.
8. Xem lịch sử phân quyền.
9. Cảnh báo khi người dùng có quyền nhạy cảm.

Bảng user có thể gồm:

* Họ tên
* Email / Số điện thoại
* Vai trò hiện tại
* Trạng thái
* Ngày được phân quyền
* Người phân quyền
* Hành động

---

# 17. Quy tắc nghiệp vụ nên có

Vì đây là hệ thống y tế, phần phân quyền cần chặt chẽ.

## Quy tắc role

* Một người dùng có thể có một hoặc nhiều vai trò.
* Vai trò Admin có toàn quyền.
* Vai trò Doctor chỉ nên truy cập dữ liệu chuyên môn liên quan.
* Vai trò Receptionist được quản lý lịch hẹn, tiếp đón, thông tin cơ bản bệnh nhân.
* Vai trò Accountant được quản lý thanh toán, hóa đơn, báo cáo tài chính.
* Không cho xóa role nếu đang có người dùng thuộc role đó, trừ khi chuyển người dùng sang role khác.
* Role mặc định của hệ thống nên được bảo vệ.

## Quy tắc permission

Permission nên đặt theo cấu trúc:

```txt
module.action
```

Ví dụ:

```txt
doctor.view
doctor.create
doctor.update
doctor.delete
patient.view
patient.create
patient.update
patient.delete
medicine.view
medicine.create
medicine.update
medicine.delete
payment.view
payment.create
report.view
system.backup
system.audit_log
```

## Quyền nhạy cảm

Các quyền sau nên có cảnh báo khi cấp:

* Xóa dữ liệu.
* Sao lưu dữ liệu.
* Khôi phục dữ liệu.
* Xem nhật ký hệ thống.
* Cấu hình hệ thống.
* Phân quyền người dùng.
* Quản lý vai trò.
* Xem báo cáo tài chính.
* Xem toàn bộ hồ sơ bệnh nhân.

---

# 18. API gợi ý

Có thể thiết kế API như sau:

```txt
GET    /api/admin/roles
GET    /api/admin/roles/:id
POST   /api/admin/roles
PUT    /api/admin/roles/:id
DELETE /api/admin/roles/:id

GET    /api/admin/permissions/groups
GET    /api/admin/roles/:id/permissions
PUT    /api/admin/roles/:id/permissions

GET    /api/admin/users/roles
PUT    /api/admin/users/:id/roles

GET    /api/admin/permission-stats
GET    /api/admin/permission-audit-logs
```

Response thống kê:

```json
{
  "totalRoles": 4,
  "assignedUsers": 18,
  "totalPermissions": 68,
  "permissionGroups": 10
}
```

---

# 19. Trạng thái cần xử lý

## Loading

Khi đang tải dữ liệu:

* Skeleton cho 4 thẻ thống kê.
* Skeleton cho role list.
* Skeleton cho bảng quyền.
* Disable nút khi đang submit.

## Empty state

Khi không có role:

* Icon rỗng.
* Text: “Chưa có vai trò nào”
* Nút: “Thêm vai trò”

Khi role chưa có quyền:

* Text: “Vai trò này chưa được cấp quyền”
* Nút: “Cấu hình quyền”

Khi tìm kiếm không có kết quả:

* Text: “Không tìm thấy vai trò phù hợp”

## Error state

Khi lỗi tải dữ liệu:

* Alert đỏ nhạt.
* Text: “Không thể tải dữ liệu phân quyền”
* Nút: “Thử lại”

## Success state

Sau khi lưu quyền:

* Toast xanh:

  * “Cập nhật quyền thành công”

Sau khi thêm role:

* Toast xanh:

  * “Tạo vai trò thành công”

Sau khi xóa role:

* Toast:

  * “Xóa vai trò thành công”

---

# 20. Responsive

## Desktop

Giao diện như ảnh:

* Sidebar cố định.
* Stats cards nằm 4 cột.
* Nội dung chính 2 cột.

## Tablet

* Sidebar có thể thu gọn chỉ còn icon.
* Stats cards chuyển thành 2 cột.
* Nội dung chính vẫn 2 cột nhưng cột role nhỏ hơn.
* Table có scroll ngang.

## Mobile

* Sidebar biến thành drawer.
* Header compact.
* Stats cards thành 1 cột hoặc 2 cột nhỏ.
* Role list nằm trên.
* Permission table nằm dưới.
* Table chuyển thành dạng card list để dễ đọc.

---

# 21. Gợi ý hành vi bảo mật

Vì đây là màn phân quyền, nên nên có thêm:

1. Ghi log mọi thay đổi quyền.
2. Hiển thị người thay đổi gần nhất.
3. Hiển thị thời gian cập nhật gần nhất.
4. Yêu cầu xác nhận khi cấp quyền nguy hiểm.
5. Không cho user tự hạ quyền Admin của chính mình.
6. Không cho hệ thống không còn Admin nào.
7. Có quyền “super admin” ẩn hoặc quyền root để khôi phục.
8. Có lịch sử rollback cấu hình quyền.
9. Có kiểm tra quyền ở cả frontend và backend.
10. Backend luôn là nơi quyết định quyền cuối cùng.

---

# 22. Tóm tắt ngắn cho người thiết kế/code

Màn hình này là dashboard phân quyền RBAC cho hệ thống CarePlus Admin. Bên trái là menu quản trị, bên phải là trang “Phân quyền hệ thống”. Trên cùng có thống kê tổng vai trò, tổng người dùng đã phân quyền, tổng quyền và tổng nhóm quyền. Bên dưới có tab “Quản lý vai trò” và “Quản lý người dùng”, kèm nút thêm vai trò và cấu hình quyền. Nội dung chính chia hai cột: cột trái là danh sách vai trò có tìm kiếm, cột phải là bảng quyền của vai trò đang chọn. Bảng quyền được nhóm theo module, mỗi nhóm có danh sách quyền, mô tả quyền và trạng thái được phép. Giao diện cần hỗ trợ tìm kiếm, chọn role, phân trang, thêm/sửa/xóa role, cấu hình quyền, gán quyền cho role, quản lý user theo role, log thay đổi và bảo vệ các quyền quan trọng của Admin.
