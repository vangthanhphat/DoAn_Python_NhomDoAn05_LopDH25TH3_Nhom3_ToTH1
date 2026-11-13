# KỊCH BẢN THUYẾT TRÌNH BẢO VỆ ĐỒ ÁN & BỘ CÂU HỎI VẤN ĐÁP
**Học phần:** Chuyên đề Python (COS525)  
**Giảng viên hướng dẫn:** ThS. Nguyễn Ngọc Minh  
**Sinh viên thực hiện:** Văng Thành Phát - MSSV: DTH245849 - Lớp: DH25TH3  
**Đề tài:** Xây dựng ứng dụng Quản lý Bệnh nhân với Python, Tkinter và MySQL  

---

## PHẦN 1: KỊCH BẢN THUYẾT TRÌNH SLIDE (Thời lượng: 5 - 7 phút)

### Slide 1: Bìa & Giới thiệu
> *"Kính thưa Thầy Nguyễn Ngọc Minh và các bạn, em tên là Văng Thành Phát, sinh viên lớp DH25TH3. Hôm nay em xin phép được báo cáo đồ án học phần Chuyên đề Python với đề tài: 'Xây dựng ứng dụng Quản lý Bệnh nhân với Python, Tkinter và Cơ sở dữ liệu MySQL'."*

### Slide 2: Đặt vấn đề & Mục tiêu
> *"Xuất phát từ thực tế tại các phòng khám vừa và nhỏ hiện nay, việc quản lý bằng sổ sách hoặc bảng tính Excel rời rạc bộc lộ nhiều bất cập: tốn thời gian tìm kiếm, dễ nhầm lẫn hồ sơ, khó kiểm soát tồn kho thuốc và khó tổng hợp doanh thu viện phí. Mục tiêu của đồ án là xây dựng một phần mềm Desktop hoàn chỉnh, giao diện thân thiện, chuẩn hóa quy trình tiếp nhận, khám lâm sàng, kê đơn điện tử, thanh toán viện phí có BHYT và thống kê báo cáo."*

### Slide 3: Kiến trúc & Cơ sở dữ liệu
> *"Về mặt kỹ thuật, hệ thống được xây dựng theo kiến trúc 3 lớp tiêu chuẩn: Tầng giao diện Tkinter, Tầng xử lý nghiệp vụ Python và Tầng dữ liệu MySQL. CSDL gồm 7 bảng quan hệ chặt chẽ: Nhân viên, Khoa phòng, Bệnh nhân, Thuốc, Phiếu khám, Toa thuốc chi tiết và Hóa đơn viện phí, đảm bảo toàn vẹn dữ liệu thông qua các ràng buộc khóa ngoại."*

### Slide 4 & 5: Các phân hệ nghiệp vụ & Demo thực tế
> *"Phần mềm có 5 phân hệ chính và cơ chế phân quyền chuẩn mực theo nghiệp vụ bệnh viện: Admin (toàn quyền 5 Tab), Bác sĩ (3 Tab chuyên môn), Dược sĩ (chuyên trách quản lý kho dược), Tiếp tân (chuyên trách tiếp nhận bệnh nhân) và Thu ngân (chuyên trách viện phí & hóa đơn). Sau đây em xin phép được Demo trực tiếp quy trình khép kín trên phần mềm..."*

---

## PHẦN 2: KỊCH BẢN THAO TÁC DEMO TRỰC TIẾP (3 - 5 phút)

Để tạo ấn tượng tốt nhất với Thầy, hãy thực hiện theo 4 bước kịch bản nghiệp vụ khép kín sau:

### Bước 1: Đăng nhập quyền Tiếp tân (`ttphat` / `123`) & Tiếp nhận Bệnh nhân mới
1. Mở phần mềm: `python QLBN.py` (hoặc nhấp đúp `Chay_Phan_Mem.bat`).
2. Đăng nhập tài khoản của bạn: **`ttphat`** / **`123`** (Tiếp tân: Văng Thành Phát).
3. Chỉ cho Thầy thấy: **Giao diện chỉ hiển thị duy nhất 1 Tab "📋 Tiếp Nhận Hồ Sơ Bệnh Nhân"**, Tiếp tân không can thiệp vào thu tiền hay kê đơn thuốc.
4. Nhấn nút **"➕ Thêm mới"** $\rightarrow$ Mã bệnh nhân tự động sinh là `BN009`.
5. Nhập thông tin bệnh nhân:
   - Họ & Tên lót: `Nguyễn Văn` | Tên: `Khoa`
   - Giới tính: `Nam` | Ngày sinh: Chọn trên lịch `DateEntry`
   - Số ĐT: `0919888999` | CCCD: `089099001122` | BHYT: `DN4890099999999`
6. Nhấn **"💾 Lưu"** $\rightarrow$ Bệnh nhân lập tức hiển thị lên bảng Treeview.
7. Thử gõ `Khoa` vào ô tìm kiếm $\rightarrow$ Bảng tự động lọc tức thì.
8. Nhấn nút **"📊 Xuất Excel"** $\rightarrow$ Lưu file và bấm "Yes" để phần mềm tự động bật Microsoft Excel lên cho Thầy xem bảng dữ liệu đẹp mắt.

### Bước 2: Đăng nhập quyền Bác sĩ (`bsminh` / `123`) & Khám bệnh
1. Bấm **"Đăng xuất"** $\rightarrow$ Đăng nhập bằng tài khoản `bsminh` / `123` (ThS.BS Nguyễn Ngọc Minh).
2. Chỉ cho Thầy thấy: **Bác sĩ chỉ thấy 3 Tab chuyên môn** (Hồ sơ bệnh nhân, Khám bệnh & Kê toa, Tra cứu kho dược), hoàn toàn không thể can thiệp vào viện phí hay doanh thu.
3. Chuyển sang Tab **"🩺 Khám Bệnh & Toa Thuốc"**:
   - Bấm **"➕ Tạo phiếu mới"** $\rightarrow$ Sinh mã `PK004`.
   - Bấm ô chọn bệnh nhân $\rightarrow$ Nhìn thấy ngay bệnh nhân `BN009 - Nguyễn Văn Khoa` vừa được Tiếp tân đăng ký!
   - Nhập chỉ số sinh tồn: Huyết áp `125/80`, Nhịp tim `76`, Cân nặng `62.0`.
   - Nhập triệu chứng: `Đau đầu, sốt nhẹ`. Chẩn đoán: `Cảm cúm thông thường`.
   - **Kê đơn thuốc:** Chọn `Paracetamol 500mg`, nhập SL: `10` $\rightarrow$ Nhấn **"➕ Thêm thuốc"**.
   - *(Mẹo ghi điểm: Thử nhập SL `9999` $\rightarrow$ Phần mềm cảnh báo vượt tồn kho ngay lập tức).*
   - Nhấn **"💾 Lưu Bệnh Án"**.

### Bước 3: Đăng nhập quyền Thu ngân (`tntriet` / `123`) & Thanh toán Viện phí
1. Bấm **"Đăng xuất"** $\rightarrow$ Đăng nhập bằng `tntriet` / `123` (Thu ngân: Lê Minh Triết).
2. Chỉ cho Thầy thấy: **Thu ngân chỉ thấy duy nhất 1 Tab "💳 Thu Viện Phí & Hóa Đơn"**, không can thiệp vào hồ sơ bệnh nhân hay chuyên môn y khoa.
3. Thao tác quyết toán:
   - Chọn phiếu khám `PK004` của bệnh nhân `Nguyễn Văn Khoa`.
   - Chỉ cho Thầy thấy: Phần mềm tự động cộng tiền khám (100.000đ) + tiền thuốc (15.000đ) = 115.000đ.
   - Nhận diện thẻ BHYT thông minh theo chuẩn BHXH Việt Nam:
     * Đầu mã `TE` (Trẻ em dưới 6 tuổi), `HT` (Hưu trí): Chi trả **100%** (Miễn phí hoàn toàn).
     * Đầu mã `DN` (Người lao động), `GD` (Hộ gia đình), `SV` (Sinh viên): Quỹ BHYT chi trả **80%** (Bệnh nhân chỉ thanh toán 20%).
     * Không có thẻ BHYT: Chi trả **100%** chi phí.
   - Nhấn nút **"💳 XÁC NHẬN THANH TOÁN"** $\rightarrow$ Trạng thái chuyển thành "Đã thanh toán".
   - Nhấn **"🖨️ XEM & IN HÓA ĐƠN"** $\rightarrow$ Mở popup phiếu hóa đơn bán lẻ dạng Bill chuyên nghiệp.

### Bước 4: Đăng nhập quyền Admin (`admin` / `123`) & Xem Báo cáo Quản trị
1. Đăng xuất $\rightarrow$ Đăng nhập bằng `admin` / `123`.
2. Chỉ cho Thầy thấy: **Admin có toàn quyền truy cập cả 5 Tab**.
3. Chuyển sang Tab **"💊 Kho Dược Phẩm"**: Chỉ cho Thầy thấy số lượng thuốc Paracetamol trong kho đã tự động bị trừ đi 10 viên sau khi Thu ngân xác nhận thanh toán! Các thuốc tồn kho $\le 100$ được tô màu hồng cảnh báo.
4. Chuyển sang Tab **"📊 Báo Cáo Thống Kê"**: Chỉ cho Thầy thấy doanh thu vừa thanh toán đã được cập nhật ngay vào KPI tổng doanh thu hôm nay!

---

## PHẦN 3: BỘ CÂU HỎI VẤN ĐÁP THƯỜNG GẶP CỦA THẦY & CÁCH TRẢ LỜI ĐẠT ĐIỂM 10

### ❓ Câu 1: Em hãy giải thích cơ chế kết nối MySQL trong ứng dụng?
> **Trả lời:**  
> *"Dạ thưa Thầy, em xây dựng module `DatabaseQLBN.py` độc lập, cấu hình chuẩn theo môi trường XAMPP cục bộ (`DB_HOST="localhost"`, `DB_USER="root"`, `DB_PASSWORD=""`, `DB_NAME="qlbenhnhan"`). Hàm `get_connection()` đảm nhận việc cấp kết nối an toàn cho các tác vụ truy vấn CRUD. Ngoài ra, hàm `init_database()` sử dụng cú pháp `CREATE DATABASE IF NOT EXISTS` và `CREATE TABLE IF NOT EXISTS` để tự động tạo CSDL chuẩn hóa 3NF và nạp dữ liệu mẫu ban đầu nếu hệ thống mới cài đặt."*

### ❓ Câu 2: Em xử lý mô hình CRUD trên bảng bệnh nhân như thế nào?
> **Trả lời:**  
> *"Dạ thưa Thầy, mô hình CRUD trong tab Bệnh nhân được thực hiện qua các hàm:
> - **Create (Thêm):** Hàm `p_action_add()` tự động truy vấn mã lớn nhất `BN...` để tăng lên 1 (VD: BN009) và xóa trắng form.
> - **Read (Đọc):** Hàm `p_load_data()` dùng câu lệnh `SELECT ... FROM benhnhan` nạp dữ liệu lên widget `ttk.Treeview`.
> - **Update (Cập nhật):** Hàm `p_action_save()` kiểm tra nếu `mabn` đã tồn tại trong CSDL thì chạy lệnh `UPDATE benhnhan SET ... WHERE mabn=%s`.
> - **Delete (Xóa):** Hàm `p_action_delete()` hiển thị hộp thoại `askyesno` xác nhận an toàn trước khi chạy lệnh `DELETE FROM benhnhan WHERE mabn=%s`."*

### ❓ Câu 3: Làm thế nào để đảm bảo khi thanh toán viện phí thì thuốc trong kho không bị thất thoát?
> **Trả lời:**  
> *"Dạ thưa Thầy, trong hàm `bill_action_pay()`, hệ thống sử dụng cơ chế giao dịch Transaction của MySQL:
> 1. Đầu tiên, truy vấn danh sách thuốc và số lượng trong bảng `toathuoc_chitiet` theo mã phiếu khám.
> 2. Chạy câu lệnh `UPDATE thuoc SET soluongton = GREATEST(0, soluongton - %s) WHERE mathuoc=%s` để khấu trừ tồn kho.
> 3. Cập nhật trạng thái phiếu khám sang `Đã thanh toán` và chèn bản ghi vào bảng `hoadon_vienphi`.
> 4. Cuối cùng thực hiện `conn.commit()` để đảm bảo toàn bộ các thao tác trên hoặc cùng thành công, hoặc rollback nếu có lỗi phát sinh."*

### ❓ Câu 4: Làm thế nào để hạn chế lỗi nhập sai định dạng ngày tháng của người dùng?
> **Trả lời:**  
> *"Dạ thưa Thầy, thay vì để người dùng gõ tay dạng text dễ nhầm lẫn (như DD/MM hay MM/DD), em đã tích hợp thư viện `tkcalendar` với widget `DateEntry(date_pattern='yyyy-mm-dd')`. Người dùng chỉ cần nhấp chuột chọn ngày trên lịch pop-up trực quan, vừa nhanh chóng vừa chuẩn hóa định dạng ngày tháng của MySQL."*

### ❓ Câu 5: Em xuất file Excel như thế nào mà không cần cài đặt phần mềm Microsoft Excel?
> **Trả lời:**  
> *"Dạ thưa Thầy, em sử dụng thư viện `openpyxl`. Thư viện này cho phép thao tác trực tiếp với cấu trúc XML của định dạng chuẩn `.xlsx`, giúp tạo file, tạo tiêu đề in đậm, đổ màu nền header `#0D9488`, kẻ viền ô Border mỏng và tự động tính toán độ rộng cột (Auto-fit width) một cách độc lập mà máy tính không cần cài đặt sẵn bộ Microsoft Office."*

