# Draft: Phân quyền lịch hẹn theo role

## Requirements (confirmed)
- "màn quản lý lịch hẹn role staff hiện tại đang có 4 role admin staff bác sĩ bệnh nhân"
- "hãy phân biệt kĩ các role này"
- "có thể sửa db" (được phép thay đổi schema/data model nếu cần)
- Người dùng xác nhận muốn làm **đầy đủ màn Quản lý lịch hẹn của Staff** (không chỉ RBAC backend).

## Technical Decisions
- Sẽ lập kế hoạch phân quyền theo role dựa trên hiện trạng code + schema DB thực tế trong `BTL.Nhóm6_Python/healthcare_management/database` và các module liên quan lịch hẹn.

## Research Findings
- Đã xác nhận thư mục DB tồn tại: `database/db.py`, `database/init_db.sql`, `database/migrate.py`.

## Open Questions
- Phạm vi cuối: chỉ màn "Quản lý lịch hẹn" cho Staff nhưng phải phân biệt rõ 4 role ở quyền truy cập/chức năng liên quan.
- Có giữ pixel-perfect theo mô tả UI hay cho phép sai khác nhỏ về spacing/icon/font.

## Scope Boundaries
- INCLUDE: phân tách quyền 4 role cho nghiệp vụ lịch hẹn + kế hoạch hoàn thiện đầy đủ màn Staff Appointment Management theo mô tả chi tiết.
- EXCLUDE: implement code ngay lập tức (giai đoạn này là lập kế hoạch quyết định-đầy-đủ).
