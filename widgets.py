import tkinter as tk
from tkinter import ttk
from config import COLORS

class DateEntry(ttk.Frame):
    def __init__(self, master, textvariable=None, **kwargs):
        super().__init__(master)
        self.var = textvariable or tk.StringVar()
        self.entry = ttk.Entry(self, textvariable=self.var, **kwargs)
        self.entry.pack(side="left", fill="x", expand=True)
        ttk.Button(self, text="📅", width=3,
                   command=self.set_today).pack(side="right", padx=(4,0))

    def set_today(self):
        from datetime import datetime
        self.var.set(datetime.now().strftime("%d/%m/%Y"))

    def get(self):
        return self.var.get()

    def insert(self, index, value):
        self.entry.insert(index, value)


class MemberCard(tk.Frame):
    """Custom Widget: thẻ thành viên CLB."""
    def __init__(self, master, member=None):
        super().__init__(master, bg=COLORS["blue"],
                         highlightbackground="#0F5FAF",
                         highlightthickness=1)
        self.configure(padx=18, pady=16)

        tk.Label(
            self, text="🔔   THẺ THÀNH VIÊN CLB   👥",
            bg=COLORS["blue"], fg="white",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w")

        self.name = tk.Label(
            self, text="", bg=COLORS["blue"],
            fg="white", font=("Segoe UI", 14, "bold")
        )
        self.name.pack(anchor="w", pady=(18, 7))

        self.info = tk.Label(
            self, text="", bg=COLORS["blue"],
            fg="white", justify="left",
            font=("Segoe UI", 9), pady=2
        )
        self.info.pack(anchor="w")

        self.qr = tk.Canvas(
            self, width=110, height=110,
            bg="white", highlightthickness=0
        )
        self.qr.pack(anchor="center", pady=15)

        self.quote = tk.Label(
            self, text="“Cùng nhau tạo nên\nnhững giá trị tốt đẹp hơn.”",
            bg=COLORS["blue"], fg="white",
            justify="center", font=("Segoe UI", 8, "italic")
        )
        self.quote.pack()

        self.set_member(member)

    def draw_fake_qr(self, seed_text):
        self.qr.delete("all")
        rng = __import__("random").Random(seed_text or "CLB")
        n = 15
        cell = 7

        for r in range(n):
            for c in range(n):
                if rng.random() > 0.55:
                    self.qr.create_rectangle(
                        c*cell+3, r*cell+3,
                        c*cell+3+cell, r*cell+3+cell,
                        fill="#111111", outline=""
                    )

        # three finder-like squares
        for x, y in [(0,0), (n-4,0), (0,n-4)]:
            self.qr.create_rectangle(
                x*cell+3, y*cell+3,
                (x+4)*cell+3, (y+4)*cell+3,
                fill="#111111", outline=""
            )
            self.qr.create_rectangle(
                (x+1)*cell+3, (y+1)*cell+3,
                (x+3)*cell+3, (y+3)*cell+3,
                fill="white", outline=""
            )
            self.qr.create_rectangle(
                (x+2)*cell+3, (y+2)*cell+3,
                (x+2)*cell+3+cell, (y+2)*cell+3+cell,
                fill="#111111", outline=""
            )

    def set_member(self, member):
        if not member:
            self.name.config(text="Chưa chọn thành viên")
            self.info.config(text="Mã TV: --\nBan: --\nĐiểm hoạt động: --\nTrạng thái: --")
            self.draw_fake_qr("empty")
            return

        self.name.config(text=member["ho_ten"])
        self.info.config(
            text=(
                f"Mã TV: {member['ma_tv']}\n"
                f"Ban: {member['ban']}\n"
                f"Điểm hoạt động: {member['diem']}\n"
                f"Trạng thái: {member['trang_thai']}"
            )
        )
        self.draw_fake_qr(member["ma_tv"])


class StatCard(tk.Frame):
    def __init__(self, master, title, value, icon, color):
        super().__init__(
            master, bg=COLORS["white"],
            highlightbackground=COLORS["border"],
            highlightthickness=1, padx=16, pady=12
        )
        tk.Label(
            self, text=icon, bg=COLORS["white"], fg=color,
            font=("Segoe UI", 20)
        ).pack(side="left", padx=(0, 12))

        box = tk.Frame(self, bg=COLORS["white"])
        box.pack(side="left", fill="both", expand=True)

        tk.Label(
            box, text=title, bg=COLORS["white"],
            fg=COLORS["muted"], font=("Segoe UI", 9)
        ).pack(anchor="w")

        tk.Label(
            box, text=value, bg=COLORS["white"],
            fg=color, font=("Segoe UI", 17, "bold")
        ).pack(anchor="w")
