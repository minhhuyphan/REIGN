#!/usr/bin/env python3
"""
Test file để kiểm tra vấn đề nhảy trong Ninja Map Man 1
"""

import pygame
import sys
import os

# Thêm thư mục gốc vào sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ma_nguon.man_choi.map_ninja_man1 import mapninjaman1Scene

class JumpTestGame:
    def __init__(self):
        pygame.init()
        self.WIDTH = 1200
        self.HEIGHT = 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Test Jump Physics - Ninja Map Man 1")
        
        self.map_width = 4000
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Khởi tạo scene
        self.current_scene = mapninjaman1Scene(self)
    
    def change_scene(self, scene_name):
        print(f"Change scene request: {scene_name}")
        pass
    
    def load_scene(self, scene_name, *args):
        print(f"Load scene: {scene_name}")
        return None
    
    def run(self):
        print("=== TEST JUMP PHYSICS - NINJA MAP MAN 1 ===")
        print("🎮 Điều khiển:")
        print("  ←→ : Di chuyển")
        print("  W  : Nhảy")
        print("  A  : Đấm")
        print("  S  : Đá") 
        print("  D  : Phòng thủ")
        print("  ESC: Thoát")
        print("")
        print("🐛 Kiểm tra vấn đề:")
        print("  - Nhảy có bị 'dính' không?")
        print("  - Có thể di chuyển khi nhảy không?")
        print("  - Nhân vật có rơi đúng về mặt đất không?")
        print("=========================================")
        
        frame_count = 0
        
        while self.running:
            frame_count += 1
            
            # Xử lý sự kiện
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                else:
                    if self.current_scene:
                        self.current_scene.handle_event(event)
            
            # Cập nhật game logic
            if self.current_scene:
                self.current_scene.update()
            
            # Vẽ everything
            self.screen.fill((135, 206, 235))  # Sky blue background
            if self.current_scene:
                self.current_scene.draw(self.screen)
            
            # Vẽ thông tin debug về nhảy
            if self.current_scene and hasattr(self.current_scene, 'player'):
                player = self.current_scene.player
                debug_info = [
                    f"=== JUMP DEBUG INFO (Frame {frame_count}) ===",
                    f"Position: ({player.x:.1f}, {player.y:.1f}) | Base Y: {player.base_y}",
                    f"State: {player.state} | Action: {getattr(player, 'action_type', 'None')}",
                    f"Jumping: {getattr(player, 'jumping', False)} | Jump Vel: {getattr(player, 'jump_vel', 0)}",
                    f"Actioning: {getattr(player, 'actioning', False)} | Frame: {player.frame}",
                    f"HP: {player.hp}/{player.max_hp}",
                    "",
                    "🎮 W-nhảy | ←→-di chuyển | A-đấm S-đá D-phòng thủ | ESC-thoát"
                ]
                
                font = pygame.font.Font(None, 24)
                for i, line in enumerate(debug_info):
                    color = (255, 255, 0) if i == 0 else (255, 255, 255)  # Vàng cho tiêu đề
                    if "Jumping: True" in line:
                        color = (255, 100, 100)  # Đỏ khi đang nhảy
                    elif "State: nhay" in line:
                        color = (100, 255, 100)  # Xanh lá khi state nhảy
                    
                    text = font.render(line, True, color)
                    self.screen.blit(text, (10, 10 + i * 25))
                
                # Vẽ đường base_y để dễ quan sát
                base_y_screen = player.base_y - self.current_scene.camera_x
                pygame.draw.line(self.screen, (255, 0, 0), 
                               (0, player.base_y), (self.WIDTH, player.base_y), 2)
                
                # Vẽ vị trí hiện tại của player
                player_screen_x = player.x - self.current_scene.camera_x
                pygame.draw.circle(self.screen, (0, 255, 0), 
                                 (int(player_screen_x + 25), int(player.y + 40)), 5)
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        print("✅ Test hoàn thành!")

if __name__ == "__main__":
    try:
        game = JumpTestGame()
        game.run()
    except Exception as e:
        print(f"❌ Lỗi khi chạy test: {e}")
        import traceback
        traceback.print_exc()