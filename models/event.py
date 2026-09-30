# ============================================================
# MODEL: EVENT - SỰ KIỆN
# ============================================================

from utils.validators import is_valid_code
from .base_model import BaseModel


class Event(BaseModel):

    def __init__(
        self,
        ma_sk,
        ten_sk,
        ngay,
        dia_diem,
        diem=10,
        suc_chua=30
    ):
        self.ma_sk = ma_sk
        self.ten_sk = ten_sk
        self.ngay = ngay
        self.dia_diem = dia_diem
        self.diem = diem
        self.suc_chua = suc_chua

    @property
    def ma_sk(self):
        return self.__ma_sk

    @ma_sk.setter
    def ma_sk(self, value):
        if not is_valid_code(value, "SK"):
            raise ValueError("Mã sự kiện phải có dạng SK001.")
        self.__ma_sk = value.strip()

    @property
    def ten_sk(self):
        return self.__ten_sk

    @ten_sk.setter
    def ten_sk(self, value):
        self._require_text(value, "Tên sự kiện")
        self.__ten_sk = value.strip()

    @property
    def ngay(self):
        return self.__ngay

    @ngay.setter
    def ngay(self, value):
        self._require_date(value, "Ngày sự kiện")
        self.__ngay = value.strip()

    @property
    def dia_diem(self):
        return self.__dia_diem

    @dia_diem.setter
    def dia_diem(self, value):
        self._require_text(value, "Địa điểm")
        self.__dia_diem = value.strip()

    @property
    def diem(self):
        return self.__diem

    @diem.setter
    def diem(self, value):
        value = int(value)
        if value < 0 or value > 100:
            raise ValueError("Điểm sự kiện phải từ 0 đến 100.")
        self.__diem = value

    @property
    def suc_chua(self):
        return self.__suc_chua

    @suc_chua.setter
    def suc_chua(self, value):
        value = int(value)
        if value <= 0:
            raise ValueError("Sức chứa phải lớn hơn 0.")
        self.__suc_chua = value

    def to_dict(self):
        return {
            "ma_sk": self.ma_sk,
            "ten_sk": self.ten_sk,
            "ngay": self.ngay,
            "dia_diem": self.dia_diem,
            "diem": self.diem,
            "suc_chua": self.suc_chua
        }

    def __str__(self):
        return f"{self.ma_sk} - {self.ten_sk} - {self.ngay}"
