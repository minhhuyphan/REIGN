# file: quai_vat_manh.py
from ma_nguon.doi_tuong.quai_vat.quai_vat import QuaiVat
import random
import pygame
class Boss1(QuaiVat):
    def __init__(self, x, y, folder, sound_folder):
        super().__init__(x, y, folder, sound_folder, color=(255,0,0), damage=15)
        self.hp = 150
        self.speed = 3
        self.damage = 10
        self.attack_cooldown = 600  # tấn công nhanh hơn

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
