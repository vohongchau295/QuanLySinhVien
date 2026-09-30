# ============================================================
# MODEL: MEMBER - THÀNH VIÊN
# ============================================================

from utils.validators import (
    is_valid_code,
    is_valid_email,
    is_valid_phone
)
from .base_model import BaseModel


class Member(BaseModel):
    """
    Class biểu diễn thành viên câu lạc bộ.

    Có sử dụng:
    - Private: __ma_tv, __ho_ten, ...
    - Protected: _require_text(), _require_date()
    - Property: getter/setter
    - Ràng buộc dữ liệu
    """

    def __init__(
        self,
        ma_tv,
        ho_ten,
        email,
        sdt,
        ban,
        ngay_tham_gia,
        diem=0,
        trang_thai="Hoạt động"
    ):
        self.ma_tv = ma_tv
        self.ho_ten = ho_ten
        self.email = email
        self.sdt = sdt
        self.ban = ban
        self.ngay_tham_gia = ngay_tham_gia
        self.diem = diem
        self.trang_thai = trang_thai

    @property
    def ma_tv(self):
        return self.__ma_tv

    @ma_tv.setter
    def ma_tv(self, value):
        if not is_valid_code(value, "TV"):
            raise ValueError("Mã thành viên phải có dạng TV001.")
        self.__ma_tv = value.strip()

    @property
    def ho_ten(self):
        return self.__ho_ten

    @ho_ten.setter
    def ho_ten(self, value):
        self._require_text(value, "Họ tên")
        self.__ho_ten = value.strip()

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        if not is_valid_email(value):
            raise ValueError("Email không hợp lệ.")
        self.__email = value.strip()

    @property
    def sdt(self):
        return self.__sdt

    @sdt.setter
    def sdt(self, value):
        if not is_valid_phone(value):
            raise ValueError("Số điện thoại không hợp lệ.")
        self.__sdt = value.replace(" ", "").strip()

    @property
    def ban(self):
        return self.__ban

    @ban.setter
    def ban(self, value):
        self._require_text(value, "Ban")
        self.__ban = value.strip()

    @property
    def ngay_tham_gia(self):
        return self.__ngay_tham_gia

    @ngay_tham_gia.setter
    def ngay_tham_gia(self, value):
        self._require_date(value, "Ngày tham gia")
        self.__ngay_tham_gia = value.strip()

    @property
    def diem(self):
        return self.__diem

    @diem.setter
    def diem(self, value):
        try:
            value = int(value)
        except (ValueError, TypeError):
            raise ValueError("Điểm phải là số nguyên.")

        if value < 0 or value > 100:
            raise ValueError("Điểm phải từ 0 đến 100.")

        self.__diem = value

    @property
    def trang_thai(self):
        return self.__trang_thai

    @trang_thai.setter
    def trang_thai(self, value):
        allowed = ["Hoạt động", "Tạm khóa", "Đã rời CLB"]

        if value not in allowed:
            raise ValueError(
                "Trạng thái thành viên không hợp lệ."
            )

        self.__trang_thai = value

    def to_dict(self):
        return {
            "ma_tv": self.ma_tv,
            "ho_ten": self.ho_ten,
            "email": self.email,
            "sdt": self.sdt,
            "ban": self.ban,
            "ngay_tham_gia": self.ngay_tham_gia,
            "diem": self.diem,
            "trang_thai": self.trang_thai
        }

    def __str__(self):
        return f"{self.ma_tv} - {self.ho_ten} - {self.ban}"
