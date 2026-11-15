# HỆ THỐNG QUẢN LÝ BỆNH NHÂN VÀ PHÒNG KHÁM ĐA KHOA
> **Học phần:** Chuyên đề Python (Mã học phần: COS525)  
> **Khoa:** Công Nghệ Thông Tin – Trường Đại học An Giang (ĐHQG TP.HCM)  
> **Giảng viên hướng dẫn:** ThS. Nguyễn Ngọc Minh  

---

## 👨‍💻 THÔNG TIN NHÓM SINH VIÊN THỰC HIỆN
- **Sinh viên 1:** Văng Thành Phát — **MSSV:** `DTH245849` — **Lớp:** `DH25TH3`
- **Sinh viên 2:** Lê Minh Triết — **MSSV:** `DTH245928` — **Lớp:** `DH25TH3`
- **Nhóm Đồ Án:** Nhóm 05 — **Tổ thực hành:** Tổ 01

---

## 📂 CẤU TRÚC THƯ MỤC DỰ ÁN (PROJECT STRUCTURE)

Dự án được tổ chức khoa học theo chuẩn kỹ thuật phần mềm:

```text
QuanLyBenhNhan/
│
├── docs/                                   # THƯ MỤC BÁO CÁO & TÀI LIỆU
│   ├── DOAN_PYTHON.docx                    # Bản báo cáo đồ án chính thức (Word)
│   ├── DOAN_PYTHON.pdf                     # Bản báo cáo đồ án chính thức (PDF)
│   ├── HUONG_DAN_SU_DUNG.md                # Cẩm nang hướng dẫn sử dụng chi tiết
│   └── SLIDE_THUYET_TRINH_...pptx          # Slide thuyết trình báo cáo trước hội đồng
│
├── src/                                    # THƯ MỤC MÃ NGUỒN CHƯƠNG TRÌNH (SOURCE CODE)
│   ├── QLBN.py                             # Giao diện chính Tkinter & Xử lý nghiệp vụ 5 Phân hệ
│   ├── DatabaseQLBN.py                     # Tầng kết nối và tự động khởi tạo CSDL MySQL
│   ├── csdl_quanlybenhnhan.sql             # Kịch bản CSDL MySQL chuẩn 3NF và dữ liệu mẫu
│   └── assets/                             # Thư mục hình ảnh, logo y tế phòng khám
│
├── scripts/                                # CÁC KỊCH BẢN TỰ ĐỘNG HÓA (.BAT)
│   ├── Day_Code_Len_Github.bat             # 1-Click tự động commit và đẩy mã nguồn lên GitHub
│   └── Dong_Goi_Nop_Bai.bat                # 1-Click đóng gói toàn bộ đồ án thành file ZIP nộp bài
│
├── Chay_Phan_Mem.bat                       # FILE KHỞI CHẠY PHẦN MỀM 1-CLICK (ROOT)
├── requirements.txt                        # Danh mục thư viện Python phụ thuộc
└── README.md                               # Tài liệu giới thiệu tổng quan dự án
```

---

## 🌟 CÁC PHÂN HỆ CHỨC NĂNG CHÍNH (5 TABS)

1. **📋 Quản lý Hồ sơ Bệnh nhân (Tab 1):**
   - Đăng ký hồ sơ bệnh nhân, quản lý thông tin hành chính, thẻ BHYT, tiền sử bệnh án.
   - Hỗ trợ tìm kiếm thông minh đa tiêu chí và **Xuất danh sách ra file Excel (.xlsx)** chuẩn định dạng.

2. **🩺 Khám bệnh & Kê đơn thuốc điện tử (Tab 2):**
   - Tiếp nhận khám lâm sàng, ghi nhận chỉ số sinh tồn (huyết áp, nhịp tim, cân nặng).
   - Kê đơn thuốc điện tử: tự động kiểm tra số lượng tồn kho và tính thành tiền tức thì.

3. **💊 Quản lý Kho Dược phẩm (Tab 3):**
   - Quản lý danh mục thuốc biệt dược, hoạt chất, hạn sử dụng, đơn giá và số lượng tồn.
   - Tự động **cảnh báo đỏ các loại thuốc có tồn kho thấp ($\le 100$ đơn vị)** cần nhập bổ sung.

4. **💳 Viện phí & Quyết toán Hóa đơn (Tab 4):**
   - Danh sách phiếu chờ thanh toán.
   - Tự động tính toán mức khấu trừ BHYT (80%, 95%, 100% hoặc 0%) và tính số tiền thực thu.
   - Hỗ trợ **Xem trước và In hóa đơn viện phí**.

5. **📊 Báo cáo Thống kê Doanh thu (Tab 5):**
   - Hiển thị 4 thẻ chỉ số KPI tổng hợp nhanh (Tổng bệnh nhân, Lượt khám, Doanh thu, Thuốc).
   - Thống kê doanh thu theo khoảng thời gian và **Xuất báo cáo tài chính ra file Excel (.xlsx)**.

---

## 🚀 HƯỚNG DẪN CÀI ĐẶT & CHẠY ỨNG DỤNG

### Bước 1: Khởi động Cơ sở dữ liệu (MySQL / XAMPP)
1. Mở bảng điều khiển **XAMPP Control Panel**.
2. Nhấn nút **Start** tại mục **MySQL** (cổng mặc định `3306`).

### Bước 2: Cài đặt thư viện phụ thuộc
Mở Command Prompt / Terminal tại thư mục dự án và chạy lệnh:
```bash
pip install -r requirements.txt
```

### Bước 3: Khởi chạy phần mềm
- **Cách 1 (Nhanh nhất):** Nhấp đúp chuột vào file **`Chay_Phan_Mem.bat`** ở thư mục gốc.
- **Cách 2 (Bằng dòng lệnh):**
  ```bash
  cd src
  python QLBN.py
  ```

---

## 🔐 TÀI KHOẢN ĐĂNG NHẬP MẶC ĐỊNH

| Tên đăng nhập | Mật khẩu | Quyền hạn (Vai trò) | Quyền truy cập các Phân hệ |
| :--- | :---: | :---: | :--- |
| **admin** | `123` | **Quản Trị Viên** | Toàn quyền sử dụng đủ cả 5 Tab |
| **bacsi01** | `123` | **Bác Sĩ** | Tab 1 (Bệnh nhân), Tab 2 (Khám bệnh), Tab 3 (Tra cứu kho) |
| **thungan01** | `123` | **Thu Ngân** | Tab 4 (Thu viện phí & In hóa đơn) |
| **duocsi01** | `123` | **Dược Sĩ** | Tab 3 (Quản lý kho dược) |
| **tieptan01** | `123` | **Tiếp Tân** | Tab 1 (Tiếp nhận hồ sơ bệnh nhân) |
