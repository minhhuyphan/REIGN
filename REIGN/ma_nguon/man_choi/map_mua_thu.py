import pygame
import os
import random
import moviepy as mp
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from doi_tuong.nhan_vat.nhan_vat import Character
from doi_tuong.quai_vat.quai_vat import QuaiVat
from doi_tuong.quai_vat.quai_vat_manh import Boss1, Boss2, Boss3
from tien_ich.parallax import ParallaxBackground


class MapMuaThuScene:
    def __init__(self, game, player=None):
        self.game = game
        self.font = pygame.font.Font("../Tai_nguyen/font/Fz-Futurik.ttf", 50)
        self.counter = 0
        
        # Khởi tạo hệ thống parallax background cho mùa thu
        self.parallax_bg = ParallaxBackground(self.game.WIDTH, self.game.HEIGHT, self.game.map_width)
        
        # Thêm các lớp cảnh nền mùa thu từ xa đến gần
        # Lớp 1: Bầu trời mùa thu (ở xa nhất, gần như đứng yên)
        self.parallax_bg.add_layer("../Tai_nguyen/hinh_anh/canh_nen/mapmuathu/bau_troi.png", speed_factor=0.05, y_pos=0)
        
        # Lớp 2: Mây mùa thu (di chuyển rất chậm) - Làm nhỏ lại
        self.parallax_bg.add_layer("../Tai_nguyen/hinh_anh/canh_nen/mapmuathu/may.png", speed_factor=0.1, y_pos=50, scale_factor=0.7)
        
        # Lớp 3: Núi xa mùa thu (di chuyển chậm)
        self.parallax_bg.add_layer("../Tai_nguyen/hinh_anh/canh_nen/mapmuathu/nui.png", speed_factor=0.2, y_pos=10, scale_factor=1.5)
        
        # Bỏ hết cây (theo yêu cầu)

        # Bỏ qua Lớp 5: Nhà mùa thu (đã bỏ theo yêu cầu)

        # Lớp 6: Mặt đất mùa thu với lá rơi (di chuyển cùng tốc độ camera)
        self.parallax_bg.add_layer("../Tai_nguyen/hinh_anh/canh_nen/mapmuathu/mat_dat.png", speed_factor=1.0, y_pos=230, repeat_x=True)

        # Khởi tạo quái vật thường dọc theo map dài
        folder_qv = os.path.join("../Tai_nguyen", "hinh_anh", "quai_vat")
        sound_qv = os.path.join("../Tai_nguyen", "am_thanh", "hieu_ung")

        self.normal_enemies = []
        for i in range(12):  # Số lượng quái vật vừa phải cho map mùa thu
            x_pos = 700 + i * 350  # Đặt quái vật dọc theo map với khoảng cách hơi xa hơn
            enemy = QuaiVat(x_pos, 300, folder_qv, sound_qv, color=(255,100,0), damage=12)  # Màu cam cho mùa thu
            # Thiết lập vùng hoạt động cho quái vật
            enemy.home_x = x_pos
            enemy.patrol_range = 250  # Khoảng cách di chuyển tối đa từ home_x
            enemy.aggro_range = 320   # Khoảng cách phát hiện và tấn công người chơi
            self.normal_enemies.append(enemy)

        # Khởi tạo boss mùa thu (mạnh hơn một chút)
        self.bosses = [
            Boss1(self.game.map_width - 900, 300, folder_qv, sound_qv),
            Boss2(self.game.map_width - 600, 300, folder_qv, sound_qv),
            Boss3(self.game.map_width - 300, 300, folder_qv, sound_qv)
        ]
        # Tăng sức mạnh cho boss mùa thu
        for boss in self.bosses:
            boss.hp = int(boss.hp * 1.2)  # Tăng 20% HP
            boss.damage = int(boss.damage * 1.1)  # Tăng 10% damage
            
        self.current_boss_index = 0
        self.current_boss = None

        # Cutscene variables
        self.showing_cutscene = False
        self.cutscene_done = False
        self.cutscene_clip = None
        self.clip_start_time = 0
        self.clip_duration = 0
        
        # Camera và giới hạn map
        self.camera_x = 0
        self.min_x = 0
        self.max_x = self.game.map_width - self.game.WIDTH
        
        # Khởi tạo player
        if player:
            self.player = player  # lấy player từ màn chọn
            self.player.x = 100
            self.player.y = 300
            self.player.base_y = 300
        else:
            folder_nv = "../Tai_nguyen/hinh_anh/nhan_vat"
            controls_p1 = {
                "left": pygame.K_LEFT,
                "right": pygame.K_RIGHT,
                "attack": pygame.K_a,
                "kick": pygame.K_s,
                "defend": pygame.K_d,
                "jump": pygame.K_w,
            }
            self.player = Character(100, 300, folder_nv, controls_p1, color=(0,255,0))
            self.player.base_y = 300
            self.player.damage = 15
            self.player.kick_damage = 20

    def play_cutscene(self, video_path):
        try:
            self.showing_cutscene = True
            self.cutscene_done = False
            self.cutscene_clip = mp.VideoFileClip(video_path)
            self.clip_duration = self.cutscene_clip.duration
            self.clip_start_time = pygame.time.get_ticks()
        except:
            # Nếu không có video thì bỏ qua cutscene
            self.showing_cutscene = False
            self.cutscene_done = True

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.change_scene("menu")

    def spawn_next_boss(self):
        if self.current_boss_index < len(self.bosses):
            # Nếu là Boss3 thì chơi video cutscene trước (nếu có)
            if self.current_boss_index == 2 and not self.cutscene_done:
                self.play_cutscene("../Tai_nguyen/video/boss3_intro.mp4")
                return

            self.current_boss = self.bosses[self.current_boss_index]
            self.current_boss_index += 1
        else:
            self.current_boss = None
            # Kiểm tra xem đã tiêu diệt tất cả kẻ địch chưa
            if not self.normal_enemies:
                # Chuyển về menu hoặc màn victory
                self.game.change_scene("victory")

    def update(self):
        keys = pygame.key.get_pressed()

        # Nếu đang chiếu video cutscene thì tạm dừng game
        if self.showing_cutscene:
            now = pygame.time.get_ticks()
            elapsed = (now - self.clip_start_time) / 1000.0
            if elapsed >= self.clip_duration:
                self.showing_cutscene = False
                self.cutscene_done = True
                self.spawn_next_boss()
            return

        # Cập nhật camera theo nhân vật
        screen_center_x = self.game.WIDTH // 2
        
        if self.player.x > screen_center_x and self.player.x < self.game.map_width - screen_center_x:
            self.camera_x = self.player.x - screen_center_x
        
        # Giữ camera trong giới hạn map
        self.camera_x = max(0, min(self.camera_x, self.max_x))
        
        if self.player.hp > 0:
            old_x = self.player.x
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

            # Va chạm với quái thường
            for enemy in self.normal_enemies:
                rect_player = self.player.image.get_rect(topleft=(self.player.x, self.player.y))
                rect_enemy = enemy.image.get_rect(topleft=(enemy.x, enemy.y))
                if rect_player.colliderect(rect_enemy):
                    if self.player.state == "danh" and not enemy.damaged:
                        enemy.take_damage(self.player.damage, self.player.flip)
                        enemy.damaged = True
                    elif self.player.state == "da" and not enemy.damaged:
                        enemy.take_damage(self.player.kick_damage, self.player.flip)
                        enemy.damaged = True

                    if enemy.state in ["danh", "da"] and not self.player.damaged:
                        self.player.take_damage(enemy.damage, enemy.flip)
                        self.player.damaged = True
                        
            # Va chạm với boss
            if self.current_boss:
                rect_boss = self.current_boss.image.get_rect(topleft=(self.current_boss.x, self.current_boss.y))
                rect_player = self.player.image.get_rect(topleft=(self.player.x, self.player.y))
                if rect_boss.colliderect(rect_player):
                    if self.player.state == "danh" and not self.current_boss.damaged:
                        self.current_boss.take_damage(self.player.damage, self.player.flip)
                        self.current_boss.damaged = True
                    elif self.player.state == "da" and not self.current_boss.damaged:
                        self.current_boss.take_damage(self.player.kick_damage, self.player.flip)
                        self.current_boss.damaged = True

                    if self.current_boss.state in ["danh", "da"] and not self.player.damaged:
                        self.player.take_damage(self.current_boss.damage, self.current_boss.flip)
                        self.player.damaged = True

        else:
            # Player chết
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
        if self.showing_cutscene and self.cutscene_clip:
            now = pygame.time.get_ticks()
            elapsed = (now - self.clip_start_time) / 1000.0
            try:
                frame = self.cutscene_clip.get_frame(elapsed)
                frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0,1))
                screen.blit(pygame.transform.scale(frame_surface, screen.get_size()), (0,0))
                return
            except:
                # Nếu lỗi khi phát video thì kết thúc cutscene
                self.showing_cutscene = False
                self.cutscene_done = True

        # Vẽ các lớp nền phía sau (từ xa đến gần)
        self.parallax_bg.draw_background_layers(screen, self.camera_x)
        
        # Vẽ thông tin màn chơi mùa thu
        text = self.font.render("Map Mùa Thu - Thử Thách Mới!", True, (255,200,100))
        screen.blit(text, (screen.get_width()//2 - text.get_width()//2, 50))
        info = self.font.render("Nhấn ESC để về menu", True, (255,255,0))
        screen.blit(info, (screen.get_width()//2 - info.get_width()//2, 120))

        # Vẽ quái vật (với camera offset)
        for enemy in self.normal_enemies:
            if enemy.x + 150 >= self.camera_x and enemy.x - 150 <= self.camera_x + self.game.WIDTH:
                enemy.draw(screen, self.camera_x)

        # Vẽ boss (với camera offset)
        if self.current_boss:
            self.current_boss.draw(screen, self.camera_x)

        # Vẽ nhân vật (với camera offset)
        self.player.draw(screen, self.camera_x)
        
        # Vẽ các lớp nền phía trước (che phủ nhân vật)
        self.parallax_bg.draw_foreground_layers(screen, self.camera_x)