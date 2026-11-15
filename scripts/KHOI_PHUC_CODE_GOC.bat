@echo off
chcp 65001 >nul
title KHOI PHUC CODE GOC - QUAN LY BENH NHAN

echo =====================================================================
echo                 TIEN ICH KHOI PHUC CODE GOC
echo =====================================================================
echo.
echo Ban co chac chan muon huy moi thay doi va quay ve ban goc chuan?
echo.
set /p confirm="Nhap Y de dong y khoi phuc, hoac nhan phim bat ky de huy: "
if /i not "%confirm%"=="Y" goto cancel

echo.
echo Dang tien hanh khoi phuc code ve trang thai goc...
cd /d "%~dp0.."
git restore .
git clean -fd

echo.
echo =====================================================================
echo [THANH CONG] Toan bo code da duoc khoi phuc ve trang thai chuan!
echo =====================================================================
echo.
pause
exit /b

:cancel
echo.
echo Da huy thao tac khoi phuc. Code hien tai duoc giu nguyen!
pause
exit /b
