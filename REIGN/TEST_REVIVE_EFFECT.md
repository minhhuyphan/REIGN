# 🎮 HƯỚNG DẪN TEST HIỆU ỨNG HỒI SINH

## 🎯 Giáp Ánh Sáng - Revive Effect

**Hiệu ứng**: Hồi sinh 1 lần với 50% HP khi nhân vật chết

---

## 📋 CÁCH TEST NHANH (5 phút)

### Option 1: Test với Ninja (Nhanh nhất!)

Ninja đã có **Giáp Ánh Sáng** sẵn trong file save!

#### Bước 1: Chạy game
```bash
cd D:\GamePygame\REIGN\REIGN
python -m ma_nguon.main
```

#### Bước 2: Vào game
1. Chọn **Level 1** (hoặc màn nào cũng được)
2. Chọn nhân vật **Ninja**
3. Nhấn ENTER vào game

#### Bước 3: Test revive
1. **Đứng yên để quái đánh** cho đến khi HP = 0
2. **Quan sát**:
   - Console sẽ in: `[Equipment] ... revived with XXX HP!`
   - HP bar sẽ hồi phục lên ~50% (từ 0 → 300/600)
   - Nhân vật tiếp tục sống!

#### Bước 4: Test revive chỉ 1 lần
1. Tiếp tục để quái đánh đến chết lần 2
2. **Quan sát**: Lần này nhân vật sẽ chết thật (không revive)

---

### Option 2: Test với nhân vật khác

#### Bước 1: Trang bị Giáp Ánh Sáng
1. Chạy game
2. Nhấn **E** để vào Equipment Scene
3. Chọn nhân vật (ví dụ: Chiến Binh)
4. Click **Giáp Ánh Sáng** trong Inventory
5. Click vào **Armor slot** để trang bị
6. Nhấn ESC về Menu

#### Bước 2-4: Giống Option 1

---

## 🔍 Dấu Hiệu Thành Công

### ✅ Console Messages
Khi test, bạn PHẢI thấy messages này:

```
# Khi trang bị (trong Equipment Scene)
[Equipment] Giáp Ánh Sáng revive effect enabled!

# Khi vào game (Character Select)
[CharacterSelect] Created character: Ninja (ID: ninja) with equipment
  Stats: HP=600, DMG=35, SPD=10, DEF=10

# Khi chết lần 1
[Equipment] tai_nguyen/hinh_anh/nhan_vat/ninja revived with 300 HP!

# Khi chết lần 2 - KHÔNG có message revive
```

### ✅ Hiện Tượng Trong Game

#### Lần chết thứ 1 (Revive):
- HP giảm về 0
- **HP bar bỗng nhiên hồi lại 50%** (ví dụ: 0 → 300/600)
- Nhân vật **KHÔNG vào animation chết**
- Nhân vật tiếp tục đứng/chiến đấu bình thường
- Console có message revive

#### Lần chết thứ 2 (Không revive):
- HP giảm về 0
- Nhân vật **vào animation chết** (nga)
- HP bar = 0/600
- Màn hình Game Over
- Console KHÔNG có message revive

---

## 📊 So Sánh: Có vs Không Có Giáp

| Tình huống | Không có Giáp | Có Giáp Ánh Sáng |
|------------|---------------|-------------------|
| Chết lần 1 | Game Over ❌ | Revive với 50% HP ✅ |
| Chết lần 2 | - | Game Over ❌ |
| Console | No message | "revived with XXX HP!" |
| HP bar | 0/max | Hồi lên 50% |

---

## 🐛 Nếu Không Work

### Kiểm tra 1: File equipment có Giáp không?
```bash
type du_lieu\save\character_equipment.json
```

Phải thấy:
```json
{
  "ninja": {
    "armor": "giap_anh_sang",
    ...
  }
}
```

### Kiểm tra 2: Console có messages không?
Nếu KHÔNG thấy message `[Equipment] ... revive effect enabled!`:
- Giáp chưa được trang bị đúng
- Vào Equipment Scene và trang bị lại

### Kiểm tra 3: Chạy test script
```bash
python test_revive_effect.py
```

Phải thấy: `✅ TEST PASSED!`

---

## 💡 Tips

### Cách chết nhanh để test:
1. **Đứng yên** không né tránh
2. Hoặc nhảy vào giữa đám quái
3. Hoặc để Boss đánh (damage lớn, chết nhanh)

### Quan sát HP bar:
- Góc trên trái màn hình
- Xem số HP: `XXX/YYY`
- Khi revive, số HP sẽ nhảy từ 0 lên ~50%

### Debug:
- Luôn xem Console/Terminal
- Nếu không thấy message → Chưa work
- Nếu thấy message → Work rồi!

---

## 📸 Screenshots Mong Muốn

### Trước khi chết:
```
HP: 150/600
```

### Khi chết (HP = 0):
```
HP: 0/600
[Console] [Equipment] ninja revived with 300 HP!
```

### Sau revive:
```
HP: 300/600  ← Hồi lên 50%!
Nhân vật vẫn đứng, tiếp tục chiến đấu
```

---

## ✅ Checklist Test

Đánh dấu khi test xong:

- [ ] Chạy game thành công
- [ ] Vào Equipment Scene
- [ ] Chọn nhân vật và trang bị Giáp Ánh Sáng
- [ ] Console in message "revive effect enabled!"
- [ ] Vào game với nhân vật đã trang bị
- [ ] Để nhân vật chết (HP = 0)
- [ ] **Nhân vật hồi sinh** với ~50% HP
- [ ] Console in message "revived with XXX HP!"
- [ ] HP bar tăng từ 0 lên 50%
- [ ] Nhân vật tiếp tục sống
- [ ] Chết lần 2 → Không revive nữa
- [ ] Game Over bình thường

---

## 🎉 Khi Test Thành Công

Bạn sẽ thấy:
1. ✅ Console có message revive
2. ✅ HP bar hồi từ 0 → 50%
3. ✅ Nhân vật không chết, tiếp tục chơi
4. ✅ Revive chỉ work 1 lần
5. ✅ Chết lần 2 vào Game Over

**Chúc mừng! Hiệu ứng hồi sinh đã hoạt động!** 🎊

---

**Lưu ý quan trọng**: 
- Revive CHỈ hoạt động khi có **Giáp Ánh Sáng** equipped
- Revive CHỈ work **1 lần** cho đến khi restart level
- Nếu không thấy message trong console → Chưa work, cần check lại

**File test**: `test_revive_effect.py` - Chạy để verify logic
**File docs**: `REVIVE_EFFECT_COMPLETE.md` - Chi tiết kỹ thuật
