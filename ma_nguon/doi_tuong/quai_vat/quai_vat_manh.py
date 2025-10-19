# file: quai_vat_manh.py
from ma_nguon.doi_tuong.quai_vat.quai_vat import QuaiVat
import random
import pygame
import os
class Boss1(QuaiVat):
    def __init__(self, x, y, folder, sound_folder):
        super().__init__(x, y, folder, sound_folder, color=(255,0,0), damage=15)
        self.hp = 150
        self.speed = 3
        self.damage = 10
        self.attack_cooldown = 600  # tấn công nhanh hơn
        # Phóng to boss để nổi bật hơn
        self.target_size = (320, 320)
        # Boss Map Công Nghệ: folder chứa các frame 0..6.png ở ngay trong thư mục
        # Ghi đè animations để dùng chuỗi ảnh đơn giản này cho tất cả action
        try:
            frames = []
            if os.path.isdir(folder):
                # lấy các file png tên dạng số, sắp xếp theo số
                files = []
                for f in os.listdir(folder):
                    if f.lower().endswith('.png'):
                        try:
                            _ = int(os.path.splitext(f)[0])
                            files.append(f)
                        except Exception:
                            pass
                files.sort(key=lambda n: int(os.path.splitext(n)[0]))

                # nạp ảnh và scale vừa với kích thước mục tiêu đã set
                target_size = self.target_size
                for f in files:
                    p = os.path.join(folder, f)
                    img = pygame.image.load(p).convert_alpha()
                    w, h = img.get_size()
                    scale_ratio = min(target_size[0] / w, target_size[1] / h)
                    new_size = (int(w * scale_ratio), int(h * scale_ratio))
                    img = pygame.transform.scale(img, new_size)
                    canvas = pygame.Surface(target_size, pygame.SRCALPHA)
                    x_off = (target_size[0] - new_size[0]) // 2
                    y_off = (target_size[1] - new_size[1])
                    canvas.blit(img, (x_off, y_off))
                    frames.append(canvas)

            # nếu nạp được ít nhất 1 frame thì set cho mọi trạng thái để an toàn
            if frames:
                seq = frames
                self.animations = {
                    "dung_yen": seq,
                    "chay": seq,
                    "danh": seq,
                    "da": seq,
                    "do": seq,
                    "nhay": seq,
                    "nga": seq,
                }
                self.image = self.animations["dung_yen"][0]
                self.frame = 0
        except Exception:
            # Nếu lỗi, giữ nguyên animations đã được base class thiết lập
            pass
        
class Boss2(QuaiVat):
    def __init__(self, x, y, folder, sound_folder):
        super().__init__(x, y, folder, sound_folder, color=(255,0,0), damage=15)
        self.hp = 250
        self.speed = 4
        self.damage = 15
        self.attack_cooldown = 500
        self.special_chance = 0.3  # tỉ lệ dùng đòn đặc biệt
        self.special_damage_multiplier = 2.0  # Đòn đặc biệt gấp đôi sát thương

    def update(self, target=None):
        super().update(target)
        # Boss2 có thể tấn công mạnh hơn với xác suất cao hơn
        if target and not self.dead and not self.attacking:
            distance = abs(self.x - target.x)
            if distance < 80 and random.random() < self.special_chance:
                now = pygame.time.get_ticks()
                if now - self.last_attack_time > self.attack_cooldown:
                    self.state = "danh"  # Ưu tiên đòn đánh mạnh
                    self.attacking = True
                    self.frame = 0
                    self.last_attack_time = now
                    self.image = self.animations[self.state][self.frame]
                    if self.sounds[self.state]:
                        self.sounds[self.state].play()
    
    def get_current_damage(self):
        # Trả về damage hiện tại (có thể là đòn đặc biệt)
        if self.state == "danh" and hasattr(self, 'special_damage_multiplier'):
            return int(self.damage * self.special_damage_multiplier)
        return self.damage

class Boss3(QuaiVat):
    def __init__(self, x, y, folder, sound_folder):
        super().__init__(x, y, folder, sound_folder, color=(255,0,0), damage=20)
        self.hp = 400
        self.speed = 5
        self.damage = 20
        self.attack_cooldown = 400
        self.special_chance = 0.5
        self.special_damage_multiplier = 2.0  # Đòn đặc biệt gấp đôi sát thương

    def update(self, target=None):
        super().update(target)
        # Boss3 có thể tấn công nhảy với sát thương mạnh
        if target and not self.dead and not self.attacking:
            distance = abs(self.x - target.x)
            if distance < 80 and random.random() < self.special_chance:
                now = pygame.time.get_ticks()
                if now - self.last_attack_time > self.attack_cooldown:
                    # Chọn ngẫu nhiên giữa đòn nhảy và đòn đánh thường
                    attack_type = random.choice(["da", "danh"])
                    self.state = attack_type
                    self.attacking = True
                    self.frame = 0
                    self.last_attack_time = now
                    self.image = self.animations[self.state][self.frame]
                    if self.sounds[self.state]:
                        self.sounds[self.state].play()
    
    def get_current_damage(self):
        # Trả về damage hiện tại (đòn nhảy có damage đặc biệt)
        if self.state in ["da", "danh"] and hasattr(self, 'special_damage_multiplier'):
            return int(self.damage * self.special_damage_multiplier)
        return self.damage
