# 🎮 HƯỚNG DẪN TEST: TRANG BỊ TRONG GAME

## 📋 Các Bước Test

### 1️⃣ Vào Equipment Scene và Trang Bị Item
1. Chạy game: `python -m ma_nguon.main`
2. Từ Menu, nhấn **E** để vào Equipment Scene
3. Chọn một nhân vật (ví dụ: Chiến Binh)
4. Trang bị các item:
   - **Weapon slot**: Chọn Cung Băng Lam (+8 Damage)
   - **Armor slot**: Chọn Giáp Ánh Sáng (+200 HP)
   - **Boots slot**: Chọn Giày Thiên Thần (+50 HP, +2 Speed)
5. Nhấn ESC để quay về Menu

### 2️⃣ Kiểm Tra Stats Trong Character Select
1. Từ Menu, chọn màn chơi bất kỳ (ví dụ: Level 1)
2. Trong Character Select:
   - Chọn Chiến Binh (nhân vật vừa trang bị)
   - **Kiểm tra**: Bạn sẽ thấy:
     - ⚔ Icon trên góc card nhân vật
     - Stats với bonus màu xanh:
       - HP: 600 **(+250)** ← màu xanh
       - Tốc độ: 10 **(+2)** ← màu xanh
       - ST: 33 **(+8)** ← màu xanh
       - PT: 10

### 3️⃣ Test Trong Gameplay - QUAN TRỌNG!
1. Nhấn ENTER để vào game
2. **Xem Console/Terminal** - bạn sẽ thấy debug message:
   ```
   [CharacterSelect] Created character: Chiến Binh (ID: chien_binh) with equipment
     Stats: HP=600, DMG=33, SPD=10, DEF=10
   [Man1] Received player with stats: HP=600, DMG=33, SPD=10
   ```

3. **Test trong game**:
   - Nhấn TAB hoặc xem góc trên bên phải để xem thanh máu
   - Máu tối đa phải là **600 HP** (không phải 350)
   - Tốc độ di chuyển phải nhanh hơn (10 thay vì 8)
   - Đánh quái - sát thương phải là **33** (không phải 25)

### 4️⃣ So Sánh Với/Không Có Trang Bị

#### KHÔNG có trang bị:
```
HP: 350
Damage: 25
Speed: 8
Defense: 10
```

#### CÓ full trang bị (Cung + Giáp + Giày):
```
HP: 600 (+250 bonus)
Damage: 33 (+8 bonus)
Speed: 10 (+2 bonus)
Defense: 10 (no bonus)
```

## 🎯 Điểm Cần Kiểm Tra

### ✅ Checklist Test
- [ ] Equipment Scene: Có thể trang bị item cho nhân vật
- [ ] Equipment được lưu (nhấn ESC rồi vào lại vẫn còn)
- [ ] Character Select hiển thị icon ⚔ cho nhân vật có trang bị
- [ ] Character Select hiển thị stats với bonus màu xanh
- [ ] **Console có debug message khi vào game**
- [ ] **Trong game: HP tối đa là 600 (không phải 350)**
- [ ] **Trong game: Tốc độ di chuyển nhanh hơn**
- [ ] **Trong game: Damage cao hơn khi đánh quái**

## 🐛 Nếu Vẫn Không Work

### Kiểm tra Console Output
Khi vào game, phải thấy message:
```
[CharacterSelect] Created character: Chiến Binh (ID: chien_binh) with equipment
  Stats: HP=600, DMG=33, SPD=10, DEF=10
[Man1] Received player with stats: HP=600, DMG=33, SPD=10
```

Nếu thấy:
```
[Man1] Created new player with default stats
```
→ Nghĩa là game không nhận player từ Character Select!

### Debug Steps:
1. Kiểm tra file `du_lieu/save/character_equipment.json`:
   ```json
   {
     "chien_binh": {
       "weapon": "cung_bang_lam",
       "armor": "giap_anh_sang",
       "boots": "giay_thien_than"
     }
   }
   ```

2. Chạy test script:
   ```bash
   python test_ingame_equipment_stats.py
   ```
   Phải thấy: `✅ TEST PASSED!`

3. Kiểm tra `quan_ly_game.py` - phương thức `change_scene()`:
   ```python
   # Phải truyền selected_player vào scene
   if scene_name == "level1":
       scene = Level1Scene(self, player=self.selected_player)
   ```

## 📊 Test Cases

### Test Case 1: Full Equipment
```
Setup:
- Equip: Cung Băng Lam, Giáp Ánh Sáng, Giày Thiên Thần
- Character: Chiến Binh

Expected Result in Game:
- HP: 600/600
- Damage: 33
- Speed: 10
- Defense: 10
```

### Test Case 2: Only Weapon
```
Setup:
- Equip: Cung Băng Lam only
- Character: Chiến Binh

Expected Result in Game:
- HP: 350/350 (no change)
- Damage: 33 (+8 from weapon)
- Speed: 8 (no change)
- Defense: 10 (no change)
```

### Test Case 3: No Equipment
```
Setup:
- No equipment
- Character: Chiến Binh

Expected Result in Game:
- HP: 350/350
- Damage: 25
- Speed: 8
- Defense: 10
```

## 🎉 Khi Test Thành Công

Bạn sẽ thấy:
1. ✅ Console có debug messages với stats đúng
2. ✅ HP bar trong game hiển thị 600/600
3. ✅ Character di chuyển nhanh hơn
4. ✅ Damage lên quái cao hơn (33 thay vì 25)
5. ✅ Hiệu ứng đặc biệt của trang bị hoạt động:
   - Cung Băng Lam: Làm chậm quái khi đánh
   - Giáp Ánh Sáng: Hồi sinh khi chết (1 lần)
   - Giày Thiên Thần: Double jump

---

**Lưu ý**: Nếu test thành công, có nghĩa là hệ thống trang bị đã hoạt động HOÀN TOÀN từ Equipment Scene → Character Select → Actual Gameplay! 🎊
