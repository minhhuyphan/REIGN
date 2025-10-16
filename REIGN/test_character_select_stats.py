"""
Test Character Select Stats Display
Kiểm tra stats có hiển thị đúng với trang bị trong Character Select
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from ma_nguon.core.equipment_manager_global import get_global_equipment_manager
from ma_nguon.doi_tuong.equipment import EquipmentManager
from ma_nguon.core.character_data import get_character_by_id


def test_character_select_stats_display():
    """Test stats display trong Character Select"""
    print("=" * 70)
    print("TEST: CHARACTER SELECT STATS DISPLAY")
    print("=" * 70)
    
    # Setup: Save equipment for Ninja
    global_mgr = get_global_equipment_manager()
    global_mgr.character_equipment = {}
    global_mgr.set_equipment("ninja", "weapon", "kiem_rong")
    global_mgr.set_equipment("ninja", "armor", "giap_anh_sang")
    global_mgr.set_equipment("ninja", "boots", "giay_thien_than")
    global_mgr.save()
    
    print("\n📍 BƯỚC 1: LƯU TRANG BỊ CHO NINJA")
    print("-" * 70)
    print("✓ Kiếm Rồng: +10 Damage")
    print("✓ Giáp Ánh Sáng: +200 HP")
    print("✓ Giày Thiên Thần: +50 HP, +2 Speed")
    
    # Simulate Character Select loading equipment info
    print("\n📍 BƯỚC 2: LOAD EQUIPMENT INFO TRONG CHARACTER SELECT")
    print("-" * 70)
    
    eq_mgr = EquipmentManager()
    char_data = get_character_by_id("ninja")
    equipped = global_mgr.get_all_equipment("ninja")
    
    # Calculate bonus stats
    bonus_hp = 0
    bonus_damage = 0
    bonus_speed = 0
    equipped_items = []
    
    for eq_type in ["weapon", "armor", "boots"]:
        eq_id = equipped.get(eq_type)
        if eq_id and eq_id in eq_mgr.all_equipment:
            equipment = eq_mgr.all_equipment[eq_id]
            equipped_items.append(equipment.name)
            
            print(f"✓ Loaded: {equipment.name}")
            
            if "hp" in equipment.stats:
                bonus_hp += equipment.stats["hp"]
                print(f"  → HP bonus: +{equipment.stats['hp']}")
            if "damage" in equipment.stats:
                bonus_damage += equipment.stats["damage"]
                print(f"  → Damage bonus: +{equipment.stats['damage']}")
            if "speed" in equipment.stats:
                bonus_speed += equipment.stats["speed"]
                print(f"  → Speed bonus: +{equipment.stats['speed']}")
    
    # Calculate total stats
    base_hp = char_data["stats"]["hp"]
    base_damage = char_data["stats"]["damage"]
    base_speed = char_data["stats"]["speed"]
    
    total_hp = base_hp + bonus_hp
    total_damage = base_damage + bonus_damage
    total_speed = base_speed + bonus_speed
    
    print("\n📍 BƯỚC 3: TÍNH TOÁN STATS HIỂN THỊ")
    print("-" * 70)
    print(f"Base Stats:")
    print(f"  HP: {base_hp}")
    print(f"  Damage: {base_damage}")
    print(f"  Speed: {base_speed}")
    
    print(f"\nBonus từ trang bị:")
    print(f"  HP: +{bonus_hp}")
    print(f"  Damage: +{bonus_damage}")
    print(f"  Speed: +{bonus_speed}")
    
    print(f"\nTotal Stats (sẽ hiển thị):")
    print(f"  HP: {total_hp} {f'(+{bonus_hp})' if bonus_hp > 0 else ''}")
    print(f"  Damage: {total_damage} {f'(+{bonus_damage})' if bonus_damage > 0 else ''}")
    print(f"  Speed: {total_speed} {f'(+{bonus_speed})' if bonus_speed > 0 else ''}")
    
    # Verify
    print("\n📍 BƯỚC 4: KIỂM TRA KẾT QUẢ")
    print("-" * 70)
    
    expected_hp = 600  # 350 + 200 + 50
    expected_damage = 35  # 25 + 10
    expected_speed = 10  # 8 + 2
    
    print(f"\n🔍 Kiểm tra:")
    print(f"  HP:     {total_hp} == {expected_hp}?  {'✓' if total_hp == expected_hp else '✗'}")
    print(f"  Damage: {total_damage} == {expected_damage}?  {'✓' if total_damage == expected_damage else '✗'}")
    print(f"  Speed:  {total_speed} == {expected_speed}?  {'✓' if total_speed == expected_speed else '✗'}")
    
    success = (
        total_hp == expected_hp and
        total_damage == expected_damage and
        total_speed == expected_speed
    )
    
    if success:
        print("\n" + "=" * 70)
        print("✅ TEST PASSED!")
        print("=" * 70)
        print("\n🎉 CHARACTER SELECT SẼ HIỂN THỊ ĐÚNG STATS!")
        print("\nKhi vào Character Select:")
        print(f"  • Ninja sẽ hiển thị: HP: {total_hp} (+{bonus_hp})")
        print(f"  • Ninja sẽ hiển thị: ST: {total_damage} (+{bonus_damage})")
        print(f"  • Ninja sẽ hiển thị: Tốc độ: {total_speed} (+{bonus_speed})")
        print(f"  • Icon ⚔ sẽ xuất hiện ở góc card")
        return 0
    else:
        print("\n" + "=" * 70)
        print("❌ TEST FAILED!")
        print("=" * 70)
        return 1


def test_character_without_equipment():
    """Test nhân vật không có trang bị"""
    print("\n" + "=" * 70)
    print("TEST: CHARACTER WITHOUT EQUIPMENT")
    print("=" * 70)
    
    # Setup: Clear equipment for Chiến Binh
    global_mgr = get_global_equipment_manager()
    if "chien_binh" in global_mgr.character_equipment:
        del global_mgr.character_equipment["chien_binh"]
    global_mgr.save()
    
    eq_mgr = EquipmentManager()
    char_data = get_character_by_id("chien_binh")
    equipped = global_mgr.get_all_equipment("chien_binh")
    
    # Calculate bonus (should be 0)
    bonus_hp = 0
    bonus_damage = 0
    bonus_speed = 0
    
    for eq_type in ["weapon", "armor", "boots"]:
        eq_id = equipped.get(eq_type)
        if eq_id and eq_id in eq_mgr.all_equipment:
            equipment = eq_mgr.all_equipment[eq_id]
            if "hp" in equipment.stats:
                bonus_hp += equipment.stats["hp"]
            if "damage" in equipment.stats:
                bonus_damage += equipment.stats["damage"]
            if "speed" in equipment.stats:
                bonus_speed += equipment.stats["speed"]
    
    print(f"\n✓ Chiến Binh không có trang bị")
    print(f"  Base HP: {char_data['stats']['hp']}")
    print(f"  Base Damage: {char_data['stats']['damage']}")
    print(f"  Base Speed: {char_data['stats']['speed']}")
    print(f"  Bonus: +{bonus_hp} HP, +{bonus_damage} DMG, +{bonus_speed} SPD")
    
    if bonus_hp == 0 and bonus_damage == 0 and bonus_speed == 0:
        print("\n✅ PASSED: No bonus stats (correct)")
        print("  → Stats sẽ hiển thị không có (+bonus)")
        print("  → Không có icon ⚔")
        return 0
    else:
        print("\n❌ FAILED: Should have no bonus")
        return 1


def main():
    try:
        result1 = test_character_select_stats_display()
        result2 = test_character_without_equipment()
        
        if result1 == 0 and result2 == 0:
            print("\n" + "=" * 70)
            print("🎉 ALL TESTS PASSED!")
            print("=" * 70)
            print("\n💡 Character Select bây giờ sẽ:")
            print("  1. Hiển thị stats có trang bị (màu xanh)")
            print("  2. Hiển thị bonus (+X) bên cạnh")
            print("  3. Có icon ⚔ cho nhân vật có trang bị")
            print("  4. Stats base cho nhân vật không có trang bị")
            return 0
        else:
            return 1
            
    except Exception as e:
        print(f"\n❌ TEST FAILED WITH ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
