"""Test script để kiểm tra special effects của equipment"""

from ma_nguon.doi_tuong.items import EQUIPMENT_DATA
from ma_nguon.doi_tuong.equipment import EquipmentManager

def test_special_effects():
    """Test xem special effects có được set đúng không"""
    
    print("="*70)
    print("TEST SPECIAL EFFECTS CỦA EQUIPMENT")
    print("="*70)
    
    # Test legendary items
    legendary_items = {k: v for k, v in EQUIPMENT_DATA.items() if v.get('rarity') == 'legendary'}
    
    print(f"\nTìm thấy {len(legendary_items)} legendary items:\n")
    
    for item_name, item_data in legendary_items.items():
        effects = item_data.get('effects', [])
        print(f"📌 {item_name}")
        print(f"   Type: {item_data.get('type')}")
        print(f"   Effects: {effects}")
        
        # Tạo equipment object để test
        eq_manager = EquipmentManager()
        eq = eq_manager._create_equipment_from_data(item_name, item_data)
        
        # Check flags
        flags = []
        if hasattr(eq, 'has_burn_effect') and eq.has_burn_effect:
            flags.append("✓ has_burn_effect")
        if hasattr(eq, 'has_slow_effect') and eq.has_slow_effect:
            flags.append("✓ has_slow_effect")
        if hasattr(eq, 'has_revive_effect') and eq.has_revive_effect:
            flags.append("✓ has_revive_effect")
        if hasattr(eq, 'has_double_jump') and eq.has_double_jump:
            flags.append("✓ has_double_jump")
        
        if flags:
            print(f"   Flags set: {', '.join(flags)}")
        else:
            print(f"   ⚠️ WARNING: Không có flags nào được set!")
        
        print()
    
    print("="*70)
    print("SUMMARY")
    print("="*70)
    
    print("\n🔥 BURN EFFECT (Kiếm Rồng):")
    print("   - Gây thêm 2 damage/giây trong 30 frames")
    print("   - Áp dụng cho enemy khi player tấn công")
    print("   - Code: enemy.apply_burn(damage, duration)")
    
    print("\n❄️  SLOW EFFECT (Cung Băng Lãm):")
    print("   - Làm chậm enemy xuống 50% tốc độ trong 2 giây")
    print("   - Áp dụng khi player tấn công")
    print("   - Code: enemy.apply_slow(duration)")
    
    print("\n✨ REVIVE EFFECT (Giáp Ánh Sáng):")
    print("   - Hồi sinh 1 lần khi HP xuống 0")
    print("   - Hồi 50% max HP")
    print("   - Code: if equipment.has_revive_effect -> player.hp = max_hp * 0.5")
    
    print("\n🦘 DOUBLE JUMP (Giày Thiên Thần):")
    print("   - Cho phép nhảy 2 lần trên không")
    print("   - max_jumps = 2 khi có equipment")
    print("   - jump_count track số lần đã nhảy")
    
    print("\n" + "="*70)
    print("✓ TEST COMPLETE")
    print("="*70)

if __name__ == "__main__":
    test_special_effects()
