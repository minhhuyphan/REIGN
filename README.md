# REIGN

Game nhập vai hành động với hệ thống chiến đấu và trang bị phong phú.

## Tính Năng Chính

- **Nhiều nhân vật**: Chiến binh, Ninja, Thợ săn quái vật, Võ sĩ, và nhiều nhân vật khác
- **Nhiều map**: Map mùa thu, Map công nghệ, Map ninja, Map rừng linh vực
- **Hệ thống trang bị**: Trang bị vũ khí và giáp để tăng sức mạnh
- **Chiến đấu động**: Đánh, đá, phòng thủ, và nhảy
- **Shop**: Mua thuốc và trang bị
- **Hệ thống profile**: Lưu tiến trình và trang bị của từng người chơi
- **Auto-Login**: Tự động đăng nhập khi mở lại game (không cần nhập password lại)

## Hướng Dẫn Cài Đặt

1. Cài đặt Python 3.7+
2. Cài đặt pygame:
   ```bash
   pip install pygame
   ```
3. Chạy game:
   ```bash
   python ma_nguon/main.py
   ```

## Hệ Thống Trang Bị

Xem hướng dẫn chi tiết tại [Equipment_Guide.md](tai_lieu/Equipment_Guide.md)

### Các Trang Bị Có Sẵn

1. **Cung Băng Lãm** (Công): +8 Công, làm chậm địch
2. **Kiếm Rồng** (Công): +10 Công, thiêu đốt 1 HP/giây trong 30s
3. **Giáp Ánh Sáng** (Thủ): +200 HP, hồi sinh với 50% HP
4. **Giày Thiên Thần** (Tốc Độ): +2 Tốc độ, +50 HP

### Cách Sử Dụng

1. Từ menu chính, chọn "Trang bị"
2. Click vào trang bị trong kho đồ để chọn
3. Click vào slot tương ứng (Công/Thủ/Tốc Độ) để trang bị
4. Nhấn ESC hoặc E để quay lại

## Phím Điều Khiển

### Mặc Định
- **←/→**: Di chuyển trái/phải
- **↑**: Nhảy
- **Z**: Đánh
- **X**: Đá
- **C**: Phòng thủ
- **N**: Dùng thuốc HP
- **M**: Dùng thuốc MP
- **E**: Mở màn hình trang bị (trong game)
- **ESC**: Thoát/Quay lại

### Tùy Chỉnh
Vào menu "Cài đặt" để thay đổi phím điều khiển

## Tài Liệu

- [Action Button Guide](tai_lieu/Action_Button_Guide.md) - Hướng dẫn nút hành động
- [Settings Guide](tai_lieu/Huong_dan_Settings.md) - Hướng dẫn cài đặt
- [Equipment Guide](tai_lieu/Equipment_Guide.md) - Hướng dẫn hệ thống trang bị

## Cấu Trúc Dự Án

```
REIGN/
├── ma_nguon/           # Mã nguồn chính
│   ├── core/          # Quản lý game, settings, profile
│   ├── doi_tuong/     # Character, monsters, items, equipment
│   ├── giao_dien/     # UI components
│   ├── man_choi/      # Game scenes/levels
│   └── tien_ich/      # Utilities (user_store cho login/session)
├── Tai_nguyen/        # Assets (images, sounds, fonts)
│   ├── hinh_anh/
│   │   ├── nhan_vat/
│   │   ├── quai_vat/
│   │   └── trang_bi/  # Equipment images
│   ├── am_thanh/
│   └── font/
├── du_lieu/           # Game data (saves, settings, session)
│   └── save/
│       ├── users.json      # User accounts (hashed passwords)
│       ├── profiles.json   # User profiles & equipment
│       ├── session.json    # Current logged-in user (auto-login)
│       └── settings.json   # Game settings
└── tai_lieu/          # Documentation
    ├── Equipment_Guide.md
    ├── Huong_dan_Auto_Login.md  # Auto-login documentation
    └── ...
```

## Tài Liệu

- [Hướng dẫn Trang bị](tai_lieu/Equipment_Guide.md)
- [Hướng dẫn Auto-Login](tai_lieu/Huong_dan_Auto_Login.md)
- [Hướng dẫn Settings](tai_lieu/Huong_dan_Settings.md)
- [Hướng dẫn Action Buttons](tai_lieu/Action_Button_Guide.md)

## License

Dự án này thuộc về minhhuyphan.
