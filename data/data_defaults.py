# ============================================================
# DATA DEFAULTS - DỮ LIỆU MẪU BAN ĐẦU
# ============================================================

from models import Member, Event, Registration, Fee

def get_default_data():
    """Tạo dữ liệu mẫu ban đầu cho hệ thống."""

    return {
        "members": [
            Member(
                "TV001", "Nguyễn Văn A", "a@gmail.com",
                "0987654321", "Truyền thông", "22/09/2026", 50
            ).to_dict(),

            Member(
                "TV002", "Trần Thị B", "b@gmail.com",
                "0912345678", "Sự kiện", "23/09/2026", 40
            ).to_dict(),

            Member(
                "TV003", "Lê Văn C", "c@gmail.com",
                "0923456789", "Media", "24/09/2026", 30
            ).to_dict(),

            Member(
                "TV004", "Phạm Thị D", "d@gmail.com",
                "0934567890", "Truyền thông", "25/09/2026", 25
            ).to_dict(),

            Member(
                "TV005", "Hoàng Văn E", "e@gmail.com",
                "0945678901", "Sự kiện", "26/09/2026", 20
            ).to_dict()
        ],

        "events": [
            Event(
                "SK001", "Workshop Python",
                "25/09/2026", "Phòng A101", 10
            ).to_dict(),

            Event(
                "SK002", "Hội thảo TMĐT",
                "27/09/2026", "Phòng B102", 15
            ).to_dict(),

            Event(
                "SK003", "Cuộc thi ảnh",
                "10/10/2026", "Sân trường", 10
            ).to_dict(),

            Event(
                "SK004", "Workshop UI/UX",
                "25/09/2026", "Phòng B201", 10
            ).to_dict(),

            Event(
                "SK005", "Team Building",
                "02/10/2026", "Sân vận động HUIT", 15
            ).to_dict()
        ],

        "registrations": [
            Registration(
                "DK001", "TV001", "SK001",
                "22/09/2026", "Đã đăng ký", "Có mặt"
            ).to_dict(),

            Registration(
                "DK002", "TV002", "SK002",
                "23/09/2026", "Đã đăng ký", "Có mặt"
            ).to_dict(),

            Registration(
                "DK003", "TV003", "SK003",
                "24/09/2026", "Đã đăng ký", "Có mặt"
            ).to_dict()
        ],

        "fees": [
            Fee(
                "TH001", "TV001", "Hội phí",
                100000, "Hội phí năm 2026",
                "Đã đóng", "22/09/2026"
            ).to_dict(),

            Fee(
                "TH002", "TV002", "Hội phí",
                100000, "Hội phí năm 2026",
                "Chưa đóng", ""
            ).to_dict(),

            Fee(
                "TH003", "TV003", "Hội phí",
                100000, "Hội phí năm 2026",
                "Đã đóng", "23/09/2026"
            ).to_dict(),

            Fee(
                "TH004", "TV004", "Hội phí",
                100000, "Hội phí năm 2026",
                "Đã đóng", "24/09/2026"
            ).to_dict()
        ]
    }
