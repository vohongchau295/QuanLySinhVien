# ============================================================
# UTILS - NHÓM HÀM TIỆN ÍCH DÙNG CHUNG
# ============================================================

import re
from datetime import datetime

# Kiểm tra chuỗi có tồn tại và không được để trống
def is_non_empty(value):
    return isinstance(value, str) and bool(value.strip())

# Kiểm tra email có đúng định dạng cơ bản hay không
def is_valid_email(email):
    return bool(
        re.match(
            r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
            str(email).strip()
        )
    )

# Kiểm tra số điện thoại Việt Nam
# Chấp nhận dạng: 0********* hoặc +84*********
def is_valid_phone(phone):
    return bool(
        re.match(
            r"^(0|\+84)\d{9,10}$",
            str(phone).replace(" ", "").strip()
        )
    )

# Kiểm tra ngày có đúng định dạng dd/mm/yyyy hay không
def is_valid_date(value):
    try:
        datetime.strptime(
            str(value).strip(),
            "%d/%m/%Y"
        )
        return True
    except (ValueError, TypeError):
        return False

# Chuyển giá trị thành số nguyên an toàn
# Nếu chuyển đổi thất bại thì trả về giá trị mặc định
def safe_int(value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

# Định dạng số tiền theo dạng có dấu phân cách hàng nghìn
# Ví dụ: 100000 -> 100,000đ
def money(value):
    return f"{safe_int(value):,}đ"

# Tự động tạo mã mới theo dạng PREFIX001
# Ví dụ: TV001, TV002 -> mã tiếp theo là TV003
def generate_code(prefix, rows, field):
    max_number = 0

    for row in rows:
        code = str(row.get(field, ""))

        # Kiểm tra mã có đúng tiền tố và phần sau là số
        if code.startswith(prefix) and code[len(prefix):].isdigit():
            max_number = max(
                max_number,
                int(code[len(prefix):])
            )

    return f"{prefix}{max_number + 1:03d}"

# Tìm một bản ghi theo mã
# Nếu tìm thấy thì trả về bản ghi, nếu không thì trả về None
def find_by_id(rows, field, value):
    return next(
        (row for row in rows if row.get(field) == value),
        None
    )

# In tiêu đề dùng chung cho các màn hình/chức năng
def print_header(title):
    print("\n" + "=" * 60)
    print(title.center(60))
    print("=" * 60)