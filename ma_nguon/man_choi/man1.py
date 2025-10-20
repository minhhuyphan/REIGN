import pygame
import os
import random
import math
import moviepy as mp

from ma_nguon.doi_tuong.nhan_vat.nhan_vat import Character
from ma_nguon.doi_tuong.quai_vat.quai_vat import QuaiVat
from ma_nguon.doi_tuong.quai_vat.quai_vat_manh import Boss1, Boss2, Boss3
from ma_nguon.tien_ich.parallax import ParallaxBackground
from ma_nguon.giao_dien.action_buttons import ActionButtonsUI
from ma_nguon.tien_ich.bullet_handler import update_bullets, draw_bullets
from ma_nguon.man_choi.skill_video import SkillVideoPlayer


class Level1Scene:
    def __init__(self, game,player=None):
        self.game = game
        self.font = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 50)
        self.counter = 0
        
        # Khởi tạo hệ thống parallax background
        self.parallax_bg = ParallaxBackground(self.game.WIDTH, self.game.HEIGHT, self.game.map_width)
        
        # Thêm các lớp cảnh nền từ xa đến gần (tốc độ tăng dần từ 0 đến 1)
        # Lớp 1: Trăng/Bầu trời (ở xa nhất, gần như đứng yên)
        self.parallax_bg.add_layer("tai_nguyen/hinh_anh/canh_nen//man1/trang_sao.png", speed_factor=0.05, y_pos=0)
        
        # Lớp 2: Mây (di chuyển rất chậm)
        self.parallax_bg.add_layer("tai_nguyen/hinh_anh/canh_nen/man1/may.png", speed_factor=0.1, y_pos=50)
        
        # Lớp 3: Núi xa (di chuyển chậm)
        self.parallax_bg.add_layer("tai_nguyen/hinh_anh/canh_nen/man1/nui.png", speed_factor=0.2, y_pos=10, scale_factor=1.5)
        
        # Lớp 4: Cây xa (di chuyển nhanh hơn núi)
        self.parallax_bg.add_layer("tai_nguyen/hinh_anh/canh_nen/man1/cay_xa.png", speed_factor=0.4, y_pos=150, scale_factor=1.5)

        # Lớp 5: Nhà (di chuyển gần bằng mặt đất)
        self.parallax_bg.add_layer("tai_nguyen/hinh_anh/canh_nen/man1/nha.png", speed_factor=0.6, y_pos=80, scale_factor=1.5)

        # Lớp 6: Mặt đất (di chuyển cùng tốc độ camera)
        self.parallax_bg.add_layer("tai_nguyen/hinh_anh/canh_nen/man1/mat_dat.png", speed_factor=1.0, y_pos=230, repeat_x=True)
        
        # Lớp 7: Cây gần (phía trước nhân vật, di chuyển nhanh hơn camera)
        self.parallax_bg.add_layer("tai_nguyen/hinh_anh/canh_nen/man1/cay_gan.png", speed_factor=1.6, y_pos=500, scale_factor=2.5, above_player=True)

        # Khởi tạo player
        folder_nv = os.path.join("tai_nguyen", "hinh_anh", "nhan_vat")
        # Không truyền controls để Character tự lấy từ settings
        self.player = Character(100, 300, folder_nv, color=(0,255,0))
        self.player.damage = 15       # Damage đấm
        self.player.kick_damage = 20  # Damage đá

        # Khởi tạo quái vật thường dọc theo map dài
        folder_qv = os.path.join("tai_nguyen", "hinh_anh", "quai_vat", "quai_vat_bay")
        sound_qv = os.path.join("tai_nguyen", "am_thanh", "hieu_ung")

        self.normal_enemies = []
        # Items dropped on the ground
        self.items = []
        for i in range(15):  # Tăng số lượng quái vật
            x_pos = 600 + i * 300  # Đặt quái vật dọc theo map dài
            enemy = QuaiVat(x_pos, 300, folder_qv, sound_qv, color=(255,0,0), damage=10)
            # Thiết lập vùng hoạt động cho quái vật
            enemy.home_x = x_pos
            enemy.patrol_range = 200  # Khoảng cách di chuyển tối đa từ home_x
            enemy.aggro_range = 300   # Khoảng cách phát hiện và tấn công người chơi
            self.normal_enemies.append(enemy)
        # Khởi tạo boss với kích thước tùy chỉnh cho từng boss
        self.bosses = [
            Boss1(self.game.map_width - 800, 300, folder_qv, sound_qv, target_size=(150, 150)),
            Boss2(self.game.map_width - 500, 260, folder_qv, sound_qv, target_size=(200, 200)),
            Boss3(self.game.map_width - 200, 200, folder_qv, sound_qv, target_size=(250, 250))
        ]
        self.current_boss_index = 0
        self.current_boss = None
        # ⬅️ Thêm biến cutscene
        self.showing_cutscene = False
        self.cutscene_done = False
        self.cutscene_clip = None
        self.clip_start_time = 0
        self.clip_duration = 0
        
        # Skill video system
        self.skill_video = None
        self.showing_skill_video = False
        
        # Camera và giới hạn map
        self.camera_x = 0
        self.min_x = 0  # Giới hạn trái của map
        self.max_x = self.game.map_width - self.game.WIDTH  # Giới hạn phải của map
        # Thay đổi từ dòng 124-137
        if player:
            self.player = player  # lấy player từ màn chọn
            self.player.x = 100
            self.player.y = 300
            self.player.base_y = 300
        else:
            folder_nv = "tai_nguyen/hinh_anh/nhan_vat"
            # Không truyền controls để Character tự lấy từ settings
            self.player = Character(100, 300, folder_nv, color=(0,255,0))
            self.player.base_y = 300
            self.player.damage = 15
            self.player.kick_damage = 20
        
        # Khởi tạo Action Buttons UI  
        self.action_buttons = ActionButtonsUI(self.game.WIDTH, self.game.HEIGHT)

    def play_cutscene(self, video_path):  # ⬅️ thêm mới
        self.showing_cutscene = True
        self.cutscene_done = False
        self.cutscene_clip = mp.VideoFileClip(video_path)
        self.clip_duration = self.cutscene_clip.duration
        self.clip_start_time = pygame.time.get_ticks()


    def handle_event(self, event):
        # Xử lý Action Buttons trước
        if self.action_buttons.handle_event(event, self.player):
            return  # Nếu action button được click thì không xử lý events khác
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.change_scene("menu")
            
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
                        print(f"[SKILL] Không đủ mana ({self.player.mana}/{self.player.skill_mana_cost})")
    
    def activate_skill(self):
        """Kích hoạt skill - phát video và gây sát thương"""
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
        """Gây sát thương cho tất cả quái vật trong phạm vi"""
        damaged_count = 0
        
        # Damage quái thường
        for enemy in self.normal_enemies:
            if enemy.hp > 0:
                # Kiểm tra khoảng cách
                distance = abs(enemy.x - self.player.x)
                if distance <= self.player.skill_range:
                    enemy.hp -= self.player.skill_damage
                    enemy.damaged = True
                    damaged_count += 1
                    print(f"[SKILL] Hit enemy at distance {distance:.0f}px, HP: {enemy.hp}")
        
        # Damage boss
        if self.current_boss and self.current_boss.hp > 0:
            distance = abs(self.current_boss.x - self.player.x)
            if distance <= self.player.skill_range:
                self.current_boss.hp -= self.player.skill_damage
                self.current_boss.damaged = True
                damaged_count += 1
                print(f"[SKILL] Hit BOSS at distance {distance:.0f}px, HP: {self.current_boss.hp}")
        
        print(f"[SKILL] Damaged {damaged_count} enemies!")



    def spawn_next_boss(self):
        if self.current_boss_index < len(self.bosses):
            # Nếu là Boss3 thì chơi video cutscene trước
            if self.current_boss_index == 2 and not self.cutscene_done:
                self.play_cutscene("tai_nguyen/video/boss3_intro.mp4")
                return

            self.current_boss = self.bosses[self.current_boss_index]
            self.current_boss_index += 1
        else:
            self.current_boss = None
            # Kiểm tra xem đã tiêu diệt tất cả kẻ địch chưa
            if not self.normal_enemies:
                # Chuyển sang màn 2
                self.game.change_scene("level2")



    def update(self):
        keys = pygame.key.get_pressed()

        # Update Action Buttons
        self.action_buttons.update()
        
        # Nếu đang phát skill video thì pause game
        if self.showing_skill_video and self.skill_video:
            self.skill_video.update()
            return

        # Nếu đang chiếu video cutscene thì tạm dừng game
        if self.showing_cutscene:  # ⬅️ thêm mới
            now = pygame.time.get_ticks()
            elapsed = (now - self.clip_start_time) / 1000.0
            if elapsed >= self.clip_duration:
                self.showing_cutscene = False
                self.cutscene_done = True
                self.spawn_next_boss()
            return

        # --- Cập nhật camera theo nhân vật ---
        screen_center_x = self.game.WIDTH // 2
        
        # Nếu nhân vật vượt qua giữa màn hình, camera di chuyển theo
        if self.player.x > screen_center_x and self.player.x < self.game.map_width - screen_center_x:
            self.camera_x = self.player.x - screen_center_x
        
        # Giữ camera trong giới hạn map
        self.camera_x = max(0, min(self.camera_x, self.max_x))
        
        if self.player.hp > 0:
            old_x = self.player.x  # Lưu vị trí cũ để kiểm tra va chạm biên
            self.player.update(keys)
            
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
                else:
                    # Collect drops from dead enemies into the scene
                    if hasattr(enemy, 'spawned_drops') and enemy.spawned_drops:
                        for it in enemy.spawned_drops:
                            self.items.append(it)
                            print(f"[DEBUG] Collected drop into scene: {type(it).__name__} at ({it.x},{it.y})")
                        enemy.spawned_drops = []
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
                any_enemy_attacking = any_enemy_attacking or (self.current_boss.attacking and self.current_boss.state in ["danh", "da"])
            
            # Chỉ reset damaged flag khi KHÔNG có enemy nào đang tấn công
            if not any_enemy_attacking:
                self.player.damaged = False

            # Cập nhật viên đạn của player
            update_bullets(self.player, self.normal_enemies, self.current_boss)

            # Va chạm với quái thường
            for enemy in self.normal_enemies:
                rect_player = self.player.image.get_rect(topleft=(self.player.x, self.player.y))
                rect_enemy = enemy.image.get_rect(topleft=(enemy.x, enemy.y))

                # If player is performing an attack, use attack_hitbox for hit detection
                attacked = False
                if self.player.state in ["danh", "da"] and self.player.actioning and not enemy.damaged:
                    hitbox = self.player.attack_hitbox()
                    # Translate hitbox to camera coordinates if needed (we're using world coordinates here)
                    if hitbox.colliderect(rect_enemy):
                        # Only apply on last frames of the attack animation
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

                # Fallback: if not attacked and rects overlap (touching), allow enemy to still damage player or vice versa
                if not attacked and rect_player.colliderect(rect_enemy):
                    # Quái chỉ gây damage ở frame cuối của đòn tấn công
                    if enemy.state in ["danh", "da"] and not self.player.damaged:
                        if hasattr(enemy, 'animations') and enemy.state in enemy.animations:
                            max_frames = len(enemy.animations[enemy.state])
                            damage_frame_threshold = max(1, int(max_frames * 0.8))
                            if enemy.frame >= damage_frame_threshold:
                                self.player.take_damage(enemy.damage, enemy.flip)
                                self.player.damaged = True

                    # Quái chỉ gây damage ở frame cuối của đòn tấn công
                    if enemy.state in ["danh", "da"] and not self.player.damaged:
                        # Kiểm tra xem có đang ở frame cuối của animation không
                        if hasattr(enemy, 'animations') and enemy.state in enemy.animations:
                            max_frames = len(enemy.animations[enemy.state])
                            # Gây damage ở frame cuối hoặc gần cuối (frame 80-100% của animation)
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
                                self.current_boss.take_damage(self.player.damage, self.player.flip)
                                self.current_boss.damaged = True
                    elif self.player.state == "da" and self.player.actioning and not self.current_boss.damaged:
                        # Kiểm tra frame cuối cho đòn đá
                        if hasattr(self.player, 'animations') and self.player.state in self.player.animations:
                            max_frames = len(self.player.animations[self.player.state])
                            damage_frame_threshold = max(1, int(max_frames * 0.8))
                            if self.player.frame >= damage_frame_threshold:
                                self.current_boss.take_damage(self.player.kick_damage, self.player.flip)
                                self.current_boss.damaged = True

                    # Boss chỉ gây damage ở frame cuối của đòn tấn công
                    if self.current_boss.state in ["danh", "da"] and not self.player.damaged:
                        # Kiểm tra xem có đang ở frame cuối của animation không
                        if hasattr(self.current_boss, 'animations') and self.current_boss.state in self.current_boss.animations:
                            max_frames = len(self.current_boss.animations[self.current_boss.state])
                            # Gây damage ở frame cuối hoặc gần cuối (frame 80-100% của animation)
                            damage_frame_threshold = max(1, int(max_frames * 0.8))
                            if self.current_boss.frame >= damage_frame_threshold:
                                self.player.take_damage(self.current_boss.damage, self.current_boss.flip)
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
                if hasattr(self, 'initial_enemy_count'):
                    score += (self.initial_enemy_count - len(self.normal_enemies)) * 100
                
                # Chuyển đến màn hình Game Over
                self.game.game_over_scene = self.game.load_scene("game_over", "Level 1", score)
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


    def draw(self, screen):
        # Nếu đang phát skill video, vẽ video toàn màn hình
        if self.showing_skill_video and self.skill_video:
            # Nền đen để flash trắng nổi bật hơn
            screen.fill((0, 0, 0))
            # Vẽ video skill (hoặc white flash)
            self.skill_video.draw(screen)
            return
        
        if self.showing_cutscene and self.cutscene_clip:  # ⬅️ thêm mới
            now = pygame.time.get_ticks()
            elapsed = (now - self.clip_start_time) / 1000.0
            frame = self.cutscene_clip.get_frame(elapsed)
            frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0,1))
            screen.blit(pygame.transform.scale(frame_surface, screen.get_size()), (0,0))
            return

        # Vẽ các lớp nền phía sau (từ xa đến gần)
        self.parallax_bg.draw_background_layers(screen, self.camera_x)
        
        # Vẽ thông tin màn chơi (UI luôn cố định trên màn hình)
        text = self.font.render("Đây là màn chơi chính!", True, (255,255,255))
        screen.blit(text, (screen.get_width()//2 - text.get_width()//2, 50))
        info = self.font.render("Nhấn ESC để về menu", True, (255,255,0))
        screen.blit(info, (screen.get_width()//2 - info.get_width()//2, 120))

        # Vẽ items rơi (với camera offset)
        for item in self.items:
            item.draw(screen, self.camera_x)

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
        
        # Vẽ viên đạn
        draw_bullets(self.player, screen, self.camera_x)
        
        # Vẽ các lớp nền phía trước (che phủ nhân vật)
        self.parallax_bg.draw_foreground_layers(screen, self.camera_x)
        
        # --- Pickup items ---
        remaining_items = []
        for item in self.items:
            if item.picked:
                continue
            item_rect = pygame.Rect(item.x, item.y, 24, 24)
            player_rect = pygame.Rect(self.player.x, self.player.y, 50, 80)
            if player_rect.colliderect(item_rect):
                item.on_pickup(self.player)
                # Trigger HUD pickup animation
                if hasattr(self, 'action_buttons'):
                    if type(item).__name__ == 'Gold':
                        amount = getattr(item, 'amount', 0)
                        self.action_buttons.trigger_pickup_animation('gold', amount)
                        # persist to profile if user logged in
                        if hasattr(self.game, 'current_user') and self.game.current_user:
                            profile = self.game.profile or {}
                            profile['gold'] = profile.get('gold', 0) + amount
                            self.game.profile = profile
                            self.game.save_current_profile()
                    elif type(item).__name__ in ('HealthPotion', 'Health_Potion'):
                        self.action_buttons.trigger_pickup_animation('hp', 1)
                        # save potions if desired (not implemented here)
                    elif type(item).__name__ in ('ManaPotion', 'Mana_Potion'):
                        self.action_buttons.trigger_pickup_animation('mp', 1)
            else:
                remaining_items.append(item)
        self.items = remaining_items

        # Vẽ Action Buttons UI (luôn ở trên cùng, không bị ảnh hưởng camera)
        self.action_buttons.draw(screen, player=self.player)
        
        # Vẽ skill cooldown UI (chỉ cho Chiến Thần Lạc Hồng)
        if "chien_than_lac_hong" in self.player.folder:
            self.draw_skill_ui(screen)
    
    def draw_skill_ui(self, screen):
        """Vẽ UI hiển thị cooldown và mana skill - Dưới thanh máu/mana"""
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
                pulse = abs(math.sin(pygame.time.get_ticks() / 300.0))
                glow_alpha = int(100 + pulse * 100)
                glow_surface = pygame.Surface((80, 30), pygame.SRCALPHA)
                pygame.draw.ellipse(glow_surface, (0, 255, 0, glow_alpha), glow_surface.get_rect())
                screen.blit(glow_surface, (status_x - 10, status_y - 5))
            else:
                # Không đủ mana
                need_text = font_small.render(f"Cần {self.player.skill_mana_cost} MP", True, (255, 100, 100))
                screen.blit(need_text, (status_x - 10, status_y + 8))