# 🎮 HƯỚNG DẪN SỬ DỤNG ĐỒNG BỘ TRANG BỊ

## 📖 Hướng Dẫn Nhanh

### Bước 1: Mở Equipment Scene
```
Menu Chính → Chọn "Trang bị"
```
![Equipment Scene](Bạn sẽ thấy màn hình trang bị)

### Bước 2: Chọn Nhân Vật
```
Click nút "Chọn Nhân Vật" → Chọn nhân vật muốn trang bị
```
**5 Nhân Vật Có Sẵn:**
- 🗡️ Chiến Binh
- 🥷 Ninja
- 🥊 Võ Sĩ
- ⚔️ Chiến Thần Lạc Hồng
- 🏹 Thợ Săn Quái Vật

### Bước 3: Lắp Trang Bị
```
Click vào item trong Inventory → Item được lắp vào slot tương ứng
```

**Các Trang Bị Có Sẵn:**

#### 🗡️ Vũ Khí (Weapon Slot)
- **Cung Băng Lam**: +8 Damage, Hiệu ứng làm chậm
- **Kiếm Rồng**: +10 Damage, Hiệu ứng burn

#### 🛡️ Giáp (Armor Slot)
- **Giáp Ánh Sáng**: +200 HP, Hiệu ứng hồi sinh 1 lần

#### 👟 Giày (Boots Slot)
- **Giày Thiên Thần**: +2 Speed, +50 HP

### Bước 4: Gỡ Trang Bị (Tùy Chọn)
```
Click vào item đã lắp → Item quay về Inventory
```

### Bước 5: Chơi Game
```
ESC → Quay lại Menu → Chọn "Chơi"
Chọn màn chơi → Chọn nhân vật (cùng nhân vật đã trang bị)
```

## ✨ Tính Năng Đặc Biệt

### 🔄 Tự Động Đồng Bộ
- Trang bị được **lưu tự động** khi lắp/gỡ
- Khi chọn nhân vật để chơi, trang bị **tự động được áp dụng**
- **Mỗi nhân vật** có bộ trang bị riêng

### 📊 Preview Stats
- Hover chuột lên item để xem **thông tin chi tiết**
- Stats nhân vật **tự động cập nhật** khi lắp trang bị
- Xem **chỉ số tăng thêm** từ trang bị

## 🎯 Ví Dụ Thực Tế

### Scenario 1: Tăng Sức Mạnh Cho Ninja

**Trước khi trang bị:**
- HP: 800
- Damage: 35
- Speed: 7

**Lắp trang bị:**
1. Kiếm Rồng (Weapon)
2. Giáp Ánh Sáng (Armor)
3. Giày Thiên Thần (Boots)

**Sau khi trang bị:**
- HP: 1,050 (800 + 200 + 50)
- Damage: 45 (35 + 10)
- Speed: 9 (7 + 2)
- **Bonus**: Burn effect, Revive 1 lần

### Scenario 2: Build Chiến Binh Tank

**Mục tiêu**: Tăng HP và phòng thủ

**Trang bị:**
1. Cung Băng Lam (Weapon) - Slow enemies
2. Giáp Ánh Sáng (Armor) - +200 HP + Revive
3. Giày Thiên Thần (Boots) - +50 HP + Speed

**Kết quả:**
- Base HP: 1,000
- Total HP: 1,250
- Hiệu ứng: Slow + Revive

## 💾 Lưu Trữ

### Tự Động Lưu
- Mỗi khi lắp/gỡ trang bị → **Tự động lưu**
- Không cần nhấn nút "Save"
- File lưu: `du_lieu/save/character_equipment.json`

### Kiểm Tra Dữ Liệu Đã Lưu
```
Mở file: du_lieu/save/character_equipment.json
```

**Ví dụ nội dung:**
```json
{
  "ninja": {
    "weapon": "kiem_rong",
    "armor": "giap_anh_sang",
    "boots": "giay_thien_than"
  },
  "chien_binh": {
    "weapon": null,
    "armor": "giap_anh_sang",
    "boots": null
  }
}
```

## 🎮 Phím Tắt

| Phím | Chức Năng |
|------|-----------|
| **ESC** | Quay lại Menu |
| **Left Click** | Lắp/Gỡ trang bị |
| **Hover** | Xem thông tin item |

## 🔍 Troubleshooting

### ❓ Trang bị không được lưu?
**Giải pháp**: Đảm bảo đã chọn nhân vật trước khi lắp trang bị

### ❓ Nhân vật không có trang bị khi chơi?
**Giải pháp**: 
1. Kiểm tra đã chọn **đúng nhân vật** trong Equipment Scene
2. Chọn **cùng nhân vật đó** trong Character Select

### ❓ Stats không đúng?
**Giải pháp**: 
1. Hover lên item để xem bonus stats
2. Kiểm tra panel "Chỉ Số Nhân Vật" bên phải

### ❓ Item biến mất?
**Giải pháp**: 
- Item không biến mất, chỉ được lắp vào slot
- Click vào slot để gỡ item về inventory

## 📈 Tips & Tricks

### 🎯 Build Recommendations

**1. Speed Build (Ninja + Thợ Săn)**
```
- Giày Thiên Thần (Boots): +2 Speed
- Focus: Dodge và hit-and-run
```

**2. Tank Build (Chiến Binh + Võ Sĩ)**
```
- Giáp Ánh Sáng (Armor): +200 HP + Revive
- Giày Thiên Thần (Boots): +50 HP
- Total bonus: +250 HP
```

**3. Damage Build (All)**
```
- Kiếm Rồng (Weapon): +10 Damage + Burn
- Cung Băng Lam (Weapon): +8 Damage + Slow
```

### 💡 Strategy Tips

1. **Chiến Thần Lạc Hồng**: Đã mạnh, chỉ cần thêm Giáp Ánh Sáng cho Revive
2. **Ninja**: Cần thêm HP → Ưu tiên Giáp và Giày
3. **Võ Sĩ**: Đã có HP cao → Ưu tiên Damage
4. **Thợ Săn**: Balanced → Lắp full bộ 3 items

## 🎊 Kết Luận

**Hệ thống trang bị giúp bạn:**
- ✅ Tăng sức mạnh nhân vật
- ✅ Customize build theo phong cách chơi
- ✅ Unlock special effects
- ✅ Tự động lưu và đồng bộ

**Chúc bạn chơi game vui vẻ!** 🎮

---

## 📞 Support

Nếu gặp vấn đề, xem tài liệu chi tiết:
- `tai_lieu/Equipment_Synchronization_Guide.md` - Hướng dẫn kỹ thuật
- `tai_lieu/Equipment_System_Guide.md` - Hướng dẫn hệ thống
- `EQUIPMENT_SYNC_COMPLETE.md` - Tóm tắt

Hoặc chạy test để kiểm tra:
```bash
python test_equipment_sync.py
```
