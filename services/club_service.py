# ============================================================
# CLUB SERVICE - NGHIỆP VỤ QUẢN LÝ CLB
# ============================================================

from models import Member, Event, Registration, Fee
from utils.helpers import generate_code, find_by_id

class ClubService:
    """
    Service không trực tiếp lo giao diện.
    Service nhận dữ liệu -> kiểm tra nghiệp vụ -> gọi DataManager.
    """

    def __init__(self, manager):
        self._db = manager

    # ========================================================
    # MEMBER
    # ========================================================

    def get_members(self):
        return self._db.load("members")

    def add_member(self, member):
        members = self.get_members()

        if find_by_id(members, "ma_tv", member.ma_tv):
            return False, "Mã thành viên đã tồn tại."

        members.append(member.to_dict())

        if self._db.save("members", members):
            return True, "Thêm thành viên thành công."

        return False, "Không thể lưu dữ liệu."

    def update_member(self, member):
        members = self.get_members()

        for index, item in enumerate(members):
            if item["ma_tv"] == member.ma_tv:
                members[index] = member.to_dict()

                if self._db.save("members", members):
                    return True, "Cập nhật thành viên thành công."

                return False, "Không thể lưu dữ liệu."

        return False, "Không tìm thấy thành viên."

    def delete_member(self, ma_tv):
        members = self.get_members()

        for index, item in enumerate(members):
            if item["ma_tv"] == ma_tv:
                members.pop(index)

                if self._db.save("members", members):
                    return True, "Xóa thành viên thành công."

                return False, "Không thể lưu dữ liệu."

        return False, "Không tìm thấy thành viên."

    def search_member(self, keyword):
        """Tìm thành viên theo mã, tên, email hoặc ban."""
        keyword = str(keyword).strip().lower()

        return [
            item
            for item in self.get_members()
            if (
                keyword in item["ma_tv"].lower()
                or keyword in item["ho_ten"].lower()
                or keyword in item["email"].lower()
                or keyword in item["ban"].lower()
            )
        ]

    # ========================================================
    # EVENT
    # ========================================================

    def get_events(self):
        return self._db.load("events")

    def add_event(self, event):
        events = self.get_events()

        if find_by_id(events, "ma_sk", event.ma_sk):
            return False, "Mã sự kiện đã tồn tại."

        events.append(event.to_dict())

        if self._db.save("events", events):
            return True, "Thêm sự kiện thành công."

        return False, "Không thể lưu dữ liệu."

    def update_event(self, event):
        events = self.get_events()

        for index, item in enumerate(events):
            if item["ma_sk"] == event.ma_sk:
                events[index] = event.to_dict()

                if self._db.save("events", events):
                    return True, "Cập nhật sự kiện thành công."

                return False, "Không thể lưu dữ liệu."

        return False, "Không tìm thấy sự kiện."

    def delete_event(self, ma_sk):
        events = self.get_events()

        for index, item in enumerate(events):
            if item["ma_sk"] == ma_sk:
                events.pop(index)

                if self._db.save("events", events):
                    return True, "Xóa sự kiện thành công."

                return False, "Không thể lưu dữ liệu."

        return False, "Không tìm thấy sự kiện."

    # ========================================================
    # REGISTRATION
    # ========================================================

    def get_registrations(self):
        return self._db.load("registrations")

    def register_event(self, registration):
        registrations = self.get_registrations()

        if not find_by_id(
            self.get_members(),
            "ma_tv",
            registration.ma_tv
        ):
            return False, "Thành viên không tồn tại."

        if not find_by_id(
            self.get_events(),
            "ma_sk",
            registration.ma_sk
        ):
            return False, "Sự kiện không tồn tại."

        for item in registrations:
            if (
                item["ma_tv"] == registration.ma_tv
                and item["ma_sk"] == registration.ma_sk
                and item["trang_thai"] == "Đã đăng ký"
            ):
                return False, "Thành viên đã đăng ký sự kiện này."

        registrations.append(registration.to_dict())

        if self._db.save("registrations", registrations):
            return True, "Đăng ký sự kiện thành công."

        return False, "Không thể lưu dữ liệu."

    def mark_attendance(self, ma_dk, co_mat):
        registrations = self.get_registrations()

        for item in registrations:
            if item["ma_dk"] == ma_dk:
                if co_mat not in ["Có mặt", "Vắng", "Chưa điểm danh"]:
                    return False, "Trạng thái điểm danh không hợp lệ."

                item["co_mat"] = co_mat

                if self._db.save("registrations", registrations):
                    return True, "Cập nhật điểm danh thành công."

                return False, "Không thể lưu dữ liệu."

        return False, "Không tìm thấy đăng ký."

    # ========================================================
    # FEE
    # ========================================================

    def get_fees(self):
        return self._db.load("fees")

    def add_fee(self, fee):
        fees = self.get_fees()

        if not find_by_id(
            self.get_members(),
            "ma_tv",
            fee.ma_tv
        ):
            return False, "Thành viên không tồn tại."

        if find_by_id(fees, "ma_thu", fee.ma_thu):
            return False, "Mã khoản thu đã tồn tại."

        fees.append(fee.to_dict())

        if self._db.save("fees", fees):
            return True, "Thêm khoản thu thành công."

        return False, "Không thể lưu dữ liệu."

    def mark_fee_paid(self, ma_thu, ngay_thu):
        fees = self.get_fees()

        for item in fees:
            if item["ma_thu"] == ma_thu:
                item["trang_thai"] = "Đã đóng"
                item["ngay_thu"] = ngay_thu

                if self._db.save("fees", fees):
                    return True, "Đã cập nhật trạng thái đóng phí."

                return False, "Không thể lưu dữ liệu."

        return False, "Không tìm thấy khoản thu."

    # ========================================================
    # THỐNG KÊ NGHIỆP VỤ CƠ BẢN
    # ========================================================

    def stats(self):
        """Thống kê dữ liệu phục vụ phần nghiệp vụ."""
        members = self.get_members()
        events = self.get_events()
        registrations = self.get_registrations()
        fees = self.get_fees()

        return {
            "members": len(members),
            "events": len(events),
            "participants": len(registrations),
            "paid": sum(
                item["so_tien"]
                for item in fees
                if item["trang_thai"] == "Đã đóng"
            ),
            "unpaid": sum(
                item["so_tien"]
                for item in fees
                if item["trang_thai"] != "Đã đóng"
            )
        }

    # ========================================================
    # TẠO MÃ TỰ ĐỘNG
    # ========================================================

    def next_member_code(self):
        return generate_code(
            "TV", self.get_members(), "ma_tv"
        )

    def next_event_code(self):
        return generate_code(
            "SK", self.get_events(), "ma_sk"
        )

    def next_registration_code(self):
        return generate_code(
            "DK", self.get_registrations(), "ma_dk"
        )

    def next_fee_code(self):
        return generate_code(
            "TH", self.get_fees(), "ma_thu"
        )
