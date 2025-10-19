# Hướng Dẫn Đồng Bộ Equipment & Character Stats

## 📋 Tổng Quan
Hệ thống đồng bộ hóa giúp thuộc tính từ trang bị được áp dụng nhất quán giữa màn hình trang bị và khi chơi game.

## 🎯 Cách Hoạt Động

### 1. **File Shared: `character_stats.py`**
Chứa tất cả stats cơ bản của nhân vật:
```python
CHARACTER_STATS = {
    "chien_binh": {
        "hp": 500,
        "damage": 30,
        "defense": 2,
        "speed": 5,
        ...
    },
    ...
}
```

### 2. **Equipment Screen** (`equipment_screen.py`)
Hiển thị stats theo format:
```
HP:      500  +200  = 700
Công:    30   +10   = 40
Thủ:     2    +0    = 2
Tốc độ:  5    +2    = 7
```

- **500** = Base stats từ `CHARACTER_STATS`
- **+200** = Bonus từ equipment
- **= 700** = Tổng cộng (màu vàng)

### 3. **Character Select** (`chon_nhan_vat.py`)
- Load stats từ `CHARACTER_STATS`
- Khi chọn nhân vật → tạo Character object
- Áp dụng equipment đã lưu trong profile
- Stats cuối = Base + Equipment Bonus

### 4. **In-Game** (Character class)
Các hàm tính stats:
```python
get_effective_damage()  # damage + equipment bonus
get_effective_speed()   # speed + equipment bonus
get_max_hp_with_equipment()  # max_hp + equipment bonus
```

## 🔄 Flow Đồng Bộ

```
1. Equipment Screen
   ↓
   Chọn nhân vật → Load base stats từ CHARACTER_STATS
   ↓
   Lắp trang bị → Equipment bonus được thêm vào
   ↓
   Hiển thị: Base + Bonus = Total
   ↓
   Lưu vào profile: character_equipment

2. Character Select
   ↓
   Chọn nhân vật để chơi
   ↓
   Load base stats từ CHARACTER_STATS
   ↓
   Load equipment từ profile
   ↓
   Áp dụng equipment vào Character object
   ↓
   Character.equipped = {equipment_data}

3. In-Game
   ↓
   Khi attack: damage = get_effective_damage()
   ↓
   Khi move: speed = get_effective_speed()
   ↓
   Khi check HP: max_hp = get_max_hp_with_equipment()
   ↓
   Stats LUÔN bao gồm equipment bonus!
```

## 📊 Ví Dụ Cụ Thể

### Tình huống: Chiến binh lắp Kiếm Rồng

**1. Trong Equipment Screen:**
```
Character: Chiến binh
Base Stats (từ CHARACTER_STATS):
  - HP: 500
  - Damage: 30
  - Defense: 2
  - Speed: 5

Equipped: Kiếm Rồng (+10 Damage, Burn Effect)

Display:
  HP:      500  +0   = 500
  Công:    30   +10  = 40    ← Tăng lên!
  Thủ:     2    +0   = 2
  Tốc độ:  5    +0   = 5
  
Special Effects:
  🔥 Thiêu 1 HP/30s
```

**2. Khi chọn nhân vật chơi game:**
```python
# chon_nhan_vat.py - _create_player()
player = Character(...)
player.hp = 500        # Base
player.damage = 30     # Base
player.defense = 2     # Base
player.speed = 5       # Base

# Load equipment
equipment = KiemRong()
player.equip_item(equipment)  # Lắp Kiếm Rồng

# In-game stats
player.get_effective_damage()  # Returns 40 (30 + 10)
```

**3. Trong trận đấu:**
```python
# Khi nhân vật attack enemy
damage_dealt = self.player.get_effective_damage()  # 40
enemy.take_damage(damage_dealt, self.player)

# Kiếm Rồng có burn effect
if equipment.has_burn_effect:
    enemy.apply_burn(1, 30)  # 1 HP/s for 30s
```

## ✅ Checklist Đồng Bộ

### Khi thêm nhân vật mới:
- [ ] Thêm stats vào `character_stats.py`
- [ ] Stats tự động hiện trong Equipment Screen
- [ ] Stats tự động hiện trong Character Select
- [ ] Không cần sửa code ở 2 file kia!

### Khi thêm equipment mới:
- [ ] Tạo class trong `equipment.py`
- [ ] Set `attack_bonus`, `defense_bonus`, `hp_bonus`, `speed_bonus`
- [ ] Set `has_burn_effect`, `has_slow_effect`, `has_revive_effect` nếu có
- [ ] Thêm vào `EquipmentManager.load_all_equipment()`

### Khi thay đổi stats nhân vật:
- [ ] Chỉ sửa trong `character_stats.py`
- [ ] Thay đổi tự động áp dụng khắp nơi!

## 🐛 Troubleshooting

### Stats không tăng khi lắp trang bị:
**Nguyên nhân**: Equipment chưa được equip đúng cách

**Giải pháp**:
1. Kiểm tra `equipment.equipment_type` khớp với slot type
2. Kiểm tra `player.equip_item()` được gọi
3. Kiểm tra `player.equipped[slot_type]` có equipment chưa

### Stats trong game khác với Equipment Screen:
**Nguyên nhân**: Character Select không load equipment

**Giải pháp**:
1. Kiểm tra profile có lưu `character_equipment` chưa
2. Kiểm tra `_create_player()` có gọi `player.equip_item()` chưa
3. Check console có thông báo "✓ Đã áp dụng trang bị" không

### Equipment bị mất sau khi chơi xong:
**Nguyên nhân**: Không lưu profile

**Giải pháp**:
- Equipment tự động lưu khi equip/unequip trong Equipment Screen
- Nhưng stats trong game KHÔNG lưu lại (chỉ là tạm thời)
- Equipment settings được lưu vào `profiles.json`

## 📝 Code Examples

### Đọc stats trong Equipment Screen:
```python
from ma_nguon.doi_tuong.character_stats import get_character_stats

char_stats = get_character_stats("chien_binh")
base_damage = char_stats['damage']  # 30
```

### Tạo player với equipment:
```python
# Load base stats
stats = selected["stats"]
player.hp = stats["hp"]
player.damage = stats["damage"]

# Load equipment
for slot_type, eq_name in character_equipment.items():
    equipment = eq_manager.get_equipment_by_name(eq_name)
    if equipment:
        player.equip_item(equipment)
```

### Sử dụng stats in-game:
```python
# Luôn dùng get_effective_xxx()
damage = self.player.get_effective_damage()
speed = self.player.get_effective_speed()
max_hp = self.player.get_max_hp_with_equipment()
```

## 🎮 Testing

### Test Equipment Screen:
1. Mở Equipment
2. Chọn nhân vất
3. Xem base stats hiển thị đúng
4. Lắp trang bị
5. Xem bonus và total tính đúng

### Test In-Game:
1. Vào Equipment, lắp Kiếm Rồng cho Chiến binh
2. Quay Menu, chọn Màn 1
3. Chọn Chiến binh
4. Check console: "✓ Đã áp dụng trang bị"
5. Đánh quái → damage = 40 (30+10)
6. Quái bị burn (1 HP/s)

---

**Kết luận**: Hệ thống đã đồng bộ hoàn toàn. Stats được chia sẻ qua `character_stats.py`, equipment được lưu trong profile, và tất cả được áp dụng nhất quán!
