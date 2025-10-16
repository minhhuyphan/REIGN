# 🎯 HƯỚNG DẪN: TRANG BỊ VÀ TEST NGAY

## ⚠️ VẤN ĐỀ HIỆN TẠI

File `character_equipment.json` cho thấy **Chiến Binh KHÔNG CÓ trang bị**:
```json
"chien_binh": {
  "weapon": null,
  "armor": null, 
  "boots": null
}
```

**Ninja** mới là nhân vật có trang bị đầy đủ!

---

## 🎮 CÁCH TEST ĐÚNG

### Bước 1: Chạy game
```bash
cd D:\GamePygame\REIGN\REIGN
python -m ma_nguon.main
```

### Bước 2: Vào Equipment Scene
- Từ Menu, nhấn phím **E**

### Bước 3: Trang bị cho **Chiến Binh**
1. **Click vào nhân vật Chiến Binh** (card bên trái)
2. Trang bị các items:
   - **Weapon**: Click "Cung Băng Lam"
   - **Armor**: Click "Giáp Ánh Sáng"
   - **Boots**: Click "Giày Thiên Thần"
3. **Xem stats preview** bên phải - phải thấy:
   ```
   HP: 500 → 750
   DMG: 30 → 38
   SPD: 5 → 7
   ```
4. Nhấn **ESC** để lưu

### Bước 4: Vào Game
1. Chọn màn chơi (Level 1)
2. **Chọn Chiến Binh** (phải thấy icon ⚔ và stats xanh)
3. Nhấn **ENTER**
4. **Trong game**:
   - Thanh máu góc trên trái: **750/750** ✅
   - Tốc độ di chuyển: Nhanh hơn
   - Damage: 38 khi đánh quái

---

## 🔧 HOẶC: Test với Ninja (Đã có trang bị sẵn!)

Ninja đã có trang bị:
- Weapon: Kiếm Rồng (+10 DMG)
- Armor: Giáp Ánh Sáng (+200 HP)
- Boots: Giày Thiên Thần (+50 HP, +2 SPD)

### Test nhanh:
1. Chạy game
2. Chọn màn chơi → Chọn **Ninja**
3. Phải thấy icon ⚔ và stats với bonus
4. Vào game → Thanh máu phải cao hơn base stats

---

## 📊 Base Stats Mỗi Nhân Vật

| Nhân vật | HP | Damage | Speed | Defense |
|----------|-----|--------|-------|---------|
| Chiến Binh | 500 | 30 | 5 | 2 |
| Ninja | 350 | 25 | 8 | 10 |
| Võ Sĩ | 400 | 28 | 6 | 5 |

### Với Full Equipment (Cung/Kiếm + Giáp + Giày):
- **HP**: +250 (200 từ Giáp + 50 từ Giày)
- **Damage**: +8 (Cung) hoặc +10 (Kiếm)
- **Speed**: +2 (Giày)

### Ví dụ Chiến Binh với full equipment:
```
HP: 500 + 250 = 750
Damage: 30 + 8 = 38
Speed: 5 + 2 = 7
```

---

## 🐛 Debug Checklist

Nếu vẫn không work, kiểm tra:

### 1. File equipment có lưu không?
```bash
type du_lieu\save\character_equipment.json
```

Phải thấy nhân vật có equipment (không phải null):
```json
"chien_binh": {
  "weapon": "cung_bang_lam",
  "armor": "giap_anh_sang",
  "boots": "giay_thien_than"
}
```

### 2. Console có debug messages không?
Khi vào game, phải thấy:
```
[CharacterSelect] Created character: Chiến binh (ID: chien_binh) with equipment
  Stats: HP=750, DMG=38, SPD=7, DEF=2
[Man1] Received player with stats: HP=750, DMG=38, SPD=7
```

### 3. Chạy test scripts
```bash
python test_full_game_flow.py
```
Phải PASS ✅

---

## 🎯 TL;DR - CÁCH NHANH NHẤT

**Option 1: Test với Ninja (Đã có equipment):**
1. Chạy game
2. Chọn Level 1 → Chọn Ninja
3. Xem thanh máu trong game

**Option 2: Trang bị cho Chiến Binh:**
1. Chạy game
2. Nhấn **E** → Chọn Chiến Binh
3. Trang bị 3 items (Cung + Giáp + Giày)
4. ESC → Chọn Level 1 → Chọn Chiến Binh
5. Xem thanh máu trong game

---

**Lưu ý**: File `character_equipment.json` hiện tại cho thấy chỉ **Ninja** có equipment đầy đủ. Hãy test với Ninja hoặc trang bị lại cho Chiến Binh!
