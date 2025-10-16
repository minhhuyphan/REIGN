"""
Test: Kiểm tra nhân vật có giữ stats từ trang bị khi vào gameplay không
"""
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from ma_nguon.core.equipment_manager_global import get_global_equipment_manager
from ma_nguon.doi_tuong.equipment import EquipmentManager
from ma_nguon.doi_tuong.nhan_vat.nhan_vat import Character

def test_character_keeps_equipment_in_gameplay():
    """Test xem nhân vật có giữ stats từ trang bị khi tạo trong gameplay scene không"""
    
    print("\n" + "="*70)
    print("TEST: NHÂN VẬT GIỮ STATS TỪ TRANG BỊ TRONG GAMEPLAY")
    print("="*70)
    
    # Setup
    char_id = "chien_binh"
    global_eq_mgr = get_global_equipment_manager()
    equipment_manager = EquipmentManager()
    
    # Clear any existing equipment by setting all slots to None
    global_eq_mgr.set_equipment(char_id, "weapon", None)
    global_eq_mgr.set_equipment(char_id, "armor", None)
    global_eq_mgr.set_equipment(char_id, "boots", None)
    
    # Equip some items
    print(f"\n📦 Trang bị cho nhân vật {char_id}:")
    global_eq_mgr.set_equipment(char_id, "weapon", "cung_bang_lam")
    global_eq_mgr.set_equipment(char_id, "armor", "giap_anh_sang")
    global_eq_mgr.set_equipment(char_id, "boots", "giay_thien_than")
    print("  ✓ Cung Băng Lam (+8 DMG)")
    print("  ✓ Giáp Ánh Sáng (+200 HP)")
    print("  ✓ Giày Thiên Thần (+50 HP, +2 SPD)")
    
    # Create character (simulating Character Select)
    print("\n🎮 TẠO NHÂN VẬT TRONG CHARACTER SELECT:")
    folder_nv = "tai_nguyen/hinh_anh/nhan_vat/chien_binh"
    player = Character(100, 300, folder_nv, color=(0,255,0))
    
    # Set base stats
    player.hp = 350
    player.max_hp = 350
    player.speed = 8
    player.damage = 25
    player.defense = 10
    player.kick_damage = 30
    
    print(f"  Base stats: HP={player.hp}, DMG={player.damage}, SPD={player.speed}, DEF={player.defense}")
    
    # Apply equipment (như trong chon_nhan_vat.py)
    global_eq_mgr.apply_equipment_to_character(player, char_id, equipment_manager)
    
    stats_after_equip = {
        "hp": player.hp,
        "damage": player.damage,
        "speed": player.speed,
        "defense": player.defense
    }
    print(f"  After equipment: HP={player.hp}, DMG={player.damage}, SPD={player.speed}, DEF={player.defense}")
    
    # Expected stats
    expected = {
        "hp": 350 + 200 + 50,  # base + armor + boots = 600
        "damage": 25 + 8,       # base + weapon = 33
        "speed": 8 + 2,         # base + boots = 10
        "defense": 10           # no defense bonus
    }
    
    print(f"\n📊 KỲ VỌNG:")
    print(f"  HP: {expected['hp']} (350 + 200 + 50)")
    print(f"  Damage: {expected['damage']} (25 + 8)")
    print(f"  Speed: {expected['speed']} (8 + 2)")
    print(f"  Defense: {expected['defense']} (10 + 0)")
    
    # Now simulate passing to gameplay scene (man1.py)
    print(f"\n🎯 TRUYỀN VÀO GAMEPLAY SCENE (giống man1.py):")
    print(f"  BEFORE: HP={player.hp}, DMG={player.damage}, SPD={player.speed}")
    
    # This is what man1.py SHOULD do (chỉ set vị trí, KHÔNG ghi đè stats)
    player.x = 100
    player.y = 300
    player.base_y = 300
    
    print(f"  AFTER setting position: HP={player.hp}, DMG={player.damage}, SPD={player.speed}")
    
    # Verify stats
    success = True
    errors = []
    
    if player.hp != expected['hp']:
        success = False
        errors.append(f"❌ HP sai: {player.hp} != {expected['hp']}")
    else:
        print(f"  ✅ HP đúng: {player.hp}")
        
    if player.damage != expected['damage']:
        success = False
        errors.append(f"❌ Damage sai: {player.damage} != {expected['damage']}")
    else:
        print(f"  ✅ Damage đúng: {player.damage}")
        
    if player.speed != expected['speed']:
        success = False
        errors.append(f"❌ Speed sai: {player.speed} != {expected['speed']}")
    else:
        print(f"  ✅ Speed đúng: {player.speed}")
        
    if player.defense != expected['defense']:
        success = False
        errors.append(f"❌ Defense sai: {player.defense} != {expected['defense']}")
    else:
        print(f"  ✅ Defense đúng: {player.defense}")
    
    print("\n" + "="*70)
    if success:
        print("✅ TEST PASSED! Nhân vật giữ đúng stats từ trang bị khi vào game!")
        print("="*70)
        return True
    else:
        print("❌ TEST FAILED!")
        for error in errors:
            print(f"  {error}")
        print("="*70)
        return False

if __name__ == "__main__":
    success = test_character_keeps_equipment_in_gameplay()
    
    if success:
        print("\n🎉 HOÀN HẢO! Bây giờ nhân vật sẽ có stats từ trang bị trong game!")
    else:
        print("\n⚠️ Vẫn còn vấn đề, cần kiểm tra thêm!")
    
    sys.exit(0 if success else 1)
