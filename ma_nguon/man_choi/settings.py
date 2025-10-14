import pygame
import json
import os
import math
from ma_nguon.man_choi.loading import LoadingScene
from ma_nguon.core.settings_manager import get_settings_manager

class SettingsScene(LoadingScene):
    def __init__(self, game_manager):
        super().__init__(game_manager, "Settings")
        self.game = game_manager  # Thêm reference này để tương thích
        self.settings_manager = get_settings_manager()
        self.settings = self.settings_manager.settings
        self.setup_ui()
        
    def save_settings(self):
        """Lưu settings thông qua settings manager"""
        self.settings_manager.settings = self.settings
        self.settings_manager.save_settings()
        self.settings_manager.apply_settings()
    
    def setup_ui(self):
        """Thiết lập giao diện settings"""
        self.font_title = pygame.font.Font("tai_nguyen/font/Fz-Futurik.ttf", 48)
        self.font_header = pygame.font.Font("tai_nguyen/font/Fz-Futurik.ttf", 32)
        self.font_text = pygame.font.Font("tai_nguyen/font/Fz-Futurik.ttf", 24)
        
        # Tabs
        self.tabs = ["Audio", "Video", "Controls", "Graphics", "Gameplay"]
        self.current_tab = 0
        
        # UI Elements
        self.sliders = {}
        self.buttons = {}
        self.dropdowns = {}
        self.toggles = {}
        
        # Colors
        self.colors = {
            "bg": (20, 25, 40),
            "panel": (40, 50, 70),
            "accent": (70, 130, 255),
            "text": (255, 255, 255),
            "text_dim": (180, 180, 180),
            "slider_bg": (60, 70, 90),
            "slider_fill": (70, 130, 255),
            "button": (50, 60, 80),
            "button_hover": (70, 80, 100)
        }
        
        # Animation
        self.bounce_offset = 0
        self.hover_states = {}
        
        self.setup_audio_controls()
        self.setup_video_controls()
        self.setup_control_bindings()
        self.setup_graphics_controls()
        self.setup_gameplay_controls()
    
    def setup_audio_controls(self):
        """Thiết lập controls cho audio"""
        self.sliders["master_volume"] = {
            "rect": pygame.Rect(300, 200, 300, 20),
            "value": self.settings["master_volume"],
            "label": "Master Volume"
        }
        self.sliders["music_volume"] = {
            "rect": pygame.Rect(300, 250, 300, 20),
            "value": self.settings["music_volume"],
            "label": "Music Volume"
        }
        self.sliders["sfx_volume"] = {
            "rect": pygame.Rect(300, 300, 300, 20),
            "value": self.settings["sfx_volume"],
            "label": "SFX Volume"
        }
    
    def setup_video_controls(self):
        """Thiết lập controls cho video"""
        self.dropdowns["resolution"] = {
            "rect": pygame.Rect(300, 200, 200, 40),
            "options": ["800x600", "1024x768", "1280x720", "1920x1080"],
            "selected": self.settings["resolution"],
            "label": "Resolution",
            "open": False
        }
        
        self.toggles["fullscreen"] = {
            "rect": pygame.Rect(300, 260, 40, 25),
            "value": self.settings["fullscreen"],
            "label": "Fullscreen"
        }
        
        self.toggles["vsync"] = {
            "rect": pygame.Rect(300, 310, 40, 25),
            "value": self.settings["vsync"],
            "label": "VSync"
        }
    
    def setup_control_bindings(self):
        """Thiết lập key bindings"""
        self.control_labels = {
            "move_left": "Move Left",
            "move_right": "Move Right", 
            "jump": "Jump",
            "attack": "Attack",
            "kick": "Kick",
            "defend": "Defend"
        }
        
        self.key_binding_mode = None
        self.waiting_for_key = False
    
    def setup_graphics_controls(self):
        """Thiết lập graphics controls"""
        self.dropdowns["quality"] = {
            "rect": pygame.Rect(300, 200, 150, 40),
            "options": ["Low", "Medium", "High", "Ultra"],
            "selected": self.settings["graphics"]["quality"],
            "label": "Graphics Quality",
            "open": False
        }
        
        self.toggles["particles"] = {
            "rect": pygame.Rect(300, 260, 40, 25),
            "value": self.settings["graphics"]["particles"],
            "label": "Particle Effects"
        }
        
        self.toggles["shadows"] = {
            "rect": pygame.Rect(300, 310, 40, 25),
            "value": self.settings["graphics"]["shadows"],
            "label": "Shadows"
        }
        
        self.toggles["effects"] = {
            "rect": pygame.Rect(300, 360, 40, 25),
            "value": self.settings["graphics"]["effects"],
            "label": "Visual Effects"
        }
    
    def setup_gameplay_controls(self):
        """Thiết lập gameplay settings"""
        self.dropdowns["language"] = {
            "rect": pygame.Rect(300, 200, 150, 40),
            "options": ["English", "Vietnamese", "Japanese", "Korean"],
            "selected": self.settings["language"],
            "label": "Language",
            "open": False
        }
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.waiting_for_key and self.key_binding_mode:
                # Gán phím mới
                self.settings["controls"][self.key_binding_mode] = event.key
                self.waiting_for_key = False
                self.key_binding_mode = None
                return
                
            if event.key == pygame.K_ESCAPE:
                self.save_settings()
                self.game.change_scene("menu")
            elif event.key == pygame.K_LEFT and self.current_tab > 0:
                self.current_tab -= 1
            elif event.key == pygame.K_RIGHT and self.current_tab < len(self.tabs) - 1:
                self.current_tab += 1
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                self.handle_click(event.pos)
    
    def handle_click(self, pos):
        """Xử lý click chuột"""
        # Check tab clicks
        for i, tab in enumerate(self.tabs):
            tab_rect = pygame.Rect(50 + i * 120, 100, 110, 40)
            if tab_rect.collidepoint(pos):
                self.current_tab = i
                return
        
        # Handle controls based on current tab
        if self.tabs[self.current_tab] == "Audio":
            self.handle_audio_click(pos)
        elif self.tabs[self.current_tab] == "Video":
            self.handle_video_click(pos)
        elif self.tabs[self.current_tab] == "Controls":
            self.handle_controls_click(pos)
        elif self.tabs[self.current_tab] == "Graphics":
            self.handle_graphics_click(pos)
        elif self.tabs[self.current_tab] == "Gameplay":
            self.handle_gameplay_click(pos)
        
        # Back button
        back_rect = pygame.Rect(50, 500, 100, 40)
        if back_rect.collidepoint(pos):
            self.save_settings()
            self.game.change_scene("menu")
        
        # Reset button
        reset_rect = pygame.Rect(200, 500, 120, 40)
        if reset_rect.collidepoint(pos):
            self.reset_settings()
        
        # Apply button
        apply_rect = pygame.Rect(370, 500, 120, 40)
        if apply_rect.collidepoint(pos):
            self.apply_settings()
    
    def handle_audio_click(self, pos):
        """Xử lý click cho audio tab"""
        for name, slider in self.sliders.items():
            if slider["rect"].collidepoint(pos):
                # Calculate new value based on click position
                relative_x = pos[0] - slider["rect"].x
                new_value = relative_x / slider["rect"].width
                new_value = max(0, min(1, new_value))
                slider["value"] = new_value
                self.settings[name] = new_value
    
    def handle_video_click(self, pos):
        """Xử lý click cho video tab"""
        # Resolution dropdown
        if "resolution" in self.dropdowns:
            dropdown = self.dropdowns["resolution"]
            if dropdown["rect"].collidepoint(pos):
                dropdown["open"] = not dropdown["open"]
            elif dropdown["open"]:
                for i, option in enumerate(dropdown["options"]):
                    option_rect = pygame.Rect(dropdown["rect"].x, 
                                            dropdown["rect"].y + 45 + i * 35, 
                                            dropdown["rect"].width, 30)
                    if option_rect.collidepoint(pos):
                        dropdown["selected"] = option
                        self.settings["resolution"] = option
                        dropdown["open"] = False
                        break
        
        # Toggles
        for name, toggle in self.toggles.items():
            if toggle["rect"].collidepoint(pos):
                toggle["value"] = not toggle["value"]
                self.settings[name] = toggle["value"]
    
    def handle_controls_click(self, pos):
        """Xử lý click cho controls tab"""
        y_offset = 200
        for i, (key, label) in enumerate(self.control_labels.items()):
            button_rect = pygame.Rect(400, y_offset + i * 50, 150, 35)
            if button_rect.collidepoint(pos):
                self.key_binding_mode = key
                self.waiting_for_key = True
                break
    
    def handle_graphics_click(self, pos):
        """Xử lý click cho graphics tab"""
        # Quality dropdown
        if "quality" in self.dropdowns:
            dropdown = self.dropdowns["quality"]
            if dropdown["rect"].collidepoint(pos):
                dropdown["open"] = not dropdown["open"]
            elif dropdown["open"]:
                for i, option in enumerate(dropdown["options"]):
                    option_rect = pygame.Rect(dropdown["rect"].x, 
                                            dropdown["rect"].y + 45 + i * 35, 
                                            dropdown["rect"].width, 30)
                    if option_rect.collidepoint(pos):
                        dropdown["selected"] = option
                        self.settings["graphics"]["quality"] = option
                        dropdown["open"] = False
                        break
        
        # Graphics toggles
        for name, toggle in self.toggles.items():
            if toggle["rect"].collidepoint(pos):
                toggle["value"] = not toggle["value"]
                self.settings["graphics"][name] = toggle["value"]
    
    def handle_gameplay_click(self, pos):
        """Xử lý click cho gameplay tab"""
        # Language dropdown
        if "language" in self.dropdowns:
            dropdown = self.dropdowns["language"]
            if dropdown["rect"].collidepoint(pos):
                dropdown["open"] = not dropdown["open"]
            elif dropdown["open"]:
                for i, option in enumerate(dropdown["options"]):
                    option_rect = pygame.Rect(dropdown["rect"].x, 
                                            dropdown["rect"].y + 45 + i * 35, 
                                            dropdown["rect"].width, 30)
                    if option_rect.collidepoint(pos):
                        dropdown["selected"] = option
                        self.settings["language"] = option
                        dropdown["open"] = False
                        break
    
    def update(self):
        """Update animations"""
        import math
        import pygame
        self.bounce_offset = math.sin(pygame.time.get_ticks() * 0.003) * 3
        
        # Update mouse hover states
        mouse_pos = pygame.mouse.get_pos()
        
        # Check tab hovers
        for i, tab in enumerate(self.tabs):
            tab_rect = pygame.Rect(50 + i * 120, 100, 110, 40)
            self.hover_states[f"tab_{i}"] = tab_rect.collidepoint(mouse_pos)
    
    def draw(self, surface):
        """Vẽ settings UI"""
        # Background
        surface.fill(self.colors["bg"])
        
        # Draw background pattern
        self.draw_background_pattern(surface)
        
        # Title
        title_surface = self.font_title.render("SETTINGS", True, self.colors["text"])
        title_rect = title_surface.get_rect(center=(surface.get_width()//2, 50))
        title_rect.y += self.bounce_offset
        surface.blit(title_surface, title_rect)
        
        # Tabs
        self.draw_tabs(surface)
        
        # Content based on current tab
        if self.tabs[self.current_tab] == "Audio":
            self.draw_audio_tab(surface)
        elif self.tabs[self.current_tab] == "Video":
            self.draw_video_tab(surface)
        elif self.tabs[self.current_tab] == "Controls":
            self.draw_controls_tab(surface)
        elif self.tabs[self.current_tab] == "Graphics":
            self.draw_graphics_tab(surface)
        elif self.tabs[self.current_tab] == "Gameplay":
            self.draw_gameplay_tab(surface)
        
        # Back button
        self.draw_back_button(surface)
        
        # Reset and Apply buttons
        self.draw_action_buttons(surface)
        
        # Instructions
        self.draw_instructions(surface)
    
    def draw_background_pattern(self, surface):
        """Vẽ pattern nền"""
        for x in range(0, surface.get_width(), 100):
            for y in range(0, surface.get_height(), 100):
                alpha = 20 + int(10 * abs(math.sin((x + y + pygame.time.get_ticks()) * 0.01)))
                color = (*self.colors["accent"], alpha)
                s = pygame.Surface((50, 50), pygame.SRCALPHA)
                s.fill(color)
                surface.blit(s, (x, y))
    
    def draw_tabs(self, surface):
        """Vẽ tabs"""
        for i, tab in enumerate(self.tabs):
            tab_rect = pygame.Rect(50 + i * 120, 100, 110, 40)
            
            # Tab background
            color = self.colors["accent"] if i == self.current_tab else self.colors["panel"]
            if self.hover_states.get(f"tab_{i}", False) and i != self.current_tab:
                color = self.colors["button_hover"]
            
            pygame.draw.rect(surface, color, tab_rect, border_radius=8)
            if i == self.current_tab:
                pygame.draw.rect(surface, self.colors["text"], tab_rect, 2, border_radius=8)
            
            # Tab text
            text_color = self.colors["text"] if i == self.current_tab else self.colors["text_dim"]
            text_surface = self.font_text.render(tab, True, text_color)
            text_rect = text_surface.get_rect(center=tab_rect.center)
            surface.blit(text_surface, text_rect)
    
    def draw_audio_tab(self, surface):
        """Vẽ audio settings"""
        for name, slider in self.sliders.items():
            # Label
            label_surface = self.font_text.render(slider["label"], True, self.colors["text"])
            surface.blit(label_surface, (50, slider["rect"].y - 5))
            
            # Slider background
            pygame.draw.rect(surface, self.colors["slider_bg"], slider["rect"], border_radius=10)
            
            # Slider fill
            fill_width = int(slider["rect"].width * slider["value"])
            if fill_width > 0:
                fill_rect = pygame.Rect(slider["rect"].x, slider["rect"].y, fill_width, slider["rect"].height)
                pygame.draw.rect(surface, self.colors["slider_fill"], fill_rect, border_radius=10)
            
            # Slider handle
            handle_x = slider["rect"].x + fill_width - 10
            handle_rect = pygame.Rect(handle_x, slider["rect"].y - 5, 20, slider["rect"].height + 10)
            pygame.draw.ellipse(surface, self.colors["text"], handle_rect)
            
            # Value text
            value_text = f"{int(slider['value'] * 100)}%"
            value_surface = self.font_text.render(value_text, True, self.colors["text"])
            surface.blit(value_surface, (slider["rect"].right + 20, slider["rect"].y - 5))
    
    def draw_video_tab(self, surface):
        """Vẽ video settings"""
        # Resolution dropdown
        if "resolution" in self.dropdowns:
            dropdown = self.dropdowns["resolution"]
            
            # Label
            label_surface = self.font_text.render(dropdown["label"], True, self.colors["text"])
            surface.blit(label_surface, (50, dropdown["rect"].y - 30))
            
            # Dropdown button
            pygame.draw.rect(surface, self.colors["button"], dropdown["rect"], border_radius=5)
            pygame.draw.rect(surface, self.colors["accent"], dropdown["rect"], 2, border_radius=5)
            
            # Selected value
            selected_surface = self.font_text.render(dropdown["selected"], True, self.colors["text"])
            selected_rect = selected_surface.get_rect(center=dropdown["rect"].center)
            surface.blit(selected_surface, selected_rect)
            
            # Dropdown arrow
            arrow_points = [
                (dropdown["rect"].right - 20, dropdown["rect"].centery - 5),
                (dropdown["rect"].right - 10, dropdown["rect"].centery + 5),
                (dropdown["rect"].right - 30, dropdown["rect"].centery + 5)
            ]
            pygame.draw.polygon(surface, self.colors["text"], arrow_points)
            
            # Dropdown options (if open)
            if dropdown["open"]:
                for i, option in enumerate(dropdown["options"]):
                    option_rect = pygame.Rect(dropdown["rect"].x, 
                                            dropdown["rect"].y + 45 + i * 35, 
                                            dropdown["rect"].width, 30)
                    color = self.colors["button_hover"] if option == dropdown["selected"] else self.colors["button"]
                    pygame.draw.rect(surface, color, option_rect, border_radius=5)
                    pygame.draw.rect(surface, self.colors["accent"], option_rect, 1, border_radius=5)
                    
                    option_surface = self.font_text.render(option, True, self.colors["text"])
                    option_text_rect = option_surface.get_rect(center=option_rect.center)
                    surface.blit(option_surface, option_text_rect)
        
        # Toggles
        for name, toggle in self.toggles.items():
            # Label
            label_surface = self.font_text.render(toggle["label"], True, self.colors["text"])
            surface.blit(label_surface, (50, toggle["rect"].y))
            
            # Toggle background
            bg_color = self.colors["accent"] if toggle["value"] else self.colors["slider_bg"]
            pygame.draw.rect(surface, bg_color, toggle["rect"], border_radius=toggle["rect"].height//2)
            
            # Toggle handle
            handle_x = toggle["rect"].right - 20 if toggle["value"] else toggle["rect"].x + 5
            handle_rect = pygame.Rect(handle_x, toggle["rect"].y + 3, 15, toggle["rect"].height - 6)
            pygame.draw.ellipse(surface, self.colors["text"], handle_rect)
    
    def draw_controls_tab(self, surface):
        """Vẽ controls settings"""
        header_surface = self.font_header.render("Key Bindings", True, self.colors["text"])
        surface.blit(header_surface, (50, 160))
        
        if self.waiting_for_key:
            waiting_surface = self.font_text.render("Press any key...", True, self.colors["accent"])
            surface.blit(waiting_surface, (400, 160))
        
        y_offset = 200
        for key, label in self.control_labels.items():
            # Label
            label_surface = self.font_text.render(f"{label}:", True, self.colors["text"])
            surface.blit(label_surface, (50, y_offset))
            
            # Key button
            button_rect = pygame.Rect(400, y_offset, 150, 35)
            color = self.colors["accent"] if self.key_binding_mode == key else self.colors["button"]
            pygame.draw.rect(surface, color, button_rect, border_radius=5)
            pygame.draw.rect(surface, self.colors["text"], button_rect, 2, border_radius=5)
            
            # Key name
            key_name = pygame.key.name(self.settings["controls"][key])
            key_surface = self.font_text.render(key_name.upper(), True, self.colors["text"])
            key_rect = key_surface.get_rect(center=button_rect.center)
            surface.blit(key_surface, key_rect)
            
            y_offset += 50
    
    def draw_graphics_tab(self, surface):
        """Vẽ graphics settings"""
        # Quality dropdown (similar to resolution)
        if "quality" in self.dropdowns:
            dropdown = self.dropdowns["quality"]
            
            # Label
            label_surface = self.font_text.render(dropdown["label"], True, self.colors["text"])
            surface.blit(label_surface, (50, dropdown["rect"].y - 30))
            
            # Dropdown button
            pygame.draw.rect(surface, self.colors["button"], dropdown["rect"], border_radius=5)
            pygame.draw.rect(surface, self.colors["accent"], dropdown["rect"], 2, border_radius=5)
            
            # Selected value
            selected_surface = self.font_text.render(dropdown["selected"], True, self.colors["text"])
            selected_rect = selected_surface.get_rect(center=dropdown["rect"].center)
            surface.blit(selected_surface, selected_rect)
            
            # Dropdown arrow
            arrow_points = [
                (dropdown["rect"].right - 20, dropdown["rect"].centery - 5),
                (dropdown["rect"].right - 10, dropdown["rect"].centery + 5),
                (dropdown["rect"].right - 30, dropdown["rect"].centery + 5)
            ]
            pygame.draw.polygon(surface, self.colors["text"], arrow_points)
            
            # Dropdown options (if open)
            if dropdown["open"]:
                for i, option in enumerate(dropdown["options"]):
                    option_rect = pygame.Rect(dropdown["rect"].x, 
                                            dropdown["rect"].y + 45 + i * 35, 
                                            dropdown["rect"].width, 30)
                    color = self.colors["button_hover"] if option == dropdown["selected"] else self.colors["button"]
                    pygame.draw.rect(surface, color, option_rect, border_radius=5)
                    pygame.draw.rect(surface, self.colors["accent"], option_rect, 1, border_radius=5)
                    
                    option_surface = self.font_text.render(option, True, self.colors["text"])
                    option_text_rect = option_surface.get_rect(center=option_rect.center)
                    surface.blit(option_surface, option_text_rect)
        
        # Graphics toggles
        for name, toggle in self.toggles.items():
            if name in ["particles", "shadows", "effects"]:
                # Label
                label_surface = self.font_text.render(toggle["label"], True, self.colors["text"])
                surface.blit(label_surface, (50, toggle["rect"].y))
                
                # Toggle background
                bg_color = self.colors["accent"] if toggle["value"] else self.colors["slider_bg"]
                pygame.draw.rect(surface, bg_color, toggle["rect"], border_radius=toggle["rect"].height//2)
                
                # Toggle handle
                handle_x = toggle["rect"].right - 20 if toggle["value"] else toggle["rect"].x + 5
                handle_rect = pygame.Rect(handle_x, toggle["rect"].y + 3, 15, toggle["rect"].height - 6)
                pygame.draw.ellipse(surface, self.colors["text"], handle_rect)
    
    def draw_gameplay_tab(self, surface):
        """Vẽ gameplay settings"""
        # Language dropdown
        if "language" in self.dropdowns:
            dropdown = self.dropdowns["language"]
            
            # Label
            label_surface = self.font_text.render(dropdown["label"], True, self.colors["text"])
            surface.blit(label_surface, (50, dropdown["rect"].y - 30))
            
            # Dropdown button
            pygame.draw.rect(surface, self.colors["button"], dropdown["rect"], border_radius=5)
            pygame.draw.rect(surface, self.colors["accent"], dropdown["rect"], 2, border_radius=5)
            
            # Selected value
            selected_surface = self.font_text.render(dropdown["selected"], True, self.colors["text"])
            selected_rect = selected_surface.get_rect(center=dropdown["rect"].center)
            surface.blit(selected_surface, selected_rect)
            
            # Dropdown arrow
            arrow_points = [
                (dropdown["rect"].right - 20, dropdown["rect"].centery - 5),
                (dropdown["rect"].right - 10, dropdown["rect"].centery + 5),
                (dropdown["rect"].right - 30, dropdown["rect"].centery + 5)
            ]
            pygame.draw.polygon(surface, self.colors["text"], arrow_points)
            
            # Dropdown options (if open)
            if dropdown["open"]:
                for i, option in enumerate(dropdown["options"]):
                    option_rect = pygame.Rect(dropdown["rect"].x, 
                                            dropdown["rect"].y + 45 + i * 35, 
                                            dropdown["rect"].width, 30)
                    color = self.colors["button_hover"] if option == dropdown["selected"] else self.colors["button"]
                    pygame.draw.rect(surface, color, option_rect, border_radius=5)
                    pygame.draw.rect(surface, self.colors["accent"], option_rect, 1, border_radius=5)
                    
                    option_surface = self.font_text.render(option, True, self.colors["text"])
                    option_text_rect = option_surface.get_rect(center=option_rect.center)
                    surface.blit(option_surface, option_text_rect)
    
    def draw_back_button(self, surface):
        """Vẽ nút Back"""
        back_rect = pygame.Rect(50, 500, 100, 40)
        mouse_pos = pygame.mouse.get_pos()
        color = self.colors["button_hover"] if back_rect.collidepoint(mouse_pos) else self.colors["button"]
        
        pygame.draw.rect(surface, color, back_rect, border_radius=8)
        pygame.draw.rect(surface, self.colors["accent"], back_rect, 2, border_radius=8)
        
        back_surface = self.font_text.render("BACK", True, self.colors["text"])
        back_text_rect = back_surface.get_rect(center=back_rect.center)
        surface.blit(back_surface, back_text_rect)
    
    def draw_instructions(self, surface):
        """Vẽ hướng dẫn"""
        instructions = [
            "← → : Switch Tabs",
            "ESC : Back to Menu",
            "Click to modify settings"
        ]
        
        y_offset = surface.get_height() - 80
        for instruction in instructions:
            instruction_surface = self.font_text.render(instruction, True, self.colors["text_dim"])
            surface.blit(instruction_surface, (surface.get_width() - instruction_surface.get_width() - 20, y_offset))
            y_offset += 25
    
    def draw_action_buttons(self, surface):
        """Vẽ các nút Reset và Apply"""
        mouse_pos = pygame.mouse.get_pos()
        
        # Reset button
        reset_rect = pygame.Rect(200, 500, 120, 40)
        reset_color = self.colors["button_hover"] if reset_rect.collidepoint(mouse_pos) else self.colors["button"]
        pygame.draw.rect(surface, reset_color, reset_rect, border_radius=8)
        pygame.draw.rect(surface, (255, 100, 100), reset_rect, 2, border_radius=8)  # Red border
        
        reset_surface = self.font_text.render("RESET", True, self.colors["text"])
        reset_text_rect = reset_surface.get_rect(center=reset_rect.center)
        surface.blit(reset_surface, reset_text_rect)
        
        # Apply button
        apply_rect = pygame.Rect(370, 500, 120, 40)
        apply_color = self.colors["button_hover"] if apply_rect.collidepoint(mouse_pos) else self.colors["button"]
        pygame.draw.rect(surface, apply_color, apply_rect, border_radius=8)
        pygame.draw.rect(surface, (100, 255, 100), apply_rect, 2, border_radius=8)  # Green border
        
        apply_surface = self.font_text.render("APPLY", True, self.colors["text"])
        apply_text_rect = apply_surface.get_rect(center=apply_rect.center)
        surface.blit(apply_surface, apply_text_rect)
    
    def reset_settings(self):
        """Reset settings về default"""
        self.settings_manager.reset_to_defaults()
        self.settings = self.settings_manager.settings
        self.setup_ui()  # Refresh UI với settings mới
    
    def apply_settings(self):
        """Áp dụng settings ngay lập tức"""
        self.settings_manager.settings = self.settings
        self.settings_manager.apply_settings()