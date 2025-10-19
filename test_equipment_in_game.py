"""
Test equipment bonuses hiển thị và áp dụng trong game
"""
import pygame
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ma_nguon.doi_tuong.nhan_vat.nhan_vat import Character
from ma_nguon.doi_tuong.equipment import get_equipment_manager

def test_equipment_stats():
    """Test equipment bonuses được áp dụng đúng"""
    print("="*70)
    print("TEST EQUIPMENT STATS IN GAME")
    print("="*70)
    
    # Initialize pygame (minimal)
    pygame.init()
    screen = pygame.display.set_mode((100, 100))
    
    # 1. Tạo character với base stats
    print("\n1. Tạo nhân vật Chiến binh:")
    stats = {
        'hp': 500,
        'damage': 30,
        'speed': 5,
        'defense': 2,
        'kick_damage': 20,
        'max_mana': 200,
        'mana_regen': 5
    }
    player = Character(100, 300, "tai_nguyen/hinh_anh/nhan_vat", stats=stats)
    print(f"   Base HP: {player.hp}/{player.max_hp}")
    print(f"   Base Damage: {player.damage}")
    print(f"   Base Speed: {player.speed}")
    
    # 2. Equip trang bị
    print("\n2. Lắp trang bị:")
    eq_manager = get_equipment_manager()
    
    # Equip Kiếm Rồng (+10 damage)
    kiem_rong = eq_manager.get_equipment_by_name("Kiếm Rồng")
    if kiem_rong and player.equip_item(kiem_rong):
        print(f"   ✓ Lắp {kiem_rong.name} -> +{kiem_rong.attack_bonus} Damage")
    
    # Equip Giáp Ánh Sáng (+200 HP)
    giap = eq_manager.get_equipment_by_name("Giáp Ánh Sáng")
    if giap and player.equip_item(giap):
        print(f"   ✓ Lắp {giap.name} -> +{giap.hp_bonus} HP")
    
    # Equip Giày Thiên Thần (+2 speed, +50 HP)
    giay = eq_manager.get_equipment_by_name("Giày Thiên Thần")
    if giay and player.equip_item(giay):
        print(f"   ✓ Lắp {giay.name} -> +{giay.speed_bonus} Speed, +{giay.hp_bonus} HP")
    
    # 3. Kiểm tra stats sau khi equip
    print("\n3. Stats sau khi lắp trang bị:")
    max_hp = player.get_max_hp_with_equipment()
    damage = player.get_effective_damage()
    speed = player.get_effective_speed()
    
    print(f"   Max HP: {player.max_hp} + {max_hp - player.max_hp} = {max_hp}")
    print(f"   Damage: {player.damage} + {damage - player.damage} = {damage}")
    print(f"   Speed: {player.speed} + {speed - player.speed} = {speed}")
    
    # 4. Test HP recovery (như khi vào màn chơi mới)
    print("\n4. Test hồi máu khi vào màn mới:")
    player.hp = 100  # Giả sử bị thương
    print(f"   HP hiện tại: {player.hp}")
    
    # Simulate màn chơi hồi máu
    max_hp_with_equipment = player.get_max_hp_with_equipment() if hasattr(player, 'get_max_hp_with_equipment') else player.max_hp
    player.hp = max_hp_with_equipment
    print(f"   Sau khi hồi: {player.hp}/{max_hp_with_equipment}")
    
    # 5. Verify kết quả
    print("\n5. Kiểm tra kết quả:")
    expected_hp = 500 + 200 + 50  # base + giáp + giày = 750
    expected_damage = 30 + 10  # base + kiếm = 40
    expected_speed = 5 + 2  # base + giày = 7
    
    results = []
    
    if max_hp == expected_hp:
        print(f"   ✅ Max HP: {max_hp} (expected {expected_hp})")
        results.append(True)
    else:
        print(f"   ❌ Max HP: {max_hp} (expected {expected_hp})")
        results.append(False)
    
    if damage == expected_damage:
        print(f"   ✅ Damage: {damage} (expected {expected_damage})")
        results.append(True)
    else:
        print(f"   ❌ Damage: {damage} (expected {expected_damage})")
        results.append(False)
    
    if speed == expected_speed:
        print(f"   ✅ Speed: {speed} (expected {expected_speed})")
        results.append(True)
    else:
        print(f"   ❌ Speed: {speed} (expected {expected_speed})")
        results.append(False)
    
    if player.hp == expected_hp:
        print(f"   ✅ Current HP: {player.hp} (hồi đầy đúng)")
        results.append(True)
    else:
        print(f"   ❌ Current HP: {player.hp} (expected {expected_hp})")
        results.append(False)
    
    print("\n" + "="*70)
    if all(results):
        print("✅ TẤT CẢ TESTS PASSED - Equipment hoạt động đúng!")
    else:
        print("❌ CÓ LỖI - Equipment chưa hoạt động đúng")
    print("="*70)
    
    pygame.quit()
    return all(results)

if __name__ == "__main__":
    test_equipment_stats()
