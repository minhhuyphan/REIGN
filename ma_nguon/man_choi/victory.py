import pygame
import os
import sys
import time
import math
import random
from ma_nguon.core import high_scores

class VictoryScene:
    def __init__(self, game, level_name="Unknown", score=0, stats=None):
        self.game = game
        self.level_name = level_name
        self.score = score
        self.stats = stats or {}
        
        # Save score to leaderboard
        try:
            user = getattr(self.game, 'current_user', None) or 'Guest'
            key = level_name.replace(' ', '_').lower()
            high_scores.add_score(key, user, int(score))
        except Exception:
            pass
        
        # Fonts
        self.title_font = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 90)
        self.button_font = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 40)
        self.info_font = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 30)
        self.small_font = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 24)
        
        # Button selection
        self.selected = 0
        self.buttons = ["Màn tiếp theo", "Chơi lại", "Về Menu"]
        
        # Colors
        self.title_color = (255, 215, 0)  # Gold
        self.button_normal = (200, 200, 200)
        self.button_selected = (255, 215, 0)
        self.button_hover_bg = (80, 120, 80)
        
        self.start_time = pygame.time.get_ticks()
        self.auto_continue_duration = 10000  # 10 giây tự động chuyển
        
        # Load âm thanh chiến thắng
        try:
            self.victory_sound = pygame.mixer.Sound("tai_nguyen/am_thanh/hieu_ung/da.mp3")
            self.victory_sound.play()
        except:
            pass
        
        # Animation
        self.fade_alpha = 0
        self.fade_speed = 5
        self.title_scale = 0.5
        self.title_scale_speed = 0.03
        self.bounce_offset = 0
        self.bounce_speed = 0.1
        self.particle_timer = 0
        
        # Fireworks/Stars particles
        self.stars = []
        screen_size = pygame.display.get_surface().get_size()
        for i in range(80):
            self.stars.append({
                'x': random.randint(0, screen_size[0]),
                'y': random.randint(0, screen_size[1]),
                'vx': random.uniform(-2, 2),
                'vy': random.uniform(-3, -1),
                'size': random.randint(2, 6),
                'color': random.choice([
                    (255, 215, 0),   # Gold
                    (255, 255, 100), # Yellow
                    (255, 165, 0),   # Orange
                    (255, 100, 100), # Red
                    (100, 255, 100), # Green
                ]),
                'life': random.randint(100, 200),
                'max_life': 200
            })

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.buttons)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.buttons)
            elif event.key == pygame.K_RETURN:
                self.execute_button_action()
            elif event.key == pygame.K_ESCAPE:
                self.game.change_scene("menu")
    
    def execute_button_action(self):
        """Thực hiện hành động của button được chọn"""
        if self.selected == 0:  # Màn tiếp theo
            self.next_level()
        elif self.selected == 1:  # Chơi lại
            self.restart_level()
        elif self.selected == 2:  # Về Menu
            self.game.change_scene("menu")
    
    def next_level(self):
        """Chuyển sang màn tiếp theo"""
        # Logic chuyển màn - có thể customize dựa vào level hiện tại
        if hasattr(self.game, 'target_level'):
            current_level = self.game.target_level
            
            # Map progression logic
            level_progression = {
                'level1': 'level2',
                'map_mua_thu_man1': 'map_mua_thu_man2',
                'map_mua_thu_man2': 'map_mua_thu_man3',
                'map_ninja_man1': 'map_ninja_man2',
            }
            
            next_level = level_progression.get(current_level, None)
            
            if next_level:
                self.game.target_level = next_level
                self.game.change_scene(next_level)
            else:
                # Không có màn tiếp theo, về menu
                self.game.change_scene("menu")
        else:
            self.game.change_scene("menu")
    
    def restart_level(self):
        """Chơi lại màn hiện tại"""
        if hasattr(self.game, 'selected_player') and self.game.selected_player:
            player = self.game.selected_player
            # Reset player stats
            max_hp = player.get_max_hp_with_equipment() if hasattr(player, 'get_max_hp_with_equipment') else player.max_hp
            player.hp = max_hp
            player.x = 100
            player.y = 300
            player.base_y = 300
            
        # Restart current level
        if hasattr(self.game, 'target_level') and self.game.target_level:
            self.game.change_scene(self.game.target_level)
        else:
            self.game.change_scene("chon_map")

    def update(self):
        # Fade in animation
        if self.fade_alpha < 255:
            self.fade_alpha = min(255, self.fade_alpha + self.fade_speed)
        
        # Title scale animation
        if self.title_scale < 1.0:
            self.title_scale = min(1.0, self.title_scale + self.title_scale_speed)
        
        # Bounce animation
        self.bounce_offset = 5 * math.sin(pygame.time.get_ticks() * self.bounce_speed / 100)
        
        # Update particles
        screen_size = pygame.display.get_surface().get_size()
        for star in self.stars:
            star['x'] += star['vx']
            star['y'] += star['vy']
            star['vy'] += 0.1  # Gravity
            star['life'] -= 1
            
            # Respawn particle if dead
            if star['life'] <= 0:
                star['x'] = random.randint(0, screen_size[0])
                star['y'] = screen_size[1]
                star['vx'] = random.uniform(-2, 2)
                star['vy'] = random.uniform(-3, -1)
                star['life'] = star['max_life']
        
        # Auto continue after duration (optional)
        # now = pygame.time.get_ticks()
        # if now - self.start_time > self.auto_continue_duration:
        #     self.next_level()

    def draw(self, screen):
        # Gradient background - victory theme (green/gold)
        self._draw_gradient_background(screen)
        
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        
        # Draw particles first (background layer)
        self._draw_particles(screen)
        
        # Calculate layout positions
        title_y = 70
        info_y = 200
        stats_y = 280
        leaderboard_y = 420
        buttons_y = screen_height - 280
        
        # ===== VICTORY TITLE =====
        title_surface = self.title_font.render("CHIẾN THẮNG!", True, self.title_color)
        scaled_width = int(title_surface.get_width() * self.title_scale)
        scaled_height = int(title_surface.get_height() * self.title_scale)
        title_scaled = pygame.transform.scale(title_surface, (scaled_width, scaled_height))
        
        # Title shadow
        shadow_offset = 5
        shadow_surface = self.title_font.render("CHIẾN THẮNG!", True, (50, 50, 0))
        shadow_scaled = pygame.transform.scale(shadow_surface, (scaled_width, scaled_height))
        screen.blit(shadow_scaled, (screen_width // 2 - scaled_width // 2 + shadow_offset, 
                                    title_y + shadow_offset))
        # Title main with glow
        screen.blit(title_scaled, (screen_width // 2 - scaled_width // 2, title_y))
        
        # Title glow effect
        glow_surf = pygame.Surface((scaled_width + 20, scaled_height + 20), pygame.SRCALPHA)
        glow_color = (255, 215, 0, 30)
        for i in range(3):
            offset = (3 - i) * 5
            pygame.draw.rect(glow_surf, glow_color, 
                           (offset, offset, scaled_width + 20 - offset * 2, scaled_height + 20 - offset * 2), 
                           border_radius=20)
        screen.blit(glow_surf, (screen_width // 2 - scaled_width // 2 - 10, title_y - 10))
        
        # ===== LEVEL AND SCORE PANEL =====
        panel_width = 500
        panel_height = 60
        panel_x = screen_width // 2 - panel_width // 2
        panel_y = info_y
        
        # Panel background
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        pygame.draw.rect(panel_surface, (40, 80, 40, 200), (0, 0, panel_width, panel_height), border_radius=15)
        pygame.draw.rect(panel_surface, (100, 200, 100, 150), (0, 0, panel_width, panel_height), 3, border_radius=15)
        screen.blit(panel_surface, (panel_x, panel_y))
        
        # Level and Score
        level_text = self.info_font.render(f"🎮 {self.level_name}", True, (255, 255, 255))
        score_text = self.info_font.render(f"⭐ {self.score}", True, (255, 215, 0))
        
        screen.blit(level_text, (panel_x + 30, panel_y + 15))
        screen.blit(score_text, (panel_x + panel_width - score_text.get_width() - 30, panel_y + 15))
        
        # ===== STATS PANEL (if available) =====
        if self.stats:
            stats_panel_width = 500
            stats_panel_height = 100
            stats_panel_x = screen_width // 2 - stats_panel_width // 2
            stats_panel_y = stats_y
            
            # Panel background
            stats_surf = pygame.Surface((stats_panel_width, stats_panel_height), pygame.SRCALPHA)
            pygame.draw.rect(stats_surf, (50, 50, 80, 200), (0, 0, stats_panel_width, stats_panel_height), border_radius=15)
            pygame.draw.rect(stats_surf, (150, 150, 200, 100), (0, 0, stats_panel_width, stats_panel_height), 2, border_radius=15)
            screen.blit(stats_surf, (stats_panel_x, stats_panel_y))
            
            # Stats title
            stats_title = self.info_font.render("📊 Thống kê", True, (200, 200, 255))
            screen.blit(stats_title, (stats_panel_x + stats_panel_width // 2 - stats_title.get_width() // 2, stats_panel_y + 10))
            
            # Stats details
            stat_y = stats_panel_y + 50
            stats_text = []
            if 'enemies_defeated' in self.stats:
                stats_text.append(f"Tiêu diệt: {self.stats['enemies_defeated']}")
            if 'time' in self.stats:
                stats_text.append(f"Thời gian: {self.stats['time']:.1f}s")
            if 'accuracy' in self.stats:
                stats_text.append(f"Độ chính xác: {self.stats['accuracy']:.0f}%")
            
            for i, text in enumerate(stats_text[:3]):  # Max 3 stats
                stat_surf = self.small_font.render(text, True, (200, 200, 200))
                x = stats_panel_x + 40 + i * 150
                screen.blit(stat_surf, (x, stat_y))
        
        # ===== LEADERBOARD (compact) =====
        try:
            key = self.level_name.replace(' ', '_').lower()
            top = high_scores.get_top_scores(key, 3)  # Only top 3 for victory screen
            
            if top:
                lb_width = 400
                lb_height = 120
                lb_x = screen_width // 2 - lb_width // 2
                lb_y = leaderboard_y
                
                # Panel
                lb_surf = pygame.Surface((lb_width, lb_height), pygame.SRCALPHA)
                pygame.draw.rect(lb_surf, (30, 30, 50, 220), (0, 0, lb_width, lb_height), border_radius=15)
                pygame.draw.rect(lb_surf, (150, 150, 200, 80), (0, 0, lb_width, lb_height), 2, border_radius=15)
                screen.blit(lb_surf, (lb_x, lb_y))
                
                # Title
                lb_title = self.small_font.render("🏆 Top 3", True, (255, 215, 0))
                screen.blit(lb_title, (lb_x + lb_width // 2 - lb_title.get_width() // 2, lb_y + 8))
                
                # Entries
                for i, e in enumerate(top):
                    rank_color = [(255, 215, 0), (192, 192, 192), (205, 127, 50)][i]
                    txt = f"{i+1}. {e.get('user','Guest')[:10]}"
                    score_str = f"{e.get('score',0)}"
                    
                    txt_s = self.small_font.render(txt, True, rank_color)
                    score_s = self.small_font.render(score_str, True, (200, 255, 200))
                    
                    entry_y = lb_y + 40 + i * 25
                    screen.blit(txt_s, (lb_x + 30, entry_y))
                    screen.blit(score_s, (lb_x + lb_width - score_s.get_width() - 30, entry_y))
        except Exception:
            pass
        
        # ===== BUTTONS =====
        button_spacing = 65
        
        for i, button_text in enumerate(self.buttons):
            button_y = buttons_y + i * button_spacing
            if i == self.selected:
                button_y += self.bounce_offset
            
            # Button style
            button_width = 350
            button_height = 50
            button_x = screen_width // 2 - button_width // 2
            
            if i == self.selected:
                # Selected - green theme for victory
                button_surf = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
                pygame.draw.rect(button_surf, (80, 150, 80, 230), (0, 0, button_width, button_height), border_radius=12)
                pygame.draw.rect(button_surf, self.button_selected, (0, 0, button_width, button_height), 4, border_radius=12)
                screen.blit(button_surf, (button_x, button_y))
                
                # Glow
                glow_surf = pygame.Surface((button_width + 10, button_height + 10), pygame.SRCALPHA)
                pygame.draw.rect(glow_surf, (255, 215, 0, 50), (0, 0, button_width + 10, button_height + 10), border_radius=15)
                screen.blit(glow_surf, (button_x - 5, button_y - 5))
            else:
                button_surf = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
                pygame.draw.rect(button_surf, (50, 70, 50, 180), (0, 0, button_width, button_height), border_radius=12)
                pygame.draw.rect(button_surf, (100, 150, 100, 150), (0, 0, button_width, button_height), 2, border_radius=12)
                screen.blit(button_surf, (button_x, button_y))
            
            # Button text
            color = self.button_selected if i == self.selected else self.button_normal
            text_surf = self.button_font.render(button_text, True, color)
            text_x = screen_width // 2 - text_surf.get_width() // 2
            text_y = button_y + (button_height - text_surf.get_height()) // 2
            screen.blit(text_surf, (text_x, text_y))
        
        # ===== INSTRUCTIONS =====
        instruction_text = self.small_font.render("↑↓ Di chuyển | Enter Chọn | ESC Menu", True, (180, 180, 180))
        screen.blit(instruction_text, (screen_width // 2 - instruction_text.get_width() // 2, screen_height - 40))
        
        # Decorations
        self._draw_decorations(screen)
    
    def _draw_gradient_background(self, screen):
        """Draw victory gradient background - green/gold theme"""
        width = screen.get_width()
        height = screen.get_height()
        
        for y in range(height):
            progress = y / height
            r = int(10 + (30 - 10) * progress)
            g = int(30 + (50 - 30) * progress)
            b = int(20 + (30 - 20) * progress)
            pygame.draw.line(screen, (r, g, b), (0, y), (width, y))
    
    def _draw_particles(self, screen):
        """Draw victory particles/fireworks"""
        for star in self.stars:
            if 0 <= star['x'] < screen.get_width() and 0 <= star['y'] < screen.get_height():
                alpha = int(255 * (star['life'] / star['max_life']))
                color = (*star['color'][:3], alpha)
                
                # Draw star
                surf = pygame.Surface((star['size'] * 2, star['size'] * 2), pygame.SRCALPHA)
                pygame.draw.circle(surf, color, (star['size'], star['size']), star['size'])
                screen.blit(surf, (int(star['x']) - star['size'], int(star['y']) - star['size']))
    
    def _draw_decorations(self, screen):
        """Draw decorative elements"""
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        
        time_ms = pygame.time.get_ticks()
        
        # Animated corners - victory theme (green/gold)
        corner_length = 80
        corner_thickness = 4
        glow_intensity = int(100 + 100 * math.sin(time_ms * 0.003))
        glow_color = (100, 255, glow_intensity)
        
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