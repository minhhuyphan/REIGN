"""
Quick test: So sánh Ninja (có equipment) vs Chiến Binh (không có equipment)
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from ma_nguon.core.equipment_manager_global import get_global_equipment_manager
from ma_nguon.doi_tuong.equipment import EquipmentManager
from ma_nguon.core.character_data import get_character_by_id

print("\n" + "="*80)
print("KIỂM TRA TRANG BỊ CỦA TỪNG NHÂN VẬT")
print("="*80)

global_eq_mgr = get_global_equipment_manager()
eq_mgr = EquipmentManager()

characters = ["chien_binh", "ninja", "vo_si"]

for char_id in characters:
    char_data = get_character_by_id(char_id)
    print(f"\n👤 {char_data['name']} ({char_id}):")
    print("-" * 40)
    
    # Get base stats
    stats = char_data["stats"]
    print(f"  Base stats:")
    print(f"    HP: {stats['hp']}")
    print(f"    Damage: {stats['damage']}")
    print(f"    Speed: {stats['speed']}")
    
    # Get equipment
    equipped = global_eq_mgr.get_all_equipment(char_id)
    
    has_equipment = False
    bonus_hp = 0
    bonus_damage = 0
    bonus_speed = 0
    
    print(f"\n  Equipment:")
    for slot, eq_id in equipped.items():
        if eq_id and eq_id in eq_mgr.all_equipment:
            equipment = eq_mgr.all_equipment[eq_id]
            has_equipment = True
            print(f"    {slot}: ✅ {equipment.name}")
            
            if "hp" in equipment.stats:
                bonus_hp += equipment.stats["hp"]
            if "damage" in equipment.stats:
                bonus_damage += equipment.stats["damage"]
            if "speed" in equipment.stats:
                bonus_speed += equipment.stats["speed"]
        else:
            print(f"    {slot}: ❌ Không có")
    
    if has_equipment:
        print(f"\n  💪 Stats với equipment:")
        print(f"    HP: {stats['hp']} + {bonus_hp} = {stats['hp'] + bonus_hp}")
        print(f"    Damage: {stats['damage']} + {bonus_damage} = {stats['damage'] + bonus_damage}")
        print(f"    Speed: {stats['speed']} + {bonus_speed} = {stats['speed'] + bonus_speed}")
        print(f"\n  ✅ Nhân vật này CÓ TRANG BỊ - test với nhân vật này!")
    else:
        print(f"\n  ❌ Nhân vật này KHÔNG CÓ TRANG BỊ - cần vào Equipment Scene để trang bị!")

print("\n" + "="*80)
print("💡 KẾT LUẬN:")
print("="*80)

# Count characters with equipment
chars_with_eq = []
chars_without_eq = []

for char_id in characters:
    equipped = global_eq_mgr.get_all_equipment(char_id)
    has_eq = any(eq_id and eq_id in eq_mgr.all_equipment 
                 for eq_id in equipped.values())
    if has_eq:
        char_data = get_character_by_id(char_id)
        chars_with_eq.append(char_data['name'])
    else:
        char_data = get_character_by_id(char_id)
        chars_without_eq.append(char_data['name'])

if chars_with_eq:
    print(f"\n✅ Nhân vật có trang bị: {', '.join(chars_with_eq)}")
    print(f"   → TEST VỚI NHÂN VẬT NÀY để xem stats từ trang bị!")

if chars_without_eq:
    print(f"\n❌ Nhân vật không có trang bị: {', '.join(chars_without_eq)}")
    print(f"   → Vào Equipment Scene (nhấn E) để trang bị!")

print("\n🎮 HƯỚNG DẪN TEST:")
if chars_with_eq:
    print(f"  1. Chạy game: python -m ma_nguon.main")
    print(f"  2. Chọn màn chơi → Chọn {chars_with_eq[0]}")
    print(f"  3. Xem thanh máu trong game - phải CAO HƠN base stats!")
else:
    print(f"  1. Chạy game: python -m ma_nguon.main")
    print(f"  2. Nhấn E vào Equipment Scene")
    print(f"  3. Trang bị items cho nhân vật bất kỳ")
    print(f"  4. ESC → Chọn màn chơi → Chọn nhân vật đó")
    print(f"  5. Xem stats trong game!")

print()
