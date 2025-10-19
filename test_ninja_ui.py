#!/usr/bin/env python3
"""
Test file for Ninja Map Man 1 with updated UI
"""

import pygame
import sys
import os

# Thêm thư mục gốc vào sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ma_nguon.man_choi.map_ninja_man1 import mapninjaman1Scene

class TestGame:
    def __init__(self):
        pygame.init()
        self.WIDTH = 1200
        self.HEIGHT = 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Test Ninja Map Man 1 - Updated UI")
        
        self.map_width = 4000  # Chiều rộng của map
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Khởi tạo scene
        self.current_scene = mapninjaman1Scene(self)
    
    def change_scene(self, scene_name):
        print(f"Chuyển đến scene: {scene_name}")
        # Trong test này, chỉ print thông báo
        pass
    
    def load_scene(self, scene_name, *args):
        print(f"Tải scene: {scene_name} với args: {args}")
        return None
    
    def run(self):
        print("=== TEST NINJA MAP MAN 1 - UI UPDATE ===")
        print("- Sử dụng phím mũi tên để di chuyển")
        print("- A: Đấm, S: Đá, D: Phòng thủ, W: Nhảy")
        print("- Click vào các nút trên màn hình để điều khiển")
        print("- ESC: Thoát")
        print("========================================")
        
        while self.running:
            # Xử lý sự kiện
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                else:
                    # Chuyển sự kiện cho scene hiện tại
                    if self.current_scene:
                        self.current_scene.handle_event(event)
            
            # Cập nhật game logic
            if self.current_scene:
                self.current_scene.update()
            
            # Vẽ everything
            self.screen.fill((135, 206, 235))  # Sky blue background
            if self.current_scene:
                self.current_scene.draw(self.screen)
            
            # Vẽ thông tin debug
            debug_info = [
                "=== NINJA MAP MAN 1 - UI UPDATED ===",
                "Phím: ←→ di chuyển | A-đấm S-đá D-phòng thủ W-nhảy",
                "UI: Click các nút trên màn hình",
                "ESC: Thoát",
            ]
            
            font = pygame.font.Font(None, 24)
            for i, line in enumerate(debug_info):
                color = (255, 255, 255) if i == 0 else (200, 200, 200)
                text = font.render(line, True, color)
                self.screen.blit(text, (10, 10 + i * 25))
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        print("Test hoàn thành!")

if __name__ == "__main__":
    try:
        game = TestGame()
        game.run()
    except Exception as e:
        print(f"Lỗi khi chạy test: {e}")
        import traceback
        traceback.print_exc()