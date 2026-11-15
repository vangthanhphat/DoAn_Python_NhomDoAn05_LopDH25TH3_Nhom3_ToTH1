@echo off
chcp 65001 >nul
title DONG BO VA DAY CODE LEN GITHUB
color 0A

echo =======================================================
echo     TỰ ĐỘNG ĐẨY TOÀN BỘ DỰ ÁN LÊN GITHUB (GIT PUSH)
echo =======================================================
echo.

cd /d "%~dp0.."

echo [1/3] Kiểm tra các tệp đã sửa đổi...
git status -s

set /p msg="Nhập nội dung cập nhật (Bấm Enter để dùng mặc định: 'Cap nhat do an'): "
if "%msg%"=="" set msg=Cap nhat do an

echo.
echo [2/3] Đang thêm tệp và commit...
git add -A
git commit -m "%msg%"

echo.
echo [3/3] Đang đẩy lên GitHub (git push origin main)...
git push origin main

echo.
echo =======================================================
echo    ĐÃ ĐỒNG BỘ LÊN GITHUB THÀNH CÔNG!
echo =======================================================
echo.
pause
