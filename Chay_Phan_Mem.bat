@echo off
title PHAN MEM QUAN LY BENH NHAN - KHOA CNTT DH AN GIANG
color 0B
echo ==============================================================
echo        HE THONG QUAN LY BENH NHAN VA KHAM CHUA BENH
echo             HOC PHAN: CHUYEN DE PYTHON (COS525)
echo     GVHD: ThS. Nguyen Ngoc Minh - SVTH: Vang Thanh Phat
echo ==============================================================
echo.
echo Dang kiem tra va khoi dong ung dung...
python QLBN.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [LOI] Khong the khoi chay! Vui long kiem tra:
    echo 1. Ban da bat MySQL trong XAMPP chua?
    echo 2. Ban da cai dat cac thu vien trong requirements.txt chua?
    echo.
    pause
)

