import pygame
import os
import random

# Hàm load ảnh động
def load_action_images(folder, action, target_size=(150, 150)):
    action_folder = os.path.join(folder, action)
    images = []
    if os.path.exists(action_folder):
        # Lọc chỉ lấy file png và có tên là số
        valid_files = []
        for file in os.listdir(action_folder):
            if file.lower().endswith('.png'):
                try:
                    # Thử chuyển đổi tên file thành số
                    num = int(file.split('.')[0])
                    valid_files.append(file)
                except ValueError:
                    # Bỏ qua file có tên không phải số (như Thumbs.db)
                    pass
                    
        # Sắp xếp file theo số
        valid_files.sort(key=lambda x: int(x.split('.')[0]))
        
        for file in valid_files:
            path = os.path.join(action_folder, file)
            img = pygame.image.load(path).convert_alpha()
            w, h = img.get_size()
            scale_ratio = min(target_size[0] / w, target_size[1] / h)
            new_size = (int(w * scale_ratio), int(h * scale_ratio))
            img = pygame.transform.scale(img, new_size)
            canvas = pygame.Surface(target_size, pygame.SRCALPHA)
            x = (target_size[0] - new_size[0]) // 2
            y = (target_size[1] - new_size[1])
            canvas.blit(img, (x, y))
            images.append(canvas)
    return images if images else [pygame.Surface(target_size, pygame.SRCALPHA)]

# Load âm thanh
def load_sound(folder, name):
    path = os.path.join(folder, name)
    if os.path.exists(path):
        return pygame.mixer.Sound(path)
    return None


class QuaiVat:
    def __init__(self, x, y, folder, sound_folder, color=(255,0,0), damage=5, target_size=(150, 150)):
        self.x = x
        self.y = y
        self.hp = 100
        self.speed = 2
        self.color = color
        self.damage = damage
        self.state = "dung_yen"
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = 120
        self.attacking = False
        self.damaged = False  # cờ để chỉ trừ HP 1 lần/đòn
        self.target_size = target_size
        self.flip = False
        self.dead = False
        self.knockback_speed = 0  # vận tốc té ngược
        self.attack_cooldown = 800  # ms giữa 2 lần tấn công
        self.last_attack_time = 0
        
        # Status effects
        self.is_slowed = False
        self.slow_end_time = 0
        self.burn_damage_per_second = 0
        self.burn_end_time = 0
        self.last_burn_tick = 0
        
        # Vùng hoạt động của quái vật
        self.home_x = x  # Vị trí ban đầu
        self.patrol_range = 200  # Phạm vi đi tuần tra
        self.aggro_range = 300  # Phạm vi phát hiện và tấn công người chơi
        self.returning_home = False  # Cờ đánh dấu quái đang trở về vị trí


        # Load animations
        self.animations = {
            "dung_yen": load_action_images(folder, "dung_yen", self.target_size),
            "chay": load_action_images(folder, "chay", self.target_size),
            "danh": load_action_images(folder, "danh", self.target_size),
            "da": load_action_images(folder, "da", self.target_size),
            "do": load_action_images(folder, "do", self.target_size),
            "nhay": load_action_images(folder, "nhay", self.target_size),
            "nga": load_action_images(folder, "nga", self.target_size),
        }
        self.image = self.animations["dung_yen"][0]

        # Load âm thanh
        self.sounds = {
            "danh": load_sound(sound_folder, "danh.mp3"),
            "da": load_sound(sound_folder, "da.mp3"),
            "dinh_don": load_sound(sound_folder, "dinh_don.mp3"),
            "chet": load_sound(sound_folder, "chet.mp3"),
        }

    def update(self, target=None):
        now = pygame.time.get_ticks()
        
        # Apply burn effect
        if self.burn_end_time > 0 and now < self.burn_end_time:
            if now - self.last_burn_tick >= 1000:  # Every second
                self.hp -= self.burn_damage_per_second
                self.last_burn_tick = now
                if self.hp <= 0 and not self.dead:
                    self.dead = True
                    self.state = "nga"
                    self.frame = 0
                    self.image = self.animations["nga"][0]
                    if self.sounds.get("chet"):
                        self.sounds["chet"].play()
                    self.knockback_speed = 5
                    try:
                        self.spawned_drops = self.spawn_drops()
                    except Exception:
                        self.spawned_drops = []
        elif now >= self.burn_end_time:
            self.burn_end_time = 0
            self.burn_damage_per_second = 0
        
        # Check slow status
        if self.is_slowed and now >= self.slow_end_time:
            self.is_slowed = False
        
        # Get effective speed (reduced if slowed)
        effective_speed = self.speed * 0.5 if self.is_slowed else self.speed
        
        # Reset damaged flag chỉ khi player THỰC SỰ dừng tấn công
        if target and hasattr(target, 'actioning') and hasattr(target, 'action_type'):
            # Chỉ reset khi player không đang trong trạng thái action attack
            if not target.actioning and target.action_type not in ["danh", "da"]:
                self.damaged = False
            # Hoặc khi player ở xa quá (không thể đánh trúng)
            elif abs(self.x - target.x) > 120:
                self.damaged = False
        else:
            # Không có target hoặc target không hợp lệ
            self.damaged = False

        # --- Nếu đã chết ---
        if self.dead:
            self.x += self.knockback_speed
            self.knockback_speed *= 0.9  # giảm dần ma sát
            if now - self.last_update > self.animation_cooldown:
                self.last_update = now
                if self.frame < len(self.animations["nga"]) - 1:
                    self.frame += 1
                self.image = self.animations["nga"][self.frame]
            return

        # --- Nếu đang tấn công ---
        if self.attacking:
            if now - self.last_update > self.animation_cooldown:
                self.last_update = now
                self.frame += 1
                if self.frame >= len(self.animations[self.state]):
                    self.attacking = False
                    self.state = "dung_yen"
                    self.frame = 0
                else:
                    self.image = self.animations[self.state][self.frame]
            return

        # --- AI di chuyển và tấn công ---
        if target and not self.dead:
            distance = abs(self.x - target.x)
            distance_from_home = abs(self.x - self.home_x)
            
            # Kiểm tra nếu quái vật ở ngoài vùng tuần tra và không đuổi theo target
            if distance_from_home > self.patrol_range and distance > self.aggro_range:
                self.returning_home = True
            
            # Quái vật đang quay về nhà
            if self.returning_home:
                self.state = "chay"
                if self.x < self.home_x:
                    self.flip = False
                    self.x += effective_speed
                elif self.x > self.home_x:
                    self.flip = True
                    self.x -= effective_speed
                
                # Nếu đã về gần vị trí home, dừng lại
                if abs(self.x - self.home_x) < 10:
                    self.returning_home = False
                    self.state = "dung_yen"
            
            # Target trong tầm tấn công và trong phạm vi hoạt động
            elif distance < 80 and distance < self.aggro_range:
                self.flip = self.x > target.x
                if now - self.last_attack_time > self.attack_cooldown:
                    self.state = random.choice(["danh", "da"])
                    self.attacking = True
                    self.frame = 0
                    self.last_attack_time = now
                    self.image = self.animations[self.state][self.frame]
                    # phát âm thanh
                    if self.sounds[self.state]:
                        self.sounds[self.state].play()
            
            # Target trong tầm phát hiện, nhưng chưa trong tầm tấn công
            elif distance < self.aggro_range:
                self.returning_home = False
                self.state = "chay"
                self.flip = self.x > target.x
                
                if self.x < target.x:
                    self.x += effective_speed
                else:
                    self.x -= effective_speed
            
            # Đi tuần tra trong vùng hoạt động khi không có target
            elif not self.returning_home and random.random() < 0.01:  # Xác suất nhỏ để thay đổi hướng
                self.state = "chay"
                self.flip = not self.flip
            else:
                self.state = "dung_yen"
                
            # Giữ quái vật trong vùng tuần tra
            if distance_from_home > self.patrol_range and not self.returning_home:
                self.returning_home = True
        else:
            self.state = "dung_yen"

        # --- Animation bình thường ---
        if now - self.last_update > self.animation_cooldown:
            self.last_update = now
            self.frame = (self.frame + 1) % len(self.animations[self.state])
            self.image = self.animations[self.state][self.frame]

    def take_damage(self, damage, attacker_flip, attacker=None):
        if self.dead:
            return

        # If attacker object is provided, derive the damage from attacker to avoid
        # callers accidentally passing an already-adjusted damage value (which
        # could double-count equipment bonuses). We still accept the numeric
        # damage parameter when attacker is None.
        computed_damage = damage
        try:
            if attacker is not None:
                # If attacker is performing a kick, include kick_damage plus attack bonus
                atk_type = getattr(attacker, 'action_type', None)
                if atk_type == 'da' or atk_type == 'kick':
                    # include equipment attack bonus for kicks too
                    computed_damage = int(getattr(attacker, 'kick_damage', 0) + attacker.get_attack_bonus())
                else:
                    # default: use effective damage (already includes equipment bonuses)
                    computed_damage = int(attacker.get_effective_damage())
        except Exception:
            # Fallback to provided damage if anything goes wrong
            computed_damage = damage

        # Apply raw damage
        self.hp -= computed_damage
        if self.sounds.get("dinh_don"):
            self.sounds["dinh_don"].play()

        # Apply special effects from attacker's equipment
        if attacker:
            # Check for slow effect
            if hasattr(attacker, 'has_slow_effect') and attacker.has_slow_effect():
                self.apply_slow(2.0)  # 2 seconds slow

            # Check for burn effect
            if hasattr(attacker, 'get_burn_effect'):
                burn_dmg, burn_dur = attacker.get_burn_effect()
                if burn_dmg > 0:
                    self.apply_burn(burn_dmg, burn_dur)

        # Death handling
        if self.hp <= 0:
            self.dead = True
            self.state = "nga"
            self.frame = 0
            self.image = self.animations["nga"][0]
            if self.sounds.get("chet"):
                self.sounds["chet"].play()
            # Té ngược chiều người đánh
            self.knockback_speed = -10 if attacker_flip == False else 10
            # generate drops and store them for the scene to collect
            try:
                self.spawned_drops = self.spawn_drops()
            except Exception:
                self.spawned_drops = []
    
    def apply_slow(self, duration):
        """Apply slow effect for duration seconds"""
        self.is_slowed = True
        self.slow_end_time = pygame.time.get_ticks() + int(duration * 1000)
    
    def apply_burn(self, damage, duration):
        """Apply burn effect"""
        self.burn_damage_per_second = damage
        self.burn_end_time = pygame.time.get_ticks() + int(duration * 1000)
        self.last_burn_tick = pygame.time.get_ticks()

    def spawn_drops(self):
        """Return a list of item instances dropped at the enemy position."""
        drops = []
        try:
            from ma_nguon.doi_tuong.items import Gold, HealthPotion, ManaPotion
        except Exception:
            return drops

        # Always drop small gold
        amount = random.randint(5, 20)
        drops.append(Gold(self.x, self.y, amount))
        print(f"[DEBUG] QuaiVat at ({self.x},{self.y}) will drop Gold={amount}")

        # Small chance for health potion (10%)
        if random.random() < 0.10:
            drops.append(HealthPotion(self.x + random.randint(-20,20), self.y, heal=random.randint(100, 300)))
            print(f"[DEBUG] QuaiVat at ({self.x},{self.y}) will drop HealthPotion")

        # Small chance for mana potion (15%)
        if random.random() < 0.15:
            drops.append(ManaPotion(self.x + random.randint(-20,20), self.y, mana=random.randint(50, 150)))
            print(f"[DEBUG] QuaiVat at ({self.x},{self.y}) will drop ManaPotion")

        return drops
    def draw(self, screen, camera_x=0):
        # Tính toán vị trí vẽ sau khi trừ camera offset
        draw_x = self.x - camera_x
        
        # Đảm bảo rằng chúng ta đang dùng frame hiện tại của animation
        if 0 <= self.frame < len(self.animations[self.state]):
            self.image = self.animations[self.state][self.frame]
        else:
            # Nếu frame index không hợp lệ, reset về 0
            self.frame = 0
            self.image = self.animations[self.state][self.frame]
        
        # Lật ảnh nếu quái vật đang hướng sang trái
        img = pygame.transform.flip(self.image, self.flip, False)
        
        # Vẽ quái vật
        screen.blit(img, (draw_x, self.y))
        
        # Vẽ thanh máu nếu quái vật còn sống
        if not self.dead:
            pygame.draw.rect(screen, (100,100,100), (draw_x, self.y-15, 60, 8))
            # Luôn dùng màu đỏ cho thanh máu của quái
            pygame.draw.rect(screen, (255, 0, 0), (draw_x, self.y-15, int(60*self.hp/100), 8))
            
            # Visual indicators for status effects
            indicator_x = draw_x + 65
            indicator_y = self.y - 15
            
            # Burn effect indicator (fire icon)
            if self.burn_end_time > 0 and pygame.time.get_ticks() < self.burn_end_time:
                # Draw small fire icon (orange/red circle with flame)
                pygame.draw.circle(screen, (255, 100, 0), (indicator_x, indicator_y + 4), 6)
                pygame.draw.circle(screen, (255, 200, 0), (indicator_x, indicator_y + 2), 4)
                indicator_x += 15
            
            # Slow effect indicator (ice/snowflake icon)
            if self.is_slowed and pygame.time.get_ticks() < self.slow_end_time:
                # Draw ice crystal (light blue diamond)
                points = [
                    (indicator_x, indicator_y),
                    (indicator_x + 4, indicator_y + 4),
                    (indicator_x, indicator_y + 8),
                    (indicator_x - 4, indicator_y + 4)
                ]
                pygame.draw.polygon(screen, (100, 200, 255), points)
                pygame.draw.polygon(screen, (200, 240, 255), points, 1)
