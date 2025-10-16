# 🎮 DEMO: Kiểm Tra Trang Bị Persist

## 🎯 Mục Đích
Kiểm tra trang bị đã lắp trong Equipment Scene có được giữ lại khi chơi game không.

## 📋 Các Bước Test

### 1️⃣ Chạy Game
```bash
cd "d:\GamePygame\REIGN\REIGN"
$env:PYTHONPATH="d:\GamePygame\REIGN\REIGN"
python -m ma_nguon.main
```

### 2️⃣ Vào Equipment Scene
1. Ở **Menu chính**
2. Chọn **"Trang bị"**
3. Màn hình Equipment Scene sẽ mở

### 3️⃣ Chọn Nhân Vật
1. Click nút **"Chọn Nhân Vật"** (góc phải dưới)
2. Popup hiện ra với 5 nhân vật
3. Chọn **Ninja**

### 4️⃣ Kiểm Tra Stats Ban Đầu
Nhìn panel **"Chỉ Số Nhân Vật"** bên phải:
```
HP: 350/350
Sát Thương: 25
Đá: 18
Tốc Độ: 8
Phòng Thủ: 1
```

### 5️⃣ Lắp Trang Bị

#### Lắp Kiếm Rồng
1. Click **Kiếm Rồng** trong Inventory (kho đồ bên trái)
2. Item sẽ chuyển vào slot **WEAPON**
3. Stats update:
   ```
   HP: 350/350
   Sát Thương: 35  ← Tăng +10
   ```

#### Lắp Giáp Ánh Sáng
1. Click **Giáp Ánh Sáng** trong Inventory
2. Item sẽ chuyển vào slot **ARMOR**
3. Stats update:
   ```
   HP: 550/550  ← Tăng +200
   Sát Thương: 35
   ```

#### Lắp Giày Thiên Thần
1. Click **Giày Thiên Thần** trong Inventory
2. Item sẽ chuyển vào slot **BOOTS**
3. Stats update:
   ```
   HP: 600/600  ← Tăng +50
   Sát Thương: 35
   Tốc Độ: 10   ← Tăng +2
   ```

### 6️⃣ GHI NHỚ Stats Cuối Cùng
```
✍️ Ghi lại:
HP:     600
Damage: 35
Speed:  10
```

### 7️⃣ Quay Lại Menu
1. Nhấn **ESC**
2. Về màn hình Menu chính

### 8️⃣ Vào Character Select
1. Chọn **"Chơi"**
2. Chọn màn chơi (ví dụ: Mùa Thu - Màn 1)
3. Màn hình Character Select hiện ra

### 9️⃣ Chọn Ninja Để Chơi
1. Dùng **←→** để chọn Ninja
2. Nhấn **ENTER** để xác nhận

### 🔟 Kiểm Tra Console Output
Trong console sẽ thấy:
```
[GlobalEquipment] Áp dụng trang bị cho ninja:
  - weapon: Kiếm Rồng (HP=350, DMG=35)
  - armor: Giáp Ánh Sáng (HP=550, DMG=35)
  - boots: Giày Thiên Thần (HP=600, DMG=35)
[CharacterSelect] Created character: Ninja (ID: ninja) with equipment
  Stats: HP=600, DMG=35, SPD=10, DEF=1
```

### 1️⃣1️⃣ Kiểm Tra Trong Game
1. Game bắt đầu với Ninja
2. Nếu có health bar, sẽ thấy:
   ```
   HP: 600/600  ✓
   ```
3. Ninja sẽ đánh mạnh hơn (35 damage thay vì 25)
4. Ninja chạy nhanh hơn (10 speed thay vì 8)

## ✅ Kết Quả Mong Đợi

| Stage | HP | Damage | Speed |
|-------|-----|--------|-------|
| **Equipment Scene (Lúc lắp)** | 600 | 35 | 10 |
| **Character Select** | 600 | 35 | 10 |
| **In Game** | 600 | 35 | 10 |

✅ **Tất cả đều phải giống nhau!**

## ❌ Nếu Không Đúng

### Stats không giống nhau?
1. Check console có thấy:
   ```
   [GlobalEquipment] Áp dụng trang bị cho ninja:
   ```
   không?

2. Check file save:
   ```bash
   cat du_lieu/save/character_equipment.json
   ```
   
   Phải thấy:
   ```json
   {
     "ninja": {
       "weapon": "kiem_rong",
       "armor": "giap_anh_sang",
       "boots": "giay_thien_than"
     }
   }
   ```

3. Run test để verify:
   ```bash
   python test_full_equipment_flow.py
   ```

## 🎥 Video Demo Flow

```
[Menu] 
  ↓ Click "Trang bị"
[Equipment Scene]
  ↓ Click "Chọn Nhân Vật"
[Character Selector Popup]
  ↓ Click "Ninja"
[Equipment Scene - Ninja Selected]
  ↓ Click items trong inventory
[Stats Update Real-time]
  ↓ HP: 350→550→600
  ↓ DMG: 25→35
  ↓ SPD: 8→10
[Press ESC]
  ↓
[Menu]
  ↓ Click "Chơi"
[Select Level]
  ↓
[Character Select]
  ↓ Press ENTER on Ninja
[Game Starts]
  ✓ Ninja has HP=600, DMG=35, SPD=10!
```

## 🧪 Quick Test Script

Nếu muốn test nhanh không cần chạy game:
```bash
python test_full_equipment_flow.py
```

Kết quả mong đợi:
```
✅ TEST PASSED!
🎉 STATS ĐƯỢC ĐỒNG BỘ HOÀN HẢO!
```

## 📊 Test Cases

| Test Case | Expected Result |
|-----------|----------------|
| Lắp Kiếm Rồng | DMG: 25 → 35 |
| Lắp Giáp Ánh Sáng | HP: 350 → 550 |
| Lắp Giày Thiên Thần | HP: 550 → 600, SPD: 8 → 10 |
| Save và Load | Stats persist across scenes |
| Multiple characters | Each character has own equipment |

## 🎉 Success Criteria

✅ Stats trong Equipment Scene = Stats khi chơi  
✅ Console shows equipment loading messages  
✅ File JSON chứa đúng equipment  
✅ Test script passes 100%  

---

**Happy Testing!** 🎮
