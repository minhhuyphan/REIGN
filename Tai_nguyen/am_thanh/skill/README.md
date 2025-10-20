# 🎵 Skill Sounds

## 📁 Thư Mục Âm Thanh Skill

Thư mục này chứa các file âm thanh cho kỹ năng (skills) của các nhân vật.

## 📝 Cách Thêm Âm Thanh Cho Skill

### Bước 1: Chuẩn Bị File Âm Thanh

**Định dạng hỗ trợ**:
- `.mp3` (khuyến nghị) - kích thước nhỏ
- `.wav` - chất lượng cao nhưng file lớn
- `.ogg` - cân bằng giữa chất lượng và kích thước

**Đặt tên file**:
```
skill_chien_than.mp3    → Âm thanh cho skill Chiến Thần Lạc Hồng
skill_ten_khac.mp3      → Âm thanh cho skill khác
```

### Bước 2: Copy File Vào Đây

```
Tai_nguyen/
  am_thanh/
    skill/
      skill_chien_than.mp3  ← ĐẶT FILE ÂM THANH VÀO ĐÂY
      skill_khac.mp3
      ...
```

### Bước 3: Hệ Thống Tự Động Load

Không cần code thêm! `SkillVideoPlayer` sẽ tự động:
1. Tìm file âm thanh với tên tương ứng video
2. Phát audio đồng thời với video
3. Nếu không có file audio → chỉ phát video (không lỗi)

## 🎯 Ví Dụ: Skill Chiến Thần Lạc Hồng

**File cần**:
```
Tai_nguyen/
  video/
    skill_chien_than.mp4   ← Video (đã có)
  am_thanh/
    skill/
      skill_chien_than.mp3 ← Audio (THÊM FILE NÀY)
```

**Hệ thống sẽ**:
- Phát `skill_chien_than.mp4` (video)
- Đồng thời phát `skill_chien_than.mp3` (audio)
- Sync hoàn hảo!

## 🔧 Khuyến Nghị Kỹ Thuật

### Thời Lượng
- Âm thanh nên **cùng độ dài** với video (hoặc ngắn hơn 1 chút)
- Video skill: 8 giây → Audio nên: 7-8 giây

### Chất Lượng
- **Bitrate**: 128-192 kbps (MP3)
- **Sample rate**: 44100 Hz
- **Channels**: Stereo hoặc Mono

### Kích Thước File
- Mục tiêu: < 500KB cho 8 giây
- MP3 128kbps ~= 128KB cho 8 giây ✅

## 🎮 Testing

### Test Nhanh
```bash
# Thêm file skill_chien_than.mp3 vào thư mục này
# Sau đó chạy:
python demo_skill_video.py
```

### Test In-Game
```bash
python ma_nguon/main.py
# Chọn Chiến Thần Lạc Hồng
# Vào map → Nhấn F
# Nghe audio + xem video!
```

## 📊 Danh Sách File

### Hiện Tại
- ❌ `skill_chien_than.mp3` - **CHƯA CÓ** (cần thêm)

### Tương Lai (khi có thêm skills)
- ⏳ `skill_khac.mp3` - Skill khác
- ⏳ ...

---

**Lưu ý**: Nếu không có file audio, video vẫn phát bình thường (không lỗi)
