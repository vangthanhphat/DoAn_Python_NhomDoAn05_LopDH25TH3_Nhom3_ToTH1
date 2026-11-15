@echo off
chcp 65001 >nul
title ĐÓNG GÓI NỘP BÀI - CHUYÊN ĐỀ PYTHON (COS525)
color 0A

echo ==============================================================
echo        ĐÓNG GÓI ĐỒ ÁN QUẢN LÝ BỆNH NHÂN ĐỂ NỘP BÀI
echo     GVHD: ThS. Nguyễn Ngọc Minh
echo     SVTH: Văng Thành Phát (DTH245849) - Lê Minh Triết (DTH245928)
echo ==============================================================
echo.

set ROOT_DIR=%~dp0..
set ZIP_NAME=DTH245849.VangThanhPhat.DH25TH3_Nhom01_To01.zip
set DEST_ZIP=%ROOT_DIR%\..\%ZIP_NAME%

echo Đang nén toàn bộ thư mục đồ án thành file ZIP chuẩn...
powershell -Command "Compress-Archive -Path '%ROOT_DIR%\*' -DestinationPath '%DEST_ZIP%' -Force"

if exist "%DEST_ZIP%" (
    echo.
    echo ==============================================================
    echo [THÀNH CÔNG] Đã tạo file zip nộp bài tại:
    echo %DEST_ZIP%
    echo ==============================================================
) else (
    echo.
    echo [LỖI] Không thể tạo file zip!
)
echo.
pause
