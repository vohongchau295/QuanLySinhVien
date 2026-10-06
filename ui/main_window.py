import tkinter as tk
from tkinter import ttk, messagebox


class MainWindow:
    def __init__(self, root, service):
        self.root = root
        self.service = service

        self.root.title("Quản lý Câu lạc bộ Sinh viên")
        self.root.geometry("1100x650")
        self.root.resizable(True, True)

        # =========================
        # MENU BÊN TRÁI
        # =========================
        self.menu = tk.Frame(self.root, width=200)
        self.menu.pack(side="left", fill="y")

        tk.Label(
            self.menu,
            text="QUẢN LÝ CLB",
            font=("Arial", 16, "bold")
        ).pack(pady=25)

        self.create_menu_button("Dashboard", self.show_dashboard)
        self.create_menu_button("Thành viên", self.show_members)
        self.create_menu_button("Phòng ban", self.show_departments)
        self.create_menu_button("Sự kiện", self.show_events)
        self.create_menu_button("Đăng ký", self.show_registrations)
        self.create_menu_button("Hoạt động", self.show_activities)
        self.create_menu_button("Hội phí", self.show_fees)

        # =========================
        # KHU VỰC NỘI DUNG
        # =========================
        self.content = tk.Frame(self.root)
        self.content.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.show_dashboard()

    # =========================
    # TẠO NÚT MENU
    # =========================
    def create_menu_button(self, text, command):
        ttk.Button(
            self.menu,
            text=text,
            command=command,
            width=22
        ).pack(pady=5)

    # =========================
    # XÓA MÀN HÌNH CŨ
    # =========================
    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    # =========================
    # TIÊU ĐỀ
    # =========================
    def create_title(self, text):
        ttk.Label(
            self.content,
            text=text,
            font=("Arial", 20, "bold")
        ).pack(pady=20)

    # =========================
    # DASHBOARD
    # =========================
    def show_dashboard(self):
        self.clear_content()
        self.create_title("DASHBOARD")

        frame = tk.Frame(self.content)
        frame.pack(pady=30)

        member_count = 0
        event_count = 0

        try:
            members = self.service.get_members()
            member_count = len(members)
        except:
            pass

        try:
            events = self.service.get_events()
            event_count = len(events)
        except:
            pass

        self.create_stat_box(
            frame,
            "Số thành viên",
            member_count,
            0
        )

        self.create_stat_box(
            frame,
            "Số sự kiện",
            event_count,
            1
        )

        self.create_stat_box(
            frame,
            "Trạng thái",
            "Hoạt động",
            2
        )

    def create_stat_box(self, parent, title, value, column):
        box = tk.Frame(
            parent,
            width=220,
            height=120,
            relief="solid",
            borderwidth=1
        )

        box.grid(
            row=0,
            column=column,
            padx=15
        )

        box.pack_propagate(False)

        tk.Label(
            box,
            text=title,
            font=("Arial", 12)
        ).pack(pady=10)

        tk.Label(
            box,
            text=str(value),
            font=("Arial", 22, "bold")
        ).pack()

    # =========================
    # THÀNH VIÊN
    # =========================
    def show_members(self):
        self.clear_content()
        self.create_title("QUẢN LÝ THÀNH VIÊN")

        button_frame = tk.Frame(self.content)
        button_frame.pack(pady=10)

        ttk.Button(
            button_frame,
            text="Thêm thành viên",
            command=self.add_member_form
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame,
            text="Tìm kiếm",
            command=self.search_member
        ).pack(side="left", padx=5)
        
        ttk.Button(
            button_frame,
            text="Sửa",
            command=self.edit_member_form
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame,
            text="Xóa",
            command=self.delete_member
        ).pack(side="left", padx=5)

        columns = (
            "ID",
            "Mã SV",
            "Họ tên",
            "Email",
            "SĐT"
        )

        self.member_table = ttk.Treeview(
            self.content,
            columns=columns,
            show="headings"
        )

        for column in columns:
            self.member_table.heading(
                column,
                text=column
            )
            self.member_table.column(
                column,
                width=130
            )

        self.member_table.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.load_members()

    def load_members(self):
        try:
            members = self.service.get_members()

            for item in self.member_table.get_children():
                self.member_table.delete(item)

            for member in members:
                try:
                    values = (
                        member.member_id,
                        member.student_id,
                        member.name,
                        member.email,
                        member.phone
                    )
                except:
                    values = (
                        getattr(member, "code", ""),
                        getattr(member, "code", ""),
                        getattr(member, "name", ""),
                        getattr(member, "email", ""),
                        getattr(member, "phone", "")
                    )

                self.member_table.insert(
                    "",
                    "end",
                    values=values
                )

        except Exception:
            messagebox.showinfo(
                "Thông báo",
                "Chưa có dữ liệu thành viên."
            )

    # =========================
    # FORM THÊM THÀNH VIÊN
    # =========================
    def add_member_form(self):
        window = tk.Toplevel(self.root)
        window.title("Thêm thành viên")
        window.geometry("400x450")

        tk.Label(
            window,
            text="THÊM THÀNH VIÊN",
            font=("Arial", 16, "bold")
        ).pack(pady=15)

        fields = [
            ("Mã thành viên", "member_id"),
            ("Mã sinh viên", "student_id"),
            ("Họ tên", "name"),
            ("Email", "email"),
            ("Số điện thoại", "phone"),
            ("Mã phòng ban", "department_id"),
            ("Ngày tham gia", "join_date")
        ]

        entries = {}

        for label, key in fields:
            frame = tk.Frame(window)
            frame.pack(pady=5)

            tk.Label(
                frame,
                text=label,
                width=15,
                anchor="w"
            ).pack(side="left")

            entry = ttk.Entry(
                frame,
                width=25
            )
            entry.pack(side="left")

            entries[key] = entry

        def save_member():
            data = {}

            for key, entry in entries.items():
                data[key] = entry.get()

            if data["member_id"] == "":
                messagebox.showerror(
                    "Lỗi",
                    "Vui lòng nhập mã thành viên!"
                )
                return

            if data["student_id"] == "":
                messagebox.showerror(
                    "Lỗi",
                    "Vui lòng nhập mã sinh viên!"
                )
                return

            if data["name"] == "":
                messagebox.showerror(
                    "Lỗi",
                    "Vui lòng nhập họ tên!"
                )
                return

            try:
                if hasattr(self.service, "create_member"):
                    self.service.create_member(data)

                elif hasattr(self.service, "add_member"):
                    self.service.add_member(data)

                else:
                    messagebox.showinfo(
                        "Thông báo",
                        "Chưa kết nối MemberManager."
                    )
                    return

                messagebox.showinfo(
                    "Thành công",
                    "Đã thêm thành viên!"
                )

                window.destroy()
                self.load_members()

            except Exception as e:
                messagebox.showerror(
                    "Lỗi",
                    str(e)
                )

        ttk.Button(
            window,
            text="Lưu",
            command=save_member
        ).pack(pady=20)

        ttk.Button(
            window,
            text="Hủy",
            command=window.destroy
        ).pack()

    # =========================
    # TÌM KIẾM THÀNH VIÊN
    # =========================
    def search_member(self):
        window = tk.Toplevel(self.root)
        window.title("Tìm kiếm thành viên")
        window.geometry("400x180")

        tk.Label(
            window,
            text="Nhập tên hoặc mã sinh viên:"
        ).pack(pady=15)

        entry = ttk.Entry(
            window,
            width=35
        )
        entry.pack()

        def search():
            keyword = entry.get()

            if keyword == "":
                messagebox.showwarning(
                    "Thông báo",
                    "Vui lòng nhập từ khóa!"
                )
                return

            try:
                if hasattr(self.service, "search_member"):
                    members = self.service.search_member(keyword)

                    for item in self.member_table.get_children():
                        self.member_table.delete(item)

                    for member in members:
                        values = (
                            getattr(member, "member_id", ""),
                            getattr(member, "student_id", ""),
                            getattr(member, "name", ""),
                            getattr(member, "email", ""),
                            getattr(member, "phone", "")
                        )

                        self.member_table.insert(
                            "",
                            "end",
                            values=values
                        )

                    window.destroy()

                else:
                    messagebox.showinfo(
                        "Thông báo",
                        "Chưa kết nối chức năng tìm kiếm."
                    )

            except Exception as e:
                messagebox.showerror(
                    "Lỗi",
                    str(e)
                )

        ttk.Button(
            window,
            text="Tìm kiếm",
            command=search
        ).pack(pady=15)

    # =========================
    # SỬA THÀNH VIÊN
    # =========================
    def edit_member_form(self):
        selected = self.member_table.selection()

        if not selected:
            messagebox.showwarning(
                "Thông báo",
                "Vui lòng chọn thành viên cần sửa!"
            )
            return

        item = self.member_table.item(selected[0])
        values = item["values"]

        window = tk.Toplevel(self.root)
        window.title("Sửa thành viên")
        window.geometry("400x450")

        tk.Label(
            window,
            text="SỬA THÀNH VIÊN",
            font=("Arial", 16, "bold")
        ).pack(pady=15)

        fields = [
            ("Mã thành viên", values[0]),
            ("Mã sinh viên", values[1]),
            ("Họ tên", values[2]),
            ("Email", values[3]),
            ("Số điện thoại", values[4])
        ]

        entries = {}

        for label, value in fields:
            frame = tk.Frame(window)
            frame.pack(pady=5)

            tk.Label(
                frame,
                text=label,
                width=15,
                anchor="w"
            ).pack(side="left")

            entry = ttk.Entry(
                frame,
                width=25
            )
            entry.insert(0, value)
            entry.pack(side="left")

            entries[label] = entry

        def save_edit():
            data = {
                "member_id": entries["Mã thành viên"].get(),
                "student_id": entries["Mã sinh viên"].get(),
                "name": entries["Họ tên"].get(),
                "email": entries["Email"].get(),
                "phone": entries["Số điện thoại"].get()
            }

            try:
                if hasattr(self.service, "update_member"):
                    self.service.update_member(
                        data["member_id"],
                        data
                    )

                    messagebox.showinfo(
                        "Thành công",
                        "Đã cập nhật thành viên!"
                    )

                    window.destroy()
                    self.load_members()

                else:
                    messagebox.showinfo(
                        "Thông báo",
                        "Chưa kết nối chức năng sửa thành viên."
                    )

            except Exception as e:
                messagebox.showerror(
                    "Lỗi",
                    str(e)
                )

        ttk.Button(
            window,
            text="Lưu thay đổi",
            command=save_edit
        ).pack(pady=20)

        ttk.Button(
            window,
            text="Hủy",
            command=window.destroy
        ).pack()

    # =========================
    # XÓA THÀNH VIÊN
    # =========================
    def delete_member(self):
        selected = self.member_table.selection()

        if not selected:
            messagebox.showwarning(
                "Thông báo",
                "Vui lòng chọn thành viên cần xóa!"
            )
            return

        item = self.member_table.item(selected[0])
        member_id = item["values"][0]

        confirm = messagebox.askyesno(
            "Xác nhận",
            "Bạn có chắc muốn xóa thành viên này không?"
        )

        if not confirm:
            return

        try:
            if hasattr(self.service, "delete_member"):
                self.service.delete_member(member_id)

                messagebox.showinfo(
                    "Thành công",
                    "Đã xóa thành viên!"
                )

                self.load_members()

            else:
                messagebox.showinfo(
                    "Thông báo",
                    "Chưa kết nối chức năng xóa thành viên."
                )

        except Exception as e:
            messagebox.showerror(
                "Lỗi",
                str(e)
            )

    # =========================
    # PHÒNG BAN
    # =========================
    def show_departments(self):
        self.clear_content()
        self.create_title("QUẢN LÝ PHÒNG BAN")
        
        ttk.Button(
            self.content,
            text="Thêm phòng ban",
            command=self.add_department_form
        ).pack(pady=10)

        ttk.Button(
            self.content,
            text="Sửa",
            command=self.edit_department_form
        ).pack(pady=5)

        ttk.Button(
            self.content,
            text="Xóa",
            command=self.delete_department
        ).pack(pady=5)

        ttk.Button(
            self.content,
            text="Làm mới",
            command=self.load_departments
        ).pack(pady=5)
        
        columns = (
            "Mã phòng ban",
            "Tên phòng ban",
            "Mô tả"
        )

        table = ttk.Treeview(
            self.content,
            columns=columns,
            show="headings"
        )

        for column in columns:
            table.heading(
                column,
                text=column
            )
            table.column(
                column,
                width=200
            )

        table.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

    def add_department_form(self):
        messagebox.showinfo(
            "Phòng ban",
            "Form thêm phòng ban sẽ được kết nối với DepartmentManager."
        )

    # =========================
    # SỰ KIỆN
    # =========================
    def show_events(self):
        self.clear_content()
        self.create_title("QUẢN LÝ SỰ KIỆN")

        button_frame = tk.Frame(self.content)
        button_frame.pack(pady=10)

        ttk.Button(
            button_frame,
            text="Thêm sự kiện",
            command=self.add_event_form
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame,
            text="Sửa",
            command=self.edit_event_form
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame,
            text="Xóa",
            command=self.delete_event
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame,
            text="Tìm kiếm",
            command=self.search_event
        ).pack(side="left", padx=5)

        columns = (
            "Mã sự kiện",
            "Tên sự kiện",
            "Ngày",
            "Địa điểm",
            "Sức chứa"
        )

        self.event_table = ttk.Treeview(
            self.content,
            columns=columns,
            show="headings"
        )

        for column in columns:
            self.event_table.heading(
                column,
                text=column
            )
            self.event_table.column(
                column,
                width=150
            )

        self.event_table.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )
    
        
        try:
            events = self.service.get_events()

            for event in events:
                values = (
                    getattr(event, "event_id", ""),
                    getattr(event, "name", ""),
                    getattr(event, "date", ""),
                    getattr(event, "location", ""),
                    getattr(event, "capacity", "")
                )

                self.event_table.insert(
                    "",
                    "end",
                    values=values
                )

        except:
            pass

    def add_event_form(self):
        window = tk.Toplevel(self.root)
        window.title("Thêm sự kiện")
        window.geometry("400x450")

        tk.Label(
            window,
            text="THÊM SỰ KIỆN",
            font=("Arial", 16, "bold")
        ).pack(pady=15)

        fields = [
            ("Mã sự kiện", "event_id"),
            ("Tên sự kiện", "name"),
            ("Ngày", "date"),
            ("Địa điểm", "location"),
            ("Sức chứa", "capacity")
        ]

        entries = {}

        for label, key in fields:
            frame = tk.Frame(window)
            frame.pack(pady=5)

            tk.Label(
                frame,
                text=label,
                width=15,
                anchor="w"
            ).pack(side="left")

            entry = ttk.Entry(
                frame,
                width=25
            )
            entry.pack(side="left")

            entries[key] = entry

        def save_event():
            data = {
                "event_id": entries["event_id"].get(),
                "name": entries["name"].get(),
                "date": entries["date"].get(),
                "location": entries["location"].get(),
                "capacity": entries["capacity"].get()
            }

            try:
                if hasattr(self.service, "create_event"):
                    self.service.create_event(data)

                    messagebox.showinfo(
                        "Thành công",
                        "Đã thêm sự kiện!"
                    )

                    window.destroy()

                else:
                    messagebox.showinfo(
                        "Thông báo",
                        "Chưa kết nối chức năng thêm sự kiện."
                    )

            except Exception as e:
                messagebox.showerror(
                    "Lỗi",
                    str(e)
                )

        ttk.Button(
            window,
            text="Lưu",
            command=save_event
        ).pack(pady=20)

        ttk.Button(
            window,
            text="Hủy",
            command=window.destroy
        ).pack()
    
    def edit_event_form(self):
        selected = self.event_table.selection()

        if not selected:
            messagebox.showwarning(
                "Thông báo",
                "Vui lòng chọn sự kiện cần sửa!"
            )
            return

        item = self.event_table.item(selected[0])
        values = item["values"]

        window = tk.Toplevel(self.root)
        window.title("Sửa sự kiện")
        window.geometry("400x450")

        tk.Label(
            window,
            text="SỬA SỰ KIỆN",
            font=("Arial", 16, "bold")
        ).pack(pady=15)

        fields = [
            ("Mã sự kiện", "event_id"),
            ("Tên sự kiện", "name"),
            ("Ngày", "date"),
            ("Địa điểm", "location"),
            ("Sức chứa", "capacity")
        ]

        entries = {}
        
        for i, (label, key) in enumerate(fields):
            frame = tk.Frame(window)
            frame.pack(pady=5)

            tk.Label(
                frame,
                text=label,
                width=15,
                anchor="w"            
        ).pack(side="left")

            entry = ttk.Entry(
                frame,
                width=25
            )
            entry.insert(0, values[i])
            entry.pack(side="left")

            entries[key] = entry

        def save_edit():
            data = {
                "event_id": entries["event_id"].get(),
                "name": entries["name"].get(),
                "date": entries["date"].get(),
                "location": entries["location"].get(),
                "capacity": entries["capacity"].get()
            }

            try:
                if hasattr(self.service, "update_event"):
                    self.service.update_event(
                        data["event_id"],
                        data
                    )

                    messagebox.showinfo(
                        "Thành công",
                        "Đã cập nhật sự kiện!"
                    )

                    window.destroy()
                    
                else:
                    messagebox.showinfo(
                        "Thông báo",
                        "Chưa kết nối chức năng sửa sự kiện."
                    )

            except Exception as e:
                messagebox.showerror(
                    "Lỗi",
                    str(e)
                )

        ttk.Button(
            window,
            text="Lưu thay đổi",
            command=save_edit
        ).pack(pady=20)

        ttk.Button(
            window,
            text="Hủy",
            command=window.destroy
        ).pack()
    
    def delete_event(self):
        selected = self.event_table.selection()

        if not selected:
            messagebox.showwarning(
                "Thông báo",
                "Vui lòng chọn sự kiện cần xóa!"
            )
            return

        item = self.event_table.item(selected[0])
        event_id = item["values"][0]

        confirm = messagebox.askyesno(
            "Xác nhận",
            "Bạn có chắc muốn xóa sự kiện này không?"
        )

        if not confirm:
            return

        try:
            if hasattr(self.service, "delete_event"):
                self.service.delete_event(event_id)

                messagebox.showinfo(
                    "Thành công",
                    "Đã xóa sự kiện!"
                )

            else:
                messagebox.showinfo(
                    "Thông báo",
                    "Chưa kết nối chức năng xóa sự kiện."
                )
                
        except Exception as e:
            messagebox.showerror(
                "Lỗi",
                str(e)
            )

    def search_event(self):
        window = tk.Toplevel(self.root)
        window.title("Tìm kiếm sự kiện")
        window.geometry("350x200")

        tk.Label(
            window,
            text="Nhập tên sự kiện hoặc mã sự kiện:"
        ).pack(pady=10)

        search_entry = ttk.Entry(
            window,
            width=30
        )
        search_entry.pack(pady=5)

        def do_search():
            keyword = search_entry.get()

            try:
                if hasattr(self.service, "search_event"):
                    events = self.service.search_event(keyword)
                    
                    for item in self.event_table.get_children():
                        self.event_table.delete(item)

                    for event in events:
                        self.event_table.insert(
                            "",
                            "end",
                            values=(
                                getattr(event, "event_id", ""),
                                getattr(event, "name", ""),
                                getattr(event, "date", ""),
                                getattr(event, "location", ""),
                                getattr(event, "capacity", "")
                            )
                        )

                    window.destroy()
                    
                else:
                    messagebox.showinfo(
                        "Thông báo",
                        "Chưa kết nối chức năng tìm kiếm sự kiện."
                    )

            except Exception as e:
                messagebox.showerror(
                    "Lỗi",
                    str(e)
                )

        ttk.Button(
            window,
            text="Tìm kiếm",
            command=do_search
        ).pack(pady=15)

    # =========================
    # ĐĂNG KÝ
    # =========================
    def show_registrations(self):
        self.clear_content()
        self.create_title("QUẢN LÝ ĐĂNG KÝ")

        ttk.Button(
            self.content,
            text="Đăng ký sự kiện",
            command=self.register_form
        ).pack(pady=10)

        ttk.Button(
            self.content,
            text="Hủy đăng ký",
            command=self.cancel_registration
        ).pack(pady=5)

        ttk.Button(
            self.content,
            text="Điểm danh",
            command=self.attendance_form
        ).pack(pady=5)

        tk.Label(
            self.content,
            text="Quản lý đăng ký và điểm danh thành viên",
            font=("Arial", 12)
        ).pack(pady=30)

    def register_form(self):
        window = tk.Toplevel(self.root)
        window.title("Đăng ký sự kiện")
        window.geometry("400x300")

        tk.Label(
            window,
            text="ĐĂNG KÝ SỰ KIỆN",
            font=("Arial", 16, "bold")
        ).pack(pady=15)

        tk.Label(
            window,
            text="Mã sự kiện"
        ).pack(pady=5)

        event_entry = ttk.Entry(
            window,
            width=30
        )
        event_entry.pack()

        tk.Label(
            window,
            text="Mã thành viên"
        ).pack(pady=5)

        member_entry = ttk.Entry(
            window,
            width=30
        )
        member_entry.pack()

        def register():
            event_id = event_entry.get()
            member_id = member_entry.get()

            try:
                if hasattr(self.service, "register"):
                    self.service.register(
                        event_id,
                        member_id
                    )

                    messagebox.showinfo(
                        "Thành công",
                        "Đăng ký sự kiện thành công!"
                    )

                    window.destroy()

                else:
                    messagebox.showinfo(
                        "Thông báo",
                        "Chưa kết nối chức năng đăng ký."
                    )

            except Exception as e:
                messagebox.showerror(
                    "Lỗi",
                    str(e)
                )

        ttk.Button(
            window,
            text="Đăng ký",
            command=register
        ).pack(pady=20)

        ttk.Button(
            window,
            text="Hủy",
            command=window.destroy
        ).pack()

    def cancel_registration(self):
        window = tk.Toplevel(self.root)
        window.title("Hủy đăng ký")
        window.geometry("350x220")

        tk.Label(
            window,
            text="HỦY ĐĂNG KÝ",
            font=("Arial", 16, "bold")
        ).pack(pady=15)

        tk.Label(
            window,
            text="Mã đăng ký"
        ).pack(pady=5)

        registration_entry = ttk.Entry(
            window,
            width=30
        )
        registration_entry.pack()

        def cancel():
            registration_id = registration_entry.get()

            try:
                if hasattr(self.service, "cancel"):
                    self.service.cancel(registration_id)

                    messagebox.showinfo(
                        "Thành công",
                        "Đã hủy đăng ký!"
                    )

                    window.destroy()

                else:
                    messagebox.showinfo(
                        "Thông báo",
                        "Chưa kết nối chức năng hủy đăng ký."
                    )

            except Exception as e:
                messagebox.showerror(
                    "Lỗi",
                    str(e)
                )

        ttk.Button(
            window,
            text="Hủy đăng ký",
            command=cancel
        ).pack(pady=20)

        ttk.Button(
            window,
            text="Đóng",
            command=window.destroy
        ).pack()

    def attendance_form(self):
        window = tk.Toplevel(self.root)
        window.title("Điểm danh")
        window.geometry("350x250")

        tk.Label(
            window,
            text="ĐIỂM DANH",
            font=("Arial", 16, "bold")
        ).pack(pady=15)

        tk.Label(
            window,
            text="Mã đăng ký"
        ).pack(pady=5)

        registration_entry = ttk.Entry(
            window,
            width=30
        )
        registration_entry.pack()

        def mark_attendance():
            registration_id = registration_entry.get()

            try:
                if hasattr(self.service, "mark_attendance"):
                    self.service.mark_attendance(registration_id)

                    messagebox.showinfo(
                        "Thành công",
                        "Điểm danh thành công!"
                    )

                    window.destroy()

                else:
                    messagebox.showinfo(
                        "Thông báo",
                        "Chưa kết nối chức năng điểm danh."
                    )

            except Exception as e:
                messagebox.showerror(
                    "Lỗi",
                    str(e)
                )

        ttk.Button(
            window,
            text="Điểm danh",
            command=mark_attendance
        ).pack(pady=20)

        ttk.Button(
            window,
            text="Đóng",
            command=window.destroy
        ).pack()

    # =========================
    # HOẠT ĐỘNG
    # =========================
    def show_activities(self):
        self.clear_content()
        self.create_title("QUẢN LÝ HOẠT ĐỘNG")

        ttk.Button(
            self.content,
            text="Thêm hoạt động",
            command=self.add_activity_form
        ).pack(pady=10)

        ttk.Button(
            self.content,
            text="Xem hoạt động",
            command=self.view_activities
        ).pack(pady=5)

        tk.Label(
            self.content,
            text="Quản lý điểm hoạt động và tình trạng tham gia",
            font=("Arial", 12)
        ).pack(pady=30)

    def add_activity_form(self):
        window = tk.Toplevel(self.root)
        window.title("Thêm hoạt động")
        window.geometry("400x400")

        tk.Label(
            window,
            text="THÊM HOẠT ĐỘNG",
            font=("Arial", 16, "bold")
        ).pack(pady=15)

        fields = [
            ("Mã hoạt động", "activity_id"),
            ("Mã sự kiện", "event_id"),
            ("Mã thành viên", "member_id"),
            ("Điểm", "points"),
            ("Tham gia", "attendance"),
            ("Ghi chú", "note")
        ]

        entries = {}

        for label, key in fields:
            frame = tk.Frame(window)
            frame.pack(pady=5)

            tk.Label(
                frame,
                text=label,
                width=15,
                anchor="w"
            ).pack(side="left")

            entry = ttk.Entry(
                frame,
                width=25
            )
            entry.pack(side="left")

            entries[key] = entry

        def save():
            data = {
                "activity_id": entries["activity_id"].get(),
                "event_id": entries["event_id"].get(),
                "member_id": entries["member_id"].get(),
                "points": entries["points"].get(),
                "attendance": entries["attendance"].get(),
                "note": entries["note"].get()
            }

            try:
                if hasattr(self.service, "create_activity"):
                    self.service.create_activity(data)
                    
                    messagebox.showinfo(
                        "Thành công",
                        "Đã thêm hoạt động!"
                    )
                    
                    window.destroy()

                else:
                    messagebox.showinfo(
                        "Thông báo",
                        "Chưa kết nối chức năng thêm hoạt động."
                    )

            except Exception as e:
                messagebox.showerror(
                    "Lỗi",
                    str(e)
                )

        ttk.Button(
            window,
            text="Lưu",
            command=save
        ).pack(pady=20)

        ttk.Button(
            window,
            text="Hủy",
            command=window.destroy
        ).pack()

    def view_activities(self):
        window = tk.Toplevel(self.root)
        window.title("Danh sách hoạt động")
        window.geometry("800x400")

        tk.Label(
            window,
            text="DANH SÁCH HOẠT ĐỘNG",
            font=("Arial", 16, "bold")
        ).pack(pady=15)

        columns = (
            "Mã hoạt động",
            "Mã sự kiện",
            "Mã thành viên",
            "Điểm",
            "Tham gia",
            "Ghi chú"
        )

        table = ttk.Treeview(
            window,
            columns=columns,
            show="headings"
        )

        for column in columns:
            table.heading(column, text=column)
            table.column(column, width=120)
            
            table.pack(
                fill="both",
                expand=True,
                padx=10,
                pady=10
            )

        try:
            if hasattr(self.service, "get_activities"):
                activities = self.service.get_activities()
                
                for activity in activities:
                    table.insert(
                        "",
                        "end",
                        values=(
                            getattr(activity, "activity_id", ""),
                            getattr(activity, "event_id", ""),
                            getattr(activity, "member_id", ""),
                            getattr(activity, "points", ""),
                            getattr(activity, "attendance", ""),
                            getattr(activity, "note", "")
                        )
                    )

            else:
                messagebox.showinfo(
                    "Thông báo",
                    "Chưa kết nối chức năng xem hoạt động."
                )

        except Exception as e:
            messagebox.showerror(
                "Lỗi",
                str(e)
            )

    # =========================
    # HỘI PHÍ
    # =========================

    def show_fees(self):
        self.clear_content()
        self.create_title("QUẢN LÝ HỘI PHÍ")

        button_frame = tk.Frame(self.content)
        button_frame.pack(pady=10)
        
        ttk.Button(
            button_frame,
            text="Cập nhật trạng thái đã đóng",
            command=self.update_fee
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame,
            text="Làm mới",
            command=self.show_fees
        ).pack(side="left", padx=5)

        columns = (
            "Mã hội phí",
            "Mã thành viên",
            "Số tiền",
            "Hạn đóng",
            "Ngày đóng",
            "Trạng thái",
            "Ghi chú"
        )

        self.fee_table = ttk.Treeview(
            self.content,
            columns=columns,
            show="headings"
        )

        for column in columns:
            self.fee_table.heading(
                column,
                text=column
            )

            self.fee_table.column(
                column,
                width=110
            )

        self.fee_table.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # Lấy danh sách hội phí
        try:
            if hasattr(self.service, "get_fees"):
                fees = self.service.get_fees()
                
                for fee in fees:
                    self.fee_table.insert(
                        "",
                        "end",
                        values=(
                            getattr(fee, "fee_id", ""),
                            getattr(fee, "member_id", ""),
                            getattr(fee, "amount", ""),
                            getattr(fee, "due_date", ""),
                            getattr(fee, "paid_date", ""),
                            getattr(fee, "status", ""),
                            getattr(fee, "note", "")
                        )
                    )

            else:
                messagebox.showinfo(
                    "Thông báo",
                    "Chưa kết nối chức năng xem hội phí."
                )

        except Exception as e:
            messagebox.showerror(
                "Lỗi",
                str(e)
            )


    def update_fee(self):
        selected = self.fee_table.selection()
        
        if not selected:
            messagebox.showwarning(
                "Thông báo",
                "Vui lòng chọn hội phí cần cập nhật!"
            )
            return

        item = self.fee_table.item(selected[0])
        fee_id = item["values"][0]
        
        confirm = messagebox.askyesno(
            "Xác nhận",
            "Bạn có chắc muốn cập nhật hội phí này thành đã đóng không?"
        )

        if not confirm:
            return
        
        try:
            if hasattr(self.service, "mark_paid"):
                self.service.mark_paid(fee_id)
                
                messagebox.showinfo(
                    "Thành công",
                    "Đã cập nhật trạng thái hội phí!"
                )

                self.show_fees()
                
            else:
                messagebox.showinfo(
                    "Thông báo",
                    "Chưa kết nối chức năng cập nhật hội phí."
                )
                    
        except Exception as e:
            messagebox.showerror(
                "Lỗi",
                str(e)
            )