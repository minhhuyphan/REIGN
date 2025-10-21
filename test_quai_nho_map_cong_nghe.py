"""
Test script để kiểm tra việc load 2 loại quái nhỏ trên Map Công Nghệ
"""
import pygame
import os
import sys

# Thêm thư mục gốc vào path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from ma_nguon.doi_tuong.quai_vat.quai_vat import QuaiVat
from ma_nguon.doi_tuong.quai_vat.quai_nho_type1 import QuaiNhoType1

def test_quai_nho():
    """Test load và hiển thị 2 loại quái nhỏ"""
    pygame.init()
    
    WIDTH, HEIGHT = 1000, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Test Quái Nhỏ Map Công Nghệ")
    clock = pygame.time.Clock()
    
    # Đường dẫn đến assets
    folder_qv = os.path.join("Tai_nguyen", "hinh_anh", "quai_vat", "quai_map_cong_nghe", "quai_nho")
    sound_qv = os.path.join("Tai_nguyen", "am_thanh", "hieu_ung")
    
    # Kiểm tra folder tồn tại
    print(f"Checking folder: {folder_qv}")
    if not os.path.exists(folder_qv):
        print(f"ERROR: Folder không tồn tại: {folder_qv}")
        return
    
    # List các subfolder
    print("\nSubfolders trong quai_nho:")
    for item in os.listdir(folder_qv):
        item_path = os.path.join(folder_qv, item)
        if os.path.isdir(item_path):
            print(f"  - {item}")
    
    print("\n" + "="*60)
    print("Đang khởi tạo quái vật...")
    print("="*60)
    
    # Tạo 2 quái: 1 loại thường, 1 loại type 1
    try:
        print("\n1. Tạo QuaiVat (sử dụng folder không có số)...")
        quai_normal = QuaiVat(200, 400, folder_qv, sound_qv, color=(0, 255, 255), damage=15)
        print("   ✓ QuaiVat khởi tạo thành công!")
        print(f"   - HP: {quai_normal.hp}")
        print(f"   - Speed: {quai_normal.speed}")
        print(f"   - Animations loaded: {list(quai_normal.animations.keys())}")
    except Exception as e:
        print(f"   ✗ Lỗi khi tạo QuaiVat: {e}")
        import traceback
        traceback.print_exc()
        quai_normal = None
    
    try:
        print("\n2. Tạo QuaiNhoType1 (sử dụng folder có số 1)...")
        quai_type1 = QuaiNhoType1(600, 400, folder_qv, sound_qv, color=(255, 0, 255), damage=14)
        print("   ✓ QuaiNhoType1 khởi tạo thành công!")
        print(f"   - HP: {quai_type1.hp}")
        print(f"   - Speed: {quai_type1.speed}")
        print(f"   - Animations loaded: {list(quai_type1.animations.keys())}")
    except Exception as e:
        print(f"   ✗ Lỗi khi tạo QuaiNhoType1: {e}")
        import traceback
        traceback.print_exc()
        quai_type1 = None
    
    print("\n" + "="*60)
    print("Bắt đầu render test...")
    print("Nhấn ESC để thoát, SPACE để thay đổi animation")
    print("="*60)
    
    # Danh sách các state để test
    states = ["dung_yen", "chay", "danh", "da", "nhay", "nga"]
    current_state_idx = 0
    
    running = True
    camera_x = 0
    
    while running:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    # Chuyển sang animation tiếp theo
                    current_state_idx = (current_state_idx + 1) % len(states)
                    new_state = states[current_state_idx]
                    if quai_normal:
                        quai_normal.state = new_state
                        quai_normal.frame = 0
                    if quai_type1:
                        quai_type1.state = new_state
                        quai_type1.frame = 0
                    print(f"Changed to state: {new_state}")
        
        # Update
        if quai_normal:
            quai_normal.update(target=None)
        if quai_type1:
            quai_type1.update(target=None)
        
        # Draw
        screen.fill((20, 20, 40))
        
        # Vẽ mặt đất
        pygame.draw.rect(screen, (60, 60, 100), (0, 450, WIDTH, 150))
        
        # Vẽ nhãn
        font = pygame.font.Font(None, 36)
        title = font.render("Test Quai Nho Map Cong Nghe", True, (255, 255, 255))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 20))
        
        font_small = pygame.font.Font(None, 24)
        
        if quai_normal:
            label1 = font_small.render("QuaiVat (folder: chay, danh, etc.)", True, (0, 255, 255))
            screen.blit(label1, (50, 70))
            quai_normal.draw(screen, camera_x)
        
        if quai_type1:
            label2 = font_small.render("QuaiNhoType1 (folder: chay1, danh1, etc.)", True, (255, 0, 255))
            screen.blit(label2, (450, 70))
            quai_type1.draw(screen, camera_x)
        
        # Hiển thị state hiện tại
        state_text = font_small.render(f"State: {states[current_state_idx]}", True, (255, 255, 0))
        screen.blit(state_text, (WIDTH//2 - state_text.get_width()//2, HEIGHT - 100))
        
        help_text = font_small.render("SPACE: Change Animation | ESC: Exit", True, (200, 200, 200))
        screen.blit(help_text, (WIDTH//2 - help_text.get_width()//2, HEIGHT - 60))
        
        pygame.display.flip()
    
    pygame.quit()
    print("\nTest hoàn tất!")

if __name__ == "__main__":
    print("="*60)
    print("TEST QUÁI NHỎ MAP CÔNG NGHỆ")
    print("="*60)
    test_quai_nho()
