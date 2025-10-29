# 🛠️ Fix: Equipment Bonus Display & Application

## ❌ Vấn đề
1. **Màn chọn nhân vật**: Thông số cộng thêm từ trang bị không hiển thị
2. **Màn chơi**: Bonus từ equipment chưa được áp dụng vào nhân vật

## ✅ Giải pháp đã áp dụng

### 1. Sửa `equipment.py` - Hàm `get_equipment_by_name()`

**File**: `ma_nguon/doi_tuong/equipment.py`

**Vấn đề cũ**: Hàm chỉ trả về equipment đầu tiên khớp tên, kể cả khi đã được trang bị cho nhân vật khác.

**Sửa chữa**:
```python
def get_equipment_by_name(self, name, only_available=False):
    """Lấy equipment theo tên
    
    Args:
        name: Tên equipment cần tìm
        only_available: Nếu True, chỉ trả về equipment chưa được trang bị
    """
    for eq in self.all_equipment:
        if eq.name == name:
            if only_available and eq.equipped_to is not None:
                continue
            return eq
    return None
```

**Lợi ích**: Có thể lấy equipment chưa được trang bị bằng cách truyền `only_available=True`.

---

### 2. Sửa `chon_nhan_vat.py` - Hiển thị Bonus

**File**: `ma_nguon/man_choi/chon_nhan_vat.py` (dòng ~499)

**Vấn đề cũ**: 
- Code dùng `eq_manager.get_equipment_by_name()` để lấy bonus
- Equipment manager có thể chưa load inventory → trả về `None`

**Sửa chữa**:
```python
# Get equipment bonuses for this character
equipment_bonuses = {'hp': 0, 'damage': 0, 'defense': 0, 'speed': 0}
if user and cid and owned:
    try:
        from ma_nguon.doi_tuong.items import EQUIPMENT_DATA
        profile = profile_manager.load_profile(user)
        char_equipment = profile.get('character_equipment', {}).get(cid, {})
        
        if char_equipment:
            # Lấy bonus trực tiếp từ EQUIPMENT_DATA thay vì qua manager
            for slot_type, eq_name in char_equipment.items():
                eq_data = EQUIPMENT_DATA.get(eq_name)
                if eq_data:
                    equipment_bonuses['hp'] += eq_data.get('hp_bonus', 0)
                    equipment_bonuses['damage'] += eq_data.get('attack_bonus', 0)
                    equipment_bonuses['defense'] += eq_data.get('defense_bonus', 0)
                    equipment_bonuses['speed'] += eq_data.get('speed_bonus', 0)
    except Exception as e:
        print(f"[CHON_NV] Lỗi load equipment bonuses: {e}")
```

**Lợi ích**: 
- Lấy bonus trực tiếp từ `EQUIPMENT_DATA` (luôn available)
- Không phụ thuộc vào equipment manager
- Debug log để phát hiện lỗi

---

## 📊 Cách hoạt động

### Màn chọn nhân vật (`chon_nhan_vat.py`)

1. **Load profile** → Lấy `character_equipment` dict
2. **Với mỗi nhân vật**:
   - Kiểm tra `character_equipment[char_id]`
   - Lấy equipment data từ `EQUIPMENT_DATA`
   - Tính tổng bonus: HP, Damage, Defense, Speed
3. **Hiển thị**:
   ```
   HP: 350 (+250)    ← 100 base + 250 từ Giáp Ánh Sáng
   ST: 35 (+15)      ← 20 base + 15 từ Kiếm Rồng
   Tốc: 8 (+3)       ← 5 base + 3 từ Giày Thiên Thần
   ```

### Khi vào màn chơi (`_create_player()`)

1. **Tạo Character** với base stats
2. **Load inventory** vào equipment manager:
   ```python
   eq_manager.load_inventory_from_profile(inventory)
   ```
3. **Load character equipment**:
   ```python
   eq_manager.load_character_equipment(char_id, character_equipment[char_id])
   ```
4. **Apply từng equipment**:
   ```python
   for slot_type, eq_name in character_equipment[char_id].items():
       equipment = eq_manager.get_equipment_by_name(eq_name)
       if equipment:
           player.equip_item(equipment)  # Áp dụng bonus
   ```
5. **Đánh dấu đã apply**:
   ```python
   player._equipment_applied = True  # Tránh apply lại
   ```

---

## 🧪 Test Case

### Test Data
```python
username = 'huy'
character_equipment = {
    'chien_binh': {
        'attack': 'Kiếm Rồng',      # +15 ATK, burn effect
        'defense': 'Giáp Ánh Sáng',  # +250 HP, revive effect
        'boots': 'Giày Thiên Thần'   # +3 SPD, double_jump
    }
}
```

### Expected Result
- **Màn chọn nhân vật**:
  - ✅ Hiển thị bonus bên cạnh base stats
  - ✅ Tổng stats = base + bonus
  
- **Màn chơi**:
  - ✅ Nhân vật có HP = base_hp + 250
  - ✅ Damage = base_damage + 15
  - ✅ Speed = base_speed + 3
  - ✅ Special effects hoạt động (burn, revive, double_jump)

---

## 📝 Lưu ý quan trọng

### 1. Load order trong `_create_player()`
```python
# ✅ ĐÚNG: Load inventory TRƯỚC
eq_manager.load_inventory_from_profile(inventory)

# ❌ SAI: Load character equipment trước khi có inventory
eq_manager.load_character_equipment(...)  # Sẽ không tìm thấy equipment
```

### 2. Hiển thị bonus vs Apply bonus

**Hiển thị** (màn chọn nhân vật):
- Lấy từ `EQUIPMENT_DATA` (không cần equipment objects)
- Chỉ cần tên equipment từ profile

**Apply** (vào màn chơi):
- Cần equipment objects từ manager
- Gọi `player.equip_item(equipment)` để apply

### 3. Profile structure
```json
{
  "equipment_inventory": {
    "Kiếm Rồng": 10,
    "Giáp Ánh Sáng": 1,
    "Giày Thiên Thần": 6
  },
  "character_equipment": {
    "chien_binh": {
      "attack": "Kiếm Rồng",
      "defense": "Giáp Ánh Sáng",
      "boots": "Giày Thiên Thần"
    },
    "sasuke": {
      "attack": "Cung Băng Lãm"
    }
  }
}
```

---

## 🔍 Debug Tips

### Kiểm tra bonus hiển thị đúng không:
```python
python test_equipment_bonus_display.py
```

### Kiểm tra bonus áp dụng vào nhân vật:
1. Chạy game
2. Login với user có equipment (vd: 'huy')
3. Chọn nhân vật đã trang bị
4. Xem console log:
   ```
   Base stats - HP: 100/100, Damage: 20, Speed: 5
   Sau khi lắp trang bị - HP: 350/350, Damage: 35, Speed: 8
   ```

### Nếu bonus không hiển thị:
- Kiểm tra `character_equipment` có data không:
  ```python
  profile['character_equipment']
  ```
- Kiểm tra equipment name có trong `EQUIPMENT_DATA`:
  ```python
  from ma_nguon.doi_tuong.items import EQUIPMENT_DATA
  print("Kiếm Rồng" in EQUIPMENT_DATA)
  ```

### Nếu bonus không áp dụng vào game:
- Kiểm tra inventory có equipment không:
  ```python
  profile['equipment_inventory']
  ```
- Xem log console khi tạo nhân vật (có "Lắp ... vào ..." không?)
- Kiểm tra `player._equipment_applied` flag

---

## ✨ Kết quả

### Trước khi sửa
- ❌ Bonus không hiển thị trong màn chọn
- ❌ Stats không tăng khi vào game
- ❌ Special effects không hoạt động

### Sau khi sửa
- ✅ Bonus hiển thị đúng: `HP: 350 (+250)`
- ✅ Stats tăng đúng trong game
- ✅ Special effects hoạt động (burn, revive, double_jump)
- ✅ Code dễ maintain, debug

---

## 📚 Related Files

- `ma_nguon/doi_tuong/equipment.py` - Equipment manager
- `ma_nguon/man_choi/chon_nhan_vat.py` - Character selection screen
- `ma_nguon/doi_tuong/items.py` - EQUIPMENT_DATA dictionary
- `ma_nguon/doi_tuong/nhan_vat/nhan_vat.py` - Character class với `equip_item()`
- `test_equipment_bonus_display.py` - Test script

---

**Last Updated**: 2025-10-28  
**Status**: ✅ Fixed và tested
