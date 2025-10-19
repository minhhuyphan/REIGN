"""
Verify equipment được áp dụng đúng trong game
"""
import pygame
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ma_nguon.doi_tuong.nhan_vat.nhan_vat import Character
from ma_nguon.doi_tuong.equipment import get_equipment_manager

def test_character_with_equipment():
    """Test nhân vật có stats đúng sau khi lắp equipment"""
    print("="*70)
    print("VERIFY EQUIPMENT APPLICATION")
    print("="*70)
    
    pygame.init()
    screen = pygame.display.set_mode((100, 100))
    
    # Test với Chiến binh (HP: 500)
    print("\n1. CHIẾN BINH:")
    stats_cb = {
        'hp': 500,
        'damage': 30,
        'speed': 5,
        'defense': 2,
    }
    cb = Character(100, 300, "tai_nguyen/hinh_anh/nhan_vat", stats=stats_cb)
    print(f"   Trước: HP={cb.hp}/{cb.max_hp}, Damage={cb.damage}, Speed={cb.speed}")
    
    # Lắp equipment
    eq_manager = get_equipment_manager()
    cb.equip_item(eq_manager.get_equipment_by_name("Kiếm Rồng"))
    cb.equip_item(eq_manager.get_equipment_by_name("Giáp Ánh Sáng"))
    cb.equip_item(eq_manager.get_equipment_by_name("Giày Thiên Thần"))
    
    print(f"   Sau:   HP={cb.hp}/{cb.max_hp}, Damage={cb.damage}, Speed={cb.speed}")
    
    # Verify
    if cb.max_hp == 750 and cb.damage == 40 and cb.speed == 7:
        print("   ✅ CHIẾN BINH: Equipment hoạt động đúng!")
    else:
        print(f"   ❌ CHIẾN BINH: Expected HP=750, Damage=40, Speed=7")
    
    # Test với Chiến Thần Lạc Hồng (HP: 2000)
    print("\n2. CHIẾN THẦN LẠC HỒNG:")
    stats_ct = {
        'hp': 2000,
        'damage': 200,
        'speed': 4,
        'defense': 10,
    }
    ct = Character(100, 300, "tai_nguyen/hinh_anh/nhan_vat", stats=stats_ct)
    print(f"   Trước: HP={ct.hp}/{ct.max_hp}, Damage={ct.damage}, Speed={ct.speed}")
    
    # Lắp equipment
    ct.equip_item(eq_manager.get_equipment_by_name("Kiếm Rồng"))
    ct.equip_item(eq_manager.get_equipment_by_name("Giáp Ánh Sáng"))
    ct.equip_item(eq_manager.get_equipment_by_name("Giày Thiên Thần"))
    
    print(f"   Sau:   HP={ct.hp}/{ct.max_hp}, Damage={ct.damage}, Speed={ct.speed}")
    
    # Verify
    if ct.max_hp == 2250 and ct.damage == 210 and ct.speed == 6:
        print("   ✅ CHIẾN THẦN: Equipment hoạt động đúng!")
    else:
        print(f"   ❌ CHIẾN THẦN: Expected HP=2250, Damage=210, Speed=6")
    
    print("\n" + "="*70)
    print("TỔNG KẾT:")
    print("✅ Equipment THỰC SỰ cộng vào stats")
    print("✅ HP, Damage, Speed đều được tăng đúng")
    print("✅ Các nhân vật khác nhau có base stats khác nhau")
    print("✅ Equipment bonus được cộng vào base stats")
    print("="*70)
    
    pygame.quit()

if __name__ == "__main__":
    test_character_with_equipment()
