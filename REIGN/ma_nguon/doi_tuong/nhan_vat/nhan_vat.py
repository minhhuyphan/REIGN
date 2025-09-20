import pygame, os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.quan_ly_tai_nguyen import load_images, load_sound_safe

class Character:
    def __init__(self, x, y, folder, controls=None, color=(0,255,0), auto=False, stats=None):
        self.x = x
        self.y = y
        self.base_y = y
        self.flip = False
        
        # Thêm stats để dễ tùy chỉnh từ màn chọn nhân vật
        if stats:
            self.hp = stats.get("hp", 500)
            self.max_hp = stats.get("hp", 500)
            self.speed = stats.get("speed", 5)
            self.damage = stats.get("damage", 30)
            self.kick_damage = stats.get("kick_damage", 20)
            self.defense = stats.get("defense", 2)
            self.regen_hp = stats.get("regen_hp", 0)
        else:
            self.hp = 500
            self.max_hp = 500
            self.speed = 5
            self.damage = 30
            self.kick_damage = 20
            self.defense = 2
            self.regen_hp = 1  # HP hồi mỗi giây
        
        self.controls = controls or {}
        self.color = color
        self.auto = auto
        self.folder = folder  # Lưu folder để tải lại animation nếu cần

        # Animation
        self.animations = self._load_animations(folder)
        self.state = "dung_yen"
        self.frame = 0
        self.image = self.animations[self.state][0] if self.animations[self.state] else None
        self.animation_cooldown = 100
        self.last_update = pygame.time.get_ticks()

        # Âm thanh
        self.sound_punch = load_sound_safe("../Tai_nguyen/am_thanh/hieu_ung/danh.mp3", 1.0)
        self.sound_kick = load_sound_safe("../Tai_nguyen/am_thanh/hieu_ung/da.mp3", 1.0)
        self.sound_hit = load_sound_safe("../Tai_nguyen/am_thanh/hieu_ung/trung.mp3", 1.0)
        self.sound_run = load_sound_safe("../Tai_nguyen/am_thanh/hieu_ung/chay.mp3", 0.5)

        # Trạng thái động
        self.actioning = False
        self.action_type = ""
        self.jumping = False
        self.jump_vel = 0
        self.running_sound_playing = False
        self.damaged = False
        self.defending = False
        self.dead = False
        self.knockback_speed = 0

# Trong phương thức _load_animations, thêm xử lý scale riêng cho từng loại animation

    def _load_animations(self, folder):
        """Tải tất cả animation từ thư mục, đảm bảo tất cả có cùng kích thước"""
        animations = {}
        action_types = ["dung_yen", "chay", "danh", "da", "nga", "do", "nhay"]
        
        # Chuẩn hóa kích thước mặc định cho mọi animation
        base_width = 100
        base_height = 150
        
        # Lưu giữ kích thước gốc của mỗi animation
        self.animation_sizes = {}
        
        # Tải tất cả các animation trước
        raw_animations = {}
        for action in action_types:
            action_path = os.path.join(folder, action)
            try:
                images = load_images(action_path)
                if images:
                    raw_animations[action] = images
                    # Lưu kích thước gốc
                    self.animation_sizes[action] = (images[0].get_width(), images[0].get_height())
                else:
                    print(f"Warning: No images found for {action} in {action_path}")
                    # Tạo 1 hình ảnh giả làm placeholder
                    dummy = pygame.Surface((base_width, base_height), pygame.SRCALPHA)
                    dummy.fill((100, 100, 100, 150))
                    raw_animations[action] = [dummy]
                    self.animation_sizes[action] = (base_width, base_height)
            except Exception as e:
                print(f"Error loading animation {action}: {e}")
                # Tạo 1 hình ảnh giả làm placeholder
                dummy = pygame.Surface((base_width, base_height), pygame.SRCALPHA)
                dummy.fill((100, 100, 100, 150))
                raw_animations[action] = [dummy]
                self.animation_sizes[action] = (base_width, base_height)
        
        # Tìm kích thước trung bình của tất cả animation
        total_width = 0
        total_height = 0
        count = 0
        
        for action, images in raw_animations.items():
            if images:
                width, height = self.animation_sizes[action]
                total_width += width
                total_height += height
                count += 1
        
        # Tính kích thước trung bình
        if count > 0:
            avg_width = total_width // count
            avg_height = total_height // count
        else:
            avg_width = base_width
            avg_height = base_height
        
        # Scale tất cả animation về cùng kích thước trung bình
        for action, images in raw_animations.items():
            scaled_images = []
            for img in images:
                # Scale hình ảnh về kích thước trung bình
                scaled = pygame.transform.scale(img, (avg_width, avg_height))
                scaled_images.append(scaled)
            animations[action] = scaled_images
    
        return animations
    def start_action(self, action_type):
        if self.actioning and action_type != "nga":
            return
        
        # Kiểm tra nếu animation tồn tại
        if action_type not in self.animations:
            print(f"Warning: Animation {action_type} not found")
            return
            
        self.actioning = True
        self.action_type = action_type
        self.state = action_type
        self.frame = 0
        self.damaged = False

        if action_type == "nhay" and not self.jumping:
            self.jumping = True
            self.jump_vel = -12
            if self.running_sound_playing and self.sound_run:
                self.sound_run.stop()
                self.running_sound_playing = False
        if action_type == "danh" and self.sound_punch:
            self.sound_punch.play()
        elif action_type == "da" and self.sound_kick:
            self.sound_kick.play()

    def play_animation(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_cooldown:
            self.last_update = now
            self.frame += 1

        # Đảm bảo animation tồn tại
        if self.state not in self.animations:
            self.state = "dung_yen"
            self.frame = 0
            
        # Đảm bảo frame luôn nằm trong khoảng hợp lệ
        max_frames = len(self.animations[self.state])
        
        # Kiểm tra và xử lý khi animation kết thúc
        if self.frame >= max_frames:
            if self.state in ["danh", "da", "do", "nhay"]:
                self.actioning = False
                self.state = "dung_yen"
                self.frame = 0
                self.damaged = False
            elif self.state == "nga":
                self.frame = max_frames - 1
            else:
                self.frame = 0

    def update(self, keys=None, target=None):
        # Xử lý knockback khi bị đánh
        if self.knockback_speed != 0:
            self.x += self.knockback_speed
            self.knockback_speed = int(self.knockback_speed * 0.8)  # Giảm dần tốc độ
            if abs(self.knockback_speed) < 1:
                self.knockback_speed = 0
        
        # Hồi máu nhỏ
        if self.hp > 0:
            self.hp = min(self.hp + self.regen_hp, self.max_hp)

        # Nếu đã chết và animation ngã hết thì đứng yên
        if self.dead and self.frame == len(self.animations["nga"]) - 1:
            return

        moving = False
        self.defending = False

        # --- Xử lý action ---
        if self.actioning:
            if self.action_type == "nhay" and self.jumping:
                self.y += self.jump_vel
                self.jump_vel += 1
                if self.y >= self.base_y:
                    self.y = self.base_y
                    self.jumping = False
                    self.jump_vel = 0
                    self.actioning = False
                    self.action_type = ""
                    if keys and (self.controls.get("left") and keys[self.controls.get("left", pygame.K_LEFT)] or
                                 self.controls.get("right") and keys[self.controls.get("right", pygame.K_RIGHT)]):
                        self.state = "chay"
                    else:
                        self.state = "dung_yen"
            self.play_animation()
            return

        # --- Người chơi điều khiển ---
        if not self.auto and keys and self.hp > 0:
            if self.controls.get("jump") and keys[self.controls["jump"]] and not self.jumping:
                self.start_action("nhay")
            elif self.controls.get("defend") and keys[self.controls["defend"]]:
                self.start_action("do")
                self.defending = True
            elif self.controls.get("attack") and keys[self.controls["attack"]]:
                self.start_action("danh")
            elif self.controls.get("kick") and keys[self.controls["kick"]]:
                self.start_action("da")
            elif self.controls.get("right") and keys[self.controls["right"]]:
                self.state = "chay"
                self.flip = False
                self.x += self.speed
                moving = True
            elif self.controls.get("left") and keys[self.controls["left"]]:
                self.state = "chay"
                self.flip = True
                self.x -= self.speed
                moving = True
            else:
                self.state = "dung_yen"

        # --- Enemy auto ---
        if self.auto and self.hp > 0 and target:
            distance = abs(self.x - target.x)
            # Quái di chuyển đến gần người chơi
            if distance > 120:
                self.state = "chay"
                if self.x < target.x:
                    self.flip = False
                    self.x += self.speed
                else:
                    self.flip = True
                    self.x -= self.speed
                moving = True
            # Quái tấn công khi đủ gần
            elif distance < 120:
                # Random giữa đánh và đá
                import random
                if not self.actioning and random.random() < 0.03:  # 3% mỗi frame
                    action = random.choice(["danh", "da"])
                    self.start_action(action)
            else:
                self.state = "dung_yen"

        # --- Âm thanh chạy ---
        if self.sound_run:
            if moving and not self.running_sound_playing:
                self.sound_run.play(-1)
                self.running_sound_playing = True
            elif not moving and self.running_sound_playing:
                self.sound_run.stop()
                self.running_sound_playing = False

        self.play_animation()

        # --- Nếu chết ---
        if self.hp <= 0 and not self.dead:
            self.dead = True
            self.start_action("nga")

    def draw(self, surface, camera_x=0):
        # Tính toán vị trí vẽ sau khi trừ camera offset
        draw_x = self.x - camera_x
        
        # Đảm bảo rằng chúng ta đang dùng frame hiện tại của animation
        if self.state in self.animations and 0 <= self.frame < len(self.animations[self.state]):
            self.image = self.animations[self.state][self.frame]
        else:
            # Nếu frame không hợp lệ, đặt lại về 0
            self.frame = 0
            if self.state in self.animations and len(self.animations[self.state]) > 0:
                self.image = self.animations[self.state][0]
        
        # Kiểm tra xem image có tồn tại không
        if self.image:
            # Lật ảnh nếu nhân vật đang hướng sang trái
            img = pygame.transform.flip(self.image, self.flip, False)
            
            # Vẽ nhân vật
            surface.blit(img, (draw_x, self.y))
        
        # Không vẽ thanh máu ở đây nữa, nó sẽ được vẽ ở góc màn hình

    def take_damage(self, damage, attacker_flip):
        # Nếu đang đỡ, giảm damage
        if self.defending:
            damage = max(1, damage // 5)  # Chỉ nhận 20% damage khi đỡ
        
        if self.hp <= 0 or self.dead:
            return
            
        # Giảm damage bởi defense
        net_damage = max(damage - self.defense, 0)
        self.hp -= net_damage
        
        if self.sound_hit:
            self.sound_hit.play()
            
        # Khi nhận damage, reset trạng thái damaged
        self.damaged = True
        
        if self.hp <= 0:
            self.dead = True
            self.start_action("nga")
            # Té ngược
            self.knockback_speed = -15 if not attacker_flip else 15
        else:
            # Bị đẩy lùi khi trúng đòn
            self.knockback_speed = -5 if not attacker_flip else 5