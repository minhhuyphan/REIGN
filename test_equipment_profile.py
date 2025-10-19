"""
Test script cho equipment system với character selection và profile saving
"""
import json
import os

def test_equipment_profile_flow():
    """Test equipment save/load flow"""
    print("=" * 60)
    print("TEST EQUIPMENT SYSTEM WITH PROFILE")
    print("=" * 60)
    
    # 1. Test profile structure
    print("\n1. Kiểm tra cấu trúc profile...")
    profile_example = {
        'gold': 500,
        'purchased_characters': ['chien_binh', 'ninja'],
        'character_equipment': {
            'chien_binh': {
                'attack': 'Cung Băng Lãm',
                'defense': 'Giáp Ánh Sáng',
                'speed': None
            },
            'ninja': {
                'attack': 'Kiếm Rồng',
                'defense': None,
                'speed': 'Giày Thiên Thần'
            }
        }
    }
    print("✓ Cấu trúc profile mẫu:")
    print(json.dumps(profile_example, indent=2, ensure_ascii=False))
    
    # 2. Test equipment manager
    print("\n2. Kiểm tra Equipment Manager...")
    try:
        import sys
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from ma_nguon.doi_tuong.equipment import get_equipment_manager
        
        eq_manager = get_equipment_manager()
        print(f"✓ Equipment Manager khởi tạo thành công")
        print(f"✓ Số trang bị có sẵn: {len(eq_manager.get_all_equipment())}")
        
        # Test equip cho character
        eq = eq_manager.get_equipment_by_name('Cung Băng Lãm')
        if eq:
            eq_manager.equip_to_character(eq, 'chien_binh')
            print(f"✓ Đã gắn {eq.name} cho chiến binh")
            
            char_eq = eq_manager.get_character_equipment('chien_binh')
            print(f"✓ Equipment của chiến binh: {char_eq}")
            
            # Test save
            all_eq = eq_manager.save_all_character_equipment()
            print(f"✓ Save data: {all_eq}")
        
    except Exception as e:
        print(f"✗ Lỗi: {e}")
        import traceback
        traceback.print_exc()
    
    # 3. Test flow hoàn chỉnh
    print("\n3. Flow hoàn chỉnh:")
    print("   a. User đăng nhập")
    print("   b. Vào màn hình trang bị")
    print("   c. Chọn nhân vật (←/→)")
    print("   d. Click chọn trang bị từ kho")
    print("   e. Click vào slot (Công/Thủ/Tốc Độ) để gắn")
    print("   f. Nhấn ESC → Tự động lưu vào profile")
    print("   g. Vào menu → Chọn màn chơi")
    print("   h. Chọn nhân vật → Tự động load equipment")
    print("   i. Vào game → Equipment đã được áp dụng!")
    
    # 4. Kiểm tra file đường dẫn
    print("\n4. Kiểm tra files...")
    files_to_check = [
        'ma_nguon/doi_tuong/equipment.py',
        'ma_nguon/man_choi/equipment_screen.py',
        'ma_nguon/man_choi/chon_nhan_vat.py',
        'ma_nguon/core/profile_manager.py'
    ]
    
    for file_path in files_to_check:
        full_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), file_path)
        if os.path.exists(full_path):
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} KHÔNG TÌM THẤY!")
    
    print("\n" + "=" * 60)
    print("TEST HOÀN TẤT!")
    print("=" * 60)
    print("\nHướng dẫn sử dụng:")
    print("1. Chạy game: python ma_nguon/main.py")
    print("2. Đăng nhập (hoặc register)")
    print("3. Chọn 'Trang bị' từ menu")
    print("4. Dùng ←/→ để chuyển nhân vật")
    print("5. Click trang bị → Click slot để gắn")
    print("6. ESC để lưu và thoát")
    print("7. Chọn màn chơi → Chọn nhân vật")
    print("8. Equipment sẽ tự động áp dụng!")

if __name__ == "__main__":
    test_equipment_profile_flow()
