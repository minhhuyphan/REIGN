"""
Test Full Equipment Flow - Từ Equipment Scene đến Character Select
Kiểm tra stats có được áp dụng đúng khi chuyển scene
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from ma_nguon.core.equipment_manager_global import get_global_equipment_manager
from ma_nguon.doi_tuong.equipment import EquipmentManager, Equipment
from ma_nguon.doi_tuong.nhan_vat.nhan_vat import Character
from ma_nguon.core.character_data import get_character_by_id


def test_full_flow():
    """Test toàn bộ flow từ Equipment Scene đến Character Select"""
    print("=" * 70)
    print("TEST: FULL EQUIPMENT FLOW")
    print("=" * 70)
    
    # Clear previous data
    global_mgr = get_global_equipment_manager()
    global_mgr.character_equipment = {}
    global_mgr.save()
    
    print("\n📍 BƯỚC 1: VÀO EQUIPMENT SCENE")
    print("-" * 70)
    
    # Simulate Equipment Scene
    char_data = get_character_by_id("ninja")
    print(f"✓ Chọn nhân vật: {char_data['name']}")
    print(f"  Base stats: HP={char_data['stats']['hp']}, DMG={char_data['stats']['damage']}, SPD={char_data['stats']['speed']}")
    
    # Create character with base stats
    ninja = Character(100, 300, char_data["folder"])
    ninja.hp = char_data["stats"]["hp"]
    ninja.max_hp = char_data["stats"]["hp"]
    ninja.damage = char_data["stats"]["damage"]
    ninja.speed = char_data["stats"]["speed"]
    ninja.defense = char_data["stats"]["defense"]
    
    print(f"\n  Character created: HP={ninja.hp}, DMG={ninja.damage}, SPD={ninja.speed}")
    
    # Equipment Manager
    eq_mgr = EquipmentManager()
    eq_mgr.add_to_inventory("kiem_rong")
    eq_mgr.add_to_inventory("giap_anh_sang")
    eq_mgr.add_to_inventory("giay_thien_than")
    
    print("\n📍 BƯỚC 2: LẮP TRANG BỊ")
    print("-" * 70)
    
    # Equip items
    kiem_rong = eq_mgr.all_equipment["kiem_rong"]
    giap_anh_sang = eq_mgr.all_equipment["giap_anh_sang"]
    giay_thien_than = eq_mgr.all_equipment["giay_thien_than"]
    
    print(f"✓ Lắp Kiếm Rồng (+10 DMG)")
    eq_mgr.equip(kiem_rong, ninja)
    global_mgr.set_equipment("ninja", "weapon", "kiem_rong")
    print(f"  → Stats: HP={ninja.hp}, DMG={ninja.damage}, SPD={ninja.speed}")
    
    print(f"\n✓ Lắp Giáp Ánh Sáng (+200 HP)")
    eq_mgr.equip(giap_anh_sang, ninja)
    global_mgr.set_equipment("ninja", "armor", "giap_anh_sang")
    print(f"  → Stats: HP={ninja.hp}, DMG={ninja.damage}, SPD={ninja.speed}")
    
    print(f"\n✓ Lắp Giày Thiên Thần (+50 HP, +2 SPD)")
    eq_mgr.equip(giay_thien_than, ninja)
    global_mgr.set_equipment("ninja", "boots", "giay_thien_than")
    print(f"  → Stats: HP={ninja.hp}, DMG={ninja.damage}, SPD={ninja.speed}")
    
    final_hp_in_equipment = ninja.hp
    final_dmg_in_equipment = ninja.damage
    final_spd_in_equipment = ninja.speed
    
    print("\n📦 TRANG BỊ ĐÃ LƯU:")
    print(f"  - Weapon: Kiếm Rồng")
    print(f"  - Armor: Giáp Ánh Sáng")
    print(f"  - Boots: Giày Thiên Thần")
    print(f"\n💪 STATS SAU KHI LẮP TRANG BỊ:")
    print(f"  - HP: {final_hp_in_equipment}")
    print(f"  - Damage: {final_dmg_in_equipment}")
    print(f"  - Speed: {final_spd_in_equipment}")
    
    # Simulate going back to menu and then Character Select
    print("\n📍 BƯỚC 3: QUAY LẠI MENU VÀ VÀO CHARACTER SELECT")
    print("-" * 70)
    
    # Create NEW character instance (simulating Character Select)
    char_data = get_character_by_id("ninja")
    ninja_new = Character(100, 300, char_data["folder"])
    ninja_new.hp = char_data["stats"]["hp"]
    ninja_new.max_hp = char_data["stats"]["hp"]
    ninja_new.damage = char_data["stats"]["damage"]
    ninja_new.speed = char_data["stats"]["speed"]
    ninja_new.defense = char_data["stats"]["defense"]
    
    print(f"✓ Chọn nhân vật Ninja trong Character Select")
    print(f"  Base stats: HP={ninja_new.hp}, DMG={ninja_new.damage}, SPD={ninja_new.speed}")
    
    # Create NEW equipment manager
    eq_mgr_new = EquipmentManager()
    
    print(f"\n📍 BƯỚC 4: ÁP DỤNG TRANG BỊ ĐÃ LƯU")
    print("-" * 70)
    
    # Apply saved equipment
    global_mgr.apply_equipment_to_character(ninja_new, "ninja", eq_mgr_new)
    
    print(f"\n💪 STATS SAU KHI ÁP DỤNG TRANG BỊ:")
    print(f"  - HP: {ninja_new.hp}")
    print(f"  - Damage: {ninja_new.damage}")
    print(f"  - Speed: {ninja_new.speed}")
    
    # Verify
    print("\n📍 BƯỚC 5: KIỂM TRA KẾT QUẢ")
    print("-" * 70)
    
    print(f"\n🔍 So sánh stats:")
    print(f"  Equipment Scene → Character Select")
    print(f"  HP:     {final_hp_in_equipment:4d} → {ninja_new.hp:4d}  {'✓' if ninja_new.hp == final_hp_in_equipment else '✗'}")
    print(f"  Damage: {final_dmg_in_equipment:4d} → {ninja_new.damage:4d}  {'✓' if ninja_new.damage == final_dmg_in_equipment else '✗'}")
    print(f"  Speed:  {final_spd_in_equipment:4d} → {ninja_new.speed:4d}  {'✓' if ninja_new.speed == final_spd_in_equipment else '✗'}")
    
    # Final check
    success = (
        ninja_new.hp == final_hp_in_equipment and
        ninja_new.damage == final_dmg_in_equipment and
        ninja_new.speed == final_spd_in_equipment
    )
    
    if success:
        print("\n" + "=" * 70)
        print("✅ TEST PASSED!")
        print("=" * 70)
        print("\n🎉 STATS ĐƯỢC ĐỒNG BỘ HOÀN HẢO!")
        print("\nKhi bạn:")
        print("  1. Lắp trang bị cho Ninja trong Equipment Scene")
        print("  2. Quay lại Menu")
        print("  3. Chọn Ninja trong Character Select để chơi")
        print("\n→ Ninja sẽ có ĐÚNG stats như khi đã lắp trang bị!")
        return 0
    else:
        print("\n" + "=" * 70)
        print("❌ TEST FAILED!")
        print("=" * 70)
        print("\nStats không khớp giữa Equipment Scene và Character Select!")
        return 1


def main():
    try:
        return test_full_flow()
    except Exception as e:
        print(f"\n❌ TEST FAILED WITH ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
