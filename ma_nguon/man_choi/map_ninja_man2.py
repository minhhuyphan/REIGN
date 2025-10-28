import pygame
import os
import random
import math

from ma_nguon.doi_tuong.nhan_vat.nhan_vat import Character
from ma_nguon.doi_tuong.quai_vat.quai_vat import QuaiVat
from ma_nguon.doi_tuong.quai_vat.quai_vat_manh import Boss1, Boss2
from ma_nguon.tien_ich.parallax import ParallaxBackground
from ma_nguon.giao_dien.action_buttons import ActionButtonsUI
from ma_nguon.man_choi.skill_video import SkillVideoPlayer, HAS_CV2


class mapninjaman2Scene:
    def __init__(self, game, player=None):
        self.game = game
        # Debug flag to print alignment info
        self.DEBUG_ALIGN = True
        # Fine-tune vertical alignment: positive value moves enemies DOWN (towards bottom of screen)
        # Set to 0 by default — you can increase if enemies still float above ground.
        self.enemy_vertical_offset = 0

        # Helper: find bottommost non-transparent pixel row index in a Surface
        def _bottom_visible_row(surf):
            try:
                w, h = surf.get_size()
            except Exception:
                return None
            for row in range(h - 1, -1, -1):
                for x in range(w):
                    try:
                        if surf.get_at((x, row))[3] != 0:
                            return row
                    except Exception:
                        continue
            return None

        self._bottom_visible_row = _bottom_visible_row
        self.font = pygame.font.Font("Tai_nguyen/font/Fz-Donsky.ttf", 50)
        self.counter = 0

        # Skill / boss video system - SIMPLIFIED like map1
        self.skill_video = None
        self.showing_skill_video = False
        # Final boss video flag
        self.final_boss_video_played = False

        # On-screen action buttons UI
        self.action_buttons = ActionButtonsUI(self.game.WIDTH, self.game.HEIGHT)
        
        # Khởi tạo hệ thống parallax background - Ninja Màn 2 (2 layers cải tiến)
        self.parallax_bg = ParallaxBackground(self.game.WIDTH, self.game.HEIGHT, self.game.map_width)
        # 2 LỚP ẢNH ĐƯỢC ĐIỀU CHỈNH ĐỂ KHÔNG BỊ CẮT
        # Lớp 1: Background xa - kéo dài tới khung kết thúc
        self.parallax_bg.add_layer( "Tai_nguyen/hinh_anh/canh_nen/mapninja/man2/may.png",speed_factor=0.2,y_pos=-30,scale_factor=1.3,repeat_x=True)
        # Lớp 2: Background gần - cũng kéo dài tới cuối
        self.parallax_bg.add_layer("Tai_nguyen/hinh_anh/canh_nen/mapninja/man2/1.png",speed_factor=0.3,y_pos=0,scale_factor=1.3,repeat_x=True)
        # Kiểm tra và sử dụng player truyền vào hoặc tạo mới
        if player:
            self.player = player
            # Đặt lại vị trí và hồi đầy máu cho màn mới
            self.player.x = 100
            self.player.y = 300
            self.player.base_y = 300
            self.player.hp = self.player.max_hp  # Hồi đầy máu
        else:
            # Code tạo player mới - Ninja theme
            folder_nv = os.path.join("Tai_nguyen", "hinh_anh", "nhan_vat",)
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

        # --- Compute a consistent ground baseline using the player's visible bottom ---
        try:
            p_vis = self._bottom_visible_row(self.player.image)
            if p_vis is None:
                p_vis = self.player.image.get_height() - 1
            # ground_y is the screen Y coordinate where visible bottoms should sit
            self.ground_y = self.player.y + p_vis
            # Re-anchor player so their visible bottom matches ground_y exactly
            self.player.y = self.ground_y - p_vis
            self.player.base_y = self.player.y
            if self.DEBUG_ALIGN:
                print(f"[ALIGN] ground_y computed from player: ground_y={self.ground_y}, player_vis_row={p_vis}, player.y set to {self.player.y}")
        except Exception:
            # Fallback to previous baseline
            self.ground_y = 300 + (self.player.image.get_height() if getattr(self.player, 'image', None) else 150)
    
        # MÀN 2: TRUNG BÌNH - NHIỀU QUÁI NINJA HỠN
        folder_qv = os.path.join("Tai_nguyen", "hinh_anh", "quai_vat", "quai_vat_ninja","quai_thuong")
        sound_qv = os.path.join("Tai_nguyen", "am_thanh", "hieu_ung")

        self.normal_enemies = []

        # Items dropped on the ground (collected from dead enemies)
        self.items = []
        
        # Tạo 4 nhóm quái vật - nhiều hơn màn 1
        total_enemies = 0
        for group in range(4):
            group_x = 600 + group * 900  # Các nhóm gần nhau hơn
            
            # Mỗi nhóm có 2-3 quái vật
            num_enemies = random.randint(2, 3)
            total_enemies += num_enemies
            for i in range(num_enemies):
                x_pos = group_x + random.randint(-120, 120)
                # Tougher enemy for map2
                enemy = QuaiVat(x_pos, 300, folder_qv, sound_qv, color=(255, 140, 0), damage=14)
                # Align enemy vertical position to player's baseline so feet match
                try:
                    # Better align enemy bottom to current player's bottom using current player.y
                    player_h = self.player.image.get_height() if getattr(self.player, 'image', None) else 150
                    enemy_h = enemy.image.get_height() if getattr(enemy, 'image', None) else enemy.target_size[1]
                    player_bottom = self.player.y + player_h
                    enemy.y = player_bottom - enemy_h + self.enemy_vertical_offset
                    enemy.base_y = enemy.y
                    if getattr(self, 'DEBUG_ALIGN', False):
                        print(f"[ALIGN] Enemy created at x={x_pos}: player.y={self.player.y}, player_h={player_h}, enemy_h={enemy_h}, set enemy.y={enemy.y}")
                except Exception:
                    enemy.y = 300
                    enemy.base_y = enemy.y
                # Thiết lập vùng hoạt động trung bình
                enemy.speed = 2.8
                enemy.home_x = x_pos
                enemy.patrol_range = 200
                enemy.aggro_range = 300
                enemy.hp = int(enemy.hp * 1.2)  # Buff HP cho map2
                enemy.damage = int(enemy.damage * 1.2)
                self.normal_enemies.append(enemy)

        # 2 boss trung bình, mạnh hơn map1
        self.bosses = [
            Boss1(self.game.map_width - 700, 300, folder_qv, sound_qv),
            Boss2(self.game.map_width - 350, 300, folder_qv, sound_qv),
        ]

        # Buff các boss cho map2
        for boss in self.bosses:
            boss.hp = int(boss.hp * 1.4)
            boss.damage = int(boss.damage * 1.3)
            boss.speed = boss.speed * 1.1
            # Align boss bottom to current player's bottom
            try:
                player_h = self.player.image.get_height() if getattr(self.player, 'image', None) else 150
                boss_h = boss.image.get_height() if getattr(boss, 'image', None) else getattr(boss, 'target_size', [150,150])[1]
                player_bottom = self.player.y + player_h
                boss.y = player_bottom - boss_h
                boss.base_y = boss.y
            except Exception:
                pass
            
        self.current_boss_index = 0
        self.current_boss = None
        # Auto intro control: play a short intro video when entering the scene
        # without automatically spawning the boss (spawn_on_finish=False)
        self._auto_intro_started = False

        # --- Recompute a single consistent ground baseline anchored to the first enemy/boss ---
        try:
            anchor = None
            if self.normal_enemies:
                anchor = self.normal_enemies[0]
            elif self.bosses:
                anchor = self.bosses[0]

            if anchor is not None:
                a_vis = self._bottom_visible_row(anchor.image) if getattr(anchor, 'image', None) else None
                if a_vis is None:
                    a_vis = (anchor.image.get_height() if getattr(anchor, 'image', None) else getattr(anchor, 'target_size', [150,150])[1]) - 1
                # ground_y is the screen Y coordinate where visible bottoms should sit
                self.ground_y = anchor.y + a_vis

                # Re-anchor player and all enemies/bosses to this ground_y
                try:
                    p_vis = self._bottom_visible_row(self.player.image)
                    if p_vis is None:
                        p_vis = self.player.image.get_height() - 1
                    self.player.y = self.ground_y - p_vis
                    self.player.base_y = self.player.y
                except Exception:
                    pass

                # Align normal enemies
                for enemy in self.normal_enemies:
                    try:
                        e_vis = self._bottom_visible_row(enemy.image)
                        if e_vis is None:
                            e_vis = enemy.image.get_height() - 1
                        enemy.y = self.ground_y - e_vis + self.enemy_vertical_offset
                        enemy.base_y = enemy.y
                    except Exception:
                        pass

                # Align bosses
                for boss in self.bosses:
                    try:
                        b_vis = self._bottom_visible_row(boss.image)
                        if b_vis is None:
                            b_vis = boss.image.get_height() - 1
                        boss.y = self.ground_y - b_vis + self.enemy_vertical_offset
                        boss.base_y = boss.y
                    except Exception:
                        pass

                if self.DEBUG_ALIGN:
                    print(f"[ALIGN] Anchor chosen: {type(anchor).__name__} at y={anchor.y}, anchor_vis={a_vis}, ground_y={self.ground_y}")
        except Exception:
            # keep previous ground_y if any
            pass
        
        # Lưu số quái ban đầu để tính điểm
        self.initial_enemy_count = total_enemies
        
        # Camera và giới hạn map
        self.camera_x = 0
        self.min_x = 0  # Giới hạn trái của map
        # Đặt giới hạn camera với margin an toàn để tránh cắt background
        safe_margin = 100
        self.max_x = self.game.map_width - self.game.WIDTH - safe_margin
        
        # Biến đếm đã tiêu diệt tất cả kẻ địch
        self.all_enemies_defeated = False
        
        # Hiệu ứng lá rơi mùa thu trung bình (125 lá)
        self.falling_leaves = []
        leaf_colors = [
            (255, 215, 0),   # Vàng gold
            (255, 140, 0),   # Cam đậm
            (255, 69, 0),    # Đỏ cam
            (255, 165, 0),   # Cam
            (218, 165, 32),  # Vàng đậm
        ]
        
        # Trung bình lá cho màn 2
        for i in range(125):
            self.falling_leaves.append({
                'x': random.randint(0, self.game.map_width),
                'y': random.randint(-100, self.game.HEIGHT),
                'speed': random.uniform(1.5, 3.5),  # Tốc độ trung bình
                'swing': random.uniform(0.5, 2.0),  # Dao động trung bình
                'swing_offset': random.uniform(0, 2 * math.pi),
                'size': random.randint(3, 7),  # Kích thước trung bình
                'color': random.choice(leaf_colors),
                'rotation': random.uniform(0, 360),
                'rotation_speed': random.uniform(-2, 2)  # Xoay trung bình
            })

        # Auto intro will be started on the first update() call. Starting it in
        # __init__ may happen before the display/context is ready on some systems.
        # We set `_auto_intro_started` above and will trigger the intro in update().
        # DISABLED: No auto intro video for regular bosses - only final boss gets video
        self._auto_intro_started = True  # Skip auto intro

    def handle_event(self, event):
        # Let UI handle clicks first
        if self.action_buttons.handle_event(event, player=self.player):
            return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.change_scene("menu")
            elif event.key == pygame.K_b:
                # Debug: force play FINAL boss intro now (removed regular boss debug)
                if not hasattr(self, 'final_boss_spawned'):
                    print("🎬 [DEBUG] B pressed - forcing FINAL boss video start")
                    self.final_boss_spawned = True
                    self.start_final_boss_sequence()
                else:
                    print("🎬 [DEBUG] Final boss already spawned!")
            elif event.key == pygame.K_v:
                # Test: Trigger final boss video ngay lập tức  
                print("🎬 [TEST] V pressed - FORCING FINAL BOSS VIDEO NOW!")
                if not hasattr(self, 'final_boss_triggered'):
                    self.final_boss_triggered = True
                    self.start_final_boss_sequence()
                else:
                    print("🎬 [TEST] Final boss already triggered!")
                if not hasattr(self, 'final_boss_triggered'):
                    self.final_boss_triggered = True
                    print("🎬 [DEBUG] Force triggering final boss sequence")
                    self.start_final_boss_sequence()


    def spawn_next_boss(self):
        if self.current_boss_index < len(self.bosses):
            boss = self.bosses[self.current_boss_index]
            self.current_boss = boss
            self.current_boss_index += 1
            # Place boss at center of screen (camera_x + half width) and align to ground
            try:
                # center horizontally in current camera view
                boss.x = int(self.camera_x + self.game.WIDTH // 2)
                b_vis = self._bottom_visible_row(boss.image) if getattr(boss, 'image', None) else None
                if b_vis is None:
                    b_vis = (boss.image.get_height() if getattr(boss, 'image', None) else getattr(boss, 'target_size', [150,150])[1]) - 1
                boss.y = self.ground_y - b_vis + self.enemy_vertical_offset
                boss.base_y = boss.y
            except Exception:
                pass
            print(f"[BOSS] Regular boss {self.current_boss_index} spawned")
        else:
            self.current_boss = None
            # Kiểm tra xem đã tiêu diệt tất cả kẻ địch chưa
            if not self.normal_enemies:
                # PHÁT VIDEO FINAL BOSS như màn 1 phát skill video
                if not self.final_boss_video_played:
                    self.play_final_boss_video()
                else:
                    # Victory - chuyển màn
                    self.game.change_scene("victory")

    def play_final_boss_video(self):
        """Phát video final boss như màn 1 phát skill video"""
        print("🎬 [FINAL BOSS] Playing final boss video...")
        video_path = "Tai_nguyen/video/boss_cuuvi.mp4"
        
        try:
            self.skill_video = SkillVideoPlayer(video_path, self.on_final_boss_video_finish)
            self.showing_skill_video = True
            self.final_boss_video_played = True
            print("🎬 [FINAL BOSS] Video started successfully!")
        except Exception as e:
            print(f"❌ [FINAL BOSS] Video failed: {e}")
            # Fallback: spawn final boss ngay
            self.on_final_boss_video_finish()
    
    def on_final_boss_video_finish(self):
        """Callback khi video final boss kết thúc - spawn final boss"""
        print("🎬 [FINAL BOSS] Video finished! Spawning final boss...")
        self.showing_skill_video = False
        self.skill_video = None
        
        # Attempt to transform an existing small normal enemy into the final boss
        from ma_nguon.doi_tuong.quai_vat.quai_vat_manh import Boss2
        folder_qv = os.path.join("Tai_nguyen", "hinh_anh", "quai_vat", "quai_vat_ninja","boss")
        sound_qv = os.path.join("Tai_nguyen", "am_thanh", "hieu_ung")

        transformed = False
        try:
            # Prefer transforming a remaining normal enemy into the final boss
            if self.normal_enemies:
                # Pick a random surviving small enemy to transform
                idx = random.randrange(len(self.normal_enemies))
                src = self.normal_enemies.pop(idx)
                fb_x = getattr(src, 'x', None) or int(self.camera_x + self.game.WIDTH // 2)
                fb_y = getattr(src, 'y', None) or 300
                final_boss = Boss2(fb_x, fb_y, folder_qv, sound_qv)
                transformed = True
                print(f"[FINAL BOSS] Transformed normal enemy at x={fb_x} into final boss")

        except Exception:
            transformed = False

        if not transformed:
            # Spawn final boss centered on screen rather than at map edge
            final_boss = Boss2(self.game.map_width - 400, 300, folder_qv, sound_qv)
            try:
                final_boss.x = int(self.camera_x + self.game.WIDTH // 2)
            except Exception:
                # fallback to default placement if camera not ready
                final_boss.x = self.game.map_width - 400

        # Buff final boss stats regardless of spawn method
        try:
            final_boss.hp = int(final_boss.hp * 1.5)  # Mạnh hơn
            final_boss.max_hp = final_boss.hp
            final_boss.damage = int(final_boss.damage * 1.3)
        except Exception:
            pass

        # Align với ground
        try:
            b_vis = self._bottom_visible_row(final_boss.image) if getattr(final_boss, 'image', None) else None
            if b_vis is None:
                b_vis = (final_boss.image.get_height() if getattr(final_boss, 'image', None) else getattr(final_boss, 'target_size', [150,150])[1]) - 1
            final_boss.y = self.ground_y - b_vis + self.enemy_vertical_offset
            final_boss.base_y = final_boss.y
        except Exception:
            final_boss.y = 300
            final_boss.base_y = 300

        # Name and register final boss
        if hasattr(final_boss, 'name'):
            final_boss.name = "Cửu Vĩ Hồ Ly"

        self.current_boss = final_boss
        print(f"🔥 [FINAL BOSS] 'Cửu Vĩ Hồ Ly' spawned! HP: {getattr(final_boss,'hp',None)}")

    def start_final_boss_sequence(self):
        """Bắt đầu sequence cuối màn: phát video boss_cuuvi và spawn final boss"""
        print("🎬 [FINAL BOSS] Starting end-of-level boss sequence...")
        print(f"🎬 [FINAL BOSS] Current state: normal_enemies={len(self.normal_enemies)}, current_boss_index={self.current_boss_index}, bosses_total={len(self.bosses)}")
        
        # Tạo final boss mạnh hơn các boss thường
        from ma_nguon.doi_tuong.quai_vat.quai_vat_manh import Boss2
        folder_qv = os.path.join("Tai_nguyen", "hinh_anh", "quai_vat", "quai_vat_ninja","boss")
        sound_qv = os.path.join("Tai_nguyen", "am_thanh", "hieu_ung")
        
        # Tạo final boss tại vị trí cuối map
        final_boss = Boss2(self.game.map_width - 400, 300, folder_qv, sound_qv)
        
        # Tăng stats cho final boss (boss cuối mạnh hơn)
        final_boss.hp = int(final_boss.hp * 1.8)  # Máu x1.8
        final_boss.max_hp = final_boss.hp
        final_boss.damage = int(final_boss.damage * 1.5)  # Damage x1.5
        final_boss.speed = final_boss.speed * 1.3  # Tốc độ x1.3
        
        # Đặt tên đặc biệt cho final boss
        if hasattr(final_boss, 'name'):
            final_boss.name = "Cửu Vĩ Hồ Ly"
        
        # Align final boss với ground
        try:
            b_vis = self._bottom_visible_row(final_boss.image) if getattr(final_boss, 'image', None) else None
            if b_vis is None:
                b_vis = (final_boss.image.get_height() if getattr(final_boss, 'image', None) else getattr(final_boss, 'target_size', [150,150])[1]) - 1
            final_boss.y = self.ground_y - b_vis + self.enemy_vertical_offset
            final_boss.base_y = final_boss.y
        except Exception:
            final_boss.y = 300
            final_boss.base_y = 300
        
        print(f"[FINAL BOSS] Created final boss 'Cửu Vĩ Hồ Ly' with HP: {final_boss.hp}, Damage: {final_boss.damage}")
        
        # Phát video boss_cuuvi với callback spawn final boss
        def on_final_video_finish():
            print("🎉 [FINAL BOSS] Video finished - spawning final boss!")
            # Prefer transforming an existing small enemy into the final boss
            transformed_inner = False
            try:
                if self.normal_enemies:
                    idx = random.randrange(len(self.normal_enemies))
                    src = self.normal_enemies.pop(idx)
                    final_boss.x = getattr(src, 'x', final_boss.x)
                    final_boss.y = getattr(src, 'y', final_boss.y)
                    transformed_inner = True
                    print(f"[FINAL BOSS] Inner-transform used enemy at x={final_boss.x}")
            except Exception:
                transformed_inner = False

            # Place final boss in center if no transform happened
            if not transformed_inner:
                try:
                    final_boss.x = int(self.camera_x + self.game.WIDTH // 2)
                except Exception:
                    pass

            self.current_boss = final_boss
            self.pending_boss = None
            self.showing_skill_video = False
            self.skill_video = None
            print(f"🔥 [FINAL BOSS] Boss spawned with HP: {final_boss.hp}")
            
        # Sử dụng video boss_cuuvi cho final boss
        try:
                # Prefer a map-specific intro video if available, otherwise use generic boss_cuuvi
                candidate1 = os.path.join("Tai_nguyen", "video", "boss_ninja2_intro.mp4")
                candidate2 = os.path.join("Tai_nguyen", "video", "boss_cuuvi.mp4")
                video_path = candidate1 if os.path.exists(candidate1) else candidate2

                print(f"🎬 [FINAL BOSS] Selected video path: {video_path}")
                print(f"🎬 [FINAL BOSS] Video exists: {os.path.exists(video_path)}")
                print(f"🎬 [FINAL BOSS] HAS_CV2: {HAS_CV2}")

                # If cv2 not available, use splash fallback and timer
                if not HAS_CV2 or not os.path.exists(video_path):
                    print("🎬 [FINAL BOSS] Using splash fallback for final boss intro")
                    self.showing_skill_video = True
                    self.skill_video = None
                    self.pending_boss = final_boss
                    self._boss_video_timer_start = pygame.time.get_ticks()
                    self._boss_video_timer_duration = 4000  # 4 seconds splash
                    return

                # Create video player and set callback
                self.pending_boss = final_boss
                self.skill_video = SkillVideoPlayer(video_path, on_final_video_finish)
                self.showing_skill_video = bool(self.skill_video and not getattr(self.skill_video, 'finished', False))

                print(f"🎬 [FINAL BOSS] Video player created: {self.skill_video is not None}")
                print(f"🎬 [FINAL BOSS] Showing video: {self.showing_skill_video}")

                if not self.showing_skill_video:
                    # Video couldn't start -> spawn immediately
                    print("🎬 [FINAL BOSS] Video failed to start - spawning boss directly")
                    on_final_video_finish()
                
        except Exception as e:
            print(f"🎬 [FINAL BOSS] Error starting video: {e}")
            import traceback
            traceback.print_exc()
            # Fallback: spawn final boss ngay
            print("🎬 [FINAL BOSS] Fallback - spawning boss directly")
            self.current_boss = final_boss
            self.pending_boss = None

    def start_boss_video(self, boss, spawn_on_finish=True):
        """Start the boss intro video.

        If spawn_on_finish is True, the boss will be placed into the scene after the
        video/splash completes. If False, the intro plays as decoration and the
        boss is NOT spawned automatically.
        """
        try:
            video_path = os.path.join("Tai_nguyen", "video", "boss_cuuvi.mp4")
            video_exists = os.path.exists(video_path)
            print(f"[BOSS VIDEO] start: path={video_path}, exists={video_exists}, HAS_CV2={HAS_CV2}")
            def _on_boss_video_finish():
                print("[BOSS VIDEO] finished")
                try:
                    if spawn_on_finish and getattr(self, 'pending_boss', None):
                        self.current_boss = self.pending_boss
                        try:
                            b_vis = self._bottom_visible_row(self.current_boss.image) if getattr(self.current_boss, 'image', None) else None
                            if b_vis is None:
                                b_vis = (self.current_boss.image.get_height() if getattr(self.current_boss, 'image', None) else getattr(self.current_boss, 'target_size', [150,150])[1]) - 1
                            self.current_boss.y = self.ground_y - b_vis + self.enemy_vertical_offset
                            self.current_boss.base_y = self.current_boss.y
                        except Exception:
                            pass
                        self.pending_boss = None
                except Exception as e:
                    print(f"[BOSS VIDEO] spawn callback error: {e}")
                finally:
                    # Always clear video state even if we didn't spawn
                    self.showing_skill_video = False
                    self.skill_video = None

            # If cv2 is unavailable, use a timed splash fallback
            if not HAS_CV2:
                print("[BOSS VIDEO] cv2 not available - using splash fallback")
                self.showing_skill_video = True
                self.skill_video = None
                # Only set pending_boss if we intend to spawn on finish
                if spawn_on_finish:
                    self.pending_boss = boss
                else:
                    # Ensure no pending boss so the timer will just clear the splash
                    self.pending_boss = None
                self._boss_video_timer_start = pygame.time.get_ticks()
                return

            # For actual video playback, let SkillVideoPlayer call the finish callback
            # and decide whether to spawn based on spawn_on_finish flag.
            if spawn_on_finish:
                # when spawning on finish, ensure pending_boss is set
                self.pending_boss = boss
            else:
                # do not set pending_boss: this is just an intro
                self.pending_boss = None

            self.skill_video = SkillVideoPlayer(video_path, _on_boss_video_finish)
            self.showing_skill_video = bool(self.skill_video and not getattr(self.skill_video, 'finished', False))
            if self.DEBUG_ALIGN:
                print(f"[BOSS VIDEO] start: playing={self.showing_skill_video}")

            if not self.showing_skill_video:
                # video not playable -> spawn immediately
                _on_boss_video_finish()
        except Exception as e:
            print(f"[WARNING] Could not start boss video: {e}")
            # fallback: spawn immediately
            try:
                self.current_boss = boss
                self.pending_boss = None
            except Exception:
                pass


    def update(self):
        """Cập nhật trạng thái màn chơi ninja man 2"""
        # If final boss video is playing (like skill video in map1)
        if self.showing_skill_video and self.skill_video:
            self.skill_video.update()
            return  # Pause game logic while video plays

        # If we're using the splash/timer fallback for boss intro video,
        # spawn the pending boss once the timer elapses.
        if self.showing_skill_video and not self.skill_video and getattr(self, 'pending_boss', None):
            start = getattr(self, '_boss_video_timer_start', None)
            dur = getattr(self, '_boss_video_timer_duration', 0)
            if start and pygame.time.get_ticks() - start >= dur:
                try:
                    pb = self.pending_boss
                    # Place pending boss in center of current camera view when spawning
                    try:
                        pb.x = int(self.camera_x + self.game.WIDTH // 2)
                    except Exception:
                        pass
                    try:
                        b_vis = self._bottom_visible_row(pb.image) if getattr(pb, 'image', None) else None
                        if b_vis is None:
                            b_vis = (pb.image.get_height() if getattr(pb, 'image', None) else getattr(pb, 'target_size', [150,150])[1]) - 1
                        pb.y = self.ground_y - b_vis + self.enemy_vertical_offset
                        pb.base_y = pb.y
                    except Exception:
                        pass
                    self.current_boss = pb
                    print(f"🔥 [FINAL BOSS] Timer-splash spawned pending boss at x={getattr(pb,'x',None)}")
                except Exception as e:
                    print(f"[BOSS VIDEO] Timer spawn error: {e}")
                finally:
                    self.pending_boss = None
                    self.showing_skill_video = False
                    self.skill_video = None
                    self._boss_video_timer_start = None

        keys = pygame.key.get_pressed()
        
        # Update UI
        self.action_buttons.update()

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
            
            # Update bullets and handle collisions
            from ma_nguon.tien_ich import bullet_handler
            bullet_handler.update_bullets(self.player, self.normal_enemies, self.current_boss)
            
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
                else:
                    # Nếu quái vừa chết và có drops, thu thập chúng vào scene
                    if hasattr(enemy, 'spawned_drops') and enemy.spawned_drops:
                        for it in enemy.spawned_drops:
                            self.items.append(it)
                            print(f"[DEBUG] Collected drop into scene: {type(it).__name__} at ({it.x},{it.y})")
                        enemy.spawned_drops = []

            self.normal_enemies = alive_enemies

            # Spawn boss khi hết quái - ĐƠN GIẢN như màn 1
            if not self.normal_enemies:
                if not self.current_boss or self.current_boss.dead:
                    self.spawn_next_boss()
            
            # Backup check: if all normal enemies dead and no current boss and haven't triggered final boss
            if not self.normal_enemies and not self.current_boss and not hasattr(self, 'final_boss_triggered'):
                if self.current_boss_index >= len(self.bosses):
                    print("🎬 [FINAL BOSS] Backup trigger - all enemies clear, no boss, starting final sequence")
                    self.final_boss_triggered = True
                    self.start_final_boss_sequence()

            # Boss update
            if self.current_boss and not self.current_boss.dead:
                self.current_boss.update(target=self.player)
                
            # Kiểm tra boss chết -> trigger final boss
            if self.current_boss and self.current_boss.dead and not hasattr(self, 'final_boss_triggered'):
                print(f"🎯 [DEBUG] Boss died! boss_index={self.current_boss_index}, total_bosses={len(self.bosses)}")
                if self.current_boss_index >= len(self.bosses) and not self.normal_enemies:
                    print("🎬 [TRIGGER] Boss cuối chết + không còn quái -> FINAL BOSS!")
                    self.final_boss_triggered = True
                    self.start_final_boss_sequence()
            
            # Check if current boss just died and trigger final boss
            if self.current_boss and self.current_boss.dead and not hasattr(self, 'final_boss_triggered'):
                if self.current_boss_index >= len(self.bosses):
                    # This was the last regular boss - trigger final boss
                    self.final_boss_triggered = True
                    print("🎬 [FINAL BOSS] Last regular boss died - starting final sequence")
                    self.start_final_boss_sequence()

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
                self.game.game_over_scene = self.game.load_scene("game_over", "NINJA - Màn 2", score)
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
        # If showing final boss video, draw it fullscreen (like skill video in map1)
        if self.showing_skill_video and self.skill_video:
            screen.fill((0, 0, 0))
            self.skill_video.draw(screen)
            return

        # Vẽ các lớp nền phía sau (từ xa đến gần)
        self.parallax_bg.draw_background_layers(screen, self.camera_x)
        
        # Vẽ hiệu ứng lá rơi phía sau nhân vật
        for leaf in self.falling_leaves:
            if leaf['y'] < 400:  # Lá ở phía sau
                self.draw_leaf(screen, leaf, self.camera_x)
        
        # Vẽ thông tin màn chơi (UI luôn cố định trên màn hình)
        text = self.font.render("Màn 2 - Trận Chiến Của Ninja Huyền Thoại", True, (139, 69, 19))
        screen.blit(text, (screen.get_width()//2 - text.get_width()//2, 50))
        info = pygame.font.Font("Tai_nguyen/font/Fz-Donsky.ttf", 30).render("Nhấn ESC để về menu", True, (160, 82, 45))
        screen.blit(info, (screen.get_width()//2 - info.get_width()//2, 100))

        # --- Pickup items ---
        # Pickup items (simple AABB)
        remaining_items = []
        for item in self.items:
            if item.picked:
                continue
            # simple pickup AABB check with player
            item_rect = pygame.Rect(item.x, item.y, 24, 24)
            player_rect = pygame.Rect(self.player.x, self.player.y, 50, 80)
            if player_rect.colliderect(item_rect):
                item.on_pickup(self.player)
                # Trigger HUD pickup animation
                if hasattr(self, 'action_buttons'):
                    if type(item).__name__ == 'Gold':
                        self.action_buttons.trigger_pickup_animation('gold', getattr(item, 'amount', 0))
                    elif type(item).__name__ in ('HealthPotion', 'Health_Potion', 'HealthPotion'):
                        self.action_buttons.trigger_pickup_animation('hp', 1)
                    elif type(item).__name__ in ('ManaPotion', 'Mana_Potion', 'ManaPotion'):
                        self.action_buttons.trigger_pickup_animation('mp', 1)
            else:
                remaining_items.append(item)
        self.items = remaining_items

        # Vẽ quái vật (với camera offset)
        for enemy in self.normal_enemies:
            # Chỉ vẽ quái vật trong tầm nhìn camera
            if enemy.x + 150 >= self.camera_x and enemy.x - 150 <= self.camera_x + self.game.WIDTH:
                enemy.draw(screen, self.camera_x)

        # Vẽ items rơi (với camera offset)
        for item in self.items:
            item.draw(screen, self.camera_x)

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

        # Draw bullets for ALL characters  
        from ma_nguon.tien_ich import bullet_handler
        bullet_handler.draw_bullets(self.player, screen, self.camera_x)

        # Draw UI buttons and HUD on top
        self.action_buttons.draw(screen, player=self.player)


    def handle_events(self, event):
        """Xử lý các sự kiện của màn chơi"""
        # Handle action buttons events first
        if hasattr(self, 'action_buttons'):
            button_action = self.action_buttons.handle_event(event)
            if button_action:
                if button_action == 'attack':
                    self.player.attack()
                elif button_action == 'jump':
                    self.player.jump()
                elif button_action == 'left':
                    self.player.move_left()
                elif button_action == 'right':
                    self.player.move_right()
                elif button_action == 'crouch':
                    self.player.crouch()
                elif button_action == 'skill1':
                    self.player.cast_skill1()
                elif button_action == 'skill2':
                    self.player.cast_skill2()
                elif button_action == 'use_item':
                    self.player.use_health_potion()

        # Xử lý phím tắt
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "menu"
            elif event.key == pygame.K_SPACE:
                self.player.attack()
            elif event.key == pygame.K_w:
                self.player.jump()
            elif event.key == pygame.K_a:
                self.player.move_left()
            elif event.key == pygame.K_d:
                self.player.move_right()  
            elif event.key == pygame.K_s:
                self.player.crouch()
            elif event.key == pygame.K_q:
                self.player.cast_skill1()
            elif event.key == pygame.K_e:
                self.player.cast_skill2()
            elif event.key == pygame.K_r:
                self.player.use_health_potion()

        return None


    def run(self):
        """Chạy màn chơi ninja man 2"""
        clock = pygame.time.Clock()
        
        while True:
            # Xử lý events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                
                result = self.handle_events(event)
                if result:
                    return result

            # Update game state
            self.update()
            
            # Kiểm tra kết thúc game
            # Player HP is stored in `hp` (consistent with other scenes)
            if getattr(self.player, 'hp', getattr(self.player, 'health', 0)) <= 0:
                return "game_over"
            
            # Kiểm tra thắng (tất cả boss đã bị tiêu diệt)
            if self.victory_condition_met():
                # Chuyển sang màn tiếp theo hoặc về menu
                return "victory"
            
            # Vẽ everything
            self.game.screen.fill((0, 0, 0))  # Clear screen
            self.draw(self.game.screen)
            pygame.display.flip()
            
            clock.tick(60)  # 60 FPS


    def victory_condition_met(self):
        """Kiểm tra điều kiện thắng"""
        # Thắng khi không còn quái thường và boss nào
        return len(self.normal_enemies) == 0 and self.current_boss is None