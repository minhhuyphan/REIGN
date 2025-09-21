"""
Script test để kiểm tra nhân vật Chiến Thần Lạc Hồng
"""
import os
import sys

# Thêm thư mục gốc vào Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ma_nguon.core.quan_ly_game import Game

def test_chien_than_lac_hong():
    """Test nhân vật Chiến Thần Lạc Hồng"""
    print("🔥 Testing Chiến Thần Lạc Hồng Character...")
    
    # Kiểm tra các file ảnh có tồn tại không
    base_path = "Tai_nguyen/hinh_anh/nhan_vat/chien_than_lac_hong"
    animations = ["dung_yen", "chay", "danh", "da", "do", "nga", "nhay"]
    
    for anim in animations:
        anim_path = os.path.join(base_path, anim)
        if os.path.exists(anim_path):
            files = os.listdir(anim_path)
            png_files = [f for f in files if f.endswith('.png')]
            print(f"✅ {anim}: {len(png_files)} frames")
        else:
            print(f"❌ {anim}: Không tìm thấy thư mục")
    
    print("\n🎮 Starting game...")
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_chien_than_lac_hong()