"""
Test Equipment Synchronization
Kiểm tra đồng bộ hóa trang bị giữa Equipment Scene và Character Select
"""

import os
import sys
import json

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from ma_nguon.core.equipment_manager_global import get_global_equipment_manager
from ma_nguon.doi_tuong.equipment import EquipmentManager, Equipment
from ma_nguon.doi_tuong.nhan_vat.nhan_vat import Character


def test_save_and_load():
    """Test save equipment and load for character"""
    print("=" * 60)
    print("TEST 1: Save and Load Equipment")
    print("=" * 60)
    
    # Get global manager
    global_mgr = get_global_equipment_manager()
    
    # Clear previous data
    global_mgr.data = {}
    global_mgr.save()
    
    # Save equipment for Ninja
    print("\n1. Saving equipment for Ninja...")
    global_mgr.set_equipment("ninja", Equipment.TYPE_WEAPON, "kiem_rong")
    global_mgr.set_equipment("ninja", Equipment.TYPE_ARMOR, "giap_anh_sang")
    
    # Save equipment for Warrior
    print("2. Saving equipment for Warrior...")
    global_mgr.set_equipment("chien_binh", Equipment.TYPE_BOOTS, "giay_thien_than")
    
    # Verify saved
    print("\n3. Verifying saved data...")
    ninja_eq = global_mgr.get_all_equipment("ninja")
    warrior_eq = global_mgr.get_all_equipment("chien_binh")
    
    print(f"   Ninja equipment: {ninja_eq}")
    print(f"   Warrior equipment: {warrior_eq}")
    
    assert ninja_eq["weapon"] == "kiem_rong", "Ninja weapon should be kiem_rong"
    assert ninja_eq["armor"] == "giap_anh_sang", "Ninja armor should be giap_anh_sang"
    assert warrior_eq["boots"] == "giay_thien_than", "Warrior boots should be giay_thien_than"
    
    print("\n✓ Save and load test PASSED")
    return True


def test_apply_equipment():
    """Test applying saved equipment to character"""
    print("\n" + "=" * 60)
    print("TEST 2: Apply Equipment to Character")
    print("=" * 60)
    
    # Get global manager
    global_mgr = get_global_equipment_manager()
    
    # Create character
    print("\n1. Creating Ninja character...")
    ninja = Character(100, 300, "Tai_nguyen/hinh_anh/nhan_vat/ninja")
    ninja.hp = 800
    ninja.max_hp = 800
    ninja.damage = 35
    ninja.speed = 7
    
    print(f"   Base stats - HP: {ninja.hp}, Damage: {ninja.damage}, Speed: {ninja.speed}")
    
    # Create equipment manager with items in inventory
    eq_mgr = EquipmentManager()
    # Add all items to inventory first
    for item_id in ["kiem_rong", "giap_anh_sang", "cung_bang_lam", "giay_thien_than"]:
        eq_mgr.add_to_inventory(item_id)
    
    # Apply saved equipment
    print("\n2. Applying saved equipment to Ninja...")
    global_mgr.apply_equipment_to_character(ninja, "ninja", eq_mgr)
    
    print(f"   After equipment - HP: {ninja.hp}, Damage: {ninja.damage}, Speed: {ninja.speed}")
    
    # Verify stats changed
    assert ninja.damage == 45, f"Damage should be 45 (35 + 10 from Kiếm Rồng), got {ninja.damage}"
    assert ninja.hp == 1000, f"HP should be 1000 (800 + 200 from Giáp Ánh Sáng), got {ninja.hp}"
    
    # Verify equipment is equipped
    weapon = eq_mgr.get_equipped_by_type(Equipment.TYPE_WEAPON)
    armor = eq_mgr.get_equipped_by_type(Equipment.TYPE_ARMOR)
    
    assert weapon is not None and weapon.id == "kiem_rong", "Kiếm Rồng should be equipped"
    assert armor is not None and armor.id == "giap_anh_sang", "Giáp Ánh Sáng should be equipped"
    
    print("\n✓ Apply equipment test PASSED")
    return True


def test_persistence():
    """Test that equipment persists across sessions"""
    print("\n" + "=" * 60)
    print("TEST 3: Persistence Across Sessions")
    print("=" * 60)
    
    # First session: save equipment
    print("\n1. Session 1 - Saving equipment...")
    mgr1 = get_global_equipment_manager()
    mgr1.data = {}  # Clear
    mgr1.set_equipment("vo_si", Equipment.TYPE_WEAPON, "cung_bang_lam")
    mgr1.set_equipment("vo_si", Equipment.TYPE_ARMOR, "giap_anh_sang")
    mgr1.save()
    
    # Simulate new session: create new manager instance
    print("\n2. Session 2 - Loading equipment...")
    # Force reload by clearing singleton
    from ma_nguon.core import equipment_manager_global
    equipment_manager_global._global_equipment_manager = None
    
    mgr2 = get_global_equipment_manager()
    vo_si_eq = mgr2.get_all_equipment("vo_si")
    
    print(f"   Loaded equipment for Võ Sĩ: {vo_si_eq}")
    
    assert vo_si_eq["weapon"] == "cung_bang_lam", "Weapon should persist"
    assert vo_si_eq["armor"] == "giap_anh_sang", "Armor should persist"
    
    print("\n✓ Persistence test PASSED")
    return True


def test_unequip():
    """Test unequipping (setting to None)"""
    print("\n" + "=" * 60)
    print("TEST 4: Unequip Equipment")
    print("=" * 60)
    
    global_mgr = get_global_equipment_manager()
    
    # Equip first
    print("\n1. Equipping weapon...")
    global_mgr.set_equipment("ninja", Equipment.TYPE_WEAPON, "kiem_rong")
    
    eq = global_mgr.get_equipment("ninja", Equipment.TYPE_WEAPON)
    assert eq == "kiem_rong", "Should be equipped"
    
    # Unequip
    print("2. Unequipping weapon...")
    global_mgr.set_equipment("ninja", Equipment.TYPE_WEAPON, None)
    
    eq = global_mgr.get_equipment("ninja", Equipment.TYPE_WEAPON)
    assert eq is None, "Should be None after unequip"
    
    print("\n✓ Unequip test PASSED")
    return True


def test_multiple_characters():
    """Test that different characters have separate equipment"""
    print("\n" + "=" * 60)
    print("TEST 5: Multiple Characters Independence")
    print("=" * 60)
    
    global_mgr = get_global_equipment_manager()
    
    # Clear all data and reload
    global_mgr.character_equipment = {}
    global_mgr.save()
    global_mgr.load()
    
    # Equip different items to different characters
    print("\n1. Equipping different characters...")
    global_mgr.set_equipment("chien_binh", Equipment.TYPE_WEAPON, "kiem_rong")
    global_mgr.set_equipment("ninja", Equipment.TYPE_WEAPON, "cung_bang_lam")
    global_mgr.set_equipment("vo_si", Equipment.TYPE_ARMOR, "giap_anh_sang")
    
    # Verify each character has correct equipment
    print("2. Verifying each character's equipment...")
    assert global_mgr.get_equipment("chien_binh", Equipment.TYPE_WEAPON) == "kiem_rong"
    assert global_mgr.get_equipment("ninja", Equipment.TYPE_WEAPON) == "cung_bang_lam"
    assert global_mgr.get_equipment("vo_si", Equipment.TYPE_ARMOR) == "giap_anh_sang"
    
    # Verify other slots are None
    assert global_mgr.get_equipment("chien_binh", Equipment.TYPE_ARMOR) is None
    assert global_mgr.get_equipment("ninja", Equipment.TYPE_ARMOR) is None
    
    print("\n✓ Multiple characters test PASSED")
    return True


def verify_save_file():
    """Verify the JSON save file structure"""
    print("\n" + "=" * 60)
    print("BONUS: Verify Save File Structure")
    print("=" * 60)
    
    save_path = "du_lieu/save/character_equipment.json"
    
    if os.path.exists(save_path):
        with open(save_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"\nSave file contents:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        print("\n✓ Save file structure is valid")
    else:
        print("\n! Save file not created yet (will be created on first save)")


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("EQUIPMENT SYNCHRONIZATION TEST SUITE")
    print("=" * 60)
    
    tests = [
        test_save_and_load,
        test_apply_equipment,
        test_persistence,
        test_unequip,
        test_multiple_characters
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"\n✗ Test FAILED: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    # Verify save file
    try:
        verify_save_file()
    except Exception as e:
        print(f"\n! Save file verification failed: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Total tests: {len(tests)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print("\n✓ ALL TESTS PASSED!")
        print("\nEquipment synchronization is working correctly!")
        print("You can now:")
        print("1. Go to Equipment Scene from menu")
        print("2. Select a character and equip items")
        print("3. Go to Character Select and choose that character")
        print("4. The character will start with the equipped items!")
    else:
        print("\n✗ SOME TESTS FAILED")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
