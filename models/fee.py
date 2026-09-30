# ============================================================
# MODEL: FEE - KHOẢN THU
# ============================================================

from utils.validators import is_valid_code
from .base_model import BaseModel


class Fee(BaseModel):

    def __init__(
        self,
        ma_thu,
        ma_tv,
        loai_thu,
        so_tien,
        noi_dung,
        trang_thai="Chưa đóng",
        ngay_thu=""
    ):
        self.ma_thu = ma_thu
        self.ma_tv = ma_tv
        self.loai_thu = loai_thu
        self.so_tien = so_tien
        self.noi_dung = noi_dung
        self.trang_thai = trang_thai
        self.ngay_thu = ngay_thu

    @property
    def ma_thu(self):
        return self.__ma_thu

    @ma_thu.setter
    def ma_thu(self, value):
        if not is_valid_code(value, "TH"):
            raise ValueError("Mã khoản thu phải có dạng TH001.")
        self.__ma_thu = value.strip()

    @property
    def ma_tv(self):
        return self.__ma_tv

    @ma_tv.setter
    def ma_tv(self, value):
        if not is_valid_code(value, "TV"):
            raise ValueError("Mã thành viên không hợp lệ.")
        self.__ma_tv = value.strip()

    @property
    def loai_thu(self):
        return self.__loai_thu

    @loai_thu.setter
    def loai_thu(self, value):
        self._require_text(value, "Loại thu")
        self.__loai_thu = value.strip()

    @property
    def so_tien(self):
        return self.__so_tien

    @so_tien.setter
    def so_tien(self, value):
        try:
            value = int(value)
        except (ValueError, TypeError):
            raise ValueError("Số tiền phải là số nguyên.")

        if value <= 0:
            raise ValueError("Số tiền phải lớn hơn 0.")

        self.__so_tien = value

    @property
    def noi_dung(self):
        return self.__noi_dung

    @noi_dung.setter
    def noi_dung(self, value):
        self._require_text(value, "Nội dung")
        self.__noi_dung = value.strip()

    @property
    def trang_thai(self):
        return self.__trang_thai

    @trang_thai.setter
    def trang_thai(self, value):
        allowed = ["Đã đóng", "Chưa đóng"]
        if value not in allowed:
            raise ValueError("Trạng thái khoản thu không hợp lệ.")
        self.__trang_thai = value

    @property
    def ngay_thu(self):
        return self.__ngay_thu

    @ngay_thu.setter
    def ngay_thu(self, value):
        if value == "":
            self.__ngay_thu = ""
            return

        self._require_date(value, "Ngày thu")
        self.__ngay_thu = value.strip()

    def to_dict(self):
        return {
            "ma_thu": self.ma_thu,
            "ma_tv": self.ma_tv,
            "loai_thu": self.loai_thu,
            "so_tien": self.so_tien,
            "noi_dung": self.noi_dung,
            "trang_thai": self.trang_thai,
            "ngay_thu": self.ngay_thu
        }

    def __str__(self):
        return f"{self.ma_thu} - {self.ma_tv} - {self.so_tien:,}đ"
