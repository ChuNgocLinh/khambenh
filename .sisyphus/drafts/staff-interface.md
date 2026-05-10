# Draft: Giao diện Nhân viên (Staff)

## Requirements (confirmed)
- "giao diện mới nhân viên"
- "Giải thích chi tiết giao diện Nhân viên (Staff)"
- Vai trò chính: tiếp nhận bệnh nhân, quản lý lịch hẹn, hỗ trợ bác sĩ, xử lý thanh toán, điều phối hoạt động phòng khám.
- Sidebar mong muốn gồm: Dashboard, Tiếp nhận bệnh nhân, Quản lý lịch hẹn, Danh sách bệnh nhân, Thanh toán & Hóa đơn, Dịch vụ & Gói khám, Thông báo, Báo cáo, Cài đặt.
- Dashboard mong muốn có: thẻ thống kê đầu trang, bảng "Lịch hẹn hôm nay", "Thao tác nhanh", "Bệnh nhân chờ tiếp nhận", "Thông báo", "Thống kê dịch vụ", "Công việc hôm nay".

## Technical Decisions
- Nền tảng chính là PyQt6 desktop app (không phải web frontend) tại `BTL.Nhóm6_Python/healthcare_management`.
- Thêm role `staff` theo pattern role routing hiện có trong `views/main_view.py`.
- Staff UI sẽ bám pattern dashboard/menu doctor/admin (reuse cấu trúc điều hướng và khung trang).

## Research Findings
- `views/main_view.py`: role dispatch hiện có `admin`, `doctor`, còn lại fallback patient; đây là điểm chèn role `staff`.
- `views/dashboard_view.py`: pattern menu + chuyển trang cho dashboard doctor/admin.
- `views/admin_management_views.py`: có các màn hình quản trị bệnh nhân/lịch hẹn/thanh toán dùng lại cho staff theo phân quyền.
- `views/doctor_management_views.py`: có luồng lịch khám/khám bệnh để staff phối hợp check-in/chờ khám.
- Không có hạ tầng test tự động/CI/E2E rõ ràng trong repo hiện tại.

## Open Questions
- Staff có cần role DB riêng (`staff`) hay dùng tạm role hiện có?
- Mức quyền staff trên từng module (đặc biệt bệnh án chuyên môn) chi tiết tới chức năng nào?
- Có yêu cầu triển khai thực thi UI ngay trong code hay chỉ cần đặc tả/plan chi tiết?

## Scope Boundaries
- INCLUDE: Thiết kế cấu trúc Staff UI, luồng nghiệp vụ, menu, widget dashboard, quyền hạn, kế hoạch triển khai.
- EXCLUDE: Chỉnh sửa bệnh án chuyên môn bởi staff; thay đổi kiến trúc toàn hệ thống ngoài phạm vi staff.
