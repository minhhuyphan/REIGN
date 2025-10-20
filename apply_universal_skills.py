"""
Script để tự động apply universal skill system cho tất cả maps
Chạy: python apply_universal_skills.py
"""
import os
import sys

# Add root directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def update_map_file(file_path):
    """Update một map file để sử dụng universal skill system"""
    print(f"Updating {file_path}...")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if already updated
        if 'BaseMapScene' in content:
            print(f"  ✅ {file_path} đã được update")
            return True
        
        # Add import
        if 'from ma_nguon.man_choi.skill_video import SkillVideoPlayer' in content:
            content = content.replace(
                'from ma_nguon.man_choi.skill_video import SkillVideoPlayer',
                'from ma_nguon.man_choi.skill_video import SkillVideoPlayer\nfrom ma_nguon.man_choi.base_map_scene import BaseMapScene'
            )
        elif 'from ma_nguon.tien_ich.bullet_handler import update_bullets, draw_bullets' in content:
            content = content.replace(
                'from ma_nguon.tien_ich.bullet_handler import update_bullets, draw_bullets',
                'from ma_nguon.tien_ich.bullet_handler import update_bullets, draw_bullets\nfrom ma_nguon.man_choi.base_map_scene import BaseMapScene'
            )
        else:
            # Add import at the end of imports
            import_pos = content.find('\nclass ')
            if import_pos != -1:
                content = content[:import_pos] + '\nfrom ma_nguon.man_choi.base_map_scene import BaseMapScene' + content[import_pos:]
        
        # Update class declaration
        class_patterns = [
            ('class Level2Scene:', 'class Level2Scene(BaseMapScene):'),
            ('class MapNinjaScene:', 'class MapNinjaScene(BaseMapScene):'),
            ('class mapninjaman1Scene:', 'class mapninjaman1Scene(BaseMapScene):'),
            ('class MapMuaThuScene:', 'class MapMuaThuScene(BaseMapScene):'),
            ('class MapMuaThuMan1Scene:', 'class MapMuaThuMan1Scene(BaseMapScene):'),
            ('class MapMuaThuMan2Scene:', 'class MapMuaThuMan2Scene(BaseMapScene):'),
            ('class MapMuaThuMan3Scene:', 'class MapMuaThuMan3Scene(BaseMapScene):'),
            ('class MapCongNgheScene:', 'class MapCongNgheScene(BaseMapScene):'),
        ]
        
        for old_class, new_class in class_patterns:
            if old_class in content:
                content = content.replace(old_class, new_class)
                
                # Add super().__init__() call
                init_pattern = f'    def __init__(self, game'
                if init_pattern in content:
                    # Find the line after __init__ definition
                    init_pos = content.find(init_pattern)
                    if init_pos != -1:
                        # Find the next line after __init__(...)
                        next_line_pos = content.find('\n        ', init_pos + len(init_pattern))
                        if next_line_pos != -1:
                            # Insert super().__init__() before the first line in __init__
                            content = (content[:next_line_pos + 1] + 
                                     '        super().__init__()  # Initialize BaseMapScene\n' + 
                                     content[next_line_pos + 1:])
                break
        
        # Replace skill handling in handle_event
        skill_patterns = [
            # Pattern 1: F key check với chien_than_lac_hong
            (
                r'if event\.key == pygame\.K_f and "chien_than_lac_hong" in self\.player\.folder:.*?\n.*?else:.*?\n.*?print\(f".*?"\)',
                '# Universal skill handling\n        if self.handle_universal_skill_input(event):\n            return  # Skill was handled'
            ),
            # Pattern 2: Simple F key check
            (
                r'if event\.key == pygame\.K_f:.*?\n.*?else:.*?\n.*?print\(f".*?"\)',
                '# Universal skill handling\n        if self.handle_universal_skill_input(event):\n            return  # Skill was handled'
            )
        ]
        
        import re
        for pattern, replacement in skill_patterns:
            if re.search(pattern, content, re.DOTALL):
                content = re.sub(pattern, replacement, content, flags=re.DOTALL)
                break
        
        # Replace skill video update
        if 'if self.showing_skill_video and self.skill_video:' in content:
            content = content.replace(
                'if self.showing_skill_video and self.skill_video:\n            self.skill_video.update()\n            return',
                '# Universal skill system update\n        if self.update_universal_skills():\n            return  # Pause game if skill video is playing'
            )
        
        # Replace skill UI drawing
        if 'self.draw_skill_ui(screen)' in content:
            content = content.replace(
                'self.draw_skill_ui(screen)',
                'self.draw_universal_skill_ui(screen)'
            )
        
        # Add get_all_enemies method if not exists
        if 'def get_all_enemies(self):' not in content:
            # Find a good place to add the method (before draw method usually)
            draw_pos = content.rfind('\n    def draw(self, screen):')
            if draw_pos != -1:
                get_enemies_method = '''
    def get_all_enemies(self):
        """Lấy tất cả enemies để truyền cho skill system"""
        all_enemies = []
        if hasattr(self, 'normal_enemies'):
            all_enemies.extend(self.normal_enemies)
        if hasattr(self, 'current_boss') and self.current_boss:
            all_enemies.append(self.current_boss)
        return all_enemies
'''
                content = content[:draw_pos] + get_enemies_method + content[draw_pos:]
        
        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"  ✅ Updated {file_path}")
        return True
        
    except Exception as e:
        print(f"  ❌ Error updating {file_path}: {e}")
        return False

def main():
    """Apply universal skill system to all map files"""
    print("🔧 APPLYING UNIVERSAL SKILL SYSTEM TO ALL MAPS")
    print("=" * 50)
    
    # Map files to update
    map_files = [
        "ma_nguon/man_choi/man2.py",
        "ma_nguon/man_choi/map_ninja.py", 
        "ma_nguon/man_choi/map_ninja_man1.py",
        "ma_nguon/man_choi/map_mua_thu.py",
        "ma_nguon/man_choi/map_mua_thu_man1.py",
        "ma_nguon/man_choi/map_mua_thu_man2.py",
        "ma_nguon/man_choi/map_mua_thu_man3.py",
        "ma_nguon/man_choi/map_cong_nghe.py",
    ]
    
    updated_count = 0
    for map_file in map_files:
        if os.path.exists(map_file):
            if update_map_file(map_file):
                updated_count += 1
        else:
            print(f"  ⚠️ File not found: {map_file}")
    
    print(f"\n✅ HOÀN THÀNH: Updated {updated_count}/{len(map_files)} files")
    print("\n📋 Skill system giờ đây hoạt động universal trên tất cả maps!")
    print("   - Chiến binh có skill phân thân ở mọi map")
    print("   - Chiến Thần Lạc Hồng có skill video ở mọi map") 
    print("   - Dễ dàng thêm skill mới cho nhân vật khác")

if __name__ == "__main__":
    main()