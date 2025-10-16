# Hệ Thống Trang Bị - Equipment System

## Tổng Quan

Hệ thống trang bị cho phép người chơi trang bị đồ để tăng sức mạnh cho nhân vật. Có 3 loại trang bị:
- **Vũ Khí** (Công): Tăng sát thương
- **Giáp** (Thủ): Tăng máu và phòng thủ
- **Giày** (Tốc độ): Tăng tốc độ di chuyển

## Các Trang Bị Có Sẵn

### 1. Cung Băng Lam (Vũ Khí)
- **Vị trí**: `Tai_nguyen/hinh_anh/trang_bi/trang_bi_cong/cung_bang_lam.png`
- **Chỉ số**: +8 Sát Thương
- **Hiệu ứng đặc biệt**: Làm chậm kẻ địch
  - Giảm 50% tốc độ kẻ địch
  - Kéo dài 3 giây

### 2. Kiếm Rồng (Vũ Khí)
- **Vị trí**: `Tai_nguyen/hinh_anh/trang_bi/trang_bi_cong/kiem_rong.png`
- **Chỉ số**: +10 Sát Thương
- **Hiệu ứng đặc biệt**: Thiêu đốt
  - Gây 1 HP sát thương mỗi giây
  - Kéo dài 30 giây

### 3. Giáp Ánh Sáng (Giáp)
- **Vị trí**: `Tai_nguyen/hinh_anh/trang_bi/trang_bi_thu/giap_anh_sang.png`
- **Chỉ số**: +200 HP
- **Hiệu ứng đặc biệt**: Hồi sinh
  - Khi HP giảm về 0, tự động hồi sinh với 50% HP tối đa
  - Cooldown: 120 giây (chỉ sử dụng được 1 lần trong 2 phút)

### 4. Giày Thiên Thần (Giày)
- **Vị trí**: `Tai_nguyen/hinh_anh/trang_bi/trang_bi_toc_chay/giay_thien_than.png`
- **Chỉ số**: 
  - +2 Tốc Độ
  - +50 HP
- **Hiệu ứng đặc biệt**: Tăng tốc độ di chuyển

## Cách Sử Dụng

### Mở UI Trang Bị
1. Từ menu chính, chọn **"Trang bị"**
2. Hoặc nhấn phím **I** (sẽ được thêm trong tương lai) trong game

### Trang Bị Đồ
1. Trong UI Trang Bị, bạn sẽ thấy 2 vùng:
   - **Bên trái**: Các slot trang bị (Vũ Khí, Giáp, Giày)
   - **Bên phải**: Kho đồ (Inventory)

2. **Để trang bị đồ**:
   - Click vào item trong kho đồ (bên phải)
   - Item sẽ tự động được trang bị vào slot phù hợp

3. **Để gỡ trang bị**:
   - Click vào item đã trang bị (bên trái)
   - Item sẽ được chuyển về kho đồ

### Xem Thông Tin Chi Tiết
- Di chuột qua bất kỳ item nào để xem tooltip với:
  - Tên item
  - Loại trang bị
  - Chỉ số tăng thêm
  - Hiệu ứng đặc biệt

## Cấu Trúc Code

### Classes Chính

#### `Equipment` (ma_nguon/doi_tuong/equipment.py)
- Đại diện cho một món trang bị
- Chứa thông tin: tên, loại, hình ảnh, stats, hiệu ứng đặc biệt
- Methods:
  - `apply_to_character(character)`: Áp dụng stats lên nhân vật
  - `remove_from_character(character)`: Gỡ bỏ stats khỏi nhân vật

#### `EquipmentManager` (ma_nguon/doi_tuong/equipment.py)
- Quản lý kho đồ và trang bị đang mặc
- Properties:
  - `inventory`: List các item trong kho
  - `equipped`: Dict các item đang mặc {type: Equipment}
- Methods:
  - `add_to_inventory(equipment_id)`: Thêm item vào kho
  - `equip(equipment, character)`: Trang bị item
  - `unequip(equipment_type, character)`: Gỡ trang bị

#### `EquipmentEffectManager` (ma_nguon/doi_tuong/equipment.py)
- Quản lý các hiệu ứng đặc biệt từ trang bị
- Methods:
  - `apply_slow(target, slow_factor, duration)`: Áp dụng làm chậm
  - `apply_burn(target, damage_per_sec, duration)`: Áp dụng thiêu đốt
  - `trigger_revive(character, equipment_id)`: Kích hoạt hồi sinh
  - `update(dt)`: Cập nhật tất cả effects theo thời gian

#### `EquipmentUI` (ma_nguon/giao_dien/equipment_ui.py)
- Giao diện hiển thị trang bị
- Methods:
  - `toggle()`: Bật/tắt hiển thị
  - `handle_event(event, equipment_manager, character)`: Xử lý input
  - `draw(screen, equipment_manager)`: Vẽ UI

#### `EquipmentScene` (ma_nguon/man_choi/equipment_scene.py)
- Scene riêng để quản lý trang bị
- Tích hợp EquipmentUI và EquipmentManager

## Tích Hợp Vào Game

### Trong Character (ma_nguon/doi_tuong/nhan_vat/nhan_vat.py)
```python
# Thêm vào __init__
self.base_damage = self.damage
self.base_kick_damage = self.kick_damage
self.base_speed = self.speed
self.active_effects = []
self.revive_available = True
self.equipped_armor_has_revive = False

# Trong take_damage method
if self.hp <= 0:
    if self.revive_available and self.equipped_armor_has_revive:
        self.hp = int(self.max_hp * 0.5)
        self.dead = False
        self.revive_available = False
        return
```

### Trong Game Scenes
```python
# Import
from ma_nguon.doi_tuong.equipment import EquipmentManager, EquipmentEffectManager
from ma_nguon.giao_dien.equipment_ui import EquipmentUI

# Trong __init__
if not hasattr(self.game, 'equipment_manager'):
    self.game.equipment_manager = EquipmentManager()
self.equipment_manager = self.game.equipment_manager

if not hasattr(self.game, 'equipment_effect_manager'):
    self.game.equipment_effect_manager = EquipmentEffectManager()
self.effect_manager = self.game.equipment_effect_manager

self.equipment_ui = EquipmentUI(self.game.WIDTH, self.game.HEIGHT)

# Trong handle_event
if event.key == pygame.K_i:
    self.equipment_ui.toggle()

if self.equipment_ui.visible:
    if self.equipment_ui.handle_event(event, self.equipment_manager, self.player):
        return

# Trong update
dt = self.game.clock.get_time() / 1000.0
self.effect_manager.update(dt)

# Trong draw
self.equipment_ui.draw(screen, self.equipment_manager)
```

## Thêm Trang Bị Mới

### Bước 1: Thêm hình ảnh
- Thêm file PNG vào thư mục phù hợp:
  - Vũ khí: `Tai_nguyen/hinh_anh/trang_bi/trang_bi_cong/`
  - Giáp: `Tai_nguyen/hinh_anh/trang_bi/trang_bi_thu/`
  - Giày: `Tai_nguyen/hinh_anh/trang_bi/trang_bi_toc_chay/`

### Bước 2: Thêm vào EquipmentManager
Trong `ma_nguon/doi_tuong/equipment.py`, trong method `_init_all_equipment()`:

```python
"ten_item": Equipment(
    item_id="ten_item",
    name="Tên Hiển Thị",
    item_type=Equipment.TYPE_WEAPON,  # hoặc TYPE_ARMOR, TYPE_BOOTS
    image_path="Tai_nguyen/hinh_anh/trang_bi/.../ten_item.png",
    stats={
        "damage": 15,
        "hp": 100,
        "speed": 3,
        # ...
    },
    special_effect={
        "type": "burn",  # hoặc "slow", "revive", custom
        "description": "Mô tả hiệu ứng",
        # ... params khác
    }
)
```

## Lưu Ý Quan Trọng

1. **Equipment Manager là Global**: Equipment Manager được lưu trong `game.equipment_manager` để duy trì trạng thái giữa các scenes.

2. **Effect Manager**: Effect Manager cũng là global (`game.equipment_effect_manager`) để theo dõi các hiệu ứng đang hoạt động.

3. **Base Stats**: Character lưu cả base stats và stats sau khi trang bị để dễ dàng tính toán khi thay đổi trang bị.

4. **Revive Effect**: Chỉ kích hoạt 1 lần cho đến khi respawn hoặc restart level.

5. **Test Mode**: Trong EquipmentScene, mặc định thêm tất cả items vào inventory để test. Trong production, items sẽ được thu thập từ enemies hoặc mua trong shop.

## Phát Triển Tương Lai

- [ ] Thêm phím tắt I để mở Equipment UI trong game
- [ ] Lưu trang bị vào profile
- [ ] Thêm items vào drops từ boss
- [ ] Thêm items vào shop để mua
- [ ] Thêm animation khi trang bị
- [ ] Thêm sound effects
- [ ] Thêm nhiều trang bị mới
- [ ] Thêm hệ thống nâng cấp trang bị
- [ ] Thêm set bonus (khi trang bị đủ bộ)
