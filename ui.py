# ============================================================
# UI TKINTER - GIAO DIỆN CHÍNH
# ============================================================
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv, json, random, urllib.request
from datetime import datetime
from config import COLORS, APP_TITLE, WINDOW_SIZE
from widgets import DateEntry, MemberCard, StatCard

# ============================================================
# LOGIN
# ============================================================
class LoginWindow(tk.Tk):
    def __init__(self, on_login):
        super().__init__()
        self.on_login = on_login
        self.title("Đăng nhập - CLB Sinh viên")
        self.geometry("500x610")
        self.resizable(False, False)
        self.configure(bg=COLORS["bg"])
        self.setup_style()
        self.build()

    def setup_style(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure("TEntry", padding=10, font=("Segoe UI", 10))
        s.configure("TButton", font=("Segoe UI", 10, "bold"), padding=(12, 9))
        s.configure("Primary.TButton", background=COLORS["blue"], foreground="white")
        s.map("Primary.TButton", background=[("active", COLORS["blue_dark"])])

    def build(self):
        outer = tk.Frame(self, bg=COLORS["bg"], padx=45, pady=35)
        outer.pack(fill="both", expand=True)

        tk.Label(outer, text="👥", bg=COLORS["bg"], fg=COLORS["blue"],
                 font=("Segoe UI Emoji", 64)).pack(pady=(8, 0))
        tk.Label(outer, text="QUẢN LÝ CLB SINH VIÊN",
                 bg=COLORS["bg"], fg="#123E78",
                 font=("Segoe UI", 22, "bold")).pack()
        tk.Label(outer, text="Kết nối - Học hỏi - Phát triển",
                 bg=COLORS["bg"], fg=COLORS["muted"],
                 font=("Segoe UI", 11)).pack(pady=(4, 28))

        card = tk.Frame(outer, bg="white", padx=28, pady=26,
                        highlightbackground="#CFE0F2", highlightthickness=1)
        card.pack(fill="x")

        tk.Label(card, text="Tài khoản", bg="white", fg=COLORS["text"],
                 font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.user = ttk.Entry(card)
        self.user.pack(fill="x", pady=(6, 14))
        self.user.insert(0, "admin")

        tk.Label(card, text="Mật khẩu", bg="white", fg=COLORS["text"],
                 font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.pw = ttk.Entry(card, show="•")
        self.pw.pack(fill="x", pady=(6, 18))
        self.pw.insert(0, "123")

        ttk.Button(card, text="Đăng nhập", style="Primary.TButton",
                   command=self.login).pack(fill="x")
        tk.Label(outer, text="Chưa có tài khoản? Liên hệ Admin",
                 bg=COLORS["bg"], fg=COLORS["muted"],
                 font=("Segoe UI", 9)).pack(pady=18)
        self.bind("<Return>", lambda e: self.login())

    def login(self):
        from models import DataManager, ClubService
        service = ClubService(DataManager())
        user = service.login(self.user.get().strip(), self.pw.get())
        if not user:
            messagebox.showerror("Đăng nhập", "Sai tài khoản hoặc mật khẩu.")
            return
        self.destroy()
        self.on_login(user)


# ============================================================
# MAIN APPLICATION - SIDEBAR STYLE
# ============================================================
class MainApp(tk.Tk):
    def __init__(self, user):
        super().__init__()
        self.user = user

        from models import DataManager, ClubService
        self.db = DataManager()
        self.service = ClubService(self.db)

        self.title(f"Quản lý CLB Sinh viên - {user['username']}")
        self.geometry("1350x800")
        self.minsize(1120, 700)
        self.configure(bg=COLORS["bg"])

        self.current_page = None
        self.pages = {}
        self.nav_buttons = {}

        self.setup_style()
        self.build_header()
        self.build_layout()
        self.show_page("Trang chủ")

    # ---------------- STYLE ----------------
    def setup_style(self):
        s = ttk.Style(self)
        s.theme_use("clam")

        s.configure("TEntry", padding=8, font=("Segoe UI", 9))
        s.configure("TCombobox", padding=8, font=("Segoe UI", 9))
        s.configure("TButton", font=("Segoe UI", 9, "bold"), padding=(10, 7))

        s.configure("Primary.TButton", background=COLORS["blue"],
                    foreground="white", padding=(12, 8))
        s.map("Primary.TButton",
              background=[("active", COLORS["blue_dark"])])

        s.configure("Success.TButton", background=COLORS["green"],
                    foreground="white", padding=(12, 8))
        s.configure("Danger.TButton", background=COLORS["red"],
                    foreground="white", padding=(12, 8))

        s.configure("Treeview", rowheight=32, font=("Segoe UI", 9),
                    background="white", fieldbackground="white",
                    borderwidth=0)
        s.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"),
                    background="#EAF2FA", foreground=COLORS["text"], padding=8)
        s.map("Treeview", background=[("selected", "#DCEEFF")],
              foreground=[("selected", COLORS["text"])])

    # ---------------- HEADER ----------------
    def build_header(self):
        self.header = tk.Frame(
            self, bg="white", height=72,
            highlightbackground="#D8E2EF", highlightthickness=1
        )
        self.header.pack(fill="x", side="top")

        left = tk.Frame(self.header, bg="white")
        left.pack(side="left", padx=22, pady=9)

        tk.Label(left, text="👥", bg="white", fg=COLORS["blue"],
                 font=("Segoe UI Emoji", 34)).pack(side="left", padx=(0, 10))

        titlebox = tk.Frame(left, bg="white")
        titlebox.pack(side="left")
        tk.Label(titlebox, text="QUẢN LÝ CLB SINH VIÊN",
                 bg="white", fg="#123E78",
                 font=("Segoe UI", 17, "bold")).pack(anchor="w")
        tk.Label(titlebox, text="Kết nối - Học hỏi - Phát triển",
                 bg="white", fg=COLORS["muted"],
                 font=("Segoe UI", 9)).pack(anchor="w")

        right = tk.Frame(self.header, bg="white")
        right.pack(side="right", padx=18)

        tk.Label(right, text="●", bg="white", fg=COLORS["blue"],
                 font=("Segoe UI", 16)).pack(side="left", padx=(0, 7))
        tk.Label(right, text=f"Xin chào, {self.user['username']}\n({self.user['role']})",
                 bg="white", fg=COLORS["text"], justify="right",
                 font=("Segoe UI", 9, "bold")).pack(side="left", padx=7)

        ttk.Button(right, text="⇥", width=3,
                   command=self.logout).pack(side="left", padx=(8, 0))

    # ---------------- LAYOUT ----------------
    def build_layout(self):
        body = tk.Frame(self, bg=COLORS["bg"])
        body.pack(fill="both", expand=True)

        self.sidebar = tk.Frame(
            body, bg="#F0F6FC", width=205,
            highlightbackground="#D7E4F1", highlightthickness=1
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.content = tk.Frame(body, bg=COLORS["bg"])
        self.content.pack(side="right", fill="both", expand=True)

        self.build_sidebar()

    def build_sidebar(self):
        tk.Label(self.sidebar, text="MENU", bg="#F0F6FC",
                 fg=COLORS["muted"], font=("Segoe UI", 8, "bold")).pack(
                     anchor="w", padx=18, pady=(18, 8))

        items = [
            ("⌂", "Trang chủ"),
            ("♟", "Thành viên"),
            ("▣", "Sự kiện"),
            ("☑", "Đăng ký & Điểm danh"),
            ("₫", "Khoản thu"),
            ("◔", "Thống kê"),
            ("▤", "Báo cáo"),
        ]

        for icon, name in items:
            btn = tk.Button(
                self.sidebar,
                text=f"  {icon}   {name}",
                anchor="w",
                relief="flat",
                bd=0,
                bg="#F0F6FC",
                fg="#24405F",
                activebackground="#DCEEFF",
                activeforeground=COLORS["blue_dark"],
                font=("Segoe UI", 9, "bold"),
                padx=12, pady=10,
                cursor="hand2",
                command=lambda n=name: self.show_page(n)
            )
            btn.pack(fill="x", padx=9, pady=2)
            self.nav_buttons[name] = btn

        sep = tk.Frame(self.sidebar, bg="#D5E2EE", height=1)
        sep.pack(fill="x", padx=14, pady=14)

        tk.Label(self.sidebar, text="TÀI KHOẢN", bg="#F0F6FC",
                 fg=COLORS["muted"], font=("Segoe UI", 8, "bold")).pack(
                     anchor="w", padx=18, pady=(0, 8))

        tk.Button(
            self.sidebar, text="  ⚙   Cài đặt",
            anchor="w", relief="flat", bd=0,
            bg="#F0F6FC", fg="#24405F",
            activebackground="#DCEEFF",
            font=("Segoe UI", 9, "bold"),
            padx=12, pady=10
        ).pack(fill="x", padx=9)

    # ---------------- PAGE CONTROL ----------------
    def register_page(self, name, builder):
        page = tk.Frame(self.content, bg=COLORS["bg"])
        self.pages[name] = page
        builder(page)

    def show_page(self, name):
        if self.current_page:
            self.current_page.pack_forget()

        if name not in self.pages:
            builders = {
                "Trang chủ": self.build_dashboard,
                "Thành viên": self.build_members,
                "Sự kiện": self.build_events,
                "Đăng ký & Điểm danh": self.build_registrations,
                "Khoản thu": self.build_fees,
                "Thống kê": self.build_stats,
                "Báo cáo": self.build_reports,
            }
            self.register_page(name, builders[name])

        self.current_page = self.pages[name]
        self.current_page.pack(fill="both", expand=True, padx=14, pady=14)

        for n, b in self.nav_buttons.items():
            b.configure(
                bg=COLORS["blue"] if n == name else "#F0F6FC",
                fg="white" if n == name else "#24405F"
            )

        if name == "Trang chủ":
            self.refresh_dashboard()
        elif name == "Thành viên":
            self.refresh_members()
        elif name == "Sự kiện":
            self.refresh_events()
        elif name == "Đăng ký & Điểm danh":
            self.refresh_reg()
        elif name == "Khoản thu":
            self.refresh_fees()
        elif name == "Thống kê":
            self.refresh_stats()

    # ========================================================
    # DASHBOARD
    # ========================================================
    def build_dashboard(self, parent):
        self.dashboard_parent = parent

        top = tk.Frame(parent, bg=COLORS["bg"])
        top.pack(fill="x", pady=(0, 10))

        tk.Label(top, text="Chào mừng bạn đến với hệ thống quản lý CLB sinh viên!",
                 bg=COLORS["bg"], fg=COLORS["text"],
                 font=("Segoe UI", 12, "bold")).pack(anchor="w")
        tk.Label(top, text="Tổng quan hoạt động của câu lạc bộ",
                 bg=COLORS["bg"], fg=COLORS["muted"],
                 font=("Segoe UI", 9)).pack(anchor="w", pady=(2, 0))

        self.dashboard_cards = tk.Frame(parent, bg=COLORS["bg"])
        self.dashboard_cards.pack(fill="x", pady=(0, 10))

        middle = tk.Frame(parent, bg=COLORS["bg"])
        middle.pack(fill="both", expand=True)

        self.upcoming_box = tk.Frame(
            middle, bg="white",
            highlightbackground=COLORS["border"], highlightthickness=1
        )
        self.upcoming_box.pack(side="left", fill="both", expand=True, padx=(0, 7))

        self.top_member_box = tk.Frame(
            middle, bg="white",
            highlightbackground=COLORS["border"], highlightthickness=1
        )
        self.top_member_box.pack(side="right", fill="both", expand=True, padx=(7, 0))

        self.refresh_dashboard()

    def clear_children(self, widget):
        for child in widget.winfo_children():
            child.destroy()

    def refresh_dashboard(self):
        if not hasattr(self, "dashboard_cards"):
            return

        s = self.service.stats()
        self.clear_children(self.dashboard_cards)

        cards = [
            ("👥", "Tổng thành viên", s["members"], COLORS["blue"], "#E8F3FF"),
            ("▦", "Tổng sự kiện", s["events"], COLORS["green"], "#E8FAF1"),
            ("●", "Tổng lượt tham gia", s["participants"], "#F59E0B", "#FFF5DF"),
            ("₫", "Tổng tiền đã thu", f"{s['paid']:,}đ", COLORS["purple"], "#F1ECFF"),
        ]

        for icon, title, value, color, bg in cards:
            card = tk.Frame(self.dashboard_cards, bg=bg,
                            highlightbackground="#D9E5F1", highlightthickness=1,
                            padx=16, pady=13)
            card.pack(side="left", fill="x", expand=True, padx=5)

            tk.Label(card, text=icon, bg=bg, fg=color,
                     font=("Segoe UI Emoji", 22)).pack(side="left", padx=(0, 12))
            info = tk.Frame(card, bg=bg)
            info.pack(side="left")
            tk.Label(info, text=title, bg=bg, fg=COLORS["muted"],
                     font=("Segoe UI", 9)).pack(anchor="w")
            tk.Label(info, text=str(value), bg=bg, fg=color,
                     font=("Segoe UI", 18, "bold")).pack(anchor="w")

        self.clear_children(self.upcoming_box)
        tk.Label(self.upcoming_box, text="▣  Sự kiện sắp tới",
                 bg="white", fg=COLORS["text"],
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=15, pady=(14, 9))

        cols = ("ma", "ten", "ngay", "dia")
        tree = ttk.Treeview(self.upcoming_box, columns=cols,
                            show="headings", height=9)
        for c, h, w in [
            ("ma", "Mã SK", 70),
            ("ten", "Tên sự kiện", 190),
            ("ngay", "Ngày diễn ra", 110),
            ("dia", "Địa điểm", 170),
        ]:
            tree.heading(c, text=h)
            tree.column(c, width=w)
        tree.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        for e in self.db.load("events")[:6]:
            tree.insert("", "end",
                        values=(e["ma_sk"], e["ten_sk"], e["ngay"], e["dia_diem"]))

        self.clear_children(self.top_member_box)
        tk.Label(self.top_member_box, text="♟  Top 5 thành viên tích cực",
                 bg="white", fg=COLORS["text"],
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=15, pady=(14, 9))

        members = sorted(self.db.load("members"),
                         key=lambda x: x.get("diem", 0), reverse=True)[:5]
        maxv = max([m.get("diem", 0) for m in members] + [1])

        for i, m in enumerate(members):
            row = tk.Frame(self.top_member_box, bg="white")
            row.pack(fill="x", padx=15, pady=7)

            tk.Label(row, text=m["ho_ten"], bg="white", fg=COLORS["text"],
                     width=19, anchor="w",
                     font=("Segoe UI", 9)).pack(side="left")

            bar_bg = tk.Frame(row, bg="#E7EEF7", height=17)
            bar_bg.pack(side="left", fill="x", expand=True, padx=8)
            bar_bg.pack_propagate(False)

            bar = tk.Frame(bar_bg, bg=COLORS["blue"], height=17,
                           width=max(10, int(260 * m.get("diem", 0) / maxv)))
            bar.pack(side="left")

            tk.Label(row, text=str(m.get("diem", 0)),
                     bg="white", fg=COLORS["text"], width=5,
                     font=("Segoe UI", 9, "bold")).pack(side="right")

    # ========================================================
    # COMMON FORM HELPERS
    # ========================================================
    def labeled_entry(self, parent, label, var, row, col=0, width=22):
        tk.Label(parent, text=label, bg="white", fg=COLORS["text"],
                 font=("Segoe UI", 9, "bold")).grid(
                     row=row * 2, column=col, sticky="w", padx=10, pady=(7, 2))
        e = ttk.Entry(parent, textvariable=var, width=width)
        e.grid(row=row * 2 + 1, column=col, sticky="ew",
               padx=10, pady=(0, 5))
        return e

    def page_title(self, parent, title, subtitle):
        tk.Label(parent, text=title, bg=COLORS["bg"],
                 fg=COLORS["text"], font=("Segoe UI", 16, "bold")).pack(anchor="w")
        tk.Label(parent, text=subtitle, bg=COLORS["bg"],
                 fg=COLORS["muted"], font=("Segoe UI", 9)).pack(
                     anchor="w", pady=(2, 12))

    # ========================================================
    # MEMBERS
    # ========================================================
    def build_members(self, parent):
        self.page_title(parent, "Quản lý thành viên",
                        "Thêm, sửa, xóa, tìm kiếm và theo dõi điểm hoạt động.")

        form = tk.Frame(parent, bg="white", padx=10, pady=8,
                        highlightbackground=COLORS["border"], highlightthickness=1)
        form.pack(fill="x", pady=(0, 10))

        self.mv = {k: tk.StringVar() for k in
                   ["ma", "ten", "email", "sdt", "ban", "ngay"]}

        self.labeled_entry(form, "Mã thành viên", self.mv["ma"], 0)
        self.labeled_entry(form, "Họ tên", self.mv["ten"], 0, 1)
        self.labeled_entry(form, "Email", self.mv["email"], 0, 2)
        self.labeled_entry(form, "Số điện thoại", self.mv["sdt"], 1)

        tk.Label(form, text="Ban", bg="white",
                 font=("Segoe UI", 9, "bold")).grid(
                     row=2, column=1, sticky="w", padx=10, pady=(7, 2))
        ttk.Combobox(form, textvariable=self.mv["ban"],
                     values=["Truyền thông", "Sự kiện", "Media"],
                     state="readonly").grid(
                         row=3, column=1, sticky="ew", padx=10, pady=(0, 5))

        tk.Label(form, text="Ngày tham gia", bg="white",
                 font=("Segoe UI", 9, "bold")).grid(
                     row=2, column=2, sticky="w", padx=10, pady=(7, 2))
        DateEntry(form, textvariable=self.mv["ngay"]).grid(
            row=3, column=2, sticky="ew", padx=10, pady=(0, 5))

        for i in range(3):
            form.columnconfigure(i, weight=1)

        buttons = tk.Frame(form, bg="white")
        buttons.grid(row=4, column=0, columnspan=3,
                     sticky="w", padx=10, pady=7)

        ttk.Button(buttons, text="＋ Thêm", style="Primary.TButton",
                   command=self.add_member).pack(side="left", padx=3)
        ttk.Button(buttons, text="✎ Sửa", style="Success.TButton",
                   command=self.edit_member).pack(side="left", padx=3)
        ttk.Button(buttons, text="✕ Xóa", style="Danger.TButton",
                   command=self.delete_member).pack(side="left", padx=3)
        ttk.Button(buttons, text="↻ Làm mới",
                   command=self.clear_member).pack(side="left", padx=3)
        ttk.Button(buttons, text="Sinh dữ liệu mẫu",
                   command=self.seed_members).pack(side="left", padx=3)
        ttk.Button(buttons, text="Xuất CSV",
                   command=self.export_members).pack(side="left", padx=3)

        body = tk.Frame(parent, bg=COLORS["bg"])
        body.pack(fill="both", expand=True)

        tablebox = tk.Frame(body, bg="white",
                            highlightbackground=COLORS["border"],
                            highlightthickness=1)
        tablebox.pack(side="left", fill="both", expand=True)

        cols = ("ma", "ten", "email", "sdt", "ban", "ngay", "diem", "tt")
        self.member_tree = ttk.Treeview(tablebox, columns=cols,
                                        show="headings")
        heads = {
            "ma": "Mã TV", "ten": "Họ tên", "email": "Email",
            "sdt": "SĐT", "ban": "Ban", "ngay": "Ngày tham gia",
            "diem": "Điểm", "tt": "Trạng thái"
        }
        widths = {
            "ma": 70, "ten": 135, "email": 155, "sdt": 105,
            "ban": 100, "ngay": 105, "diem": 60, "tt": 100
        }

        for c in cols:
            self.member_tree.heading(c, text=heads[c])
            self.member_tree.column(c, width=widths[c])

        self.member_tree.pack(fill="both", expand=True, padx=6, pady=6)
        self.member_tree.bind("<<TreeviewSelect>>", self.select_member)

        cardbox = tk.Frame(body, bg="white", width=285,
                           highlightbackground=COLORS["border"],
                           highlightthickness=1)
        cardbox.pack(side="right", fill="y", padx=(10, 0))
        cardbox.pack_propagate(False)

        tk.Label(cardbox, text="Thẻ thành viên",
                 bg="white", fg=COLORS["blue_dark"],
                 font=("Segoe UI", 12, "bold")).pack(
                     anchor="w", padx=15, pady=12)

        self.member_card = MemberCard(cardbox)
        self.member_card.pack(fill="x", padx=12)

        self.refresh_members()

    def refresh_members(self):
        if not hasattr(self, "member_tree"):
            return
        for x in self.member_tree.get_children():
            self.member_tree.delete(x)
        for m in self.db.load("members"):
            self.member_tree.insert(
                "", "end",
                values=(m["ma_tv"], m["ho_ten"], m["email"], m["sdt"],
                        m["ban"], m["ngay_tham_gia"], m["diem"],
                        m["trang_thai"])
            )

    def member_data(self):
        return {
            "ma_tv": self.mv["ma"].get().strip(),
            "ho_ten": self.mv["ten"].get().strip(),
            "email": self.mv["email"].get().strip(),
            "sdt": self.mv["sdt"].get().strip(),
            "ban": self.mv["ban"].get().strip(),
            "ngay_tham_gia": self.mv["ngay"].get().strip(),
            "diem": 0,
            "trang_thai": "Hoạt động"
        }

    def add_member(self):
        data = self.member_data()
        ok, msg = self.service.validate_member(data)
        if not ok:
            messagebox.showwarning("Kiểm tra dữ liệu", msg)
            return
        rows = self.db.load("members")
        rows.append(data)
        self.db.save("members", rows)
        self.refresh_members()
        self.clear_member()
        messagebox.showinfo("Thành công", "Đã thêm thành viên.")

    def select_member(self, event=None):
        sel = self.member_tree.selection()
        if not sel:
            return
        vals = self.member_tree.item(sel[0], "values")
        for k, v in zip(["ma", "ten", "email", "sdt", "ban", "ngay"], vals):
            self.mv[k].set(v)
        member = next(
            (m for m in self.db.load("members") if m["ma_tv"] == vals[0]),
            None
        )
        self.member_card.set_member(member)

    def edit_member(self):
        if not self.mv["ma"].get():
            messagebox.showwarning("Sửa", "Hãy chọn thành viên.")
            return
        data = self.member_data()
        old = self.mv["ma"].get()
        ok, msg = self.service.validate_member(data, old)
        if not ok:
            messagebox.showwarning("Kiểm tra dữ liệu", msg)
            return
        rows = self.db.load("members")
        for i, m in enumerate(rows):
            if m["ma_tv"] == old:
                data["diem"] = m.get("diem", 0)
                rows[i] = data
        self.db.save("members", rows)
        self.refresh_members()
        messagebox.showinfo("Thành công", "Đã cập nhật thành viên.")

    def delete_member(self):
        ma = self.mv["ma"].get()
        if not ma:
            return
        if not messagebox.askyesno("Xác nhận",
                                   "Bạn có chắc muốn xóa thành viên này?"):
            return
        self.db.save(
            "members",
            [m for m in self.db.load("members") if m["ma_tv"] != ma]
        )
        self.refresh_members()
        self.clear_member()

    def clear_member(self):
        for v in self.mv.values():
            v.set("")
        self.member_card.set_member(None)

    def seed_members(self):
        self.db.seed()
        self.refresh_members()
        messagebox.showinfo("Dữ liệu mẫu",
                            "Đã thêm 5 thành viên mẫu.")

    def export_members(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv")]
        )
        if not path:
            return
        rows = self.db.load("members")
        if not rows:
            return
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
        messagebox.showinfo("Xuất dữ liệu", "Đã xuất file CSV.")

    # ========================================================
    # EVENTS
    # ========================================================
    def build_events(self, parent):
        self.page_title(parent, "Quản lý sự kiện",
                        "Tạo sự kiện, cập nhật thông tin và theo dõi điểm hoạt động.")

        frame = tk.Frame(parent, bg="white", padx=15, pady=12,
                         highlightbackground=COLORS["border"],
                         highlightthickness=1)
        frame.pack(fill="both", expand=True)

        form = tk.Frame(frame, bg="white")
        form.pack(fill="x")

        self.ev = {k: tk.StringVar() for k in
                   ["ma", "ten", "ngay", "dia", "diem"]}

        self.labeled_entry(form, "Mã sự kiện", self.ev["ma"], 0)
        self.labeled_entry(form, "Tên sự kiện", self.ev["ten"], 0, 1)
        self.labeled_entry(form, "Ngày diễn ra", self.ev["ngay"], 0, 2)
        self.labeled_entry(form, "Địa điểm", self.ev["dia"], 1)
        self.labeled_entry(form, "Điểm hoạt động", self.ev["diem"], 1, 1)

        for i in range(3):
            form.columnconfigure(i, weight=1)

        b = tk.Frame(frame, bg="white")
        b.pack(fill="x", pady=10)
        ttk.Button(b, text="＋ Thêm", style="Primary.TButton",
                   command=self.add_event).pack(side="left", padx=3)
        ttk.Button(b, text="✎ Sửa", style="Success.TButton",
                   command=self.edit_event).pack(side="left", padx=3)
        ttk.Button(b, text="✕ Xóa", style="Danger.TButton",
                   command=self.delete_event).pack(side="left", padx=3)
        ttk.Button(b, text="↻ Làm mới",
                   command=self.clear_event).pack(side="left", padx=3)

        self.event_tree = ttk.Treeview(
            frame,
            columns=("ma", "ten", "ngay", "dia", "diem"),
            show="headings"
        )

        for c, h, w in [
            ("ma", "Mã SK", 90),
            ("ten", "Tên sự kiện", 230),
            ("ngay", "Ngày diễn ra", 130),
            ("dia", "Địa điểm", 230),
            ("diem", "Điểm", 80)
        ]:
            self.event_tree.heading(c, text=h)
            self.event_tree.column(c, width=w)

        self.event_tree.pack(fill="both", expand=True)
        self.event_tree.bind("<<TreeviewSelect>>", self.select_event)
        self.refresh_events()

    def refresh_events(self):
        if not hasattr(self, "event_tree"):
            return
        for x in self.event_tree.get_children():
            self.event_tree.delete(x)
        for e in self.db.load("events"):
            self.event_tree.insert(
                "", "end",
                values=(e["ma_sk"], e["ten_sk"], e["ngay"],
                        e["dia_diem"], e["diem"])
            )

    def add_event(self):
        try:
            diem = int(self.ev["diem"].get() or 0)
        except ValueError:
            messagebox.showwarning("Lỗi", "Điểm phải là số.")
            return

        d = {
            "ma_sk": self.ev["ma"].get().strip(),
            "ten_sk": self.ev["ten"].get().strip(),
            "ngay": self.ev["ngay"].get().strip(),
            "dia_diem": self.ev["dia"].get().strip(),
            "diem": diem
        }

        if not all([d["ma_sk"], d["ten_sk"], d["ngay"], d["dia_diem"]]):
            messagebox.showwarning("Lỗi", "Nhập đủ thông tin.")
            return

        ok, msg = self.service.validate_event(d)
        if not ok:
            messagebox.showwarning("Kiểm tra dữ liệu", msg)
            return

        rows = self.db.load("events")
        rows.append(d)
        self.db.save("events", rows)
        self.refresh_events()
        self.clear_event()

    def select_event(self, event=None):
        s = self.event_tree.selection()
        if not s:
            return
        v = self.event_tree.item(s[0], "values")
        for k, x in zip(["ma", "ten", "ngay", "dia", "diem"], v):
            self.ev[k].set(x)

    def edit_event(self):
        ma = self.ev["ma"].get().strip()
        if not ma:
            messagebox.showwarning("Sửa", "Hãy chọn sự kiện.")
            return
        try:
            diem = int(self.ev["diem"].get() or 0)
        except ValueError:
            messagebox.showwarning("Lỗi", "Điểm phải là số nguyên.")
            return

        data = {
            "ma_sk": ma,
            "ten_sk": self.ev["ten"].get().strip(),
            "ngay": self.ev["ngay"].get().strip(),
            "dia_diem": self.ev["dia"].get().strip(),
            "diem": diem
        }
        ok, msg = self.service.validate_event(data, ma)
        if not ok:
            messagebox.showwarning("Kiểm tra dữ liệu", msg)
            return

        rows = self.db.load("events")
        for i, event in enumerate(rows):
            if event["ma_sk"] == ma:
                rows[i] = data
                break
        self.db.save("events", rows)
        self.refresh_events()
        self.clear_event()

    def delete_event(self):
        ma = self.ev["ma"].get()
        if not ma:
            return
        if messagebox.askyesno("Xóa", "Xóa sự kiện đã chọn?"):
            self.db.save(
                "events",
                [e for e in self.db.load("events") if e["ma_sk"] != ma]
            )
            self.refresh_events()
            self.clear_event()

    def clear_event(self):
        for v in self.ev.values():
            v.set("")

    # ========================================================
    # REGISTRATION
    # ========================================================
    def build_registrations(self, parent):
        self.page_title(parent, "Đăng ký & điểm danh",
                        "Đăng ký sự kiện và ghi nhận mức độ tham gia của thành viên.")

        top = tk.Frame(parent, bg="white", padx=15, pady=15,
                       highlightbackground=COLORS["border"],
                       highlightthickness=1)
        top.pack(fill="x")

        left = tk.Frame(top, bg="white")
        left.pack(side="left", fill="x", expand=True)

        right = tk.Frame(top, bg="white")
        right.pack(side="right", fill="x", expand=True)

        self.reg_tv = tk.StringVar()
        self.reg_sk = tk.StringVar()

        tk.Label(left, text="ĐĂNG KÝ SỰ KIỆN", bg="white",
                 fg=COLORS["blue_dark"],
                 font=("Segoe UI", 10, "bold")).pack(anchor="w")

        self.reg_tv_cb = ttk.Combobox(left, textvariable=self.reg_tv,
                                      state="readonly")
        self.reg_tv_cb.pack(fill="x", pady=6)

        self.reg_sk_cb = ttk.Combobox(left, textvariable=self.reg_sk,
                                      state="readonly")
        self.reg_sk_cb.pack(fill="x", pady=6)

        ttk.Button(left, text="Đăng ký", style="Primary.TButton",
                   command=self.register).pack(anchor="w")

        tk.Label(right, text="ĐIỂM DANH", bg="white",
                 fg=COLORS["green"],
                 font=("Segoe UI", 10, "bold")).pack(anchor="w")

        tk.Label(right, text="Chọn một dòng trong danh sách bên dưới để điểm danh.",
                 bg="white", fg=COLORS["muted"],
                 font=("Segoe UI", 9)).pack(anchor="w", pady=(5, 10))

        ttk.Button(right, text="✓  Cập nhật điểm danh",
                   style="Success.TButton",
                   command=self.attend).pack(anchor="w")

        self.reg_tree = ttk.Treeview(
            parent,
            columns=("dk", "tv", "sk", "ngay", "tt", "mat"),
            show="headings"
        )

        for c, h, w in [
            ("dk", "Mã ĐK", 80),
            ("tv", "Mã TV", 100),
            ("sk", "Mã SK", 100),
            ("ngay", "Ngày đăng ký", 120),
            ("tt", "Trạng thái", 130),
            ("mat", "Điểm danh", 130)
        ]:
            self.reg_tree.heading(c, text=h)
            self.reg_tree.column(c, width=w)

        self.reg_tree.pack(fill="both", expand=True, pady=12)
        self.refresh_reg()

    def refresh_reg(self):
        if not hasattr(self, "reg_tree"):
            return
        members = self.db.load("members")
        events = self.db.load("events")

        self.reg_tv_cb["values"] = [
            f"{m['ma_tv']} - {m['ho_ten']}" for m in members
        ]
        self.reg_sk_cb["values"] = [
            f"{e['ma_sk']} - {e['ten_sk']}" for e in events
        ]

        for x in self.reg_tree.get_children():
            self.reg_tree.delete(x)

        for r in self.db.load("registrations"):
            self.reg_tree.insert(
                "", "end",
                values=(r["ma_dk"], r["ma_tv"], r["ma_sk"],
                        r["ngay_dk"], r["trang_thai"], r["co_mat"])
            )

    def register(self):
        if not self.reg_tv.get() or not self.reg_sk.get():
            messagebox.showwarning("Đăng ký",
                                   "Chọn thành viên và sự kiện.")
            return

        tv = self.reg_tv.get().split(" - ")[0]
        sk = self.reg_sk.get().split(" - ")[0]
        ok, msg = self.service.validate_registration(tv, sk)
        if not ok:
            messagebox.showwarning("Đăng ký", msg)
            return

        rows = self.db.load("registrations")

        rows.append({
            "ma_dk": f"DK{len(rows)+1:03d}",
            "ma_tv": tv,
            "ma_sk": sk,
            "ngay_dk": datetime.now().strftime("%d/%m/%Y"),
            "trang_thai": "Đã đăng ký",
            "co_mat": "Chưa điểm danh"
        })

        self.db.save("registrations", rows)
        self.refresh_reg()

    def attend(self):
        s = self.reg_tree.selection()
        if not s:
            messagebox.showwarning("Điểm danh",
                                   "Chọn một đăng ký.")
            return

        dk = self.reg_tree.item(s[0], "values")[0]
        rows = self.db.load("registrations")
        sk = None
        tv = None

        for r in rows:
            if r["ma_dk"] == dk:
                r["co_mat"] = "Có mặt"
                sk = r["ma_sk"]
                tv = r["ma_tv"]

        self.db.save("registrations", rows)

        event = next(
            (e for e in self.db.load("events") if e["ma_sk"] == sk),
            None
        )

        if event:
            members = self.db.load("members")
            for m in members:
                if m["ma_tv"] == tv:
                    m["diem"] = m.get("diem", 0) + int(event["diem"])
            self.db.save("members", members)

        self.refresh_reg()

    # ========================================================
    # FEES
    # ========================================================
    def build_fees(self, parent):
        self.page_title(parent, "Khoản thu hội phí",
                        "Theo dõi hội phí, trạng thái đóng và tổng số tiền.")

        top = tk.Frame(parent, bg="white", padx=15, pady=12,
                       highlightbackground=COLORS["border"],
                       highlightthickness=1)
        top.pack(fill="x", pady=(0, 10))

        self.fv = {k: tk.StringVar() for k in
                   ["ma", "tv", "loai", "tien", "noidung", "tt"]}

        self.labeled_entry(top, "Mã thu", self.fv["ma"], 0)
        self.labeled_entry(top, "Mã TV", self.fv["tv"], 0, 1)
        self.labeled_entry(top, "Loại thu", self.fv["loai"], 0, 2)
        self.labeled_entry(top, "Số tiền", self.fv["tien"], 1)
        self.labeled_entry(top, "Nội dung", self.fv["noidung"], 1, 1)

        tk.Label(top, text="Trạng thái", bg="white",
                 font=("Segoe UI", 9, "bold")).grid(
                     row=2, column=2, sticky="w", padx=10, pady=(7, 2))
        ttk.Combobox(top, textvariable=self.fv["tt"],
                     values=["Đã đóng", "Chưa đóng"],
                     state="readonly").grid(
                         row=3, column=2, sticky="ew",
                         padx=10, pady=(0, 5))

        for i in range(3):
            top.columnconfigure(i, weight=1)

        b = tk.Frame(top, bg="white")
        b.grid(row=4, column=0, columnspan=3,
               sticky="w", padx=10, pady=7)

        ttk.Button(b, text="＋ Thêm", style="Primary.TButton",
                   command=self.add_fee).pack(side="left", padx=3)
        ttk.Button(b, text="✎ Sửa", style="Success.TButton",
                   command=self.edit_fee).pack(side="left", padx=3)
        ttk.Button(b, text="✕ Xóa", style="Danger.TButton",
                   command=self.delete_fee).pack(side="left", padx=3)

        self.fee_tree = ttk.Treeview(
            parent,
            columns=("ma", "tv", "ten", "loai", "tien", "tt", "ngay"),
            show="headings"
        )

        for c, h, w in [
            ("ma", "Mã thu", 80),
            ("tv", "Mã TV", 80),
            ("ten", "Tên thành viên", 160),
            ("loai", "Loại thu", 100),
            ("tien", "Số tiền", 110),
            ("tt", "Trạng thái", 110),
            ("ngay", "Ngày thu", 110)
        ]:
            self.fee_tree.heading(c, text=h)
            self.fee_tree.column(c, width=w)

        self.fee_tree.pack(fill="both", expand=True)
        self.refresh_fees()

    def refresh_fees(self):
        if not hasattr(self, "fee_tree"):
            return

        members = {
            m["ma_tv"]: m["ho_ten"]
            for m in self.db.load("members")
        }

        for x in self.fee_tree.get_children():
            self.fee_tree.delete(x)

        for f in self.db.load("fees"):
            self.fee_tree.insert(
                "", "end",
                values=(f["ma_thu"], f["ma_tv"],
                        members.get(f["ma_tv"], ""),
                        f["loai_thu"], f"{f['so_tien']:,}",
                        f["trang_thai"], f["ngay_thu"])
            )

    def add_fee(self):
        try:
            tien = int(self.fv["tien"].get())
        except ValueError:
            messagebox.showwarning("Lỗi", "Số tiền phải là số.")
            return

        data = {
            "ma_thu": self.fv["ma"].get().strip(),
            "ma_tv": self.fv["tv"].get().strip(),
            "loai_thu": self.fv["loai"].get().strip(),
            "so_tien": tien,
            "noi_dung": self.fv["noidung"].get().strip(),
            "trang_thai": self.fv["tt"].get() or "Chưa đóng",
            "ngay_thu": datetime.now().strftime("%d/%m/%Y")
            if self.fv["tt"].get() == "Đã đóng" else ""
        }
        ok, msg = self.service.validate_fee(data)
        if not ok:
            messagebox.showwarning("Kiểm tra dữ liệu", msg)
            return

        rows = self.db.load("fees")
        rows.append(data)
        self.db.save("fees", rows)
        self.refresh_fees()

    def edit_fee(self):
        s = self.fee_tree.selection()
        if not s:
            return

        ma = self.fee_tree.item(s[0], "values")[0]
        rows = self.db.load("fees")

        for f in rows:
            if f["ma_thu"] == ma:
                f["trang_thai"] = self.fv["tt"].get()

        self.db.save("fees", rows)
        self.refresh_fees()

    def delete_fee(self):
        s = self.fee_tree.selection()
        if not s:
            return

        ma = self.fee_tree.item(s[0], "values")[0]
        self.db.save(
            "fees",
            [f for f in self.db.load("fees") if f["ma_thu"] != ma]
        )
        self.refresh_fees()

    # ========================================================
    # STATISTICS
    # ========================================================
    def build_stats(self, parent):
        self.page_title(parent, "Thống kê & biểu đồ",
                        "Tổng hợp thành viên, sự kiện, lượt tham gia và điểm hoạt động.")

        self.stat_cards = tk.Frame(parent, bg=COLORS["bg"])
        self.stat_cards.pack(fill="x", pady=(0, 10))

        self.chart = tk.Canvas(
            parent, bg="white", height=450,
            highlightbackground=COLORS["border"],
            highlightthickness=1
        )
        self.chart.pack(fill="both", expand=True)

        self.refresh_stats()

    def refresh_stats(self):
        if not hasattr(self, "stat_cards"):
            return

        self.clear_children(self.stat_cards)
        s = self.service.stats()

        cards = [
            ("Tổng thành viên", s["members"], "👥", COLORS["blue"], "#E8F3FF"),
            ("Tổng sự kiện", s["events"], "▦", COLORS["green"], "#E8FAF1"),
            ("Tổng lượt tham gia", s["participants"], "●", "#F59E0B", "#FFF5DF"),
            ("Tổng tiền đã thu", f"{s['paid']:,}đ", "₫", COLORS["purple"], "#F1ECFF")
        ]

        for title, value, icon, color, bg in cards:
            card = tk.Frame(self.stat_cards, bg=bg,
                            highlightbackground=COLORS["border"],
                            highlightthickness=1, padx=15, pady=12)
            card.pack(side="left", fill="x", expand=True, padx=5)
            tk.Label(card, text=icon, bg=bg, fg=color,
                     font=("Segoe UI Emoji", 22)).pack(side="left", padx=8)
            box = tk.Frame(card, bg=bg)
            box.pack(side="left")
            tk.Label(box, text=title, bg=bg, fg=COLORS["muted"],
                     font=("Segoe UI", 9)).pack(anchor="w")
            tk.Label(box, text=str(value), bg=bg, fg=color,
                     font=("Segoe UI", 17, "bold")).pack(anchor="w")

        self.chart.delete("all")
        members = sorted(
            self.db.load("members"),
            key=lambda x: x.get("diem", 0),
            reverse=True
        )[:5]

        self.chart.create_text(
            30, 25, anchor="w",
            text="Top 5 thành viên tích cực",
            font=("Segoe UI", 13, "bold"),
            fill=COLORS["text"]
        )

        maxv = max([m.get("diem", 0) for m in members] + [1])

        for i, m in enumerate(members):
            y = 75 + i * 55
            value = m.get("diem", 0)

            self.chart.create_text(
                35, y + 12, anchor="w",
                text=m["ho_ten"],
                fill=COLORS["text"],
                font=("Segoe UI", 9)
            )

            self.chart.create_rectangle(
                190, y, 900, y + 27,
                fill="#E8EEF6", outline=""
            )
            self.chart.create_rectangle(
                190, y,
                190 + int(710 * value / maxv),
                y + 27,
                fill=COLORS["blue"], outline=""
            )
            self.chart.create_text(
                920, y + 13, anchor="w",
                text=str(value),
                fill=COLORS["text"],
                font=("Segoe UI", 9, "bold")
            )

    # ========================================================
    # REPORT / API
    # ========================================================
    def build_reports(self, parent):
        self.page_title(parent, "Báo cáo & dữ liệu",
                        "Xuất dữ liệu, sinh dữ liệu mẫu và mô phỏng lấy dữ liệu từ API.")

        box = tk.Frame(parent, bg="white", padx=18, pady=18,
                       highlightbackground=COLORS["border"],
                       highlightthickness=1)
        box.pack(fill="both", expand=True)

        tk.Label(box, text="Chức năng xuất báo cáo",
                 bg="white", fg=COLORS["text"],
                 font=("Segoe UI", 12, "bold")).pack(anchor="w")

        b = tk.Frame(box, bg="white")
        b.pack(anchor="w", pady=12)

        ttk.Button(b, text="Xuất CSV",
                   command=self.export_members).pack(side="left", padx=4)
        ttk.Button(b, text="Xuất TXT",
                   command=self.export_txt).pack(side="left", padx=4)
        ttk.Button(b, text="Xuất JSON",
                   command=self.export_json).pack(side="left", padx=4)
        ttk.Button(b, text="Sinh dữ liệu mẫu",
                   style="Primary.TButton",
                   command=self.seed_members).pack(side="left", padx=4)
        ttk.Button(b, text="Lấy dữ liệu API",
                   command=self.fetch_api).pack(side="left", padx=4)

        tk.Label(box, text="Dữ liệu trả về từ API",
                 bg="white", fg=COLORS["text"],
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(15, 5))

        self.api_text = tk.Text(
            box, height=20, font=("Consolas", 9),
            bg="#F8FAFC", fg=COLORS["text"],
            relief="flat", padx=10, pady=10
        )
        self.api_text.pack(fill="both", expand=True)

    def export_json(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON", "*.json")]
        )
        if not path:
            return

        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                self.db.load("members"), f,
                ensure_ascii=False, indent=2
            )

        messagebox.showinfo("Xuất dữ liệu", "Đã xuất JSON.")

    def export_txt(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text", "*.txt")]
        )
        if not path:
            return

        rows = self.db.load("members")
        with open(path, "w", encoding="utf-8") as f:
            f.write("DANH SÁCH THÀNH VIÊN CLB\n")
            f.write("=" * 70 + "\n")
            for m in rows:
                f.write(
                    f"{m['ma_tv']} | {m['ho_ten']} | "
                    f"{m['ban']} | Điểm: {m['diem']}\n"
                )

        messagebox.showinfo("Xuất dữ liệu", "Đã xuất TXT.")

    def fetch_api(self):
        self.api_text.delete("1.0", "end")
        try:
            url = "https://jsonplaceholder.typicode.com/posts/1"
            with urllib.request.urlopen(url, timeout=5) as response:
                data = json.loads(response.read().decode("utf-8"))

            self.api_text.insert(
                "end", json.dumps(data, ensure_ascii=False, indent=2)
            )
            self.api_text.insert(
                "end", "\n\n✓ Đã lấy dữ liệu từ API."
            )
        except Exception:
            sample = {
                "id": 1,
                "title": "Ngày hội CLB sinh viên HUIT",
                "date": "2026-10-15",
                "description": "Dữ liệu API mô phỏng khi không có Internet."
            }
            self.api_text.insert(
                "end", json.dumps(sample, ensure_ascii=False, indent=2)
            )
            self.api_text.insert(
                "end", "\n\n! Không kết nối được API, đang dùng dữ liệu dự phòng."
            )

    # ========================================================
    # LOGOUT
    # ========================================================
    def logout(self):
        if messagebox.askyesno("Đăng xuất",
                               "Bạn có muốn đăng xuất không?"):
            self.destroy()
            LoginWindow(start_app).mainloop()


def start_app(user):
    app = MainApp(user)
    app.mainloop()


def run():
    LoginWindow(start_app).mainloop()


if __name__ == "__main__":
    run()
