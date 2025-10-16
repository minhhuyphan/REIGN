# Hướng Dẫn Auto-Login (Tự Động Đăng Nhập)

## 📋 Tổng Quan
Tính năng Auto-Login cho phép người chơi không phải đăng nhập lại mỗi khi mở game. Session sẽ được lưu và tự động khôi phục khi khởi động game.

## 🎯 Tính Năng

### 1. **Tự Động Đăng Nhập**
- Khi đăng nhập thành công, session được lưu vào `du_lieu/save/session.json`
- Lần sau mở game, tự động vào Menu (bỏ qua màn hình Login)
- Hiển thị tên người chơi và số vàng ở góc phải trên Menu

### 2. **Đăng Xuất**
- Trong Menu có option "Đăng xuất" (chỉ hiện khi đã đăng nhập)
- Click "Đăng xuất" sẽ:
  - Xóa session
  - Quay về màn hình Login
  - Lần sau mở game sẽ phải đăng nhập lại

### 3. **Menu Động**
- **Khi chưa đăng nhập**: Menu có 11 options (không có "Đăng xuất")
- **Khi đã đăng nhập**: Menu có 12 options (có "Đăng xuất" và "Thoát" riêng)

## 🔧 Cách Thức Hoạt Động

### File Liên Quan:
1. **`ma_nguon/core/quan_ly_game.py`**
   - Khởi tạo game
   - Load session khi start
   - Auto-login nếu có session

2. **`ma_nguon/tien_ich/user_store.py`**
   - `save_current_user(username)`: Lưu session
   - `load_current_user()`: Đọc session
   - `clear_session()`: Xóa session (logout)

3. **`ma_nguon/man_choi/login.py`**
   - Sau khi login thành công, gọi `save_current_user()`

4. **`ma_nguon/man_choi/menu.py`**
   - Hiển thị tên user và số vàng
   - Option "Đăng xuất" (chỉ khi đã login)

### Flow Auto-Login:

```
Mở Game
   ↓
Đọc session.json
   ↓
Có username?
   ├─ CÓ → Load profile → Vào Menu (skip Login)
   └─ KHÔNG → Hiển thị màn hình Login
```

### Flow Logout:

```
Click "Đăng xuất" trong Menu
   ↓
Xóa session.json
   ↓
Set current_user = None
   ↓
Quay về màn hình Login
```

## 📁 File Session

**Vị trí**: `du_lieu/save/session.json`

**Format**:
```json
{
  "current_user": "username_của_bạn"
}
```

**Lưu ý**:
- File này tự động tạo khi đăng nhập thành công
- Tự động xóa khi đăng xuất
- Có thể xóa thủ công nếu muốn force logout

## 🎮 Hướng Dẫn Sử Dụng

### Đăng Nhập Lần Đầu:
1. Mở game → Màn hình Login
2. Nhập username và password
3. Click "Đăng nhập" hoặc nhấn Enter
4. Vào Menu

### Mở Game Lần Sau:
1. Mở game → **Tự động vào Menu** (không cần login)
2. Thấy tên bạn ở góc phải trên
3. Chơi game bình thường

### Đăng Xuất:
1. Trong Menu, dùng ↓ di chuyển đến "Đăng xuất"
2. Nhấn Enter
3. Quay về màn hình Login
4. Lần sau phải đăng nhập lại

### Đổi Tài Khoản:
1. Đăng xuất tài khoản hiện tại
2. Đăng nhập bằng tài khoản khác
3. Session mới được lưu

## 🔒 Bảo Mật

### Hiện Tại:
- ✅ Password được hash bằng PBKDF2-HMAC-SHA256
- ✅ Salt ngẫu nhiên cho mỗi user
- ✅ Session chỉ lưu username (không lưu password)

### Lưu Ý An Toàn:
- **KHÔNG** share file `users.json` (chứa hash password)
- **KHÔNG** share file `session.json` nếu dùng máy công cộng
- Nếu muốn logout hoàn toàn, click "Đăng xuất" trước khi tắt game

## 🐛 Troubleshooting

### Game không tự động login dù đã đăng nhập trước:
- **Nguyên nhân**: File `session.json` bị xóa hoặc corrupt
- **Giải pháp**: Đăng nhập lại, hệ thống sẽ tạo session mới

### Muốn force logout mà game đang tắt:
- Xóa file: `du_lieu/save/session.json`
- Mở game lại sẽ hiện màn hình Login

### Muốn xóa tất cả dữ liệu user:
- Xóa file: `du_lieu/save/users.json`
- Xóa file: `du_lieu/save/session.json`
- Xóa file: `du_lieu/save/profiles.json`
- Mở game → Đăng ký tài khoản mới

## 📊 Thống Kê Hiển Thị

Menu hiển thị:
- **Người chơi**: Tên username đang đăng nhập
- **Vàng**: Số vàng hiện có (từ profile)
- **Chưa đăng nhập**: Nếu chưa login

Vị trí: Góc phải trên màn hình Menu

## ✨ Tính Năng Tương Lai (Có Thể Thêm)

- [ ] Option "Ghi nhớ đăng nhập" (checkbox)
- [ ] Auto-logout sau X ngày không chơi
- [ ] Multi-session (nhiều users cùng lúc)
- [ ] Encrypted session file
- [ ] Login bằng email/token

---

**Tác giả**: REIGN Game Development Team  
**Ngày cập nhật**: 16/10/2025  
**Phiên bản**: 1.0
