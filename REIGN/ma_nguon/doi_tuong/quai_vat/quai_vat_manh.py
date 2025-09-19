# file: quai_vat_manh.py
from ma_nguon.doi_tuong.quai_vat.quai_vat import QuaiVat
import random
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

    def update(self, target=None):
        super().update(target)
        # 30% tỉ lệ tung đòn mạnh
        if target and not self.dead and random.random() < self.special_chance:
            if self.state in ["dung_yen","chay"]:
                self.state = "danh"
                self.attacking = True
                self.frame = 0
                if hasattr(target,"take_damage"):
                    target.take_damage(self.damage*2, self.flip)

class Boss3(QuaiVat):
    def __init__(self, x, y, folder, sound_folder):
        super().__init__(x, y, folder, sound_folder, color=(255,0,0), damage=20)
        self.hp = 400
        self.speed = 5
        self.damage = 20
        self.attack_cooldown = 400
        self.special_chance = 0.5

    def update(self, target=None):
        super().update(target)
        # 50% tỉ lệ tung đòn mạnh + nhảy đánh
        if target and not self.dead and random.random() < self.special_chance:
            if self.state in ["dung_yen","chay"]:
                self.state = "nhay"
                self.attacking = True
                self.frame = 0
                if hasattr(target,"take_damage"):
                    target.take_damage(self.damage*2, self.flip)
