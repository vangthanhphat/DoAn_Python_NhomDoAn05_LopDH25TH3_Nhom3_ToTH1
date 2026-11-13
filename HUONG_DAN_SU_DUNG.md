# HƯỚNG DẪN CÀI ĐẶT & CHẠY ĐỒ ÁN QUẢN LÝ BỆNH NHÂN
**Học phần:** Chuyên đề Python (COS525)  
**Giảng viên hướng dẫn:** ThS. Nguyễn Ngọc Minh  
**Trường:** Đại học An Giang - Khoa Công nghệ Thông tin  

---

## 1. Cấu trúc thư mục đồ án
```
d:\chuyen de python\QuanLyBenhNhan\
│
├── QLBN.py                           # Chương trình chính (Giao diện Tkinter + Nghiệp vụ)
├── DatabaseQLBN.py                   # Module kết nối MySQL & Khởi tạo CSDL tự động
├── csdl_quanlybenhnhan.sql           # File kịch bản SQL (dùng import thủ công nếu cần)
├── requirements.txt                  # Danh sách thư viện Python cần cài
├── BAOCAO_DOAN_QUANLYBENHNHAN.docx   # File Báo cáo Word chuẩn 100% quy định của Thầy
├── HUONG_DAN_SU_DUNG.md              # File hướng dẫn này
│
└── assets/                           # Thư mục hình ảnh & logo
    ├── logo.png                      # Logo phòng khám / y tế
    └── diagrams/                     # Các sơ đồ kiến trúc, E-R, quy trình và mockup
```

---

## 2. Các bước cài đặt môi trường
Mở cửa sổ dòng lệnh (Terminal / PowerShell / Command Prompt) và chạy lệnh:
```bash
pip install -r requirements.txt
```
*(Hoặc: `pip install mysql-connector-python tkcalendar pillow openpyxl python-docx`)*

---

## 3. Khởi động Cơ sở Dữ liệu MySQL
1. Khởi động máy chủ MySQL (bằng phần mềm **VertrigoServ** hoặc **XAMPP** hoặc **MySQL Server**).
2. Ứng dụng đã được tích hợp thuật toán **tự động dò mật khẩu** (`vertrigo`, mật khẩu rỗng `""`, `root`, `12345679`, `123456`, `admin`).
3. Ứng dụng sẽ **tự động tạo database `qlbenhnhan` và nạp toàn bộ dữ liệu mẫu** (bệnh nhân, bác sĩ, thuốc, phiếu khám, viện phí) ngay trong lần đầu chạy mà bạn không cần phải import thủ công!

---

## 4. Chạy phần mềm
Mở terminal tại thư mục chứa đồ án và chạy:
```bash
python QLBN.py
```

---

## 5. Tài khoản đăng nhập mẫu
Hệ thống hỗ trợ cơ chế phân quyền đa người dùng:

| Tên đăng nhập | Mật khẩu | Họ và tên | Vai trò / Quyền hạn | Ghi chú |
| :--- | :---: | :--- | :--- | :--- |
| **`admin`** | `123` | Quản Trị Viên | **Admin** | Toàn quyền kiểm soát toàn bộ 5 Tab chức năng |
| **`bsminh`** | `123` | ThS.BS Nguyễn Ngọc Minh | **Bác sĩ** | 3 Tab chuyên môn: Hồ sơ bệnh nhân, Khám bệnh & Kê toa, Tra cứu kho dược |
| **`dsanh`** | `123` | DS. Huỳnh Minh Anh | **Dược sĩ** | Chỉ 1 Tab chuyên trách: Quản lý kho dược phẩm, kiểm kê tồn kho, cập nhật giá thuốc |
| **`ttphat`** | `123` | Văng Thành Phát | **Tiếp tân** | Chỉ 1 Tab chuyên trách: Tiếp nhận hồ sơ bệnh nhân, cấp mã BN mới |
| **`tntriet`** | `123` | Lê Minh Triết | **Thu ngân** | Chỉ 1 Tab chuyên trách: Thu viện phí, áp dụng BHYT, in hóa đơn |

*(Bạn cũng có thể bấm nút **"Đăng ký tài khoản nhân viên"** tại màn hình đăng nhập để tạo thêm tài khoản mới).*

---

## 6. Các tính năng nổi bật của phần mềm
1. **Quản lý Hồ sơ Bệnh nhân:**
   - Đầy đủ chức năng CRUD (Thêm, Sửa, Lưu, Xóa, Làm mới).
   - Tự động sinh mã bệnh nhân thông minh (`BN001`, `BN002`...).
   - Nhập ngày sinh bằng lịch chọn trực quan (`DateEntry`).
   - Tìm kiếm nhanh đa tiêu chí (theo Tên, Mã số, Số điện thoại, CCCD).
   - **Xuất danh sách bệnh nhân ra file Excel (.xlsx)** có định dạng màu sắc chuyên nghiệp.

2. **Tiếp nhận & Khám bệnh & Kê đơn thuốc:**
   - Nhập chỉ số sinh tồn: Huyết áp, Nhịp tim, Cân nặng.
   - Thăm khám triệu chứng, chẩn đoán xác định bệnh lý và kết luận lời dặn.
   - Kê đơn thuốc điện tử: Chọn thuốc trực tiếp từ kho dược, nhập số lượng và liều dùng.
   - **Tự động kiểm tra số lượng tồn kho** cảnh báo nếu kê vượt quá số thuốc còn lại.

3. **Quản lý Kho Dược phẩm:**
   - Quản lý danh mục thuốc, hoạt chất, đơn vị tính, đơn giá, hạn dùng.
   - Nút **"Cảnh báo tồn kho ít"** lọc các thuốc sắp hết để lên kế hoạch nhập hàng.

4. **Quản lý Viện phí & Hóa đơn:**
   - Tự động tổng hợp tiền công khám + tổng tiền các loại thuốc trong đơn.
   - **Tự động áp dụng giảm trừ BHYT thông minh chuẩn BHXH Việt Nam**:
     * Đầu mã `TE` (Trẻ em dưới 6 tuổi), `HT` (Hưu trí, người có công): Chi trả **100%** (Miễn phí hoàn toàn).
     * Đầu mã `DN` (Người lao động), `GD` (Hộ gia đình), `SV` (Sinh viên) hoặc mã hợp lệ: Quỹ BHYT chi trả **80%** (Bệnh nhân chỉ trả 20%).
     * Không có thẻ BHYT: Chi trả **100%**.
   - Khấu trừ số lượng tồn kho thuốc ngay khi thanh toán.
   - Xem và in **Hóa đơn Viện phí** dạng Bill chi tiết, hỗ trợ lưu ra file `.txt`.

5. **Báo cáo Thống kê:**
   - 4 thẻ KPI chỉ số tổng quan (Tổng số bệnh nhân, Lượt khám, Danh mục thuốc, Doanh thu).
   - Lọc doanh thu theo khoảng thời gian tùy chọn (Từ ngày ... Đến ngày ...).
   - **Xuất báo cáo doanh thu ra file Excel (.xlsx)** phục vụ quản lý và kế toán.

---

## 7. Báo cáo đồ án (.docx)
- File báo cáo hoàn chỉnh được lưu tại:  
  `d:\chuyen de python\QuanLyBenhNhan\BAOCAO_DOAN_QUANLYBENHNHAN.docx`
- Tuân thủ 100% quy định trình bày của ThS. Nguyễn Ngọc Minh (Font Times New Roman 13, căn lề Trái 4.0cm, Trên/Dưới/Phải 2.5cm, giãn dòng 1.2, có đủ hình vẽ sơ đồ kiến trúc, luồng quy trình, sơ đồ E-R CSDL và ảnh minh họa từng giao diện chức năng).

