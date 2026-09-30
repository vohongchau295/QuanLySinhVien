# ============================================================
# QUẢN LÝ CÂU LẠC BỘ SINH VIÊN - PHẦN NGƯỜI 1
# OOP + DATA + JSON + CRUD
# ============================================================

from models import Member, Event, Registration, Fee
from data.data_manager import DataManager
from services.club_service import ClubService
from utils.helpers import print_header, print_rows, money


def main():
    # Khởi tạo lớp quản lý dữ liệu và lớp nghiệp vụ.
    manager = DataManager("database")
    service = ClubService(manager)

    # ========================================================
    # 1. HIỂN THỊ THÀNH VIÊN
    # ========================================================

    print_header("DANH SÁCH THÀNH VIÊN")
    print_rows(service.get_members())

    # ========================================================
    # 2. TẠO MỘT THÀNH VIÊN MỚI
    # ========================================================

    print_header("THÊM THÀNH VIÊN")

    member = Member(
        service.next_member_code(),
        "Nguyễn Thành Công",
        "cong@gmail.com",
        "0955555555",
        "Truyền thông",
        "30/09/2026",
        35
    )

    success, message = service.add_member(member)
    print(message)

    # ========================================================
    # 3. TÌM KIẾM
    # ========================================================

    print_header("TÌM KIẾM THÀNH VIÊN")

    result = service.search_member("Công")
    print_rows(result)

    # ========================================================
    # 4. THÊM SỰ KIỆN
    # ========================================================

    print_header("THÊM SỰ KIỆN")

    event = Event(
        service.next_event_code(),
        "Workshop OOP Python",
        "05/10/2026",
        "Phòng C101",
        20,
        40
    )

    success, message = service.add_event(event)
    print(message)

    # ========================================================
    # 5. ĐĂNG KÝ SỰ KIỆN
    # ========================================================

    print_header("ĐĂNG KÝ SỰ KIỆN")

    registration = Registration(
        service.next_registration_code(),
        member.ma_tv,
        event.ma_sk,
        "30/09/2026"
    )

    success, message = service.register_event(registration)
    print(message)

    # ========================================================
    # 6. THÊM KHOẢN THU
    # ========================================================

    print_header("THÊM KHOẢN THU")

    fee = Fee(
        service.next_fee_code(),
        member.ma_tv,
        "Hội phí",
        100000,
        "Hội phí năm 2026"
    )

    success, message = service.add_fee(fee)
    print(message)

    # ========================================================
    # 7. THỐNG KÊ
    # ========================================================

    print_header("THỐNG KÊ")

    stats = service.stats()

    print("Số thành viên:", stats["members"])
    print("Số sự kiện:", stats["events"])
    print("Số lượt đăng ký:", stats["participants"])
    print("Tổng đã đóng:", money(stats["paid"]))
    print("Tổng chưa đóng:", money(stats["unpaid"]))

if __name__ == "__main__":
    main()
