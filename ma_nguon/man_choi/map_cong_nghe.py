import pygame
import os
import random
import math
import traceback

from ma_nguon.doi_tuong.nhan_vat.nhan_vat import Character
from ma_nguon.doi_tuong.quai_vat.quai_vat import QuaiVat
from ma_nguon.doi_tuong.quai_vat.quai_nho_type1 import QuaiNhoType1
from ma_nguon.doi_tuong.quai_vat.quai_vat_manh import Boss1, Boss2, Boss3
from ma_nguon.tien_ich.parallax import ParallaxBackground
from ma_nguon.giao_dien.action_buttons import ActionButtonsUI
from ma_nguon.tien_ich import bullet_handler
from ma_nguon.tien_ich.equipment_loader import load_and_apply_equipment

from ma_nguon.man_choi.skill_video import SkillVideoPlayer
from ma_nguon.man_choi.base_map_scene import BaseMapScene
from ma_nguon.core import high_scores


class MapCongNgheScene(BaseMapScene):
    def __init__(self, game, player=None):
        super().__init__()  # Initialize BaseMapScene
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
                # Gán tham chiếu scene cho player để quái có thể drop item qua attacker.scene
                try:
                    self.player.scene = self
                except Exception:
                    pass
                
                # Load và apply equipment stats
                load_and_apply_equipment(self.player, self.game, "MAP_CONG_NGHE")
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
            
            # Skill video system
            self.skill_video = None
            self.showing_skill_video = False

            tech_colors = [
                (0, 255, 255),
                (0, 255, 0),
                (255, 0, 255),
                (255, 255, 0),
                (255, 255, 255),
                (0, 191, 255),
            ]

            # Tạo enemies nhỏ - bọc try/except riêng để tiếp tục nếu một con lỗi
            # Mix 2 loại quái: QuaiVat (không có số) và QuaiNhoType1 (có số 1)
            # Tổng cộng 30 con quái: 15 con mỗi loại, phân bố đều
            total_enemies = 0
            num_type1 = 0  # Đếm số quái type 1
            num_type2 = 0  # Đếm số quái type 2
            target_per_type = 15  # Mỗi loại 15 con
            
            # Tạo 6 groups, mỗi group có 5 quái (tổng 30 quái)
            for group in range(6):
                group_x = 700 + group * 700  # Giảm khoảng cách giữa các nhóm
                num_enemies_in_group = 5
                
                for i in range(num_enemies_in_group):
                    try:
                        x_pos = group_x + random.randint(-150, 150)
                        # Tạo độ cao khác nhau để tránh chồng lên nhau
                        # Quái type 1 (không số) bay cao hơn (y=320-360)
                        # Quái type 2 (có số 1) ở mặt đất (y=400)
                        
                        # Spawn luân phiên giữa 2 loại để đảm bảo số lượng bằng nhau
                        if num_type1 < target_per_type and (num_type2 >= target_per_type or (total_enemies % 2 == 0)):
                            # Quái loại 1 (không có số) - bay cao hơn - CÓ BẮN ĐẠN
                            y_pos = random.randint(320, 360)  # Cao hơn một chút
                            enemy = QuaiVat(x_pos, y_pos, folder_qv, sound_qv, color=random.choice(tech_colors), damage=15)
                            enemy.speed = 3.0
                            enemy.hp = 150  # HP = 150
                            enemy.base_y = y_pos  # Lưu vị trí y gốc
                            enemy.can_shoot = True  # BẬT khả năng bắn đạn
                            enemy.bullet_damage = 2  # Mỗi viên đạn gây 2 damage
                            num_type1 += 1
                        else:
                            # Quái loại 2 (có số 1: chay1, danh1, etc.) - ở mặt đất
                            y_pos = 400
                            enemy = QuaiNhoType1(x_pos, y_pos, folder_qv, sound_qv, color=random.choice(tech_colors), damage=14)
                            enemy.speed = 3.2
                            enemy.hp = 150  # HP = 150
                            enemy.max_hp = 150  # Cập nhật max HP để thanh máu hiển thị đúng
                            enemy.base_y = y_pos  # Lưu vị trí y gốc
                            num_type2 += 1
                        
                        enemy.home_x = x_pos
                        enemy.patrol_range = 200
                        enemy.aggro_range = 400
                        enemy.damaged = False
                        self.normal_enemies.append(enemy)
                        total_enemies += 1
                    except Exception as e:
                        print(f"[WARNING] Lỗi tạo enemy ở group {group} idx {i}: {e}")
                        traceback.print_exc()
            
            print(f"[MAP_CONG_NGHE] Đã tạo {total_enemies} quái vật: {num_type1} QuaiVat + {num_type2} QuaiNhoType1")

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
            self.current_boss = None  # Boss chưa spawn
            self.initial_enemy_count = total_enemies
            
            # KHÔNG spawn boss ngay - chờ tiêu diệt hết 30 con quái nhỏ
            if self.bosses:
                print(f"[DEBUG] Boss created: {len(self.bosses)} bosses available - waiting for all enemies defeated")
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
                self.game.change_scene("menu")
                
        # Universal skill handling
        if self.handle_universal_skill_input(event):
            return  # Skill was handled
    
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
                    if hasattr(self, 'spawn_next_boss') and not hasattr(self, 'victory_triggered'):
                        self.spawn_next_boss()
        
        print(f"[SKILL] Damaged {damage_count} enemies!")
        
    def spawn_next_boss(self):
        """Spawn boss tiếp theo - chỉ gọi sau khi tiêu diệt hết quái nhỏ"""
        if hasattr(self, 'current_boss_index') and hasattr(self, 'bosses'):
            if self.current_boss_index < len(self.bosses):
                self.current_boss = self.bosses[self.current_boss_index]
                self.current_boss_index += 1
                print(f"[BOSS] ✨ Boss #{self.current_boss_index} spawned! (Đã tiêu diệt hết {self.initial_enemy_count} quái nhỏ)")
            else:
                self.current_boss = None
                print("[BOSS] All bosses defeated")
                # Check if all enemies are defeated to change scene
                if not self.normal_enemies and not hasattr(self, 'victory_triggered'):
                    print("[VICTORY] All enemies defeated!")
                    # Mark victory and reward player + update leaderboard
                    self.victory_triggered = True
                    try:
                        # Compute score similar to game over logic
                        bosses_killed = len([b for b in (self.bosses or []) if getattr(b, "dead", False)]) if self.bosses else 0
                        score = bosses_killed * 1500
                        score += (self.initial_enemy_count - len(self.normal_enemies)) * 150

                        # Add to leaderboard (non-fatal)
                        try:
                            user = getattr(self.game, 'current_user', None) or 'Guest'
                            key = "map_cong_nghe"
                            high_scores.add_score(key, user, int(score))
                        except Exception as e:
                            print(f"[WARN] Could not update high scores: {e}")

                        # Reward gold to player (will be committed by Game.change_scene via commit_session_gold)
                        gold_reward = max(50, int(score / 10))
                        try:
                            if hasattr(self, 'player') and self.player:
                                if hasattr(self.player, 'gold'):
                                    self.player.gold += gold_reward
                                else:
                                    self.player.gold = gold_reward
                                print(f"[REWARD] Awarded {gold_reward} gold to player (session).")
                        except Exception:
                            pass
                    except Exception:
                        traceback.print_exc()

                    # Finally change to victory scene (Game.change_scene will commit session gold)
                    self.game.change_scene("victory")
        else:
            print("[ERROR] Boss system not properly initialized")

    def update(self):
        # Update skill video if showing
        # Universal skill system update
        if self.update_universal_skills():
            return  # Pause game if skill video is playing  # Pause game logic while showing skill video
        
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
                    else:
                        # Thu thập vật phẩm rơi ra (nếu có) từ enemy.spawned_drops
                        try:
                            if hasattr(enemy, 'spawned_drops') and enemy.spawned_drops and not getattr(enemy, 'drops_collected', False):
                                if not hasattr(self, 'items'):
                                    self.items = []
                                self.items.extend(enemy.spawned_drops)
                                enemy.drops_collected = True
                        except Exception:
                            traceback.print_exc()
                except Exception:
                    traceback.print_exc()
            self.normal_enemies = alive_enemies

            # Spawn boss when normal enemies cleared
            if not self.normal_enemies and not hasattr(self, 'victory_triggered'):
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
                
                # Check collision with enemy bullets
                if hasattr(enemy, 'bullets') and enemy.bullets:
                    bullets_to_keep = []
                    for bullet in enemy.bullets:
                        # Create bullet rect
                        bullet_rect = pygame.Rect(int(bullet['x']) - 5, int(bullet['y']) - 5, 10, 10)
                        
                        # Check collision with player
                        if rect_player.colliderect(bullet_rect):
                            # Đạn trúng player - LUÔN gây damage (bỏ qua defense)
                            try:
                                # Trừ HP trực tiếp, bỏ qua defense (đạn xuyên giáp)
                                self.player.hp -= bullet['damage']
                                if self.player.sound_hit:
                                    self.player.sound_hit.play()
                                # Không giữ đạn này (đã va chạm)
                            except Exception:
                                traceback.print_exc()
                        else:
                            # Giữ đạn nếu chưa va chạm
                            bullets_to_keep.append(bullet)
                    
                    enemy.bullets = bullets_to_keep

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

    def get_all_enemies(self):
        """Lấy tất cả enemies để truyền cho skill system"""
        all_enemies = []
        if hasattr(self, 'normal_enemies'):
            all_enemies.extend(self.normal_enemies)
        if hasattr(self, 'current_boss') and self.current_boss:
            all_enemies.append(self.current_boss)
        return all_enemies

    def draw(self, screen):
        # If showing skill video, render it first
        if self.showing_skill_video and self.skill_video:
            screen.fill((0, 0, 0))  # Black background
            self.skill_video.draw(screen)
            return  # Don't draw game elements during skill video
        
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

        # Vẽ vật phẩm rơi ra (vàng, bình máu/mana, ...)
        try:
            for item in getattr(self, 'items', []):
                if hasattr(item, 'draw'):
                    item.draw(screen, self.camera_x)
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

        # Vẽ đạn của người chơi (vẽ sau foreground để luôn nhìn thấy)
        try:
            bullet_handler.draw_bullets(self.player, screen, self.camera_x)
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
            # Draw skill UI if player is Chiến Thần Lạc Hồng
            if "chien_than_lac_hong" in self.player.folder:
                self.draw_universal_skill_ui(screen)
        except Exception:
            pass

    
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
        title_text = font_title.render("THẦN NỘ", True, (255, 215, 0))
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

    # Việc vẽ đạn được thực hiện trực tiếp trong draw() nên không cần vẽ ở đây nữa

