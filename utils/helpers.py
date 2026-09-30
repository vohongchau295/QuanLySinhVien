# ============================================================
# HELPERS - CÁC HÀM TIỆN ÍCH DÙNG CHUNG
# ============================================================

def safe_int(value, default=0):
    """Chuyển dữ liệu sang int an toàn."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def money(value):
    """Định dạng số tiền."""
    return f"{safe_int(value):,}đ"


def generate_code(prefix, rows, field):
    """Tạo mã tiếp theo theo dạng PREFIX001."""
    max_number = 0

    for row in rows:
        code = str(row.get(field, ""))

        if code.startswith(prefix) and code[len(prefix):].isdigit():
            max_number = max(
                max_number,
                int(code[len(prefix):])
            )

    return f"{prefix}{max_number + 1:03d}"


def find_by_id(rows, field, value):
    """Tìm bản ghi theo mã."""
    for row in rows:
        if row.get(field) == value:
            return row
    return None


def print_header(title):
    """In tiêu đề dùng chung."""
    print("\n" + "=" * 60)
    print(title.center(60))
    print("=" * 60)


def print_rows(rows):
    """In danh sách dictionary."""
    if not rows:
        print("Không có dữ liệu.")
        return

    for row in rows:
        print(row)
