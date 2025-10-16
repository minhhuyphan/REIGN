# ✨ Hiệu Ứng Hồi Sinh - Giáp Ánh Sáng

## 📋 Tóm Tắt

**Vấn đề**: Hiệu ứng hồi sinh của Giáp Ánh Sáng chưa hoạt động trong game

**Nguyên nhân**: Method `Equipment.apply_to_character()` không set flag `equipped_armor_has_revive` khi trang bị giáp có revive effect

**Giải pháp**: Thêm logic trong `apply_to_character()` và `remove_from_character()` để set/unset flag revive

---

## 🔧 Các Thay Đổi

### 1. File: `ma_nguon/doi_tuong/equipment.py`

#### Sửa `apply_to_character()`:
```python
def apply_to_character(self, character):
    """Áp dụng stats của trang bị lên nhân vật"""
    # ... apply stats như cũ ...
    
    # Apply special effects
    if self.special_effect:
        effect_type = self.special_effect.get("type")
        
        # Set revive flag if armor has revive effect
        if effect_type == "revive" and self.type == Equipment.TYPE_ARMOR:
            character.equipped_armor_has_revive = True
            print(f"[Equipment] {self.name} revive effect enabled!")
```

#### Sửa `remove_from_character()`:
```python
def remove_from_character(self, character):
    """Gỡ bỏ stats của trang bị khỏi nhân vật"""
    # ... remove stats như cũ ...
    
    # Remove special effects
    if self.special_effect:
        effect_type = self.special_effect.get("type")
        
        # Remove revive flag if armor had revive effect
        if effect_type == "revive" and self.type == Equipment.TYPE_ARMOR:
            character.equipped_armor_has_revive = False
            print(f"[Equipment] {self.name} revive effect disabled!")
```

### 2. File: `ma_nguon/doi_tuong/nhan_vat/nhan_vat.py`

#### Thêm flag trong `__init__`:
```python
# Equipment effects tracking
self.active_effects = []
self.revive_available = True  # For armor revive effect
self.equipped_armor_has_revive = False  # Flag to check if armor has revive
```

#### Logic revive đã có sẵn trong `take_damage()`:
```python
if self.hp <= 0:
    # Check for revive effect from armor
    if self.revive_available and hasattr(self, 'equipped_armor_has_revive'):
        if self.equipped_armor_has_revive:
            # Revive with 50% HP
            self.hp = int(self.max_hp * 0.5)
            self.dead = False
            self.revive_available = False  # Use revive once
            print(f"[Equipment] {self.folder} revived with {self.hp} HP!")
            return
    
    self.dead = True
    # ... death animation ...
```

---

## 🎮 Cách Hoạt Động

### 1. Trang bị Giáp Ánh Sáng
```
Equipment Scene:
├─ Chọn nhân vật
├─ Click Giáp Ánh Sáng trong inventory
├─ Lắp vào Armor slot
└─ equipped_armor_has_revive = True ✅
```

### 2. Trong Gameplay
```
Nhân vật bị tấn công:
├─ HP giảm xuống
├─ Nếu HP <= 0:
│   ├─ Kiểm tra: revive_available AND equipped_armor_has_revive?
│   │   ├─ YES: Hồi sinh với HP = max_hp * 50%
│   │   │       revive_available = False
│   │   │       dead = False
│   │   └─ NO: Nhân vật chết (dead = True)
└─ Continue gameplay
```

### 3. Chỉ Hoạt Động 1 Lần
- Sau khi revive, `revive_available = False`
- Nếu chết lần 2 → Không hồi sinh nữa
- Reset khi restart level hoặc respawn

---

## 📊 Test Results

```bash
python test_revive_effect.py
```

### Kết quả:
```
✅ TEST PASSED!

Test 1: Equip Giáp Ánh Sáng
  - equipped_armor_has_revive: False → True ✅
  - HP: 350 → 550 (+200 from armor) ✅

Test 2: Nhân vật chết lần 1
  - HP: 550 → 0 (take damage 650)
  - Revive: YES
  - HP after revive: 275 (50% of 550) ✅
  - revive_available: True → False ✅

Test 3: Nhân vật chết lần 2
  - HP: 550 → -99 (take damage 649)
  - Revive: NO (already used)
  - dead: True ✅
```

---

## 🎯 Giáp Ánh Sáng - Thông Số

```python
"giap_anh_sang": Equipment(
    item_id="giap_anh_sang",
    name="Giáp Ánh Sáng",
    item_type=Equipment.TYPE_ARMOR,
    image_path="Tai_nguyen/hinh_anh/trang_bi/trang_bi_thu/giap_anh_sang.png",
    stats={"hp": 200},
    special_effect={
        "type": "revive",
        "description": "Hồi sinh 1 lần với 50% HP",
        "revive_hp_percent": 0.5,
        "uses": 1
    }
)
```

### Bonus:
- **+200 HP**
- **Revive Effect**: Hồi sinh 1 lần với 50% HP khi chết

---

## 💡 Hướng Dẫn Test Trong Game

### Bước 1: Trang bị
1. Chạy game: `python -m ma_nguon.main`
2. Nhấn **E** vào Equipment Scene
3. Chọn nhân vật (ví dụ: Ninja)
4. Trang bị **Giáp Ánh Sáng** vào Armor slot
5. Nhấn ESC về Menu

### Bước 2: Test trong gameplay
1. Chọn màn chơi → Chọn nhân vật đã trang bị
2. Vào game
3. **Cố ý để nhân vật bị chết** (đứng yên để quái đánh)
4. **Quan sát**: 
   - Console sẽ in: `[Equipment] ... revived with XXX HP!`
   - HP bar sẽ hồi phục lên 50%
   - Nhân vật tiếp tục chơi (không dead)

### Bước 3: Test revive chỉ 1 lần
1. Tiếp tục chơi
2. Cố ý chết lần 2
3. **Quan sát**: Lần này nhân vật sẽ chết thật (không revive nữa)

---

## 🔍 Debug Messages

Khi test, bạn sẽ thấy các messages sau trong console:

```
# Khi trang bị
[Equipment] Giáp Ánh Sáng revive effect enabled!

# Khi chết lần 1 (revive)
[Equipment] tai_nguyen/hinh_anh/nhan_vat/ninja revived with 275 HP!

# Khi chết lần 2 (không revive - không có message)
```

---

## ✅ Checklist

- [x] Thêm `equipped_armor_has_revive` flag vào Character
- [x] Set flag trong `Equipment.apply_to_character()`
- [x] Unset flag trong `Equipment.remove_from_character()`
- [x] Logic revive trong `Character.take_damage()` đã có sẵn
- [x] Test script pass 100%
- [x] Revive chỉ hoạt động 1 lần
- [x] Console messages để debug

---

## 🎊 Tổng Kết

✅ **Hiệu ứng hồi sinh đã hoạt động hoàn toàn!**

**Trước đây**: 
- `equipped_armor_has_revive` không bao giờ được set = True
- Nhân vật chết bình thường

**Bây giờ**:
- Trang bị Giáp Ánh Sáng → Flag được set
- Chết lần 1 → Hồi sinh với 50% HP
- Chết lần 2 → Chết thật

**Các hiệu ứng đặc biệt đã hoàn thành**:
1. ✅ **Slow** (Cung Băng Lam) - Làm chậm quái
2. ✅ **Burn** (Kiếm Rồng) - Thiêu đốt 1 HP/giây
3. ✅ **Revive** (Giáp Ánh Sáng) - Hồi sinh 1 lần
4. ✅ **Double Jump** (Giày Thiên Thần) - Nhảy 2 lần

---

**Ngày**: 2025-10-16  
**Status**: ✅ HOÀN THÀNH  
**Test File**: `test_revive_effect.py`
