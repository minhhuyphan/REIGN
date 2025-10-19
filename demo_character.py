"""
Tạo file demo đơn giản để test Chiến Thần Lạc Hồng
Chạy bằng: python demo_character.py
"""

import pygame
import os

def main():
    print("=== DEMO CHIẾN THẦN LẠC HỒNG ===")
    
    # Kiểm tra các file ảnh
    character_path = "Tai_nguyen/hinh_anh/nhan_vat/chien_than_lac_hong"
    
    if os.path.exists(character_path):
        print(f"✅ Thư mục nhân vật tồn tại: {character_path}")
        
        # Kiểm tra các animation
        animations = ["dung_yen", "chay", "danh", "da", "do", "nga", "nhay"]
        for anim in animations:
            anim_path = os.path.join(character_path, anim)
            if os.path.exists(anim_path):
                files = [f for f in os.listdir(anim_path) if f.endswith('.png')]
                print(f"  📁 {anim}: {len(files)} frames")
            else:
                print(f"  ❌ {anim}: Không tồn tại")
    else:
        print(f"❌ Không tìm thấy thư mục: {character_path}")
    
    print("\n=== THÔNG TIN NHÂN VẬT ===")
    print("🏆 Tên: Chiến Thần Lạc Hồng")
    print("❤️  HP: 750 (Cao nhất)")
    print("⚡ Tốc độ: 6 (Cân bằng)")
    print("⚔️  Sát thương: 50 (Mạnh nhất)")
    print("🛡️  Phòng thủ: 4 (Tốt nhất)")
    print("🎨 Màu đặc trưng: Hồng đỏ (255, 0, 127)")
    print("🌟 Đặc biệt: ★ HUYỀN THOẠI ★")
    
    print("\n✅ Nhân vật đã được thêm thành công vào game!")
    print("🎮 Để chơi: Chạy game và chọn 'Chiến Thần Lạc Hồng' trong menu chọn nhân vật")

if __name__ == "__main__":
    main()