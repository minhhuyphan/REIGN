@echo off
REM ===== AUTO PUSH SCRIPT CHO NHÓM REIGN =====
REM Tạo bởi: Tai
REM Mục đích: Tự động push code lên GitHub

echo.
echo 🚀 ===== REIGN GAME - AUTO PUSH TO GITHUB =====
echo 👤 Author: Tai
echo 📅 Date: %date% %time%
echo.

echo ⏳ Đang kiểm tra Git status...
git status

echo.
echo ⏳ Đang thêm tất cả files vào staging...
git add .

echo.
set /p commit_msg="💬 Nhập commit message (hoặc Enter để dùng default): "
if "%commit_msg%"=="" set commit_msg=🎮 Update REIGN game - Team collaboration

echo.
echo ⏳ Đang commit với message: "%commit_msg%"
git commit -m "%commit_msg%"

echo.
echo ⏳ Đang pull updates mới nhất từ GitHub...
git pull origin main

echo.
echo ⏳ Đang push lên GitHub...
git push origin main

echo.
echo ✅ ===== HOÀN THÀNH! =====
echo 🎯 Code đã được push lên GitHub thành công!
echo 🔗 Repository: https://github.com/minhhuyphan/REIGN
echo 👥 Team members có thể pull về để lấy updates mới nhất
echo.

echo ⏳ Script sẽ tự động đóng sau 10 giây...
timeout /t 10 /nobreak >nul