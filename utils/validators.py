# ============================================================
# VALIDATORS - CÁC HÀM KIỂM TRA DỮ LIỆU
# ============================================================

import re
from datetime import datetime


def is_non_empty(value):
    """Kiểm tra chuỗi không được rỗng."""
    return isinstance(value, str) and bool(value.strip())


def is_valid_email(email):
    """Kiểm tra email có đúng định dạng cơ bản."""
    return bool(
        re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", str(email).strip())
    )


def is_valid_phone(phone):
    """Kiểm tra số điện thoại Việt Nam."""
    return bool(
        re.match(
            r"^(0|\+84)\d{9,10}$",
            str(phone).replace(" ", "").strip()
        )
    )


def is_valid_date(value):
    """Kiểm tra ngày theo định dạng dd/mm/yyyy."""
    try:
        datetime.strptime(str(value).strip(), "%d/%m/%Y")
        return True
    except (ValueError, TypeError):
        return False


def is_valid_code(code, prefix):
    """Kiểm tra mã có dạng PREFIX + 3 chữ số."""
    return bool(
        re.fullmatch(rf"{re.escape(prefix)}\d{{3}}", str(code).strip())
    )


def is_positive_number(value):
    """Kiểm tra số lớn hơn 0."""
    try:
        return float(value) > 0
    except (ValueError, TypeError):
        return False
