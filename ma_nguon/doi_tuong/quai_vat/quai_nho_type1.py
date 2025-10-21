import pygame
import os
import random

# Hàm load ảnh động cho quái nhỏ type 1 (dùng folder có đuôi 1: chay1, danh1, etc.)
def load_action_images(folder, action, target_size=(150, 150)):
    # Thêm đuôi "1" vào tên action để load từ folder _1
    action_folder = os.path.join(folder, action + "1")
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


class QuaiNhoType1:
    """Quái nhỏ type 1 - sử dụng các animation folder có đuôi 1 (chay1, danh1, etc.)"""
    
    def __init__(self, x, y, folder, sound_folder, color=(255,0,0), damage=5, target_size=(150, 150)):
        self.x = x
        self.y = y
        self.hp = 80  # Ít máu hơn quái thường một chút
        self.max_hp = 80  # Lưu HP tối đa
        self.speed = 2.5  # Nhanh hơn một chút
        self.color = color
        self.damage = damage
        self.state = "dung_yen"
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = 120
        self.attacking = False
        self.damaged = False  # cờ để chỉ trừ HP 1 lần/đòn
        self.has_been_damaged = False  # Cờ để biết quái đã bị đánh chưa
        self.target_size = target_size
        self.flip = False
        self.dead = False
        self.knockback_speed = 0  # vận tốc té ngược
        self.attack_cooldown = 700  # ms giữa 2 lần tấn công (nhanh hơn một chút)
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

        self.folder = folder
        # Load animations - sử dụng các folder có đuôi "1"
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
        
        # Giá trị điểm khi tiêu diệt
        self.score_value = 100

    def update(self, target=None):
        """Cập nhật trạng thái của quái vật"""
        now = pygame.time.get_ticks()

        # Xử lý status effects
        if self.is_slowed and now > self.slow_end_time:
            self.is_slowed = False
            
        if self.burn_damage_per_second > 0 and now < self.burn_end_time:
            if now - self.last_burn_tick > 1000:
                self.hp -= self.burn_damage_per_second
                self.last_burn_tick = now
        elif now >= self.burn_end_time:
            self.burn_damage_per_second = 0

        # Nếu đã chết, chỉ update animation
        if self.dead:
            if self.state != "do":
                self.state = "do"
                self.frame = 0
            self.update_animation()
            return

        # Nếu HP <= 0, chuyển sang trạng thái chết
        if self.hp <= 0 and not self.dead:
            self.dead = True
            self.state = "do"
            self.frame = 0
            if self.sounds["chet"]:
                self.sounds["chet"].play()
            return

        # Xử lý knockback
        if self.knockback_speed != 0:
            self.x += self.knockback_speed
            self.knockback_speed *= 0.85  # Giảm dần
            if abs(self.knockback_speed) < 0.5:
                self.knockback_speed = 0
                self.damaged = False

        # AI logic
        if target and not self.dead:
            dist_to_target = abs(self.x - target.x)
            dist_to_home = abs(self.x - self.home_x)

            # Nếu đang tấn công
            if self.attacking:
                # Chờ animation tấn công hoàn thành
                if self.state in ["danh", "da"]:
                    if self.frame >= len(self.animations[self.state]) - 1:
                        self.attacking = False
                        self.state = "dung_yen"
                        self.frame = 0
                self.update_animation()
                return

            # Nếu xa home quá và player không ở gần
            if dist_to_home > self.patrol_range * 1.5 and dist_to_target > self.aggro_range:
                self.returning_home = True

            # Nếu đang về nhà
            if self.returning_home:
                if dist_to_home < 10:
                    self.returning_home = False
                    self.state = "dung_yen"
                    self.x = self.home_x
                else:
                    self.state = "chay"
                    direction = 1 if self.home_x > self.x else -1
                    self.flip = direction < 0
                    current_speed = self.speed
                    if self.is_slowed:
                        current_speed *= 0.5
                    self.x += direction * current_speed
            # Nếu player trong tầm aggro
            elif dist_to_target < self.aggro_range:
                # Nếu đủ gần để tấn công
                if dist_to_target < 100:
                    if now - self.last_attack_time > self.attack_cooldown:
                        self.attacking = True
                        self.state = random.choice(["danh", "da"])
                        self.frame = 0
                        self.last_attack_time = now
                        if self.sounds[self.state]:
                            self.sounds[self.state].play()
                    else:
                        self.state = "dung_yen"
                # Nếu chưa đủ gần, chạy lại gần
                else:
                    self.state = "chay"
                    direction = 1 if target.x > self.x else -1
                    self.flip = direction < 0
                    current_speed = self.speed
                    if self.is_slowed:
                        current_speed *= 0.5
                    self.x += direction * current_speed
            # Nếu player ngoài tầm aggro, đi tuần tra
            else:
                if dist_to_home < self.patrol_range:
                    # Random di chuyển trong vùng patrol
                    if random.random() < 0.02:
                        direction = random.choice([-1, 1])
                        self.flip = direction < 0
                        current_speed = self.speed
                        if self.is_slowed:
                            current_speed *= 0.5
                        self.x += direction * current_speed * 0.5
                        self.state = "chay"
                    else:
                        self.state = "dung_yen"
                else:
                    # Quay về home nếu đi xa quá
                    self.returning_home = True

        self.update_animation()

    def update_animation(self):
        """Cập nhật frame animation"""
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_cooldown:
            self.last_update = now
            if self.state in self.animations:
                self.frame += 1
                if self.frame >= len(self.animations[self.state]):
                    if self.state == "do":
                        self.frame = len(self.animations[self.state]) - 1
                    else:
                        self.frame = 0
                
                self.image = self.animations[self.state][self.frame]
                if self.flip:
                    self.image = pygame.transform.flip(self.image, True, False)

    def draw(self, screen, camera_x):
        """Vẽ quái vật lên màn hình"""
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
        
        # Vẽ thanh HP nếu chưa chết (luôn hiển thị như QuaiVat)
        if not self.dead:
            hp_bar_width = 60
            hp_bar_height = 8
            hp_bar_x = draw_x
            hp_bar_y = self.y - 15
            
            # Background (xám)
            pygame.draw.rect(screen, (100, 100, 100), 
                           (hp_bar_x, hp_bar_y, hp_bar_width, hp_bar_height))
            # Foreground (đỏ) - tính theo max_hp
            hp_percentage = max(0, self.hp / self.max_hp)
            pygame.draw.rect(screen, (255, 0, 0), 
                           (hp_bar_x, hp_bar_y, int(hp_bar_width * hp_percentage), hp_bar_height))

    def take_damage(self, damage, attacker_flip=False, attacker=None):
        """Nhận sát thương từ player"""
        if self.dead:
            return
        
        self.has_been_damaged = True  # Đánh dấu đã bị damage
        self.hp -= damage
        
        # Hiệu ứng knockback
        knockback_direction = -1 if attacker_flip else 1
        self.knockback_speed = knockback_direction * 8
        
        # Phát âm thanh
        if self.sounds["dinh_don"]:
            self.sounds["dinh_don"].play()
        
        # Chuyển sang trạng thái bị đánh
        if self.hp > 0:
            self.state = "nga"
            self.frame = 0
        else:
            # Chết
            self.dead = True
            self.state = "do"
            self.frame = 0
            if self.sounds["chet"]:
                self.sounds["chet"].play()
            
            # Tạo item rơi ra nếu có attacker
            if attacker and hasattr(attacker, 'scene'):
                self.drop_item(attacker.scene)
    
    def drop_item(self, scene):
        """Tạo item rơi ra khi quái chết"""
        # Import tại thời điểm cần thiết để tránh circular import
        try:
            from ma_nguon.doi_tuong.items import HealthPotion, ManaPotion, Gold
        except Exception:
            return
        
        # 30% rơi health potion, 20% rơi mana potion, 50% rơi vàng
        rand = random.random()
        if rand < 0.3:
            item = HealthPotion(self.x + 50, self.y + 50)
        elif rand < 0.5:
            item = ManaPotion(self.x + 50, self.y + 50)
        else:
            item = Gold(self.x + 50, self.y + 50, amount=random.randint(10, 30))
        
        if hasattr(scene, 'items'):
            scene.items.append(item)

    def apply_slow(self, duration_ms):
        """Áp dụng hiệu ứng làm chậm"""
        self.is_slowed = True
        self.slow_end_time = pygame.time.get_ticks() + duration_ms
        
    def apply_burn(self, damage_per_second, duration_ms):
        """Áp dụng hiệu ứng bỏng"""
        self.burn_damage_per_second = damage_per_second
        self.burn_end_time = pygame.time.get_ticks() + duration_ms
        self.last_burn_tick = pygame.time.get_ticks()
