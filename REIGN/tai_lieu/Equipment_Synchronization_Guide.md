# Hướng Dẫn Đồng Bộ Trang Bị (Equipment Synchronization)

## Tổng Quan

Hệ thống đồng bộ trang bị cho phép trang bị được lựa chọn trong **Equipment Scene** sẽ tự động được áp dụng khi chọn nhân vật trong **Character Select Scene**.

### Luồng Hoạt Động

```
Equipment Scene → Chọn nhân vật → Lắp trang bị → Lưu vào file
                                                      ↓
Character Select → Chọn nhân vật → Load trang bị từ file → Áp dụng vào nhân vật
```

## Các Thành Phần Chính

### 1. GlobalEquipmentManager

**File**: `ma_nguon/core/equipment_manager_global.py`

Lớp này quản lý việc lưu trữ và tải trang bị cho từng nhân vật.

#### Phương Thức Chính

##### `set_equipment(character_id, equipment_type, equipment_id)`
Lưu trang bị cho nhân vật cụ thể.

**Tham số**:
- `character_id`: ID nhân vật ("chien_binh", "ninja", "vo_si", "chien_than_lac_hong", "tho_san_quai_vat")
- `equipment_type`: Loại trang bị ("weapon", "armor", "boots")
- `equipment_id`: ID trang bị hoặc None để gỡ bỏ

**Ví dụ**:
```python
global_mgr = get_global_equipment_manager()
global_mgr.set_equipment("ninja", "weapon", "kiem_rong")
global_mgr.set_equipment("ninja", "armor", "giap_anh_sang")
```

##### `get_equipment(character_id, equipment_type)`
Lấy ID trang bị đã lưu cho nhân vật.

**Ví dụ**:
```python
weapon_id = global_mgr.get_equipment("ninja", "weapon")
# Returns: "kiem_rong"
```

##### `get_all_equipment(character_id)`
Lấy tất cả trang bị của nhân vật.

**Trả về**: Dictionary với keys "weapon", "armor", "boots"

**Ví dụ**:
```python
equipment = global_mgr.get_all_equipment("ninja")
# Returns: {'weapon': 'kiem_rong', 'armor': 'giap_anh_sang', 'boots': None}
```

##### `apply_equipment_to_character(character, character_id, equipment_manager)`
Áp dụng trang bị đã lưu lên nhân vật.

**Tham số**:
- `character`: Instance của Character
- `character_id`: ID nhân vật
- `equipment_manager`: Instance của EquipmentManager

**Chức năng**:
- Tải trang bị đã lưu từ file
- Equip các item vào character
- Áp dụng stats bonus
- Kích hoạt special effects

### 2. EquipmentUI Callback

**File**: `ma_nguon/giao_dien/equipment_ui.py`

Có property `on_equipment_change` để thông báo khi trang bị thay đổi.

**Signature**: `on_equipment_change(character_id, equipment_type, equipment_id)`

**Được gọi khi**:
- Người chơi equip một item từ inventory
- Người chơi unequip một item đã trang bị

### 3. EquipmentScene Integration

**File**: `ma_nguon/man_choi/equipment_scene.py`

#### Khởi Tạo
```python
# Tạo global equipment manager
self.global_eq_manager = get_global_equipment_manager()

# Theo dõi nhân vật hiện tại
self.current_character_id = "chien_binh"

# Set callback
self.equipment_ui.on_equipment_change = self._on_equipment_change
```

#### Callback Handler
```python
def _on_equipment_change(self, character_id, equipment_type, equipment_id):
    """Lưu khi trang bị thay đổi"""
    self.global_eq_manager.set_equipment(character_id, equipment_type, equipment_id)
```

#### Character Selection
```python
def _select_character(self, char_data):
    # Tạo nhân vật mới
    self.player = Character(...)
    
    # Update current character ID
    self.current_character_id = char_data["id"]
    
    # Load và áp dụng trang bị đã lưu
    self.global_eq_manager.apply_equipment_to_character(
        self.player,
        self.current_character_id,
        self.equipment_manager
    )
```

### 4. CharacterSelectScene Integration

**File**: `ma_nguon/man_choi/chon_nhan_vat.py`

```python
def _create_player(self):
    selected = self.characters[self.selected_idx]
    
    # Tạo nhân vật
    player = Character(...)
    
    # Áp dụng trang bị đã lưu
    global_eq_manager = get_global_equipment_manager()
    if not hasattr(self.game, 'equipment_manager'):
        self.game.equipment_manager = EquipmentManager()
    
    global_eq_manager.apply_equipment_to_character(
        player,
        selected["id"],
        self.game.equipment_manager
    )
    
    self.game.selected_player = player
```

## Cấu Trúc File Lưu

**Đường dẫn**: `du_lieu/save/character_equipment.json`

### Cấu Trúc
```json
{
  "chien_binh": {
    "weapon": "kiem_rong",
    "armor": null,
    "boots": "giay_thien_than"
  },
  "ninja": {
    "weapon": "cung_bang_lam",
    "armor": "giap_anh_sang",
    "boots": null
  },
  "vo_si": {
    "weapon": null,
    "armor": "giap_anh_sang",
    "boots": null
  }
}
```

### Đặc Điểm
- **Persistence**: Tự động lưu mỗi khi có thay đổi
- **Per-character**: Mỗi nhân vật có trang bị riêng
- **Null values**: Slot không có trang bị = null
- **Encoding**: UTF-8 with indent=2

## Hướng Dẫn Sử Dụng

### Cho Người Chơi

1. **Vào Equipment Scene**
   - Từ Menu, chọn "Trang bị"

2. **Chọn Nhân Vật**
   - Click nút "Chọn Nhân Vật"
   - Chọn nhân vật muốn trang bị

3. **Lắp Trang Bị**
   - Click vào item trong Inventory để lắp
   - Click vào item đã lắp để gỡ bỏ
   - Xem stats preview khi hover

4. **Chơi Game**
   - Quay lại Menu (ESC)
   - Chọn "Chơi" → Chọn màn → Chọn nhân vật
   - Nhân vật sẽ có trang bị đã lắp!

### Cho Developer

#### Thêm Trang Bị Mới

1. **Thêm hình ảnh**: `Tai_nguon/hinh_anh/trang_bi/item_id.png`

2. **Thêm vào Equipment class**:
```python
# In equipment.py
all_equipment = {
    "item_id": Equipment(
        id="item_id",
        name="Tên Item",
        type=Equipment.TYPE_WEAPON,  # or TYPE_ARMOR, TYPE_BOOTS
        image_path="Tai_nguyen/hinh_anh/trang_bi/item_id.png",
        stats={"damage": 15, "hp": 50},
        special_effect={}
    )
}
```

3. **Add to inventory** (trong EquipmentScene hoặc khi boss drop):
```python
equipment_manager.add_to_inventory("item_id")
```

#### Debug Equipment

```python
# In Python console hoặc debug script
from ma_nguon.core.equipment_manager_global import get_global_equipment_manager

mgr = get_global_equipment_manager()

# Xem trang bị của nhân vật
print(mgr.get_all_equipment("ninja"))

# Set trang bị thủ công
mgr.set_equipment("ninja", "weapon", "kiem_rong")

# Clear trang bị
mgr.character_equipment = {}
mgr.save()
```

## Kiểm Tra (Testing)

Chạy test suite:
```bash
python test_equipment_sync.py
```

### Test Cases

1. **Save and Load**: Verify equipment is saved and loaded correctly
2. **Apply Equipment**: Verify stats are applied to character
3. **Persistence**: Verify data persists across sessions
4. **Unequip**: Verify unequipping sets to None
5. **Multiple Characters**: Verify each character has independent equipment

## Troubleshooting

### Trang Bị Không Được Lưu

**Nguyên nhân**: Callback không được set
**Giải pháp**: Kiểm tra `equipment_ui.on_equipment_change` đã được gán

### Trang Bị Không Load Khi Chơi

**Nguyên nhân**: Không gọi `apply_equipment_to_character` trong Character Select
**Giải pháp**: Kiểm tra `_create_player()` có gọi hàm apply

### File JSON Bị Lỗi

**Nguyên nhân**: File bị corrupt hoặc format sai
**Giải pháp**: 
```python
# Xóa file và tạo lại
import os
os.remove("du_lieu/save/character_equipment.json")
# Khởi động lại game
```

### Stats Không Đúng

**Nguyên nhân**: Equipment chưa được equip qua EquipmentManager
**Giải pháp**: Đảm bảo dùng `equipment_manager.equip()` chứ không chỉ `apply_to_character()`

## Best Practices

### 1. Luôn Use EquipmentManager
```python
# ✓ ĐÚNG
equipment_manager.equip(equipment, character)

# ✗ SAI - Chỉ áp stats, không track state
equipment.apply_to_character(character)
```

### 2. Check Inventory Trước Khi Apply
```python
# Ensure items exist in inventory
for item_id in ["kiem_rong", "giap_anh_sang"]:
    if item_id not in [eq.id for eq in equipment_manager.inventory]:
        equipment_manager.add_to_inventory(item_id)
```

### 3. Sync Character ID
```python
# Đảm bảo current_character_id match với character đang sử dụng
self.current_character_id = selected["id"]
```

### 4. Handle Missing Equipment
```python
# Trong apply_equipment_to_character, có check:
if eq_id in equipment_manager.all_equipment:
    # Apply
else:
    # Log warning
```

## Tương Lai

### Planned Features
- [ ] Hotkey (I) để mở Equipment UI trong game
- [ ] Boss drops equipment items
- [ ] Shop để mua trang bị
- [ ] Trang bị có level requirement
- [ ] Upgrade equipment system
- [ ] Set bonuses (equip 3 items from same set)

### API Extensions
```python
# Planned methods
global_mgr.get_equipped_items_as_objects(character_id)  # Return Equipment objects
global_mgr.can_equip(character_id, equipment_id)  # Check requirements
global_mgr.get_character_power_level(character_id)  # Calculate total power
```

## Tham Khảo

- **Equipment System Guide**: `tai_lieu/Equipment_System_Guide.md`
- **Main Equipment Code**: `ma_nguon/doi_tuong/equipment.py`
- **UI Code**: `ma_nguon/giao_dien/equipment_ui.py`
- **Test Suite**: `test_equipment_sync.py`

---

**Last Updated**: 2024
**Version**: 1.0
**Author**: REIGN Development Team
