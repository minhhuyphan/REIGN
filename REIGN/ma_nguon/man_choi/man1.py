import pygame
import os
import random
import moviepy as mp

from ma_nguon.doi_tuong.nhan_vat.nhan_vat import Character
from ma_nguon.doi_tuong.quai_vat.quai_vat import QuaiVat
from ma_nguon.doi_tuong.quai_vat.quai_vat_manh import Boss1, Boss2, Boss3
from ma_nguon.tien_ich.parallax import ParallaxBackground


class Level1Scene:
    def __init__(self, game,player=None):
        self.game = game
        self.font = pygame.font.Font("tai_nguyen/font/Fz-Futurik.ttf", 50)
        self.counter = 0
        
        # Khởi tạo hệ thống parallax background
        self.parallax_bg = ParallaxBackground(self.game.WIDTH, self.game.HEIGHT, self.game.map_width)
        
        # Thêm các lớp cảnh nền từ xa đến gần (tốc độ tăng dần từ 0 đến 1)
        # Lớp 1: Trăng/Bầu trời (ở xa nhất, gần như đứng yên)
        self.parallax_bg.add_layer("tai_nguyen/hinh_anh/canh_nen/trang_sao.png", speed_factor=0.05, y_pos=0)
        
        # Lớp 2: Mây (di chuyển rất chậm)
        self.parallax_bg.add_layer("tai_nguyen/hinh_anh/canh_nen/may.png", speed_factor=0.1, y_pos=50)
        
        # Lớp 3: Núi xa (di chuyển chậm)
        self.parallax_bg.add_layer("tai_nguyen/hinh_anh/canh_nen/nui.png", speed_factor=0.2, y_pos=10, scale_factor=1.5)
        
        # Lớp 4: Cây xa (di chuyển nhanh hơn núi)
        self.parallax_bg.add_layer("tai_nguyen/hinh_anh/canh_nen/cay_xa.png", speed_factor=0.4, y_pos=150, scale_factor=1.5)

        # Lớp 5: Nhà (di chuyển gần bằng mặt đất)
        self.parallax_bg.add_layer("tai_nguyen/hinh_anh/canh_nen/nha.png", speed_factor=0.6, y_pos=80, scale_factor=1.5)

        # Lớp 6: Mặt đất (di chuyển cùng tốc độ camera)
        self.parallax_bg.add_layer("tai_nguyen/hinh_anh/canh_nen/mat_dat.png", speed_factor=1.0, y_pos=230, repeat_x=True)
        
        # Lớp 7: Cây gần (phía trước nhân vật, di chuyển nhanh hơn camera)
        self.parallax_bg.add_layer("tai_nguyen/hinh_anh/canh_nen/cay_gan.png", speed_factor=1.2, y_pos=400, scale_factor=1.5, above_player=True)

        # Khởi tạo player
        folder_nv = os.path.join("tai_nguyen", "hinh_anh", "nhan_vat")
        controls_p1 = {
            "left": pygame.K_LEFT,
            "right": pygame.K_RIGHT,
            "attack": pygame.K_a,
            "kick": pygame.K_s,
            "defend": pygame.K_d,
            "jump": pygame.K_w,
        }
        self.player = Character(100, 300, folder_nv, controls_p1, color=(0,255,0))
        self.player.damage = 15       # Damage đấm
        self.player.kick_damage = 20  # Damage đá

        # Khởi tạo quái vật thường dọc theo map dài
        folder_qv = os.path.join("tai_nguyen", "hinh_anh", "quai_vat")
        sound_qv = os.path.join("tai_nguyen", "am_thanh", "hieu_ung")

        self.normal_enemies = []
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

    def play_cutscene(self, video_path):  # ⬅️ thêm mới
        self.showing_cutscene = True
        self.cutscene_done = False
        self.cutscene_clip = mp.VideoFileClip(video_path)
        self.clip_duration = self.cutscene_clip.duration
        self.clip_start_time = pygame.time.get_ticks()


    def handle_event(self, event):
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
