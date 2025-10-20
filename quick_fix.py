"""
Quick fix for all indentation errors in map files
"""
import os
import glob

def quick_fix_file(file_path):
    """Quick fix common indentation issues"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # Pattern 1: Fix broken if statements
        patterns = [
            # Pattern: if event.type == pygame.KEYDOWN:\n                        # comment\n            # Universal skill handling
            (
                'if event.type == pygame.KEYDOWN:\n                        # Skill activation - F key (chỉ cho Chiến Thần Lạc Hồng)\n            # Universal skill handling\n        if self.handle_universal_skill_input(event):',
                '''if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.change_scene("menu")
                
        # Universal skill handling
        if self.handle_universal_skill_input(event):'''
            ),
            
            # Pattern: el# Universal skill handling
            (
                'el# Universal skill handling\n        if self.handle_universal_skill_input(event):',
                '''
        # Universal skill handling
        if self.handle_universal_skill_input(event):'''
            ),
            
            # Pattern: broken if with comment
            (
                'if event.type == pygame.KEYDOWN:\n            # Skill activation - F key (chỉ cho Chiến Thần Lạc Hồng)\n            # Universal skill handling\n        if self.handle_universal_skill_input(event):',
                '''if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.change_scene("menu")
                
        # Universal skill handling
        if self.handle_universal_skill_input(event):'''
            ),
        ]
        
        for old_pattern, new_pattern in patterns:
            if old_pattern in content:
                content = content.replace(old_pattern, new_pattern)
                print(f"  ✅ Fixed pattern in {file_path}")
                
        # Write back if changed
        if content != original:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
            
    except Exception as e:
        print(f"  ❌ Error in {file_path}: {e}")
    
    return False

def main():
    print("🔧 QUICK FIX FOR INDENTATION ERRORS")
    print("=" * 40)
    
    # Find all map files
    map_files = glob.glob("ma_nguon/man_choi/map_*.py") + glob.glob("ma_nguon/man_choi/man*.py")
    
    fixed = 0
    for file_path in map_files:
        print(f"Checking {file_path}...")
        if quick_fix_file(file_path):
            fixed += 1
            
    print(f"\n✅ Fixed {fixed} files")

if __name__ == "__main__":
    main()