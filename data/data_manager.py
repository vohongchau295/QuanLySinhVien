# ============================================================
# DATA MANAGER - QUẢN LÝ ĐỌC/GHI JSON
# ============================================================

import json
import os
import shutil

from data.data_defaults import get_default_data


class DataManager:
    """
    Quản lý dữ liệu JSON.

    Private:
        __data_dir
        __files

    Các phương thức public:
        load()
        save()
        ensure_files()
        reset_data()
    """

    def __init__(self, data_dir="database"):
        self.__data_dir = data_dir

        self.__files = {
            "members": "members.json",
            "events": "events.json",
            "registrations": "registrations.json",
            "fees": "fees.json"
        }

        self.ensure_files()

    def __path(self, key):
        """Private method: lấy đường dẫn file theo key."""
        if key not in self.__files:
            raise KeyError(f"Không tồn tại nhóm dữ liệu: {key}")

        return os.path.join(
            self.__data_dir,
            self.__files[key]
        )

    def ensure_files(self):
        """Tạo file JSON nếu chưa có."""
        os.makedirs(self.__data_dir, exist_ok=True)

        defaults = get_default_data()

        for key in self.__files:
            path = self.__path(key)

            if not os.path.exists(path):
                self.save(key, defaults[key])

    def load(self, key):
        """Đọc dữ liệu từ JSON."""
        path = self.__path(key)

        try:
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)

            return data if isinstance(data, list) else []

        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save(self, key, rows):
        """Lưu dữ liệu vào JSON và tạo file backup."""
        path = self.__path(key)

        os.makedirs(self.__data_dir, exist_ok=True)

        try:
            if os.path.exists(path):
                shutil.copy2(path, path + ".bak")

            with open(path, "w", encoding="utf-8") as file:
                json.dump(
                    rows,
                    file,
                    ensure_ascii=False,
                    indent=4
                )

            return True

        except OSError:
            return False

    def reset_data(self):
        """Khôi phục toàn bộ dữ liệu về dữ liệu mẫu."""
        defaults = get_default_data()

        for key in self.__files:
            self.save(key, defaults[key])

        return True
