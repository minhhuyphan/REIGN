# Hướng dẫn sử dụng hệ thống Settings

## Tổng quan
Hệ thống Settings trong game REIGN cung cấp các tính năng tùy chỉnh đầy đủ như các game 2D chuyên nghiệp hiện đại.

## Các tính năng chính

### 1. Audio Settings (Cài đặt âm thanh)
- **Master Volume**: Điều chỉnh âm lượng tổng thể của game (0-100%)
- **Music Volume**: Điều chỉnh âm lượng nhạc nền (0-100%)
- **SFX Volume**: Điều chỉnh âm lượng hiệu ứng âm thanh (0-100%)

### 2. Video Settings (Cài đặt hình ảnh)
- **Resolution**: Chọn độ phân giải màn hình
  - 800x600 (4:3)
  - 1024x768 (4:3)
  - 1280x720 (16:9)
  - 1920x1080 (16:9)
- **Fullscreen**: Bật/tắt chế độ toàn màn hình
- **VSync**: Đồng bộ hóa dọc để giảm screen tearing

### 3. Controls (Điều khiển)
Tùy chỉnh phím điều khiển cho nhân vật:
- **Move Left**: Di chuyển sang trái (mặc định: A)
- **Move Right**: Di chuyển sang phải (mặc định: D)
- **Jump**: Nhảy (mặc định: W)
- **Attack**: Tấn công bằng tay (mặc định: J)
- **Kick**: Tấn công bằng chân (mặc định: K)
- **Defend**: Phòng thủ (mặc định: S)

#### Cách thay đổi phím:
1. Click vào nút hiển thị phím hiện tại
2. Nhấn phím mới mà bạn muốn sử dụng
3. Phím sẽ được cập nhật ngay lập tức

### 4. Graphics (Đồ họa)
- **Graphics Quality**: Chất lượng đồ họa
  - Low: Hiệu suất cao, chất lượng thấp
  - Medium: Cân bằng giữa hiệu suất và chất lượng
  - High: Chất lượng cao, hiệu suất trung bình
  - Ultra: Chất lượng tối đa, yêu cầu máy mạnh
- **Particle Effects**: Bật/tắt hiệu ứng hạt
- **Shadows**: Bật/tắt hiệu ứng bóng đổ
- **Visual Effects**: Bật/tắt các hiệu ứng hình ảnh đặc biệt

### 5. Gameplay (Lối chơi)
- **Language**: Chọn ngôn ngữ
  - English
  - Vietnamese
  - Japanese
  - Korean

## Cách sử dụng

### Truy cập Settings
1. Từ menu chính, sử dụng phím mũi tên ↑↓ để chọn "Cài đặt"
2. Nhấn Enter để vào màn hình Settings

### Điều hướng trong Settings
- **← →**: Chuyển đổi giữa các tab (Audio, Video, Controls, Graphics, Gameplay)
- **Mouse**: Click để thay đổi các thiết lập
- **ESC**: Quay lại menu chính

### Các nút chức năng
- **BACK**: Lưu settings và quay lại menu
- **RESET**: Khôi phục tất cả settings về mặc định
- **APPLY**: Áp dụng các thay đổi ngay lập tức

## Lưu trữ Settings
- Settings được lưu tự động vào file `du_lieu/save/settings.json`
- Các thay đổi được áp dụng ngay lập tức khi bạn thực hiện
- Settings được load tự động khi khởi động game

## Tính năng nâng cao

### Volume Control
- Master Volume ảnh hưởng đến tất cả âm thanh trong game
- Music Volume và SFX Volume được tính dựa trên Master Volume
- Công thức: Final Volume = Master Volume × Specific Volume

### Key Binding System
- Hệ thống binding phím linh hoạt, cho phép gán bất kỳ phím nào
- Không thể gán cùng một phím cho nhiều hành động
- Các phím đặc biệt như ESC, F-keys vẫn có thể được sử dụng

### Graphics Quality
- Low Quality: Scale hình ảnh xuống 50%
- Medium Quality: Scale hình ảnh xuống 75%
- High Quality: Kích thước gốc (100%)
- Ultra Quality: Scale hình ảnh lên 125%

## Khắc phục sự cố

### Settings không được lưu
- Kiểm tra quyền ghi file trong thư mục game
- Đảm bảo thư mục `du_lieu/save` tồn tại

### Phím điều khiển không hoạt động
- Vào Settings → Controls để kiểm tra key bindings
- Click nút RESET để khôi phục controls mặc định

### Âm thanh không có
- Kiểm tra Master Volume và SFX/Music Volume
- Đảm bảo file âm thanh tồn tại trong thư mục `tai_nguyen/am_thanh`

### Hiệu suất game giảm
- Giảm Graphics Quality xuống Low hoặc Medium
- Tắt Particle Effects, Shadows, và Visual Effects
- Giảm độ phân giải màn hình

## Ghi chú kỹ thuật
- Settings sử dụng định dạng JSON để lưu trữ
- Hệ thống Settings Manager quản lý việc load/save/apply settings
- Tích hợp với Pygame mixer để điều khiển âm thanh
- Hỗ trợ hot-reload settings mà không cần restart game

## Phiên bản và cập nhật
- Phiên bản hiện tại: 1.0
- Tương thích với Python 3.7+
- Yêu cầu Pygame 2.0+