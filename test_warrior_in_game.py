"""
Test integration của clone skill trong game thực
Chạy: python test_warrior_in_game.py
"""
import os
import sys
import pygame

# Add root directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ma_nguon.main import Game

def test_warrior_clone_in_game():
    """Test chiến binh với clone skill trong game thực"""
    print("🎮 TESTING WARRIOR CLONE SKILL IN GAME")
    print("="*50)
    
    # Kiểm tra assets cần thiết
    required_assets = [
        "tai_nguyen/hinh_anh/nhan_vat/chien_binh",
        "tai_nguyen/hinh_anh/quai_vat",
        "tai_nguyen/font/Fz-Futurik.ttf"
    ]
    
    print("Kiểm tra assets:")
    for asset in required_assets:
        if os.path.exists(asset):
            print(f"  ✅ {asset}")
        else:
            print(f"  ❌ {asset}")
    
    print("\nHướng dẫn test:")
    print("1. Chọn nhân vật 'Chiến binh' trong game")
    print("2. Bắt đầu Level 1")
    print("3. Nhấn phím F để kích hoạt skill phân thân")
    print("4. Quan sát 2 phân thân xuất hiện và tự động đánh quái")
    print("5. Phân thân sẽ tự động biến mất sau 15 giây")
    
    print("\nBắt đầu game...")
    
    try:
        # Tạo game instance và chạy
        game = Game()
        game.run()
        
    except Exception as e:
        print(f"Lỗi khi chạy game: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_warrior_clone_in_game()