# QUẢN LÝ CÂU LẠC BỘ SINH VIÊN

## Chạy
Mở folder bằng VS Code rồi chạy:

```bash
python main.py
```

Tài khoản mẫu:
- admin / 123
- user / 123

## OOP
- **Private:** `__ma_tv`, `__diem`, `__files`, `__validate_email()`...
- **Protected:** `_data_dir`, `_db`, `_require_text()`, `_date()`...
- **Public:** `to_dict()`, `cong_diem()`, `load()`, `save()`.
- `@property` + setter dùng để đóng gói dữ liệu và kiểm tra trước khi gán.

## Ràng buộc
- Thành viên: mã `TV001`, email/SĐT hợp lệ, ngày hợp lệ, điểm >= 0, trạng thái hợp lệ.
- Sự kiện: mã `SK001`, thông tin bắt buộc, ngày hợp lệ, điểm 1-100, không trùng mã.
- Đăng ký: thành viên và sự kiện phải tồn tại, không đăng ký trùng.
- Khoản thu: mã `TH001`, thành viên tồn tại, số tiền > 0, trạng thái hợp lệ.

## Hàm tiện ích
`utils.py` chứa các hàm dùng chung: kiểm tra rỗng, email, SĐT, ngày, số nguyên, định dạng tiền, tạo mã, tìm theo ID.

## Luồng
Tkinter UI -> ClubService -> validation/OOP -> DataManager -> JSON

`DataManager.save()` tạo file `.bak` trước khi ghi để có bản sao lưu.