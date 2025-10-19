import pygame
import sys
import math

class GameOverScene:
    def __init__(self, game, level_name="Unknown", score=0):
        self.game = game
        self.level_name = level_name
        self.score = score
        
        # Fonts
        self.title_font = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 80)
        self.button_font = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 40)
        self.info_font = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 30)

        # Button selection
        self.selected = 0
        self.buttons = ["Chơi lại", "Về Menu", "Thoát game"]
        
        # Colors
        self.bg_color = (20, 20, 30)
        self.title_color = (255, 50, 50)  # Red for Game Over
        self.button_normal = (200, 200, 200)
        self.button_selected = (255, 215, 0)  # Gold
        self.button_hover_bg = (80, 80, 100)
        self.overlay_color = (0, 0, 0, 180)  # Semi-transparent overlay
        
        # Animation
        self.fade_alpha = 0
        self.fade_speed = 3
        self.title_scale = 0.5
        self.title_scale_speed = 0.02
        self.bounce_offset = 0
        self.bounce_speed = 0.1
        
        # Sound effects (if needed)
        try:
            # You can add game over sound here
            # pygame.mixer.Sound("tai_nguyen/am_thanh/game_over.wav").play()
            pass
        except:
            pass
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.buttons)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.buttons)
            elif event.key == pygame.K_RETURN:
                self.execute_button_action()
            elif event.key == pygame.K_ESCAPE:
                # ESC acts like "Về Menu"
                self.game.change_scene("menu")
    
    def execute_button_action(self):
        if self.selected == 0:  # Chơi lại
            self.restart_level()
        elif self.selected == 1:  # Về Menu
            self.game.change_scene("menu")
        elif self.selected == 2:  # Thoát game
            self.game.running = False
    
    def restart_level(self):
        """Restart the current level"""
        if hasattr(self.game, 'current_character') and self.game.current_character:
            # Reset player stats
            player = self.game.current_character
            player.hp = player.max_hp  # Full health
            player.x = 100  # Reset position
            player.y = 300
            player.base_y = 300
            
            # Restart the same level
            if self.level_name == "Level 1" or hasattr(self.game, 'target_level') and self.game.target_level == "level1":
                self.game.change_scene("level1")
            elif self.level_name == "Level 2" or hasattr(self.game, 'target_level') and self.game.target_level == "level2":
                self.game.change_scene("level2")
            elif self.level_name == "Map Mùa Thu" or hasattr(self.game, 'target_level') and self.game.target_level == "map_mua_thu":
                self.game.change_scene("map_mua_thu")
            elif "Mùa Thu - Màn 1" in self.level_name or hasattr(self.game, 'target_level') and self.game.target_level == "map_mua_thu_man1":
                self.game.change_scene("map_mua_thu_man1")
            elif "Mùa Thu - Màn 2" in self.level_name or hasattr(self.game, 'target_level') and self.game.target_level == "map_mua_thu_man2":
                self.game.change_scene("map_mua_thu_man2")
            elif "Mùa Thu - Màn 3" in self.level_name or hasattr(self.game, 'target_level') and self.game.target_level == "map_mua_thu_man3":
                self.game.change_scene("map_mua_thu_man3")
            else:
                # Default to level 1
                self.game.target_level = "level1"
                self.game.change_scene("level1")
        else:
            # No character selected, go to character select
            self.game.change_scene("character_select")
    
    def update(self):
        # Fade in animation
        if self.fade_alpha < 255:
            self.fade_alpha = min(255, self.fade_alpha + self.fade_speed)
        
        # Title scale animation
        if self.title_scale < 1.0:
            self.title_scale = min(1.0, self.title_scale + self.title_scale_speed)
        
        # Bounce animation for selected button
        self.bounce_offset = 5 * math.sin(pygame.time.get_ticks() * self.bounce_speed / 100)
    
    def draw(self, screen):
        # Semi-transparent overlay
        overlay = pygame.Surface(screen.get_size())
        overlay.set_alpha(self.fade_alpha)
        overlay.fill(self.overlay_color[:3])
        screen.blit(overlay, (0, 0))
        
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        
        # Game Over Title with scaling animation
        title_surface = self.title_font.render("GAME OVER", True, self.title_color)
        scaled_width = int(title_surface.get_width() * self.title_scale)
        scaled_height = int(title_surface.get_height() * self.title_scale)
        title_scaled = pygame.transform.scale(title_surface, (scaled_width, scaled_height))
        
        title_x = screen_width // 2 - title_scaled.get_width() // 2
        title_y = screen_height // 4
        screen.blit(title_scaled, (title_x, title_y))
        
        # Level and Score info
        level_text = self.info_font.render(f"Màn: {self.level_name}", True, (200, 200, 200))
        score_text = self.info_font.render(f"Điểm: {self.score}", True, (200, 200, 200))
        
        screen.blit(level_text, (screen_width // 2 - level_text.get_width() // 2, title_y + title_scaled.get_height() + 20))
        screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, title_y + title_scaled.get_height() + 60))
        
        # Buttons
        button_start_y = screen_height // 2 + 50
        button_spacing = 80
        
        for i, button_text in enumerate(self.buttons):
            # Calculate button position with bounce effect
            button_y = button_start_y + i * button_spacing
            if i == self.selected:
                button_y += self.bounce_offset
            
            # Button text
            color = self.button_selected if i == self.selected else self.button_normal
            button_surface = self.button_font.render(button_text, True, color)
            button_x = screen_width // 2 - button_surface.get_width() // 2
            
            # Button background for selected button (aligned with text)
            if i == self.selected:
                button_bg_rect = pygame.Rect(0, 0, 300, 60)
                button_bg_rect.center = (screen_width // 2, button_y + button_surface.get_height() // 2)
                pygame.draw.rect(screen, self.button_hover_bg, button_bg_rect, border_radius=10)
                pygame.draw.rect(screen, self.button_selected, button_bg_rect, 3, border_radius=10)
            
            # Draw button text
            screen.blit(button_surface, (button_x, button_y))
        
        # Instructions
        instruction_text = self.info_font.render("↑↓ Di chuyển | Enter Chọn | ESC Về Menu", True, (150, 150, 150))
        instruction_x = screen_width // 2 - instruction_text.get_width() // 2
        instruction_y = screen_height - 80
        screen.blit(instruction_text, (instruction_x, instruction_y))
        
        # Optional: Add some decorative elements
        self.draw_decorations(screen)
    
    def draw_decorations(self, screen):
        """Draw some decorative elements to make the screen more appealing"""
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        
        # Draw some fading particles or effects
        time_ms = pygame.time.get_ticks()
        
        # Animated border
        border_color = (100 + 50 * math.sin(time_ms * 0.003), 50, 50)
        pygame.draw.rect(screen, border_color, (10, 10, screen_width - 20, screen_height - 20), 5)
        
        # Corner decorations
        corner_size = 50
        corner_color = (255, 100, 100, 100)
        
        # Top-left corner
        pygame.draw.lines(screen, corner_color[:3], False, 
                         [(20, 60), (20, 20), (60, 20)], 3)
        
        # Top-right corner  
        pygame.draw.lines(screen, corner_color[:3], False,
                         [(screen_width - 60, 20), (screen_width - 20, 20), (screen_width - 20, 60)], 3)
        
        # Bottom-left corner
        pygame.draw.lines(screen, corner_color[:3], False,
                         [(20, screen_height - 60), (20, screen_height - 20), (60, screen_height - 20)], 3)
        
        # Bottom-right corner
        pygame.draw.lines(screen, corner_color[:3], False,
                         [(screen_width - 60, screen_height - 20), (screen_width - 20, screen_height - 20), 
                          (screen_width - 20, screen_height - 60)], 3)