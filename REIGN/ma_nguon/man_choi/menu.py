import pygame
import math

class MenuScene:
    def __init__(self, game):
        self.game = game  # Tham chiếu đến GameManager hoặc SceneManager
        self.font = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 50)
        self.selected = 0
        self.options = ["Màn 1", "Màn 2", "Hướng dẫn", "Cài đặt", "Thoát"]
        
        # Animation variables
        self.bounce_offset = 0
        self.bounce_speed = 0.1
        self.title_scale = 0.5
        self.title_scale_speed = 0.02
        
        # Load background image
        try:
            self.background = pygame.image.load("Tai_nguyen/hinh_anh/giao_dien/bg.png")
            self.background = pygame.transform.scale(self.background, (1600, 700))  # Scale to screen size
        except pygame.error:
            # Fallback to a background from canh_nen if bg.png doesn't work
            try:
                self.background = pygame.image.load("Tai_nguyen/hinh_anh/canh_nen/trang_sao.png")
                self.background = pygame.transform.scale(self.background, (1600, 700))
            except pygame.error:
                self.background = None  # No background if both fail

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                if self.selected == 0:
                    # Lưu thông tin là chọn Màn 1
                    self.game.target_level = "level1"
                    self.game.change_scene("character_select")
                elif self.selected == 1:
                    # Lưu thông tin là chọn Màn 2
                    self.game.target_level = "level2"
                    self.game.change_scene("character_select")
                elif self.selected == 2:
                    # Chuyển đến menu chọn màn mùa thu
                    self.game.change_scene("autumn_levels")
                elif self.selected == 3:
                    self.game.change_scene("settings")
                elif self.selected == 4
                    self.game.change_scene("help")
                elif self.selected == 5
                    self.game.running = False

    def update(self):
        # Title scale animation
        if self.title_scale < 1.0:
            self.title_scale = min(1.0, self.title_scale + self.title_scale_speed)
        
        # Bounce animation for selected button
        self.bounce_offset = 5 * math.sin(pygame.time.get_ticks() * self.bounce_speed / 100)

    def draw(self, screen):
        # Draw background image if available, otherwise fill with solid color
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill((30, 30, 60))
        
        # Title with scaling animation and royal gold color
        title_color = (255, 215, 0)  # Gold color for royal theme
        shadow_color = (139, 69, 19)  # Dark brown shadow
        
        # Create title with scaling animation
        title_surface = self.font.render("GAME PYGAME", True, title_color)
        scaled_width = int(title_surface.get_width() * self.title_scale)
        scaled_height = int(title_surface.get_height() * self.title_scale)
        title_scaled = pygame.transform.scale(title_surface, (scaled_width, scaled_height))
        
        # Create shadow with same scaling
        title_shadow_surface = self.font.render("GAME PYGAME", True, shadow_color)
        shadow_scaled_width = int(title_shadow_surface.get_width() * self.title_scale)
        shadow_scaled_height = int(title_shadow_surface.get_height() * self.title_scale)
        shadow_scaled = pygame.transform.scale(title_shadow_surface, (shadow_scaled_width, shadow_scaled_height))
        
        # Draw title shadow first
        shadow_x = screen.get_width()//2 - shadow_scaled.get_width()//2 + 3
        shadow_y = 103
        screen.blit(shadow_scaled, (shadow_x, shadow_y))
        
        # Draw main title
        title_x = screen.get_width()//2 - title_scaled.get_width()//2
        title_y = 100
        screen.blit(title_scaled, (title_x, title_y))
        
        # Menu options with medieval-themed colors and bounce effect
        for i, text in enumerate(self.options):
            # Calculate base position
            base_y = 250 + i*70
            option_y = base_y
            
            if i == self.selected:
                # Selected option - bright orange/amber with bounce effect
                color = (255, 140, 0)  # Bright amber
                option_y += self.bounce_offset  # Add bounce animation
                
                # Add background rectangle for selected option
                option_surface = self.font.render(text, True, color)
                bg_rect = pygame.Rect(0, 0, option_surface.get_width() + 40, option_surface.get_height() + 20)
                bg_rect.center = (screen.get_width()//2, option_y + option_surface.get_height()//2)
                pygame.draw.rect(screen, (80, 80, 100), bg_rect, border_radius=10)
                pygame.draw.rect(screen, color, bg_rect, 3, border_radius=10)
                
                # Add glow effect for selected option
                glow_color = (255, 215, 0)  # Gold glow
                glow_option = self.font.render(text, True, glow_color)
                screen.blit(glow_option, (screen.get_width()//2 - glow_option.get_width()//2 + 1, option_y + 1))
                screen.blit(glow_option, (screen.get_width()//2 - glow_option.get_width()//2 - 1, option_y - 1))
            else:
                # Unselected options - light cream/beige
                color = (245, 245, 220)  # Light beige
            
            option = self.font.render(text, True, color)
            screen.blit(option, (screen.get_width()//2 - option.get_width()//2, option_y))