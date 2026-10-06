# ============================================================
# QUẢN LÝ CÂU LẠC BỘ SINH VIÊN
# GIAO DIỆN TKINTER
# ============================================================

import tkinker as tk
from models import Member, Event, Registration, Fee
from data.data_manager import DataManager
from services.club_service import ClubService
from ui.login_window import LoginWindow
from ui.main_window import MainWindow
from utils.helpers import print_header, print_rows, money

def main():
    # Khởi tạo lớp quản lý dữ liệu và lớp nghiệp vụ.
    manager = DataManager("database")
    service = ClubService(manager)

    # Tạo cửa sổ chính
    root = tk.Tk()

    # Ẩn cửa sổ chính trong lúc đăng nhập
    root.withdraw()

    # Sau khi đăng nhập thành công
    def open_main_window():
        root.deiconify()
        MainWindow(root, service)

    # Hiển thị màn hình đăng nhập
    LoginWindow(root, open_main_window)

    # Chạy chương trình
    root.mainloop()

if __name__ == "__main__":
    main()