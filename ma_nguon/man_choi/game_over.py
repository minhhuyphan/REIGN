import pygame
import sys
import math
from ma_nguon.core import high_scores

class GameOverScene:
    def __init__(self, game, level_name="Unknown", score=0):
        self.game = game
        self.level_name = level_name
        self.score = score
        # Save score to leaderboard (non-fatal)
        try:
            user = getattr(self.game, 'current_user', None) or 'Guest'
            key = level_name.replace(' ', '_').lower()
            high_scores.add_score(key, user, int(score))
        except Exception:
            pass
        
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
        # Dark gradient background
        self._draw_gradient_background(screen)
        
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        
        # Calculate layout positions to avoid overlap
        title_y = 80
        info_y = 200
        leaderboard_y = 280
        buttons_y = screen_height - 300
        
        # ===== GAME OVER TITLE =====
        title_surface = self.title_font.render("GAME OVER", True, self.title_color)
        scaled_width = int(title_surface.get_width() * self.title_scale)
        scaled_height = int(title_surface.get_height() * self.title_scale)
        title_scaled = pygame.transform.scale(title_surface, (scaled_width, scaled_height))
        
        # Title shadow
        shadow_offset = 4
        shadow_surface = self.title_font.render("GAME OVER", True, (50, 0, 0))
        shadow_scaled = pygame.transform.scale(shadow_surface, (scaled_width, scaled_height))
        screen.blit(shadow_scaled, (screen_width // 2 - scaled_width // 2 + shadow_offset, 
                                    title_y + shadow_offset))
        # Title main
        screen.blit(title_scaled, (screen_width // 2 - scaled_width // 2, title_y))
        
        # ===== LEVEL AND SCORE INFO PANEL =====
        panel_width = 500
        panel_height = 60
        panel_x = screen_width // 2 - panel_width // 2
        panel_y = info_y
        
        # Panel background
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        pygame.draw.rect(panel_surface, (40, 40, 60, 200), (0, 0, panel_width, panel_height), border_radius=15)
        pygame.draw.rect(panel_surface, (100, 100, 150, 150), (0, 0, panel_width, panel_height), 3, border_radius=15)
        screen.blit(panel_surface, (panel_x, panel_y))
        
        # Level and Score text side by side
        level_text = self.info_font.render(f"Màn: {self.level_name}", True, (255, 255, 255))
        score_text = self.info_font.render(f"Điểm: {self.score}", True, (255, 215, 0))
        
        screen.blit(level_text, (panel_x + 30, panel_y + 15))
        screen.blit(score_text, (panel_x + panel_width - score_text.get_width() - 30, panel_y + 15))

        # ===== LEADERBOARD PANEL =====
        try:
            key = self.level_name.replace(' ', '_').lower()
            top = high_scores.get_top_scores(key, 5)
            
            # Leaderboard panel
            lb_panel_width = 400
            lb_panel_height = 200
            lb_panel_x = screen_width // 2 - lb_panel_width // 2
            lb_panel_y = leaderboard_y
            
            # Panel background
            lb_surface = pygame.Surface((lb_panel_width, lb_panel_height), pygame.SRCALPHA)
            pygame.draw.rect(lb_surface, (30, 30, 50, 220), (0, 0, lb_panel_width, lb_panel_height), border_radius=15)
            pygame.draw.rect(lb_surface, (150, 150, 200, 100), (0, 0, lb_panel_width, lb_panel_height), 2, border_radius=15)
            screen.blit(lb_surface, (lb_panel_x, lb_panel_y))
            
            # Leaderboard title
            lb_title = self.info_font.render("🏆 BẢNG XẾP HẠNG", True, (255, 215, 0))
            screen.blit(lb_title, (lb_panel_x + lb_panel_width // 2 - lb_title.get_width() // 2, lb_panel_y + 10))
            
            # Leaderboard entries
            entry_font = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 24)
            for i, e in enumerate(top):
                rank_color = [(255, 215, 0), (192, 192, 192), (205, 127, 50), (200, 200, 200), (200, 200, 200)][i]
                txt = f"{i+1}. {e.get('user','Guest')[:12]}"
                score_str = f"{e.get('score',0)}"
                
                txt_s = entry_font.render(txt, True, rank_color)
                score_s = entry_font.render(score_str, True, (200, 255, 200))
                
                entry_y = lb_panel_y + 50 + i * 28
                screen.blit(txt_s, (lb_panel_x + 30, entry_y))
                screen.blit(score_s, (lb_panel_x + lb_panel_width - score_s.get_width() - 30, entry_y))
        except Exception as e:
            pass
        
        # ===== BUTTONS =====
        button_spacing = 70
        
        for i, button_text in enumerate(self.buttons):
            # Calculate button position with bounce effect
            button_y = buttons_y + i * button_spacing
            if i == self.selected:
                button_y += self.bounce_offset
            
            # Button background with modern style
            button_width = 350
            button_height = 55
            button_x = screen_width // 2 - button_width // 2
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            
            if i == self.selected:
                # Selected button - gradient effect
                button_surf = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
                pygame.draw.rect(button_surf, (80, 80, 120, 230), (0, 0, button_width, button_height), border_radius=12)
                pygame.draw.rect(button_surf, self.button_selected, (0, 0, button_width, button_height), 4, border_radius=12)
                screen.blit(button_surf, (button_x, button_y))
                
                # Glow effect
                glow_surf = pygame.Surface((button_width + 10, button_height + 10), pygame.SRCALPHA)
                pygame.draw.rect(glow_surf, (255, 215, 0, 50), (0, 0, button_width + 10, button_height + 10), border_radius=15)
                screen.blit(glow_surf, (button_x - 5, button_y - 5))
            else:
                # Normal button
                button_surf = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
                pygame.draw.rect(button_surf, (50, 50, 70, 180), (0, 0, button_width, button_height), border_radius=12)
                pygame.draw.rect(button_surf, (100, 100, 130, 150), (0, 0, button_width, button_height), 2, border_radius=12)
                screen.blit(button_surf, (button_x, button_y))
            
            # Button text centered
            color = self.button_selected if i == self.selected else self.button_normal
            button_surface = self.button_font.render(button_text, True, color)
            text_x = screen_width // 2 - button_surface.get_width() // 2
            text_y = button_y + (button_height - button_surface.get_height()) // 2
            screen.blit(button_surface, (text_x, text_y))
        
        # ===== INSTRUCTIONS =====
        instruction_text = self.info_font.render("↑↓ Di chuyển | Enter Chọn | ESC Menu", True, (180, 180, 180))
        instruction_x = screen_width // 2 - instruction_text.get_width() // 2
        instruction_y = screen_height - 50
        screen.blit(instruction_text, (instruction_x, instruction_y))
        
        # Optional decorations
        self.draw_decorations(screen)
    
    def _draw_gradient_background(self, screen):
        """Draw a dark gradient background"""
        width = screen.get_width()
        height = screen.get_height()
        
        for y in range(height):
            progress = y / height
            r = int(15 + (25 - 15) * progress)
            g = int(15 + (20 - 15) * progress)
            b = int(30 + (40 - 30) * progress)
            pygame.draw.line(screen, (r, g, b), (0, y), (width, y))
    
    def draw_decorations(self, screen):
        """Draw decorative elements to make the screen more appealing"""
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        
        time_ms = pygame.time.get_ticks()
        
        # Animated particles floating around
        import random
        random.seed(42)  # Fixed seed for consistent particle positions
        
        for i in range(30):
            x = random.randint(0, screen_width)
            base_y = random.randint(0, screen_height)
            # Floating animation
            y = base_y + 10 * math.sin(time_ms * 0.001 + i * 0.5)
            
            size = random.randint(2, 5)
            alpha = int(100 + 100 * math.sin(time_ms * 0.002 + i))
            alpha = max(50, min(200, alpha))
            
            particle_surf = pygame.Surface((size, size), pygame.SRCALPHA)
            color = random.choice([
                (255, 100, 100, alpha),  # Red
                (100, 100, 255, alpha),  # Blue
                (200, 200, 200, alpha)   # White
            ])
            pygame.draw.circle(particle_surf, color, (size // 2, size // 2), size // 2)
            screen.blit(particle_surf, (x, y))
        
        # Modern corner decorations
        corner_length = 80
        corner_thickness = 4
        corner_color = (255, 100, 100)
        
        # Animated glow
        glow_intensity = int(50 + 50 * math.sin(time_ms * 0.003))
        glow_color = (255, glow_intensity, glow_intensity)
        
        # Top-left
        pygame.draw.line(screen, glow_color, (30, 30), (30 + corner_length, 30), corner_thickness)
        pygame.draw.line(screen, glow_color, (30, 30), (30, 30 + corner_length), corner_thickness)
        
        # Top-right
        pygame.draw.line(screen, glow_color, (screen_width - 30, 30), 
                        (screen_width - 30 - corner_length, 30), corner_thickness)
        pygame.draw.line(screen, glow_color, (screen_width - 30, 30), 
                        (screen_width - 30, 30 + corner_length), corner_thickness)
        
        # Bottom-left
        pygame.draw.line(screen, glow_color, (30, screen_height - 30), 
                        (30 + corner_length, screen_height - 30), corner_thickness)
        pygame.draw.line(screen, glow_color, (30, screen_height - 30), 
                        (30, screen_height - 30 - corner_length), corner_thickness)
        
        # Bottom-right
        pygame.draw.line(screen, glow_color, (screen_width - 30, screen_height - 30), 
                        (screen_width - 30 - corner_length, screen_height - 30), corner_thickness)
        pygame.draw.line(screen, glow_color, (screen_width - 30, screen_height - 30), 
                        (screen_width - 30, screen_height - 30 - corner_length), corner_thickness)
        
        # Subtle border frame
        border_rect = pygame.Rect(20, 20, screen_width - 40, screen_height - 40)
        pygame.draw.rect(screen, (80, 80, 100, 100), border_rect, 2, border_radius=10)