# 🎯 HƯỚNG DẪN KIỂM TRA TRANG BỊ TRONG GAME

## ⚠️ LƯU Ý QUAN TRỌNG

Nếu bạn vẫn thấy stats cũ trong game, có thể do:
1. **Game đang chạy phiên bản cũ** - cần restart game
2. **Trang bị chưa được lưu** - cần vào Equipment Scene và trang bị lại
3. **Console messages bị ẩn** - cần xem Console để debug

---

## 📋 BƯỚC 1: XÓA SAVE CŨ (Tuỳ chọn)

Để đảm bảo test sạch, có thể xóa file save cũ:

```bash
# Xóa file trang bị cũ
del du_lieu\save\character_equipment.json
```

Hoặc mở file `du_lieu/save/character_equipment.json` và xóa nội dung, thay bằng:
```json
{}
```

---

## 📋 BƯỚC 2: CHẠY GAME

```bash
cd D:\GamePygame\REIGN\REIGN
python -m ma_nguon.main
```

**✅ Điểm quan trọng**: Phải chạy từ thư mục `REIGN` (thư mục con), không phải thư mục cha!

---

## 📋 BƯỚC 3: TRANG BỊ ITEMS

1. **Từ Menu**, nhấn phím **E** để vào Equipment Scene
2. **Chọn nhân vật** Chiến Binh (hoặc nhân vật khác bạn muốn test)
3. **Trang bị các items**:
   - Weapon slot: Click chọn **Cung Băng Lam**
   - Armor slot: Click chọn **Giáp Ánh Sáng**  
   - Boots slot: Click chọn **Giày Thiên Thần**
4. **Xem stats preview** bên phải:
   ```
   HP: 500 → 750 (+250)
   Damage: 30 → 38 (+8)
   Speed: 5 → 7 (+2)
   ```
5. Nhấn **ESC** để lưu và quay về Menu

---

## 📋 BƯỚC 4: VÀO GAME VÀ KIỂM TRA

1. **Từ Menu**, chọn màn chơi bất kỳ (ví dụ: **Level 1**)

2. **Trong Character Select**:
   - Chọn Chiến Binh (nhân vật vừa trang bị)
   - **Phải thấy**:
     - Icon ⚔ ở góc trên card nhân vật
     - Stats với bonus màu xanh:
       ```
       HP: 750 (+250)
       ST: 38 (+8)
       Tốc độ: 7 (+2)
       ```

3. **Nhấn ENTER** để vào game

4. **🔍 QUAN TRỌNG: XEM CONSOLE/TERMINAL**
   
   Bạn **PHẢI** thấy các dòng debug sau trong console:
   ```
   [CharacterSelect] Created character: Chiến binh (ID: chien_binh) with equipment
     Stats: HP=750, DMG=38, SPD=7, DEF=2
   [GlobalEquipment] Áp dụng trang bị cho chien_binh:
     - weapon: Cung Băng Lam (HP=500, DMG=38)
     - armor: Giáp Ánh Sáng (HP=700, DMG=38)
     - boots: Giày Thiên Thần (HP=750, DMG=38)
   [Man1] Received player with stats: HP=750, DMG=38, SPD=7
   ```

5. **Kiểm tra trong gameplay**:

   ✅ **Thanh máu góc trên trái**: Phải hiện **750/750** (không phải 500/500)
   
   ✅ **Tốc độ di chuyển**: Nhanh hơn đáng kể (7 thay vì 5)
   
   ✅ **Damage**: Khi đánh quái, sẽ thấy số damage là **38** (không phải 30)

---

## 🐛 NẾU VẪN KHÔNG WORK

### Kiểm tra Console

**Nếu thấy dòng này**:
```
[Man1] Created new player with default stats
```
→ ❌ **Có vấn đề**: Game không nhận player từ Character Select!

**Nếu KHÔNG thấy dòng nào**:
→ ❌ **Có vấn đề**: Debug messages bị tắt hoặc code chưa được sửa

---

### Kiểm tra File Equipment

Mở file: `du_lieu/save/character_equipment.json`

Phải thấy:
```json
{
  "chien_binh": {
    "weapon": "cung_bang_lam",
    "armor": "giap_anh_sang",
    "boots": "giay_thien_than"
  }
}
```

Nếu **KHÔNG có** hoặc **rỗng** → Trang bị chưa được lưu!

---

### Chạy Test Scripts

```bash
# Test 1: Kiểm tra equipment sync
python test_full_game_flow.py

# Test 2: Kiểm tra in-game stats
python test_ingame_equipment_stats.py
```

Cả 2 test phải **PASS** ✅

---

## 📊 SO SÁNH: TRƯỚC VÀ SAU

### KHÔNG có trang bị (Base Stats):
```
HP: 500/500
Damage: 30
Speed: 5
```

### CÓ full trang bị (Cung + Giáp + Giày):
```
HP: 750/750 (+250)
Damage: 38 (+8)
Speed: 7 (+2)
```

**Cách test nhanh**: 
- Đi thử → Phải nhanh hơn rõ rệt
- Đánh quái → Quái chết nhanh hơn
- Nhìn thanh máu → Dài hơn (750 thay vì 500)

---

## 🎉 KHI TEST THÀNH CÔNG

Bạn sẽ thấy:

1. ✅ **Console có đủ debug messages** với stats đúng
2. ✅ **HP bar hiển thị 750/750** (không phải 500/500)
3. ✅ **Character di chuyển nhanh hơn** (speed 7 vs 5)
4. ✅ **Damage cao hơn** khi đánh quái (38 vs 30)
5. ✅ **Hiệu ứng trang bị hoạt động**:
   - Cung Băng Lam: Làm chậm quái
   - Giáp Ánh Sáng: Hồi sinh khi chết
   - Giày Thiên Thần: Nhảy 2 lần

---

## 💡 TIPS

- **Nhấn TAB** hoặc nhìn góc trên trái để xem HP bar
- **Console/Terminal** sẽ có debug messages chi tiết
- Nếu vẫn không work, chụp ảnh console và báo lại!

---

**Ngày**: 2025-10-16  
**Trạng thái**: ✅ Code đã được sửa, chờ test trong game thật
**Files đã sửa**: 7 gameplay files (man1.py, man2.py, map_mua_thu*.py, map_cong_nghe.py)
