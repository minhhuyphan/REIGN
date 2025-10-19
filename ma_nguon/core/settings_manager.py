import pygame
import json
import os

class SettingsManager:
    """Class quản lý và áp dụng settings cho toàn bộ game"""
    
    def __init__(self):
        self.settings_file = "du_lieu/save/settings.json"
        self.settings = self.load_settings()
        self.apply_settings()
    
    def load_settings(self):
        """Load settings từ file"""
        default_settings = {
            "master_volume": 0.7,
            "music_volume": 0.8,
            "sfx_volume": 0.9,
            "resolution": "1024x768",
            "fullscreen": False,
            "vsync": True,
            "language": "Vietnamese",
            "controls": {
                "move_left": pygame.K_LEFT,
                "move_right": pygame.K_RIGHT,
                "jump": pygame.K_SPACE,
                "attack": pygame.K_a,
                "kick": pygame.K_s,
                "defend": pygame.K_d
            },
            "graphics": {
                "quality": "High",
                "particles": True,
                "shadows": True,
                "effects": True
            }
        }
        
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                    # Merge với default
                    for key, value in default_settings.items():
                        if key not in loaded_settings:
                            loaded_settings[key] = value
                        elif isinstance(value, dict):
                            for sub_key, sub_value in value.items():
                                if sub_key not in loaded_settings[key]:
                                    loaded_settings[key][sub_key] = sub_value
                    return loaded_settings
            else:
                return default_settings
        except Exception as e:
            print(f"Error loading settings: {e}")
            return default_settings
    
    def save_settings(self):
        """Lưu settings vào file"""
        try:
            os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def apply_settings(self):
        """Áp dụng settings vào game"""
        try:
            # Áp dụng volume settings
            self.apply_audio_settings()
            
            # Áp dụng display settings
            self.apply_display_settings()
            
            # Áp dụng graphics settings
            self.apply_graphics_settings()
            
        except Exception as e:
            print(f"Error applying settings: {e}")
    
    def apply_audio_settings(self):
        """Áp dụng audio settings"""
        try:
            # Set master volume
            pygame.mixer.set_num_channels(32)  # Đảm bảo đủ channels
            
            # Set music volume
            music_volume = self.settings["master_volume"] * self.settings["music_volume"]
            pygame.mixer.music.set_volume(music_volume)
            
            print(f"Applied audio settings: Master={self.settings['master_volume']}, Music={self.settings['music_volume']}")
        except Exception as e:
            print(f"Error applying audio settings: {e}")
    
    def apply_display_settings(self):
        """Áp dụng display settings"""
        try:
            # Parse resolution
            width, height = map(int, self.settings["resolution"].split('x'))
            
            # Tạo display surface với settings mới
            flags = 0
            if self.settings["fullscreen"]:
                flags |= pygame.FULLSCREEN
            if self.settings["vsync"]:
                flags |= pygame.DOUBLEBUF
            
            # Note: Trong game thực tế, việc thay đổi resolution cần restart
            print(f"Display settings: {width}x{height}, Fullscreen={self.settings['fullscreen']}, VSync={self.settings['vsync']}")
            
        except Exception as e:
            print(f"Error applying display settings: {e}")
    
    def apply_graphics_settings(self):
        """Áp dụng graphics settings"""
        try:
            quality = self.settings["graphics"]["quality"]
            particles = self.settings["graphics"]["particles"]
            shadows = self.settings["graphics"]["shadows"]
            effects = self.settings["graphics"]["effects"]
            
            print(f"Graphics settings: Quality={quality}, Particles={particles}, Shadows={shadows}, Effects={effects}")
            
        except Exception as e:
            print(f"Error applying graphics settings: {e}")
    
    def get_control_key(self, action):
        """Lấy key được bind cho action"""
        return self.settings["controls"].get(action, pygame.K_SPACE)
    
    def get_sfx_volume(self):
        """Lấy volume cho sound effects"""
        return self.settings["master_volume"] * self.settings["sfx_volume"]
    
    def get_music_volume(self):
        """Lấy volume cho music"""
        return self.settings["master_volume"] * self.settings["music_volume"]
    
    def is_graphics_enabled(self, feature):
        """Kiểm tra graphics feature có được bật không"""
        return self.settings["graphics"].get(feature, True)
    
    def get_language(self):
        """Lấy ngôn ngữ hiện tại"""
        return self.settings.get("language", "Vietnamese")
    
    def update_setting(self, category, key, value):
        """Cập nhật một setting cụ thể"""
        if category in self.settings:
            if isinstance(self.settings[category], dict):
                self.settings[category][key] = value
            else:
                self.settings[category] = value
        else:
            self.settings[key] = value
        
        # Áp dụng thay đổi ngay lập tức
        self.apply_settings()
    
    def reset_to_defaults(self):
        """Reset tất cả settings về default"""
        default_settings = {
            "master_volume": 0.7,
            "music_volume": 0.8,
            "sfx_volume": 0.9,
            "resolution": "1024x768",
            "fullscreen": False,
            "vsync": True,
            "language": "Vietnamese",
            "controls": {
                "move_left": pygame.K_LEFT,
                "move_right": pygame.K_RIGHT,
                "jump": pygame.K_SPACE,
                "attack": pygame.K_a,
                "kick": pygame.K_s,
                "defend": pygame.K_d
            },
            "graphics": {
                "quality": "High",
                "particles": True,
                "shadows": True,
                "effects": True
            }
        }
        
        self.settings = default_settings
        self.apply_settings()
        self.save_settings()

# Global settings instance
settings_manager = None

def get_settings_manager():
    """Lấy global settings manager instance"""
    global settings_manager
    if settings_manager is None:
        settings_manager = SettingsManager()
    return settings_manager

def play_sound(sound_file):
    """Play sound với volume từ settings"""
    try:
        settings = get_settings_manager()
        sound = pygame.mixer.Sound(sound_file)
        sound.set_volume(settings.get_sfx_volume())
        sound.play()
    except Exception as e:
        print(f"Error playing sound {sound_file}: {e}")

def create_scaled_surface(width, height):
    """Tạo surface với scale phù hợp với graphics quality"""
    settings = get_settings_manager()
    quality = settings.settings["graphics"]["quality"]
    
    # Scale dựa trên quality setting
    scale_factors = {
        "Low": 0.5,
        "Medium": 0.75,
        "High": 1.0,
        "Ultra": 1.25
    }
    
    scale = scale_factors.get(quality, 1.0)
    scaled_width = int(width * scale)
    scaled_height = int(height * scale)
    
    return pygame.Surface((scaled_width, scaled_height))