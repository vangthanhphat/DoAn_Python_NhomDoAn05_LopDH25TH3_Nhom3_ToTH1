-- ==============================================================================
-- ĐỒ ÁN MÔN HỌC: CHUYÊN ĐỀ PYTHON (COS525)
-- ĐỀ TÀI: XÂY DỰNG ỨNG DỤNG QUẢN LÝ BỆNH NHÂN
-- Sinh viên: Văng Thành Phát - MSSV: DTH245849 - Lớp: DH25TH3
-- Giảng viên hướng dẫn: ThS. Nguyễn Ngọc Minh
-- Khoa Công nghệ Thông tin - Trường Đại học An Giang
-- ==============================================================================

CREATE DATABASE IF NOT EXISTS qlbenhnhan CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE qlbenhnhan;

-- Xóa bảng cũ nếu tồn tại (theo thứ tự khóa ngoại)
DROP TABLE IF EXISTS toathuoc_chitiet;
DROP TABLE IF EXISTS hoadon_vienphi;
DROP TABLE IF EXISTS phieukham;
DROP TABLE IF EXISTS thuoc;
DROP TABLE IF EXISTS benhnhan;
DROP TABLE IF EXISTS khoaphong;
DROP TABLE IF EXISTS nhanvien;

-- 1. Bảng Nhân viên / Tài khoản (Toàn bộ NOT NULL để quản lý liên lạc chặt chẽ)
CREATE TABLE nhanvien (
    manv VARCHAR(20) PRIMARY KEY,
    hoten VARCHAR(100) NOT NULL,
    sodienthoai VARCHAR(20) NOT NULL,
    email VARCHAR(100) NOT NULL,
    tendangnhap VARCHAR(50) UNIQUE NOT NULL,
    matkhau VARCHAR(100) NOT NULL,
    vaitro VARCHAR(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. Bảng Khoa / Phòng
CREATE TABLE khoaphong (
    makhoa VARCHAR(20) PRIMARY KEY,
    tenkhoa VARCHAR(100) NOT NULL,
    mota VARCHAR(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. Bảng Bệnh nhân
CREATE TABLE benhnhan (
    mabn VARCHAR(20) PRIMARY KEY,
    holot VARCHAR(100) NOT NULL,
    ten VARCHAR(50) NOT NULL,
    phai VARCHAR(10) NOT NULL,
    ngaysinh DATE NOT NULL,
    cccd VARCHAR(20) NOT NULL,
    sdt VARCHAR(20) NOT NULL,
    diachi VARCHAR(255) NOT NULL,
    bhyt VARCHAR(30),
    nhommau VARCHAR(10) DEFAULT 'O',
    tiensubenh TEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4. Bảng Thuốc & Dược phẩm (Toàn bộ NOT NULL: bắt buộc rõ hoạt chất, giá, hạn dùng)
CREATE TABLE thuoc (
    mathuoc VARCHAR(20) PRIMARY KEY,
    tenthuoc VARCHAR(100) NOT NULL,
    hoatchat VARCHAR(150) NOT NULL,
    donvitinh VARCHAR(30) NOT NULL,
    dongia DECIMAL(12,2) NOT NULL,
    soluongton INT NOT NULL DEFAULT 0,
    cachdung VARCHAR(255) NOT NULL,
    hansudung DATE NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 5. Bảng Phiếu khám & Bệnh án (Triệu chứng & chẩn đoán NOT NULL)
CREATE TABLE phieukham (
    mapk VARCHAR(20) PRIMARY KEY,
    mabn VARCHAR(20) NOT NULL,
    manv_bacsi VARCHAR(20) NOT NULL,
    makhoa VARCHAR(20) NOT NULL,
    ngaykham DATETIME NOT NULL,
    trieuchung TEXT NOT NULL,
    huyetap VARCHAR(20) NOT NULL,
    nhiptim INT NOT NULL,
    cannang FLOAT NOT NULL,
    chandoan TEXT NOT NULL,
    ketluan TEXT NOT NULL,
    trangthai VARCHAR(30) NOT NULL DEFAULT 'Chờ thanh toán',
    FOREIGN KEY (mabn) REFERENCES benhnhan(mabn) ON DELETE CASCADE,
    FOREIGN KEY (manv_bacsi) REFERENCES nhanvien(manv) ON DELETE CASCADE,
    FOREIGN KEY (makhoa) REFERENCES khoaphong(makhoa) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 6. Bảng Chi tiết Toa thuốc (cachdung có thể NULL nếu dùng theo chỉ định riêng)
CREATE TABLE toathuoc_chitiet (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mapk VARCHAR(20) NOT NULL,
    mathuoc VARCHAR(20) NOT NULL,
    tenthuoc VARCHAR(100) NOT NULL,
    donvitinh VARCHAR(30) NOT NULL,
    soluong INT NOT NULL,
    dongia DECIMAL(12,2) NOT NULL,
    cachdung VARCHAR(255) DEFAULT NULL,
    thanhtien DECIMAL(12,2) NOT NULL,
    FOREIGN KEY (mapk) REFERENCES phieukham(mapk) ON DELETE CASCADE,
    FOREIGN KEY (mathuoc) REFERENCES thuoc(mathuoc) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 7. Bảng Hóa đơn viện phí
-- Ràng buộc 1 - 1 với Phiếu khám: mapk UNIQUE
-- Chuẩn hóa 3NF: Loại bỏ mabn (phụ thuộc bắc cầu qua phieukham)
-- Toàn bộ NOT NULL để minh bạch hóa tài chính
CREATE TABLE hoadon_vienphi (
    mahd VARCHAR(20) PRIMARY KEY,
    mapk VARCHAR(20) NOT NULL UNIQUE,
    ngaylap DATETIME NOT NULL,
    tienkham DECIMAL(12,2) NOT NULL,
    tienthuoc DECIMAL(12,2) NOT NULL,
    giamtru_bhyt DECIMAL(12,2) NOT NULL DEFAULT 0,
    tongtien DECIMAL(12,2) NOT NULL,
    trangthai VARCHAR(30) NOT NULL DEFAULT 'Đã thanh toán',
    nguoithu VARCHAR(100) NOT NULL,
    FOREIGN KEY (mapk) REFERENCES phieukham(mapk) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ==============================================================================
-- DỮ LIỆU KHỞI TẠO BAN ĐẦU (SEED DATA ĐÃ ĐỒNG BỘ)
-- ==============================================================================

-- Dữ liệu Nhân viên
INSERT INTO nhanvien (manv, hoten, sodienthoai, email, tendangnhap, matkhau, vaitro) VALUES
('NV01', 'Quản Trị Viên', '0912345678', 'admin@benhvien.vn', 'admin', '123', 'Admin'),
('NV02', 'ThS.BS Nguyễn Ngọc Minh', '0987654321', 'minh.nn@benhvien.vn', 'bsminh', '123', 'Bác sĩ'),
('NV03', 'DS. Huỳnh Minh Anh', '0908112233', 'anh.hm@benhvien.vn', 'dsanh', '123', 'Dược sĩ'),
('NV04', 'Văng Thành Phát', '0977223344', 'phat.vt@benhvien.vn', 'ttphat', '123', 'Tiếp tân'),
('NV05', 'Lê Minh Triết', '0933445566', 'triet.lm@benhvien.vn', 'tntriet', '123', 'Thu ngân');

-- Dữ liệu Khoa phòng
INSERT INTO khoaphong (makhoa, tenkhoa, mota) VALUES
('K01', 'Khoa Khám Bệnh', 'Tiếp nhận và khám sàng lọc ban đầu'),
('K02', 'Khoa Nội Tổng Hợp', 'Chẩn đoán và điều trị bệnh nội khoa'),
('K03', 'Khoa Ngoại Tổng Quát', 'Khám và xử lý phẫu thuật'),
('K04', 'Khoa Nhi', 'Khám và chăm sóc sức khỏe trẻ em'),
('K05', 'Khoa Tai Mũi Họng', 'Chuyên khoa tai mũi họng người lớn và trẻ em'),
('K06', 'Khoa Tim Mạch', 'Chuyên khoa chẩn đoán các bệnh lý tim mạch');

-- Dữ liệu Thuốc
INSERT INTO thuoc (mathuoc, tenthuoc, hoatchat, donvitinh, dongia, soluongton, cachdung, hansudung) VALUES
('T01', 'Paracetamol 500mg', 'Paracetamol', 'Viên', 1500.00, 500, 'Uống 1 viên khi sốt trên 38.5 độ, cách 4-6h', '2027-12-31'),
('T02', 'Amoxicillin 500mg', 'Amoxicillin', 'Viên', 3500.00, 300, 'Uống 1 viên x 2 lần/ngày sau khi ăn no', '2027-10-15'),
('T03', 'Augmentin 1g', 'Amoxicillin + Clavulanic', 'Hộp', 185000.00, 80, 'Uống 1 viên sáng, 1 viên chiều sau ăn', '2028-01-20'),
('T04', 'Panadol Extra', 'Paracetamol + Caffeine', 'Vỉ', 18000.00, 250, 'Uống 1-2 viên khi đau nhức đầu nhiều', '2027-08-30'),
('T05', 'Omeprazole 20mg', 'Omeprazole', 'Hộp', 65000.00, 120, 'Uống 1 viên trước bữa ăn sáng 30 phút', '2027-11-25'),
('T06', 'Cefuroxime 500mg', 'Cefuroxime axetil', 'Hộp', 145000.00, 90, 'Uống 1 viên x 2 lần/ngày sau bữa ăn', '2027-09-10'),
('T07', 'Berberin 50mg', 'Berberin clorid', 'Lọ', 25000.00, 180, 'Uống 4 viên x 2 lần/ngày khi đau bụng đi ngoài', '2028-05-01'),
('T08', 'Vitamin C 500mg', 'Acid Ascorbic', 'Hộp', 45000.00, 200, 'Uống 1 viên/ngày vào buổi sáng sau ăn', '2028-02-15'),
('T09', 'Amlodipine 5mg', 'Amlodipine besylate', 'Hộp', 85000.00, 110, 'Uống 1 viên/ngày cố định giờ buổi sáng', '2027-12-01'),
('T10', 'Gliclazide 80mg', 'Gliclazide', 'Hộp', 95000.00, 75, 'Uống 1 viên vào bữa ăn sáng', '2027-07-20');

-- Dữ liệu Bệnh nhân (Khu vực An Giang)
INSERT INTO benhnhan (mabn, holot, ten, phai, ngaysinh, cccd, sdt, diachi, bhyt, nhommau, tiensubenh) VALUES
('BN001', 'Võ Đức', 'Thịnh', 'Nam', '1985-05-12', '089085001234', '0918123456', 'Số 123 Hà Hoàng Hổ, Mỹ Xuyên, TP. Long Xuyên, An Giang', 'DN4890012345678', 'O', 'Dị ứng phấn hoa'),
('BN002', 'Hà Minh ', 'Trí', 'Nữ', '1992-08-20', '089192002345', '0982234567', 'Số 45 Trần Hưng Đạo, Mỹ Bình, TP. Long Xuyên, An Giang', 'GD4890023456789', 'A', 'Không'),
('BN003', 'Trần Sĩ', 'Tấn', 'Nam', '1978-03-15', '089078003456', '0903345678', 'Số 78 Lý Thái Tổ, Mỹ Long, TP. Long Xuyên, An Giang', 'DN4890034567890', 'B', 'Tăng huyết áp'),
('BN004', 'Huỳnh Thành', 'Trí', 'Nữ', '2000-11-05', '089100004567', '0974456789', 'Thị trấn Chợ Mới, Huyện Chợ Mới, An Giang', 'SV4890045678901', 'AB', 'Không'),
('BN005', 'Lê Đức', 'Việt', 'Nam', '1965-09-28', '089065005678', '0935567890', 'Phường Châu Phú A, TP. Châu Đốc, An Giang', 'HT4890056789012', 'O', 'Đái tháo đường týp 2'),
('BN006', 'Lê Minh', 'Vương', 'Nữ', '1998-04-18', '089198006789', '0966678901', 'Thị trấn Phú Mỹ, Huyện Phú Tân, An Giang', 'DN4890067890123', 'A', 'Viêm mũi xoang'),
('BN007', 'Nguyễn Đình', 'Trí', 'Nam', '2015-06-22', '089015007890', '0917789012', 'Xã Mỹ Hòa Hưng, TP. Long Xuyên, An Giang', 'TE4890078901234', 'B', 'Không'),
('BN008', 'Nguyễn Hoàng', 'Thiện', 'Nữ', '1973-12-30', '089173008901', '0948890123', 'Thị trấn Núi Sập, Huyện Thoại Sơn, An Giang', 'GD4890089012345', 'O', 'Đau dạ dày mạn tính');

-- Dữ liệu Phiếu khám
INSERT INTO phieukham (mapk, mabn, manv_bacsi, makhoa, ngaykham, trieuchung, huyetap, nhiptim, cannang, chandoan, ketluan, trangthai) VALUES
('PK001', 'BN001', 'NV02', 'K02', '2026-11-01 08:30:00', 'Sốt nhẹ, ho khan, đau rát họng 3 ngày', '120/80', 78, 65.5, 'Viêm họng cấp', 'Uống thuốc theo toa, nghỉ ngơi, uống nhiều nước', 'Đã thanh toán'),
('PK002', 'BN003', 'NV02', 'K06', '2026-11-02 09:15:00', 'Chóng mặt, đau đầu vùng gáy', '150/95', 85, 72.0, 'Tăng huyết áp độ 1', 'Duy trì thuốc hạ áp hàng ngày, tái khám sau 1 tháng', 'Đã thanh toán'),
('PK003', 'BN005', 'NV02', 'K02', '2026-11-03 10:00:00', 'Đầy hơi, ợ chua, đau rát thượng vị', '125/82', 74, 68.0, 'Viêm loét dạ dày tá tràng', 'Uống thuốc trước bữa ăn, kiêng đồ chua cay', 'Đã thanh toán');

-- Dữ liệu Toa thuốc chi tiết
INSERT INTO toathuoc_chitiet (id, mapk, mathuoc, tenthuoc, donvitinh, soluong, dongia, cachdung, thanhtien) VALUES
(1, 'PK001', 'T01', 'Paracetamol 500mg', 'Viên', 10, 1500.00, 'Uống 1 viên khi sốt > 38.5 độ', 15000.00),
(2, 'PK001', 'T02', 'Amoxicillin 500mg', 'Viên', 14, 3500.00, 'Uống 1 viên x 2 lần/ngày sau ăn', 49000.00),
(3, 'PK001', 'T08', 'Vitamin C 500mg', 'Hộp', 1, 45000.00, 'Uống 1 viên/ngày vào buổi sáng', 45000.00),
(4, 'PK002', 'T09', 'Amlodipine 5mg', 'Hộp', 1, 85000.00, 'Uống 1 viên mỗi sáng', 85000.00),
(5, 'PK003', 'T05', 'Omeprazole 20mg', 'Hộp', 1, 65000.00, 'Uống 1 viên trước ăn sáng 30p', 65000.00);

-- Dữ liệu Hóa đơn viện phí
INSERT INTO hoadon_vienphi (mahd, mapk, ngaylap, tienkham, tienthuoc, giamtru_bhyt, tongtien, trangthai, nguoithu) VALUES
('HD001', 'PK001', '2026-11-01 09:10:00', 100000.00, 109000.00, 41800.00, 167200.00, 'Đã thanh toán', 'Lê Minh Triết'),
('HD002', 'PK002', '2026-11-02 09:45:00', 100000.00, 85000.00, 37000.00, 148000.00, 'Đã thanh toán', 'Lê Minh Triết'),
('HD003', 'PK003', '2026-11-03 10:40:00', 100000.00, 65000.00, 33000.00, 132000.00, 'Đã thanh toán', 'Lê Minh Triết');

