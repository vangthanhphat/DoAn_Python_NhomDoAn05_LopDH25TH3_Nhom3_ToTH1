@echo off
chcp 65001 >nul
title KHÔI PHỤC CODE GỐC - QUẢN LÝ BỆNH NHÂN

echo =====================================================================
echo         TIỆN ÍCH KHÔI PHỤC CODE GỐC CHUẨN (CHECKPOINT)
echo =====================================================================
echo.
echo Bạn có chắc chắn muốn hủy mọi thay đổi đang sửa và quay về bản gốc chuẩn?
echo.
set /p confirm="Nhập 'Y' để đồng ý khôi phục, hoặc nhấn phím khác để hủy: "
if /i "%confirm%" neq "Y" (
    echo.
    echo Đã hủy thao tác khôi phục. Code hiện tại được giữ nguyên!
    pause
    exit /b
)

echo.
echo Đang tiến hành khôi phục code từ Checkpoint Git gốc...

cd /d "%~dp0.."
git restore .
git clean -fd

echo.
echo =====================================================================
echo [THÀNH CÔNG] Toàn bộ code đã được khôi phục về trạng thái chuẩn ban đầu!
echo Bạn có thể yên tâm tiếp tục thực hành, sửa code thoải mái.
echo =====================================================================
echo.
pause
