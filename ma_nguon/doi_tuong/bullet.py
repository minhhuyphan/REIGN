import pygame
import os

class Bullet:
    """Class đại diện cho viên đạn"""
    def __init__(self, x, y, direction, damage, owner):
        self.x = x
        self.y = y
        self.direction = direction  # 1 = phải, -1 = trái
        self.speed = 15
        self.damage = damage
        self.owner = owner
        self.active = True
        
        # Load hình ảnh đạn từ folder chieu của tho_san_quai_vat
        try:
            bullet_path = os.path.join("tai_nguyen", "hinh_anh", "nhan_vat", "tho_san_quai_vat", "chieu", "dan.png")
            self.image = pygame.image.load(bullet_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (30, 15))  # Scale đạn cho phù hợp
        except Exception as e:
            print(f"Error loading bullet image: {e}")
            # Tạo hình ảnh giả nếu không load được
            self.image = pygame.Surface((30, 15))
            self.image.fill((255, 200, 0))
    
    def update(self):
        """Cập nhật vị trí viên đạn"""
        self.x += self.speed * self.direction
        
        # Kiểm tra viên đạn bay ra khỏi màn hình (giả sử map rộng 4800)
        if self.x < 0 or self.x > 4800:
            self.active = False
    
    def draw(self, surface, camera_x=0):
        """Vẽ viên đạn"""
        if self.active:
            draw_x = self.x - camera_x
            # Lật ảnh nếu bắn sang trái
            if self.direction == -1:
                img = pygame.transform.flip(self.image, True, False)
            else:
                img = self.image
            surface.blit(img, (draw_x, self.y))
    
    def get_rect(self):
        """Lấy rect để kiểm tra va chạm"""
        return pygame.Rect(self.x, self.y, 30, 15)
