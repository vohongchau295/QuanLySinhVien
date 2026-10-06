import tkinter as tk
from tkinter import ttk, messagebox


class LoginWindow:
    def __init__(self, root, on_login):
        self.root = root
        self.on_login = on_login

        self.window = tk.Toplevel(root)
        self.window.title("Đăng nhập")
        self.window.geometry("400x300")
        self.window.resizable(False, False)

        ttk.Label(
            self.window,
            text="QUẢN LÝ CLB SINH VIÊN",
            font=("Arial", 16, "bold")
        ).pack(pady=30)

        ttk.Label(self.window, text="Tên đăng nhập").pack()

        self.username = ttk.Entry(self.window, width=30)
        self.username.pack(pady=5)

        ttk.Label(self.window, text="Mật khẩu").pack()

        self.password = ttk.Entry(
            self.window,
            width=30,
            show="*"
        )
        self.password.pack(pady=5)

        ttk.Button(
            self.window,
            text="Đăng nhập",
            command=self.login
        ).pack(pady=20)

    def login(self):
        username = self.username.get()
        password = self.password.get()

        # Tạm thời dùng để kiểm tra giao diện
        if username == "admin" and password == "admin":
            self.window.destroy()
            self.on_login()
        else:
            messagebox.showerror(
                "Lỗi",
                "Tên đăng nhập hoặc mật khẩu không đúng!"
            )