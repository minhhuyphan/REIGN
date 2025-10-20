"""
Base Map Scene - Universal skill handling for all maps
Cung cấp functionality chung cho tất cả maps
"""
import pygame
from ma_nguon.man_choi.skill_video import SkillVideoPlayer

class BaseMapScene:
    """
    Base class cho tất cả map scenes
    Xử lý skill system universal
    """
    
    def __init__(self):
        # Skill video system (cho Chiến Thần Lạc Hồng)
        self.skill_video = None
        self.showing_skill_video = False
        
    def handle_universal_skill_input(self, event):
        """
        Xử lý skill input universal cho mọi nhân vật
        Gọi method này trong handle_event của mỗi map
        """
        if not hasattr(self, 'player') or not self.player:
            return False
            
        # Lấy danh sách enemies của map hiện tại
        enemies = self.get_all_enemies() if hasattr(self, 'get_all_enemies') else []
        
        # Để Character class xử lý skill
        skill_result = self.player.handle_skill_input(event, enemies)
        
        if skill_result:
            print(f"[SKILL] {skill_result['message']}")
            
            if skill_result['success']:
                # Xử lý thêm dựa trên skill type
                return self._handle_skill_activation(skill_result['skill_type'])
            
        return skill_result is not None
        
    def _handle_skill_activation(self, skill_type):
        """Xử lý activation cho từng loại skill"""
        if skill_type == "clone_summon":
            # Clone skill - chỉ cần update enemies reference
            print("[SKILL] Phân thân đã được tạo!")
            return True
            
        elif skill_type == "damage_aoe":
            # Video skill cho Chiến Thần Lạc Hồng
            return self._play_skill_video()
            
        else:
            print(f"[SKILL] Unknown skill type: {skill_type}")
            return False
            
    def _play_skill_video(self):
        """Phát video skill cho Chiến Thần Lạc Hồng"""
        try:
            # Tạo callback để gây damage sau khi video kết thúc
            def on_skill_finish():
                self.damage_nearby_enemies()
                self.showing_skill_video = False
                self.skill_video = None
            
            # Phát video skill
            video_path = "Tai_nguyen/video/skill_chien_than.mp4"
            self.skill_video = SkillVideoPlayer(video_path, on_skill_finish)
            self.showing_skill_video = True
            return True
            
        except Exception as e:
            print(f"[SKILL] Lỗi phát video: {e}")
            # Fallback - gây damage luôn
            self.damage_nearby_enemies()
            return False
            
    def update_universal_skills(self):
        """
        Update skill systems - gọi trong method update của map
        """
        # Update skill video nếu đang phát
        if self.showing_skill_video and self.skill_video:
            self.skill_video.update()
            return True  # Map nên pause game khi phát video
            
        # Update clone manager nếu player có
        if hasattr(self, 'player') and self.player and self.player.clone_manager:
            enemies = self.get_all_enemies() if hasattr(self, 'get_all_enemies') else []
            self.player.set_enemies_reference(enemies)
            
        return False
        
    def damage_nearby_enemies(self):
        """
        Default implementation - map nên override method này
        """
        if not hasattr(self, 'player') or not self.player:
            return
            
        print("[SKILL] Default damage_nearby_enemies - Map should override this!")
        
        # Try to find enemies and damage them
        enemies = []
        if hasattr(self, 'normal_enemies'):
            enemies.extend(self.normal_enemies)
        if hasattr(self, 'current_boss') and self.current_boss:
            enemies.append(self.current_boss)
            
        damaged_count = 0
        for enemy in enemies:
            if hasattr(enemy, 'hp') and enemy.hp > 0:
                distance = abs(enemy.x - self.player.x)
                if distance <= self.player.skill_range:
                    enemy.hp -= self.player.skill_damage
                    if hasattr(enemy, 'damaged'):
                        enemy.damaged = True
                    damaged_count += 1
                    
        print(f"[SKILL] Damaged {damaged_count} enemies")
        
    def draw_universal_skill_ui(self, screen):
        """
        Vẽ UI skill universal - gọi trong method draw của map
        """
        if not hasattr(self, 'player') or not self.player:
            return
            
        # Kiểm tra nếu player có special skill
        if not self.player.special_skill:
            return
            
        # Vị trí UI - Dưới thanh mana
        ui_x = 20
        ui_y = 84
        ui_width = 300
        ui_height = 50
        
        # Font
        try:
            font = pygame.font.Font("tai_nguyen/font/Fz-Futurik.ttf", 18)
            font_small = pygame.font.Font("tai_nguyen/font/Fz-Futurik.ttf", 14)
        except:
            font = pygame.font.Font(None, 18)
            font_small = pygame.font.Font(None, 14)
        
        # Background panel
        bg_surface = pygame.Surface((ui_width, ui_height), pygame.SRCALPHA)
        pygame.draw.rect(bg_surface, (30, 30, 40, 200), (0, 0, ui_width, ui_height), border_radius=8)
        screen.blit(bg_surface, (ui_x, ui_y))
        
        # Border
        pygame.draw.rect(screen, (255, 215, 0), (ui_x, ui_y, ui_width, ui_height), 2, border_radius=8)
        
        # Skill icon
        icon_size = 40
        icon_x = ui_x + 8
        icon_y = ui_y + (ui_height - icon_size) // 2
        
        pygame.draw.rect(screen, (50, 50, 60), (icon_x, icon_y, icon_size, icon_size), border_radius=4)
        pygame.draw.rect(screen, (255, 215, 0), (icon_x, icon_y, icon_size, icon_size), 1, border_radius=4)
        
        # "F" key
        key_text = font.render("F", True, (255, 215, 0))
        key_rect = key_text.get_rect(center=(icon_x + icon_size//2, icon_y + icon_size//2))
        screen.blit(key_text, key_rect)
        
        # Skill name
        name_x = icon_x + icon_size + 10
        name_y = ui_y + 8
        
        skill_names = {
            "clone_summon": "PHÂN THÂN",
            "damage_aoe": "CHIẾN THẦN",
        }
        skill_name = skill_names.get(self.player.special_skill, "SKILL")
        
        skill_text = font.render(skill_name, True, (255, 215, 0))
        screen.blit(skill_text, (name_x, name_y))
        
        # Cooldown info
        remaining = self.player.get_skill_cooldown_remaining()
        cost_y = name_y + 22
        
        if remaining > 0:
            cd_text = font_small.render(f"Hồi chiêu: {remaining:.1f}s", True, (255, 150, 150))
            screen.blit(cd_text, (name_x, cost_y))
        else:
            ready_text = font_small.render(f"Hồi chiêu: {self.player.skill_cooldown/1000:.0f}s", True, (150, 150, 150))
            screen.blit(ready_text, (name_x, cost_y))
        
        # Status indicator
        status_x = ui_x + ui_width - 100
        status_y = ui_y + (ui_height - 30) // 2
        
        if remaining > 0:
            cd_big = font.render(f"{remaining:.1f}s", True, (255, 100, 100))
            screen.blit(cd_big, (status_x + 10, status_y + 8))
        else:
            if self.player.mana >= self.player.skill_mana_cost:
                ready_text = font.render("READY!", True, (0, 255, 0))
                screen.blit(ready_text, (status_x, status_y + 8))
                
        # Clone info for warrior
        if self.player.special_skill == "clone_summon":
            clone_count = self.player.get_clone_count()
            if clone_count > 0:
                clone_ui_y = ui_y + ui_height + 5
                clone_bg = pygame.Surface((ui_width, 30), pygame.SRCALPHA)
                pygame.draw.rect(clone_bg, (20, 40, 60, 180), (0, 0, ui_width, 30), border_radius=5)
                screen.blit(clone_bg, (ui_x, clone_ui_y))
                
                clone_text = font_small.render(f"Phân thân: {clone_count} hoạt động", True, (100, 200, 255))
                screen.blit(clone_text, (ui_x + 8, clone_ui_y + 8))
                
                clone_info = self.player.get_clone_info()
                if clone_info:
                    max_time = max(info['remaining_time'] for info in clone_info)
                    time_text = font_small.render(f"Thời gian: {max_time:.1f}s", True, (150, 200, 255))
                    screen.blit(time_text, (ui_x + 150, clone_ui_y + 8))