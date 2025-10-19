"""
Script để áp dụng skill system cho tất cả map
"""
import os

# Danh sách tất cả các file map cần cập nhật
MAP_FILES = [
    "ma_nguon/man_choi/man2.py",
    "ma_nguon/man_choi/map_mua_thu.py",
    "ma_nguon/man_choi/map_mua_thu_man1.py",
    "ma_nguon/man_choi/map_mua_thu_man2.py",
    "ma_nguon/man_choi/map_mua_thu_man3.py",
    "ma_nguon/man_choi/map_ninja.py",
    "ma_nguon/man_choi/map_ninja_man1.py",
    "ma_nguon/man_choi/map_cong_nghe.py",
    "ma_nguon/man_choi/maprunglinhvuc.py"
]

# Template code để thêm vào imports
IMPORT_CODE = """from ma_nguon.man_choi.skill_video import SkillVideoPlayer"""

# Template code để thêm vào __init__
INIT_CODE = """        
        # Skill video system
        self.skill_video = None
        self.showing_skill_video = False"""

# Template code để thêm vào handle_event
HANDLE_EVENT_CODE = """            
            # Xử lý phím F - skill (chỉ cho Chiến Thần Lạc Hồng)
            if event.key == pygame.K_f and "chien_than_lac_hong" in self.player.folder:
                if self.player.can_use_skill():
                    self.activate_skill()
                else:
                    # Hiển thị thông báo không đủ mana hoặc đang cooldown
                    remaining = self.player.get_skill_cooldown_remaining()
                    if remaining > 0:
                        print(f"[SKILL] Cooldown: {remaining:.1f}s")
                    else:
                        print(f"[SKILL] Không đủ mana ({self.player.mana}/{self.player.skill_mana_cost})")"""

# Template methods để thêm vào class
METHOD_CODE = """
    def activate_skill(self):
        \"\"\"Kích hoạt skill - phát video và gây sát thương\"\"\"
        if not self.player.use_skill():
            return
        
        print("[SKILL] Chiến Thần Lạc Hồng sử dụng skill!")
        
        # Tạo callback để gây damage sau khi video kết thúc
        def on_skill_finish():
            self.damage_nearby_enemies()
            self.showing_skill_video = False
            self.skill_video = None
        
        # Phát video skill
        video_path = "Tai_nguyen/video/skill_chien_than.mp4"
        self.skill_video = SkillVideoPlayer(video_path, on_skill_finish)
        self.showing_skill_video = True
    
    def damage_nearby_enemies(self):
        \"\"\"Gây sát thương cho tất cả quái vật trong phạm vi\"\"\"
        damaged_count = 0
        
        # Damage quái thường
        if hasattr(self, 'normal_enemies'):
            for enemy in self.normal_enemies:
                if enemy.hp > 0:
                    # Kiểm tra khoảng cách
                    distance = abs(enemy.x - self.player.x)
                    if distance <= self.player.skill_range:
                        enemy.hp -= self.player.skill_damage
                        enemy.damaged = True
                        damaged_count += 1
                        print(f"[SKILL] Hit enemy at distance {distance:.0f}px, HP: {enemy.hp}")
        
        # Damage enemies list (một số map dùng tên khác)
        if hasattr(self, 'enemies'):
            for enemy in self.enemies:
                if enemy.hp > 0:
                    distance = abs(enemy.x - self.player.x)
                    if distance <= self.player.skill_range:
                        enemy.hp -= self.player.skill_damage
                        enemy.damaged = True
                        damaged_count += 1
                        print(f"[SKILL] Hit enemy at distance {distance:.0f}px, HP: {enemy.hp}")
        
        # Damage boss
        if hasattr(self, 'current_boss') and self.current_boss and self.current_boss.hp > 0:
            distance = abs(self.current_boss.x - self.player.x)
            if distance <= self.player.skill_range:
                self.current_boss.hp -= self.player.skill_damage
                self.current_boss.damaged = True
                damaged_count += 1
                print(f"[SKILL] Hit BOSS at distance {distance:.0f}px, HP: {self.current_boss.hp}")
        
        # Damage boss list
        if hasattr(self, 'bosses'):
            for boss in self.bosses:
                if boss.hp > 0:
                    distance = abs(boss.x - self.player.x)
                    if distance <= self.player.skill_range:
                        boss.hp -= self.player.skill_damage
                        boss.damaged = True
                        damaged_count += 1
                        print(f"[SKILL] Hit BOSS at distance {distance:.0f}px, HP: {boss.hp}")
        
        print(f"[SKILL] Damaged {damaged_count} enemies!")
    
    def draw_skill_ui(self, screen):
        \"\"\"Vẽ UI hiển thị cooldown và mana skill - Dưới thanh máu/mana\"\"\"
        # Vị trí UI - Dưới thanh mana (thanh mana ở y=58, height=18)
        # HP bar: (20, 20, 300, 30)
        # Mana bar: (20, 58, 300, 18)
        # Skill UI sẽ ở (20, 84) - ngay dưới mana bar
        ui_x = 20
        ui_y = 84  # Dưới thanh mana (58 + 18 + 8px spacing)
        ui_width = 300  # Same width as HP/Mana bars
        ui_height = 50
        
        # Font
        try:
            font = pygame.font.Font("tai_nguyen/font/Fz-Futurik.ttf", 18)
            font_small = pygame.font.Font("tai_nguyen/font/Fz-Futurik.ttf", 14)
        except:
            font = pygame.font.Font(None, 18)
            font_small = pygame.font.Font(None, 14)
        
        # Background panel (dark, semi-transparent)
        bg_surface = pygame.Surface((ui_width, ui_height), pygame.SRCALPHA)
        pygame.draw.rect(bg_surface, (30, 30, 40, 200), (0, 0, ui_width, ui_height), border_radius=8)
        screen.blit(bg_surface, (ui_x, ui_y))
        
        # Border (golden)
        pygame.draw.rect(screen, (255, 215, 0), (ui_x, ui_y, ui_width, ui_height), 2, border_radius=8)
        
        # Skill icon area (left side)
        icon_size = 40
        icon_x = ui_x + 8
        icon_y = ui_y + (ui_height - icon_size) // 2
        
        # Draw icon background
        pygame.draw.rect(screen, (50, 50, 60), (icon_x, icon_y, icon_size, icon_size), border_radius=4)
        pygame.draw.rect(screen, (255, 215, 0), (icon_x, icon_y, icon_size, icon_size), 1, border_radius=4)
        
        # Draw "F" key in icon
        key_text = font.render("F", True, (255, 215, 0))
        key_rect = key_text.get_rect(center=(icon_x + icon_size//2, icon_y + icon_size//2))
        screen.blit(key_text, key_rect)
        
        # Skill name (right of icon)
        name_x = icon_x + icon_size + 10
        name_y = ui_y + 8
        skill_text = font.render("SKILL CHIẾN THẦN", True, (255, 215, 0))
        screen.blit(skill_text, (name_x, name_y))
        
        # Cooldown info (below name) - HIỂN THỊ THỜI GIAN HỒI CHIÊU
        remaining = self.player.get_skill_cooldown_remaining()
        cost_y = name_y + 22
        
        if remaining > 0:
            # Đang hồi chiêu - hiển thị thời gian còn lại
            cd_text = font_small.render(f"Hồi chiêu: {remaining:.1f}s", True, (255, 150, 150))
            screen.blit(cd_text, (name_x, cost_y))
        else:
            # Sẵn sàng - hiển thị tổng thời gian hồi chiêu
            ready_text = font_small.render(f"Hồi chiêu: {self.player.skill_cooldown/1000:.0f}s", True, (150, 150, 150))
            screen.blit(ready_text, (name_x, cost_y))
        
        # Status indicator (right side)
        status_x = ui_x + ui_width - 100
        status_y = ui_y + (ui_height - 30) // 2
        
        if remaining > 0:
            # Đang cooldown - hiển thị timer lớn
            cd_big = font.render(f"{remaining:.1f}s", True, (255, 100, 100))
            screen.blit(cd_big, (status_x + 10, status_y + 8))
        else:
            if self.player.mana >= self.player.skill_mana_cost:
                # Ready to use - hiển thị READY với glow
                ready_text = font.render("READY!", True, (0, 255, 0))
                screen.blit(ready_text, (status_x, status_y + 8))
                
                # Add pulsing glow effect
                import math
                pulse = abs(math.sin(pygame.time.get_ticks() / 300.0))
                glow_alpha = int(100 + pulse * 100)
                glow_surface = pygame.Surface((80, 30), pygame.SRCALPHA)
                pygame.draw.ellipse(glow_surface, (0, 255, 0, glow_alpha), glow_surface.get_rect())
                screen.blit(glow_surface, (status_x - 10, status_y - 5))
            else:
                # Không đủ mana
                need_text = font_small.render(f"Cần {self.player.skill_mana_cost} MP", True, (255, 100, 100))
                screen.blit(need_text, (status_x - 10, status_y + 8))
"""

# Template code để thêm vào đầu update()
UPDATE_CODE = """        
        # Nếu đang phát skill video thì pause game
        if self.showing_skill_video and self.skill_video:
            self.skill_video.update()
            return
"""

# Template code để thêm vào đầu draw()
DRAW_CODE = """        # Nếu đang phát skill video, vẽ video toàn màn hình
        if self.showing_skill_video and self.skill_video:
            # Vẽ video skill
            self.skill_video.draw(screen)
            return
"""

# Template code để thêm vào cuối draw() trước return cuối cùng
DRAW_UI_CODE = """        
        # Vẽ skill cooldown UI (chỉ cho Chiến Thần Lạc Hồng)
        if "chien_than_lac_hong" in self.player.folder:
            self.draw_skill_ui(screen)
"""

print("=" * 60)
print("HƯỚNG DẪN ÁP DỤNG SKILL SYSTEM CHO TẤT CẢ MAP")
print("=" * 60)
print("\n⚠️  Script này chỉ hiển thị hướng dẫn. Bạn cần áp dụng thủ công.")
print("\nĐể áp dụng skill system cho mỗi map, làm theo các bước sau:\n")

print("📝 BƯỚC 1: Thêm import vào đầu file")
print("-" * 60)
print(IMPORT_CODE)

print("\n📝 BƯỚC 2: Thêm vào __init__ (sau phần khởi tạo camera)")
print("-" * 60)
print(INIT_CODE)

print("\n📝 BƯỚC 3: Thêm vào handle_event (trong if event.type == pygame.KEYDOWN)")
print("-" * 60)
print(HANDLE_EVENT_CODE)

print("\n📝 BƯỚC 4: Thêm các method mới vào class")
print("-" * 60)
print(METHOD_CODE)

print("\n📝 BƯỚC 5: Thêm vào đầu hàm update()")
print("-" * 60)
print(UPDATE_CODE)

print("\n📝 BƯỚC 6: Thêm vào đầu hàm draw()")
print("-" * 60)
print(DRAW_CODE)

print("\n📝 BƯỚC 7: Thêm vào cuối hàm draw() (trước return cuối)")
print("-" * 60)
print(DRAW_UI_CODE)

print("\n" + "=" * 60)
print("📋 DANH SÁCH MAP CẦN CẬP NHẬT:")
print("=" * 60)
for i, map_file in enumerate(MAP_FILES, 1):
    exists = "✅" if os.path.exists(map_file) else "❌"
    print(f"{i}. {exists} {map_file}")

print("\n" + "=" * 60)
print("✨ Lưu ý:")
print("=" * 60)
print("- Map man1.py đã được cập nhật làm mẫu")
print("- Áp dụng tương tự cho các map còn lại")
print("- Skill chỉ hoạt động khi chơi Chiến Thần Lạc Hồng")
print("- Video skill: Tai_nguyen/video/skill_chien_than.mp4")
print("- Phím F để kích hoạt skill")
print("- Chi phí: 100 mana")
print("- Cooldown: 30 giây")
print("- Damage: 100 HP")
print("- Phạm vi: 400 pixel")
print("=" * 60)
