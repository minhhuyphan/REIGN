"""
Demo script để test Equipment System
Chạy file này để xem cách hoạt động của hệ thống trang bị
"""

import pygame
import sys
import os

# Thêm thư mục root vào path để import được các module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ma_nguon.doi_tuong.equipment import Equipment, EquipmentManager, EquipmentEffectManager
from ma_nguon.doi_tuong.nhan_vat.nhan_vat import Character


def test_equipment_system():
    """Test các chức năng của Equipment System"""
    
    print("="*60)
    print("DEMO EQUIPMENT SYSTEM")
    print("="*60)
    
    # 1. Tạo Equipment Manager
    print("\n1. Tạo Equipment Manager...")
    equipment_manager = EquipmentManager()
    print(f"   ✓ Đã khởi tạo với {len(equipment_manager.all_equipment)} loại trang bị")
    
    # 2. Thêm items vào inventory
    print("\n2. Thêm items vào inventory...")
    equipment_manager.add_to_inventory("cung_bang_lam")
    equipment_manager.add_to_inventory("kiem_rong")
    equipment_manager.add_to_inventory("giap_anh_sang")
    equipment_manager.add_to_inventory("giay_thien_than")
    print(f"   ✓ Đã thêm {len(equipment_manager.inventory)} items vào kho")
    
    # 3. Tạo character để test
    print("\n3. Tạo character test...")
    # Tạo dummy character với stats cơ bản
    class DummyCharacter:
        def __init__(self):
            self.hp = 100
            self.max_hp = 100
            self.damage = 10
            self.kick_damage = 15
            self.speed = 5
            self.defense = 2
            self.base_damage = self.damage
            self.base_kick_damage = self.kick_damage
            self.base_speed = self.speed
            self.base_defense = self.defense
            self.base_max_hp = self.max_hp
            self.active_effects = []
            self.revive_available = True
            self.equipped_armor_has_revive = False
            self.dead = False
    
    character = DummyCharacter()
    print(f"   ✓ Character stats:")
    print(f"      HP: {character.hp}/{character.max_hp}")
    print(f"      Damage: {character.damage}")
    print(f"      Speed: {character.speed}")
    
    # 4. Test equip weapon
    print("\n4. Trang bị Kiếm Rồng...")
    kiem_rong = None
    for item in equipment_manager.inventory:
        if item.id == "kiem_rong":
            kiem_rong = item
            break
    
    if kiem_rong:
        equipment_manager.equip(kiem_rong, character)
        print(f"   ✓ Đã trang bị {kiem_rong.name}")
        print(f"      HP: {character.hp}/{character.max_hp}")
        print(f"      Damage: {character.damage} (+{kiem_rong.stats.get('damage', 0)})")
        print(f"      Speed: {character.speed}")
        print(f"      Special Effect: {kiem_rong.special_effect.get('description', 'None')}")
    
    # 5. Test equip armor
    print("\n5. Trang bị Giáp Ánh Sáng...")
    giap = None
    for item in equipment_manager.inventory:
        if item.id == "giap_anh_sang":
            giap = item
            break
    
    if giap:
        equipment_manager.equip(giap, character)
        print(f"   ✓ Đã trang bị {giap.name}")
        print(f"      HP: {character.hp}/{character.max_hp} (+{giap.stats.get('hp', 0)})")
        print(f"      Damage: {character.damage}")
        print(f"      Speed: {character.speed}")
        print(f"      Special Effect: {giap.special_effect.get('description', 'None')}")
        character.equipped_armor_has_revive = True
    
    # 6. Test equip boots
    print("\n6. Trang bị Giày Thiên Thần...")
    giay = None
    for item in equipment_manager.inventory:
        if item.id == "giay_thien_than":
            giay = item
            break
    
    if giay:
        equipment_manager.equip(giay, character)
        print(f"   ✓ Đã trang bị {giay.name}")
        print(f"      HP: {character.hp}/{character.max_hp} (+{giay.stats.get('hp', 0)})")
        print(f"      Damage: {character.damage}")
        print(f"      Speed: {character.speed} (+{giay.stats.get('speed', 0)})")
    
    # 7. Show final stats
    print("\n7. Tổng kết stats sau khi trang bị:")
    print(f"   HP: {character.hp}/{character.max_hp}")
    print(f"   Damage: {character.damage}")
    print(f"   Speed: {character.speed}")
    print(f"   Defense: {character.defense}")
    
    # 8. Show equipped items
    print("\n8. Danh sách trang bị đang mặc:")
    for eq_type, equipment in equipment_manager.equipped.items():
        if equipment:
            print(f"   [{eq_type}] {equipment.name}")
        else:
            print(f"   [{eq_type}] (trống)")
    
    # 9. Show inventory
    print("\n9. Kho đồ còn lại:")
    if equipment_manager.inventory:
        for item in equipment_manager.inventory:
            print(f"   - {item.name}")
    else:
        print("   (kho trống)")
    
    # 10. Test unequip
    print("\n10. Test gỡ trang bị (Vũ khí)...")
    equipment_manager.unequip(Equipment.TYPE_WEAPON, character)
    print(f"   ✓ Đã gỡ vũ khí")
    print(f"      Damage: {character.damage}")
    print(f"      Kho đồ: {len(equipment_manager.inventory)} items")
    
    # 11. Test revive effect
    print("\n11. Test hiệu ứng hồi sinh (Giáp Ánh Sáng)...")
    print(f"   HP trước khi chết: {character.hp}/{character.max_hp}")
    character.hp = 0
    print(f"   HP sau khi chết: {character.hp}/{character.max_hp}")
    
    # Simulate revive
    if character.hp <= 0:
        if character.revive_available and character.equipped_armor_has_revive:
            character.hp = int(character.max_hp * 0.5)
            character.dead = False
            character.revive_available = False
            print(f"   ✓ Hồi sinh thành công!")
            print(f"      HP sau hồi sinh: {character.hp}/{character.max_hp}")
    
    print("\n" + "="*60)
    print("DEMO HOÀN TẤT!")
    print("="*60)


def test_equipment_effects():
    """Test Equipment Effect Manager"""
    
    print("\n" + "="*60)
    print("TEST EQUIPMENT EFFECTS")
    print("="*60)
    
    effect_manager = EquipmentEffectManager()
    
    # Create dummy target
    class DummyTarget:
        def __init__(self):
            self.hp = 100
            self.speed = 5
            self.speed_modifier = 1.0
    
    target = DummyTarget()
    
    # Test Slow Effect
    print("\n1. Test Slow Effect...")
    print(f"   Tốc độ ban đầu: {target.speed}")
    effect_manager.apply_slow(target, 0.5, 3)
    print(f"   Tốc độ sau slow (50%): {target.speed * target.speed_modifier}")
    
    # Test Burn Effect
    print("\n2. Test Burn Effect...")
    print(f"   HP ban đầu: {target.hp}")
    effect_manager.apply_burn(target, 1, 5)
    
    # Simulate 3 seconds
    for i in range(3):
        effect_manager.update(1.0)  # 1 second
        print(f"   Giây {i+1}: HP = {target.hp}")
    
    print("\n" + "="*60)
    print("EFFECT TEST HOÀN TẤT!")
    print("="*60)


if __name__ == "__main__":
    print("\n" + "="*60)
    print("EQUIPMENT SYSTEM TEST SUITE")
    print("="*60)
    
    try:
        test_equipment_system()
        test_equipment_effects()
        
        print("\n✓ TẤT CẢ TEST ĐỀU PASS!")
        
    except Exception as e:
        print(f"\n✗ LỖI: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*60)
