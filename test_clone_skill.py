"""
Test script cho skill phân thân của Chiến Binh
Chạy: python test_clone_skill.py
"""
import os
import sys
import pygame
import random

# Add root directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ma_nguon.doi_tuong.nhan_vat.nhan_vat import Character
from ma_nguon.doi_tuong.quai_vat.quai_vat import QuaiVat

class CloneTestScene:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 600))
        pygame.display.set_caption("Test Clone Skill - Chiến Binh")
        self.clock = pygame.time.Clock()
        
        # Load font
        try:
            self.font = pygame.font.Font("tai_nguyen/font/Fz-Futurik.ttf", 24)
            self.font_small = pygame.font.Font("tai_nguon/font/Fz-Futurik.ttf", 18)
        except:
            self.font = pygame.font.Font(None, 24)
            self.font_small = pygame.font.Font(None, 18)
            
        # Tạo nhân vật chiến binh
        self.create_warrior()
        
        # Tạo một số quái vật để test
        self.create_enemies()
        
        # Camera
        self.camera_x = 0
        
        # UI
        self.show_debug = True
        
        print("=== CLONE SKILL TEST ===")
        print("Phím điều khiển:")
        print("  WASD: Di chuyển")
        print("  J: Đấm")
        print("  K: Đá")
        print("  F: Kích hoạt skill phân thân")
        print("  SPACE: Toggle debug info")
        print("  ESC: Thoát")
        print("========================")
        
    def create_warrior(self):
        """Tạo nhân vật chiến binh với skill phân thân"""
        # Stats đặc biệt cho test
        stats = {
            'hp': 800,
            'damage': 40,
            'speed': 6,
            'defense': 3,
            'kick_damage': 30,
            'max_mana': 150,
            'mana_regen': 5
        }
        
        # Controls
        controls = {
            "left": pygame.K_a,
            "right": pygame.K_d,
            "attack": pygame.K_j,
            "kick": pygame.K_k,
            "defend": pygame.K_s,
            "jump": pygame.K_w,
        }
        
        folder = "tai_nguyen/hinh_anh/nhan_vat/chien_binh"
        self.player = Character(200, 400, folder, controls, color=(0, 255, 0), stats=stats)
        self.player.base_y = 400
        
        print(f"[WARRIOR] Tạo chiến binh - HP: {self.player.hp}, Mana: {self.player.mana}")
        print(f"[WARRIOR] Special skill: {self.player.special_skill}")
        print(f"[WARRIOR] Skill mana cost: {self.player.skill_mana_cost}")
        
    def create_enemies(self):
        """Tạo quái vật để test"""
        self.enemies = []
        
        enemy_folder = "tai_nguyen/hinh_anh/quai_vat/quai_vat_bay"
        sound_folder = "tai_nguyen/am_thanh/hieu_ung"
        
        # Tạo 5 con quái ở các vị trí khác nhau
        enemy_positions = [
            (400, 400),
            (600, 400), 
            (800, 400),
            (350, 400),
            (950, 400)
        ]
        
        for i, (x, y) in enumerate(enemy_positions):
            try:
                enemy = QuaiVat(x, y, enemy_folder, sound_folder, damage=15)
                enemy.hp = 100  # Ít HP để dễ test
                enemy.base_y = y
                self.enemies.append(enemy)
                print(f"[ENEMY] Tạo quái {i+1} tại ({x}, {y})")
            except Exception as e:
                print(f"[WARNING] Không tạo được quái {i+1}: {e}")
                
        # Set enemies reference cho player để clone có thể tấn công
        self.player.set_enemies_reference(self.enemies)
        
    def handle_events(self):
        """Xử lý sự kiện"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_SPACE:
                    self.show_debug = not self.show_debug
                elif event.key == pygame.K_f:
                    # Kích hoạt skill
                    if self.player.can_use_skill():
                        self.player.use_skill()
                        print(f"[SKILL] Activated! Mana: {self.player.mana}/{self.player.max_mana}")
                    else:
                        remaining = self.player.get_skill_cooldown_remaining()
                        print(f"[SKILL] Cannot use - Cooldown: {remaining:.1f}s, Mana: {self.player.mana}/{self.player.skill_mana_cost}")
                        
        return True
        
    def update(self):
        """Cập nhật logic game"""
        keys = pygame.key.get_pressed()
        
        # Cập nhật player
        self.player.update(keys)
        
        # Cập nhật enemies
        for enemy in self.enemies[:]:
            if not enemy.dead:
                enemy.update(target=self.player)
            
        # Remove dead enemies
        self.enemies = [e for e in self.enemies if not e.dead]
        
        # Cập nhật camera để theo player
        target_camera_x = self.player.x - 400
        self.camera_x += (target_camera_x - self.camera_x) * 0.1
        self.camera_x = max(0, self.camera_x)
        
    def draw(self):
        """Vẽ màn hình"""
        # Background
        self.screen.fill((50, 50, 100))
        
        # Vẽ ground line
        ground_y = 450
        pygame.draw.line(self.screen, (100, 100, 100), (0, ground_y), (1200, ground_y), 2)
        
        # Vẽ player (bao gồm cả clones)
        self.player.draw(self.screen, self.camera_x)
        
        # Vẽ enemies
        for enemy in self.enemies:
            enemy.draw(self.screen, self.camera_x)
            
        # Vẽ UI
        self.draw_ui()
        
        pygame.display.flip()
        
    def draw_ui(self):
        """Vẽ giao diện"""
        # Player stats
        hp_text = f"HP: {self.player.hp}/{self.player.max_hp}"
        mana_text = f"Mana: {self.player.mana:.0f}/{self.player.max_mana}"
        
        hp_surface = self.font.render(hp_text, True, (255, 255, 255))
        mana_surface = self.font.render(mana_text, True, (100, 150, 255))
        
        self.screen.blit(hp_surface, (10, 10))
        self.screen.blit(mana_surface, (10, 40))
        
        # Skill cooldown
        if self.player.can_use_skill():
            skill_text = "Skill: READY (Press F)"
            color = (0, 255, 0)
        else:
            remaining = self.player.get_skill_cooldown_remaining()
            skill_text = f"Skill: {remaining:.1f}s"
            color = (255, 100, 100)
            
        skill_surface = self.font.render(skill_text, True, color)
        self.screen.blit(skill_surface, (10, 70))
        
        # Clone info
        clone_count = self.player.get_clone_count()
        if clone_count > 0:
            clone_text = f"Clones Active: {clone_count}"
            clone_surface = self.font.render(clone_text, True, (255, 255, 0))
            self.screen.blit(clone_surface, (10, 100))
            
            # Detailed clone info
            if self.show_debug:
                clone_info = self.player.get_clone_info()
                for i, info in enumerate(clone_info):
                    detail_text = f"Clone {i+1}: HP {info['hp']:.0f}/{info['max_hp']} | Time: {info['remaining_time']:.1f}s"
                    detail_surface = self.font_small.render(detail_text, True, (200, 200, 200))
                    self.screen.blit(detail_surface, (20, 130 + i * 20))
                    
        # Enemies count
        alive_enemies = len([e for e in self.enemies if not e.dead])
        enemy_text = f"Enemies: {alive_enemies}"
        enemy_surface = self.font.render(enemy_text, True, (255, 100, 100))
        self.screen.blit(enemy_surface, (10, 200))
        
        # Debug info
        if self.show_debug:
            debug_y = 250
            debug_info = [
                f"Player pos: ({self.player.x:.0f}, {self.player.y:.0f})",
                f"Camera: {self.camera_x:.0f}",
                f"Special skill: {self.player.special_skill}",
                f"Press SPACE to toggle debug info"
            ]
            
            for text in debug_info:
                debug_surface = self.font_small.render(text, True, (150, 150, 150))
                self.screen.blit(debug_surface, (10, debug_y))
                debug_y += 20
                
        # Controls help
        controls_info = [
            "Controls:",
            "WASD - Move",
            "J - Punch", 
            "K - Kick",
            "F - Clone Skill",
            "SPACE - Debug",
            "ESC - Exit"
        ]
        
        help_y = self.screen.get_height() - len(controls_info) * 20 - 10
        for text in controls_info:
            help_surface = self.font_small.render(text, True, (120, 120, 120))
            self.screen.blit(help_surface, (self.screen.get_width() - 150, help_y))
            help_y += 20
            
    def run(self):
        """Chạy test scene"""
        running = True
        
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
            
        pygame.quit()

def main():
    print("🎮 CLONE SKILL TEST")
    print("==================")
    
    # Kiểm tra files cần thiết
    required_paths = [
        "tai_nguyen/hinh_anh/nhan_vat/chien_binh",
        "tai_nguyen/hinh_anh/quai_vat/quai_vat_bay"
    ]
    
    for path in required_paths:
        if os.path.exists(path):
            print(f"✅ Found: {path}")
        else:
            print(f"❌ Missing: {path}")
            
    print("\nStarting test...")
    
    try:
        test_scene = CloneTestScene()
        test_scene.run()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()