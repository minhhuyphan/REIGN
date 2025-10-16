"""
Debug script: Kiểm tra xem các file gameplay có nhận player đúng không
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

print("\n" + "="*80)
print("KIỂM TRA CÁC FILE GAMEPLAY")
print("="*80)

files_to_check = [
    "ma_nguon/man_choi/man1.py",
    "ma_nguon/man_choi/man2.py",
    "ma_nguon/man_choi/map_mua_thu.py",
    "ma_nguon/man_choi/map_mua_thu_man1.py",
    "ma_nguon/man_choi/map_mua_thu_man2.py",
    "ma_nguon/man_choi/map_mua_thu_man3.py",
    "ma_nguon/man_choi/map_cong_nghe.py"
]

print("\n🔍 Kiểm tra từng file xem có ghi đè stats không...\n")

issues = []
for filepath in files_to_check:
    print(f"📄 {filepath}")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check for problematic patterns
        has_player_param = "def __init__(self, game, player=" in content
        
        # Look for lines that override damage/kick_damage OUTSIDE of else block
        lines = content.split('\n')
        problem_found = False
        
        for i, line in enumerate(lines):
            # Skip comments
            if line.strip().startswith('#'):
                continue
                
            # Check if damage is being set unconditionally (not inside else block)
            if 'self.player.damage = ' in line and 'else:' not in lines[max(0, i-5):i]:
                # Check if it's inside "if player:" block
                context = '\n'.join(lines[max(0, i-10):min(len(lines), i+5)])
                if 'if player:' in context and 'else:' not in context[context.index('if player:'):]:
                    problem_found = True
                    issues.append(f"  ❌ Line {i+1}: Ghi đè damage TRONG 'if player:' block!")
                    print(f"  ❌ Line {i+1}: {line.strip()}")
                    
            if 'self.player.kick_damage = ' in line and 'else:' not in lines[max(0, i-5):i]:
                context = '\n'.join(lines[max(0, i-10):min(len(lines), i+5)])
                if 'if player:' in context and 'else:' not in context[context.index('if player:'):]:
                    problem_found = True
                    issues.append(f"  ❌ Line {i+1}: Ghi đè kick_damage TRONG 'if player:' block!")
                    print(f"  ❌ Line {i+1}: {line.strip()}")
        
        if not has_player_param:
            issues.append(f"  ❌ Không có tham số player trong __init__!")
            print(f"  ❌ Không có tham số player trong __init__!")
        elif not problem_found:
            print(f"  ✅ OK - Không ghi đè stats")
            
    except Exception as e:
        print(f"  ⚠️ Lỗi khi đọc file: {e}")
        issues.append(f"  ⚠️ Lỗi: {e}")
    
    print()

print("="*80)
if issues:
    print("❌ CÓ VẤN ĐỀ!")
    print("="*80)
    for issue in issues:
        print(issue)
    print("\nCẦN SỬA:")
    print("- Đảm bảo chỉ set damage/kick_damage trong khối 'else:' (khi tạo player mới)")
    print("- KHÔNG set damage/kick_damage trong khối 'if player:' (khi nhận player từ Character Select)")
else:
    print("✅ TẤT CẢ FILES OK!")
    print("="*80)
    print("\n💡 Nếu vẫn không work, kiểm tra:")
    print("1. File character_equipment.json có đúng trang bị không?")
    print("2. Khi vào game, có thấy debug messages trong console không?")
    print("3. Có chạy đúng từ thư mục REIGN (thư mục con) không?")

print()
