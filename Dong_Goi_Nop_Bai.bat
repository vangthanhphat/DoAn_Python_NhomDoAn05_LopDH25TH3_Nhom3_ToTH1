@echo off
title DONG GOI NOP BAI - CHUYEN DE PYTHON (COS525)
color 0A
echo ==============================================================
echo        DONG GOI DO AN QUAN LY BENH NHAN DE NOP BAI
echo     GVHD: ThS. Nguyen Ngoc Minh - SVTH: Vang Thanh Phat
echo                  MSSV: DTH245849 - LOP: DH25TH3
echo ==============================================================
echo.
echo Dang nen thu muc thanh file zip...

set ZIP_NAME=DTH245849.VangThanhPhat.DH25TH3_Nhom01_To01.zip
set SRC_DIR=d:\chuyen de python\QuanLyBenhNhan
set DEST_ZIP=d:\chuyen de python\%ZIP_NAME%

powershell -Command "Compress-Archive -Path '%SRC_DIR%' -DestinationPath '%DEST_ZIP%' -Force"

if exist "%DEST_ZIP%" (
    echo.
    echo ==============================================================
    echo [THANH CONG] Da dong goi file zip nop bai tai:
    echo %DEST_ZIP%
    echo ==============================================================
) else (
    echo.
    echo [LOI] Khong the tao file zip!
)
echo.
pause

