"""
Fix indentation errors caused by auto-update script
Chạy: python fix_indentation.py
"""
import os
import re

def fix_map_file(file_path):
    """Fix indentation issues in map files"""
    print(f"Fixing {file_path}...")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix common indentation issues from auto-update
        fixes = [
            # Fix broken if-else statements
            (
                r'if event\.type == pygame\.KEYDOWN:\s*# Skill activation.*?\n\s*# Universal skill handling\s*\nif self\.handle_universal_skill_input\(event\):',
                '''if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.change_scene("menu")
                
        # Universal skill handling
        if self.handle_universal_skill_input(event):'''
            ),
            # Fix broken else statements
            (
                r'el# Universal skill handling\s*\nif self\.handle_universal_skill_input\(event\):',
                '''
        # Universal skill handling
        if self.handle_universal_skill_input(event):'''
            ),
            # Fix misplaced function calls
            (
                r'\s+self\.on_skill_finish\(\)\s*\ndef ',
                '''
    def '''
            ),
            # Fix update method issues
            (
                r'# Universal skill system update\s*\nif self\.update_universal_skills\(\):\s*\nreturn  # Pause game if skill video is playing\s*\nif self\.showing_skill_video and self\.skill_video:',
                '''# Universal skill system update
        if self.update_universal_skills():
            return  # Pause game if skill video is playing'''
            ),
        ]
        
        for pattern, replacement in fixes:
            if re.search(pattern, content, re.DOTALL):
                content = re.sub(pattern, replacement, content, flags=re.DOTALL)
                print(f"  ✅ Applied fix: {pattern[:50]}...")
        
        # Additional manual fixes for specific cases
        
        # Fix broken skill video update patterns
        if 'if self.showing_skill_video and self.skill_video:' in content and 'if self.update_universal_skills():' in content:
            # Remove duplicate skill video handling
            content = re.sub(
                r'if self\.showing_skill_video and self\.skill_video:\s*\n\s*self\.skill_video\.update\(\)\s*\n\s*return',
                '',
                content
            )
        
        # Ensure proper indentation for class methods
        lines = content.split('\n')
        fixed_lines = []
        in_class = False
        
        for i, line in enumerate(lines):
            if line.strip().startswith('class ') and line.strip().endswith(':'):
                in_class = True
                fixed_lines.append(line)
            elif in_class and line.strip().startswith('def ') and not line.startswith('    def '):
                # Fix method indentation
                fixed_lines.append('    ' + line.strip())
            elif in_class and line.strip() and not line.startswith(' ') and not line.strip().startswith('class '):
                # Fix class content indentation
                if not line.strip().startswith('import') and not line.strip().startswith('from'):
                    fixed_lines.append('    ' + line.strip())
                else:
                    in_class = False
                    fixed_lines.append(line)
            else:
                fixed_lines.append(line)
        
        content = '\n'.join(fixed_lines)
        
        # Only write if content changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ Fixed {file_path}")
            return True
        else:
            print(f"  ℹ️ No fixes needed for {file_path}")
            return False
            
    except Exception as e:
        print(f"  ❌ Error fixing {file_path}: {e}")
        return False

def main():
    """Fix all map files with indentation issues"""
    print("🔧 FIXING INDENTATION ERRORS")
    print("=" * 40)
    
    # Files that might have issues
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
    
    fixed_count = 0
    for map_file in map_files:
        if os.path.exists(map_file):
            if fix_map_file(map_file):
                fixed_count += 1
        else:
            print(f"⚠️ File not found: {map_file}")
    
    print(f"\n✅ COMPLETED: Fixed {fixed_count} files")
    print("🎮 Try running the game again!")

if __name__ == "__main__":
    main()