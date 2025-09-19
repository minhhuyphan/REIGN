import pygame
import os
import sys
import time
import math

class VictoryScene:
    def __init__(self, game):
        self.game = game
        self.font_large = pygame.font.Font(None, 80)
        self.font_medium = pygame.font.Font(None, 50)
        self.font_small = pygame.font.Font(None, 30)
        self.start_time = pygame.time.get_ticks()
        self.duration = 5000  # Hiển thị màn hình chiến thắng trong 5 giây
        
        # Load âm thanh chiến thắng nếu có
        try:
            self.victory_sound = pygame.mixer.Sound("tai_nguyen/am_thanh/hieu_ung/da.mp3")
            self.victory_sound.play()
        except:
            self.victory_sound = None
            print("Không load được âm thanh chiến thắng")
        
        # Animation hiệu ứng
        self.animation_frame = 0
        self.animation_tick = 0
        self.stars = []
        for i in range(50):
            self.stars.append({
                'x': pygame.math.Vector2(pygame.math.Vector2(pygame.display.get_surface().get_size()) * pygame.math.Vector2(pygame.math.Vector2(pygame.math.Vector2(pygame.math.Vector2(pygame.math.Vector2.random()).normalize()))) * pygame.math.Vector2(pygame.math.Vector2(pygame.display.get_surface().get_size()).length() / 2)),
                'speed': 2 + pygame.math.Vector2.random().x * 3,
                'angle': pygame.math.Vector2.random().x * 360,
                'size': 3 + pygame.math.Vector2.random().x * 5,
                'color': (200 + pygame.math.Vector2.random().x * 55, 
                          200 + pygame.math.Vector2.random().x * 55, 
                          100 + pygame.math.Vector2.random().x * 155)
            })

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                self.game.change_scene("menu")

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.start_time > self.duration:
            self.game.change_scene("menu")
        
        # Cập nhật hiệu ứng
        self.animation_tick += 1
        if self.animation_tick % 5 == 0:
            self.animation_frame = (self.animation_frame + 1) % 60
        
        # Di chuyển các ngôi sao
        for star in self.stars:
            star['angle'] += 1
            if star['angle'] >= 360:
                star['angle'] = 0
            
            center = pygame.math.Vector2(self.game.WIDTH // 2, self.game.HEIGHT // 2)
            direction = pygame.math.Vector2(star['x']) - center
            direction.normalize_ip()
            star['x'].x += direction.x * star['speed']
            star['x'].y += direction.y * star['speed']
            
            # Nếu sao ra khỏi màn hình, tạo lại ở giữa
            if (star['x'].x < 0 or star['x'].x > self.game.WIDTH or 
                star['x'].y < 0 or star['x'].y > self.game.HEIGHT):
                star['x'] = pygame.math.Vector2(self.game.WIDTH // 2, self.game.HEIGHT // 2)

    def draw(self, screen):
        # Vẽ màu nền gradient
        for y in range(0, self.game.HEIGHT, 2):
            progress = y / self.game.HEIGHT
            color = (int(20 + 20 * progress), 
                    int(20 + 50 * progress), 
                    int(50 + 150 * progress))
            pygame.draw.line(screen, color, (0, y), (self.game.WIDTH, y), 2)
        
        # Vẽ các ngôi sao
        for star in self.stars:
            pygame.draw.circle(screen, star['color'], 
                              (int(star['x'].x), int(star['x'].y)), 
                              int(star['size'] + math.sin(self.animation_frame / 10) * 2))
        
        # Vẽ thông báo chiến thắng
        title = self.font_large.render("CHIẾN THẮNG!", True, (255, 255, 0))
        screen.blit(title, (self.game.WIDTH//2 - title.get_width()//2, 
                          self.game.HEIGHT//2 - 100 + math.sin(self.animation_frame / 10) * 5))
        
        # Vẽ thông tin phụ
        subtitle = self.font_medium.render("Bạn đã đánh bại tất cả kẻ địch!", True, (255, 200, 100))
        screen.blit(subtitle, (self.game.WIDTH//2 - subtitle.get_width()//2, self.game.HEIGHT//2))
        
        # Vẽ hướng dẫn
        if self.animation_frame % 40 < 20:  # Nhấp nháy
            guide = self.font_small.render("Nhấn ENTER hoặc ESC để trở về menu", True, (200, 200, 200))
            screen.blit(guide, (self.game.WIDTH//2 - guide.get_width()//2, self.game.HEIGHT - 100))