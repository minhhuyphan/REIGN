"""
Script để cập nhật tất cả các file map với equipment system
"""
import os
import re

# Danh sách các file cần update
map_files = [
    "ma_nguon/man_choi/man2.py",
    "ma_nguon/man_choi/map_mua_thu.py",
    "ma_nguon/man_choi/map_mua_thu_man2.py",
    "ma_nguon/man_choi/map_mua_thu_man3.py",
    "ma_nguon/man_choi/map_ninja.py",
    "ma_nguon/man_choi/map_ninja_man1.py",
    "ma_nguon/man_choi/map_cong_nghe.py",
    "ma_nguon/man_choi/maprunglinhvuc.py",
]

def update_take_damage_calls(file_path):
    """Update take_damage calls to include attacker parameter"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Pattern 1: enemy.take_damage(self.player.damage, self.player.flip)
        content = re.sub(
            r'enemy\.take_damage\(self\.player\.damage, self\.player\.flip\)',
            'enemy.take_damage(self.player.get_effective_damage(), self.player.flip, self.player)',
            content
        )
        
        # Pattern 2: enemy.take_damage(self.player.kick_damage, self.player.flip)
        content = re.sub(
            r'enemy\.take_damage\(self\.player\.kick_damage, self\.player\.flip\)',
            'enemy.take_damage(self.player.kick_damage, self.player.flip, self.player)',
            content
        )
        
        # Pattern 3: boss variations
        content = re.sub(
            r'(self\.current_boss|boss)\.take_damage\(self\.player\.damage, self\.player\.flip\)',
            r'\1.take_damage(self.player.get_effective_damage(), self.player.flip, self.player)',
            content
        )
        
        content = re.sub(
            r'(self\.current_boss|boss)\.take_damage\(self\.player\.kick_damage, self\.player\.flip\)',
            r'\1.take_damage(self.player.kick_damage, self.player.flip, self.player)',
            content
        )
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Updated {file_path}")
            return True
        else:
            print(f"- No changes needed for {file_path}")
            return False
            
    except Exception as e:
        print(f"✗ Error updating {file_path}: {e}")
        return False

if __name__ == "__main__":
    print("Updating map files with equipment system support...\n")
    
    updated_count = 0
    for file_path in map_files:
        if update_take_damage_calls(file_path):
            updated_count += 1
    
    print(f"\n✓ Updated {updated_count} files")
    print("✓ Equipment system integration complete!")
