import pygame
import math
import os
from ma_nguon.core.settings_manager import get_settings_manager

class ActionButtonsUI:
    """Hệ thống UI hiển thị các nút hành động trên màn hình game"""
    
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.settings_manager = get_settings_manager()
        
        # Button configuration - phải được định nghĩa trước load_button_images
        self.button_size = 60
        self.button_spacing = 10
        self.button_alpha = 200  # Transparency
        self.hover_scale = 1.2
        
        # Load button images
        self.button_images = self.load_button_images()
        
        # Animation
        self.pulse_time = 0
        self.hover_states = {}
        self.press_states = {}
        self.cooldown_states = {}
        
        # Button layout positions
        self.setup_button_layout()
        
        # Colors
        self.colors = {
            "button_bg": (50, 50, 50, 180),
            "button_border": (255, 255, 255, 200),
            "button_hover": (100, 150, 255, 200),
            "button_press": (255, 100, 100, 200),
            "cooldown_overlay": (100, 100, 100, 150),
            "text": (255, 255, 255),
            "text_shadow": (0, 0, 0)
        }
        
        # Font for key bindings
        try:
            self.font = pygame.font.Font("tai_nguyen/font/Fz-Futurik.ttf", 16)
        except:
            self.font = pygame.font.Font(None, 16)
    
    def load_button_images(self):
        """Load tất cả ảnh nút từ thư mục nut_bam"""
        images = {}
        button_path = "Tai_nguyen/hinh_anh/nut_bam"
        
        # Mapping filename to action
        button_mapping = {
            "danh.png": "attack",           # Nút đấm/tấn công
            "da.png": "kick",               # Nút đá  
            "phong_thu.png": "defend",      # Nút phòng thủ
            "nhay.png": "jump",             # Nút nhảy
            "chay.png": "run",              # Nút chạy
            "binh_mau.png": "health",       # Bình máu
            "binh_nang_luong.png": "energy", # Bình năng lượng
            "ban_sung.png": "special",      # Kỹ năng đặc biệt/bắn súng
            "chuong.png": "bell"            # Chuông (có thể dùng cho menu/pause)
        }
        
        for filename, action in button_mapping.items():
            file_path = os.path.join(button_path, filename)
            try:
                if os.path.exists(file_path):
                    image = pygame.image.load(file_path).convert_alpha()
                    # Scale to button size
                    image = pygame.transform.scale(image, (self.button_size, self.button_size))
                    images[action] = image
                    print(f"Loaded button: {action} from {filename}")
                else:
                    print(f"Button file not found: {file_path}")
            except Exception as e:
                print(f"Error loading button {filename}: {e}")
        
        return images
    
    def setup_button_layout(self):
        """Thiết lập layout các nút trên màn hình"""
        # Right side action buttons (attack, kick, defend, etc.)
        right_x = self.screen_width - self.button_size - 20
        right_y_start = self.screen_height - (self.button_size + self.button_spacing) * 3 - 20
        
        # Left side movement buttons
        left_x = 20
        left_y = self.screen_height - self.button_size - 20
        
        self.button_layout = {
            # Combat buttons (right side) - Nút chiến đấu bên phải
            "attack": {
                "rect": pygame.Rect(right_x, right_y_start, self.button_size, self.button_size),
                "key_action": "attack",
                "category": "combat",
                "description": "Đấm/Tấn công"
            },
            "kick": {
                "rect": pygame.Rect(right_x, right_y_start + (self.button_size + self.button_spacing), self.button_size, self.button_size),
                "key_action": "kick", 
                "category": "combat",
                "description": "Đá"
            },
            "defend": {
                "rect": pygame.Rect(right_x, right_y_start + (self.button_size + self.button_spacing) * 2, self.button_size, self.button_size),
                "key_action": "defend",
                "category": "combat",
                "description": "Phòng thủ"
            },
            
            # Movement buttons (left side) - Nút di chuyển bên trái
            "jump": {
                "rect": pygame.Rect(left_x, left_y - (self.button_size + self.button_spacing), self.button_size, self.button_size),
                "key_action": "jump",
                "category": "movement",
                "description": "Nhảy"
            },
            "run": {
                "rect": pygame.Rect(left_x + (self.button_size + self.button_spacing), left_y, self.button_size, self.button_size),
                "key_action": "move_right", 
                "category": "movement",
                "description": "Chạy"
            },
            
            # Special buttons (top right) - Nút đặc biệt góc trên phải
            "health": {
                "rect": pygame.Rect(right_x - (self.button_size + self.button_spacing), right_y_start - (self.button_size + self.button_spacing), self.button_size, self.button_size),
                "key_action": "health",
                "category": "special",
                "description": "Bình máu"
            },
            "energy": {
                "rect": pygame.Rect(right_x, right_y_start - (self.button_size + self.button_spacing), self.button_size, self.button_size),
                "key_action": "energy", 
                "category": "special",
                "description": "Bình năng lượng"
            },
            "special": {
                "rect": pygame.Rect(right_x - (self.button_size + self.button_spacing) * 2, right_y_start - (self.button_size + self.button_spacing), self.button_size, self.button_size),
                "key_action": "special",
                "category": "special",
                "description": "Bắn súng/Kỹ năng đặc biệt"
            },
            
            # Utility button (top center) - Nút tiện ích
            "bell": {
                "rect": pygame.Rect(self.screen_width // 2 - self.button_size // 2, 20, self.button_size, self.button_size),
                "key_action": "bell",
                "category": "utility",
                "description": "Menu/Pause"
            }
        }
    
    def handle_event(self, event, player=None):
        """Xử lý sự kiện click chuột trên buttons"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            mouse_pos = pygame.mouse.get_pos()
            
            for button_name, button_data in self.button_layout.items():
                if button_data["rect"].collidepoint(mouse_pos):
                    self.trigger_button_action(button_name, player)
                    self.press_states[button_name] = pygame.time.get_ticks()
                    return True
        
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            # Reset press states
            self.press_states.clear()
        
        return False
    
    def trigger_button_action(self, button_name, player=None):
        """Trigger hành động khi nút được bấm"""
        if not player:
            return
            
        key_action = self.button_layout[button_name]["key_action"]
        
        # Simulate key press for the player
        if key_action == "attack" and not player.actioning:
            player.set_action("danh")
            print("🥊 Tấn công!")
        elif key_action == "kick" and not player.actioning:
            player.set_action("da")
            print("🦵 Đá!")
        elif key_action == "defend":
            player.set_action("do")
            print("🛡️ Phòng thủ!")
        elif key_action == "jump" and not player.jumping:
            player.jump()
            print("🏃 Nhảy!")
        elif key_action == "health":
            self.use_health_potion(player)
        elif key_action == "energy":
            self.use_energy_potion(player)
        elif key_action == "special":
            self.use_special_ability(player)
        elif key_action == "bell":
            self.show_pause_menu()
        
        print(f"Button triggered: {button_name} -> {key_action}")
    
    def use_health_potion(self, player):
        """Sử dụng bình máu"""
        if hasattr(player, 'hp') and hasattr(player, 'max_hp'):
            if player.hp < player.max_hp:
                heal_amount = min(100, player.max_hp - player.hp)
                player.hp += heal_amount
                print(f"🩸 Sử dụng bình máu: +{heal_amount} HP")
                # Set cooldown
                self.cooldown_states["health"] = pygame.time.get_ticks() + 5000  # 5 second cooldown
            else:
                print("❤️ Máu đã đầy!")
    
    def use_energy_potion(self, player):
        """Sử dụng bình năng lượng"""
        # Có thể implement energy system sau
        print("⚡ Sử dụng bình năng lượng!")
        self.cooldown_states["energy"] = pygame.time.get_ticks() + 3000  # 3 second cooldown
    
    def use_special_ability(self, player):
        """Sử dụng kỹ năng đặc biệt"""
        if not player.actioning:
            # Có thể implement special attacks
            player.set_action("danh")  # Tạm thời dùng attack
            print("🔫 Sử dụng kỹ năng bắn súng!")
            self.cooldown_states["special"] = pygame.time.get_ticks() + 10000  # 10 second cooldown
    
    def show_pause_menu(self):
        """Hiển thị menu pause"""
        print("🔔 Pause Menu - Press ESC to continue")
        # Có thể implement pause menu UI sau
        # Hoặc trigger event để game scene xử lý
    
    def update(self):
        """Update animations và states"""
        self.pulse_time += 0.1
        
        # Update hover states
        mouse_pos = pygame.mouse.get_pos()
        for button_name, button_data in self.button_layout.items():
            self.hover_states[button_name] = button_data["rect"].collidepoint(mouse_pos)
        
        # Clear expired press states
        current_time = pygame.time.get_ticks()
        expired_presses = [name for name, time in self.press_states.items() if current_time - time > 200]
        for name in expired_presses:
            del self.press_states[name]
        
        # Clear expired cooldowns
        expired_cooldowns = [name for name, time in self.cooldown_states.items() if current_time > time]
        for name in expired_cooldowns:
            del self.cooldown_states[name]
    
    def draw(self, surface):
        """Vẽ tất cả action buttons"""
        current_time = pygame.time.get_ticks()
        
        for button_name, button_data in self.button_layout.items():
            rect = button_data["rect"]
            
            # Calculate button state
            is_hovered = self.hover_states.get(button_name, False)
            is_pressed = button_name in self.press_states
            is_on_cooldown = button_name in self.cooldown_states
            
            # Calculate scale and alpha
            scale = 1.0
            alpha = self.button_alpha
            
            if is_pressed:
                scale = 0.9
                alpha = 255
            elif is_hovered:
                scale = self.hover_scale
                alpha = 255
            
            # Add pulse effect
            if button_data["category"] == "combat":
                pulse = math.sin(self.pulse_time) * 0.05 + 1.0
                scale *= pulse
            
            # Calculate final rect
            final_size = int(self.button_size * scale)
            final_rect = pygame.Rect(
                rect.centerx - final_size // 2,
                rect.centery - final_size // 2,
                final_size,
                final_size
            )
            
            # Draw button background
            self.draw_button_background(surface, final_rect, button_name, is_hovered, is_pressed, is_on_cooldown)
            
            # Draw button image
            if button_name in self.button_images:
                image = self.button_images[button_name]
                scaled_image = pygame.transform.scale(image, (final_size - 8, final_size - 8))
                
                # Apply alpha
                if alpha < 255:
                    scaled_image.set_alpha(alpha)
                
                # Apply cooldown effect
                if is_on_cooldown:
                    scaled_image = scaled_image.copy()
                    scaled_image.fill((100, 100, 100), special_flags=pygame.BLEND_MULT)
                
                image_rect = scaled_image.get_rect(center=final_rect.center)
                surface.blit(scaled_image, image_rect)
            
            # Draw key binding
            self.draw_key_binding(surface, final_rect, button_data["key_action"])
            
            # Draw cooldown indicator
            if is_on_cooldown:
                self.draw_cooldown_indicator(surface, final_rect, button_name, current_time)
    
    def draw_button_background(self, surface, rect, button_name, is_hovered, is_pressed, is_on_cooldown):
        """Vẽ background cho button"""
        # Choose color based on state
        if is_on_cooldown:
            color = self.colors["cooldown_overlay"]
        elif is_pressed:
            color = self.colors["button_press"]
        elif is_hovered:
            color = self.colors["button_hover"]
        else:
            color = self.colors["button_bg"]
        
        # Draw background with alpha
        bg_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.ellipse(bg_surface, color, bg_surface.get_rect())
        surface.blit(bg_surface, rect)
        
        # Draw border
        border_color = self.colors["button_border"]
        if is_hovered:
            border_color = self.colors["button_hover"][:3] + (255,)
        
        pygame.draw.ellipse(surface, border_color, rect, 2)
    
    def draw_key_binding(self, surface, rect, key_action):
        """Vẽ phím tắt trên góc button"""
        # Get key from settings
        key = self.settings_manager.get_control_key(key_action)
        if key:
            key_name = pygame.key.name(key).upper()
            
            # Draw key text
            text_surface = self.font.render(key_name, True, self.colors["text"])
            text_rect = text_surface.get_rect()
            text_rect.topright = (rect.right - 2, rect.top + 2)
            
            # Draw shadow
            shadow_surface = self.font.render(key_name, True, self.colors["text_shadow"])
            shadow_rect = text_rect.copy()
            shadow_rect.x += 1
            shadow_rect.y += 1
            
            surface.blit(shadow_surface, shadow_rect)
            surface.blit(text_surface, text_rect)
    
    def draw_cooldown_indicator(self, surface, rect, button_name, current_time):
        """Vẽ cooldown indicator"""
        if button_name not in self.cooldown_states:
            return
        
        cooldown_end = self.cooldown_states[button_name]
        total_cooldown = 5000  # Default 5 seconds
        
        if button_name == "energy":
            total_cooldown = 3000
        elif button_name == "special":
            total_cooldown = 10000
        
        remaining_time = max(0, cooldown_end - current_time)
        progress = 1.0 - (remaining_time / total_cooldown)
        
        # Draw circular progress
        center = rect.center
        radius = rect.width // 2 - 4
        
        if progress < 1.0:
            # Draw cooldown overlay
            overlay = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            pygame.draw.circle(overlay, (0, 0, 0, 150), (rect.width//2, rect.height//2), radius)
            surface.blit(overlay, rect)
            
            # Draw progress arc
            start_angle = -math.pi/2  # Start from top
            end_angle = start_angle + (2 * math.pi * progress)
            
            if progress > 0:
                # Draw arc points
                arc_points = []
                steps = max(3, int(20 * progress))
                for i in range(steps + 1):
                    angle = start_angle + (end_angle - start_angle) * i / steps
                    x = center[0] + radius * math.cos(angle)
                    y = center[1] + radius * math.sin(angle)
                    arc_points.append((x, y))
                
                if len(arc_points) > 1:
                    pygame.draw.lines(surface, (0, 255, 0), False, arc_points, 3)
            
            # Draw remaining time text
            time_text = f"{remaining_time // 1000 + 1}"
            time_surface = self.font.render(time_text, True, (255, 255, 255))
            time_rect = time_surface.get_rect(center=center)
            surface.blit(time_surface, time_rect)
    
    def set_screen_size(self, width, height):
        """Cập nhật kích thước màn hình và layout"""
        self.screen_width = width
        self.screen_height = height
        self.setup_button_layout()
    
    def is_button_area(self, pos):
        """Kiểm tra xem vị trí có nằm trong vùng buttons không"""
        for button_data in self.button_layout.values():
            if button_data["rect"].collidepoint(pos):
                return True
        return False