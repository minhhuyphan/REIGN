"""
Test: Hiệu ứng hồi sinh của Giáp Ánh Sáng
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from ma_nguon.doi_tuong.nhan_vat.nhan_vat import Character
from ma_nguon.doi_tuong.equipment import EquipmentManager
from ma_nguon.core.equipment_manager_global import get_global_equipment_manager
from ma_nguon.core.character_data import get_character_by_id

print("\n" + "="*80)
print("TEST: HIỆU ỨNG HỒI SINH CỦA GIÁP ÁNH SÁNG")
print("="*80)

# Setup
char_data = get_character_by_id("ninja")
print(f"\n👤 Tạo nhân vật: {char_data['name']}")

# Create character
folder = char_data["folder"]
color = char_data["color"]
player = Character(100, 300, folder, color=color)

# Set base stats
stats = char_data["stats"]
player.hp = stats["hp"]
player.max_hp = stats["hp"]
player.speed = stats["speed"]
player.damage = stats["damage"]
player.defense = stats["defense"]

print(f"  Base stats: HP={player.hp}, DMG={player.damage}")
print(f"  revive_available: {player.revive_available}")
print(f"  equipped_armor_has_revive: {player.equipped_armor_has_revive}")

# Equip Giáp Ánh Sáng
print(f"\n⚔️ Trang bị Giáp Ánh Sáng...")
eq_mgr = EquipmentManager()
eq_mgr.add_to_inventory("giap_anh_sang")

giap = eq_mgr.all_equipment["giap_anh_sang"]
eq_mgr.equip(giap, player)

print(f"  Stats after equip: HP={player.hp}/{player.max_hp}")
print(f"  revive_available: {player.revive_available}")
print(f"  equipped_armor_has_revive: {player.equipped_armor_has_revive}")

# Simulate death
print(f"\n💀 Mô phỏng nhân vật chết...")
print(f"  HP trước khi chết: {player.hp}")

# Trigger take_damage to kill character
damage_to_kill = player.hp + 100
print(f"  Gây {damage_to_kill} damage...")
player.take_damage(damage_to_kill, attacker_flip=False)

print(f"\n✨ Kiểm tra kết quả:")
print(f"  HP sau khi chết: {player.hp}")
print(f"  Dead: {player.dead}")
print(f"  revive_available: {player.revive_available}")

# Check results
expected_hp = int(player.max_hp * 0.5)
success = True

if player.dead:
    print(f"\n❌ TEST FAILED!")
    print(f"  Nhân vật vẫn chết! (dead={player.dead})")
    print(f"  HP: {player.hp} (expected: {expected_hp})")
    success = False
elif player.hp != expected_hp:
    print(f"\n⚠️ TEST PARTIALLY FAILED!")
    print(f"  Nhân vật hồi sinh nhưng HP sai!")
    print(f"  HP: {player.hp} (expected: {expected_hp})")
    success = False
elif player.revive_available:
    print(f"\n⚠️ TEST PARTIALLY FAILED!")
    print(f"  Nhân vật hồi sinh nhưng revive_available vẫn = True!")
    print(f"  (Phải = False sau khi dùng)")
    success = False
else:
    print(f"\n✅ TEST PASSED!")
    print(f"  Nhân vật hồi sinh với {player.hp}/{player.max_hp} HP (50%)")
    print(f"  revive_available = False (đã dùng)")

# Test revive only once
print(f"\n🔄 Test revive chỉ hoạt động 1 lần...")
print(f"  Giết nhân vật lần 2...")
player.hp = player.max_hp  # Reset HP
print(f"  HP trước khi chết lần 2: {player.hp}")

player.take_damage(player.hp + 100, attacker_flip=False)

print(f"  HP sau khi chết lần 2: {player.hp}")
print(f"  Dead: {player.dead}")

if player.dead and player.hp <= 0:
    print(f"  ✅ Đúng! Revive chỉ work 1 lần")
else:
    print(f"  ❌ Sai! Revive không nên work lần 2")
    success = False

print("\n" + "="*80)
if success:
    print("🎉 HOÀN THÀNH! Hiệu ứng hồi sinh hoạt động đúng!")
    print("="*80)
    print("\n💡 Trong game thực tế:")
    print("  1. Trang bị Giáp Ánh Sáng cho nhân vật")
    print("  2. Khi HP = 0, nhân vật sẽ hồi sinh với 50% HP")
    print("  3. Hiệu ứng chỉ hoạt động 1 lần cho đến khi restart level")
else:
    print("❌ CÓ LỖI! Cần kiểm tra lại")
    print("="*80)

print()
sys.exit(0 if success else 1)
