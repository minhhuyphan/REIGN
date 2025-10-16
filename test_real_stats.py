"""
Test equipment bonuses được cộng TRỰC TIẾP vào stats
"""
import pygame
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ma_nguon.doi_tuong.nhan_vat.nhan_vat import Character
from ma_nguon.doi_tuong.equipment import get_equipment_manager

def test_real_stats():
    """Test equipment cộng trực tiếp vào stats"""
    print("="*70)
    print("TEST EQUIPMENT BONUSES - STATS THỰC")
    print("="*70)
    
    pygame.init()
    screen = pygame.display.set_mode((100, 100))
    
    # 1. Tạo character
    print("\n1. Tạo nhân vật với base stats:")
    stats = {
        'hp': 500,
        'damage': 30,
        'speed': 5,
        'defense': 2,
    }
    player = Character(100, 300, "tai_nguyen/hinh_anh/nhan_vat", stats=stats)
    
    print(f"   HP: {player.hp}/{player.max_hp}")
    print(f"   Damage: {player.damage}")
    print(f"   Speed: {player.speed}")
    print(f"   Defense: {player.defense}")
    
    # 2. Lắp trang bị
    print("\n2. Lắp Kiếm Rồng (+10 Damage):")
    eq_manager = get_equipment_manager()
    kiem_rong = eq_manager.get_equipment_by_name("Kiếm Rồng")
    player.equip_item(kiem_rong)
    
    print(f"   HP: {player.hp}/{player.max_hp} (không đổi)")
    print(f"   Damage: {player.damage} (phải là 40)")
    print(f"   Speed: {player.speed} (không đổi)")
    
    # 3. Lắp Giáp Ánh Sáng (+200 HP)
    print("\n3. Lắp Giáp Ánh Sáng (+200 HP):")
    giap = eq_manager.get_equipment_by_name("Giáp Ánh Sáng")
    player.equip_item(giap)
    
    print(f"   HP: {player.hp}/{player.max_hp} (max phải là 700)")
    print(f"   Damage: {player.damage} (vẫn 40)")
    
    # 4. Lắp Giày Thiên Thần (+2 Speed, +50 HP)
    print("\n4. Lắp Giày Thiên Thần (+2 Speed, +50 HP):")
    giay = eq_manager.get_equipment_by_name("Giày Thiên Thần")
    player.equip_item(giay)
    
    print(f"   HP: {player.hp}/{player.max_hp} (max phải là 750)")
    print(f"   Damage: {player.damage} (vẫn 40)")
    print(f"   Speed: {player.speed} (phải là 7)")
    
    # 5. Verify
    print("\n5. KIỂM TRA KẾT QUẢ:")
    tests_passed = []
    
    # Check max HP
    if player.max_hp == 750:
        print(f"   ✅ Max HP = {player.max_hp} (ĐÚNG)")
        tests_passed.append(True)
    else:
        print(f"   ❌ Max HP = {player.max_hp} (expected 750)")
        tests_passed.append(False)
    
    # Check damage
    if player.damage == 40:
        print(f"   ✅ Damage = {player.damage} (ĐÚNG)")
        tests_passed.append(True)
    else:
        print(f"   ❌ Damage = {player.damage} (expected 40)")
        tests_passed.append(False)
    
    # Check speed
    if player.speed == 7:
        print(f"   ✅ Speed = {player.speed} (ĐÚNG)")
        tests_passed.append(True)
    else:
        print(f"   ❌ Speed = {player.speed} (expected 7)")
        tests_passed.append(False)
    
    # 6. Test unequip
    print("\n6. GỠ Kiếm Rồng:")
    player.unequip_item('attack')
    print(f"   Damage: {player.damage} (phải về 30)")
    
    if player.damage == 30:
        print(f"   ✅ Damage reset về {player.damage} (ĐÚNG)")
        tests_passed.append(True)
    else:
        print(f"   ❌ Damage = {player.damage} (expected 30)")
        tests_passed.append(False)
    
    print("\n" + "="*70)
    if all(tests_passed):
        print("✅ TẤT CẢ TESTS PASSED - Stats thực sự được cộng!")
        print("Equipment bây giờ cộng TRỰC TIẾP vào player.damage, player.speed, player.max_hp")
    else:
        print("❌ CÓ LỖI - Cần kiểm tra lại")
    print("="*70)
    
    pygame.quit()
    return all(tests_passed)

if __name__ == "__main__":
    test_real_stats()
