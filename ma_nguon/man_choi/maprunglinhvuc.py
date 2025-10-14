import pygame
import os
import random
import math

from ma_nguon.doi_tuong.nhan_vat.nhan_vat import Character
from ma_nguon.doi_tuong.quai_vat.quai_vat import QuaiVat
from ma_nguon.doi_tuong.quai_vat.quai_vat_manh import Boss1, Boss2, Boss3
from ma_nguon.tien_ich.parallax import ParallaxBackground
from ma_nguon.giao_dien.action_buttons import ActionButtonsUI


class MapRungLinhVucScene:
    def __init__(self, game,player=None):
        self.game = game
        self.font = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 50)
        self.counter = 0
        
        # Khởi tạo hệ thống parallax background
        self.parallax_bg = ParallaxBackground(self.game.WIDTH, self.game.HEIGHT, self.game.map_width)
        
        # Thêm các lớp cảnh nền từ xa đến gần (tốc độ tăng dần từ 0 đến 1)
        # Lớp 1: Trăng/Bầu trời (ở xa nhất, gần như đứng yên)
        self.parallax_bg.add_layer("tai_nguyen/hinh_anh/canh_nen/maptutien/bau_troi.png", speed_factor=0.05, y_pos=0)

        # Lớp 2: Núi xa (di chuyển chậm)
        self.parallax_bg.add_layer("tai_nguyen/hinh_anh/canh_nen/maptutien/nui.png", speed_factor=0.2, y_pos=10, scale_factor=0.8)

        # Lớp 3: Mặt đất (di chuyển cùng tốc độ camera) - cân bằng để không che cây đào
        self.parallax_bg.add_layer("tai_nguyen/hinh_anh/canh_nen/maptutien/mat_dat.png", speed_factor=1.0, y_pos=420, repeat_x=True, scale_factor=2.2)


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
        # Khởi tạo boss
        self.bosses = [
            Boss1(self.game.map_width - 800, 300, folder_qv, sound_qv),
            Boss2(self.game.map_width - 500, 300, folder_qv, sound_qv),
            Boss3(self.game.map_width - 200, 300, folder_qv, sound_qv)
        ]
        self.current_boss_index = 0
        self.current_boss = None
        # ⬅️ Thêm biến cutscene
        self.showing_cutscene = False
        self.cutscene_done = False
        self.cutscene_clip = None
        self.clip_start_time = 0
        self.clip_duration = 0
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
        
        # Hiệu ứng cánh hoa đào rơi
        self.falling_leaves = []
        leaf_colors = [
             (255, 182, 193),  # Hồng nhạt (Light Pink)
             (255, 105, 180),  # Hồng đậm (Hot Pink)
             (219, 112, 147),  # Hồng tím (Pale Violet Red)
             (199, 21, 133),   # Hồng tím đậm (Medium Violet Red)
             (178, 34, 34)     # Đỏ sậm (Firebrick)
        ]
        
        # tùy chỉnh hiệu ứng lá rơi nhẹ nhàng hơn
        for i in range(200):
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
        
        # Khởi tạo Action Buttons UI  
        self.action_buttons = ActionButtonsUI(self.game.WIDTH, self.game.HEIGHT)

    def handle_event(self, event):
        # Xử lý Action Buttons trước
        if self.action_buttons.handle_event(event, self.player):
            return  # Nếu action button được click thì không xử lý events khác
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.change_scene("menu")


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

        # Update hiệu ứng lá rơi
        for leaf in self.falling_leaves:
            leaf['y'] += leaf['speed']
            leaf['x'] += math.sin(pygame.time.get_ticks() * 0.001 + leaf['swing_offset']) * leaf['swing']
            leaf['rotation'] += leaf['rotation_speed']
            
            # Reset lá khi rơi xuống dưới màn hình
            if leaf['y'] > self.game.HEIGHT + 50:
                leaf['y'] = random.randint(-100, -10)
                leaf['x'] = random.randint(0, self.game.map_width)

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

            # Va chạm với quái thường
            for enemy in self.normal_enemies:
                rect_player = self.player.image.get_rect(topleft=(self.player.x, self.player.y))
                rect_enemy = enemy.image.get_rect(topleft=(enemy.x, enemy.y))
                    
                if rect_player.colliderect(rect_enemy):
                    # Player chỉ gây damage ở frame cuối của đòn tấn công
                    if self.player.state == "danh" and self.player.actioning and not enemy.damaged:
                        # Kiểm tra xem có đang ở frame cuối của animation không
                        if hasattr(self.player, 'animations') and self.player.state in self.player.animations:
                            max_frames = len(self.player.animations[self.player.state])
                            damage_frame_threshold = max(1, int(max_frames * 0.8))
                            if self.player.frame >= damage_frame_threshold:
                                enemy.take_damage(self.player.damage, self.player.flip)
                                enemy.damaged = True
                    elif self.player.state == "da" and self.player.actioning and not enemy.damaged:
                        # Kiểm tra frame cuối cho đòn đá
                        if hasattr(self.player, 'animations') and self.player.state in self.player.animations:
                            max_frames = len(self.player.animations[self.player.state])
                            damage_frame_threshold = max(1, int(max_frames * 0.8))
                            if self.player.frame >= damage_frame_threshold:
                                enemy.take_damage(self.player.kick_damage, self.player.flip)
                                enemy.damaged = True

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
        # Vẽ các lớp nền phía sau (từ xa đến gần)
        self.parallax_bg.draw_background_layers(screen, self.camera_x)
        
        # Vẽ hiệu ứng lá rơi (với camera offset)
        for leaf in self.falling_leaves:
            # Chỉ vẽ lá trong tầm nhìn camera
            screen_x = leaf['x'] - self.camera_x
            if -20 <= screen_x <= self.game.WIDTH + 20:
                # Tạo hình elip cho lá
                leaf_rect = pygame.Rect(screen_x - leaf['size']//2, leaf['y'] - leaf['size']//2, 
                                       leaf['size'], leaf['size'])
                pygame.draw.ellipse(screen, leaf['color'], leaf_rect)
                
                # Thêm viền nhẹ cho lá
                pygame.draw.ellipse(screen, (139, 69, 19), leaf_rect, 1)
        
        # Vẽ thông tin màn chơi (UI luôn cố định trên màn hình)
        text = self.font.render("Map Rừng Linh Vực", True, (255,255,255))
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