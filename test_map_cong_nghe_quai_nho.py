"""
Test script để chơi thử Map Công Nghệ với 2 loại quái nhỏ
"""
import pygame
import os
import sys

# Thêm thư mục gốc vào path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from ma_nguon.core.quan_ly_game import Game

def test_map_cong_nghe():
    """Test chơi Map Công Nghệ"""
    print("="*60)
    print("TEST MAP CÔNG NGHỆ VỚI 2 LOẠI QUÁI NHỎ")
    print("="*60)
    print("\nHướng dẫn:")
    print("- Mũi tên trái/phải: Di chuyển")
    print("- W: Nhảy")
    print("- A: Đấm")
    print("- S: Đá")
    print("- D: Phòng thủ")
    print("- ESC: Thoát về menu")
    print("\nKiểm tra:")
    print("✓ Có 2 loại quái vật xuất hiện (màu khác nhau)")
    print("✓ Animation của 2 loại quái khác nhau")
    print("✓ Cả 2 loại đều có thể tấn công và nhận damage")
    print("="*60)
    print("\nĐang khởi động game...")
    
    try:
        game = Game()
        # Chuyển thẳng đến Map Công Nghệ
        game.change_scene("map_cong_nghe")
        game.run()
    except Exception as e:
        print(f"\nLỗi khi chạy game: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_map_cong_nghe()
