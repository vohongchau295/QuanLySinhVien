# ============================================================
# BASE MODEL - LỚP CHA DÙNG CHUNG
# ============================================================

from utils.validators import (
    is_non_empty,
    is_valid_date,
    is_positive_number
)


class BaseModel:
    """
    Lớp cha chứa các phương thức protected dùng chung.
    Các lớp con có thể sử dụng lại các phương thức này.
    """

    def _require_text(self, value, field_name):
        """Kiểm tra trường dạng chuỗi không được rỗng."""
        if not is_non_empty(value):
            raise ValueError(f"{field_name} không được để trống.")

    def _require_date(self, value, field_name):
        """Kiểm tra ngày đúng định dạng dd/mm/yyyy."""
        if not is_valid_date(value):
            raise ValueError(
                f"{field_name} phải có dạng dd/mm/yyyy."
            )

    def _require_positive(self, value, field_name):
        """Kiểm tra số phải lớn hơn 0."""
        if not is_positive_number(value):
            raise ValueError(
                f"{field_name} phải lớn hơn 0."
            )
