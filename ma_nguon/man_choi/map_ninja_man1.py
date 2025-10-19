import pygame
import os
import random
import math

from ma_nguon.doi_tuong.nhan_vat.nhan_vat import Character
from ma_nguon.doi_tuong.quai_vat.quai_vat import QuaiVat
from ma_nguon.doi_tuong.quai_vat.quai_vat_manh import Boss1
from ma_nguon.tien_ich.parallax import ParallaxBackground
from ma_nguon.giao_dien.action_buttons import ActionButtonsUI
from ma_nguon.man_choi.skill_video import SkillVideoPlayer


class mapninjaman1Scene:
    def __init__(self, game, player=None):
        self.game = game
        self.font = pygame.font.Font("Tai_nguyen/font/Fz-Donsky.ttf", 50)
        self.counter = 0

        # On-screen action buttons UI
        self.action_buttons = ActionButtonsUI(self.game.WIDTH, self.game.HEIGHT)
        
        # Khởi tạo hệ thống parallax background - phiên bản mùa thu
        self.parallax_bg = ParallaxBackground(self.game.WIDTH, self.game.HEIGHT, self.game.map_width)
        
         # Lớp 1: Mây / Mặt trời
        self.parallax_bg.add_layer(
            "Tai_nguyen/hinh_anh/canh_nen/mapninja/man1/may.png",
            speed_factor=0.1,
            y_pos=40,          # cao hơn 1 chút
            scale_factor=1.25
        )

        # Lớp 2: Núi xa
        self.parallax_bg.add_layer(
            "Tai_nguyen/hinh_anh/canh_nen/mapninja/man1/nui.png",
            speed_factor=0.25,
            y_pos=120,          # gần mặt trời hơn
            scale_factor=1.3
        )

        # Lớp 3: Nhà
        self.parallax_bg.add_layer(
            "Tai_nguyen/hinh_anh/canh_nen/mapninja/man1/nha.png",
            speed_factor=0.65,
            y_pos=160,         # cao hơn một chút
            scale_factor=1.2   # nhỏ lại để cân đối với cây và núi
        )

        # Lớp 4: Mặt đất
        self.parallax_bg.add_layer(
            "Tai_nguyen/hinh_anh/canh_nen/mapninja/man1/mat_dat.png",
            speed_factor=1.0,
            y_pos=340,         # nâng đất lên vừa tầm như bạn vẽ
            scale_factor=1.2,
            repeat_x=True
        )
        # Kiểm tra và sử dụng player truyền vào hoặc tạo mới
        if player:
            self.player = player
            # Đặt lại vị trí và hồi đầy máu cho màn mới
            self.player.x = 100
            self.player.y = 300
            self.player.base_y = 300
            # Hồi đầy máu (bao gồm cả equipment bonus)
            max_hp_with_equipment = self.player.get_max_hp_with_equipment() if hasattr(self.player, 'get_max_hp_with_equipment') else self.player.max_hp
            self.player.hp = max_hp_with_equipment
        else:
            # Code tạo player mới
            folder_nv = os.path.join("Tai_nguyen", "hinh_anh", "nhan_vat", "ninja")
            controls_p1 = {
                "left": pygame.K_LEFT,
                "right": pygame.K_RIGHT,
                "attack": pygame.K_a,
                "kick": pygame.K_s,
                "defend": pygame.K_d,
                "jump": pygame.K_w,
            }
            self.player = Character(100, 300, folder_nv, controls_p1, color=(0,255,0))
    
        # Cập nhật các thuộc tính cho nhân vật
        self.player.damage = 15       # Damage đấm
        self.player.kick_damage = 20  # Damage đá
    
        # MÀNT 1: ÍT QUÁI - DỄ NHẤT
        folder_qv = os.path.join("Tai_nguyen", "hinh_anh","quai_vat", "quai_vat_ninja")
        sound_qv = os.path.join("Tai_nguyen", "am_thanh", "hieu_ung")

        self.normal_enemies = []
        
        # Skill video system
        self.skill_video = None
        self.showing_skill_video = False
        
        # Chỉ tạo 2 nhóm quái vật - ít nhất
        total_enemies = 0
        for group in range(2):
            group_x = 800 + group * 1200  # Các nhóm cách xa nhau
            
            # Mỗi nhóm chỉ có 2 quái vật
            num_enemies = 2
            total_enemies += num_enemies
            for i in range(num_enemies):
                x_pos = group_x + random.randint(-100, 100)
                enemy = QuaiVat(x_pos, 300, folder_qv, sound_qv, color=(255, 200, 100), damage=8)  # Damage thấp
                # Thiết lập vùng hoạt động nhỏ - ít tấn công
                enemy.speed = 2
                enemy.home_x = x_pos
                enemy.patrol_range = 150
                enemy.aggro_range = 250
                enemy.hp = int(enemy.hp * 0.8)  # 20% ít máu hơn
                self.normal_enemies.append(enemy)

        # Chỉ có 1 boss dễ
        self.bosses = [
            Boss1(self.game.map_width - 400, 300, folder_qv, sound_qv),
        ]
        
        # Boss yếu hơn cho màn 1
        for boss in self.bosses:
            boss.hp = int(boss.hp * 0.7)  # 30% ít máu hơn
            boss.damage = int(boss.damage * 0.8)  # 20% ít sát thương hơn
            boss.speed = boss.speed * 0.9  # Chậm hơn 10%
            
        self.current_boss_index = 0
        self.current_boss = None
        
        # Lưu số quái ban đầu để tính điểm
        self.initial_enemy_count = total_enemies
        
        # Camera và giới hạn map
        self.camera_x = 0
        self.min_x = 0  # Giới hạn trái của map
        self.max_x = self.game.map_width - self.game.WIDTH  # Giới hạn phải của map
        
        # Biến đếm đã tiêu diệt tất cả kẻ địch
        self.all_enemies_defeated = False
        
        # Hiệu ứng lá rơi mùa thu nhẹ nhàng (ít hơn)
        self.falling_leaves = []
        leaf_colors = [
            (255, 215, 0),   # Vàng gold
            (255, 140, 0),   # Cam đậm
            (255, 165, 0),   # Cam
            (218, 165, 32),  # Vàng đậm
        ]
        
        # Ít lá hơn cho màn 1 (100 thay vì 150)
        for i in range(100):
            self.falling_leaves.append({
                'x': random.randint(0, self.game.map_width),
                'y': random.randint(-100, self.game.HEIGHT),
                'speed': random.uniform(1.0, 3.0),  # Chậm hơn
                'swing': random.uniform(0.3, 1.5),  # Ít dao động
                'swing_offset': random.uniform(0, 2 * math.pi),
                'size': random.randint(3, 6),  # Nhỏ hơn
                'color': random.choice(leaf_colors),
                'rotation': random.uniform(0, 360),
                'rotation_speed': random.uniform(-1.5, 1.5)  # Xoay chậm hơn
            })
        

    def handle_event(self, event):
        # Let UI handle clicks first
        if self.action_buttons.handle_event(event, player=self.player):
            return
        if event.type == pygame.KEYDOWN:
                        # Skill activation - F key (chỉ cho Chiến Thần Lạc Hồng)
            if event.key == pygame.K_f and "chien_than_lac_hong" in self.player.folder:
                self.activate_skill()
            elif event.key == pygame.K_ESCAPE:
                self.game.change_scene("menu")


    def spawn_next_boss(self):
        if self.current_boss_index < len(self.bosses):
            self.current_boss = self.bosses[self.current_boss_index]
            self.current_boss_index += 1
        else:
            self.current_boss = None
            # Kiểm tra xem đã tiêu diệt tất cả kẻ địch chưa
            if not self.normal_enemies:
                self.all_enemies_defeated = True
                # Chuyển sang màn 2 mùa thu
                self.game.change_scene("map_mua_thu_man2")

    
    def activate_skill(self):
        """Kích hoạt skill video cho Chiến Thần Lạc Hồng"""
        if self.player.can_use_skill():
            # Tạo video player với callback
            video_path = "Tai_nguyen/video/skill_chien_than.mp4"
            self.skill_video = SkillVideoPlayer(video_path, self.on_skill_finish)
            self.showing_skill_video = True
            
            # Sử dụng skill (trừ mana, reset cooldown)
            self.player.use_skill()
            print("[SKILL] Chiến Thần Lạc Hồng activated skill!")
    
    def on_skill_finish(self):
        """Callback khi skill video kết thúc"""
        print("[SKILL] Video finished, dealing damage to enemies...")
        self.damage_nearby_enemies()
        self.showing_skill_video = False
        self.skill_video = None
    
    def damage_nearby_enemies(self):
        """Gây damage cho tất cả quái vật trong phạm vi skill"""
        damage_count = 0
        
        # Damage normal enemies
        for enemy in self.normal_enemies[:]:
            distance = abs(enemy.x - self.player.x)
            if distance <= self.player.skill_range:
                enemy.hp -= self.player.skill_damage
                damage_count += 1
                if enemy.hp <= 0:
                    self.normal_enemies.remove(enemy)
                    if hasattr(self.player, 'score'):
                        self.player.score += enemy.score_value
        
        # Damage current boss if exists
        if hasattr(self, 'current_boss') and self.current_boss:
            distance = abs(self.current_boss.x - self.player.x)
            if distance <= self.player.skill_range:
                self.current_boss.hp -= self.player.skill_damage
                damage_count += 1
                if self.current_boss.hp <= 0:
                    if hasattr(self.player, 'score'):
                        self.player.score += self.current_boss.score_value
                    if hasattr(self, 'spawn_next_boss'):
                        self.spawn_next_boss()
        
        print(f"[SKILL] Damaged {damage_count} enemies!")

    def update(self):
        # Update skill video if showing
        if self.showing_skill_video and self.skill_video:
            self.skill_video.update()
            return  # Pause game logic while showing skill video
        
        keys = pygame.key.get_pressed()

        # --- Cập nhật camera theo nhân vật ---
        screen_center_x = self.game.WIDTH // 2
        
        # Nếu nhân vật vượt qua giữa màn hình, camera di chuyển theo
        if self.player.x > screen_center_x and self.player.x < self.game.map_width - screen_center_x:
            self.camera_x = self.player.x - screen_center_x
        
        # Giữ camera trong giới hạn map
        self.camera_x = max(0, min(self.camera_x, self.max_x))
        
        # Cập nhật hiệu ứng lá rơi
        for leaf in self.falling_leaves:
            leaf['y'] += leaf['speed']
            # Hiệu ứng dao động ngang như lá thật
            leaf['x'] += math.sin(pygame.time.get_ticks() * 0.001 + leaf['swing_offset']) * leaf['swing']
            leaf['rotation'] += leaf['rotation_speed']
            
            # Reset lá khi rơi hết màn hình
            if leaf['y'] > self.game.HEIGHT + 50:
                leaf['y'] = random.randint(-100, -50)
                leaf['x'] = random.randint(0, self.game.map_width)
        
        if self.player.hp > 0:
            old_x = self.player.x  # Lưu vị trí cũ để kiểm tra va chạm biên
            self.player.update(keys)
            
            # Đảm bảo nhân vật không rơi xuống dưới mặt đất
            if self.player.y > self.player.base_y:
                self.player.y = self.player.base_y
                self.player.jumping = False
                self.player.jump_vel = 0
                # Reset trạng thái action nếu đang nhảy
                if hasattr(self.player, 'action_type') and self.player.action_type == "nhay":
                    self.player.actioning = False
                    self.player.action_type = ""
            
            # Giới hạn nhân vật trong map
            if self.player.x < 0:
                self.player.x = 0
            elif self.player.x > self.game.map_width - 50:
                self.player.x = self.game.map_width - 50

            # Quái thường
            alive_enemies = []
            for enemy in self.normal_enemies:
                if enemy.hp > 0:
                    # Cập nhật AI quái vật với vùng hoạt động
                    enemy.update(target=self.player)
                    alive_enemies.append(enemy)
            self.normal_enemies = alive_enemies

            # Spawn boss khi hết quái
            if not self.normal_enemies:
                if not self.current_boss or self.current_boss.dead:
                    self.spawn_next_boss()

            # Boss update
            if self.current_boss and not self.current_boss.dead:
                self.current_boss.update(target=self.player)

            # Reset player damaged flag dựa trên trạng thái của tất cả enemies
            any_enemy_attacking = any(enemy.attacking and enemy.state in ["danh", "da"] for enemy in self.normal_enemies)
            if self.current_boss:
                any_enemy_attacking = any_enemy_attacking or (self.current_boss.attacking and self.current_boss.state in ["danh", "da", "nhay"])
            
            # Chỉ reset damaged flag khi KHÔNG có enemy nào đang tấn công
            if not any_enemy_attacking:
                self.player.damaged = False

            # Va chạm với quái thường
            for enemy in self.normal_enemies:
                rect_player = self.player.image.get_rect(topleft=(self.player.x, self.player.y))
                rect_enemy = enemy.image.get_rect(topleft=(enemy.x, enemy.y))

                # If player is performing an attack, use attack_hitbox for hit detection
                attacked = False
                if self.player.state in ["danh", "da"] and self.player.actioning and not enemy.damaged:
                    hitbox = self.player.attack_hitbox()
                    if hitbox.colliderect(rect_enemy):
                        if hasattr(self.player, 'animations') and self.player.state in self.player.animations:
                            max_frames = len(self.player.animations[self.player.state])
                            damage_frame_threshold = max(1, int(max_frames * 0.8))
                            if self.player.frame >= damage_frame_threshold:
                                if self.player.state == "danh":
                                    enemy.take_damage(self.player.get_effective_damage(), self.player.flip, self.player)
                                else:
                                    enemy.take_damage(self.player.kick_damage, self.player.flip, self.player)
                                enemy.damaged = True
                                attacked = True

                # Fallback: if not attacked and rects overlap (touching), allow enemy to still damage player
                if not attacked and rect_player.colliderect(rect_enemy):
                    # Quái chỉ gây damage ở frame cuối của đòn tấn công
                    if enemy.state in ["danh", "da"] and not self.player.damaged:
                        if hasattr(enemy, 'animations') and enemy.state in enemy.animations:
                            max_frames = len(enemy.animations[enemy.state])
                            damage_frame_threshold = max(1, int(max_frames * 0.8))
                            if enemy.frame >= damage_frame_threshold:
                                self.player.take_damage(enemy.damage, enemy.flip)
                                self.player.damaged = True
            # Va chạm với boss
            if self.current_boss:
                rect_boss = self.current_boss.image.get_rect(topleft=(self.current_boss.x, self.current_boss.y))
                rect_player = self.player.image.get_rect(topleft=(self.player.x, self.player.y))
                if rect_boss.colliderect(rect_player):
                    # Player chỉ gây damage ở frame cuối của đòn tấn công
                    if self.player.state == "danh" and self.player.actioning and not self.current_boss.damaged:
                        # Kiểm tra xem có đang ở frame cuối của animation không
                        if hasattr(self.player, 'animations') and self.player.state in self.player.animations:
                            max_frames = len(self.player.animations[self.player.state])
                            damage_frame_threshold = max(1, int(max_frames * 0.8))
                            if self.player.frame >= damage_frame_threshold:
                                self.current_boss.take_damage(self.player.get_effective_damage(), self.player.flip, self.player)
                                self.current_boss.damaged = True
                    elif self.player.state == "da" and self.player.actioning and not self.current_boss.damaged:
                        # Kiểm tra frame cuối cho đòn đá
                        if hasattr(self.player, 'animations') and self.player.state in self.player.animations:
                            max_frames = len(self.player.animations[self.player.state])
                            damage_frame_threshold = max(1, int(max_frames * 0.8))
                            if self.player.frame >= damage_frame_threshold:
                                self.current_boss.take_damage(self.player.kick_damage, self.player.flip, self.player)
                                self.current_boss.damaged = True

                    # Boss chỉ gây damage ở frame cuối của đòn tấn công
                    if self.current_boss.state in ["danh", "da", "nhay"] and not self.player.damaged:
                        # Kiểm tra xem có đang ở frame cuối của animation không
                        if hasattr(self.current_boss, 'animations') and self.current_boss.state in self.current_boss.animations:
                            max_frames = len(self.current_boss.animations[self.current_boss.state])
                            # Gây damage ở frame cuối hoặc gần cuối (frame 80-100% của animation)
                            damage_frame_threshold = max(1, int(max_frames * 0.8))
                            if self.current_boss.frame >= damage_frame_threshold:
                                # Sử dụng damage đặc biệt của boss nếu có
                                boss_damage = self.current_boss.damage
                                if hasattr(self.current_boss, 'get_current_damage'):
                                    boss_damage = self.current_boss.get_current_damage()
                                self.player.take_damage(boss_damage, self.current_boss.flip)
                                self.player.damaged = True
        else:
            # Player chết - chuyển đến màn hình Game Over
            if not hasattr(self, 'death_timer'):
                self.death_timer = pygame.time.get_ticks()
            
            # Cho phép animation chết hoàn thành (2 giây)
            current_time = pygame.time.get_ticks()
            if current_time - self.death_timer > 2000:
                # Tính điểm dựa trên số quái đã giết
                score = (len(self.bosses) - len([b for b in self.bosses if not b.dead])) * 1000
                score += (self.initial_enemy_count - len(self.normal_enemies)) * 100
                
                # Chuyển đến màn hình Game Over
                self.game.game_over_scene = self.game.load_scene("game_over", "NINJA - Màn 1", score)
                self.game.change_scene("game_over")
                return
            
            self.player.update(keys)
            if self.current_boss:
                self.current_boss.state = "dung_yen"
                self.current_boss.attacking = False
                self.current_boss.frame = 0
            for enemy in self.normal_enemies:
                enemy.state = "dung_yen"
                enemy.attacking = False
                enemy.frame = 0


    def draw_leaf(self, screen, leaf, camera_x):
        """Vẽ một lá với hiệu ứng xoay"""
        x = leaf['x'] - camera_x  # Điều chỉnh theo camera
        if -50 <= x < self.game.WIDTH + 50:  # Chỉ vẽ nếu gần màn hình
            # Tạo một surface nhỏ để vẽ lá
            leaf_surface = pygame.Surface((leaf['size'] * 2, leaf['size'] * 2), pygame.SRCALPHA)
            
            # Vẽ hình lá đơn giản (ellipse)
            pygame.draw.ellipse(leaf_surface, leaf['color'], 
                              (0, 0, leaf['size'] * 2, leaf['size']))
            
            # Xoay lá
            rotated_leaf = pygame.transform.rotate(leaf_surface, leaf['rotation'])
            
            # Lấy rect để căn giữa
            rect = rotated_leaf.get_rect(center=(x, leaf['y']))
            
            # Vẽ lên màn hình
            screen.blit(rotated_leaf, rect)


    def draw(self, screen):
        # If showing skill video, render it first
        if self.showing_skill_video and self.skill_video:
            screen.fill((0, 0, 0))  # Black background
            self.skill_video.draw(screen)
            return  # Don't draw game elements during skill video
                # Vẽ các lớp nền phía sau (từ xa đến gần)
        self.parallax_bg.draw_background_layers(screen, self.camera_x)
        
        # Vẽ hiệu ứng lá rơi phía sau nhân vật
        for leaf in self.falling_leaves:
            if leaf['y'] < 400:  # Lá ở phía sau
                self.draw_leaf(screen, leaf, self.camera_x)
        
        # Vẽ thông tin màn chơi (UI luôn cố định trên màn hình)
        text = self.font.render("NinJa- Màn 1: Đại chiến Ninja", True, (184, 134, 11))
        screen.blit(text, (screen.get_width()//2 - text.get_width()//2, 50))
        info = pygame.font.Font("Tai_nguyen/font/Fz-Donsky.ttf", 30).render("Nhấn ESC để về menu", True, (160, 82, 45))
        screen.blit(info, (screen.get_width()//2 - info.get_width()//2, 100))

        # Vẽ quái vật (với camera offset)
        for enemy in self.normal_enemies:
            # Chỉ vẽ quái vật trong tầm nhìn camera
            if enemy.x + 150 >= self.camera_x and enemy.x - 150 <= self.camera_x + self.game.WIDTH:
                enemy.draw(screen, self.camera_x)

        # Vẽ boss (với camera offset)
        if self.current_boss:
            self.current_boss.draw(screen, self.camera_x)

        # Vẽ nhân vật (với camera offset)
        self.player.draw(screen, self.camera_x)
        
        # Vẽ lá rơi phía trước nhân vật
        for leaf in self.falling_leaves:
            if leaf['y'] >= 400:  # Lá ở phía trước
                self.draw_leaf(screen, leaf, self.camera_x)
        
        # Vẽ các lớp nền phía trước (che phủ nhân vật) nếu có
        self.parallax_bg.draw_foreground_layers(screen, self.camera_x)

        # Draw UI buttons and HUD on top
        self.action_buttons.draw(screen, player=self.player)
        # Draw skill UI if player is Chiến Thần Lạc Hồng
        if "chien_than_lac_hong" in self.player.folder:
            self.draw_skill_ui(screen)
    def draw_skill_ui(self, screen):
        """Vẽ UI skill ở góc trên bên trái, dưới thanh máu/mana"""
        # Position below HP/Mana bars
        ui_x = 20
        ui_y = 84  # Below mana bar (20 + 30 + 8 + 18 + 8)
        ui_width = 300
        ui_height = 50
        
        # Background panel
        panel_rect = pygame.Rect(ui_x, ui_y, ui_width, ui_height)
        pygame.draw.rect(screen, (20, 20, 40), panel_rect)
        pygame.draw.rect(screen, (255, 215, 0), panel_rect, 2)  # Golden border
        
        # Skill icon with F key
        icon_size = 40
        icon_x = ui_x + 5
        icon_y = ui_y + 5
        icon_rect = pygame.Rect(icon_x, icon_y, icon_size, icon_size)
        pygame.draw.rect(screen, (50, 50, 100), icon_rect)
        pygame.draw.rect(screen, (255, 215, 0), icon_rect, 2)
        
        # F key text
        font_key = pygame.font.Font("Tai_nguyen/font/Fz-Futurik.ttf", 24)
        key_text = font_key.render("F", True, (255, 255, 255))
        screen.blit(key_text, (icon_x + icon_size//2 - key_text.get_width()//2, 
                               icon_y + icon_size//2 - key_text.get_height()//2))
        
        # Skill name and cooldown info
        font_title = pygame.font.Font("Tai_nguyen/font/Fz-Futurik.ttf", 18)
        font_small = pygame.font.Font("Tai_nguyen/font/Fz-Futurik.ttf", 14)
        
        text_x = icon_x + icon_size + 10
        
        # Title
        title_text = font_title.render("SKILL CHIẾN THẦN", True, (255, 215, 0))
        screen.blit(title_text, (text_x, ui_y + 5))
        
        # Cooldown display
        remaining = self.player.get_skill_cooldown_remaining()
        if remaining > 0:
            cd_text = font_small.render(f"Hồi chiêu: {remaining:.1f}s", True, (255, 150, 150))
        else:
            cd_text = font_small.render(f"Hồi chiêu: 30s", True, (150, 150, 150))
        screen.blit(cd_text, (text_x, ui_y + 28))
        
        # Status indicator on the right
        status_x = ui_x + ui_width - 70
        status_y = ui_y + ui_height // 2 - 15
        
        if remaining > 0:
            # Show countdown timer
            timer_text = font_title.render(f"{int(remaining)}s", True, (255, 100, 100))
            screen.blit(timer_text, (status_x, status_y))
        else:
            # Show READY with pulsing glow
            ready_text = font_title.render("READY!", True, (0, 255, 0))
            
            # Pulsing glow effect
            import math
            glow_alpha = int(155 + 100 * math.sin(pygame.time.get_ticks() / 200))
            glow_surface = pygame.Surface((ready_text.get_width() + 10, ready_text.get_height() + 10))
            glow_surface.fill((0, 255, 0))
            glow_surface.set_alpha(glow_alpha)
            screen.blit(glow_surface, (status_x - 5, status_y - 5))
            
            screen.blit(ready_text, (status_x, status_y))

