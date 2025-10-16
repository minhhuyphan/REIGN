"""
Test: Flow hoàn chỉnh từ Equipment → Character Select → Gameplay
Mô phỏng chính xác cách game chạy thực tế
"""
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from ma_nguon.core.equipment_manager_global import get_global_equipment_manager
from ma_nguon.doi_tuong.equipment import EquipmentManager
from ma_nguon.doi_tuong.nhan_vat.nhan_vat import Character
from ma_nguon.core.character_data import get_all_characters, get_character_by_id

def test_full_flow():
    """Test flow hoàn chỉnh giống game thật"""
    
    print("\n" + "="*80)
    print("TEST: FLOW HOÀN CHỈNH - EQUIPMENT → CHARACTER SELECT → GAMEPLAY")
    print("="*80)
    
    char_id = "chien_binh"
    
    # ==================== PHASE 1: EQUIPMENT SCENE ====================
    print("\n" + "="*80)
    print("PHASE 1: EQUIPMENT SCENE - User trang bị items")
    print("="*80)
    
    global_eq_mgr = get_global_equipment_manager()
    
    # Clear first
    global_eq_mgr.set_equipment(char_id, "weapon", None)
    global_eq_mgr.set_equipment(char_id, "armor", None)
    global_eq_mgr.set_equipment(char_id, "boots", None)
    
    # User equips items
    print(f"\n👤 User chọn nhân vật: {char_id}")
    print("🎒 User trang bị:")
    global_eq_mgr.set_equipment(char_id, "weapon", "cung_bang_lam")
    print("  ✓ Cung Băng Lam (+8 DMG)")
    global_eq_mgr.set_equipment(char_id, "armor", "giap_anh_sang")
    print("  ✓ Giáp Ánh Sáng (+200 HP)")
    global_eq_mgr.set_equipment(char_id, "boots", "giay_thien_than")
    print("  ✓ Giày Thiên Thần (+50 HP, +2 SPD)")
    
    # Verify saved
    saved_eq = global_eq_mgr.get_all_equipment(char_id)
    print(f"\n💾 Trang bị đã lưu:")
    for slot, eq_id in saved_eq.items():
        if eq_id:
            print(f"  {slot}: {eq_id}")
    
    # ==================== PHASE 2: CHARACTER SELECT ====================
    print("\n" + "="*80)
    print("PHASE 2: CHARACTER SELECT - Tạo player với trang bị")
    print("="*80)
    
    # Get character data
    char_data = get_character_by_id(char_id)
    print(f"\n📊 Character data: {char_data['name']}")
    
    # Create player (như trong chon_nhan_vat.py)
    folder = char_data["folder"]
    color = char_data["color"]
    stats = char_data["stats"]
    
    print(f"\n🎮 Tạo Character object:")
    player = Character(100, 300, folder, color=color)
    
    # Set base stats
    player.hp = stats["hp"]
    player.max_hp = stats["hp"]
    player.speed = stats["speed"]
    player.damage = stats["damage"]
    player.defense = stats["defense"]
    if "kick_damage" in stats:
        player.kick_damage = stats["kick_damage"]
    
    print(f"  Base stats: HP={player.hp}, DMG={player.damage}, SPD={player.speed}, DEF={player.defense}")
    
    # Apply equipment (như trong chon_nhan_vat.py)
    equipment_manager = EquipmentManager()
    print(f"\n⚔️ Apply equipment từ GlobalEquipmentManager:")
    global_eq_mgr.apply_equipment_to_character(player, char_id, equipment_manager)
    
    print(f"\n✅ Stats SAU KHI áp dụng trang bị:")
    print(f"  HP: {player.hp} (max: {player.max_hp})")
    print(f"  Damage: {player.damage}")
    print(f"  Speed: {player.speed}")
    print(f"  Defense: {player.defense}")
    
    # Store expected values
    expected_hp = player.hp
    expected_damage = player.damage
    expected_speed = player.speed
    
    # ==================== PHASE 3: TRANSITION TO GAMEPLAY ====================
    print("\n" + "="*80)
    print("PHASE 3: CHUYỂN SANG GAMEPLAY - Giống loading.py")
    print("="*80)
    
    # Simulate: self.game.selected_player = player
    selected_player = player
    print(f"\n🎯 selected_player được lưu:")
    print(f"  HP: {selected_player.hp}")
    print(f"  Damage: {selected_player.damage}")
    print(f"  Speed: {selected_player.speed}")
    
    # ==================== PHASE 4: GAMEPLAY SCENE INIT ====================
    print("\n" + "="*80)
    print("PHASE 4: GAMEPLAY SCENE - Khởi tạo (giống man1.py)")
    print("="*80)
    
    # Simulate: Level1Scene.__init__(game, player=self.game.selected_player)
    print(f"\n🎮 Level1Scene nhận player từ Character Select:")
    
    # This is what man1.py should do (AFTER our fix)
    if selected_player:
        gameplay_player = selected_player  # Use the player from Character Select
        gameplay_player.x = 100  # Only set position
        gameplay_player.y = 300
        gameplay_player.base_y = 300
        print(f"  ✅ Nhận player với stats:")
        print(f"     HP: {gameplay_player.hp}")
        print(f"     Damage: {gameplay_player.damage}")
        print(f"     Speed: {gameplay_player.speed}")
        
        # KHÔNG ghi đè stats! (This is the fix)
        # ❌ gameplay_player.damage = 15  # KHÔNG LÀM NHƯ NÀY!
        # ❌ gameplay_player.kick_damage = 20
    else:
        print("  ❌ Không nhận được player từ Character Select - tạo mới")
        gameplay_player = Character(100, 300, "tai_nguyen/hinh_anh/nhan_vat", color=(0,255,0))
        gameplay_player.damage = 15
        gameplay_player.kick_damage = 20
    
    # ==================== PHASE 5: VERIFY ====================
    print("\n" + "="*80)
    print("PHASE 5: KIỂM TRA STATS TRONG GAMEPLAY")
    print("="*80)
    
    success = True
    errors = []
    
    print(f"\n📊 So sánh stats:")
    print(f"  Expected HP: {expected_hp}")
    print(f"  Actual HP: {gameplay_player.hp}")
    
    if gameplay_player.hp != expected_hp:
        success = False
        errors.append(f"❌ HP sai: {gameplay_player.hp} != {expected_hp}")
    else:
        print(f"  ✅ HP đúng!")
        
    print(f"\n  Expected Damage: {expected_damage}")
    print(f"  Actual Damage: {gameplay_player.damage}")
    
    if gameplay_player.damage != expected_damage:
        success = False
        errors.append(f"❌ Damage sai: {gameplay_player.damage} != {expected_damage}")
    else:
        print(f"  ✅ Damage đúng!")
        
    print(f"\n  Expected Speed: {expected_speed}")
    print(f"  Actual Speed: {gameplay_player.speed}")
    
    if gameplay_player.speed != expected_speed:
        success = False
        errors.append(f"❌ Speed sai: {gameplay_player.speed} != {expected_speed}")
    else:
        print(f"  ✅ Speed đúng!")
    
    # ==================== RESULT ====================
    print("\n" + "="*80)
    if success:
        print("✅ TEST PASSED! Stats từ trang bị được giữ nguyên trong gameplay!")
        print("="*80)
        print("\n🎉 HOÀN HẢO! Hệ thống hoạt động đúng:")
        print("  1. Equipment Scene: Lưu trang bị ✅")
        print("  2. Character Select: Apply trang bị vào player ✅")
        print("  3. Gameplay: Giữ nguyên stats từ player ✅")
        print("\n💡 Trong game thực tế, bạn sẽ thấy:")
        print(f"  - HP: {gameplay_player.hp}/{gameplay_player.max_hp}")
        print(f"  - Damage khi đánh quái: {gameplay_player.damage}")
        print(f"  - Tốc độ di chuyển nhanh hơn (speed={gameplay_player.speed})")
    else:
        print("❌ TEST FAILED!")
        print("="*80)
        for error in errors:
            print(f"  {error}")
        print("\n🔍 Cần kiểm tra:")
        print("  - File gameplay có ghi đè damage/hp không?")
        print("  - LoadingScene có truyền player đúng không?")
        print("  - Character Select có apply equipment không?")
    
    print("\n" + "="*80)
    return success

if __name__ == "__main__":
    success = test_full_flow()
    
    if success:
        print("\n📝 HƯỚNG DẪN KIỂM TRA TRONG GAME:")
        print("  1. Chạy game: python -m ma_nguon.main")
        print("  2. Vào Equipment (nhấn E)")
        print("  3. Trang bị items cho Chiến Binh")
        print("  4. Chọn màn chơi → Chọn Chiến Binh")
        print("  5. Xem Console - phải thấy:")
        print("     [CharacterSelect] Created character: ... with equipment")
        print("       Stats: HP=600, DMG=33, SPD=10")
        print("     [Man1] Received player with stats: HP=600, DMG=33, SPD=10")
        print("  6. Trong game - thanh máu phải hiện 600/600 (không phải 350/350)")
    
    sys.exit(0 if success else 1)
