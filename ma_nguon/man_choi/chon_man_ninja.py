import pygame
import math
import random

class AutumnLevelsSceneninja:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 50)
        self.selected = 0
        self.options = ["Màn 1 - Trận Chiến Khởi Đầu", "Màn 2 -Trận Chiến Của Ninja Huyền Thoại", "Quay lại"]
        self.level_scenes = ["map_ninja_man1", "map_ninja_man2", "menu"]

        # Animation variables
        self.bounce_offset = 0
        self.bounce_speed = 0.1
        self.title_scale = 0.5
        self.title_scale_speed = 0.02
        self.leaf_particles = []
        
        # Load background image
        try:
            self.background = pygame.image.load("Tai_nguyen/hinh_anh/giao_dien/bg.png")
            self.background = pygame.transform.scale(self.background, (1600, 700))
        except pygame.error:
            try:
                self.background = pygame.image.load("Tai_nguyen/hinh_anh/canh_nen/mapninja/may.png")
                self.background = pygame.transform.scale(self.background, (1600, 700))
            except pygame.error:
                self.background = None
        
        # Tạo hiệu ứng lá rơi cho menu
        leaf_colors = [
            (255, 215, 0),   # Vàng gold
            (255, 140, 0),   # Cam đậm
            (255, 69, 0),    # Đỏ cam
            (218, 165, 32),  # Vàng đậm
        ]
        
        for i in range(50):
            self.leaf_particles.append({
                'x': random.randint(0, 1600),
                'y': random.randint(-100, 700),
                'speed': random.uniform(1.0, 3.0),
                'swing': random.uniform(0.5, 1.5),
                'swing_offset': random.uniform(0, 2 * math.pi),
                'size': random.randint(3, 8),
                'color': random.choice(leaf_colors),
                'rotation': random.uniform(0, 360),
                'rotation_speed': random.uniform(-2, 2)
            })

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                self._execute_selected_option()
            elif event.key == pygame.K_ESCAPE:
                # Quay lại màn chọn map
                self.game.change_scene("chon_map")
        
        # Mouse support
        elif event.type == pygame.MOUSEMOTION:
            mx, my = event.pos
            hovered = self._get_option_at_position(mx, my)
            if hovered is not None:
                self.selected = hovered
        
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            clicked = self._get_option_at_position(mx, my)
            if clicked is not None:
                self.selected = clicked
                self._execute_selected_option()
    
    def _execute_selected_option(self):
        """Thực thi option được chọn"""
        if self.selected < 2:  # Màn 1, 2 (index 0, 1)
            # Lưu thông tin màn được chọn và chuyển thẳng vào game
            self.game.target_level = self.level_scenes[self.selected]
            self.game.change_scene(self.level_scenes[self.selected])
        else:  # Quay lại menu chính
            self.game.change_scene("menu")
    
    def _get_option_at_position(self, mx, my):
        """Kiểm tra xem chuột có hover/click vào option nào không"""
        menu_start_y = 200
        menu_spacing = 80
        
        for i in range(len(self.options)):
            option_y = menu_start_y + i * menu_spacing
            option_height = 60
            
            if option_y <= my <= option_y + option_height:
                return i
        
        return None

    def update(self):
        # Title scale animation
        if self.title_scale < 1.0:
            self.title_scale = min(1.0, self.title_scale + self.title_scale_speed)
        
        # Bounce animation for selected button
        self.bounce_offset = 5 * math.sin(pygame.time.get_ticks() * self.bounce_speed / 100)
        
        # Cập nhật hiệu ứng lá rơi
        for leaf in self.leaf_particles:
            leaf['y'] += leaf['speed']
            leaf['x'] += math.sin(pygame.time.get_ticks() * 0.001 + leaf['swing_offset']) * leaf['swing']
            leaf['rotation'] += leaf['rotation_speed']
            
            # Reset lá khi rơi ra khỏi màn hình
            if leaf['y'] > 750:
                leaf['y'] = random.randint(-100, -50)
                leaf['x'] = random.randint(0, 1600)

    def draw_leaf(self, screen, leaf):
        """Vẽ một lá với hiệu ứng xoay"""
        # Tạo một surface nhỏ để vẽ lá
        leaf_surface = pygame.Surface((leaf['size'] * 2, leaf['size'] * 2), pygame.SRCALPHA)
        
        # Vẽ hình lá đơn giản (ellipse)
        pygame.draw.ellipse(leaf_surface, leaf['color'], 
                          (0, 0, leaf['size'] * 2, leaf['size']))
        
        # Xoay lá
        rotated_leaf = pygame.transform.rotate(leaf_surface, leaf['rotation'])
        
        # Lấy rect để căn giữa
        rect = rotated_leaf.get_rect(center=(leaf['x'], leaf['y']))
        
        # Vẽ lên màn hình
        screen.blit(rotated_leaf, rect)

    def draw(self, screen):
        # Draw background
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill((139, 69, 19))  # Brown autumn color
        
        # Vẽ hiệu ứng lá rơi phía sau
        for leaf in self.leaf_particles:
            self.draw_leaf(screen, leaf)
        
        # Title với màu mùa thu
        title_color = (255, 140, 0)  # Autumn orange
        shadow_color = (139, 69, 19)  # Dark brown shadow
        
        # Create title with scaling animation
        title_surface = self.font.render("CHON MAN NINJA", True, title_color)
        scaled_width = int(title_surface.get_width() * self.title_scale)
        scaled_height = int(title_surface.get_height() * self.title_scale)
        title_scaled = pygame.transform.scale(title_surface, (scaled_width, scaled_height))
        
        # Create shadow
        title_shadow_surface = self.font.render("CHON MAN NINJA", True, shadow_color)
        shadow_scaled_width = int(title_shadow_surface.get_width() * self.title_scale)
        shadow_scaled_height = int(title_shadow_surface.get_height() * self.title_scale)
        shadow_scaled = pygame.transform.scale(title_shadow_surface, (shadow_scaled_width, shadow_scaled_height))
        
        # Draw title shadow first
        shadow_x = screen.get_width()//2 - shadow_scaled.get_width()//2 + 3
        shadow_y = 83
        screen.blit(shadow_scaled, (shadow_x, shadow_y))
        
        # Draw main title
        title_x = screen.get_width()//2 - title_scaled.get_width()//2
        title_y = 80
        screen.blit(title_scaled, (title_x, title_y))
        
        # Difficulty indicators
        difficulty_colors = [
            (0, 255, 0),     # Green - Easy
            (255, 255, 0),   # Yellow - Medium  
            (255, 0, 0),     # Red - Hard
            (200, 200, 200)  # Gray - Back
        ]
        
        difficulty_texts = ["[DỄ]", "[TRUNG BÌNH]", ""]
        
        # Menu options with difficulty indicators
        for i, text in enumerate(self.options):
            # Calculate base position
            base_y = 220 + i*80
            option_y = base_y
            
            if i == self.selected:
                # Selected option with bounce effect
                color = (255, 215, 0)  # Gold
                option_y += self.bounce_offset
                
                # Background rectangle for selected option
                option_surface = self.font.render(text, True, color)
                bg_rect = pygame.Rect(0, 0, option_surface.get_width() + 60, option_surface.get_height() + 30)
                bg_rect.center = (screen.get_width()//2, option_y + option_surface.get_height()//2)
                pygame.draw.rect(screen, (80, 40, 20), bg_rect, border_radius=15)
                pygame.draw.rect(screen, color, bg_rect, 3, border_radius=15)
                
                # Glow effect
                glow_color = (255, 165, 0)
                glow_option = self.font.render(text, True, glow_color)
                screen.blit(glow_option, (screen.get_width()//2 - glow_option.get_width()//2 + 1, option_y + 1))
                screen.blit(glow_option, (screen.get_width()//2 - glow_option.get_width()//2 - 1, option_y - 1))
            else:
                # Unselected options
                color = (245, 245, 220)  # Light beige
            
            # Draw main option text
            option = self.font.render(text, True, color)
            screen.blit(option, (screen.get_width()//2 - option.get_width()//2, option_y))
            
            # Draw difficulty indicator
            if i < 3:
                difficulty_font = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 30)
                difficulty_surface = difficulty_font.render(difficulty_texts[i], True, difficulty_colors[i])
                screen.blit(difficulty_surface, (screen.get_width()//2 + option.get_width()//2 + 20, option_y + 10))
        
        # Instructions
        instruction_font = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 25)
        instruction_text = instruction_font.render("↑↓ Di chuyển | Enter Chọn | ESC Quay lại", True, (139, 69, 19))
        instruction_x = screen.get_width()//2 - instruction_text.get_width()//2
        instruction_y = screen.get_height() - 60
        screen.blit(instruction_text, (instruction_x, instruction_y))
        
        # Level descriptions
        descriptions = [
            "Ít quái vật, boss yếu - Hoàn hảo để làm quen",
            "Quái vật trung bình, 2 boss - Thử thách cân bằng", 
            "Rất nhiều quái mạnh, 3 boss khủng - Thử thách tối thượng!",
            "Trở về menu chính"
        ]
        
        desc_font = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 20)
        desc_surface = desc_font.render(descriptions[self.selected], True, (160, 82, 45))
        desc_x = screen.get_width()//2 - desc_surface.get_width()//2
        desc_y = 550
        screen.blit(desc_surface, (desc_x, desc_y))