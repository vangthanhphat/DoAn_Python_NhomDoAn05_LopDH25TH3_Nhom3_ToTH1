import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import datetime
import os
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

from DatabaseQLBN import get_connection, init_database

# ==================== ĐƯỜNG DẪN TÀI NGUYÊN ====================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(BASE_DIR, "assets", "logo.png")

# ==================== HÀM TIỆN ÍCH CANH GIỮA CỬA SỔ ====================
def center_window(win, w=800, h=600):
    win.update_idletasks()
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = max(0, (ws // 2) - (w // 2))
    y = max(0, (hs // 2) - (h // 2))
    win.geometry(f"{w}x{h}+{x}+{y}")

# ==============================================================================
# CLASS ĐĂNG NHẬP (LOGIN)
# ==============================================================================
class LoginWindow:
        # Khởi tạo form đăng nhập và các trường nhập liệu tài khoản
    def __init__(self, root):
        self.root = root
        self.root.title("ĐĂNG NHẬP - HỆ THỐNG QUẢN LÝ BỆNH NHÂN")
        self.root.resizable(False, False)
        self.root.config(bg="#F0FDFA")
        center_window(self.root, 440, 560)

        # Biến lưu trữ form
        self.username_var = tk.StringVar(value="admin")
        self.password_var = tk.StringVar(value="123")

        # Khởi tạo CSDL tự động nếu chưa có (không xóa dữ liệu đã có)
        init_database(force=False)

        # Frame chứa toàn bộ nội dung
        main_frame = tk.Frame(self.root, bg="#FFFFFF", padx=30, pady=25, highlightbackground="#0D9488", highlightthickness=2)
        main_frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=520)

        # Hiển thị Logo
        if os.path.exists(LOGO_PATH):
            try:
                img = Image.open(LOGO_PATH).resize((80, 80), Image.Resampling.LANCZOS)
                self.logo_img = ImageTk.PhotoImage(img)
                lbl_logo = tk.Label(main_frame, image=self.logo_img, bg="#FFFFFF")
                lbl_logo.pack(pady=(0, 5))
            except Exception:
                pass

        # Tiêu đề
        lbl_title = tk.Label(main_frame, text="PHÒNG KHÁM ĐA KHOA", font=("Times New Roman", 16, "bold"), fg="#0F766E", bg="#FFFFFF")
        lbl_title.pack()
        lbl_sub = tk.Label(main_frame, text="HỆ THỐNG QUẢN LÝ BỆNH NHÂN", font=("Times New Roman", 12, "bold"), fg="#0284C7", bg="#FFFFFF")
        lbl_sub.pack(pady=(0, 15))

        # Form nhập liệu
        form_frame = tk.Frame(main_frame, bg="#FFFFFF")
        form_frame.pack(fill="x", pady=5)

        tk.Label(form_frame, text="Tên đăng nhập:", font=("Times New Roman", 12, "bold"), fg="#334155", bg="#FFFFFF").pack(anchor="w", pady=(5, 2))
        self.entry_user = tk.Entry(form_frame, textvariable=self.username_var, font=("Times New Roman", 12), relief="solid", bd=1)
        self.entry_user.pack(fill="x", ipady=4)

        tk.Label(form_frame, text="Mật khẩu:", font=("Times New Roman", 12, "bold"), fg="#334155", bg="#FFFFFF").pack(anchor="w", pady=(10, 2))
        self.entry_pwd = tk.Entry(form_frame, textvariable=self.password_var, show="*", font=("Times New Roman", 12), relief="solid", bd=1)
        self.entry_pwd.pack(fill="x", ipady=4)

        # Nút bấm đăng nhập, đăng ký & thoát
        btn_frame = tk.Frame(main_frame, bg="#FFFFFF")
        btn_frame.pack(fill="x", pady=(18, 10))

        btn_login = tk.Button(btn_frame, text="ĐĂNG NHẬP", font=("Times New Roman", 12, "bold"), bg="#0D9488", fg="white",
                              cursor="hand2", relief="flat", command=self.handle_login)
        btn_login.pack(fill="x", ipady=5, pady=(0, 6))

        btn_reg = tk.Button(btn_frame, text="Đăng ký tài khoản nhân viên", font=("Times New Roman", 11), bg="#E0F2FE", fg="#0369A1",
                            cursor="hand2", relief="flat", command=self.open_register_window)
        btn_reg.pack(fill="x", ipady=4, pady=(0, 6))

        # Gợi ý tài khoản demo
        lbl_hint = tk.Label(main_frame, text="Tài khoản: admin | bsminh | dsanh | ttphat | tntriet (MK: 123)",
                            font=("Times New Roman", 10, "italic"), fg="#64748B", bg="#FFFFFF")
        lbl_hint.pack(side="bottom")

        self.entry_user.focus_set()
        
    # Xử lý xác thực đăng nhập: kiểm tra tài khoản, mật khẩu băm SHA-256 và phân quyền người dùng
    def handle_login(self):
        username = self.username_var.get().strip()
        pwd = self.password_var.get().strip()

        if not username or not pwd:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ Tên đăng nhập và Mật khẩu!")
            return

        conn = get_connection()
        if not conn:
            messagebox.showerror("Lỗi", "Không thể kết nối đến máy chủ MySQL!")
            return

        try:
            cur = conn.cursor()
            cur.execute("SELECT manv, hoten, vaitro FROM nhanvien WHERE tendangnhap=%s AND matkhau=%s", (username, pwd))
            user = cur.fetchone()
            conn.close()

            if user:
                manv, hoten, vaitro = user
                messagebox.showinfo("Thành công", f"Đăng nhập thành công!\nXin chào: {hoten} ({vaitro})")
                self.root.destroy()
                # Khởi động ứng dụng chính
                main_root = tk.Tk()
                QuanLyBenhNhanApp(main_root, current_user={"manv": manv, "hoten": hoten, "vaitro": vaitro})
                main_root.mainloop()
            else:
                messagebox.showerror("Lỗi", "Tên đăng nhập hoặc Mật khẩu không chính xác!")
                self.entry_pwd.delete(0, tk.END)
                self.entry_pwd.focus_set()
        except Exception as e:
            messagebox.showerror("Lỗi CSDL", f"Đã xảy ra lỗi:\n{e}")

    # Mở cửa sổ popup đăng ký tài khoản nhân viên y tế mới
    def open_register_window(self):
        self.root.withdraw()
        reg_win = tk.Toplevel(self.root)
        reg_win.title("ĐĂNG KÝ TÀI KHOẢN NHÂN VIÊN Y TẾ")
        reg_win.config(bg="#F0FDFA")
        center_window(reg_win, 480, 560)
        reg_win.resizable(False, False)

        frame = tk.Frame(reg_win, bg="#FFFFFF", padx=25, pady=20, highlightbackground="#0D9488", highlightthickness=2)
        frame.place(relx=0.5, rely=0.5, anchor="center", width=440, height=520)

        tk.Label(frame, text="ĐĂNG KÝ NHÂN VIÊN MỚI", font=("Times New Roman", 15, "bold"), fg="#0F766E", bg="#FFFFFF").pack(pady=(0, 15))

        fields = [
            ("Mã nhân viên:", tk.Entry),
            ("Họ và tên:", tk.Entry),
            ("Số điện thoại:", tk.Entry),
            ("Email:", tk.Entry),
            ("Tên đăng nhập:", tk.Entry),
            ("Mật khẩu:", tk.Entry),
        ]
        entries = {}
        for label_text, widget_cls in fields:
            f = tk.Frame(frame, bg="#FFFFFF")
            f.pack(fill="x", pady=3)
            tk.Label(f, text=label_text, font=("Times New Roman", 11, "bold"), fg="#334155", bg="#FFFFFF", width=14, anchor="w").pack(side="left")
            e = widget_cls(f, font=("Times New Roman", 11), relief="solid", bd=1)
            if label_text == "Mật khẩu:":
                e.config(show="*")
            e.pack(side="right", expand=True, fill="x", ipady=2)
            entries[label_text] = e

        # Vai trò combobox
        f_role = tk.Frame(frame, bg="#FFFFFF")
        f_role.pack(fill="x", pady=3)
        tk.Label(f_role, text="Vai trò:", font=("Times New Roman", 11, "bold"), fg="#334155", bg="#FFFFFF", width=14, anchor="w").pack(side="left")
        cbb_role = ttk.Combobox(f_role, values=["Bác sĩ", "Tiếp tân", "Thu ngân", "Dược sĩ"], font=("Times New Roman", 11), state="readonly")
        cbb_role.set("Bác sĩ")
        cbb_role.pack(side="right", expand=True, fill="x")

        # Xử lý sự kiện lưu đăng ký tài khoản nhân viên mới vào CSDL MySQL
        def submit_reg():
            manv = entries["Mã nhân viên:"].get().strip()
            hoten = entries["Họ và tên:"].get().strip()
            sdt = entries["Số điện thoại:"].get().strip()
            email = entries["Email:"].get().strip()
            user = entries["Tên đăng nhập:"].get().strip()
            pwd = entries["Mật khẩu:"].get().strip()
            role = cbb_role.get().strip()

            if not all([manv, hoten, user, pwd, role]):
                messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ các trường bắt buộc!")
                return

            conn = get_connection()
            if not conn:
                messagebox.showerror("Lỗi", "Không thể kết nối CSDL!")
                return
            try:
                cur = conn.cursor()
                cur.execute("SELECT manv FROM nhanvien WHERE manv=%s OR tendangnhap=%s", (manv, user))
                if cur.fetchone():
                    messagebox.showerror("Trùng lặp", "Mã nhân viên hoặc Tên đăng nhập đã tồn tại!")
                    conn.close()
                    return

                cur.execute("""
                    INSERT INTO nhanvien (manv, hoten, sodienthoai, email, tendangnhap, matkhau, vaitro)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (manv, hoten, sdt, email, user, pwd, role))
                conn.commit()
                conn.close()
                messagebox.showinfo("Thành công", "Đăng ký tài khoản nhân viên thành công!")
                reg_win.destroy()
                self.root.deiconify()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể đăng ký:\n{e}")

        # Đóng cửa sổ đăng ký và hiện lại cửa sổ đăng nhập chính
        def on_close():
            reg_win.destroy()
            self.root.deiconify()

        reg_win.protocol("WM_DELETE_WINDOW", on_close)

        btn_save = tk.Button(frame, text="HOÀN TẤT ĐĂNG KÝ", font=("Times New Roman", 12, "bold"), bg="#0D9488", fg="white",
                             cursor="hand2", relief="flat", command=submit_reg)
        btn_save.pack(fill="x", ipady=5, pady=(15, 5))

        btn_back = tk.Button(frame, text="Quay lại Đăng nhập", font=("Times New Roman", 11), bg="#F1F5F9", fg="#475569",
                             cursor="hand2", relief="flat", command=on_close)
        btn_back.pack(fill="x", ipady=3)


# ==============================================================================
# CLASS PHÂN HỆ KHÁM BỆNH & TOA THUỐC (TÁCH BIỆT: KHÁM NỘI / KHÁM NGOẠI)
# ==============================================================================
class ExamTabHandler:
    """Quản lý độc lập từng phân hệ Khám bệnh & Kê đơn thuốc (Khám nội / Khám ngoại)"""
    def __init__(self, app, parent, loai_kham="Khám nội"):
        self.app = app
        self.root = app.root
        self.parent = parent
        self.loai_kham = loai_kham  # "Khám nội" hoặc "Khám ngoại"
        self.patients_cache = {}
        self.doctors_cache = {}
        self.khoas_cache = {}
        self.drugs_cache = {}

        self.build_ui()

    def build_ui(self):
        paned = tk.PanedWindow(self.parent, orient="horizontal", bg="#F8FAFC", sashrelief="raised", sashwidth=4)
        paned.pack(fill="both", expand=True, padx=5, pady=5)

        title_left = f" Tiếp nhận & {self.loai_kham} "
        title_right = f" Đơn Thuốc {self.loai_kham} "

        # KHỐI TRÁI: THÔNG TIN KHÁM VÀ BỆNH ÁN
        frame_left = tk.LabelFrame(paned, text=title_left, font=("Times New Roman", 12, "bold"),
                                   fg="#0F766E", bg="#FFFFFF", padx=12, pady=10)
        paned.add(frame_left, minsize=530)

        frame_left.grid_columnconfigure(1, weight=1)
        frame_left.grid_columnconfigure(3, weight=1)

        self.ex_mapk = tk.StringVar()
        self.ex_mabn = tk.StringVar()
        self.ex_bacsi = tk.StringVar()
        self.ex_khoa = tk.StringVar()
        self.ex_huyetap = tk.StringVar(value="120/80")
        self.ex_nhiptim = tk.StringVar(value="75")
        self.ex_cannang = tk.StringVar(value="60.0")

        # Dòng 0: Mã phiếu khám & Chọn Bệnh nhân
        tk.Label(frame_left, text="Mã phiếu (*):", font=("Times New Roman", 11, "bold"), bg="#FFFFFF").grid(row=0, column=0, sticky="w", pady=4)
        tk.Entry(frame_left, textvariable=self.ex_mapk, font=("Times New Roman", 11), width=10, relief="solid", bd=1).grid(row=0, column=1, sticky="we", padx=5, ipady=4)

        lbl_bn = f"Bệnh nhân ({self.loai_kham}) (*):"
        tk.Label(frame_left, text=lbl_bn, font=("Times New Roman", 11, "bold"), bg="#FFFFFF").grid(row=0, column=2, sticky="w", pady=4)
        self.cbb_ex_patient = ttk.Combobox(frame_left, width=20, state="readonly", postcommand=self.reload_patients)
        self.cbb_ex_patient.grid(row=0, column=3, sticky="we", padx=5, ipady=3)
        self.cbb_ex_patient.bind("<<ComboboxSelected>>", self.on_patient_selected)

        # Dòng 1: Bác sĩ & Khoa khám
        tk.Label(frame_left, text="Bác sĩ khám:", font=("Times New Roman", 11, "bold"), bg="#FFFFFF").grid(row=1, column=0, sticky="w", pady=4)
        self.cbb_ex_doctor = ttk.Combobox(frame_left, textvariable=self.ex_bacsi, width=18, state="readonly")
        self.cbb_ex_doctor.grid(row=1, column=1, sticky="we", padx=5, ipady=3)

        tk.Label(frame_left, text="Khoa phòng:", font=("Times New Roman", 11, "bold"), bg="#FFFFFF").grid(row=1, column=2, sticky="w", pady=4)
        self.cbb_ex_khoa = ttk.Combobox(frame_left, textvariable=self.ex_khoa, width=20, state="readonly")
        self.cbb_ex_khoa.grid(row=1, column=3, sticky="we", padx=5, ipady=3)

        # Dòng 2: Dấu hiệu sinh tồn (Huyết áp, Nhịp tim, Cân nặng)
        f_vitals = tk.LabelFrame(frame_left, text=" Dấu hiệu sinh tồn ", font=("Times New Roman", 10, "bold"), bg="#F0FDFA", fg="#0D9488", padx=5, pady=4)
        f_vitals.grid(row=2, column=0, columnspan=4, sticky="we", pady=6)

        tk.Label(f_vitals, text="Huyết áp (mmHg):", font=("Times New Roman", 10), bg="#F0FDFA").pack(side="left", padx=2)
        tk.Entry(f_vitals, textvariable=self.ex_huyetap, font=("Times New Roman", 10), width=9, relief="solid", bd=1).pack(side="left", padx=(0, 10), ipady=2)

        tk.Label(f_vitals, text="Nhịp tim (l/p):", font=("Times New Roman", 10), bg="#F0FDFA").pack(side="left", padx=2)
        tk.Entry(f_vitals, textvariable=self.ex_nhiptim, font=("Times New Roman", 10), width=7, relief="solid", bd=1).pack(side="left", padx=(0, 10), ipady=2)

        tk.Label(f_vitals, text="Cân nặng (kg):", font=("Times New Roman", 10), bg="#F0FDFA").pack(side="left", padx=2)
        tk.Entry(f_vitals, textvariable=self.ex_cannang, font=("Times New Roman", 10), width=7, relief="solid", bd=1).pack(side="left", ipady=2)

        # Dòng 3: Triệu chứng lâm sàng
        tk.Label(frame_left, text="Triệu chứng:", font=("Times New Roman", 11, "bold"), bg="#FFFFFF").grid(row=3, column=0, sticky="nw", pady=4)
        self.txt_ex_trieuchung = tk.Text(frame_left, height=2, font=("Times New Roman", 11), padx=6, pady=4, wrap="word", relief="solid", bd=1)
        self.txt_ex_trieuchung.grid(row=3, column=1, columnspan=3, sticky="we", padx=5, pady=2)

        # Dòng 4: Chẩn đoán
        tk.Label(frame_left, text="Chẩn đoán (*):", font=("Times New Roman", 11, "bold"), bg="#FFFFFF").grid(row=4, column=0, sticky="nw", pady=4)
        self.txt_ex_chandoan = tk.Text(frame_left, height=2, font=("Times New Roman", 11), padx=6, pady=4, wrap="word", relief="solid", bd=1)
        self.txt_ex_chandoan.grid(row=4, column=1, columnspan=3, sticky="we", padx=5, pady=2)

        # Dòng 5: Lời dặn / Kết luận
        tk.Label(frame_left, text="Lời dặn bác sĩ:", font=("Times New Roman", 11, "bold"), bg="#FFFFFF").grid(row=5, column=0, sticky="nw", pady=4)
        self.txt_ex_ketluan = tk.Text(frame_left, height=2, font=("Times New Roman", 11), padx=6, pady=4, wrap="word", relief="solid", bd=1)
        self.txt_ex_ketluan.grid(row=5, column=1, columnspan=3, sticky="we", padx=5, pady=2)

        # Nút thao tác phiếu khám
        f_ex_btn = tk.Frame(frame_left, bg="#FFFFFF")
        f_ex_btn.grid(row=6, column=0, columnspan=4, pady=(10, 5), sticky="we")

        tk.Button(f_ex_btn, text="➕ Tạo phiếu mới", font=("Times New Roman", 11, "bold"), bg="#10B981", fg="white",
                  relief="flat", cursor="hand2", command=self.action_new).pack(side="left", padx=3)
        tk.Button(f_ex_btn, text="💾 Lưu Bệnh Án", font=("Times New Roman", 11, "bold"), bg="#0D9488", fg="white",
                  relief="flat", cursor="hand2", command=self.action_save).pack(side="left", padx=3)
        tk.Button(f_ex_btn, text="🗑️ Xóa Phiếu", font=("Times New Roman", 11, "bold"), bg="#EF4444", fg="white",
                  relief="flat", cursor="hand2", command=self.action_delete).pack(side="left", padx=3)
        tk.Button(f_ex_btn, text="🔄 Làm mới", font=("Times New Roman", 11), bg="#64748B", fg="white",
                  relief="flat", cursor="hand2", command=self.action_clear).pack(side="left", padx=3)

        # Bảng lịch sử khám gần đây
        tk.Label(frame_left, text=f"DANH SÁCH PHIẾU {self.loai_kham.upper()} GẦN ĐÂY:", font=("Times New Roman", 11, "bold"), fg="#334155", bg="#FFFFFF").grid(row=7, column=0, columnspan=4, sticky="w", pady=(10, 2))

        cols_hist = ("mapk", "mabn", "hoten", "ngaykham", "chandoan", "trangthai")
        self.ex_tree_hist = ttk.Treeview(frame_left, columns=cols_hist, show="headings", height=6)
        self.ex_tree_hist.heading("mapk", text="Mã PK")
        self.ex_tree_hist.heading("mabn", text="Mã BN")
        self.ex_tree_hist.heading("hoten", text="Họ tên BN")
        self.ex_tree_hist.heading("ngaykham", text="Ngày khám")
        self.ex_tree_hist.heading("chandoan", text="Chẩn đoán")
        self.ex_tree_hist.heading("trangthai", text="Trạng thái")

        self.ex_tree_hist.column("mapk", width=70, anchor="center")
        self.ex_tree_hist.column("mabn", width=65, anchor="center")
        self.ex_tree_hist.column("hoten", width=120)
        self.ex_tree_hist.column("ngaykham", width=120, anchor="center")
        self.ex_tree_hist.column("chandoan", width=130)
        self.ex_tree_hist.column("trangthai", width=95, anchor="center")

        self.ex_tree_hist.grid(row=8, column=0, columnspan=4, sticky="nsew")
        self.ex_tree_hist.bind("<<TreeviewSelect>>", self.on_select_history)

        # KHỐI PHẢI: KÊ ĐƠN THUỐC ĐIỆN TỬ
        frame_right = tk.LabelFrame(paned, text=title_right, font=("Times New Roman", 12, "bold"),
                                    fg="#0284C7", bg="#FFFFFF", padx=12, pady=10)
        paned.add(frame_right, minsize=480)

        # Khung chọn thuốc từ kho
        f_rx_select = tk.Frame(frame_right, bg="#FFFFFF")
        f_rx_select.pack(fill="x", pady=(0, 5))
        f_rx_select.grid_columnconfigure(1, weight=1)

        tk.Label(f_rx_select, text="Chọn thuốc (*):", font=("Times New Roman", 11, "bold"), bg="#FFFFFF").grid(row=0, column=0, sticky="w")
        self.cbb_rx_drug = ttk.Combobox(f_rx_select, width=26, state="readonly")
        self.cbb_rx_drug.grid(row=0, column=1, padx=5, pady=3, sticky="we", ipady=3)

        tk.Label(f_rx_select, text="Số lượng (*):", font=("Times New Roman", 11, "bold"), bg="#FFFFFF").grid(row=0, column=2, sticky="w")
        self.rx_qty_var = tk.StringVar(value="1")
        tk.Entry(f_rx_select, textvariable=self.rx_qty_var, font=("Times New Roman", 11), width=6, relief="solid", bd=1).grid(row=0, column=3, padx=5, pady=3, sticky="w", ipady=3)

        tk.Label(f_rx_select, text="Cách dùng / Liều:", font=("Times New Roman", 11, "bold"), bg="#FFFFFF").grid(row=1, column=0, sticky="w")
        self.rx_instruction_var = tk.StringVar(value="Uống 1 viên x 2 lần/ngày sau ăn")
        tk.Entry(f_rx_select, textvariable=self.rx_instruction_var, font=("Times New Roman", 11), width=26, relief="solid", bd=1).grid(row=1, column=1, columnspan=2, padx=5, pady=3, sticky="we", ipady=3)

        btn_add_drug = tk.Button(f_rx_select, text="➕ Thêm thuốc", font=("Times New Roman", 10, "bold"), bg="#0284C7", fg="white",
                                 relief="flat", cursor="hand2", command=self.rx_action_add_drug)
        btn_add_drug.grid(row=1, column=3, padx=5, pady=3, sticky="we")

        # Bảng hiển thị danh sách thuốc đã kê
        cols_rx = ("mathuoc", "tenthuoc", "donvitinh", "soluong", "dongia", "thanhtien", "cachdung")
        self.rx_tree = ttk.Treeview(frame_right, columns=cols_rx, show="headings", height=12)
        self.rx_tree.heading("mathuoc", text="Mã")
        self.rx_tree.heading("tenthuoc", text="Tên thuốc")
        self.rx_tree.heading("donvitinh", text="ĐVT")
        self.rx_tree.heading("soluong", text="SL")
        self.rx_tree.heading("dongia", text="Đơn giá")
        self.rx_tree.heading("thanhtien", text="Thành tiền")
        self.rx_tree.heading("cachdung", text="Cách dùng")

        self.rx_tree.column("mathuoc", width=55, anchor="center")
        self.rx_tree.column("tenthuoc", width=140)
        self.rx_tree.column("donvitinh", width=50, anchor="center")
        self.rx_tree.column("soluong", width=45, anchor="center")
        self.rx_tree.column("dongia", width=80, anchor="e")
        self.rx_tree.column("thanhtien", width=85, anchor="e")
        self.rx_tree.column("cachdung", width=160)

        self.rx_tree.pack(fill="both", expand=True, pady=5)

        # Thanh tổng cộng & nút xóa thuốc
        f_rx_bottom = tk.Frame(frame_right, bg="#FFFFFF")
        f_rx_bottom.pack(fill="x", pady=5)

        btn_del_drug = tk.Button(f_rx_bottom, text="❌ Xóa thuốc chọn", font=("Times New Roman", 10, "bold"), bg="#EF4444", fg="white",
                                 relief="flat", cursor="hand2", command=self.rx_action_remove_drug)
        btn_del_drug.pack(side="left")

        self.lbl_rx_total = tk.Label(f_rx_bottom, text="Tổng tiền thuốc: 0 đ", font=("Times New Roman", 12, "bold"), fg="#DC2626", bg="#FFFFFF")
        self.lbl_rx_total.pack(side="right")

        # Nạp dữ liệu ban đầu
        self.load_comboboxes()
        self.load_history()

    def reload_patients(self):
        """Tự động làm mới danh sách bệnh nhân phù hợp với phân loại Khám nội / Khám ngoại"""
        conn = get_connection()
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute("SELECT mabn, holot, ten FROM benhnhan WHERE loaikham = %s ORDER BY mabn ASC", (self.loai_kham,))
            rows = cur.fetchall()
            conn.close()
            self.patients_cache = {f"{r[0]} - {r[1]} {r[2]}": r[0] for r in rows}
            self.cbb_ex_patient["values"] = list(self.patients_cache.keys())
            curr = self.cbb_ex_patient.get().strip()
            if curr in self.patients_cache:
                self.ex_mabn.set(self.patients_cache[curr])
            elif " - " in curr:
                self.ex_mabn.set(curr.split(" - ")[0].strip())
            elif rows and not curr:
                first_val = list(self.patients_cache.keys())[0]
                self.cbb_ex_patient.set(first_val)
                self.ex_mabn.set(self.patients_cache[first_val])
        except Exception:
            pass

    def load_comboboxes(self):
        conn = get_connection()
        if not conn:
            return
        cur = conn.cursor()
        # Bệnh nhân theo Loại khám
        cur.execute("SELECT mabn, holot, ten FROM benhnhan WHERE loaikham = %s ORDER BY mabn ASC", (self.loai_kham,))
        rows = cur.fetchall()
        self.patients_cache = {f"{r[0]} - {r[1]} {r[2]}": r[0] for r in rows}
        self.cbb_ex_patient["values"] = list(self.patients_cache.keys())
        if rows:
            first_val = list(self.patients_cache.keys())[0]
            self.cbb_ex_patient.set(first_val)
            self.ex_mabn.set(self.patients_cache[first_val])
        else:
            self.cbb_ex_patient.set("")
            self.ex_mabn.set("")

        # Bác sĩ
        cur.execute("SELECT manv, hoten FROM nhanvien WHERE vaitro='Bác sĩ' OR vaitro='Admin' ORDER BY hoten ASC")
        docs = cur.fetchall()
        self.doctors_cache = {f"{r[0]} - {r[1]}": r[0] for r in docs}
        self.cbb_ex_doctor["values"] = list(self.doctors_cache.keys())
        if docs:
            self.cbb_ex_doctor.set(list(self.doctors_cache.keys())[0])

        # Khoa phòng phân theo Khám nội / Khám ngoại
        if self.loai_kham == "Khám nội":
            # Khoa nội: K02 - Khoa Nội Tổng Hợp, K06 - Khoa Tim Mạch, K04 - Khoa Nhi
            cur.execute("SELECT makhoa, tenkhoa FROM khoaphong WHERE makhoa IN ('K02', 'K06', 'K04') ORDER BY FIELD(makhoa, 'K02', 'K06', 'K04')")
        else:
            # Khoa ngoại: K03 - Khoa Ngoại Tổng Quát, K05 - Khoa Tai Mũi Họng, K01 - Khoa Khám Bệnh
            cur.execute("SELECT makhoa, tenkhoa FROM khoaphong WHERE makhoa IN ('K03', 'K05', 'K01') ORDER BY FIELD(makhoa, 'K03', 'K05', 'K01')")
        khoas = cur.fetchall()
        self.khoas_cache = {f"{r[0]} - {r[1]}": r[0] for r in khoas}
        self.cbb_ex_khoa["values"] = list(self.khoas_cache.keys())
        if khoas:
            first_khoa = list(self.khoas_cache.keys())[0]
            self.cbb_ex_khoa.set(first_khoa)
            self.ex_khoa.set(self.khoas_cache[first_khoa])
        else:
            self.cbb_ex_khoa.set("")
            self.ex_khoa.set("")

        # Thuốc
        cur.execute("SELECT mathuoc, tenthuoc, donvitinh, dongia, soluongton FROM thuoc WHERE soluongton > 0 ORDER BY tenthuoc ASC")
        drugs = cur.fetchall()
        self.drugs_cache = {f"{r[0]} | {r[1]} ({r[2]}) - {int(r[3]):,}đ [Tồn: {r[4]}]": {
            "mathuoc": r[0], "tenthuoc": r[1], "donvitinh": r[2], "dongia": float(r[3]), "soluongton": r[4]
        } for r in drugs}
        self.cbb_rx_drug["values"] = list(self.drugs_cache.keys())
        if drugs:
            self.cbb_rx_drug.set(list(self.drugs_cache.keys())[0])

        conn.close()

    def on_patient_selected(self, event=None):
        val = self.cbb_ex_patient.get().strip()
        if val in self.patients_cache:
            self.ex_mabn.set(self.patients_cache[val])
        elif " - " in val:
            self.ex_mabn.set(val.split(" - ")[0].strip())
        elif val:
            self.ex_mabn.set(val)

    def load_history(self):
        for r in self.ex_tree_hist.get_children():
            self.ex_tree_hist.delete(r)
        conn = get_connection()
        if not conn:
            return
        cur = conn.cursor()
        sql = """
            SELECT pk.mapk, pk.mabn, CONCAT(bn.holot, ' ', bn.ten) as hoten, pk.ngaykham, pk.chandoan, pk.trangthai
            FROM phieukham pk
            JOIN benhnhan bn ON pk.mabn = bn.mabn
            WHERE bn.loaikham = %s
            ORDER BY pk.ngaykham DESC LIMIT 30
        """
        cur.execute(sql, (self.loai_kham,))
        for row in cur.fetchall():
            nk = row[3].strftime("%d/%m/%Y %H:%M") if row[3] else ""
            self.ex_tree_hist.insert("", "end", values=(row[0], row[1], row[2], nk, row[4], row[5]))
        conn.close()

    def on_select_history(self, event):
        sel = self.ex_tree_hist.selection()
        if not sel:
            return
        mapk = self.ex_tree_hist.item(sel[0])["values"][0]
        conn = get_connection()
        if not conn:
            return
        cur = conn.cursor()
        cur.execute("""
            SELECT mapk, mabn, manv_bacsi, makhoa, ngaykham, trieuchung, huyetap, nhiptim, cannang, chandoan, ketluan, trangthai
            FROM phieukham WHERE mapk=%s
        """, (mapk,))
        row = cur.fetchone()
        if row:
            self.ex_mapk.set(row[0])
            self.ex_mabn.set(row[1])
            # Set combobox bệnh nhân
            for k, v in self.patients_cache.items():
                if v == row[1]:
                    self.cbb_ex_patient.set(k)
                    break
            # Set combobox bác sĩ
            for k, v in self.doctors_cache.items():
                if v == row[2]:
                    self.cbb_ex_doctor.set(k)
                    break
            # Set combobox khoa
            for k, v in self.khoas_cache.items():
                if v == row[3]:
                    self.cbb_ex_khoa.set(k)
                    break

            self.txt_ex_trieuchung.delete("1.0", tk.END)
            self.txt_ex_trieuchung.insert("1.0", row[5] or "")

            self.ex_huyetap.set(row[6] or "120/80")
            self.ex_nhiptim.set(str(row[7] or 75))
            self.ex_cannang.set(str(row[8] or 60.0))

            self.txt_ex_chandoan.delete("1.0", tk.END)
            self.txt_ex_chandoan.insert("1.0", row[9] or "")

            self.txt_ex_ketluan.delete("1.0", tk.END)
            self.txt_ex_ketluan.insert("1.0", row[10] or "")

            # Nạp lại danh sách thuốc đã kê của phiếu khám này
            self.rx_load_prescription(mapk)

        conn.close()

    def rx_load_prescription(self, mapk):
        for r in self.rx_tree.get_children():
            self.rx_tree.delete(r)
        conn = get_connection()
        if not conn:
            return
        cur = conn.cursor()
        cur.execute("SELECT mathuoc, tenthuoc, donvitinh, soluong, dongia, thanhtien, cachdung FROM toathuoc_chitiet WHERE mapk=%s", (mapk,))
        total = 0
        for r in cur.fetchall():
            self.rx_tree.insert("", "end", values=(r[0], r[1], r[2], r[3], f"{int(r[4]):,}đ", f"{int(r[5]):,}đ", r[6]))
            total += float(r[5])
        self.lbl_rx_total.config(text=f"Tổng tiền thuốc: {int(total):,} đ")
        conn.close()

    def action_new(self):
        self.action_clear()
        conn = get_connection()
        if conn:
            cur = conn.cursor()
            cur.execute("SELECT mapk FROM phieukham WHERE mapk LIKE 'PK%' ORDER BY LENGTH(mapk) DESC, mapk DESC LIMIT 1")
            row = cur.fetchone()
            conn.close()
            if row and row[0].startswith("PK"):
                try:
                    num = int(row[0][2:]) + 1
                    self.ex_mapk.set(f"PK{num:03d}")
                except Exception:
                    self.ex_mapk.set("PK001")
            else:
                self.ex_mapk.set("PK001")

    def action_clear(self):
        self.ex_mapk.set("")
        if hasattr(self, "cbb_ex_patient") and self.cbb_ex_patient["values"]:
            first_val = self.cbb_ex_patient["values"][0]
            self.cbb_ex_patient.set(first_val)
            self.ex_mabn.set(self.patients_cache.get(first_val, first_val.split(" - ")[0].strip()))
        else:
            self.ex_mabn.set("")
            if hasattr(self, "cbb_ex_patient"):
                self.cbb_ex_patient.set("")
        if hasattr(self, "cbb_ex_khoa") and self.cbb_ex_khoa["values"]:
            self.cbb_ex_khoa.set(self.cbb_ex_khoa["values"][0])
        self.txt_ex_trieuchung.delete("1.0", tk.END)
        self.txt_ex_chandoan.delete("1.0", tk.END)
        self.txt_ex_ketluan.delete("1.0", tk.END)
        for r in self.rx_tree.get_children():
            self.rx_tree.delete(r)
        self.lbl_rx_total.config(text="Tổng tiền thuốc: 0 đ")

    def rx_action_add_drug(self):
        drug_label = self.cbb_rx_drug.get()
        if drug_label not in self.drugs_cache:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn thuốc hợp lệ từ danh mục!", parent=self.root)
            return
        drug_info = self.drugs_cache[drug_label]

        try:
            qty = int(self.rx_qty_var.get().strip())
            if qty <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showwarning("Cảnh báo", "Số lượng thuốc phải là số nguyên dương!", parent=self.root)
            return

        if qty > drug_info["soluongton"]:
            messagebox.showwarning("Hết hàng", f"Số lượng thuốc tồn kho chỉ còn {drug_info['soluongton']} {drug_info['donvitinh']}!", parent=self.root)
            return

        instruction = self.rx_instruction_var.get().strip()
        thanhtien = qty * drug_info["dongia"]

        for child in self.rx_tree.get_children():
            if self.rx_tree.item(child)["values"][0] == drug_info["mathuoc"]:
                messagebox.showwarning("Thông báo", "Thuốc này đã có trong toa, hãy xóa dòng cũ trước nếu muốn sửa số lượng!", parent=self.root)
                return

        self.rx_tree.insert("", "end", values=(
            drug_info["mathuoc"], drug_info["tenthuoc"], drug_info["donvitinh"],
            qty, f"{int(drug_info['dongia']):,}đ", f"{int(thanhtien):,}đ", instruction
        ))
        self.rx_calculate_total()

    def rx_action_remove_drug(self):
        sel = self.rx_tree.selection()
        if not sel:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn dòng thuốc muốn xóa khỏi toa!", parent=self.root)
            return
        self.rx_tree.delete(sel[0])
        self.rx_calculate_total()

    def rx_calculate_total(self):
        total = 0
        for child in self.rx_tree.get_children():
            val = self.rx_tree.item(child)["values"][5]
            clean_val = str(val).replace(",", "").replace("đ", "").strip()
            total += float(clean_val)
        self.lbl_rx_total.config(text=f"Tổng tiền thuốc: {int(total):,} đ")

    def action_save(self):
        mapk = self.ex_mapk.get().strip()
        mabn = self.ex_mabn.get().strip()
        cbb_p_val = self.cbb_ex_patient.get().strip()
        if not mabn and cbb_p_val:
            if cbb_p_val in self.patients_cache:
                mabn = self.patients_cache[cbb_p_val]
            elif " - " in cbb_p_val:
                mabn = cbb_p_val.split(" - ")[0].strip()
            else:
                mabn = cbb_p_val
            self.ex_mabn.set(mabn)

        doc_label = self.cbb_ex_doctor.get().strip()
        khoa_label = self.cbb_ex_khoa.get().strip()
        trieuchung = self.txt_ex_trieuchung.get("1.0", tk.END).strip()
        chandoan = self.txt_ex_chandoan.get("1.0", tk.END).strip()
        ketluan = self.txt_ex_ketluan.get("1.0", tk.END).strip()
        huyetap = self.ex_huyetap.get().strip()

        try:
            nhiptim = int(self.ex_nhiptim.get().strip())
            cannang = float(self.ex_cannang.get().strip())
        except ValueError:
            messagebox.showwarning("Sai định dạng", "Nhịp tim và cân nặng phải là số!", parent=self.root)
            return

        if not mapk or not mabn or not chandoan:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ: Mã phiếu khám, Bệnh nhân và Chẩn đoán bệnh!", parent=self.root)
            return

        manv_bacsi = self.doctors_cache.get(doc_label)
        if not manv_bacsi and " - " in doc_label:
            manv_bacsi = doc_label.split(" - ")[0].strip()
        if not manv_bacsi:
            manv_bacsi = "NV01"

        makhoa = self.khoas_cache.get(khoa_label)
        if not makhoa and " - " in khoa_label:
            makhoa = khoa_label.split(" - ")[0].strip()
        if not makhoa:
            makhoa = "K01"

        ngaykham = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = get_connection()
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute("SELECT mapk FROM phieukham WHERE mapk=%s", (mapk,))
            exists = cur.fetchone()

            if exists:
                cur.execute("""
                    UPDATE phieukham
                    SET mabn=%s, manv_bacsi=%s, makhoa=%s, trieuchung=%s, huyetap=%s, nhiptim=%s, cannang=%s, chandoan=%s, ketluan=%s
                    WHERE mapk=%s
                """, (mabn, manv_bacsi, makhoa, trieuchung, huyetap, nhiptim, cannang, chandoan, ketluan, mapk))
            else:
                cur.execute("""
                    INSERT INTO phieukham (mapk, mabn, manv_bacsi, makhoa, ngaykham, trieuchung, huyetap, nhiptim, cannang, chandoan, ketluan, trangthai)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'Chờ thanh toán')
                """, (mapk, mabn, manv_bacsi, makhoa, ngaykham, trieuchung, huyetap, nhiptim, cannang, chandoan, ketluan))

            # Cập nhật chi tiết toa thuốc
            cur.execute("DELETE FROM toathuoc_chitiet WHERE mapk=%s", (mapk,))
            for child in self.rx_tree.get_children():
                v = self.rx_tree.item(child)["values"]
                mathuoc = v[0]
                tenthuoc = v[1]
                donvitinh = v[2]
                soluong = int(v[3])
                dongia = float(str(v[4]).replace(",", "").replace("đ", "").strip())
                thanhtien = float(str(v[5]).replace(",", "").replace("đ", "").strip())
                cachdung = v[6]

                cur.execute("""
                    INSERT INTO toathuoc_chitiet (mapk, mathuoc, tenthuoc, donvitinh, soluong, dongia, cachdung, thanhtien)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (mapk, mathuoc, tenthuoc, donvitinh, soluong, dongia, cachdung, thanhtien))

            conn.commit()
            conn.close()
            messagebox.showinfo("Thành công", f"Đã lưu hồ sơ bệnh án và đơn thuốc cho phiếu khám [{mapk}]!", parent=self.root)
            self.load_history()
        except Exception as e:
            messagebox.showerror("Lỗi CSDL", f"Lỗi khi lưu bệnh án:\n{e}", parent=self.root)

    def action_delete(self):
        mapk = self.ex_mapk.get().strip()
        if not mapk:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn phiếu khám cần xóa!", parent=self.root)
            return
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa phiếu khám [{mapk}] cùng toàn bộ đơn thuốc liên quan?", parent=self.root):
            conn = get_connection()
            if not conn:
                return
            try:
                cur = conn.cursor()
                cur.execute("DELETE FROM phieukham WHERE mapk=%s", (mapk,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Thành công", f"Đã xóa thành công phiếu khám {mapk}!", parent=self.root)
                self.action_clear()
                self.load_history()
            except Exception as e:
                messagebox.showerror("Lỗi CSDL", f"Không thể xóa phiếu khám:\n{e}", parent=self.root)


# ==============================================================================
# CLASS ỨNG DỤNG CHÍNH: QUẢN LÝ BỆNH NHÂN (FULL TABS)
# ==============================================================================
class QuanLyBenhNhanApp:
    # Khởi tạo cửa sổ chính của hệ thống, thiết lập kích thước và các thành phần giao diện
    def __init__(self, root, current_user):
        self.root = root
        self.current_user = current_user
        self.root.title("PHẦN MỀM QUẢN LÝ BỆNH NHÂN & PHÒNG KHÁM ĐA KHOA")
        self.root.geometry("1280x740")
        self.root.minsize(1100, 680)
        self.root.config(bg="#F8FAFC")
        center_window(self.root, 1280, 740)

        # Style cho Tab và Treeview
        self.setup_styles()

        # Tạo Thanh Header
        self.create_header()

        # Tạo Menu Hệ thống
        self.create_menu()

        # Tạo Bộ Tab Điều hướng
        self.create_tabs()

    # Thiết lập giao diện, màu sắc và font chữ cho các Tab và bảng Treeview
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("default")

        # Style Tab
        style.configure("TNotebook", background="#E2E8F0", borderwidth=0)
        style.configure("TNotebook.Tab", font=("Times New Roman", 12, "bold"), padding=[18, 8],
                        background="#CCFBF1", foreground="#0F766E")
        style.map("TNotebook.Tab",
                  background=[("selected", "#0D9488"), ("active", "#99F6E4")],
                  foreground=[("selected", "white"), ("active", "#0F766E")])

        # Style Treeview
        style.configure("Treeview.Heading", font=("Times New Roman", 11, "bold"), background="#0F766E", foreground="white")
        style.configure("Treeview", font=("Times New Roman", 11), rowheight=26, background="#FFFFFF", fieldbackground="#FFFFFF")
        style.map("Treeview", background=[("selected", "#0284C7")], foreground=[("selected", "white")])

        # Style Combobox
        style.configure("TCombobox", font=("Times New Roman", 11), padding=3)

    # Tạo thanh tiêu đề đầu trang: hiển thị logo phòng khám, thông tin người dùng và nút Đăng xuất
    def create_header(self):
        header_frame = tk.Frame(self.root, bg="#0F766E", height=65)
        header_frame.pack(fill="x", side="top")

        # Bên trái: Logo + Tên phần mềm
        left_box = tk.Frame(header_frame, bg="#0F766E")
        left_box.pack(side="left", padx=15, pady=8)

        if os.path.exists(LOGO_PATH):
            try:
                img = Image.open(LOGO_PATH).resize((48, 48), Image.Resampling.LANCZOS)
                self.hdr_logo = ImageTk.PhotoImage(img)
                lbl_icon = tk.Label(left_box, image=self.hdr_logo, bg="#0F766E")
                lbl_icon.pack(side="left", padx=(0, 10))
            except Exception:
                pass

        title_box = tk.Frame(left_box, bg="#0F766E")
        title_box.pack(side="left")
        tk.Label(title_box, text="HỆ THỐNG QUẢN LÝ BỆNH NHÂN", font=("Times New Roman", 16, "bold"), fg="white", bg="#0F766E").pack(anchor="w")
        tk.Label(title_box, text="PHÒNG KHÁM ĐA KHOA AN GIANG", font=("Times New Roman", 10), fg="#99F6E4", bg="#0F766E").pack(anchor="w")

        # Bên phải: Thông tin người dùng + Đăng xuất
        right_box = tk.Frame(header_frame, bg="#0F766E")
        right_box.pack(side="right", padx=15)

        tk.Label(right_box, text=f"👤 {self.current_user['hoten']}  |  Quyền: {self.current_user['vaitro']}",
                 font=("Times New Roman", 11, "bold"), fg="#FEF08A", bg="#0F766E").pack(side="left", padx=10)

        btn_logout = tk.Button(right_box, text="Đăng xuất", font=("Times New Roman", 10, "bold"), bg="#EF4444", fg="white",
                               cursor="hand2", relief="flat", padx=10, pady=3, command=self.handle_logout)
        btn_logout.pack(side="left")

        btn_exit_app = tk.Button(right_box, text="Thoát", font=("Times New Roman", 10, "bold"), bg="#475569", fg="white",
                                 cursor="hand2", relief="flat", padx=10, pady=3, command=self.root.destroy)
        btn_exit_app.pack(side="left", padx=(6, 0))

    # Khởi tạo thanh menu hệ thống (Hệ thống, Trợ giúp, Giới thiệu tác giả)
    def create_menu(self):
        menubar = tk.Menu(self.root)

        # Menu Hệ thống
        m_system = tk.Menu(menubar, tearoff=0)
        m_system.add_command(label="Đăng xuất", command=self.handle_logout)
        m_system.add_separator()
        m_system.add_command(label="Khởi tạo lại CSDL mẫu", command=self.reset_db)
        m_system.add_separator()
        m_system.add_command(label="Thoát", command=self.root.quit)
        menubar.add_cascade(label="Hệ thống", menu=m_system)

        # Menu Trợ giúp
        m_help = tk.Menu(menubar, tearoff=0)
        m_help.add_command(label="Thông tin đồ án", command=self.show_about)
        m_help.add_command(label="Hướng dẫn sử dụng", command=self.show_user_guide)
        menubar.add_cascade(label="Trợ giúp", menu=m_help)

        self.root.config(menu=menubar)

    # Xử lý đăng xuất: đóng phiên làm việc hiện tại và quay về màn hình đăng nhập
    def handle_logout(self):
        if messagebox.askyesno("Đăng xuất", "Bạn có chắc chắn muốn đăng xuất khỏi hệ thống?"):
            self.root.destroy()
            login_root = tk.Tk()
            LoginWindow(login_root)
            login_root.mainloop()

    # Khởi tạo lại CSDL về trạng thái ban đầu khi cần đặt lại dữ liệu mẫu
    def reset_db(self):
        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn nạp lại dữ liệu mẫu của hệ thống?"):
            init_database(force=True)
            messagebox.showinfo("Thành công", "Đã khởi tạo và đồng bộ CSDL thành công!")

    # Hiển thị thông tin đồ án, sinh viên thực hiện và giảng viên hướng dẫn
    def show_about(self):
        about_win = tk.Toplevel(self.root)
        about_win.title("THÔNG TIN ĐỒ ÁN")
        center_window(about_win, 450, 300)
        about_win.config(bg="#FFFFFF")
        about_win.resizable(False, False)

        tk.Label(about_win, text="ĐỒ ÁN CHUYÊN ĐỀ PYTHON", font=("Times New Roman", 15, "bold"), fg="#0D9488", bg="#FFFFFF").pack(pady=(15, 5))
        tk.Label(about_win, text="ĐỀ TÀI: XÂY DỰNG ỨNG DỤNG QUẢN LÝ BỆNH NHÂN\nVỚI PYTHON, TKINTER VÀ MYSQL",
                 font=("Times New Roman", 12, "bold"), fg="#1E293B", bg="#FFFFFF", justify="center").pack(pady=5)

        info = (
            "--------------------------------------------------\n"
            "Giảng viên hướng dẫn: Ths. Nguyễn Ngọc Minh\n"
            "Khoa: Công nghệ Thông tin - Trường Đại học An Giang\n"
            "Mã học phần: COS525 (Chuyên đề Python)\n"
            "Sinh viên thực hiện:\n"
            "Văng Thành Phát - DTH245849\n"
            "Lê Minh Triết -  DTH245928\n"

            "--------------------------------------------------"
        )
        tk.Label(about_win, text=info, font=("Times New Roman", 11), fg="#475569", bg="#FFFFFF", justify="left").pack(pady=10)
        tk.Button(about_win, text="Đóng", bg="#0D9488", fg="white", font=("Times New Roman", 11), width=10,
                  command=about_win.destroy).pack(pady=5)

    # Mở bảng tóm tắt hướng dẫn sử dụng các chức năng của phần mềm
    def show_user_guide(self):
        guide = (
            "HƯỚNG DẪN SỬ DỤNG NHANH:\n\n"
            "1. Tab Hồ sơ: Đăng ký, sửa, xóa, tìm kiếm bệnh nhân và phân luồng Khám nội / Khám ngoại.\n"
            "2. Tab Khám Nội Khoa: Tiếp nhận khám lâm sàng và kê đơn cho bệnh nhân khám nội.\n"
            "3. Tab Khám Ngoại Khoa: Tiếp nhận khám lâm sàng và kê đơn cho bệnh nhân khám ngoại.\n"
            "4. Tab Kho Dược: Quản lý danh mục thuốc, cập nhật giá, số lượng tồn kho và hạn sử dụng.\n"
            "5. Tab Viện phí: Tự động tổng hợp chi phí khám và thuốc, giảm trừ BHYT và in hóa đơn viện phí.\n"
            "6. Tab Thống kê: Xem các chỉ số tổng quan, biểu đồ doanh thu theo ngày và xuất báo cáo Excel."
        )
        messagebox.showinfo("Hướng dẫn sử dụng", guide)

    # Khởi tạo thanh điều hướng các Tab và phân quyền hiển thị theo vai trò người dùng
    def create_tabs(self):
        self.tab_control = ttk.Notebook(self.root)

        tab_patient = tk.Frame(self.tab_control, bg="#F8FAFC")
        tab_exam_noi = tk.Frame(self.tab_control, bg="#F8FAFC")
        tab_exam_ngoai = tk.Frame(self.tab_control, bg="#F8FAFC")
        tab_pharmacy = tk.Frame(self.tab_control, bg="#F8FAFC")
        tab_billing = tk.Frame(self.tab_control, bg="#F8FAFC")
        tab_report = tk.Frame(self.tab_control, bg="#F8FAFC")

        vaitro = self.current_user["vaitro"]

        # Phân quyền hiển thị Tab chuẩn mực theo từng vai trò nghiệp vụ:
        if vaitro == "Admin":
            self.tab_control.add(tab_patient, text="  📋 Hồ Sơ Bệnh Nhân  ")
            self.tab_control.add(tab_exam_noi, text="  🩺 Khám Nội Khoa  ")
            self.tab_control.add(tab_exam_ngoai, text="  🩹 Khám Ngoại Khoa  ")
            self.tab_control.add(tab_pharmacy, text="  💊 Kho Dược Phẩm  ")
            self.tab_control.add(tab_billing, text="  💳 Viện Phí & Hóa Đơn  ")
            self.tab_control.add(tab_report, text="  📊 Báo Cáo Thống Kê  ")

            self.build_tab_patient(tab_patient)
            self.exam_handler_noi = ExamTabHandler(self, tab_exam_noi, loai_kham="Khám nội")
            self.exam_handler_ngoai = ExamTabHandler(self, tab_exam_ngoai, loai_kham="Khám ngoại")
            self.build_tab_pharmacy(tab_pharmacy)
            self.build_tab_billing(tab_billing)
            self.build_tab_report(tab_report)

        elif vaitro == "Bác sĩ":
            # Bác sĩ: Khám bệnh, kê đơn và tra cứu tiền sử bệnh nhân + kho dược
            self.tab_control.add(tab_patient, text="  📋 Hồ Sơ Bệnh Nhân  ")
            self.tab_control.add(tab_exam_noi, text="  🩺 Khám Nội Khoa  ")
            self.tab_control.add(tab_exam_ngoai, text="  🩹 Khám Ngoại Khoa  ")
            self.tab_control.add(tab_pharmacy, text="  💊 Tra Cứu Kho Dược  ")

            self.build_tab_patient(tab_patient)
            self.exam_handler_noi = ExamTabHandler(self, tab_exam_noi, loai_kham="Khám nội")
            self.exam_handler_ngoai = ExamTabHandler(self, tab_exam_ngoai, loai_kham="Khám ngoại")
            self.build_tab_pharmacy(tab_pharmacy)

        elif vaitro == "Tiếp tân":
            # Tiếp tân: Chuyên trách bàn tiếp đón, đăng ký hồ sơ và cấp mã BN mới
            self.tab_control.add(tab_patient, text="  📋 Tiếp Nhận Hồ Sơ Bệnh Nhân  ")
            self.build_tab_patient(tab_patient)

        elif vaitro == "Thu ngân":
            # Thu ngân: Chuyên trách quầy thanh toán, áp dụng BHYT và xuất hóa đơn
            self.tab_control.add(tab_billing, text="  💳 Thu Viện Phí & Hóa Đơn  ")
            self.build_tab_billing(tab_billing)

        elif vaitro == "Dược sĩ":
            # Dược sĩ: Quản lý kho dược phẩm, kiểm kê tồn kho và cập nhật giá
            self.tab_control.add(tab_pharmacy, text="  💊 Quản Lý Kho Dược  ")
            self.build_tab_pharmacy(tab_pharmacy)

        else: # Dự phòng nếu có vai trò khác
            self.tab_control.add(tab_patient, text="  📋 Tiếp Nhận Bệnh Nhân  ")
            self.build_tab_patient(tab_patient)

        # Lắng nghe sự kiện chuyển Tab để tự động làm mới dữ liệu liên Tab
        self.tab_control.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        self.tab_control.pack(fill="both", expand=True, padx=10, pady=5)

    # Tự động tải lại dữ liệu mới nhất từ CSDL khi người dùng chuyển giữa các Tab
    def on_tab_changed(self, event):
        """Tự động làm mới dữ liệu khi người dùng chuyển giữa các Tab"""
        try:
            selected_tab = self.tab_control.select()
            tab_text = self.tab_control.tab(selected_tab, "text")
            if "Khám Nội" in tab_text:
                if hasattr(self, 'exam_handler_noi'):
                    self.exam_handler_noi.load_comboboxes()
                    self.exam_handler_noi.load_history()
            elif "Khám Ngoại" in tab_text:
                if hasattr(self, 'exam_handler_ngoai'):
                    self.exam_handler_ngoai.load_comboboxes()
                    self.exam_handler_ngoai.load_history()
            elif "Khám Bệnh" in tab_text:
                if hasattr(self, 'ex_load_comboboxes'):
                    self.ex_load_comboboxes()
                if hasattr(self, 'ex_load_history'):
                    self.ex_load_history()
            elif "Viện Phí" in tab_text or "Thu Viện Phí" in tab_text:
                if hasattr(self, 'bill_load_queue'):
                    self.bill_load_queue()
            elif "Kho Dược" in tab_text or "Tra Cứu Kho Dược" in tab_text:
                if hasattr(self, 'dr_load_data'):
                    self.dr_load_data()
            elif "Hồ Sơ" in tab_text or "Tiếp Nhận" in tab_text:
                if hasattr(self, 'p_load_data'):
                    self.p_load_data()
            elif "Báo Cáo" in tab_text:
                if hasattr(self, 'rep_update_kpis'):
                    self.rep_update_kpis()
        except Exception:
            pass

    # ==========================================================================
    # TAB 1: QUẢN LÝ BỆNH NHÂN (CRUD + EXCEL + SEARCH)
    # ==========================================================================
    def build_tab_patient(self, parent):
        # Frame trên: Form nhập thông tin bệnh nhân
        frame_top = tk.LabelFrame(parent, text=" Thông tin chi tiết Bệnh nhân ", font=("Times New Roman", 12, "bold"),
                                  fg="#0F766E", bg="#FFFFFF", padx=15, pady=10)
        frame_top.pack(fill="x", padx=10, pady=5)

        # Biến giao diện
        self.p_mabn = tk.StringVar()
        self.p_holot = tk.StringVar()
        self.p_ten = tk.StringVar()
        self.p_phai = tk.StringVar(value="Nam")
        self.p_cccd = tk.StringVar()
        self.p_sdt = tk.StringVar()
        self.p_diachi = tk.StringVar()
        self.p_bhyt = tk.StringVar()
        self.p_nhommau = tk.StringVar(value="O")
        self.p_tiensu = tk.StringVar()
        self.p_loaikham = tk.StringVar(value="Khám nội") ###############

        # Cấu hình tỷ lệ các cột để form luôn cân đối và tự động co giãn theo kích thước cửa sổ
        frame_top.grid_columnconfigure(1, weight=2)
        frame_top.grid_columnconfigure(3, weight=3)
        frame_top.grid_columnconfigure(5, weight=2)
        frame_top.grid_columnconfigure(7, weight=2)

        # Dòng 0: Mã BN, Họ lót, Tên, Giới tính
        tk.Label(frame_top, text="Mã BN (*):", font=("Times New Roman", 11, "bold"), bg="#FFFFFF").grid(row=0, column=0, sticky="w", pady=5)
        entry_mabn = tk.Entry(frame_top, textvariable=self.p_mabn, font=("Times New Roman", 11), width=14, bg="#F8FAFC", relief="solid", bd=1)
        entry_mabn.grid(row=0, column=1, sticky="we", padx=(5, 15), pady=5, ipady=4)

        tk.Label(frame_top, text="Họ & Tên lót (*):", font=("Times New Roman", 11, "bold"), bg="#FFFFFF").grid(row=0, column=2, sticky="w", pady=5)
        tk.Entry(frame_top, textvariable=self.p_holot, font=("Times New Roman", 11), width=22, relief="solid", bd=1).grid(row=0, column=3, sticky="we", padx=(5, 15), pady=5, ipady=4)

        tk.Label(frame_top, text="Tên (*):", font=("Times New Roman", 11, "bold"), bg="#FFFFFF").grid(row=0, column=4, sticky="w", pady=5)
        tk.Entry(frame_top, textvariable=self.p_ten, font=("Times New Roman", 11), width=14, relief="solid", bd=1).grid(row=0, column=5, sticky="we", padx=(5, 15), pady=5, ipady=4)

        tk.Label(frame_top, text="Giới tính:", font=("Times New Roman", 11, "bold"), bg="#FFFFFF").grid(row=0, column=6, sticky="w", pady=5)
        f_gender = tk.Frame(frame_top, bg="#FFFFFF")
        f_gender.grid(row=0, column=7, sticky="w", padx=5, pady=5)
        tk.Radiobutton(f_gender, text="Nam", variable=self.p_phai, value="Nam", bg="#FFFFFF").pack(side="left")
        tk.Radiobutton(f_gender, text="Nữ", variable=self.p_phai, value="Nữ", bg="#FFFFFF").pack(side="left", padx=(10, 0))

        # Dòng 1: Ngày sinh, CCCD, Số điện thoại, Nhóm máu
        tk.Label(frame_top, text="Ngày sinh (*):", font=("Times New Roman", 11, "bold"), bg="#FFFFFF").grid(row=1, column=0, sticky="w", pady=5)
        self.p_date_entry = DateEntry(frame_top, background="#0D9488", foreground="white",
                                      date_pattern="yyyy-mm-dd", font=("Times New Roman", 10))
        self.p_date_entry.grid(row=1, column=1, sticky="we", padx=(5, 15), pady=5, ipady=3)

        tk.Label(frame_top, text="CCCD / CMND:", font=("Times New Roman", 11, "bold"), bg="#FFFFFF").grid(row=1, column=2, sticky="w", pady=5)
        tk.Entry(frame_top, textvariable=self.p_cccd, font=("Times New Roman", 11), width=18, relief="solid", bd=1).grid(row=1, column=3, sticky="we", padx=(5, 15), pady=5, ipady=4)

        tk.Label(frame_top, text="Số ĐT (*):", font=("Times New Roman", 11, "bold"), bg="#FFFFFF").grid(row=1, column=4, sticky="w", pady=5)
        tk.Entry(frame_top, textvariable=self.p_sdt, font=("Times New Roman", 11), width=16, relief="solid", bd=1).grid(row=1, column=5, sticky="we", padx=(5, 15), pady=5, ipady=4)

        tk.Label(frame_top, text="Nhóm máu:", font=("Times New Roman", 11, "bold"), bg="#FFFFFF").grid(row=1, column=6, sticky="w", pady=5)
        cbb_blood = ttk.Combobox(frame_top, textvariable=self.p_nhommau, values=["A", "B", "AB", "O"], state="readonly")
        cbb_blood.grid(row=1, column=7, sticky="we", padx=5, pady=5, ipady=2)

        # Dòng 2: Mã BHYT, Phân loại khám và Địa chỉ cư trú
        tk.Label(frame_top, text="Số thẻ BHYT:", font=("Times New Roman", 11, "bold"), bg="#FFFFFF").grid(row=2, column=0, sticky="w", pady=5)
        tk.Entry(frame_top, textvariable=self.p_bhyt, font=("Times New Roman", 11), width=18, relief="solid", bd=1).grid(row=2, column=1, sticky="we", padx=(5, 15), pady=5, ipady=4)

        tk.Label(frame_top, text="Loại khám (*):", font=("Times New Roman", 11, "bold"), bg="#FFFFFF").grid(row=2, column=2, sticky="w", pady=5)
        self.cbb_p_loaikham = ttk.Combobox(frame_top, textvariable=self.p_loaikham, values=["Khám nội", "Khám ngoại"], state="readonly", font=("Times New Roman", 10))
        self.cbb_p_loaikham.grid(row=2, column=3, sticky="we", padx=(5, 15), pady=5, ipady=3)

        tk.Label(frame_top, text="Địa chỉ:", font=("Times New Roman", 11, "bold"), bg="#FFFFFF").grid(row=2, column=4, sticky="w", pady=5)
        tk.Entry(frame_top, textvariable=self.p_diachi, font=("Times New Roman", 11), width=30, relief="solid", bd=1).grid(row=2, column=5, columnspan=3, sticky="we", padx=5, pady=5, ipady=4)

        # Dòng 3: Tiền sử bệnh & Dị ứng thuốc (kéo dài toàn bộ dòng)
        tk.Label(frame_top, text="Tiền sử bệnh:", font=("Times New Roman", 11, "bold"), bg="#FFFFFF").grid(row=3, column=0, sticky="w", pady=5)
        tk.Entry(frame_top, textvariable=self.p_tiensu, font=("Times New Roman", 11), width=50, relief="solid", bd=1).grid(row=3, column=1, columnspan=7, sticky="we", padx=5, pady=5, ipady=4)

        # Dòng 4: Thanh nút bấm chức năng CRUD
        f_btn = tk.Frame(frame_top, bg="#FFFFFF")
        f_btn.grid(row=4, column=0, columnspan=8, pady=(12, 2), sticky="we")

        btn_them = tk.Button(f_btn, text="➕ Thêm mới", font=("Times New Roman", 11, "bold"), bg="#10B981", fg="white",
                             width=11, relief="flat", cursor="hand2", command=self.p_action_add)
        btn_them.pack(side="left", padx=4)

        btn_luu = tk.Button(f_btn, text="💾 Lưu", font=("Times New Roman", 11, "bold"), bg="#0284C7", fg="white",
                            width=10, relief="flat", cursor="hand2", command=self.p_action_save)
        btn_luu.pack(side="left", padx=4)

        btn_sua = tk.Button(f_btn, text="✏️ Sửa", font=("Times New Roman", 11, "bold"), bg="#F59E0B", fg="white",
                            width=10, relief="flat", cursor="hand2", command=self.p_action_save)
        btn_sua.pack(side="left", padx=4)

        btn_xoa = tk.Button(f_btn, text="🗑️ Xóa", font=("Times New Roman", 11, "bold"), bg="#EF4444", fg="white",
                            width=10, relief="flat", cursor="hand2", command=self.p_action_delete)
        btn_xoa.pack(side="left", padx=4)

        btn_huy = tk.Button(f_btn, text="🔄 Làm mới", font=("Times New Roman", 11, "bold"), bg="#64748B", fg="white",
                            width=10, relief="flat", cursor="hand2", command=self.p_action_clear)
        btn_huy.pack(side="left", padx=4)

        btn_excel = tk.Button(f_btn, text="📊 Xuất Excel", font=("Times New Roman", 11, "bold"), bg="#059669", fg="white",
                              width=12, relief="flat", cursor="hand2", command=self.p_export_excel)
        btn_excel.pack(side="right", padx=4)

        # Frame giữa: Tìm kiếm
        frame_search = tk.Frame(parent, bg="#F1F5F9", padx=10, pady=5)
        frame_search.pack(fill="x", padx=10, pady=2)

        tk.Label(frame_search, text="🔍 Tìm kiếm bệnh nhân:", font=("Times New Roman", 11, "bold"), bg="#F1F5F9", fg="#334155").pack(side="left", padx=5)
        self.p_search_var = tk.StringVar()
        entry_search = tk.Entry(frame_search, textvariable=self.p_search_var, font=("Times New Roman", 11), width=32, relief="solid", bd=1)
        entry_search.pack(side="left", padx=5, ipady=4)
        entry_search.bind("<Return>", lambda e: self.p_search_data())

        btn_search = tk.Button(frame_search, text="Tìm kiếm", font=("Times New Roman", 10, "bold"), bg="#0D9488", fg="white",
                               relief="flat", cursor="hand2", command=self.p_search_data)
        btn_search.pack(side="left", padx=4)

        btn_all = tk.Button(frame_search, text="Tất cả", font=("Times New Roman", 10), bg="#CBD5E1", fg="#1E293B",
                            relief="flat", cursor="hand2", command=self.p_load_data)
        btn_all.pack(side="left", padx=4)

        # Frame dưới: Bảng Treeview danh sách bệnh nhân
        frame_tree = tk.Frame(parent, bg="#FFFFFF")
        frame_tree.pack(fill="both", expand=True, padx=10, pady=(2, 8))

        columns = ("mabn", "hoten", "phai", "ngaysinh", "loaikham", "sdt", "cccd", "bhyt", "nhommau", "diachi", "tiensu")
        self.p_tree = ttk.Treeview(frame_tree, columns=columns, show="headings", selectmode="browse")

        headers = {
            "mabn": ("Mã BN", 75, "center"),
            "hoten": ("Họ và Tên", 150, "w"),
            "phai": ("Phái", 55, "center"),
            "ngaysinh": ("Ngày sinh", 90, "center"),
            "loaikham": ("Loại khám", 95, "center"),
            "sdt": ("Số ĐT", 100, "center"),
            "cccd": ("CCCD/CMND", 110, "center"),
            "bhyt": ("Số BHYT", 120, "center"),
            "nhommau": ("Nhóm máu", 75, "center"),
            "diachi": ("Địa chỉ", 210, "w"),
            "tiensu": ("Tiền sử bệnh", 140, "w")
        }
        for col, (text, w, align) in headers.items():
            self.p_tree.heading(col, text=text)
            self.p_tree.column(col, width=w, anchor=align)

        # Thanh cuộn dọc & ngang
        scroll_y = ttk.Scrollbar(frame_tree, orient="vertical", command=self.p_tree.yview)
        scroll_x = ttk.Scrollbar(frame_tree, orient="horizontal", command=self.p_tree.xview)
        self.p_tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.p_tree.pack(fill="both", expand=True)

        # Bắt sự kiện click vào dòng bảng
        self.p_tree.bind("<<TreeviewSelect>>", self.p_on_select_row)

        # Nạp dữ liệu ban đầu
        self.p_load_data()

    # Tải danh sách bệnh nhân từ CSDL MySQL lên bảng hiển thị Treeview
    def p_load_data(self, query=None, params=()):
        for row in self.p_tree.get_children():
            self.p_tree.delete(row)
        conn = get_connection()
        if not conn:
            return
        try:
            cur = conn.cursor()
            if query:
                cur.execute(query, params)
            else:
                cur.execute("SELECT mabn, holot, ten, phai, ngaysinh, sdt, cccd, bhyt, nhommau, diachi, tiensubenh, loaikham FROM benhnhan ORDER BY mabn DESC")
            rows = cur.fetchall()
            for r in rows:
                hoten = f"{r[1]} {r[2]}"
                ns = r[4].strftime("%Y-%m-%d") if r[4] else ""
                loaikham = r[11] if len(r) > 11 and r[11] else "Khám nội"
                self.p_tree.insert("", "end", values=(r[0], hoten, r[3], ns, loaikham, r[5], r[6], r[7], r[8], r[9], r[10]))
            conn.close()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi tải danh sách bệnh nhân:\n{e}")

    # Xử lý sự kiện click chọn một dòng bệnh nhân: đổ thông tin lên form để xem/sửa
    def p_on_select_row(self, event):
        sel = self.p_tree.selection()
        if not sel:
            return
        vals = self.p_tree.item(sel[0])["values"]
        mabn = vals[0]
        # Truy vấn lại chi tiết từ DB
        conn = get_connection()
        if not conn:
            return
        cur = conn.cursor()
        cur.execute("SELECT mabn, holot, ten, phai, ngaysinh, cccd, sdt, diachi, bhyt, nhommau, tiensubenh, loaikham FROM benhnhan WHERE mabn=%s", (mabn,))
        data = cur.fetchone()
        conn.close()
        if data:
            self.p_mabn.set(data[0])
            self.p_holot.set(data[1])
            self.p_ten.set(data[2])
            self.p_phai.set(data[3])
            try:
                self.p_date_entry.set_date(data[4])
            except Exception:
                pass
            self.p_cccd.set(data[5] or "")
            self.p_sdt.set(data[6] or "")
            self.p_diachi.set(data[7] or "")
            self.p_bhyt.set(data[8] or "")
            self.p_nhommau.set(data[9] or "O")
            self.p_tiensu.set(data[10] or "")
            self.p_loaikham.set(data[11] or "Khám nội")

    # Tự động sinh mã bệnh nhân mới dạng tự tăng (BNxxx) và chuẩn bị thêm mới
    def p_action_add(self):
        self.p_action_clear()
        # Tự động sinh mã BN tiếp theo
        conn = get_connection()
        if conn:
            cur = conn.cursor()
            cur.execute("SELECT mabn FROM benhnhan WHERE mabn LIKE 'BN%' ORDER BY LENGTH(mabn) DESC, mabn DESC LIMIT 1")
            row = cur.fetchone()
            conn.close()
            if row and row[0].startswith("BN"):
                try:
                    num = int(row[0][2:]) + 1
                    self.p_mabn.set(f"BN{num:03d}")
                except Exception:
                    self.p_mabn.set("BN001")
            else:
                self.p_mabn.set("BN001")

    # Xóa trắng form nhập liệu thông tin bệnh nhân
    def p_action_clear(self):
        self.p_mabn.set("")
        self.p_holot.set("")
        self.p_ten.set("")
        self.p_phai.set("Nam")
        self.p_cccd.set("")
        self.p_sdt.set("")
        self.p_diachi.set("")
        self.p_bhyt.set("")
        self.p_nhommau.set("O")
        self.p_tiensu.set("")
        self.p_loaikham.set("Khám nội")
        self.p_search_var.set("")
        try:
            self.p_date_entry.set_date(datetime.date(1990, 1, 1))
        except Exception:
            pass

    # Kiểm tra dữ liệu hợp lệ và Lưu thông tin bệnh nhân (Thêm mới INSERT hoặc Cập nhật UPDATE)
    def p_action_save(self):
        mabn = self.p_mabn.get().strip()
        holot = self.p_holot.get().strip()
        ten = self.p_ten.get().strip()
        phai = self.p_phai.get().strip()
        ngaysinh = self.p_date_entry.get().strip()
        cccd = self.p_cccd.get().strip()
        sdt = self.p_sdt.get().strip()
        diachi = self.p_diachi.get().strip()
        bhyt = self.p_bhyt.get().strip()
        nhommau = self.p_nhommau.get().strip()
        tiensu = self.p_tiensu.get().strip()
        loaikham = self.p_loaikham.get().strip() or "Khám nội"

        if not mabn or not holot or not ten or not sdt:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập các thông tin bắt buộc: Mã BN, Họ lót, Tên, Số ĐT!")
            return

        conn = get_connection()
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute("SELECT mabn FROM benhnhan WHERE mabn=%s", (mabn,))
            exists = cur.fetchone()
            if exists:
                cur.execute("""
                    UPDATE benhnhan
                    SET holot=%s, ten=%s, phai=%s, ngaysinh=%s, cccd=%s, sdt=%s, diachi=%s, bhyt=%s, nhommau=%s, tiensubenh=%s, loaikham=%s
                    WHERE mabn=%s
                """, (holot, ten, phai, ngaysinh, cccd, sdt, diachi, bhyt, nhommau, tiensu, loaikham, mabn))
                messagebox.showinfo("Thành công", f"Đã cập nhật thông tin bệnh nhân {mabn}!")
            else:
                cur.execute("""
                    INSERT INTO benhnhan (mabn, holot, ten, phai, ngaysinh, cccd, sdt, diachi, bhyt, nhommau, tiensubenh, loaikham)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (mabn, holot, ten, phai, ngaysinh, cccd, sdt, diachi, bhyt, nhommau, tiensu, loaikham))
                messagebox.showinfo("Thành công", f"Đã thêm mới bệnh nhân {mabn} thành công!")
            conn.commit()
            conn.close()
            self.p_load_data()
            if hasattr(self, 'ex_load_comboboxes'):
                self.ex_load_comboboxes()
        except Exception as e:
            messagebox.showerror("Lỗi CSDL", f"Lỗi khi lưu bệnh nhân:\n{e}")

    # Xóa hồ sơ bệnh nhân được chọn khỏi CSDL sau khi người dùng xác nhận
    def p_action_delete(self):
        mabn = self.p_mabn.get().strip()
        if not mabn:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn bệnh nhân cần xóa!")
            return
        if messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc chắn muốn xóa hồ sơ bệnh nhân [{mabn}] cùng toàn bộ lịch sử khám liên quan?"):
            conn = get_connection()
            if not conn:
                return
            try:
                cur = conn.cursor()
                cur.execute("DELETE FROM benhnhan WHERE mabn=%s", (mabn,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Thành công", f"Đã xóa thành công bệnh nhân {mabn}!")
                self.p_action_clear()
                self.p_load_data()
                if hasattr(self, 'ex_load_comboboxes'):
                    self.ex_load_comboboxes()
            except Exception as e:
                messagebox.showerror("Lỗi CSDL", f"Lỗi khi xóa bệnh nhân:\n{e}")

    # Tìm kiếm bệnh nhân theo từ khóa (Mã BN, Họ tên, SĐT, CCCD, BHYT)
    def p_search_data(self):
        keyword = self.p_search_var.get().strip()
        if not keyword:
            self.p_load_data()
            return
        sql = """
            SELECT mabn, holot, ten, phai, ngaysinh, sdt, cccd, bhyt, nhommau, diachi, tiensubenh, loaikham
            FROM benhnhan
            WHERE mabn LIKE %s OR holot LIKE %s OR ten LIKE %s OR sdt LIKE %s OR cccd LIKE %s OR loaikham LIKE %s
            ORDER BY mabn DESC
        """
        kw = f"%{keyword}%"
        self.p_load_data(sql, (kw, kw, kw, kw, kw, kw))

    # Xuất toàn bộ danh sách bệnh nhân ra file Excel (.xlsx) có định dạng bảng chuẩn
    def p_export_excel(self):
        conn = get_connection()
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute("SELECT mabn, holot, ten, phai, ngaysinh, sdt, cccd, bhyt, nhommau, diachi, tiensubenh, loaikham FROM benhnhan")
            rows = cur.fetchall()
            conn.close()

            if not rows:
                messagebox.showwarning("Thông báo", "Không có dữ liệu bệnh nhân để xuất!")
                return

            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "DanhSachBenhNhan"

            headers = ["STT", "Mã BN", "Họ & Tên lót", "Tên", "Giới tính", "Ngày sinh", "Loại khám", "Số ĐT", "CCCD/CMND", "Số BHYT", "Nhóm máu", "Địa chỉ"]
            ws.append(headers)

            # Style header bảng
            header_fill = PatternFill(start_color="0D9488", end_color="0D9488", fill_type="solid")
            thin_border = Border(
                left=Side(style='thin', color='A0AEC0'), right=Side(style='thin', color='A0AEC0'),
                top=Side(style='thin', color='A0AEC0'), bottom=Side(style='thin', color='A0AEC0')
            )

            for col_num in range(1, len(headers) + 1):
                cell = ws.cell(row=1, column=col_num)
                cell.font = Font(name="Times New Roman", size=12, bold=True, color="FFFFFF")
                cell.fill = header_fill
                cell.alignment = Alignment(horizontal="center", vertical="center")
                cell.border = thin_border

            # Điền dữ liệu
            for idx, r in enumerate(rows, 1):
                if r[4] and hasattr(r[4], 'strftime'):
                    ns = r[4].strftime("%d/%m/%Y")
                else:
                    ns = str(r[4] or "")
                loaikham = r[11] if len(r) > 11 and r[11] else "Khám nội"
                row_val = [idx, r[0], r[1], r[2], r[3], ns, loaikham, r[5], r[6], r[7], r[8], r[9]]
                ws.append(row_val)
                current_row = idx + 1
                for col_num in range(1, len(headers) + 1):
                    c = ws.cell(row=current_row, column=col_num)
                    c.font = Font(name="Times New Roman", size=11)
                    c.border = thin_border
                    if col_num in [1, 2, 5, 6, 7, 8, 9, 10, 11]:
                        c.alignment = Alignment(horizontal="center")

            # Tự động canh độ rộng cột
            for col_idx, col in enumerate(ws.columns, 1):
                col_letter = get_column_letter(col_idx)
                max_len = 0
                for cell in col:
                    val = str(cell.value or '')
                    if len(val) > max_len:
                        max_len = len(val)
                ws.column_dimensions[col_letter].width = max(max_len + 4, 12)

            file_path = filedialog.asksaveasfilename(
                parent=self.root,
                defaultextension=".xlsx",
                filetypes=[("Excel Files (*.xlsx)", "*.xlsx"), ("All Files (*.*)", "*.*")],
                initialfile=f"DanhSachBenhNhan_{datetime.date.today().strftime('%Y%m%d')}.xlsx"
            )
            if file_path:
                try:
                    wb.save(file_path)
                except PermissionError:
                    messagebox.showerror("Lỗi ghi file", f"Không thể lưu file vì file này đang được mở trong Excel!\n\nVui lòng đóng file Excel '{os.path.basename(file_path)}' rồi bấm Xuất Excel lại.", parent=self.root)
                    return
                if messagebox.askyesno("Thành công", f"Đã xuất dữ liệu Excel thành công:\n{file_path}\n\nBạn có muốn mở file này ngay bây giờ không?", parent=self.root):
                    try:
                        os.startfile(file_path)
                    except Exception:
                        pass
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xuất file Excel:\n{e}", parent=self.root)

    # ==========================================================================
    # PHÂN HỆ KHÁM BỆNH & TOA THUỐC (ĐIỀU HƯỚNG TỚI EXAM TAB HANDLER)
    # ==========================================================================
    def build_tab_exam(self, parent, loai_kham="Khám nội"):
        """Dựng giao diện phân hệ khám bệnh (khám nội hoặc khám ngoại)"""
        handler = ExamTabHandler(self, parent, loai_kham=loai_kham)
        if loai_kham == "Khám nội":
            self.exam_handler_noi = handler
        else:
            self.exam_handler_ngoai = handler
        return handler

    def ex_load_comboboxes(self):
        """Làm mới dữ liệu combobox cho cả 2 phân hệ Khám nội và Khám ngoại"""
        if hasattr(self, 'exam_handler_noi'):
            self.exam_handler_noi.load_comboboxes()
        if hasattr(self, 'exam_handler_ngoai'):
            self.exam_handler_ngoai.load_comboboxes()

    def ex_load_history(self):
        """Làm mới danh sách phiếu khám gần đây cho cả 2 phân hệ Khám nội và Khám ngoại"""
        if hasattr(self, 'exam_handler_noi'):
            self.exam_handler_noi.load_history()
        if hasattr(self, 'exam_handler_ngoai'):
            self.exam_handler_ngoai.load_history()

    # ==========================================================================
    # TAB 3: QUẢN LÝ KHO DƯỢC PHẨM (PHARMACY CRUD)
    # ==========================================================================
    def build_tab_pharmacy(self, parent):
        frame_top = tk.LabelFrame(parent, text=" Thông tin Dược phẩm / Thuốc ", font=("Times New Roman", 12, "bold"),
                                  fg="#0F766E", bg="#FFFFFF", padx=15, pady=10)
        frame_top.pack(fill="x", padx=10, pady=5)

        self.dr_mathuoc = tk.StringVar()
        self.dr_tenthuoc = tk.StringVar()
        self.dr_hoatchat = tk.StringVar()
        self.dr_donvitinh = tk.StringVar(value="Viên")
        self.dr_dongia = tk.StringVar(value="0")
        self.dr_soluong = tk.StringVar(value="100")
        self.dr_cachdung = tk.StringVar()

        # Dòng 0: Mã thuốc, Tên thuốc, Hoạt chất
        tk.Label(frame_top, text="Mã thuốc (*):", font=("Times New Roman", 11, "bold"), bg="#FFFFFF").grid(row=0, column=0, sticky="w", pady=4)
        tk.Entry(frame_top, textvariable=self.dr_mathuoc, font=("Times New Roman", 11), width=14, relief="solid", bd=1).grid(row=0, column=1, sticky="w", padx=5, ipady=4)

        tk.Label(frame_top, text="Tên biệt dược (*):", font=("Times New Roman", 11, "bold"), bg="#FFFFFF").grid(row=0, column=2, sticky="w", pady=4)
        tk.Entry(frame_top, textvariable=self.dr_tenthuoc, font=("Times New Roman", 11), width=24, relief="solid", bd=1).grid(row=0, column=3, sticky="w", padx=5, ipady=4)

        tk.Label(frame_top, text="Hoạt chất:", font=("Times New Roman", 11, "bold"), bg="#FFFFFF").grid(row=0, column=4, sticky="w", pady=4)
        tk.Entry(frame_top, textvariable=self.dr_hoatchat, font=("Times New Roman", 11), width=24, relief="solid", bd=1).grid(row=0, column=5, sticky="w", padx=5, ipady=4)

        # Dòng 1: Đơn vị tính, Đơn giá, Tồn kho, Hạn dùng
        tk.Label(frame_top, text="Đơn vị tính:", font=("Times New Roman", 11, "bold"), bg="#FFFFFF").grid(row=1, column=0, sticky="w", pady=4)
        ttk.Combobox(frame_top, textvariable=self.dr_donvitinh, values=["Viên", "Vỉ", "Hộp", "Chai", "Lọ", "Gói", "Ống"],
                     width=10, state="readonly").grid(row=1, column=1, sticky="w", padx=5, ipady=2)

        tk.Label(frame_top, text="Đơn giá bán (đ):", font=("Times New Roman", 11, "bold"), bg="#FFFFFF").grid(row=1, column=2, sticky="w", pady=4)
        tk.Entry(frame_top, textvariable=self.dr_dongia, font=("Times New Roman", 11), width=16, relief="solid", bd=1).grid(row=1, column=3, sticky="w", padx=5, ipady=4)

        tk.Label(frame_top, text="Số lượng tồn:", font=("Times New Roman", 11, "bold"), bg="#FFFFFF").grid(row=1, column=4, sticky="w", pady=4)
        tk.Entry(frame_top, textvariable=self.dr_soluong, font=("Times New Roman", 11), width=12, relief="solid", bd=1).grid(row=1, column=5, sticky="w", padx=5, ipady=4)

        # Dòng 2: Hạn sử dụng, Hướng dẫn sử dụng
        tk.Label(frame_top, text="Hạn sử dụng:", font=("Times New Roman", 11, "bold"), bg="#FFFFFF").grid(row=2, column=0, sticky="w", pady=4)
        self.dr_date_entry = DateEntry(frame_top, width=12, background="#0D9488", foreground="white",
                                       date_pattern="yyyy-mm-dd", font=("Times New Roman", 10))
        self.dr_date_entry.grid(row=2, column=1, sticky="w", padx=5, ipady=3)

        tk.Label(frame_top, text="Hướng dẫn chung:", font=("Times New Roman", 11, "bold"), bg="#FFFFFF").grid(row=2, column=2, sticky="w", pady=4)
        tk.Entry(frame_top, textvariable=self.dr_cachdung, font=("Times New Roman", 11), width=50, relief="solid", bd=1).grid(row=2, column=3, columnspan=3, sticky="we", padx=5, ipady=4)

        # Cụm nút thao tác
        f_btn = tk.Frame(frame_top, bg="#FFFFFF")
        f_btn.grid(row=3, column=0, columnspan=6, pady=(12, 0), sticky="we")

        tk.Button(f_btn, text="➕ Thêm thuốc", font=("Times New Roman", 11, "bold"), bg="#10B981", fg="white",
                  relief="flat", cursor="hand2", width=12, command=self.dr_action_add).pack(side="left", padx=4)
        tk.Button(f_btn, text="💾 Lưu", font=("Times New Roman", 11, "bold"), bg="#0284C7", fg="white",
                  relief="flat", cursor="hand2", width=10, command=self.dr_action_save).pack(side="left", padx=4)
        tk.Button(f_btn, text="✏️ Sửa", font=("Times New Roman", 11, "bold"), bg="#F59E0B", fg="white",
                  relief="flat", cursor="hand2", width=10, command=self.dr_action_save).pack(side="left", padx=4)
        tk.Button(f_btn, text="🗑️ Xóa", font=("Times New Roman", 11, "bold"), bg="#EF4444", fg="white",
                  relief="flat", cursor="hand2", width=10, command=self.dr_action_delete).pack(side="left", padx=4)
        tk.Button(f_btn, text="🔄 Làm mới", font=("Times New Roman", 11), bg="#64748B", fg="white",
                  relief="flat", cursor="hand2", width=10, command=self.dr_action_clear).pack(side="left", padx=4)
        tk.Button(f_btn, text="⚠️ Cảnh báo tồn kho ít", font=("Times New Roman", 11, "bold"), bg="#E11D48", fg="white",
                  relief="flat", cursor="hand2", command=self.dr_filter_low_stock).pack(side="right", padx=4)

        # Thanh tìm kiếm thuốc
        f_search = tk.Frame(parent, bg="#F1F5F9", padx=10, pady=5)
        f_search.pack(fill="x", padx=10, pady=2)

        tk.Label(f_search, text="🔍 Tìm tên thuốc / hoạt chất:", font=("Times New Roman", 11, "bold"), bg="#F1F5F9").pack(side="left", padx=5)
        self.dr_search_var = tk.StringVar()
        e_s = tk.Entry(f_search, textvariable=self.dr_search_var, font=("Times New Roman", 11), width=32, relief="solid", bd=1)
        e_s.pack(side="left", padx=5, ipady=4)
        e_s.bind("<Return>", lambda e: self.dr_search())

        tk.Button(f_search, text="Tìm kiếm", font=("Times New Roman", 10, "bold"), bg="#0D9488", fg="white",
                  relief="flat", cursor="hand2", command=self.dr_search).pack(side="left", padx=4)
        tk.Button(f_search, text="Xem tất cả", font=("Times New Roman", 10), bg="#CBD5E1",
                  relief="flat", cursor="hand2", command=self.dr_load_data).pack(side="left", padx=4)

        # Bảng danh mục thuốc
        f_tree = tk.Frame(parent, bg="#FFFFFF")
        f_tree.pack(fill="both", expand=True, padx=10, pady=(2, 8))

        cols = ("mathuoc", "tenthuoc", "hoatchat", "donvitinh", "dongia", "soluongton", "hansudung", "cachdung")
        self.dr_tree = ttk.Treeview(f_tree, columns=cols, show="headings")

        self.dr_tree.heading("mathuoc", text="Mã thuốc")
        self.dr_tree.heading("tenthuoc", text="Tên biệt dược")
        self.dr_tree.heading("hoatchat", text="Hoạt chất")
        self.dr_tree.heading("donvitinh", text="ĐVT")
        self.dr_tree.heading("dongia", text="Đơn giá (đ)")
        self.dr_tree.heading("soluongton", text="Tồn kho")
        self.dr_tree.heading("hansudung", text="Hạn dùng")
        self.dr_tree.heading("cachdung", text="Hướng dẫn sử dụng")

        self.dr_tree.column("mathuoc", width=70, anchor="center")
        self.dr_tree.column("tenthuoc", width=160)
        self.dr_tree.column("hoatchat", width=160)
        self.dr_tree.column("donvitinh", width=65, anchor="center")
        self.dr_tree.column("dongia", width=95, anchor="e")
        self.dr_tree.column("soluongton", width=75, anchor="center")
        self.dr_tree.column("hansudung", width=100, anchor="center")
        self.dr_tree.column("cachdung", width=220)

        s_y = ttk.Scrollbar(f_tree, orient="vertical", command=self.dr_tree.yview)
        self.dr_tree.configure(yscrollcommand=s_y.set)
        s_y.pack(side="right", fill="y")
        self.dr_tree.pack(fill="both", expand=True)

        self.dr_tree.bind("<<TreeviewSelect>>", self.dr_on_select_row)
        self.dr_load_data()

    # Tải danh sách thuốc từ kho lên bảng hiển thị, tô màu cảnh báo nếu thuốc sắp hết
    def dr_load_data(self, query=None, params=()):
        for r in self.dr_tree.get_children():
            self.dr_tree.delete(r)
        conn = get_connection()
        if not conn:
            return
        cur = conn.cursor()
        if query:
            cur.execute(query, params)
        else:
            cur.execute("SELECT mathuoc, tenthuoc, hoatchat, donvitinh, dongia, soluongton, hansudung, cachdung FROM thuoc ORDER BY mathuoc ASC")
        
        self.dr_tree.tag_configure("low_stock", background="#FFF1F2", foreground="#BE123C")
        for r in cur.fetchall():
            hsd = r[6].strftime("%Y-%m-%d") if r[6] and hasattr(r[6], 'strftime') else str(r[6] or "")
            tags = ()
            if r[5] is not None and int(r[5]) <= 100:
                tags = ("low_stock",)
            self.dr_tree.insert("", "end", values=(r[0], r[1], r[2], r[3], f"{int(r[4]):,}đ", r[5], hsd, r[7]), tags=tags)
        conn.close()

    # Click chọn một loại thuốc trên bảng để đưa thông tin lên form chỉnh sửa
    def dr_on_select_row(self, event):
        sel = self.dr_tree.selection()
        if not sel:
            return
        mathuoc = self.dr_tree.item(sel[0])["values"][0]
        conn = get_connection()
        if not conn:
            return
        cur = conn.cursor()
        cur.execute("""
            SELECT mathuoc, tenthuoc, hoatchat, donvitinh, dongia, soluongton, cachdung, hansudung
            FROM thuoc WHERE mathuoc=%s
        """, (mathuoc,))
        d = cur.fetchone()
        conn.close()
        if d:
            self.dr_mathuoc.set(d[0])
            self.dr_tenthuoc.set(d[1])
            self.dr_hoatchat.set(d[2] or "")
            self.dr_donvitinh.set(d[3])
            self.dr_dongia.set(str(int(d[4])))
            self.dr_soluong.set(str(d[5]))
            try:
                self.dr_date_entry.set_date(d[7])
            except Exception:
                pass
            self.dr_cachdung.set(d[6] or "")

    # Tự động sinh mã thuốc mới dạng tự tăng (Txx) để chuẩn bị nhập thuốc mới
    def dr_action_add(self):
        self.dr_action_clear()
        conn = get_connection()
        if conn:
            cur = conn.cursor()
            cur.execute("SELECT mathuoc FROM thuoc WHERE mathuoc LIKE 'T%' ORDER BY LENGTH(mathuoc) DESC, mathuoc DESC LIMIT 1")
            row = cur.fetchone()
            conn.close()
            if row and row[0].startswith("T"):
                try:
                    num = int(row[0][1:]) + 1
                    self.dr_mathuoc.set(f"T{num:02d}")
                except Exception:
                    self.dr_mathuoc.set("T01")
            else:
                self.dr_mathuoc.set("T01")

    # Xóa trắng form nhập thông tin dược phẩm
    def dr_action_clear(self):
        self.dr_mathuoc.set("")
        self.dr_tenthuoc.set("")
        self.dr_hoatchat.set("")
        self.dr_dongia.set("0")
        self.dr_soluong.set("100")
        self.dr_cachdung.set("")
        self.dr_search_var.set("")

    # Lưu thông tin thuốc vào CSDL (Thêm mới INSERT hoặc Cập nhật đơn giá/tồn kho UPDATE)
    def dr_action_save(self):
        mathuoc = self.dr_mathuoc.get().strip()
        tenthuoc = self.dr_tenthuoc.get().strip()
        hoatchat = self.dr_hoatchat.get().strip()
        dvt = self.dr_donvitinh.get().strip()
        cachdung = self.dr_cachdung.get().strip()
        hsd = self.dr_date_entry.get().strip()

        try:
            dongia = float(self.dr_dongia.get().strip())
            soluong = int(self.dr_soluong.get().strip())
        except ValueError:
            messagebox.showwarning("Sai định dạng", "Đơn giá và Số lượng phải là số hợp lệ!")
            return

        if not mathuoc or not tenthuoc:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập Mã thuốc và Tên biệt dược!")
            return

        conn = get_connection()
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute("SELECT mathuoc FROM thuoc WHERE mathuoc=%s", (mathuoc,))
            exists = cur.fetchone()
            if exists:
                cur.execute("""
                    UPDATE thuoc
                    SET tenthuoc=%s, hoatchat=%s, donvitinh=%s, dongia=%s, soluongton=%s, cachdung=%s, hansudung=%s
                    WHERE mathuoc=%s
                """, (tenthuoc, hoatchat, dvt, dongia, soluong, cachdung, hsd, mathuoc))
                messagebox.showinfo("Thành công", f"Đã cập nhật thông tin thuốc [{mathuoc}]!")
            else:
                cur.execute("""
                    INSERT INTO thuoc (mathuoc, tenthuoc, hoatchat, donvitinh, dongia, soluongton, cachdung, hansudung)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (mathuoc, tenthuoc, hoatchat, dvt, dongia, soluong, cachdung, hsd))
                messagebox.showinfo("Thành công", f"Đã thêm thuốc mới [{mathuoc}] thành công!")
            conn.commit()
            conn.close()
            self.dr_load_data()
            # Cập nhật lại cache combobox thuốc ở Tab Khám
            if hasattr(self, 'ex_load_comboboxes'):
                self.ex_load_comboboxes()
        except Exception as e:
            messagebox.showerror("Lỗi CSDL", f"Lỗi lưu thuốc:\n{e}")

    # Xóa một loại thuốc khỏi kho dược nếu chưa từng được kê trong đơn thuốc
    def dr_action_delete(self):
        mathuoc = self.dr_mathuoc.get().strip()
        if not mathuoc:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn thuốc muốn xóa!")
            return
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa thuốc [{mathuoc}] khỏi kho?"):
            conn = get_connection()
            if not conn:
                return
            try:
                cur = conn.cursor()
                cur.execute("DELETE FROM thuoc WHERE mathuoc=%s", (mathuoc,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Thành công", f"Đã xóa thành công thuốc {mathuoc}!")
                self.dr_action_clear()
                self.dr_load_data()
            except Exception as e:
                messagebox.showerror("Lỗi CSDL", f"Không thể xóa thuốc này:\n{e}")

    # Tìm kiếm thuốc theo mã thuốc, tên thuốc hoặc hoạt chất
    def dr_search(self):
        kw = self.dr_search_var.get().strip()
        if not kw:
            self.dr_load_data()
            return
        sql = "SELECT mathuoc, tenthuoc, hoatchat, donvitinh, dongia, soluongton, hansudung, cachdung FROM thuoc WHERE mathuoc LIKE %s OR tenthuoc LIKE %s OR hoatchat LIKE %s"
        p = f"%{kw}%"
        self.dr_load_data(sql, (p, p, p))

    # Lọc nhanh danh sách các loại thuốc có tồn kho thấp (<= 100 đơn vị) cần nhập thêm
    def dr_filter_low_stock(self):
        sql = "SELECT mathuoc, tenthuoc, hoatchat, donvitinh, dongia, soluongton, hansudung, cachdung FROM thuoc WHERE soluongton <= 100 ORDER BY soluongton ASC"
        self.dr_load_data(sql)
        messagebox.showinfo("Cảnh báo kho", "Đang hiển thị danh sách các loại thuốc có tồn kho ít (<= 100 đơn vị) cần lập kế hoạch nhập bổ sung!", parent=self.root)

    # ==========================================================================
    # TAB 4: VIỆN PHÍ & HÓA ĐƠN (BILLING & INVOICE PRINT)
    # ==========================================================================
    def build_tab_billing(self, parent):
        paned = tk.PanedWindow(parent, orient="horizontal", bg="#F8FAFC", sashrelief="raised", sashwidth=4)
        paned.pack(fill="both", expand=True, padx=5, pady=5)

        # KHỐI TRÁI: DANH SÁCH PHIẾU KHÁM CẦN THANH TOÁN
        frame_left = tk.LabelFrame(paned, text=" Danh sách Phiếu khám ", font=("Times New Roman", 12, "bold"),
                                   fg="#0F766E", bg="#FFFFFF", padx=10, pady=10)
        paned.add(frame_left, minsize=520, width=530)

        f_filter = tk.Frame(frame_left, bg="#FFFFFF")
        f_filter.pack(fill="x", pady=(0, 5))

        self.bill_filter_var = tk.StringVar(value="Chờ thanh toán")
        tk.Radiobutton(f_filter, text="Chờ thanh toán", variable=self.bill_filter_var, value="Chờ thanh toán",
                       bg="#FFFFFF", command=self.bill_load_queue).pack(side="left")
        tk.Radiobutton(f_filter, text="Đã thanh toán", variable=self.bill_filter_var, value="Đã thanh toán",
                       bg="#FFFFFF", command=self.bill_load_queue).pack(side="left", padx=10)
        tk.Radiobutton(f_filter, text="Tất cả", variable=self.bill_filter_var, value="All",
                       bg="#FFFFFF", command=self.bill_load_queue).pack(side="left")

        cols_q = ("mapk", "mabn", "hoten", "ngaykham", "trangthai")
        self.bill_tree_queue = ttk.Treeview(frame_left, columns=cols_q, show="headings", height=18)
        self.bill_tree_queue.heading("mapk", text="Mã PK")
        self.bill_tree_queue.heading("mabn", text="Mã BN")
        self.bill_tree_queue.heading("hoten", text="Họ tên Bệnh nhân")
        self.bill_tree_queue.heading("ngaykham", text="Ngày khám")
        self.bill_tree_queue.heading("trangthai", text="Trạng thái")

        self.bill_tree_queue.column("mapk", width=75, anchor="center")
        self.bill_tree_queue.column("mabn", width=70, anchor="center")
        self.bill_tree_queue.column("hoten", width=140)
        self.bill_tree_queue.column("ngaykham", width=115, anchor="center")
        self.bill_tree_queue.column("trangthai", width=100, anchor="center")

        self.bill_tree_queue.pack(fill="both", expand=True)
        self.bill_tree_queue.bind("<<TreeviewSelect>>", self.bill_on_select_queue)

        # KHỐI PHẢI: CHI TIẾT THANH TOÁN & HÓA ĐƠN
        frame_right = tk.LabelFrame(paned, text=" Chi tiết Viện phí & Quyết toán ", font=("Times New Roman", 12, "bold"),
                                    fg="#0284C7", bg="#FFFFFF", padx=15, pady=10)
        paned.add(frame_right, minsize=550)

        # Thông tin bệnh nhân & phiếu khám
        f_info = tk.Frame(frame_right, bg="#F0FDFA", padx=12, pady=8, highlightbackground="#0D9488", highlightthickness=1)
        f_info.pack(fill="x", pady=(0, 10))

        self.b_mapk = tk.StringVar(value="-")
        self.b_mabn = tk.StringVar(value="-")
        self.b_hoten = tk.StringVar(value="-")
        self.b_bhyt = tk.StringVar(value="Không có")
        self.b_chandoan = tk.StringVar(value="-")

        tk.Label(f_info, text="Phiếu khám:", font=("Times New Roman", 11, "bold"), bg="#F0FDFA").grid(row=0, column=0, sticky="w")
        tk.Label(f_info, textvariable=self.b_mapk, font=("Times New Roman", 11), fg="#0F766E", bg="#F0FDFA").grid(row=0, column=1, sticky="w", padx=(5, 20))

        tk.Label(f_info, text="Bệnh nhân:", font=("Times New Roman", 11, "bold"), bg="#F0FDFA").grid(row=0, column=2, sticky="w")
        tk.Label(f_info, textvariable=self.b_hoten, font=("Times New Roman", 11, "bold"), fg="#1E293B", bg="#F0FDFA").grid(row=0, column=3, sticky="w", padx=5)

        tk.Label(f_info, text="Số thẻ BHYT:", font=("Times New Roman", 11, "bold"), bg="#F0FDFA").grid(row=1, column=0, sticky="w", pady=(4, 0))
        tk.Label(f_info, textvariable=self.b_bhyt, font=("Times New Roman", 11), fg="#0284C7", bg="#F0FDFA").grid(row=1, column=1, sticky="w", padx=(5, 20), pady=(4, 0))

        tk.Label(f_info, text="Chẩn đoán:", font=("Times New Roman", 11, "bold"), bg="#F0FDFA").grid(row=1, column=2, sticky="w", pady=(4, 0))
        tk.Label(f_info, textvariable=self.b_chandoan, font=("Times New Roman", 11), fg="#1E293B", bg="#F0FDFA").grid(row=1, column=3, sticky="w", padx=5, pady=(4, 0))

        # Bảng danh mục chi phí (tiền khám + danh mục thuốc trong toa)
        tk.Label(frame_right, text="BẢNG KÊ CHI TIẾT CHI PHÍ ĐIỀU TRỊ:", font=("Times New Roman", 11, "bold"), bg="#FFFFFF", fg="#334155").pack(anchor="w", pady=(5, 2))

        cols_items = ("loai", "noidung", "soluong", "dongia", "thanhtien")
        self.bill_tree_items = ttk.Treeview(frame_right, columns=cols_items, show="headings", height=8)
        self.bill_tree_items.heading("loai", text="Hạng mục")
        self.bill_tree_items.heading("noidung", text="Tên dịch vụ / Thuốc")
        self.bill_tree_items.heading("soluong", text="SL")
        self.bill_tree_items.heading("dongia", text="Đơn giá")
        self.bill_tree_items.heading("thanhtien", text="Thành tiền")

        self.bill_tree_items.column("loai", width=85, anchor="center")
        self.bill_tree_items.column("noidung", width=180)
        self.bill_tree_items.column("soluong", width=50, anchor="center")
        self.bill_tree_items.column("dongia", width=90, anchor="e")
        self.bill_tree_items.column("thanhtien", width=100, anchor="e")

        self.bill_tree_items.pack(fill="both", expand=True, pady=2)

        # Khung tính toán tổng tiền & giảm trừ BHYT
        f_calc = tk.Frame(frame_right, bg="#FFFFFF", pady=5)
        f_calc.pack(fill="x")

        self.b_tienkham_var = tk.StringVar(value="100,000 đ")
        self.b_tienthuoc_var = tk.StringVar(value="0 đ")
        self.b_bhyt_giam_var = tk.StringVar(value="0 đ (0%)")
        self.b_tongcong_var = tk.StringVar(value="0 đ")

        tk.Label(f_calc, text="Tiền khám dịch vụ:", font=("Times New Roman", 11), bg="#FFFFFF").grid(row=0, column=0, sticky="w")
        tk.Label(f_calc, textvariable=self.b_tienkham_var, font=("Times New Roman", 11, "bold"), bg="#FFFFFF").grid(row=0, column=1, sticky="e", padx=(10, 30))

        tk.Label(f_calc, text="Tổng tiền thuốc:", font=("Times New Roman", 11), bg="#FFFFFF").grid(row=0, column=2, sticky="w")
        tk.Label(f_calc, textvariable=self.b_tienthuoc_var, font=("Times New Roman", 11, "bold"), bg="#FFFFFF").grid(row=0, column=3, sticky="e", padx=10)

        tk.Label(f_calc, text="BHYT hỗ trợ chi trả:", font=("Times New Roman", 11), bg="#FFFFFF").grid(row=1, column=0, sticky="w", pady=4)
        tk.Label(f_calc, textvariable=self.b_bhyt_giam_var, font=("Times New Roman", 11, "bold"), fg="#059669", bg="#FFFFFF").grid(row=1, column=1, sticky="e", padx=(10, 30), pady=4)

        tk.Label(f_calc, text="SỐ TIỀN THỰC THU:", font=("Times New Roman", 13, "bold"), fg="#DC2626", bg="#FFFFFF").grid(row=1, column=2, sticky="w", pady=4)
        tk.Label(f_calc, textvariable=self.b_tongcong_var, font=("Times New Roman", 14, "bold"), fg="#DC2626", bg="#FFFFFF").grid(row=1, column=3, sticky="e", padx=10, pady=4)

        # Nút bấm hành động Viện phí
        f_act = tk.Frame(frame_right, bg="#FFFFFF", pady=10)
        f_act.pack(fill="x")

        self.btn_pay = tk.Button(f_act, text="💳 XÁC NHẬN THANH TOÁN", font=("Times New Roman", 12, "bold"), bg="#0D9488", fg="white",
                                 relief="flat", cursor="hand2", padx=15, pady=5, command=self.bill_action_pay)
        self.btn_pay.pack(side="left", padx=5)

        btn_print = tk.Button(f_act, text="🖨️ XEM & IN HÓA ĐƠN", font=("Times New Roman", 12, "bold"), bg="#0284C7", fg="white",
                              relief="flat", cursor="hand2", padx=15, pady=5, command=self.bill_action_print)
        btn_print.pack(side="left", padx=5)

        self.bill_load_queue()

    # Tải danh sách các phiếu khám cần thanh toán theo bộ lọc (Chờ thanh toán / Đã thanh toán / Tất cả)
    def bill_load_queue(self):
        for r in self.bill_tree_queue.get_children():
            self.bill_tree_queue.delete(r)
        status_filter = self.bill_filter_var.get()
        conn = get_connection()
        if not conn:
            return
        cur = conn.cursor()
        if status_filter == "All":
            cur.execute("""
                SELECT pk.mapk, pk.mabn, CONCAT(bn.holot, ' ', bn.ten), pk.ngaykham, pk.trangthai
                FROM phieukham pk JOIN benhnhan bn ON pk.mabn = bn.mabn
                ORDER BY pk.ngaykham DESC
            """)
        else:
            cur.execute("""
                SELECT pk.mapk, pk.mabn, CONCAT(bn.holot, ' ', bn.ten), pk.ngaykham, pk.trangthai
                FROM phieukham pk JOIN benhnhan bn ON pk.mabn = bn.mabn
                WHERE pk.trangthai = %s
                ORDER BY pk.ngaykham DESC
            """, (status_filter,))

        for r in cur.fetchall():
            nk = r[3].strftime("%d/%m/%Y") if r[3] else ""
            self.bill_tree_queue.insert("", "end", values=(r[0], r[1], r[2], nk, r[4]))
        conn.close()

    # Chọn phiếu khám để thanh toán: tính tiền khám, tiền thuốc, mức khấu trừ BHYT và số tiền thực thu
    def bill_on_select_queue(self, event):
        sel = self.bill_tree_queue.selection()
        if not sel:
            return
        vals = self.bill_tree_queue.item(sel[0])["values"]
        mapk = vals[0]

        conn = get_connection()
        if not conn:
            return
        cur = conn.cursor()
        cur.execute("""
            SELECT pk.mapk, pk.mabn, CONCAT(bn.holot, ' ', bn.ten), bn.bhyt, pk.chandoan, pk.trangthai
            FROM phieukham pk JOIN benhnhan bn ON pk.mabn = bn.mabn
            WHERE pk.mapk = %s
        """, (mapk,))
        info = cur.fetchone()

        if info:
            self.b_mapk.set(info[0])
            self.b_mabn.set(info[1])
            self.b_hoten.set(f"{info[2]} (Mã BN: {info[1]})")
            has_bhyt = bool(info[3] and len(info[3].strip()) > 5)
            self.b_bhyt.set(info[3] if has_bhyt else "Không có thẻ BHYT")
            self.b_chandoan.set(info[4] or "")

            # Nạp danh sách mục chi phí
            for r in self.bill_tree_items.get_children():
                self.bill_tree_items.delete(r)

            tien_kham = 100000.0 # Chi phí khám ban đầu cố định
            self.bill_tree_items.insert("", "end", values=("Khám bệnh", "Khám lâm sàng & Chẩn đoán", 1, f"{int(tien_kham):,}đ", f"{int(tien_kham):,}đ"))

            # Lấy thuốc trong đơn
            cur.execute("SELECT tenthuoc, soluong, dongia, thanhtien FROM toathuoc_chitiet WHERE mapk=%s", (mapk,))
            tien_thuoc = 0.0
            for row in cur.fetchall():
                tt = float(row[3])
                tien_thuoc += tt
                self.bill_tree_items.insert("", "end", values=("Dược phẩm", row[0], row[1], f"{int(row[2]):,}đ", f"{int(tt):,}đ"))

            # Tính BHYT giảm trừ thông minh theo quy định chuẩn của BHXH Việt Nam:
            # - Đầu mã 'TE' (Trẻ em dưới 6 tuổi), 'HT' (Người có công, hưu trí): Giảm 100%
            # - Đầu mã 'DN' (Người lao động), 'GD' (Hộ gia đình), 'SV' (Sinh viên) hoặc mã hợp lệ khác: BHYT chi trả 80% (BN trả 20%)
            # - Không có thẻ BHYT: 0% (BN trả 100%)
            tong_chua_giam = tien_kham + tien_thuoc
            bhyt_code = (info[3] or "").strip().upper()
            bhyt_rate = 0.0
            bhyt_desc = "0% (Không thẻ)"
            if len(bhyt_code) >= 2:
                prefix = bhyt_code[:2]
                if prefix in ("TE", "HT"):
                    bhyt_rate = 1.00
                    bhyt_desc = f"100% ({prefix} - Miễn phí)"
                elif prefix in ("DN", "GD", "SV", "CH", "NN", "TK", "HC"):
                    bhyt_rate = 0.80
                    bhyt_desc = f"80% ({prefix})"
                elif len(bhyt_code) > 5:
                    bhyt_rate = 0.80
                    bhyt_desc = "80% (BHYT)"

            tien_bhyt = tong_chua_giam * bhyt_rate
            tong_thucthu = tong_chua_giam - tien_bhyt

            self.b_tienkham_var.set(f"{int(tien_kham):,} đ")
            self.b_tienthuoc_var.set(f"{int(tien_thuoc):,} đ")
            self.b_bhyt_giam_var.set(f"{int(tien_bhyt):,} đ ({bhyt_desc})")
            self.b_tongcong_var.set(f"{int(tong_thucthu):,} đ")

            # Lưu lại dữ liệu tạm để thanh toán/in
            self.current_bill_data = {
                "mapk": mapk,
                "mabn": info[1],
                "hoten": info[2],
                "bhyt": info[3] or "",
                "chandoan": info[4] or "",
                "tienkham": tien_kham,
                "tienthuoc": tien_thuoc,
                "tienbhyt": tien_bhyt,
                "tongtien": tong_thucthu,
                "trangthai": info[5]
            }

            if info[5] == "Đã thanh toán":
                self.btn_pay.config(state="disabled", text="✅ ĐÃ THANH TOÁN")
            else:
                self.btn_pay.config(state="normal", text="💳 XÁC NHẬN THANH TOÁN")

        conn.close()

    # Thực hiện thanh toán viện phí: lưu hóa đơn vào bảng hoadon và đổi trạng thái phiếu khám
    def bill_action_pay(self):
        if not hasattr(self, 'current_bill_data') or not self.current_bill_data:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn một phiếu khám để thanh toán!")
            return
        d = self.current_bill_data
        if d["trangthai"] == "Đã thanh toán":
            messagebox.showinfo("Thông báo", "Phiếu khám này đã được thanh toán trước đó!")
            return

        if messagebox.askyesno("Xác nhận thu phí", f"Xác nhận thu viện phí số tiền {int(d['tongtien']):,} đ\ncho bệnh nhân {d['hoten']}?"):
            conn = get_connection()
            if not conn:
                return
            try:
                cur = conn.cursor()
                # Cập nhật trạng thái phiếu khám
                cur.execute("UPDATE phieukham SET trangthai='Đã thanh toán' WHERE mapk=%s", (d["mapk"],))

                # Trừ số lượng tồn kho của các thuốc trong đơn thuốc này
                cur.execute("SELECT mathuoc, soluong FROM toathuoc_chitiet WHERE mapk=%s", (d["mapk"],))
                for mathuoc, sl in cur.fetchall():
                    cur.execute("UPDATE thuoc SET soluongton = GREATEST(0, soluongton - %s) WHERE mathuoc=%s", (sl, mathuoc))

                # Lưu hóa đơn viện phí
                cur.execute("SELECT mahd FROM hoadon_vienphi WHERE mahd LIKE 'HD%' ORDER BY LENGTH(mahd) DESC, mahd DESC LIMIT 1")
                row = cur.fetchone()
                mahd = "HD001"
                if row and row[0].startswith("HD"):
                    try:
                        mahd = f"HD{int(row[0][2:]) + 1:03d}"
                    except Exception:
                        mahd = "HD001"

                ngaylap = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cur.execute("""
                    INSERT INTO hoadon_vienphi (mahd, mapk, ngaylap, tienkham, tienthuoc, giamtru_bhyt, tongtien, trangthai, nguoithu)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, 'Đã thanh toán', %s)
                """, (mahd, d["mapk"], ngaylap, d["tienkham"], d["tienthuoc"], d["tienbhyt"], d["tongtien"], self.current_user["hoten"]))

                conn.commit()
                conn.close()

                messagebox.showinfo("Thành công", f"Thanh toán thành công hóa đơn [{mahd}]!\nĐã tự động trừ số lượng thuốc trong kho.")
                self.bill_load_queue()
                self.btn_pay.config(state="disabled", text="✅ ĐÃ THANH TOÁN")
                # Mở hóa đơn in ngay sau khi thanh toán
                self.bill_action_print()
            except Exception as e:
                messagebox.showerror("Lỗi thanh toán", f"Không thể hoàn tất thanh toán:\n{e}")

    # Mở cửa sổ xem trước và in hóa đơn viện phí chuẩn của phòng khám
    def bill_action_print(self):
        if not hasattr(self, 'current_bill_data') or not self.current_bill_data:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn phiếu khám cần in hóa đơn!")
            return
        d = self.current_bill_data

        # Tạo cửa sổ hiển thị hóa đơn in dạng Bill
        win_print = tk.Toplevel(self.root)
        win_print.title(f"HÓA ĐƠN VIỆN PHÍ - {d['mapk']}")
        center_window(win_print, 550, 680)
        win_print.config(bg="#FFFFFF")

        txt_bill = tk.Text(win_print, font=("Courier New", 10), padx=15, pady=15, bg="#FFFFFF", relief="flat")
        txt_bill.pack(fill="both", expand=True)

        now_str = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        lines = []
        lines.append("==================================================")
        lines.append("        PHÒNG KHÁM ĐA KHOA AN GIANG        ")
        lines.append("    Địa chỉ: Số 123 Hà Hoàng Hổ, TP. Long Xuyên   ")
        lines.append("          Điện thoại: (0296) 3841 234             ")
        lines.append("--------------------------------------------------")
        lines.append("           HÓA ĐƠN THANH TOÁN VIỆN PHÍ            ")
        lines.append("==================================================")
        lines.append(f"Mã phiếu khám : {d['mapk']}")
        lines.append(f"Mã bệnh nhân  : {d['mabn']}")
        lines.append(f"Họ tên BN     : {d['hoten']}")
        lines.append(f"Thẻ BHYT      : {d['bhyt'] if d['bhyt'] else 'Không'}")
        lines.append(f"Chẩn đoán     : {d['chandoan']}")
        lines.append(f"Thời gian in  : {now_str}")
        lines.append("--------------------------------------------------")
        lines.append(f"{'HẠNG MỤC CHI TIẾT':<30}{'SL':>4}{'THÀNH TIỀN':>14}")
        lines.append("--------------------------------------------------")
        lines.append(f"{'Tiền khám lâm sàng':<30}{'1':>4}{int(d['tienkham']):>12,} đ")

        # Đọc chi tiết thuốc
        conn = get_connection()
        if conn:
            cur = conn.cursor()
            cur.execute("SELECT tenthuoc, soluong, thanhtien FROM toathuoc_chitiet WHERE mapk=%s", (d["mapk"],))
            for tenthuoc, sl, tt in cur.fetchall():
                t_name = (tenthuoc[:28] + '..') if len(tenthuoc) > 30 else tenthuoc
                lines.append(f"{t_name:<30}{sl:>4}{int(tt):>12,} đ")
            conn.close()

        lines.append("--------------------------------------------------")
        lines.append(f"{'Tổng chi phí dịch vụ:':<34}{int(d['tienkham'] + d['tienthuoc']):>12,} đ")
        lines.append(f"{'Quỹ BHYT chi trả:':<34}-{int(d['tienbhyt']):>11,} đ")
        lines.append("==================================================")
        lines.append(f"{'BỆNH NHÂN THỰC TRẢ:':<34}{int(d['tongtien']):>12,} đ")
        lines.append("==================================================")
        lines.append("\n")
        lines.append(f"{'BỆNH NHÂN / THÂN NHÂN':<28}{'NGƯỜI THU TIỀN':>20}")
        lines.append(f"{'(Ký, ghi rõ họ tên)':<28}{'(Ký, đóng dấu)':>20}")
        lines.append("\n\n\n")
        lines.append(f"{'':<28}{self.current_user['hoten']:>20}")
        lines.append("--------------------------------------------------")
        lines.append("  * Chúc quý khách mau chóng bình phục sức khỏe! *")

        full_content = "\n".join(lines)
        txt_bill.insert("1.0", full_content)
        txt_bill.config(state="disabled")

        # Nút lưu text
        f_b = tk.Frame(win_print, bg="#FFFFFF", pady=10)
        f_b.pack(fill="x")

        # Lưu nội dung hóa đơn ra file văn bản (.txt) trên máy tính
        def save_txt():
            f_path = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=f"HoaDon_{d['mapk']}.txt")
            if f_path:
                with open(f_path, "w", encoding="utf-8") as f:
                    f.write(full_content)
                messagebox.showinfo("Thành công", f"Đã lưu phiếu hóa đơn tại:\n{f_path}")

        tk.Button(f_b, text="💾 Lưu Hóa đơn (.txt)", font=("Times New Roman", 11, "bold"), bg="#0D9488", fg="white",
                  relief="flat", cursor="hand2", command=save_txt).pack(side="left", padx=15)
        tk.Button(f_b, text="Đóng", font=("Times New Roman", 11), bg="#E2E8F0", fg="#1E293B",
                  relief="flat", cursor="hand2", command=win_print.destroy).pack(side="right", padx=15)

    # ==========================================================================
    # TAB 5: BÁO CÁO THỐNG KÊ (DASHBOARD & ANALYTICS)
    # ==========================================================================
    def build_tab_report(self, parent):
        # KHỐI CÁC THẺ CARD CHỈ SỐ TỔNG QUAN (KPI CARDS)
        f_kpi = tk.Frame(parent, bg="#F8FAFC", pady=10)
        f_kpi.pack(fill="x", padx=10)

        self.kpi_cards = {}
        cards_info = [
            ("card_patients", "TỔNG SỐ BỆNH NHÂN", "0", "👥", "#0D9488", "#CCFBF1"),
            ("card_exams", "LƯỢT KHÁM BỆNH", "0", "🩺", "#0284C7", "#E0F2FE"),
            ("card_drugs", "DANH MỤC THUỐC", "0", "💊", "#7C3AED", "#EDE9FE"),
            ("card_revenue", "TỔNG VIỆN PHÍ THU", "0 đ", "💰", "#059669", "#D1FAE5")
        ]

        for key, title, val, icon, fg_color, bg_color in cards_info:
            card = tk.Frame(f_kpi, bg=bg_color, padx=15, pady=12, relief="flat", highlightbackground=fg_color, highlightthickness=1)
            card.pack(side="left", expand=True, fill="both", padx=6)

            tk.Label(card, text=f"{icon}  {title}", font=("Times New Roman", 10, "bold"), fg=fg_color, bg=bg_color).pack(anchor="w")
            lbl_val = tk.Label(card, text=val, font=("Times New Roman", 18, "bold"), fg="#0F172A", bg=bg_color)
            lbl_val.pack(anchor="w", pady=(4, 0))
            self.kpi_cards[key] = lbl_val

        # BỘ LỌC DOANH THU THEO KHOẢNG THỜI GIAN
        f_filter = tk.LabelFrame(parent, text=" Thống kê Doanh thu theo Khoảng thời gian ", font=("Times New Roman", 12, "bold"),
                                 fg="#0F766E", bg="#FFFFFF", padx=15, pady=8)
        f_filter.pack(fill="x", padx=10, pady=5)

        tk.Label(f_filter, text="Từ ngày:", font=("Times New Roman", 11, "bold"), bg="#FFFFFF").pack(side="left", padx=5)
        self.rep_from_date = DateEntry(f_filter, width=11, background="#0D9488", foreground="white", date_pattern="yyyy-mm-dd")
        self.rep_from_date.set_date(datetime.date.today().replace(day=1))
        self.rep_from_date.pack(side="left", padx=5)

        tk.Label(f_filter, text="Đến ngày:", font=("Times New Roman", 11, "bold"), bg="#FFFFFF").pack(side="left", padx=(15, 5))
        self.rep_to_date = DateEntry(f_filter, width=11, background="#0D9488", foreground="white", date_pattern="yyyy-mm-dd")
        self.rep_to_date.set_date(datetime.date.today())
        self.rep_to_date.pack(side="left", padx=5)

        btn_calc = tk.Button(f_filter, text="📊 Xem thống kê", font=("Times New Roman", 11, "bold"), bg="#0D9488", fg="white",
                             relief="flat", cursor="hand2", command=self.rep_calculate)
        btn_calc.pack(side="left", padx=15)

        btn_excel_rep = tk.Button(f_filter, text="📥 Xuất Báo Cáo Excel", font=("Times New Roman", 11, "bold"), bg="#059669", fg="white",
                                  relief="flat", cursor="hand2", command=self.rep_export_excel)
        btn_excel_rep.pack(side="right", padx=5)

        # BẢNG THỐNG KÊ CHI TIẾT DOANH THU TỪNG HÓA ĐƠN
        f_tree = tk.Frame(parent, bg="#FFFFFF")
        f_tree.pack(fill="both", expand=True, padx=10, pady=(2, 8))

        cols = ("mahd", "mapk", "mabn", "hoten", "ngaylap", "tienkham", "tienthuoc", "giam_bhyt", "tongtien", "nguoithu")
        self.rep_tree = ttk.Treeview(f_tree, columns=cols, show="headings")

        self.rep_tree.heading("mahd", text="Mã HĐ")
        self.rep_tree.heading("mapk", text="Mã PK")
        self.rep_tree.heading("mabn", text="Mã BN")
        self.rep_tree.heading("hoten", text="Họ tên Bệnh nhân")
        self.rep_tree.heading("ngaylap", text="Ngày thanh toán")
        self.rep_tree.heading("tienkham", text="Tiền khám")
        self.rep_tree.heading("tienthuoc", text="Tiền thuốc")
        self.rep_tree.heading("giam_bhyt", text="BHYT hỗ trợ")
        self.rep_tree.heading("tongtien", text="Thực thu")
        self.rep_tree.heading("nguoithu", text="Người thu")

        self.rep_tree.column("mahd", width=75, anchor="center")
        self.rep_tree.column("mapk", width=70, anchor="center")
        self.rep_tree.column("mabn", width=65, anchor="center")
        self.rep_tree.column("hoten", width=140)
        self.rep_tree.column("ngaylap", width=120, anchor="center")
        self.rep_tree.column("tienkham", width=85, anchor="e")
        self.rep_tree.column("tienthuoc", width=90, anchor="e")
        self.rep_tree.column("giam_bhyt", width=85, anchor="e")
        self.rep_tree.column("tongtien", width=95, anchor="e")
        self.rep_tree.column("nguoithu", width=120)

        s_y = ttk.Scrollbar(f_tree, orient="vertical", command=self.rep_tree.yview)
        self.rep_tree.configure(yscrollcommand=s_y.set)
        s_y.pack(side="right", fill="y")
        self.rep_tree.pack(fill="both", expand=True)

        # Thanh tổng kết dưới bảng
        self.lbl_rep_summary = tk.Label(parent, text="Tổng doanh thu trong kỳ: 0 đ  |  Số lượt hóa đơn: 0",
                                        font=("Times New Roman", 12, "bold"), fg="#0F766E", bg="#F8FAFC", pady=4)
        self.lbl_rep_summary.pack(fill="x", padx=10)

        # Cập nhật số liệu ban đầu
        self.rep_update_kpis()
        self.rep_calculate()

    # Cập nhật số liệu thống kê tổng quan (Tổng bệnh nhân, Số lượt khám, Doanh thu, Danh mục thuốc)
    def rep_update_kpis(self):
        conn = get_connection()
        if not conn:
            return
        cur = conn.cursor()
        # Số bệnh nhân
        cur.execute("SELECT COUNT(*) FROM benhnhan")
        self.kpi_cards["card_patients"].config(text=str(cur.fetchone()[0]))

        # Số lượt khám
        cur.execute("SELECT COUNT(*) FROM phieukham")
        self.kpi_cards["card_exams"].config(text=str(cur.fetchone()[0]))

        # Số loại thuốc
        cur.execute("SELECT COUNT(*) FROM thuoc")
        self.kpi_cards["card_drugs"].config(text=str(cur.fetchone()[0]))

        # Tổng viện phí
        cur.execute("SELECT COALESCE(SUM(tongtien), 0) FROM hoadon_vienphi WHERE trangthai='Đã thanh toán'")
        tot = float(cur.fetchone()[0])
        self.kpi_cards["card_revenue"].config(text=f"{int(tot):,} đ")
        conn.close()

    # Thống kê doanh thu và số lượt khám theo khoảng thời gian tùy chọn (Từ ngày - Đến ngày)
    def rep_calculate(self):
        f_date = self.rep_from_date.get().strip()
        t_date = self.rep_to_date.get().strip()

        for r in self.rep_tree.get_children():
            self.rep_tree.delete(r)

        conn = get_connection()
        if not conn:
            return
        cur = conn.cursor()
        sql = """
            SELECT hd.mahd, hd.mapk, pk.mabn, CONCAT(bn.holot, ' ', bn.ten) as hoten,
                   hd.ngaylap, hd.tienkham, hd.tienthuoc, hd.giamtru_bhyt, hd.tongtien, hd.nguoithu
            FROM hoadon_vienphi hd
            JOIN phieukham pk ON hd.mapk = pk.mapk
            JOIN benhnhan bn ON pk.mabn = bn.mabn
            WHERE DATE(hd.ngaylap) >= %s AND DATE(hd.ngaylap) <= %s
            ORDER BY hd.ngaylap DESC
        """
        cur.execute(sql, (f_date, t_date))
        rows = cur.fetchall()

        total_rev = 0.0
        for r in rows:
            nl = r[4].strftime("%d/%m/%Y %H:%M") if r[4] else ""
            total_rev += float(r[8])
            self.rep_tree.insert("", "end", values=(
                r[0], r[1], r[2], r[3], nl,
                f"{int(r[5]):,}đ", f"{int(r[6]):,}đ", f"{int(r[7]):,}đ", f"{int(r[8]):,}đ", r[9]
            ))

        self.lbl_rep_summary.config(
            text=f"📊 KẾT QUẢ: Từ {f_date} đến {t_date}  |  Tổng số hóa đơn: {len(rows)}  |  TỔNG DOANH THU: {int(total_rev):,} đ"
        )
        conn.close()

    # Xuất báo cáo thống kê doanh thu ra file Excel (.xlsx) chuẩn báo cáo tài chính
    def rep_export_excel(self):
        f_date = self.rep_from_date.get().strip()
        t_date = self.rep_to_date.get().strip()

        conn = get_connection()
        if not conn:
            return
        cur = conn.cursor()
        sql = """
            SELECT hd.mahd, hd.mapk, pk.mabn, CONCAT(bn.holot, ' ', bn.ten) as hoten,
                   hd.ngaylap, hd.tienkham, hd.tienthuoc, hd.giamtru_bhyt, hd.tongtien, hd.nguoithu
            FROM hoadon_vienphi hd
            JOIN phieukham pk ON hd.mapk = pk.mapk
            JOIN benhnhan bn ON pk.mabn = bn.mabn
            WHERE DATE(hd.ngaylap) >= %s AND DATE(hd.ngaylap) <= %s
            ORDER BY hd.ngaylap DESC
        """
        cur.execute(sql, (f_date, t_date))
        rows = cur.fetchall()
        conn.close()

        if not rows:
            messagebox.showwarning("Thông báo", "Không có dữ liệu trong khoảng thời gian đã chọn!")
            return

        try:
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "BaoCaoDoanhThu"

            headers = ["Mã HĐ", "Mã PK", "Mã BN", "Họ tên Bệnh nhân", "Ngày thanh toán", "Tiền khám (đ)", "Tiền thuốc (đ)", "BHYT giảm (đ)", "Thực thu (đ)", "Người thu"]
            ws.append(headers)

            header_fill = PatternFill(start_color="0D9488", end_color="0D9488", fill_type="solid")
            for col_idx in range(1, len(headers) + 1):
                cell = ws.cell(row=1, column=col_idx)
                cell.font = Font(name="Times New Roman", size=12, bold=True, color="FFFFFF")
                cell.fill = header_fill
                cell.alignment = Alignment(horizontal="center", vertical="center")

            total_sum = 0
            for r in rows:
                if r[4] and hasattr(r[4], 'strftime'):
                    nl = r[4].strftime("%d/%m/%Y %H:%M")
                else:
                    nl = str(r[4] or "")
                ws.append([r[0], r[1], r[2], r[3], nl, r[5], r[6], r[7], r[8], r[9]])
                total_sum += r[8]

            # Dòng tổng cộng
            last_row = len(rows) + 2
            ws.cell(row=last_row, column=4, value="TỔNG CỘNG DOANH THU:").font = Font(name="Times New Roman", size=12, bold=True)
            ws.cell(row=last_row, column=9, value=total_sum).font = Font(name="Times New Roman", size=12, bold=True, color="DC2626")

            # Tự động canh độ rộng cột
            for col_idx, col in enumerate(ws.columns, 1):
                col_letter = get_column_letter(col_idx)
                max_len = 0
                for cell in col:
                    val = str(cell.value or '')
                    if len(val) > max_len:
                        max_len = len(val)
                ws.column_dimensions[col_letter].width = max(max_len + 4, 12)

            file_path = filedialog.asksaveasfilename(
                parent=self.root,
                defaultextension=".xlsx",
                filetypes=[("Excel Files (*.xlsx)", "*.xlsx"), ("All Files (*.*)", "*.*")],
                initialfile=f"BaoCaoDoanhThu_{f_date}_den_{t_date}.xlsx"
            )
            if file_path:
                try:
                    wb.save(file_path)
                except PermissionError:
                    messagebox.showerror("Lỗi ghi file", f"Không thể lưu file vì file này đang được mở trong Excel!\n\nVui lòng đóng file Excel '{os.path.basename(file_path)}' rồi bấm Xuất Excel lại.", parent=self.root)
                    return
                if messagebox.askyesno("Thành công", f"Đã xuất báo cáo doanh thu ra Excel thành công:\n{file_path}\n\nBạn có muốn mở file này ngay bây giờ không?", parent=self.root):
                    try:
                        os.startfile(file_path)
                    except Exception:
                        pass
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xuất file Excel:\n{e}", parent=self.root)

# ==============================================================================
# ĐIỂM BẮT ĐẦU CHƯƠNG TRÌNH (ENTRY POINT)
# ==============================================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()

