# ============================================================
# MODELS - OOP, ĐÓNG GÓI, PRIVATE/PROTECTED VÀ RÀNG BUỘC
# ============================================================
import json
import os
import random
import re
import shutil
from datetime import datetime

from utils import is_non_empty, is_valid_email, is_valid_phone

# ============================================================
# BASE MODEL
# ============================================================
class BaseModel:
    """Class cha chứa các hàm protected dùng chung."""

    def _require_text(self, value, field):
        value = str(value).strip()
        if not value:
            raise ValueError(f"{field} không được để trống.")
        return value

    def _positive_int(self, value, field):
        try:
            value = int(value)
        except (ValueError, TypeError):
            raise ValueError(f"{field} phải là số nguyên.")
        if value <= 0:
            raise ValueError(f"{field} phải lớn hơn 0.")
        return value

    def _date(self, value, field):
        value = self._require_text(value, field)
        try:
            datetime.strptime(value, "%d/%m/%Y")
        except ValueError:
            raise ValueError(f"{field} phải có dạng dd/mm/yyyy.")
        return value

# ============================================================
# MEMBER
# ============================================================
class Member(BaseModel):
    def __init__(self, ma_tv, ho_ten, email, sdt, ban,
                 ngay_tham_gia, diem=0, trang_thai="Hoạt động"):
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
        value = self._require_text(value, "Mã thành viên")
        if not re.fullmatch(r"TV\d{3,}", value):
            raise ValueError("Mã thành viên phải có dạng TV001.")
        self.__ma_tv = value

    @property
    def ho_ten(self):
        return self.__ho_ten

    @ho_ten.setter
    def ho_ten(self, value):
        value = self._require_text(value, "Họ tên")
        if len(value) < 2:
            raise ValueError("Họ tên phải có ít nhất 2 ký tự.")
        self.__ho_ten = value

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        value = self._require_text(value, "Email")
        if not is_valid_email(value):
            raise ValueError("Email không đúng định dạng.")
        self.__email = value

    @property
    def sdt(self):
        return self.__sdt

    @sdt.setter
    def sdt(self, value):
        value = self._require_text(value, "Số điện thoại")
        if not is_valid_phone(value):
            raise ValueError("Số điện thoại không hợp lệ.")
        self.__sdt = value

    @property
    def ban(self):
        return self.__ban

    @ban.setter
    def ban(self, value):
        self.__ban = self._require_text(value, "Ban")

    @property
    def ngay_tham_gia(self):
        return self.__ngay_tham_gia

    @ngay_tham_gia.setter
    def ngay_tham_gia(self, value):
        self.__ngay_tham_gia = self._date(value, "Ngày tham gia")

    @property
    def diem(self):
        return self.__diem

    @diem.setter
    def diem(self, value):
        try:
            value = int(value)
        except (ValueError, TypeError):
            raise ValueError("Điểm phải là số nguyên.")
        if value < 0:
            raise ValueError("Điểm không được âm.")
        self.__diem = value

    @property
    def trang_thai(self):
        return self.__trang_thai

    @trang_thai.setter
    def trang_thai(self, value):
        value = self._require_text(value, "Trạng thái")
        if value not in ["Hoạt động", "Tạm khóa", "Đã rời CLB"]:
            raise ValueError("Trạng thái thành viên không hợp lệ.")
        self.__trang_thai = value

    def cong_diem(self, diem):
        """Public method cộng điểm có kiểm tra."""
        self.__diem += self._positive_int(diem, "Điểm cộng")

    def to_dict(self):
        return {
            "ma_tv": self.__ma_tv, "ho_ten": self.__ho_ten,
            "email": self.__email, "sdt": self.__sdt,
            "ban": self.__ban, "ngay_tham_gia": self.__ngay_tham_gia,
            "diem": self.__diem, "trang_thai": self.__trang_thai
        }

    def __str__(self):
        return f"{self.__ma_tv} - {self.__ho_ten}"

# ============================================================
# EVENT
# ============================================================
class Event(BaseModel):
    def __init__(self, ma_sk, ten_sk, ngay, dia_diem, diem=10):
        self.ma_sk = ma_sk
        self.ten_sk = ten_sk
        self.ngay = ngay
        self.dia_diem = dia_diem
        self.diem = diem

    @property
    def ma_sk(self): return self.__ma_sk
    @ma_sk.setter
    def ma_sk(self, value):
        value = self._require_text(value, "Mã sự kiện")
        if not re.fullmatch(r"SK\d{3,}", value):
            raise ValueError("Mã sự kiện phải có dạng SK001.")
        self.__ma_sk = value

    @property
    def ten_sk(self): return self.__ten_sk
    @ten_sk.setter
    def ten_sk(self, value): self.__ten_sk = self._require_text(value, "Tên sự kiện")

    @property
    def ngay(self): return self.__ngay
    @ngay.setter
    def ngay(self, value): self.__ngay = self._date(value, "Ngày sự kiện")

    @property
    def dia_diem(self): return self.__dia_diem
    @dia_diem.setter
    def dia_diem(self, value): self.__dia_diem = self._require_text(value, "Địa điểm")

    @property
    def diem(self): return self.__diem
    @diem.setter
    def diem(self, value):
        try: value = int(value)
        except (ValueError, TypeError): raise ValueError("Điểm phải là số nguyên.")
        if not 1 <= value <= 100: raise ValueError("Điểm sự kiện phải từ 1 đến 100.")
        self.__diem = value

    def to_dict(self):
        return {"ma_sk": self.__ma_sk, "ten_sk": self.__ten_sk,
                "ngay": self.__ngay, "dia_diem": self.__dia_diem,
                "diem": self.__diem}

# ============================================================
# REGISTRATION
# ============================================================
class Registration(BaseModel):
    def __init__(self, ma_dk, ma_tv, ma_sk, ngay_dk,
                 trang_thai="Đã đăng ký", co_mat="Chưa điểm danh"):
        self.ma_dk = ma_dk
        self.ma_tv = ma_tv
        self.ma_sk = ma_sk
        self.ngay_dk = ngay_dk
        self.trang_thai = trang_thai
        self.co_mat = co_mat

    @property
    def ma_dk(self): return self.__ma_dk
    @ma_dk.setter
    def ma_dk(self, value):
        value = self._require_text(value, "Mã đăng ký")
        if not re.fullmatch(r"DK\d{3,}", value):
            raise ValueError("Mã đăng ký phải có dạng DK001.")
        self.__ma_dk = value

    @property
    def ma_tv(self): return self.__ma_tv
    @ma_tv.setter
    def ma_tv(self, value): self.__ma_tv = self._require_text(value, "Mã thành viên")

    @property
    def ma_sk(self): return self.__ma_sk
    @ma_sk.setter
    def ma_sk(self, value): self.__ma_sk = self._require_text(value, "Mã sự kiện")

    @property
    def ngay_dk(self): return self.__ngay_dk
    @ngay_dk.setter
    def ngay_dk(self, value): self.__ngay_dk = self._date(value, "Ngày đăng ký")

    @property
    def trang_thai(self): return self.__trang_thai
    @trang_thai.setter
    def trang_thai(self, value):
        value = self._require_text(value, "Trạng thái")
        if value not in ["Đã đăng ký", "Đã hủy"]:
            raise ValueError("Trạng thái đăng ký không hợp lệ.")
        self.__trang_thai = value

    @property
    def co_mat(self): return self.__co_mat
    @co_mat.setter
    def co_mat(self, value):
        value = self._require_text(value, "Điểm danh")
        if value not in ["Có mặt", "Chưa điểm danh", "Vắng"]:
            raise ValueError("Trạng thái điểm danh không hợp lệ.")
        self.__co_mat = value

    def diem_danh(self, co_mat=True):
        self.__co_mat = "Có mặt" if co_mat else "Vắng"

    def to_dict(self):
        return {"ma_dk": self.__ma_dk, "ma_tv": self.__ma_tv,
                "ma_sk": self.__ma_sk, "ngay_dk": self.__ngay_dk,
                "trang_thai": self.__trang_thai, "co_mat": self.__co_mat}

# ============================================================
# FEE
# ============================================================
class Fee(BaseModel):
    def __init__(self, ma_thu, ma_tv, loai_thu, so_tien,
                 noi_dung, trang_thai="Chưa đóng", ngay_thu=""):
        self.ma_thu = ma_thu
        self.ma_tv = ma_tv
        self.loai_thu = loai_thu
        self.so_tien = so_tien
        self.noi_dung = noi_dung
        self.trang_thai = trang_thai
        self.ngay_thu = ngay_thu

    @property
    def ma_thu(self): return self.__ma_thu
    @ma_thu.setter
    def ma_thu(self, value):
        value = self._require_text(value, "Mã khoản thu")
        if not re.fullmatch(r"TH\d{3,}", value):
            raise ValueError("Mã khoản thu phải có dạng TH001.")
        self.__ma_thu = value

    @property
    def ma_tv(self): return self.__ma_tv
    @ma_tv.setter
    def ma_tv(self, value): self.__ma_tv = self._require_text(value, "Mã thành viên")

    @property
    def loai_thu(self): return self.__loai_thu
    @loai_thu.setter
    def loai_thu(self, value): self.__loai_thu = self._require_text(value, "Loại thu")

    @property
    def so_tien(self): return self.__so_tien
    @so_tien.setter
    def so_tien(self, value):
        try: value = int(value)
        except (ValueError, TypeError): raise ValueError("Số tiền phải là số nguyên.")
        if value <= 0: raise ValueError("Số tiền phải lớn hơn 0.")
        self.__so_tien = value

    @property
    def noi_dung(self): return self.__noi_dung
    @noi_dung.setter
    def noi_dung(self, value): self.__noi_dung = self._require_text(value, "Nội dung")

    @property
    def trang_thai(self): return self.__trang_thai
    @trang_thai.setter
    def trang_thai(self, value):
        value = self._require_text(value, "Trạng thái")
        if value not in ["Đã đóng", "Chưa đóng"]:
            raise ValueError("Trạng thái khoản thu không hợp lệ.")
        self.__trang_thai = value

    @property
    def ngay_thu(self): return self.__ngay_thu
    @ngay_thu.setter
    def ngay_thu(self, value):
        value = str(value).strip()
        if self.trang_thai == "Chưa đóng":
            self.__ngay_thu = ""
            return
        self.__ngay_thu = self._date(value, "Ngày thu")

    def danh_dau_da_dong(self, ngay_thu):
        self.__trang_thai = "Đã đóng"
        self.__ngay_thu = self._date(ngay_thu, "Ngày thu")

    def to_dict(self):
        return {"ma_thu": self.__ma_thu, "ma_tv": self.__ma_tv,
                "loai_thu": self.__loai_thu, "so_tien": self.__so_tien,
                "noi_dung": self.__noi_dung, "trang_thai": self.__trang_thai,
                "ngay_thu": self.__ngay_thu}

# ============================================================
# DATA MANAGER
# ============================================================
class DataManager:
    """Đọc/ghi JSON. _data_dir protected, __files private."""

    def __init__(self, data_dir="data"):
        self._data_dir = data_dir
        self.__files = {
            "members": "members.json", "events": "events.json",
            "registrations": "registrations.json",
            "fees": "fees.json", "users": "users.json"
        }
        self.__ensure_files()

    def __path(self, key):
        if key not in self.__files:
            raise KeyError(f"Loại dữ liệu không hợp lệ: {key}")
        return os.path.join(self._data_dir, self.__files[key])

    def __ensure_files(self):
        os.makedirs(self._data_dir, exist_ok=True)
        for key in self.__files:
            if not os.path.exists(self.__path(key)):
                self.save(key, self.__defaults()[key])

    def __defaults(self):
        return {
            "members": [
                Member("TV001","Nguyễn Văn A","a@gmail.com","0987654321","Truyền thông","22/09/2026",50).to_dict(),
                Member("TV002","Trần Thị B","b@gmail.com","0912345678","Sự kiện","23/09/2026",40).to_dict(),
                Member("TV003","Lê Văn C","c@gmail.com","0923456789","Media","24/09/2026",30).to_dict(),
                Member("TV004","Phạm Thị D","d@gmail.com","0934567890","Truyền thông","25/09/2026",25).to_dict(),
                Member("TV005","Hoàng Văn E","e@gmail.com","0945678901","Sự kiện","26/09/2026",20).to_dict()
            ],
            "events": [
                Event("SK001","Workshop Python","25/09/2026","Phòng A101",10).to_dict(),
                Event("SK002","Hội thảo TMĐT","27/09/2026","Phòng B102",15).to_dict(),
                Event("SK003","Cuộc thi ảnh","10/10/2026","Sân trường",10).to_dict(),
                Event("SK004","Workshop UI/UX","25/09/2026","Phòng B201",10).to_dict(),
                Event("SK005","Team Building","02/10/2026","Sân vận động HUIT",15).to_dict()
            ],
            "registrations": [
                Registration("DK001","TV001","SK001","22/09/2026","Đã đăng ký","Có mặt").to_dict(),
                Registration("DK002","TV002","SK002","23/09/2026","Đã đăng ký","Có mặt").to_dict(),
                Registration("DK003","TV003","SK003","24/09/2026","Đã đăng ký","Có mặt").to_dict()
            ],
            "fees": [
                Fee("TH001","TV001","Hội phí",100000,"Hội phí năm 2026","Đã đóng","22/09/2026").to_dict(),
                Fee("TH002","TV002","Hội phí",100000,"Hội phí năm 2026","Chưa đóng","").to_dict(),
                Fee("TH003","TV003","Hội phí",100000,"Hội phí năm 2026","Đã đóng","23/09/2026").to_dict(),
                Fee("TH004","TV004","Hội phí",100000,"Hội phí năm 2026","Đã đóng","24/09/2026").to_dict()
            ],
            "users": [
                {"username":"admin","password":"123","role":"Quản trị viên"},
                {"username":"user","password":"123","role":"Người dùng"}
            ]
        }

    def load(self, key):
        try:
            with open(self.__path(key), "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save(self, key, rows):
        if not isinstance(rows, list):
            return False
        os.makedirs(self._data_dir, exist_ok=True)
        path = self.__path(key)
        try:
            if os.path.exists(path):
                shutil.copy2(path, path + ".bak")
            with open(path, "w", encoding="utf-8") as f:
                json.dump(rows, f, ensure_ascii=False, indent=2)
            return True
        except OSError:
            return False

    def seed(self):
        members = self.load("members")
        start = len(members) + 1
        for i in range(start, start + 5):
            members.append(Member(
                f"TV{i:03d}", f"Thành viên mẫu {i}", f"tv{i}@gmail.com",
                f"09{random.randint(10000000,99999999)}",
                random.choice(["Truyền thông","Sự kiện","Media"]),
                "30/09/2026", random.randint(5,40)
            ).to_dict())
        self.save("members", members)
        return members

# ============================================================
# CLUB SERVICE - NGHIỆP VỤ VÀ VALIDATION
# ============================================================
class ClubService:
    def __init__(self, manager):
        self._db = manager  # protected

    # Private methods: chỉ dùng bên trong ClubService.
    def __validate_email(self, email):
        return is_valid_email(email)

    def __validate_phone(self, phone):
        return is_valid_phone(phone)

    def __validate_date(self, value):
        try:
            datetime.strptime(str(value).strip(), "%d/%m/%Y")
            return True
        except (ValueError, TypeError):
            return False

    def login(self, username, password):
        username = str(username).strip()
        return next((u for u in self._db.load("users")
                     if u["username"] == username and u["password"] == password), None)

    def validate_member(self, data, existing_id=None):
        fields = ["ma_tv","ho_ten","email","sdt","ban","ngay_tham_gia"]
        if not all(is_non_empty(str(data.get(k,""))) for k in fields):
            return False, "Vui lòng nhập đầy đủ thông tin thành viên."
        if not self.__validate_email(data["email"]):
            return False, "Email không đúng định dạng."
        if not self.__validate_phone(data["sdt"]):
            return False, "Số điện thoại không hợp lệ."
        if not re.fullmatch(r"TV\d{3,}", data["ma_tv"].strip()):
            return False, "Mã thành viên phải có dạng TV001."
        if not self.__validate_date(data["ngay_tham_gia"]):
            return False, "Ngày tham gia phải có dạng dd/mm/yyyy."
        rows = self._db.load("members")
        if any(x["ma_tv"] == data["ma_tv"].strip() and x["ma_tv"] != existing_id for x in rows):
            return False, "Mã thành viên đã tồn tại."
        return True, "OK"

    def validate_event(self, data, existing_id=None):
        if not all(is_non_empty(str(data.get(k,""))) for k in ["ma_sk","ten_sk","ngay","dia_diem"]):
            return False, "Vui lòng nhập đầy đủ thông tin sự kiện."
        if not re.fullmatch(r"SK\d{3,}", data["ma_sk"].strip()):
            return False, "Mã sự kiện phải có dạng SK001."
        try: diem = int(data.get("diem",0))
        except (ValueError,TypeError): return False, "Điểm phải là số nguyên."
        if not 1 <= diem <= 100: return False, "Điểm sự kiện phải từ 1 đến 100."
        if not self.__validate_date(data["ngay"]):
            return False, "Ngày sự kiện phải có dạng dd/mm/yyyy."
        rows = self._db.load("events")
        if any(x["ma_sk"] == data["ma_sk"].strip() and x["ma_sk"] != existing_id for x in rows):
            return False, "Mã sự kiện đã tồn tại."
        return True, "OK"

    def validate_registration(self, ma_tv, ma_sk):
        members = self._db.load("members")
        events = self._db.load("events")
        regs = self._db.load("registrations")
        if not any(x["ma_tv"] == ma_tv for x in members):
            return False, "Thành viên không tồn tại."
        if not any(x["ma_sk"] == ma_sk for x in events):
            return False, "Sự kiện không tồn tại."
        if any(x["ma_tv"] == ma_tv and x["ma_sk"] == ma_sk and x["trang_thai"] == "Đã đăng ký" for x in regs):
            return False, "Thành viên đã đăng ký sự kiện này."
        return True, "OK"

    def validate_fee(self, data, existing_id=None):
        required = ["ma_thu","ma_tv","loai_thu","so_tien","noi_dung"]
        if not all(is_non_empty(str(data.get(k,""))) for k in required):
            return False, "Vui lòng nhập đầy đủ thông tin khoản thu."
        if not re.fullmatch(r"TH\d{3,}", data["ma_thu"].strip()):
            return False, "Mã khoản thu phải có dạng TH001."
        try: amount = int(data["so_tien"])
        except (ValueError,TypeError): return False, "Số tiền phải là số nguyên."
        if amount <= 0: return False, "Số tiền phải lớn hơn 0."
        if data.get("trang_thai") not in ["Đã đóng","Chưa đóng"]:
            return False, "Trạng thái khoản thu không hợp lệ."
        if not any(x["ma_tv"] == data["ma_tv"].strip() for x in self._db.load("members")):
            return False, "Mã thành viên không tồn tại."
        if any(x["ma_thu"] == data["ma_thu"].strip() and x["ma_thu"] != existing_id for x in self._db.load("fees")):
            return False, "Mã khoản thu đã tồn tại."
        return True, "OK"

    def stats(self):
        members = self._db.load("members")
        events = self._db.load("events")
        regs = self._db.load("registrations")
        fees = self._db.load("fees")
        return {
            "members": len(members),
            "events": len(events),
            "participants": len(regs),
            "paid": sum(f["so_tien"] for f in fees if f["trang_thai"] == "Đã đóng"),
            "unpaid": sum(f["so_tien"] for f in fees if f["trang_thai"] != "Đã đóng")
        }
