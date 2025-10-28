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
        # HUD pickup animations (gold, hp, mp)
        # Each entry: { 'start': ticks, 'amount': int, 'duration': ms }
        self.hud_animations = {}
        
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
            
            # Special button(s) (top right) - keep special ability only; health/energy moved to centered HUD
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
            if hasattr(player, 'start_action'):
                player.start_action("danh")
                print("🥊 Tấn công!")
        elif key_action == "kick" and not player.actioning:
            if hasattr(player, 'start_action'):
                player.start_action("da")
                print("🦵 Đá!")
        elif key_action == "defend":
            if hasattr(player, 'start_action'):
                player.start_action("do")
                print("🛡️ Phòng thủ!")
        elif key_action == "jump":
            # Nhảy cần set cả jumping flag và action type
            if hasattr(player, 'jumping') and not player.jumping:
                player.jumping = True
                player.actioning = True
                player.action_type = "nhay"
                player.jump_vel = -12  # Tốc độ nhảy (âm = lên trên)
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
        if hasattr(player, 'use_health_potion'):
            if player.use_health_potion():
                print("🩸 Sử dụng bình máu thành công!")
                self.cooldown_states["health"] = pygame.time.get_ticks() + 5000  # 5 second cooldown
            else:
                print("❌ Không có bình máu hoặc HP đã đầy!")
        else:
            print("⚠️ Nhân vật không hỗ trợ bình máu")
    
    def use_energy_potion(self, player):
        """Sử dụng bình năng lượng (mana)"""
        if hasattr(player, 'use_mana_potion'):
            if player.use_mana_potion():
                print("⚡ Sử dụng bình năng lượng thành công!")
                self.cooldown_states["energy"] = pygame.time.get_ticks() + 3000  # 3 second cooldown
            else:
                print("❌ Không có bình năng lượng hoặc mana đã đầy!")
        else:
            print("⚠️ Nhân vật không hỗ trợ bình năng lượng")
    
    def use_special_ability(self, player):
        """Sử dụng kỹ năng đặc biệt"""
        if hasattr(player, 'use_skill'):
            if player.can_use_skill() if hasattr(player, 'can_use_skill') else True:
                player.use_skill()
                print("� Sử dụng kỹ năng đặc biệt!")
                self.cooldown_states["special"] = pygame.time.get_ticks() + 10000  # 10 second cooldown
            else:
                print("⏱️ Kỹ năng đang trong thời gian hồi!")
        else:
            print("⚠️ Nhân vật không có kỹ năng đặc biệt")
    
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
    
    def draw(self, surface, player=None):
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

        # Draw HUD (gold and potion counts) if player provided
        if player:
            try:
                self.draw_hud(surface, player)
            except Exception as e:
                print(f"Error drawing HUD: {e}")

    def draw_hud(self, surface, player):
        """Draw a larger ornate HUD similar to the provided art sample.
        The panel is centered near the top of the screen and shows:
        - Large gold label (VÀNG: N)
        - HP BÌNH count with icon in red
        - MP BÌNH count with icon in blue
        """
        # Compact panel for top-right
        panel_w = min(420, int(self.screen_width * 0.27))
        panel_h = 72
        x = self.screen_width - panel_w - 18
        y = 12

        # Create panel surface with rounded corners
        panel = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        # dark translucent inner
        pygame.draw.rect(panel, (18, 18, 24, 220), (0, 0, panel_w, panel_h), border_radius=18)
        # decorative inner border (slight metallic)
        pygame.draw.rect(panel, (70, 70, 80, 100), (2, 2, panel_w-4, panel_h-4), 2, border_radius=16)

        # subtle vignette on panel
        vignette = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        for i in range(6):
            alpha = int(12 * (6 - i))
            pygame.draw.rect(vignette, (0,0,0,alpha), (i, i, panel_w-2*i, panel_h-2*i), border_radius=18-i)
        panel.blit(vignette, (0,0), special_flags=pygame.BLEND_RGBA_SUB)

        # Panel glow (outside)
        glow = pygame.Surface((panel_w+40, panel_h+40), pygame.SRCALPHA)
        pygame.draw.ellipse(glow, (20, 130, 180, 40), glow.get_rect())
        surface.blit(glow, (x-20, y-20))

        # Blit panel onto screen
        surface.blit(panel, (x, y))

        # Fonts (smaller for compact HUD)
        try:
            big_font = pygame.font.Font("Tai_nguyen/font/Fz-Donsky.ttf", 26)
            label_font = pygame.font.Font("Tai_nguyen/font/Fz-Futurik.ttf", 16)
        except:
            big_font = pygame.font.Font(None, 26)
            label_font = pygame.font.Font(None, 16)

        # Draw gold label on left side of panel (compact)
        gold = getattr(player, 'gold', 0)
        gold_label = f"{gold}"
        gold_surf = big_font.render(gold_label, True, (255, 210, 90))
        # subtle shadow
        shadow_surf = big_font.render(gold_label, True, (18, 12, 4))
        shadow_surf.set_alpha(180)
        surface.blit(shadow_surf, (x + 46 + 2, y + 16 + 2))
        surface.blit(gold_surf, (x + 46, y + 16))

        # Compact coin icon to the left
        coin_x = x + 10
        coin_y = y + panel_h//2
        r = 10
        pygame.draw.circle(surface, (212,175,55), (coin_x + r, coin_y), r)
        pygame.draw.circle(surface, (255,230,140), (coin_x + r - 5, coin_y - 4), 4)
        pygame.draw.circle(surface, (160,125,40), (coin_x + r, coin_y), r, 2)

        # Right side: HP and MP groups (aligned right inside panel)
        right_margin = 12
        group_y = y + (panel_h - 36)//2
        mp_x = x + panel_w - right_margin - 70
        hp_x = mp_x - 96

        health_img = self.button_images.get('health')
        energy_img = self.button_images.get('energy')

        # HP label (compact)
        hp_count = player.potions.get('hp', 0) if hasattr(player, 'potions') else 0
        hp_text = label_font.render(f"{hp_count}", True, (220, 80, 80))
        if health_img:
            hi = pygame.transform.scale(health_img, (28, 28))
            surface.blit(hi, (hp_x, group_y))
            surface.blit(hp_text, (hp_x + 34, group_y + 6))
        else:
            surface.blit(hp_text, (hp_x, group_y + 6))

        # MP label (compact)
        mp_count = player.potions.get('mp', 0) if hasattr(player, 'potions') else 0
        mp_text = label_font.render(f"{mp_count}", True, (110, 160, 220))
        if energy_img:
            ei = pygame.transform.scale(energy_img, (28, 28))
            surface.blit(ei, (mp_x, group_y))
            surface.blit(mp_text, (mp_x + 34, group_y + 6))
        else:
            surface.blit(mp_text, (mp_x, group_y + 6))

        # Keep displaying pickup animations (gold/hp/mp) as before
        now = pygame.time.get_ticks()
        # Gold pop animation uses panel coords (adjusted for compact panel)
        g_anim = self.hud_animations.get('gold')
        if g_anim:
            elapsed = now - g_anim['start']
            dur = g_anim.get('duration', 800)
            if elapsed < dur:
                progress = elapsed / dur
                float_y = int(y + 6 - progress * 36)
                alpha = int(255 * (1 - progress))
                pop_font = big_font
                pop_text = pop_font.render(f"+{g_anim.get('amount',0)}", True, (255, 230, 120))
                shadow = pop_font.render(f"+{g_anim.get('amount',0)}", True, (0,0,0))
                # shadow
                shadow.set_alpha(alpha)
                surface.blit(shadow, (x + 46, float_y + 2))
                pop_text.set_alpha(alpha)
                surface.blit(pop_text, (x + 46, float_y))
            else:
                del self.hud_animations['gold']

        # HP/MP pill glow animations
        hp_anim = self.hud_animations.get('hp')
        if hp_anim:
            elapsed = now - hp_anim['start']
            dur = hp_anim.get('duration', 650)
            if elapsed < dur:
                prog = elapsed / dur
                glow_alpha = int(180 * (1 - prog))
                glow_surf = pygame.Surface((56, 38), pygame.SRCALPHA)
                pygame.draw.ellipse(glow_surf, (220,100,100, glow_alpha), glow_surf.get_rect())
                surface.blit(glow_surf, (hp_x - 4, group_y - 4))
            else:
                del self.hud_animations['hp']

        mp_anim = self.hud_animations.get('mp')
        if mp_anim:
            elapsed = now - mp_anim['start']
            dur = mp_anim.get('duration', 650)
            if elapsed < dur:
                prog = elapsed / dur
                glow_alpha = int(180 * (1 - prog))
                glow_surf = pygame.Surface((56, 38), pygame.SRCALPHA)
                pygame.draw.ellipse(glow_surf, (80,160,230, glow_alpha), glow_surf.get_rect())
                surface.blit(glow_surf, (mp_x - 4, group_y - 4))
            else:
                del self.hud_animations['mp']

    def trigger_pickup_animation(self, kind, amount=1):
        """Trigger a HUD pickup animation. kind in ['gold','hp','mp']"""
        now = pygame.time.get_ticks()
        if kind == 'gold':
            self.hud_animations['gold'] = {'start': now, 'amount': amount, 'duration': 800}
        elif kind == 'hp':
            self.hud_animations['hp'] = {'start': now, 'amount': amount, 'duration': 700}
        elif kind == 'mp':
            self.hud_animations['mp'] = {'start': now, 'amount': amount, 'duration': 700}
    
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