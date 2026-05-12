Dưới đây là mô tả cực chi tiết giao diện **“Xem báo cáo thống kê”** của hệ thống **CarePlus Admin**, đủ để đưa cho designer/dev làm lại theo.

---

# 1. Tổng quan giao diện

Đây là màn hình dashboard báo cáo thống kê dành cho **Admin / Quản trị viên** trong hệ thống quản lý phòng khám hoặc dịch vụ y tế **CarePlus Admin**.

Mục đích chính của màn hình:

* Theo dõi tổng quan doanh thu.
* Theo dõi tổng tiền đã thanh toán.
* Theo dõi số lượng bệnh nhân.
* Theo dõi số lượng dịch vụ.
* Xem biểu đồ doanh thu theo ngày.
* Phân tích doanh thu theo phương thức thanh toán.
* Xem top dịch vụ có doanh thu cao.
* Thống kê bệnh nhân.
* Theo dõi tình trạng thanh toán.
* Xem danh sách giao dịch gần đây.
* Lọc báo cáo theo thời gian, loại báo cáo, nhóm, bác sĩ.
* Xuất báo cáo ra Excel.

Giao diện sử dụng phong cách **admin dashboard hiện đại**, nền sáng, nhiều card trắng, bo góc mềm, màu chủ đạo là **xanh lá CarePlus**, kết hợp xanh dương, cam, tím và đỏ để phân loại dữ liệu.

---

# 2. Bố cục tổng thể

Màn hình chia làm 2 phần chính:

## 2.1 Sidebar bên trái

Sidebar cố định ở bên trái, chiếm khoảng **260–280px chiều rộng**.

Nền sidebar màu trắng hoặc xám rất nhạt. Các mục menu xếp dọc. Logo nằm trên cùng.

## 2.2 Khu vực nội dung chính

Phần còn lại là nội dung báo cáo.

Nền tổng thể màu **#F8FAFC / #F9FAFB** hoặc trắng hơi xám.

Nội dung chính bắt đầu từ bên phải sidebar, có padding khoảng **28–32px**.

---

# 3. Sidebar chi tiết

## 3.1 Logo

Ở góc trên bên trái:

* Icon dấu cộng trong vòng tròn màu xanh lá.
* Text: **CarePlus Admin**
* Chữ màu xanh lá đậm.
* Font đậm, kích thước khoảng 22–24px.
* Dòng logo nằm ngang, icon bên trái, chữ bên phải.

Có thể dùng:

* Icon: `plus-circle`, `medical-cross`, hoặc custom logo.
* Màu chính: `#16A34A` hoặc `#22C55E`.

---

## 3.2 Danh sách menu

Các menu hiển thị theo chiều dọc, mỗi item gồm:

* Icon bên trái.
* Text bên phải.
* Padding dọc khoảng 14–16px.
* Padding ngang khoảng 20–24px.
* Khoảng cách giữa các item khoảng 4–8px.
* Font màu xanh navy đậm hoặc xám xanh.

Danh sách menu theo thứ tự:

1. **Dashboard**

   * Icon ngôi nhà.
2. **Quản lý tài khoản**

   * Icon người dùng.
3. **Quản lý bác sĩ**

   * Icon bác sĩ hoặc người có ống nghe.
4. **Quản lý bệnh nhân**

   * Icon nhóm người.
5. **Quản lý thuốc**

   * Icon viên thuốc.
6. **Quản lý dịch vụ**

   * Icon ống nghe / service.
7. **Quản lý thanh toán**

   * Icon thẻ ngân hàng.
8. **Xem báo cáo thống kê**

   * Icon biểu đồ cột.
   * Đây là menu đang active.
9. **Phân quyền hệ thống**

   * Icon khiên bảo mật.
10. **Sao lưu dữ liệu**

* Icon cloud download / backup.

---

## 3.3 Trạng thái menu active

Menu active là **“Xem báo cáo thống kê”**.

Cách hiển thị:

* Nền xanh lá rất nhạt: khoảng `#DCFCE7` hoặc `#E8F8EF`.
* Chữ màu xanh lá đậm: `#16A34A`.
* Icon cũng màu xanh lá.
* Item có bo góc khoảng 8–10px.
* So với các menu khác, item active nổi bật rõ ràng.

---

## 3.4 Nút đăng xuất

Ở cuối sidebar có nút **“Đăng xuất”**.

Vị trí:

* Nằm sát cuối sidebar.
* Có icon logout màu đỏ.
* Text màu đỏ.
* Nền đỏ rất nhạt: khoảng `#FEE2E2` hoặc `#FDECEC`.
* Bo góc khoảng 8–10px.
* Padding tương tự menu item.

Chức năng suy đoán:

* Khi bấm, hiển thị modal xác nhận:

  * “Bạn có chắc chắn muốn đăng xuất?”
  * Nút “Hủy”
  * Nút “Đăng xuất”
* Sau khi xác nhận, xóa token/session và chuyển về trang đăng nhập.

---

# 4. Header phần nội dung chính

Trên cùng khu vực nội dung chính có 2 phần:

## 4.1 Tiêu đề trang

Bên trái:

* Tiêu đề lớn: **“Xem báo cáo thống kê”**
* Font size khoảng 26–30px.
* Font weight 700 hoặc 800.
* Màu xanh navy rất đậm: `#0F172A`.

Bên dưới là breadcrumb:

```text
Dashboard / Xem báo cáo thống kê
```

* Text nhỏ hơn, khoảng 14px.
* “Dashboard” màu xám xanh.
* Dấu `/`.
* “Xem báo cáo thống kê” màu xám xanh hoặc xanh navy nhạt.

Chức năng breadcrumb:

* Bấm vào “Dashboard” có thể quay về trang dashboard.
* Phần hiện tại không cần click.

---

## 4.2 Khu vực admin bên phải

Góc trên bên phải có:

1. Icon chuông thông báo.
2. Badge đỏ số **3**.
3. Avatar người dùng.
4. Text: **Admin (Quản trị viên)**
5. Icon mũi tên dropdown.

### Chuông thông báo

* Icon chuông màu xanh navy.
* Badge đỏ nằm góc trên phải chuông.
* Badge hình tròn, màu đỏ `#EF4444`.
* Số trắng: **3**.

Chức năng suy đoán:

* Khi click chuông:

  * Mở dropdown thông báo.
  * Hiển thị danh sách thông báo mới:

    * Thanh toán mới.
    * Bệnh nhân mới.
    * Cảnh báo hệ thống.
    * Lịch hẹn mới.
  * Có nút “Xem tất cả”.
  * Có thể đánh dấu đã đọc.

### Avatar admin

* Avatar hình tròn, icon nhân vật.
* Kích thước khoảng 40–44px.
* Bên phải avatar là tên/quyền.

Chức năng suy đoán:

* Click vào avatar hoặc dropdown:

  * Hồ sơ cá nhân.
  * Đổi mật khẩu.
  * Cài đặt tài khoản.
  * Đăng xuất.

---

# 5. Hàng thẻ thống kê tổng quan

Ngay dưới header là 4 card thống kê chính, xếp ngang thành 4 cột.

Mỗi card có:

* Nền trắng.
* Border mỏng xám nhạt.
* Bo góc khoảng 12–16px.
* Padding khoảng 20–24px.
* Chiều cao khoảng 120–140px.
* Icon lớn bên trái.
* Tiêu đề nhỏ.
* Số liệu lớn.
* Dòng so sánh với tháng trước.

Khoảng cách giữa các card khoảng 20–24px.

---

## 5.1 Card 1 — Tổng doanh thu

Nội dung:

```text
Tổng doanh thu
152.450.000 đ
↑ 18% so với tháng trước
```

Thiết kế:

* Icon ví tiền trong ô vuông bo góc.
* Nền icon xanh dương: `#2563EB`.
* Số tiền màu xanh dương.
* Tăng trưởng màu xanh lá.

Ý nghĩa:

* Tổng doanh thu trong khoảng thời gian đang lọc.
* Bao gồm tất cả giao dịch thành công, có thể không bao gồm giao dịch đang chờ/thất bại.

Chức năng:

* Click card có thể mở chi tiết doanh thu.
* Có tooltip giải thích công thức:

  * “Tổng doanh thu = tổng số tiền các giao dịch thành công trong khoảng thời gian lọc”.

---

## 5.2 Card 2 — Tổng thanh toán

Nội dung:

```text
Tổng thanh toán
128.650.000 đ
↑ 16% so với tháng trước
```

Thiết kế:

* Icon dấu tick trong ô vuông xanh lá.
* Nền icon xanh lá: `#16A34A`.
* Số tiền màu xanh lá.

Ý nghĩa:

* Tổng số tiền đã thanh toán thành công.
* Có thể khác tổng doanh thu nếu có giao dịch chưa thanh toán, đang chờ hoặc hoàn tiền.

Chức năng:

* Click để xem danh sách thanh toán thành công.
* Có thể lọc bảng giao dịch phía dưới theo trạng thái “Thành công”.

---

## 5.3 Card 3 — Tổng bệnh nhân

Nội dung:

```text
Tổng bệnh nhân
256
↑ 12% so với tháng trước
```

Thiết kế:

* Icon nhóm người.
* Nền icon cam: `#F97316`.
* Số lượng màu cam.

Ý nghĩa:

* Tổng số bệnh nhân trong kỳ báo cáo.
* Có thể bao gồm bệnh nhân mới và bệnh nhân tái khám.

Chức năng:

* Click mở báo cáo bệnh nhân.
* Có thể dẫn sang trang “Quản lý bệnh nhân” với filter theo thời gian.

---

## 5.4 Card 4 — Tổng dịch vụ

Nội dung:

```text
Tổng dịch vụ
132
↑ 9% so với tháng trước
```

Thiết kế:

* Icon túi y tế / medical service.
* Nền icon tím: `#7C3AED`.
* Số lượng màu tím.

Ý nghĩa:

* Tổng số lượt dịch vụ đã được sử dụng hoặc tổng dịch vụ phát sinh trong kỳ.
* Không nhất thiết là số loại dịch vụ trong hệ thống.

Chức năng:

* Click xem thống kê dịch vụ.
* Có thể mở top dịch vụ hoặc danh sách dịch vụ phát sinh.

---

# 6. Khu vực bộ lọc báo cáo

Dưới hàng card tổng quan là một khối filter lớn, nền trắng, bo góc.

Khối này gồm các trường lọc nằm ngang:

1. Khoảng thời gian.
2. Loại báo cáo.
3. Nhóm.
4. Bác sĩ.
5. Nút lọc báo cáo.
6. Nút xuất Excel.

---

## 6.1 Trường “Khoảng thời gian”

Label:

```text
Khoảng thời gian
```

Input hiển thị:

```text
01/05/2026 - 24/05/2026
```

Bên phải input có icon lịch.

Thiết kế:

* Input nền trắng.
* Border xám nhạt.
* Bo góc 6–8px.
* Chiều cao khoảng 40–44px.
* Width khoảng 220–240px.

Chức năng:

* Click mở date range picker.
* Chọn ngày bắt đầu và ngày kết thúc.
* Có thể có preset:

  * Hôm nay.
  * 7 ngày qua.
  * Tháng này.
  * Tháng trước.
  * Quý này.
  * Năm nay.
  * Tùy chỉnh.

Validation:

* Ngày bắt đầu không được lớn hơn ngày kết thúc.
* Không cho chọn ngày tương lai nếu báo cáo chỉ dựa trên dữ liệu thực tế.
* Nếu không có dữ liệu trong khoảng thời gian, hiển thị empty state.

---

## 6.2 Dropdown “Loại báo cáo”

Label:

```text
Loại báo cáo
```

Giá trị đang chọn:

```text
Tổng quan
```

Chức năng:

Dropdown này cho phép chọn loại báo cáo khác nhau.

Các option có thể có:

* Tổng quan.
* Doanh thu.
* Thanh toán.
* Bệnh nhân.
* Dịch vụ.
* Bác sĩ.
* Thuốc.
* Công nợ.
* Lịch hẹn.
* Giao dịch.

Khi chọn loại báo cáo khác, các biểu đồ và bảng phía dưới có thể thay đổi.

Ví dụ:

* Chọn “Doanh thu” thì tập trung vào doanh thu theo ngày, phương thức thanh toán, top dịch vụ.
* Chọn “Bệnh nhân” thì hiển thị bệnh nhân mới, tái khám, giới tính, độ tuổi.
* Chọn “Bác sĩ” thì hiển thị doanh thu theo bác sĩ, số bệnh nhân theo bác sĩ.
* Chọn “Dịch vụ” thì hiển thị dịch vụ sử dụng nhiều nhất, doanh thu theo dịch vụ.

---

## 6.3 Dropdown “Nhóm”

Label:

```text
Nhóm
```

Giá trị đang chọn:

```text
Tất cả
```

Chức năng suy đoán:

“Nhóm” có thể là nhóm dữ liệu hoặc nhóm dịch vụ/khoa/phòng ban.

Các option có thể có:

* Tất cả.
* Khám tổng quát.
* Tim mạch.
* Xét nghiệm.
* Siêu âm.
* X-quang.
* Nha khoa.
* Tai mũi họng.
* Sản phụ khoa.
* Nhi khoa.
* Nội tổng quát.
* Ngoại khoa.

Có thể dùng để lọc báo cáo theo nhóm dịch vụ hoặc chuyên khoa.

---

## 6.4 Dropdown “Bác sĩ”

Label:

```text
Bác sĩ
```

Giá trị đang chọn:

```text
Tất cả
```

Chức năng:

* Lọc báo cáo theo bác sĩ.
* Khi chọn một bác sĩ cụ thể, doanh thu, bệnh nhân, dịch vụ và giao dịch chỉ hiển thị dữ liệu liên quan đến bác sĩ đó.

Các option:

* Tất cả.
* BS. Nguyễn Văn A.
* BS. Trần Thị B.
* BS. Lê Minh C.
* BS. Phạm Quốc D.
* ...

Nên có tìm kiếm trong dropdown nếu số bác sĩ nhiều.

---

## 6.5 Nút “Lọc báo cáo”

Nút màu xanh lá.

Text:

```text
Lọc báo cáo
```

Có icon phễu lọc bên trái.

Thiết kế:

* Background `#16A34A`.
* Text trắng.
* Bo góc khoảng 6–8px.
* Chiều cao 40–44px.
* Padding ngang khoảng 18–22px.
* Hover: xanh đậm hơn.
* Disabled khi đang loading.

Chức năng:

* Khi bấm, gọi API lấy lại dữ liệu báo cáo theo filter hiện tại.
* Cập nhật toàn bộ:

  * Card tổng quan.
  * Biểu đồ doanh thu.
  * Biểu đồ phương thức thanh toán.
  * Top dịch vụ.
  * Thống kê bệnh nhân.
  * Tình trạng thanh toán.
  * Bảng giao dịch gần đây.

Nên có loading:

* Spinner trong nút.
* Skeleton ở các card/chart.
* Không reload toàn trang.

---

## 6.6 Nút “Xuất Excel”

Nút viền xám, nền trắng.

Text:

```text
Xuất Excel
```

Có icon Excel màu xanh lá.

Chức năng:

* Xuất báo cáo hiện tại theo filter đang chọn.
* File có thể tên:

```text
bao-cao-thong-ke-01-05-2026-24-05-2026.xlsx
```

Nội dung file nên gồm nhiều sheet:

1. Tổng quan.
2. Doanh thu theo ngày.
3. Doanh thu theo phương thức thanh toán.
4. Top dịch vụ.
5. Thống kê bệnh nhân.
6. Tình trạng thanh toán.
7. Chi tiết giao dịch.

Có thể hiển thị toast:

* “Đang xuất báo cáo...”
* “Xuất Excel thành công”
* “Không thể xuất báo cáo, vui lòng thử lại”

---

# 7. Biểu đồ doanh thu theo ngày

Nằm bên trái hàng biểu đồ đầu tiên.

Card title:

```text
Doanh thu theo ngày
```

Bên phải title có dropdown nhỏ:

```text
7 ngày qua
```

---

## 7.1 Thiết kế card

* Nền trắng.
* Border xám nhạt.
* Bo góc 12–16px.
* Padding 20–24px.
* Chiều cao khoảng 280–320px.
* Chiếm khoảng 60% chiều ngang hàng.

---

## 7.2 Nội dung biểu đồ

Biểu đồ dạng line chart.

Trục X gồm các mốc ngày:

```text
01/05
05/05
10/05
15/05
20/05
24/05
```

Trục Y:

```text
0
5M
10M
15M
20M
25M
```

Dữ liệu hiển thị:

```text
01/05: 8.5M
05/05: 12.3M
10/05: 9.8M
15/05: 16.2M
20/05: 18.7M
24/05: 21.5M
```

Biểu đồ:

* Đường màu xanh dương.
* Có điểm tròn ở từng mốc.
* Có nhãn số tiền phía trên mỗi điểm.
* Có vùng gradient xanh nhạt phía dưới đường.
* Grid ngang màu xám rất nhạt.

---

## 7.3 Chức năng biểu đồ

Khi hover vào điểm dữ liệu:

Hiển thị tooltip:

```text
Ngày: 15/05/2026
Doanh thu: 16.200.000 đ
Số giao dịch: ...
So với ngày trước: ...
```

Dropdown “7 ngày qua” có thể có option:

* 7 ngày qua.
* 14 ngày qua.
* 30 ngày qua.
* Theo khoảng lọc.
* Theo tuần.
* Theo tháng.

Nếu chọn “Theo tháng”, trục X có thể đổi thành tuần hoặc ngày.

Có thể click vào một điểm để lọc bảng giao dịch phía dưới theo ngày đó.

---

# 8. Biểu đồ doanh thu theo phương thức thanh toán

Nằm bên phải biểu đồ doanh thu theo ngày.

Title:

```text
Doanh thu theo phương thức thanh toán
```

---

## 8.1 Thiết kế

Card nền trắng, bo góc, border nhẹ.

Bố cục bên trong chia 2 phần:

* Bên trái: donut chart.
* Bên phải: legend chi tiết.

Ở giữa donut chart hiển thị:

```text
152.450.000 đ
Tổng doanh thu
```

---

## 8.2 Dữ liệu hiển thị

Có 4 phương thức thanh toán:

1. **Tiền mặt**

   * Màu xanh lá.
   * `62.450.000 đ`
   * `41%`

2. **Chuyển khoản**

   * Màu xanh dương.
   * `51.200.000 đ`
   * `34%`

3. **Thẻ ngân hàng**

   * Màu cam.
   * `28.800.000 đ`
   * `19%`

4. **Ví điện tử**

   * Màu tím.
   * `10.000.000 đ`
   * `6%`

Tổng cộng:

```text
152.450.000 đ
```

---

## 8.3 Chức năng

Hover từng phần donut:

* Làm nổi phần đang hover.
* Hiển thị tooltip:

```text
Tiền mặt
62.450.000 đ
41% tổng doanh thu
Số giao dịch: ...
```

Click vào legend hoặc phần chart:

* Lọc bảng giao dịch gần đây theo phương thức thanh toán.
* Ví dụ click “Chuyển khoản” thì bảng bên dưới chỉ hiển thị giao dịch chuyển khoản.

Có thể cho phép ẩn/hiện từng phương thức bằng cách click legend.

---

# 9. Card “Top dịch vụ có doanh thu cao”

Nằm ở hàng giữa, bên trái.

Title:

```text
Top dịch vụ có doanh thu cao
```

Bên dưới là bảng nhỏ.

---

## 9.1 Cấu trúc bảng

Các cột:

```text
STT | Dịch vụ | Doanh thu | Số lượt
```

Dữ liệu:

| STT | Dịch vụ                   |    Doanh thu | Số lượt |
| --- | ------------------------- | -----------: | ------: |
| 1   | Khám tổng quát            | 45.200.000 đ |     120 |
| 2   | Khám chuyên khoa Tim mạch | 32.500.000 đ |      85 |
| 3   | Xét nghiệm máu tổng quát  | 28.700.000 đ |     150 |
| 4   | Siêu âm ổ bụng            | 21.150.000 đ |      75 |
| 5   | Chụp X-Quang phổi         | 14.900.000 đ |      60 |

---

## 9.2 Thiết kế

* Bảng gọn, không có border dày.
* Header text nhỏ, đậm.
* Các dòng cách nhau nhẹ.
* STT căn giữa.
* Doanh thu căn phải.
* Số lượt căn phải hoặc giữa.
* Font khoảng 13–14px.

---

## 9.3 Chức năng

* Click vào tên dịch vụ để xem chi tiết:

  * Doanh thu theo ngày của dịch vụ.
  * Số bệnh nhân sử dụng.
  * Bác sĩ liên quan.
  * Danh sách giao dịch của dịch vụ.
* Có thể thêm nút “Xem thêm” nếu muốn xem top 10/top 20.
* Có thể sort theo:

  * Doanh thu cao nhất.
  * Số lượt nhiều nhất.
  * Tăng trưởng cao nhất.

---

# 10. Card “Thống kê bệnh nhân”

Nằm giữa hàng giữa.

Title:

```text
Thống kê bệnh nhân
```

Card này hiển thị danh sách chỉ số bệnh nhân theo từng dòng.

---

## 10.1 Dữ liệu

Các dòng:

```text
Tổng bệnh nhân      256
Bệnh nhân mới       128
Bệnh nhân tái khám  128
Nam                 132 (52%)
Nữ                  124 (48%)
```

Mỗi dòng có icon bên trái:

* Tổng bệnh nhân: icon nhóm người màu xanh/navy.
* Bệnh nhân mới: icon người màu xanh lá.
* Bệnh nhân tái khám: icon lịch hoặc hồ sơ màu xanh lá.
* Nam: icon người nam màu xanh dương.
* Nữ: icon người nữ màu đỏ/hồng.

---

## 10.2 Ý nghĩa

* **Tổng bệnh nhân**: tổng số bệnh nhân phát sinh trong kỳ.
* **Bệnh nhân mới**: bệnh nhân lần đầu đến khám trong kỳ.
* **Bệnh nhân tái khám**: bệnh nhân đã từng khám và quay lại trong kỳ.
* **Nam/Nữ**: phân bổ giới tính.

---

## 10.3 Chức năng

Click từng dòng có thể lọc dữ liệu:

* Click “Bệnh nhân mới” → mở danh sách bệnh nhân mới.
* Click “Bệnh nhân tái khám” → mở danh sách tái khám.
* Click “Nam” hoặc “Nữ” → lọc bệnh nhân theo giới tính.

Có thể mở rộng thêm:

* Biểu đồ độ tuổi.
* Nhóm bệnh nhân theo khu vực.
* Tỷ lệ quay lại.
* Tỷ lệ bệnh nhân mới theo ngày/tháng.

---

# 11. Card “Tình trạng thanh toán”

Nằm bên phải hàng giữa.

Title:

```text
Tình trạng thanh toán
```

---

## 11.1 Thiết kế

Card gồm:

* Donut chart bên trái.
* Legend bên phải.

Ở giữa donut chart:

```text
256
Tổng giao dịch
```

---

## 11.2 Dữ liệu

Các trạng thái:

1. **Thành công**

   * Màu xanh lá.
   * `218`
   * `85%`

2. **Đang chờ**

   * Màu cam.
   * `22`
   * `9%`

3. **Thất bại**

   * Màu đỏ.
   * `16`
   * `6%`

Tổng:

```text
256 giao dịch
```

---

## 11.3 Chức năng

Hover từng phần donut hiển thị tooltip:

```text
Trạng thái: Thành công
Số giao dịch: 218
Tỷ lệ: 85%
Tổng tiền: ...
```

Click vào trạng thái:

* Lọc bảng giao dịch gần đây theo trạng thái tương ứng.
* Ví dụ click “Thất bại” → bảng bên dưới chỉ hiện giao dịch thất bại.

Có thể thêm cảnh báo:

* Nếu tỷ lệ thất bại vượt ngưỡng, hiển thị alert:

  * “Tỷ lệ thanh toán thất bại đang cao hơn bình thường”.

---

# 12. Bảng “Chi tiết giao dịch gần đây”

Nằm cuối màn hình, chiếm toàn bộ chiều ngang phần nội dung.

Title:

```text
Chi tiết giao dịch gần đây
```

Bên phải title có link:

```text
Xem tất cả
```

---

## 12.1 Cột bảng

Bảng gồm các cột:

```text
STT
Mã giao dịch
Bệnh nhân
Dịch vụ / Thuốc
Phương thức
Số tiền
Ngày thanh toán
Trạng thái
```

---

## 12.2 Dữ liệu đang hiển thị

Dòng 1:

```text
STT: 1
Mã giao dịch: GD250524-0001
Bệnh nhân: Nguyễn Văn Nam
Dịch vụ/Thuốc: Khám tổng quát
Phương thức: Tiền mặt
Số tiền: 150.000 đ
Ngày thanh toán: 24/05/2026 09:15
Trạng thái: Thành công
```

Dòng 2:

```text
STT: 2
Mã giao dịch: GD250524-0002
Bệnh nhân: Trần Thị Mai
Dịch vụ/Thuốc: Khám tim mạch
Phương thức: Chuyển khoản
Số tiền: 200.000 đ
Ngày thanh toán: 24/05/2026 09:30
Trạng thái: Thành công
```

Dòng 3:

```text
STT: 3
Mã giao dịch: GD250524-0003
Bệnh nhân: Lê Văn Cường
Dịch vụ/Thuốc: Xét nghiệm máu
Phương thức: Thẻ ngân hàng
Số tiền: 350.000 đ
Ngày thanh toán: 24/05/2026 10:00
Trạng thái: Thành công
```

---

## 12.3 Thiết kế bảng

* Header nền xám rất nhạt.
* Text header đậm.
* Dòng có border-bottom rất nhẹ.
* Mã giao dịch màu xanh/navy.
* Tên bệnh nhân có avatar nhỏ tròn bên trái.
* Trạng thái là badge.

Badge trạng thái **Thành công**:

* Nền xanh lá nhạt.
* Text xanh lá.
* Bo tròn.
* Padding nhỏ.

Các trạng thái khác nên có:

**Đang chờ**

* Nền cam nhạt.
* Text cam.

**Thất bại**

* Nền đỏ nhạt.
* Text đỏ.

---

## 12.4 Chức năng bảng

Các chức năng nên có:

* Click mã giao dịch → mở chi tiết giao dịch.
* Click tên bệnh nhân → mở hồ sơ bệnh nhân.
* Click dịch vụ/thuốc → mở chi tiết dịch vụ hoặc thuốc.
* Link “Xem tất cả” → chuyển sang trang danh sách giao dịch/báo cáo chi tiết.
* Có thể thêm pagination khi xem tất cả.
* Có thể thêm search theo:

  * Mã giao dịch.
  * Tên bệnh nhân.
  * Dịch vụ.
  * Phương thức.
  * Trạng thái.
* Có thể sort theo:

  * Ngày thanh toán.
  * Số tiền.
  * Trạng thái.

---

# 13. Các chức năng chính cần có trong màn hình

## 13.1 Chức năng tải dữ liệu báo cáo

Khi vào trang:

* Gọi API lấy dữ liệu mặc định.
* Khoảng thời gian mặc định có thể là tháng hiện tại hoặc 7 ngày gần nhất.
* Hiển thị loading trong lúc lấy dữ liệu.
* Sau khi có dữ liệu, render:

  * 4 card tổng quan.
  * Biểu đồ doanh thu.
  * Biểu đồ phương thức thanh toán.
  * Top dịch vụ.
  * Thống kê bệnh nhân.
  * Tình trạng thanh toán.
  * Giao dịch gần đây.

API gợi ý:

```http
GET /api/admin/reports/overview?from=2026-05-01&to=2026-05-24&type=overview&group=all&doctor=all
```

---

## 13.2 Chức năng lọc báo cáo

Filter gồm:

* Khoảng thời gian.
* Loại báo cáo.
* Nhóm.
* Bác sĩ.

Sau khi bấm “Lọc báo cáo”:

* Validate input.
* Gọi API.
* Cập nhật toàn bộ dữ liệu.
* Hiển thị toast thành công hoặc lỗi.

---

## 13.3 Chức năng xuất Excel

Khi bấm “Xuất Excel”:

* Gửi filter hiện tại lên server.
* Server tạo file Excel.
* Browser tải file về.

API gợi ý:

```http
GET /api/admin/reports/export-excel?from=2026-05-01&to=2026-05-24&type=overview&group=all&doctor=all
```

Hoặc:

```http
POST /api/admin/reports/export-excel
```

Body:

```json
{
  "from": "2026-05-01",
  "to": "2026-05-24",
  "type": "overview",
  "group": "all",
  "doctorId": null
}
```

---

## 13.4 Chức năng xem chi tiết giao dịch

Khi click một dòng giao dịch:

Mở modal hoặc trang chi tiết:

Thông tin cần có:

* Mã giao dịch.
* Bệnh nhân.
* Dịch vụ/thuốc.
* Bác sĩ phụ trách.
* Phương thức thanh toán.
* Số tiền.
* Trạng thái.
* Ngày tạo.
* Ngày thanh toán.
* Ghi chú.
* Mã hóa đơn.
* Người thu tiền.
* Lịch sử cập nhật trạng thái.

Các nút có thể có:

* In hóa đơn.
* Tải hóa đơn PDF.
* Hoàn tiền.
* Cập nhật trạng thái.
* Gửi hóa đơn qua email.

---

## 13.5 Chức năng xem tất cả giao dịch

Click “Xem tất cả”:

* Chuyển đến trang danh sách giao dịch đầy đủ.
* Giữ lại filter hiện tại.
* Có pagination, search, sort, export.

Ví dụ URL:

```text
/admin/reports/transactions?from=2026-05-01&to=2026-05-24
```

---

## 13.6 Chức năng thông báo

Click chuông:

Hiển thị dropdown thông báo:

Ví dụ:

```text
Thanh toán mới từ Nguyễn Văn Nam - 150.000 đ
Bệnh nhân Trần Thị Mai vừa đặt lịch khám
Có 2 giao dịch đang chờ xử lý
```

Chức năng:

* Đánh dấu đã đọc.
* Xem tất cả thông báo.
* Badge giảm khi đã đọc.

---

## 13.7 Chức năng tài khoản admin

Click avatar admin:

Dropdown gồm:

```text
Hồ sơ cá nhân
Đổi mật khẩu
Cài đặt
Đăng xuất
```

---

# 14. Các trạng thái giao diện cần xử lý

## 14.1 Loading state

Khi đang tải dữ liệu:

* Card hiển thị skeleton.
* Biểu đồ hiển thị placeholder.
* Bảng hiển thị skeleton rows.
* Nút “Lọc báo cáo” chuyển thành:

```text
Đang lọc...
```

---

## 14.2 Empty state

Khi không có dữ liệu:

Ở biểu đồ:

```text
Không có dữ liệu trong khoảng thời gian đã chọn
```

Ở bảng:

```text
Chưa có giao dịch nào
```

Có thể thêm icon empty.

---

## 14.3 Error state

Khi API lỗi:

Hiển thị toast:

```text
Không thể tải báo cáo. Vui lòng thử lại.
```

Trong card có thể hiển thị:

```text
Dữ liệu không khả dụng
```

Có nút:

```text
Tải lại
```

---

## 14.4 Permission state

Vì đây là trang admin, cần kiểm tra quyền.

Nếu user không có quyền xem báo cáo:

```text
Bạn không có quyền truy cập báo cáo thống kê.
```

Nên cần permission như:

```text
REPORT_VIEW
REPORT_EXPORT
REPORT_TRANSACTION_DETAIL
```

---

# 15. Gợi ý dữ liệu API trả về

Có thể thiết kế response như sau:

```json
{
  "summary": {
    "totalRevenue": 152450000,
    "totalRevenueGrowth": 18,
    "totalPaid": 128650000,
    "totalPaidGrowth": 16,
    "totalPatients": 256,
    "totalPatientsGrowth": 12,
    "totalServices": 132,
    "totalServicesGrowth": 9
  },
  "dailyRevenue": [
    {
      "date": "2026-05-01",
      "label": "01/05",
      "amount": 8500000
    },
    {
      "date": "2026-05-05",
      "label": "05/05",
      "amount": 12300000
    },
    {
      "date": "2026-05-10",
      "label": "10/05",
      "amount": 9800000
    },
    {
      "date": "2026-05-15",
      "label": "15/05",
      "amount": 16200000
    },
    {
      "date": "2026-05-20",
      "label": "20/05",
      "amount": 18700000
    },
    {
      "date": "2026-05-24",
      "label": "24/05",
      "amount": 21500000
    }
  ],
  "paymentMethods": [
    {
      "method": "cash",
      "label": "Tiền mặt",
      "amount": 62450000,
      "percentage": 41
    },
    {
      "method": "bank_transfer",
      "label": "Chuyển khoản",
      "amount": 51200000,
      "percentage": 34
    },
    {
      "method": "card",
      "label": "Thẻ ngân hàng",
      "amount": 28800000,
      "percentage": 19
    },
    {
      "method": "e_wallet",
      "label": "Ví điện tử",
      "amount": 10000000,
      "percentage": 6
    }
  ],
  "topServices": [
    {
      "rank": 1,
      "name": "Khám tổng quát",
      "revenue": 45200000,
      "count": 120
    },
    {
      "rank": 2,
      "name": "Khám chuyên khoa Tim mạch",
      "revenue": 32500000,
      "count": 85
    }
  ],
  "patientStats": {
    "total": 256,
    "newPatients": 128,
    "returningPatients": 128,
    "male": 132,
    "malePercentage": 52,
    "female": 124,
    "femalePercentage": 48
  },
  "paymentStatus": {
    "totalTransactions": 256,
    "success": 218,
    "successPercentage": 85,
    "pending": 22,
    "pendingPercentage": 9,
    "failed": 16,
    "failedPercentage": 6
  },
  "recentTransactions": [
    {
      "id": "GD250524-0001",
      "patientName": "Nguyễn Văn Nam",
      "serviceName": "Khám tổng quát",
      "paymentMethod": "Tiền mặt",
      "amount": 150000,
      "paidAt": "2026-05-24T09:15:00",
      "status": "success"
    }
  ]
}
```

---

# 16. Gợi ý màu sắc

Màu chủ đạo:

```text
Primary green: #16A34A
Primary green light: #DCFCE7
Blue: #2563EB
Orange: #F97316
Purple: #7C3AED
Red: #EF4444
Text dark: #0F172A
Text secondary: #475569
Border: #E2E8F0
Background: #F8FAFC
Card background: #FFFFFF
```

---

# 17. Gợi ý font chữ

Có thể dùng:

* Inter.
* Roboto.
* Be Vietnam Pro.
* Manrope.

Font nên đồng nhất toàn hệ thống.

Kích thước gợi ý:

```text
Page title: 28px / 700
Card number: 24px / 700
Card title: 14px / 600
Body text: 14px / 400-500
Table header: 13px / 600
Small label: 12px / 500
```

---

# 18. Responsive

## Desktop

Đúng như ảnh:

* Sidebar trái cố định.
* 4 card ngang.
* Biểu đồ doanh thu và donut chart nằm cùng hàng.
* 3 card nhỏ nằm cùng hàng.
* Bảng full width.

## Tablet

* Sidebar có thể thu gọn.
* 4 card chuyển thành 2 cột.
* Biểu đồ chuyển thành 1 cột.
* 3 card nhỏ chuyển thành 1 hoặc 2 cột.

## Mobile

* Sidebar chuyển thành drawer.
* Header gọn lại.
* Card thống kê xếp 1 cột.
* Filter xếp dọc.
* Biểu đồ full width.
* Bảng có scroll ngang.

---

# 19. Các role/quyền nên có

Vì đây là hệ thống admin y tế, nên nên chia quyền rõ:

```text
ADMIN
MANAGER
ACCOUNTANT
DOCTOR
STAFF
```

Quyền liên quan trang này:

```text
reports.view
reports.export
reports.view_revenue
reports.view_payment
reports.view_patient_stats
transactions.view
transactions.export
```

Ví dụ:

* Admin xem được tất cả.
* Kế toán xem được doanh thu, thanh toán, xuất Excel.
* Bác sĩ chỉ xem dữ liệu của chính mình.
* Nhân viên chỉ xem giao dịch gần đây nhưng không xem tổng doanh thu toàn hệ thống.

---

# 20. Luồng sử dụng thực tế

Một admin vào màn hình này sẽ làm như sau:

1. Vào menu **Xem báo cáo thống kê**.
2. Hệ thống tự tải báo cáo mặc định của tháng hiện tại.
3. Admin xem nhanh:

   * Tổng doanh thu.
   * Tổng thanh toán.
   * Tổng bệnh nhân.
   * Tổng dịch vụ.
4. Admin đổi khoảng thời gian sang 7 ngày hoặc 1 tháng.
5. Chọn nhóm dịch vụ hoặc bác sĩ nếu cần.
6. Bấm **Lọc báo cáo**.
7. Xem biểu đồ doanh thu tăng/giảm.
8. Xem phương thức thanh toán nào chiếm tỷ lệ cao nhất.
9. Xem dịch vụ nào tạo doanh thu cao nhất.
10. Xem tình trạng thanh toán có lỗi nhiều không.
11. Kiểm tra giao dịch gần đây.
12. Bấm **Xuất Excel** để tải báo cáo.

---

# 21. Tóm tắt ngắn cho dev

Màn hình này là một **admin statistics report dashboard** cho hệ thống y tế CarePlus. Layout gồm sidebar trái, header trên, 4 summary cards, bộ lọc báo cáo, line chart doanh thu theo ngày, donut chart doanh thu theo phương thức thanh toán, bảng top dịch vụ, thống kê bệnh nhân, donut chart trạng thái thanh toán và bảng giao dịch gần đây. Cần hỗ trợ filter theo thời gian, loại báo cáo, nhóm, bác sĩ; export Excel; xem chi tiết giao dịch; xem tất cả; loading/empty/error state; phân quyền theo role.
