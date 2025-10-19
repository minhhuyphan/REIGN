import pygame
import os
import random
import math
import traceback

from ma_nguon.doi_tuong.nhan_vat.nhan_vat import Character
from ma_nguon.doi_tuong.quai_vat.quai_vat import QuaiVat
from ma_nguon.doi_tuong.quai_vat.quai_vat_manh import Boss1, Boss2, Boss3
from ma_nguon.tien_ich.parallax import ParallaxBackground
from ma_nguon.giao_dien.action_buttons import ActionButtonsUI
from ma_nguon.tien_ich import bullet_handler


class MapCongNgheScene:
    def __init__(self, game, player=None):
        print("[DEBUG] Init MapCongNgheScene")
        self.game = game

        # nếu init thất bại, set flag để skip update/draw/handle_event
        self.initialized = True

        try:
            # project root để tải tài nguyên an toàn
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            self._project_root = project_root  # lưu để dùng khi log
            # Font an toàn: dùng Font file nếu tồn tại, ngược lại fallback SysFont
            try:
                font_path = os.path.join(project_root, "tai_nguyen", "font", "Fz-Donsky.ttf")
                if os.path.isfile(font_path):
                    self.font = pygame.font.Font(font_path, 50)
                else:
                    self.font = pygame.font.SysFont(None, 50)
            except Exception:
                self.font = pygame.font.SysFont(None, 50)

            self.counter = 0

            # On-screen action buttons UI (match Map Mùa Thu)
            self.action_buttons = ActionButtonsUI(self.game.WIDTH, self.game.HEIGHT)

            # Khởi tạo hệ thống parallax background (guard nếu lỗi)
            try:
                self.parallax_bg = ParallaxBackground(self.game.WIDTH, self.game.HEIGHT, self.game.map_width)
            except Exception as e:
                print(f"[WARNING] Parallax init failed: {e}")
                self.parallax_bg = None

            # Thêm các lớp cảnh nền - ĐIỀU CHỈNH ĐỂ HỢP LOGIC HƠN
            if self.parallax_bg:
                try:
                    print("Đang load assets Map Công Nghệ...")
                    self.parallax_bg.add_layer("tai_nguyen/hinh_anh/canh_nen/mapcongnghe/bau_troi.png",
                                             speed_factor=0.05, y_pos=0)
                    self.parallax_bg.add_layer("tai_nguyen/hinh_anh/canh_nen/mapcongnghe/toa_nha.png",
                                             speed_factor=0.3, y_pos=250)
                    self.parallax_bg.add_layer("tai_nguyen/hinh_anh/canh_nen/mapcongnghe/mat_dat.png",
                                             speed_factor=0.3, y_pos=200, repeat_x=True)
                    print("Load background Map Công Nghệ thành công!")
                except Exception as e:
                    print(f"Lỗi load background Map Công Nghệ: {e}")
                    self.parallax_bg = None

            # Player setup - dùng try/except để không crash nếu asset lỗi
            try:
                if player:
                    self.player = player
                    self.player.x = 100
                    self.player.y = 400
                    self.player.base_y = 400
                else:
                    folder_nv = os.path.join("tai_nguyen", "hinh_anh", "nhan_vat", "chien_binh")
                    controls_p1 = {
                        "left": pygame.K_LEFT,
                        "right": pygame.K_RIGHT,
                        "attack": pygame.K_a,
                        "kick": pygame.K_s,
                        "defend": pygame.K_d,
                        "jump": pygame.K_w,
                    }
                    self.player = Character(100, 400, folder_nv, controls_p1, color=(0,255,255))
                # Cập nhật damage cho môi trường công nghệ
                self.player.damage = 18
                self.player.kick_damage = 23
            except Exception as e:
                tb = traceback.format_exc()
                print("[ERROR] Player init failed:", e)
                print(tb)
                # ghi log để debug offline
                try:
                    with open(os.path.join(project_root, "map_init_player_error.log"), "w", encoding="utf-8") as f:
                        f.write(tb)
                except Exception:
                    pass
                self.initialized = False
                return

            # Khởi tạo quái vật
            folder_qv = os.path.join("tai_nguyen", "hinh_anh", "quai_vat","quai_map_cong_nghe","quai_nho")
            # Folder boss (chứa 7 tấm ảnh 0..6.png)
            folder_boss = os.path.join("tai_nguyen", "hinh_anh", "quai_vat","quai_map_cong_nghe","boss")
            sound_qv = os.path.join("tai_nguyen", "am_thanh", "hieu_ung")

            self.normal_enemies = []

            # items dropped on the ground (collected from dead enemies)
            self.items = []

            tech_colors = [
                (0, 255, 255),
                (0, 255, 0),
                (255, 0, 255),
                (255, 255, 0),
                (255, 255, 255),
                (0, 191, 255),
            ]

            # Tạo enemies nhỏ - bọc try/except riêng để tiếp tục nếu một con lỗi
            total_enemies = 0
            for group in range(3):
                group_x = 700 + group * 900
                num_enemies = random.randint(2, 3)
                for i in range(num_enemies):
                    try:
                        x_pos = group_x + random.randint(-100, 100)
                        enemy = QuaiVat(x_pos, 400, folder_qv, sound_qv, color=random.choice(tech_colors), damage=15)
                        enemy.speed = 3.0
                        enemy.home_x = x_pos
                        enemy.patrol_range = 200
                        enemy.aggro_range = 400
                        enemy.hp = int(getattr(enemy, "hp", 100) * 1.1)
                        enemy.damaged = False
                        self.normal_enemies.append(enemy)
                        total_enemies += 1
                    except Exception as e:
                        print(f"[WARNING] Lỗi tạo enemy ở group {group} idx {i}: {e}")
                        traceback.print_exc()

            # Tạo boss - bọc try/except
            try:
                self.bosses = []
                try:
                    # Tạo boss dùng đúng folder boss 7 frame - vị trí mặt đất
                    boss = Boss1(self.game.map_width - 400, 150, folder_boss, sound_qv)
                    # đảm bảo thuộc tính cơ bản tồn tại
                    if hasattr(boss, "hp"):
                        boss.hp = int(boss.hp * 2.0)
                    if hasattr(boss, "damage"):
                        boss.damage = int(boss.damage * 1.5)
                    if hasattr(boss, "speed"):
                        boss.speed = boss.speed * 0.9
                    # scale sprite nếu tồn tại
                    if hasattr(boss, "image") and boss.image:
                        try:
                            scale_factor = 1.8  # Giảm scale factor
                            orig_img = boss.image
                            ow, oh = orig_img.get_size()
                            new_w, new_h = int(ow * scale_factor), int(oh * scale_factor)
                            boss.image = pygame.transform.scale(orig_img, (new_w, new_h))
                            if hasattr(boss, "rect"):
                                boss.rect = boss.image.get_rect(topleft=(boss.x, boss.y))
                            if hasattr(boss, "width"):
                                boss.width = boss.image.get_width()
                            if hasattr(boss, "height"):
                                boss.height = boss.image.get_height()
                            # Không thay đổi vị trí y để tránh boss bay lên cao
                        except Exception as e:
                            print(f"[WARNING] Không thể scale boss image: {e}")
                    boss.damaged = False
                    boss.dead = getattr(boss, "dead", False)
                    self.bosses.append(boss)
                except Exception as e:
                    print(f"[WARNING] Boss1 creation failed: {e}")
                    traceback.print_exc()
            except Exception as e:
                print(f"Lỗi tạo boss (outer): {e}")
                self.bosses = []

            # ✨ KHỞI TẠO CÁC THUỘC TÍNH QUAN TRỌNG
            self.current_boss_index = 0
            self.current_boss = None
            self.initial_enemy_count = total_enemies
            
            # Spawn boss đầu tiên ngay lập tức để kiểm tra
            if self.bosses:
                print(f"[DEBUG] Boss created: {len(self.bosses)} bosses available")
                self.current_boss = self.bosses[0]
                self.current_boss_index = 1
                print(f"[DEBUG] Boss spawned at x={self.current_boss.x}, y={self.current_boss.y}")
            else:
                print("[WARNING] No bosses created!")

            # --- MỚI: chuẩn bị mid (quai_trung) wave ---
            # mid enemies removed by request (no mid wave will spawn)
            self.mid_enemies = []
            self.mid_spawned = False
            self.folder_quai_trung = None
            self.sound_quai_trung = None

            # Camera
            self.camera_x = 0
            self.min_x = 0
            self.max_x = max(0, self.game.map_width - self.game.WIDTH)
            self.all_enemies_defeated = False

            # Precompute fallback buildings
            self.fallback_buildings = []
            spacing = 150
            cols = (self.game.WIDTH // spacing) + 6
            base_x = -spacing * 3
            for i in range(cols):
                bx = base_x + i * spacing
                bh = random.randint(150, 300)
                self.fallback_buildings.append((bx, bh))

            # Hiệu ứng particles
            self.light_beams = []
            for i in range(10):
                beam = {
                    'x': random.randint(0, self.game.map_width),
                    'height': random.randint(50, 200),
                    'y': random.randint(100, 400),
                    'alpha': random.randint(30, 100),
                    'color': random.choice(tech_colors),
                    'flicker_speed': random.uniform(0.1, 0.3),
                    'width': random.randint(2, 6),
                    'current_alpha': random.randint(30, 100)
                }
                self.light_beams.append(beam)

            self.tech_particles = []
            for i in range(30):
                particle = {
                    'x': random.randint(0, self.game.map_width),
                    'y': random.randint(0, self.game.HEIGHT),
                    'speed_x': random.uniform(-1, 1),
                    'speed_y': random.uniform(-0.5, 0.5),
                    'size': random.randint(1, 4),
                    'color': random.choice(tech_colors),
                    'alpha': random.randint(100, 255),
                    'pulse_speed': random.uniform(0.02, 0.05),
                    'pulse_offset': random.uniform(0, 2 * math.pi),
                    'current_alpha': random.randint(100, 255)
                }
                self.tech_particles.append(particle)

        except Exception:
            tb = traceback.format_exc()
            print(tb)
            print("[ERROR] MapCongNgheScene initialization failed. Scene will be disabled (no auto-change).")
            try:
                with open(os.path.join(self._project_root, "map_init_error.log"), "w", encoding="utf-8") as f:
                    f.write(tb)
                print(f"[ERROR] Map init traceback written to: {os.path.join(self._project_root, 'map_init_error.log')}")
            except Exception:
                pass
            self.initialized = False
            return

    def handle_event(self, event):
        # Let UI handle clicks / buttons first
        try:
            if self.action_buttons.handle_event(event, player=getattr(self, 'player', None)):
                return
        except Exception:
            pass

        if not getattr(self, "initialized", True):
            print("[DEBUG] MapCongNgheScene.handle_event ignored (init failed)")
            return

        # in ra sự kiện để debug
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
            print(f"[DEBUG] MapCongNgheScene.handle_event: {event}")

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                try:
                    self.game.change_scene("menu")
                except Exception:
                    traceback.print_exc()


    def spawn_next_boss(self):
        # guard: only change scene if initialized
        if not getattr(self, "initialized", True):
            return
        if self.current_boss_index < len(self.bosses):
            self.current_boss = self.bosses[self.current_boss_index]
            self.current_boss_index += 1
        else:
            self.current_boss = None
            # only check normal_enemies now (mid removed)
            if not self.normal_enemies:
                self.all_enemies_defeated = True
                try:
                    self.game.change_scene("victory")
                except Exception:
                    traceback.print_exc()

    def spawn_mid_enemies(self):
        # Mid enemies disabled - no action.
        return

        try:
            # reset list and mark spawned after success
            self.mid_enemies = []

            # choose side and position ~1000 away from player
            side = random.choice([-1, 1])
            base_distance = 1000
            offset = random.randint(-50, 50)
            x_pos = int(self.player.x + side * (base_distance + offset))
            x_pos = max(50, min(self.game.map_width - 50, x_pos))

            # bright color (very saturated)
            bright_color = (255, 220, 50)

            enemy = QuaiVat(x_pos, 400, self.folder_quai_trung, self.sound_quai_trung,
                            color=bright_color, damage=40)

            # make it visually larger if sprite exists and align feet to ground
            try:
                # determine ground y (use player.base_y if present)
                ground_y = getattr(self.player, "base_y", getattr(self.player, "y", 400))

                if hasattr(enemy, "image") and enemy.image:
                    orig = enemy.image
                    scale_factor = 2.0  # adjust to make it much larger
                    ow, oh = orig.get_size()
                    new_w, new_h = int(ow * scale_factor), int(oh * scale_factor)
                    enemy.image = pygame.transform.scale(orig, (new_w, new_h))

                    # set enemy.y so the bottom of the sprite sits on ground_y
                    enemy.y = ground_y - enemy.image.get_height()

                    # update rect/size attributes if present and align bottom
                    if hasattr(enemy, "rect") and enemy.rect:
                        enemy.rect = enemy.image.get_rect(topleft=(enemy.x, enemy.y))
                    else:
                        # some classes use width/height
                        if hasattr(enemy, "width"):
                            enemy.width = enemy.image.get_width()
                        if hasattr(enemy, "height"):
                            enemy.height = enemy.image.get_height()

                else:
                    # if no image, fallback to aligning y value to ground
                    enemy.y = ground_y - getattr(enemy, "height", 100)

                # ensure physics flags / velocities are grounded (best-effort)
                if hasattr(enemy, "vy"):
                    enemy.vy = 0
                if hasattr(enemy, "on_ground"):
                    enemy.on_ground = True
                if hasattr(enemy, "grounded"):
                    enemy.grounded = True
                # expose base_y for AI
                enemy.base_y = ground_y

            except Exception:
                traceback.print_exc()

            # behavior / stats
            enemy.speed = 2.0
            enemy.x = x_pos
            enemy.home_x = x_pos
            enemy.aggro_range = 1000
            enemy.attack_range = 400
            enemy.patrol_range = 50
            enemy.hp = int(getattr(enemy, "hp", 100) * 2.5)
            if hasattr(enemy, "damage"):
                try:
                    enemy.damage = int(enemy.damage * 1.8)
                except Exception:
                    enemy.damage = getattr(enemy, "damage", 40)

            enemy.damaged = False

            self.mid_enemies.append(enemy)
            self.mid_spawned = True
            print(f"[DEBUG] Spawned 1 big bright mid enemy at x={x_pos}, y={getattr(enemy,'y',None)}")

        except Exception as e:
            print(f"[ERROR] spawn_mid_enemies failed: {e}")
            traceback.print_exc()

    def update(self):
        if not getattr(self, "initialized", True):
            return

        keys = pygame.key.get_pressed()

        # Cập nhật camera
        screen_center_x = self.game.WIDTH // 2
        if self.player and hasattr(self.player, "x") and self.player.x > screen_center_x and self.player.x < self.game.map_width - screen_center_x:
            self.camera_x = self.player.x - screen_center_x
        self.camera_x = max(0, min(self.camera_x, self.max_x))

        # Cập nhật hiệu ứng
        for particle in self.tech_particles:
            particle['x'] += particle['speed_x']
            particle['y'] += particle['speed_y']

            pulse_factor = math.sin(pygame.time.get_ticks() * particle['pulse_speed'] + particle['pulse_offset'])
            particle['current_alpha'] = int(particle['alpha'] + pulse_factor * 50)
            particle['current_alpha'] = max(50, min(255, particle['current_alpha']))

            if particle['x'] < -10:
                particle['x'] = self.game.map_width + 10
            elif particle['x'] > self.game.map_width + 10:
                particle['x'] = -10

            if particle['y'] < -10:
                particle['y'] = self.game.HEIGHT + 10
            elif particle['y'] > self.game.HEIGHT + 10:
                particle['y'] = -10

        for beam in self.light_beams:
            flicker = math.sin(pygame.time.get_ticks() * beam['flicker_speed'])
            beam['current_alpha'] = int(beam['alpha'] + flicker * 30)
            beam['current_alpha'] = max(10, min(150, beam['current_alpha']))

        if self.player and getattr(self.player, "hp", 0) > 0:
            try:
                self.player.update(keys)
            except Exception:
                traceback.print_exc()

            bullet_handler.update_bullets(self.player, self.normal_enemies, self.current_boss)

            if hasattr(self.player, "x"):
                if self.player.x < 0:
                    self.player.x = 0
                elif self.player.x > self.game.map_width - 50:
                    self.player.x = self.game.map_width - 50

            # update enemies
            alive_enemies = []
            for enemy in self.normal_enemies:
                try:
                    if getattr(enemy, "hp", 0) > 0:
                        enemy.update(target=self.player)
                        alive_enemies.append(enemy)
                except Exception:
                    traceback.print_exc()
            self.normal_enemies = alive_enemies

            # Spawn boss when normal enemies cleared
            if not self.normal_enemies:
                if not self.current_boss or getattr(self.current_boss, "dead", False):
                    self.spawn_next_boss()

            if self.current_boss and not getattr(self.current_boss, "dead", False):
                try:
                    self.current_boss.update(target=self.player)
                except Exception:
                    traceback.print_exc()

            # Update UI
            try:
                self.action_buttons.update()
            except Exception:
                pass

            # Pickup items: check collisions between player and items
            remaining_items = []
            for item in getattr(self, 'items', []):
                if getattr(item, 'picked', False):
                    continue
                item_rect = pygame.Rect(getattr(item, 'x', 0), getattr(item, 'y', 0), 24, 24)
                player_rect = pygame.Rect(getattr(self.player, 'x', 0), getattr(self.player, 'y', 0), 50, 80)
                if player_rect.colliderect(item_rect):
                    try:
                        item.on_pickup(self.player)
                    except Exception:
                        pass
                else:
                    remaining_items.append(item)
            self.items = remaining_items

            any_enemy_attacking = any(getattr(enemy, "attacking", False) and getattr(enemy, "state", "") in ["danh", "da"] for enemy in (self.normal_enemies + self.mid_enemies))
            if self.current_boss:
                any_enemy_attacking = any_enemy_attacking or (getattr(self.current_boss, "attacking", False) and getattr(self.current_boss, "state", "") in ["danh", "da", "nhay"])

            if not any_enemy_attacking:
                self.player.damaged = False

            # Collisions with small enemies
            for enemy in self.normal_enemies:
                if not hasattr(enemy, "image") or not hasattr(self.player, "image"):
                    continue
                try:
                    rect_player = self.player.image.get_rect(topleft=(self.player.x, self.player.y))
                    rect_enemy = enemy.image.get_rect(topleft=(enemy.x, enemy.y))
                except Exception:
                    continue

                # Use attack_hitbox when player is attacking for better close-range detection
                attacked = False
                if getattr(self.player, 'state', None) in ["danh", "da"] and getattr(self.player, 'actioning', False) and not getattr(enemy, 'damaged', False):
                    try:
                        hitbox = self.player.attack_hitbox()
                        if hitbox.colliderect(rect_enemy):
                            if hasattr(self.player, 'animations') and self.player.state in self.player.animations:
                                max_frames = len(self.player.animations[self.player.state])
                                damage_frame_threshold = max(1, int(max_frames * 0.8))
                                if getattr(self.player, "frame", 0) >= damage_frame_threshold:
                                    try:
                                        if self.player.state == "danh":
                                            enemy.take_damage(self.player.get_effective_damage(), self.player.flip, self.player)
                                        else:
                                            enemy.take_damage(self.player.kick_damage, self.player.flip, self.player)
                                        enemy.damaged = True
                                        attacked = True
                                    except Exception:
                                        traceback.print_exc()
                    except Exception:
                        # If attack_hitbox fails for any reason, fall back to rect collision
                        pass

                # Fallback: if not attacked and rects overlap (touching), allow enemy to still damage player
                if not attacked and rect_player.colliderect(rect_enemy):
                    # Enemy attack
                    if getattr(enemy, "state", "") in ["danh", "da"] and not getattr(self.player, "damaged", False):
                        if hasattr(enemy, 'animations') and enemy.state in enemy.animations:
                            max_frames = len(enemy.animations[enemy.state])
                            damage_frame_threshold = max(1, int(max_frames * 0.8))
                            if getattr(enemy, "frame", 0) >= damage_frame_threshold:
                                try:
                                    self.player.take_damage(enemy.damage, enemy.flip)
                                    self.player.damaged = True
                                except Exception:
                                    traceback.print_exc()

            # Collisions with boss (guarded)
            if self.current_boss and hasattr(self.current_boss, "image") and not getattr(self.current_boss, "dead", False):
                try:
                    rect_boss = self.current_boss.image.get_rect(topleft=(self.current_boss.x, self.current_boss.y))
                    rect_player = self.player.image.get_rect(topleft=(self.player.x, self.player.y))
                    if rect_boss.colliderect(rect_player):
                        if self.player.state == "danh" and getattr(self.player, "actioning", False) and not getattr(self.current_boss, "damaged", False):
                            if hasattr(self.player, 'animations') and self.player.state in self.player.animations:
                                max_frames = len(self.player.animations[self.player.state])
                                damage_frame_threshold = max(1, int(max_frames * 0.8))
                                if getattr(self.player, "frame", 0) >= damage_frame_threshold:
                                    try:
                                        self.current_boss.take_damage(self.player.get_effective_damage(), self.player.flip, self.player)
                                        self.current_boss.damaged = True
                                    except Exception:
                                        traceback.print_exc()
                        elif self.player.state == "da" and getattr(self.player, "actioning", False) and not getattr(self.current_boss, "damaged", False):
                            if hasattr(self.player, 'animations') and self.player.state in self.player.animations:
                                max_frames = len(self.player.animations[self.player.state])
                                damage_frame_threshold = max(1, int(max_frames * 0.8))
                                if getattr(self.player, "frame", 0) >= damage_frame_threshold:
                                    try:
                                        self.current_boss.take_damage(self.player.kick_damage, self.player.flip, self.player)
                                        self.current_boss.damaged = True
                                    except Exception:
                                        traceback.print_exc()

                        if getattr(self.current_boss, "state", "") in ["danh", "da", "nhay"] and not getattr(self.player, "damaged", False):
                            if hasattr(self.current_boss, 'animations') and self.current_boss.state in self.current_boss.animations:
                                max_frames = len(self.current_boss.animations[self.current_boss.state])
                                damage_frame_threshold = max(1, int(max_frames * 0.8))
                                if getattr(self.current_boss, "frame", 0) >= damage_frame_threshold:
                                    try:
                                        boss_damage = getattr(self.current_boss, "damage", 10)
                                        if hasattr(self.current_boss, 'get_current_damage'):
                                            boss_damage = self.current_boss.get_current_damage()
                                        self.player.take_damage(boss_damage, self.current_boss.flip)
                                        self.player.damaged = True
                                    except Exception:
                                        traceback.print_exc()
                except Exception:
                    traceback.print_exc()
        else:
            # Player chết - Game Over
            if not hasattr(self, 'death_timer'):
                self.death_timer = pygame.time.get_ticks()

            current_time = pygame.time.get_ticks()
            if current_time - self.death_timer > 2000:
                bosses_killed = len([b for b in (self.bosses or []) if getattr(b, "dead", False)]) if self.bosses else 0
                score = bosses_killed * 1500
                score += (self.initial_enemy_count - len(self.normal_enemies)) * 150

                try:
                    self.game.game_over_scene = self.game.load_scene("game_over", "Map Công Nghệ", score)
                    self.game.change_scene("game_over")
                except Exception:
                    traceback.print_exc()
                return

            try:
                self.player.update(keys)
            except Exception:
                traceback.print_exc()

            if self.current_boss:
                self.current_boss.state = "dung_yen"
                self.current_boss.attacking = False
                self.current_boss.frame = 0
            for enemy in self.normal_enemies:
                enemy.state = "dung_yen"
                enemy.attacking = False
                enemy.frame = 0

    def draw_tech_particle(self, screen, particle, camera_x):
        x = particle['x'] - camera_x
        if -10 <= x < self.game.WIDTH + 10:
            particle_surface = pygame.Surface((particle['size'] * 4, particle['size'] * 4), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, (*particle['color'], particle['current_alpha']),
                               (particle['size'] * 2, particle['size'] * 2), particle['size'])
            if particle['size'] > 2:
                pygame.draw.circle(particle_surface, (*particle['color'], particle['current_alpha']//3),
                                   (particle['size'] * 2, particle['size'] * 2), particle['size'] * 2)
            screen.blit(particle_surface, (x - particle['size'] * 2, particle['y'] - particle['size'] * 2))

    def draw_light_beam(self, screen, beam, camera_x):
        x = beam['x'] - camera_x
        if -10 <= x < self.game.WIDTH + 10:
            beam_surface = pygame.Surface((beam['width'], beam['height']), pygame.SRCALPHA)
            beam_surface.fill((*beam['color'], beam['current_alpha']))
            screen.blit(beam_surface, (x, beam['y']))

    def draw(self, screen):
        if not getattr(self, "initialized", True):
            screen.fill((0,0,0))
            try:
                font = pygame.font.SysFont(None, 36)
                text = font.render("Lỗi load Map. Quay lại menu.", True, (255, 0, 0))
                screen.blit(text, (20, 20))
            except Exception:
                pass
            return

        # Vẽ background
        if self.parallax_bg:
            try:
                self.parallax_bg.draw_background_layers(screen, self.camera_x)
            except Exception:
                traceback.print_exc()
        else:
            screen.fill((10, 10, 30))
            pygame.draw.rect(screen, (20, 20, 50), (0, 0, self.game.WIDTH, 450))
            offset_x = int((self.camera_x * 0.3) % 150)
            for bx, height in self.fallback_buildings:
                x = bx - offset_x
                if x < -200:
                    x += (len(self.fallback_buildings) * 150)
                pygame.draw.rect(screen, (40, 40, 80), (x, 450 - height, 100, height))
            pygame.draw.rect(screen, (60, 60, 100), (0, 450, self.game.WIDTH, 250))

        for beam in self.light_beams:
            self.draw_light_beam(screen, beam, self.camera_x)

        for particle in self.tech_particles:
            if particle['y'] < 450:
                self.draw_tech_particle(screen, particle, self.camera_x)

        try:
            title_color = (0, 255, 255)
            text = self.font.render("Map Công Nghệ: Thành Phố Tương Lai", True, title_color)
            screen.blit(text, (screen.get_width()//2 - text.get_width()//2, 50))
            info_color = (0, 255, 0)
            info = self.font.render("Nhấn ESC để về menu", True, info_color)
            screen.blit(info, (screen.get_width()//2 - info.get_width()//2, 120))
        except Exception:
            traceback.print_exc()

        # Vẽ enemies (normal only)
        for enemy in self.normal_enemies:
            try:
                if hasattr(enemy, "x") and enemy.x + 150 >= self.camera_x and enemy.x - 150 <= self.camera_x + self.game.WIDTH:
                    enemy.draw(screen, self.camera_x)
            except Exception:
                traceback.print_exc()

        # Vẽ boss
        if self.current_boss and not getattr(self.current_boss, "dead", False):
            try:
                # Vẽ boss luôn nếu nó tồn tại (bỏ điều kiện camera để debug)
                self.current_boss.draw(screen, self.camera_x)
                # Debug info
                # print(f"[DEBUG] Drawing boss at x={self.current_boss.x}, y={self.current_boss.y}, camera_x={self.camera_x}")
            except Exception as e:
                print(f"[ERROR] Boss draw failed: {e}")
                traceback.print_exc()

        # Vẽ player
        try:
            self.player.draw(screen, self.camera_x)
        except Exception:
            traceback.print_exc()

        # Vẽ các particle ở dưới cùng (mặt đất)
        try:
            for particle in self.tech_particles:
                if particle['y'] >= 450:
                    self.draw_tech_particle(screen, particle, self.camera_x)
        except Exception:
            traceback.print_exc()

        # Vẽ foreground của parallax nếu có
        if self.parallax_bg:
            try:
                self.parallax_bg.draw_foreground_layers(screen, self.camera_x)
            except Exception:
                traceback.print_exc()

        # Vẽ thanh máu hoặc UI liên quan đến player nếu game cung cấp
        if hasattr(self.game, 'draw_player_health_bar'):
            try:
                self.game.draw_player_health_bar(screen, self.player)
            except Exception:
                traceback.print_exc()

        # Draw Action Buttons HUD on top (match Map Mùa Thu)
        try:
            self.action_buttons.draw(screen, player=self.player)
        except Exception:
            pass

        # Vẽ đạn (bullet)
        if self.player:
            bullet_handler.draw_bullets(self.player, screen, self.camera_x)
