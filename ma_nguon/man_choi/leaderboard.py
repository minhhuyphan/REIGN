import pygame
import math
import random
from ma_nguon.core import high_scores


class LeaderboardScene:
    def __init__(self, game):
        self.game = game
        self.font_title = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 60)
        self.font_subtitle = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 36)
        self.font = pygame.font.Font("tai_nguyen/font/Fz-Futurik.ttf", 24)
        self.font_small = pygame.font.Font("tai_nguyen/font/Fz-Futurik.ttf", 18)
        
        try:
            data = high_scores.load_high_scores()
            self.level_keys = list(data.keys()) if data else []
        except Exception:
            self.level_keys = []
        self.selected = 0
        
        # Animation variables
        self.title_wave_offset = 0
        self.particle_timer = 0
        self.particles = []
        self.bounce_offset = 0
        
        # Load background
        try:
            self.background = pygame.image.load("Tai_nguyen/hinh_anh/giao_dien/bg.png")
        except:
            self.background = None
        
        # Pre-render gradient background
        self._create_gradient_background()
    
    def _create_gradient_background(self):
        """Pre-render a beautiful gradient background"""
        w, h = self.game.WIDTH, self.game.HEIGHT
        self.gradient_bg = pygame.Surface((w, h))
        
        # Create vertical gradient from dark blue to purple/black
        for y in range(h):
            progress = y / h
            # Dark blue at top, deep purple/black at bottom
            r = int(20 + (10 - 20) * progress)
            g = int(30 + (12 - 30) * progress)
            b = int(60 + (30 - 60) * progress)
            pygame.draw.line(self.gradient_bg, (r, g, b), (0, y), (w, y))
        
        # Add subtle stars/dots
        random.seed(42)  # Consistent star pattern
        for _ in range(150):
            x = random.randint(0, w)
            y = random.randint(0, h)
            size = random.randint(1, 3)
            brightness = random.randint(150, 255)
            pygame.draw.circle(self.gradient_bg, (brightness, brightness, brightness), (x, y), size)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.change_scene("menu")
            elif event.key == pygame.K_UP:
                if self.level_keys:
                    self.selected = max(0, self.selected - 1)
            elif event.key == pygame.K_DOWN:
                if self.level_keys:
                    self.selected = min(len(self.level_keys) - 1, self.selected + 1)
            elif event.key == pygame.K_RETURN:
                # Enter to go back to menu
                self.game.change_scene("menu")

    def update(self):
        # Animate title wave
        self.title_wave_offset += 0.05
        
        # Bounce animation for selected item
        self.bounce_offset = 5 * math.sin(pygame.time.get_ticks() * 0.005)
        
        # Spawn particles occasionally
        self.particle_timer += 1
        if self.particle_timer % 20 == 0:
            self.particles.append({
                'x': random.randint(0, self.game.WIDTH),
                'y': self.game.HEIGHT,
                'vy': random.uniform(-2, -4),
                'size': random.randint(2, 4),
                'alpha': 255
            })
        
        # Update particles
        for p in self.particles[:]:
            p['y'] += p['vy']
            p['alpha'] -= 3
            if p['alpha'] <= 0 or p['y'] < 0:
                self.particles.remove(p)

    def draw(self, screen):
        w, h = screen.get_size()
        
        # Draw gradient background
        if self.background:
            bg_scaled = pygame.transform.scale(self.background, (w, h))
            screen.blit(bg_scaled, (0, 0))
            # Add dark overlay for readability
            overlay = pygame.Surface((w, h))
            overlay.set_alpha(140)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
        else:
            screen.blit(self.gradient_bg, (0, 0))
        
        # Draw animated particles
        for p in self.particles:
            s = pygame.Surface((p['size']*2, p['size']*2), pygame.SRCALPHA)
            color = (255, 215, 0, max(0, min(255, int(p['alpha']))))
            pygame.draw.circle(s, color, (p['size'], p['size']), p['size'])
            screen.blit(s, (int(p['x']), int(p['y'])))
        
        # Draw decorative border
        border_color = (255, 215, 0)
        pygame.draw.rect(screen, border_color, (10, 10, w - 20, h - 20), 3, border_radius=15)
        
        # Corner decorations
        corner_size = 40
        # Top-left
        pygame.draw.lines(screen, border_color, False, [(20, 60), (20, 20), (60, 20)], 4)
        # Top-right
        pygame.draw.lines(screen, border_color, False, [(w - 60, 20), (w - 20, 20), (w - 20, 60)], 4)
        # Bottom-left
        pygame.draw.lines(screen, border_color, False, [(20, h - 60), (20, h - 20), (60, h - 20)], 4)
        # Bottom-right
        pygame.draw.lines(screen, border_color, False, [(w - 60, h - 20), (w - 20, h - 20), (w - 20, h - 60)], 4)
        
        # Animated title with wave effect
        title_text = "BẢNG XẾP HẠNG"
        title_y = 40
        char_spacing = 0
        total_width = sum([self.font_title.size(char)[0] for char in title_text])
        start_x = w // 2 - total_width // 2
        
        for i, char in enumerate(title_text):
            wave_y = math.sin(self.title_wave_offset + i * 0.5) * 8
            char_surf = self.font_title.render(char, True, (255, 215, 0))
            # Shadow
            shadow_surf = self.font_title.render(char, True, (139, 69, 19))
            screen.blit(shadow_surf, (start_x + char_spacing + 3, title_y + wave_y + 3))
            # Main character
            screen.blit(char_surf, (start_x + char_spacing, title_y + wave_y))
            char_spacing += char_surf.get_width()

        if not self.level_keys:
            # Beautiful empty state
            panel = pygame.Surface((600, 350), pygame.SRCALPHA)
            pygame.draw.rect(panel, (20, 20, 40, 220), panel.get_rect(), border_radius=20)
            pygame.draw.rect(panel, (255, 215, 0), panel.get_rect(), 3, border_radius=20)
            screen.blit(panel, (w // 2 - 300, h // 2 - 175))
            
            # Trophy icon (simple representation)
            trophy_y = h // 2 - 100
            pygame.draw.circle(screen, (255, 215, 0), (w // 2, trophy_y), 40, 5)
            pygame.draw.rect(screen, (255, 215, 0), (w // 2 - 15, trophy_y + 30, 30, 40), border_radius=5)
            pygame.draw.rect(screen, (255, 215, 0), (w // 2 - 30, trophy_y + 65, 60, 10), border_radius=3)
            
            msg = self.font_subtitle.render("Chưa có xếp hạng", True, (255, 215, 0))
            screen.blit(msg, (w // 2 - msg.get_width() // 2, h // 2 + 20))
            
            hint = self.font.render("Hãy chơi game để ghi điểm!", True, (200, 200, 200))
            screen.blit(hint, (w // 2 - hint.get_width() // 2, h // 2 + 70))
            
            back_hint = self.font_small.render("ESC hoặc Enter: Về Menu", True, (150, 150, 150))
            screen.blit(back_hint, (w - back_hint.get_width() - 30, h - 50))
            return

        # Draw level selector panel (left side)
        panel_left = pygame.Surface((340, h - 200), pygame.SRCALPHA)
        pygame.draw.rect(panel_left, (20, 20, 40, 230), panel_left.get_rect(), border_radius=15)
        pygame.draw.rect(panel_left, (100, 100, 150), panel_left.get_rect(), 2, border_radius=15)
        screen.blit(panel_left, (40, 140))
        
        # Level list title with icon
        lvl_title = self.font_subtitle.render("📋 Chọn Màn", True, (255, 215, 0))
        screen.blit(lvl_title, (60, 150))
        
        # Draw list of levels
        box_x = 60
        box_y = 210
        for i, key in enumerate(self.level_keys):
            display = key.replace('_', ' ').title()
            is_selected = (i == self.selected)
            
            y_offset = self.bounce_offset if is_selected else 0
            
            # Highlight selected level
            if is_selected:
                highlight = pygame.Surface((300, 40), pygame.SRCALPHA)
                pygame.draw.rect(highlight, (255, 215, 0, 100), highlight.get_rect(), border_radius=10)
                pygame.draw.rect(highlight, (255, 215, 0), highlight.get_rect(), 3, border_radius=10)
                screen.blit(highlight, (box_x - 5, box_y + i * 45 - 5 + y_offset))
            
            color = (255, 255, 255) if is_selected else (180, 180, 180)
            txt = self.font.render("▶ " + display if is_selected else "  " + display, True, color)
            screen.blit(txt, (box_x + 10, box_y + i * 45 + y_offset))

        # Draw scores panel (right side)
        selected_key = self.level_keys[self.selected]
        panel_right = pygame.Surface((w - 460, h - 200), pygame.SRCALPHA)
        pygame.draw.rect(panel_right, (20, 20, 40, 230), panel_right.get_rect(), border_radius=15)
        pygame.draw.rect(panel_right, (100, 100, 150), panel_right.get_rect(), 2, border_radius=15)
        screen.blit(panel_right, (420, 140))
        
        # Scores title with trophy
        title_lvl = self.font_subtitle.render(f"🏆 {selected_key.replace('_',' ').title()}", True, (255, 215, 0))
        screen.blit(title_lvl, (440, 150))
        
        # Column headers
        header_y = 210
        rank_txt = self.font.render("Hạng", True, (200, 200, 200))
        player_txt = self.font.render("Người chơi", True, (200, 200, 200))
        score_txt = self.font.render("Điểm", True, (200, 200, 200))
        screen.blit(rank_txt, (450, header_y))
        screen.blit(player_txt, (560, header_y))
        screen.blit(score_txt, (w - 260, header_y))
        
        # Divider line
        pygame.draw.line(screen, (100, 100, 150), (440, header_y + 35), (w - 60, header_y + 35), 2)
        
        # Draw top scores with medals
        entries = high_scores.get_top_scores(selected_key, 10)
        start_y = 255
        
        medal_icons = ["🥇", "🥈", "🥉"]
        medal_colors = [(255, 215, 0), (192, 192, 192), (205, 127, 50)]  # Gold, Silver, Bronze
        
        for i, entry in enumerate(entries):
            y_pos = start_y + i * 40
            
            # Medal/rank display
            if i < 3:
                # Draw medal circle
                pygame.draw.circle(screen, medal_colors[i], (465, y_pos + 12), 16)
                pygame.draw.circle(screen, (255, 255, 255), (465, y_pos + 12), 16, 2)
                rank_txt = self.font.render(str(i+1), True, (0, 0, 0))
                screen.blit(rank_txt, (465 - rank_txt.get_width()//2, y_pos + 3))
            else:
                rank_txt = self.font.render(f"{i+1}.", True, (180, 180, 180))
                screen.blit(rank_txt, (450, y_pos))
            
            # Player name with length limit
            player_name = entry.get('user', 'Guest')
            if len(player_name) > 18:
                player_name = player_name[:15] + "..."
            player_surf = self.font.render(player_name, True, (220, 220, 220))
            screen.blit(player_surf, (560, y_pos))
            
            # Score with formatted number (thousand separators)
            score_val = entry.get('score', 0)
            score_str = f"{score_val:,}"
            score_color = medal_colors[i] if i < 3 else (255, 215, 0)
            score_surf = self.font.render(score_str, True, score_color)
            screen.blit(score_surf, (w - 260, y_pos))

        # Footer with controls
        footer_y = h - 60
        pygame.draw.line(screen, (100, 100, 150), (40, footer_y - 15), (w - 40, footer_y - 15), 2)
        
        controls = [
            ("↑↓", "Chọn màn"),
            ("Enter", "Về Menu"),
            ("ESC", "Thoát")
        ]
        control_x = 60
        for key, desc in controls:
            # Key button
            key_surf = self.font_small.render(key, True, (255, 215, 0))
            key_rect = pygame.Rect(control_x, footer_y, key_surf.get_width() + 10, 25)
            pygame.draw.rect(screen, (50, 50, 70), key_rect, border_radius=5)
            pygame.draw.rect(screen, (255, 215, 0), key_rect, 2, border_radius=5)
            screen.blit(key_surf, (control_x + 5, footer_y + 3))
            
            # Description
            desc_surf = self.font_small.render(desc, True, (180, 180, 180))
            screen.blit(desc_surf, (control_x + key_rect.width + 10, footer_y + 3))
            
            control_x += key_rect.width + desc_surf.get_width() + 40
