"""
Equipment Loader - Helper để load và apply trang bị cho nhân vật trong mọi map
"""
import os
from ma_nguon.doi_tuong.equipment import get_equipment_manager


def load_and_apply_equipment(player, game, map_name="MAP"):
    """
    Load trang bị từ profile và apply stats vào player
    
    Args:
        player: Đối tượng nhân vật
        game: Game instance (để lấy current_user)
        map_name: Tên map (để log)
    """
    # Kiểm tra xem equipment đã được apply chưa (từ chon_nhan_vat.py)
    if hasattr(player, '_equipment_applied') and player._equipment_applied:
        print(f"[{map_name}] Equipment đã được apply trước đó, skip")
        return
    
    try:
        from ma_nguon.core import profile_manager
        
        # Get current user
        user = getattr(game, 'current_user', None)
        if not user:
            print(f"[{map_name}] Không có user, skip load equipment")
            return
        
        # Load profile
        profile = profile_manager.load_profile(user)
        
        # Get player character ID (dựa vào folder name hoặc character_id)
        player_char_id = getattr(player, 'character_id', None)
        if player_char_id:
            print(f"[{map_name}] Character ID: {player_char_id}")
        else:
            # Nếu không có, thử lấy từ folder
            if hasattr(player, 'folder_animations'):
                folder_name = os.path.basename(player.folder_animations)
                player_char_id = folder_name
            elif hasattr(player, 'folder'):
                # Lấy từ folder path
                folder_name = os.path.basename(player.folder)
                player_char_id = folder_name
            else:
                print(f"[{map_name}] Không xác định được character ID")
                return
        
        # Load equipment manager
        equipment_manager = get_equipment_manager()
        
        # Load inventory from profile
        inventory = profile.get('equipment_inventory', {})
        if inventory:
            equipment_manager.load_inventory_from_profile(inventory)
        
        # Load character equipment
        character_equipment = profile.get('character_equipment', {})
        if character_equipment:
            for char_id, equipment_data in character_equipment.items():
                equipment_manager.load_character_equipment(char_id, equipment_data)
        
        # Get equipment for this character
        char_equipment = equipment_manager.get_character_equipment(player_char_id)
        
        if not char_equipment:
            print(f"[{map_name}] Nhân vật {player_char_id} chưa có trang bị")
            return
        
        # Apply stats bonuses
        total_attack = 0
        total_hp = 0
        total_speed = 0
        
        # Special effects
        has_revive = False
        has_slow = False
        has_burn = False
        
        for slot_type, eq_name in char_equipment.items():
            eq = equipment_manager.get_equipment_by_name(eq_name)
            if eq:
                total_attack += eq.attack_bonus
                total_hp += eq.hp_bonus
                total_speed += eq.speed_bonus
                
                # Check special effects
                if eq.has_revive_effect:
                    has_revive = True
                
                if eq.has_slow_effect:
                    has_slow = True
                
                if eq.has_burn_effect:
                    has_burn = True
        
        # Apply to player stats
        if total_attack > 0:
            player.damage += total_attack
            if hasattr(player, 'kick_damage'):
                player.kick_damage += total_attack
        
        if total_hp > 0:
            player.max_hp += total_hp
            player.hp += total_hp
        
        if total_speed > 0:
            player.speed += total_speed
        
        # Apply special effects to player
        if has_revive:
            player.has_revive = True
            player.revive_used = False
            player.revive_hp_percent = 50  # Hồi sinh với 50% HP
            print(f"[{map_name}] Kích hoạt HỒI SINH - Revive 50% HP")
        
        if has_slow:
            player.attacks_slow_enemies = True  # Đánh chậm địch
            print(f"[{map_name}] Kích hoạt LÀM CHẬM - Giảm 50% tốc độ địch 3s")
        
        if has_burn:
            player.attacks_burn_enemies = True  # Đánh thiêu địch
            player.burn_damage = 1  # 1 HP/giây
            player.burn_duration = 30  # 30 giây
            print(f"[{map_name}] Kích hoạt THIÊU ĐỐT - 1 DMG/giây x 30s")
        
        print(f"[{map_name}] Đã áp dụng trang bị: DMG+{total_attack}, HP+{total_hp}, SPD+{total_speed}")
        
        # Đánh dấu đã apply equipment
        player._equipment_applied = True
        
    except Exception as e:
        print(f"[{map_name}] Lỗi khi load equipment: {e}")
        import traceback
        traceback.print_exc()
