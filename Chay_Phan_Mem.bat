@echo off
chcp 65001 >nul
title HỆ THỐNG QUẢN LÝ BỆNH NHÂN - KHOA CNTT ĐH AN GIANG
color 0B

echo ==============================================================
echo        HỆ THỐNG QUẢN LÝ BỆNH NHÂN VÀ PHÒNG KHÁM ĐA KHOA
echo             HỌC PHẦN: CHUYÊN ĐỀ PYTHON (COS525)
echo     GVHD: ThS. Nguyễn Ngọc Minh
echo     SVTH: Văng Thành Phát (DTH245849) - Lê Minh Triết (DTH245928)
echo ==============================================================
echo.
echo [*] Đang khởi động ứng dụng...

cd /d "%~dp0src"
python QLBN.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [LỖI] Không thể khởi chạy! Vui lòng kiểm tra:
    echo 1. Bạn đã BẬT MySQL trong bảng điều khiển XAMPP chưa?
    echo 2. Đã cài đặt thư viện cần thiết chưa: pip install -r requirements.txt
    echo.
    pause
)
