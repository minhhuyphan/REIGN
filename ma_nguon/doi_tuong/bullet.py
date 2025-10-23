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
        """Lấy rect để kiểm tra va chạm.

        Trả về rect dựa trên kích thước của ảnh đạn (nếu có). Nếu image
        không tồn tại thì fallback về kích thước cố định 30x15 để đảm bảo
        tương thích với code hiện tại.
        """
        try:
            w, h = self.image.get_size()
            return pygame.Rect(self.x, self.y, w, h)
        except Exception:
            return pygame.Rect(self.x, self.y, 30, 15)


class ShurikenBullet(Bullet):
    """Projectile class cho Sasuke-like skill (phi tiêu)."""
    
    def __init__(self, x, y, direction, damage=30, owner=None):
        # Sử dụng super() để kế thừa đúng cách từ Bullet
        super().__init__(x, y, direction, damage, owner)
        
        # Override các thuộc tính riêng
        self.speed = 8  # Giảm tốc độ để dễ nhìn thấy
        self.is_sasuke_skill = True
        self.rotation = 0
        
        # Load ảnh phi tiêu thay thế ảnh đạn mặc định
        self._load_shuriken_image()
    
    def _load_shuriken_image(self):
        """Load ảnh phi tiêu"""
        shuriken_loaded = False
        try:
            # Thử load từ thư mục phi tiêu
            shuriken_paths = [
                os.path.join("Tai_nguyen", "hinh_anh", "nhan_vat", "ninja", "phitieu", "phitieu.png"),
                os.path.join("Tai_nguyen", "hinh_anh", "nhan_vat", "ninja", "phitieu.png"),
                os.path.join("Tai_nguyen", "hinh_anh", "nhan_vat", "ninja", "nem_phi_tieu", "phitieu.png")
            ]
            for path in shuriken_paths:
                if os.path.exists(path):
                    print(f"[SHURIKEN] Loading phi tiêu from: {path}")
                    img = pygame.image.load(path).convert_alpha()
                    # Scale to a bigger size
                    self.image = pygame.transform.scale(img, (70, 70))
                    shuriken_loaded = True
                    print(f"[SHURIKEN] Successfully loaded phi tiêu image!")
                    break
        except Exception as e:
            print(f"[SHURIKEN] Error loading shuriken image: {e}")
            
        # Nếu không load được ảnh, tạo phi tiêu fallback đẹp
        if not shuriken_loaded:
            print("[SHURIKEN] Creating fallback shuriken image")
            self.image = pygame.Surface((70, 70), pygame.SRCALPHA)
            # Tạo phi tiêu đẹp với màu kim loại
            center = (35, 35)
            pygame.draw.circle(self.image, (192, 192, 192), center, 33)  # Bạc
            pygame.draw.circle(self.image, (160, 160, 160), center, 30)  # Xám đậm
            # Vẽ 4 cánh phi tiêu
            points = [(35, 2), (68, 35), (35, 68), (2, 35)]
            pygame.draw.polygon(self.image, (220, 220, 220), points)
            pygame.draw.polygon(self.image, (128, 128, 128), points, 2)

    def update(self):
        """Cập nhật vị trí phi tiêu"""
        self.x += self.speed * self.direction
        
        # Xoay phi tiêu nhẹ để thấy chuyển động nhưng không quá nhanh
        self.rotation += 10 * self.direction
        if self.rotation > 360:
            self.rotation -= 360
        elif self.rotation < -360:
            self.rotation += 360
        
        # Kiểm tra phi tiêu bay ra khỏi màn hình - giới hạn rộng hơn
        if self.x < -100 or self.x > 6000:
            self.active = False

    def draw(self, surface, camera_x=0):
        """Vẽ phi tiêu với hiệu ứng xoay"""
        if self.active:
            draw_x = self.x - camera_x
            
            # Xoay phi tiêu để tạo hiệu ứng bay
            rotated = pygame.transform.rotate(self.image, self.rotation)
            
            # Lật ảnh nếu bắn sang trái
            if self.direction == -1:
                rotated = pygame.transform.flip(rotated, True, False)
            
            # Tính vị trí center để xoay đúng
            rect = rotated.get_rect(center=(draw_x, self.y))
            surface.blit(rotated, rect.topleft)

    def get_rect(self):
        try:
            w, h = (self.image.get_size() if self.image else (24, 24))
            return pygame.Rect(self.x, self.y, w, h)
        except Exception:
            return super().get_rect()
