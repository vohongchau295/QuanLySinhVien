# ============================================================
# MODEL: REGISTRATION - ĐĂNG KÝ SỰ KIỆN
# ============================================================

from utils.validators import is_valid_code
from .base_model import BaseModel


class Registration(BaseModel):

    def __init__(
        self,
        ma_dk,
        ma_tv,
        ma_sk,
        ngay_dk,
        trang_thai="Đã đăng ký",
        co_mat="Chưa điểm danh"
    ):
        self.ma_dk = ma_dk
        self.ma_tv = ma_tv
        self.ma_sk = ma_sk
        self.ngay_dk = ngay_dk
        self.trang_thai = trang_thai
        self.co_mat = co_mat

    @property
    def ma_dk(self):
        return self.__ma_dk

    @ma_dk.setter
    def ma_dk(self, value):
        if not is_valid_code(value, "DK"):
            raise ValueError("Mã đăng ký phải có dạng DK001.")
        self.__ma_dk = value.strip()

    @property
    def ma_tv(self):
        return self.__ma_tv

    @ma_tv.setter
    def ma_tv(self, value):
        if not is_valid_code(value, "TV"):
            raise ValueError("Mã thành viên không hợp lệ.")
        self.__ma_tv = value.strip()

    @property
    def ma_sk(self):
        return self.__ma_sk

    @ma_sk.setter
    def ma_sk(self, value):
        if not is_valid_code(value, "SK"):
            raise ValueError("Mã sự kiện không hợp lệ.")
        self.__ma_sk = value.strip()

    @property
    def ngay_dk(self):
        return self.__ngay_dk

    @ngay_dk.setter
    def ngay_dk(self, value):
        self._require_date(value, "Ngày đăng ký")
        self.__ngay_dk = value.strip()

    @property
    def trang_thai(self):
        return self.__trang_thai

    @trang_thai.setter
    def trang_thai(self, value):
        allowed = ["Đã đăng ký", "Đã hủy"]
        if value not in allowed:
            raise ValueError("Trạng thái đăng ký không hợp lệ.")
        self.__trang_thai = value

    @property
    def co_mat(self):
        return self.__co_mat

    @co_mat.setter
    def co_mat(self, value):
        allowed = ["Có mặt", "Vắng", "Chưa điểm danh"]
        if value not in allowed:
            raise ValueError("Trạng thái điểm danh không hợp lệ.")
        self.__co_mat = value

    def to_dict(self):
        return {
            "ma_dk": self.ma_dk,
            "ma_tv": self.ma_tv,
            "ma_sk": self.ma_sk,
            "ngay_dk": self.ngay_dk,
            "trang_thai": self.trang_thai,
            "co_mat": self.co_mat
        }

    def __str__(self):
        return f"{self.ma_dk} - {self.ma_tv} - {self.ma_sk}"
