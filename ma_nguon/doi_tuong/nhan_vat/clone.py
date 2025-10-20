"""
Clone System for Chiến Binh Special Skill
Hệ thống phân thân cho skill đặc biệt của Chiến Binh
"""
import pygame
import math
import random
from ma_nguon.doi_tuong.nhan_vat.nhan_vat import Character

class WarriorClone:
    """
    Phân thân của Chiến Binh - tự động di chuyển và tấn công quái vật
    """
    def __init__(self, x, y, master, duration=15000):  # 15 giây
        self.x = x
        self.y = y
        self.base_y = y
        self.master = master  # Nhân vật chính
        self.duration = duration  # Thời gian tồn tại (ms)
        self.creation_time = pygame.time.get_ticks()
        self.active = True
        
        # Copy stats từ master (nhưng yếu hơn)
        self.hp = master.hp // 2  # Phân thân có 50% HP
        self.max_hp = self.hp
        self.damage = master.damage * 0.7  # 70% damage
        self.kick_damage = master.kick_damage * 0.7
        self.speed = master.speed * 1.2  # Nhanh hơn 20%
        self.defense = master.defense // 2
        
        # Copy animations từ master
        self.folder = master.folder
        self.animations = master.animations
        self.state = "dung_yen"
        self.frame = 0
        self.image = self.animations[self.state][0] if self.animations[self.state] else None
        self.animation_cooldown = 100
        self.last_update = pygame.time.get_ticks()
        
        # Clone properties
        self.flip = False
        self.actioning = False
        self.action_type = ""
        self.target_enemy = None
        self.dead = False
        
        # AI behavior - mở rộng phạm vi để clone có thể di chuyển full map
        self.search_radius = 9999  # Phạm vi tìm quái không giới hạn (toàn map)
        self.attack_radius = 80   # Phạm vi tấn công
        self.last_target_search = 0
        self.move_speed = master.speed * 1.5  # Tốc độ di chuyển nhanh hơn
        
        # Patrol behavior khi không có target
        self.patrol_direction = 1 if random.random() > 0.5 else -1  # Random hướng ban đầu
        self.patrol_speed = self.move_speed * 0.8  # Tốc độ tuần tra chậm hơn chase
        self.search_cooldown = 200  # Tìm target mới mỗi 0.2s (nhanh hơn)
        
        # Visual effects
        self.alpha = 180  # Trong suốt một phần để phân biệt với master
        self.glow_timer = 0
        
        print(f"[CLONE] Tạo phân thân tại ({x}, {y}) - HP: {self.hp}, Damage: {self.damage:.1f}")
        
    def update(self, enemies, delta_time=16):
        """Cập nhật logic AI của phân thân"""
        if not self.active or self.dead:
            return
            
        # Kiểm tra thời gian tồn tại
        current_time = pygame.time.get_ticks()
        if current_time - self.creation_time >= self.duration:
            self.active = False
            print("[CLONE] Phân thân hết thời gian tồn tại")
            return
            
        # Cập nhật animation
        self._update_animation()
        
        # Cập nhật hiệu ứng ánh sáng
        self.glow_timer += delta_time
        
        # AI logic
        if not self.actioning:
            self._ai_behavior(enemies)
            
    def _update_animation(self):
        """Cập nhật animation của phân thân"""
        now = pygame.time.get_ticks()
        if now - self.last_update >= self.animation_cooldown:
            self.frame = (self.frame + 1) % len(self.animations[self.state])
            self.image = self.animations[self.state][self.frame]
            self.last_update = now
            
            # Kết thúc action nếu đã phát hết animation
            if self.actioning and self.frame == 0:
                self.actioning = False
                self.state = "dung_yen"
                
    def _ai_behavior(self, enemies):
        """Logic AI cho phân thân"""
        current_time = pygame.time.get_ticks()
        
        # Tìm target mới nếu cần
        if (current_time - self.last_target_search >= self.search_cooldown or 
            not self.target_enemy or self.target_enemy.dead):
            self._find_target(enemies)
            self.last_target_search = current_time
            
        if self.target_enemy and not self.target_enemy.dead:
            # Tính khoảng cách đến target
            dx = self.target_enemy.x - self.x
            dy = self.target_enemy.y - self.y
            distance = math.sqrt(dx*dx + dy*dy)
            
            # Nếu ở trong phạm vi tấn công
            if distance <= self.attack_radius:
                self._attack_target()
            else:
                # Di chuyển về phía target
                self._move_toward_target(dx, distance)
        else:
            # Không có target -> tuần tra khắp map để tìm enemy
            self._patrol_map()
                
    def _find_target(self, enemies):
        """Tìm quái vật để tấn công - ưu tiên gần nhất, nhưng có thể tìm khắp map"""
        self.target_enemy = None
        min_distance = float('inf')  # Không giới hạn khoảng cách
        target_found = False
        
        # Tìm trong tất cả enemies trên map
        for enemy in enemies:
            if enemy.dead or enemy.hp <= 0:
                continue
                
            # Tính khoảng cách
            dx = enemy.x - self.x
            dy = enemy.y - self.y
            distance = math.sqrt(dx*dx + dy*dy)
            
            # Chọn enemy gần nhất (không giới hạn khoảng cách)
            if distance < min_distance:
                min_distance = distance
                self.target_enemy = enemy
                target_found = True
                
        if target_found:
            print(f"[CLONE] Tìm thấy target: khoảng cách {min_distance:.1f}px")
        else:
            print("[CLONE] Không tìm thấy target nào còn sống")
            
    def _move_toward_target(self, dx, distance):
        """Di chuyển về phía target với tốc độ cao"""
        # Tính toán hướng và tốc độ di chuyển
        if distance > 0:
            # Sử dụng move_speed cao hơn để di chuyển nhanh khắp map
            move_x = (dx / distance) * self.move_speed
            
            # Tăng tốc khi target ở xa (turbo mode)
            if distance > 500:  # Nếu enemy ở xa > 500 pixels
                move_x *= 2.0  # Tăng gấp đôi tốc độ
                print(f"[CLONE] Turbo mode: di chuyển nhanh đến target xa {distance:.1f}px")
            
            # Cập nhật vị trí
            self.x += move_x
            
            # Cập nhật hướng nhìn
            self.flip = dx < 0
            
            # Đổi animation thành chạy
            if self.state != "chay":
                self.state = "chay"
                self.frame = 0
                
            print(f"[CLONE] Di chuyển đến target: khoảng cách {distance:.1f}px")
            
    def _patrol_map(self):
        """Tuần tra khắp map để tìm enemy khi không có target"""
        # Di chuyển theo hướng patrol
        self.x += self.patrol_direction * self.patrol_speed
        
        # Đổi hướng khi đến biên map (giả sử map width khoảng 5000)
        if self.x <= 50:  # Biên trái
            self.patrol_direction = 1
            print("[CLONE] Đến biên trái, đổi hướng sang phải")
        elif self.x >= 4950:  # Biên phải (giả sử map width = 5000)
            self.patrol_direction = -1
            print("[CLONE] Đến biên phải, đổi hướng sang trái")
            
        # Cập nhật hướng nhìn và animation
        self.flip = self.patrol_direction < 0
        
        if self.state != "chay":
            self.state = "chay"
            self.frame = 0
            
        # Log tuần tra mỗi 2 giây
        current_time = pygame.time.get_ticks()
        if not hasattr(self, 'last_patrol_log'):
            self.last_patrol_log = 0
        if current_time - self.last_patrol_log >= 2000:
            print(f"[CLONE] Tuần tra tại x={self.x:.0f}, hướng={'trái' if self.patrol_direction < 0 else 'phải'}")
            self.last_patrol_log = current_time
            
    def _attack_target(self):
        """Tấn công target"""
        if self.actioning:
            return
            
        # Random giữa đấm và đá
        attack_type = random.choice(["danh", "da"])
        damage = self.damage if attack_type == "danh" else self.kick_damage
        
        # Bắt đầu animation tấn công
        self.actioning = True
        self.action_type = attack_type
        self.state = attack_type
        self.frame = 0
        
        # Gây damage cho target (với delay nhỏ để animation trông tự nhiên)
        if self.target_enemy:
            # Xác định hướng knockback
            attacker_flip = self.x > self.target_enemy.x
            self.target_enemy.take_damage(damage, attacker_flip)
            print(f"[CLONE] Tấn công {attack_type} - Damage: {damage:.1f}")
            
    def take_damage(self, damage, attacker_flip):
        """Phân thân nhận sát thương"""
        if self.dead:
            return
            
        self.hp -= damage
        print(f"[CLONE] Nhận damage: {damage} - HP còn lại: {self.hp}")
        
        if self.hp <= 0:
            self.dead = True
            self.active = False
            print("[CLONE] Phân thân đã bị tiêu diệt")
            
    def draw(self, screen, camera_x=0):
        """Vẽ phân thân với hiệu ứng đặc biệt"""
        if not self.active or not self.image:
            return
            
        # Tính vị trí vẽ
        draw_x = self.x - camera_x
        draw_y = self.y
        
        # Tạo surface với alpha cho hiệu ứng trong suốt
        clone_surface = self.image.copy()
        
        # Hiệu ứng ánh sáng nhấp nháy
        glow_alpha = int(50 + 30 * math.sin(self.glow_timer * 0.005))
        
        # Flip image nếu cần
        if self.flip:
            clone_surface = pygame.transform.flip(clone_surface, True, False)
            
        # Áp dụng alpha
        clone_surface.set_alpha(self.alpha)
        
        # Vẽ hiệu ứng ánh sáng (aura xanh dương)
        glow_size = (clone_surface.get_width() + 10, clone_surface.get_height() + 10)
        glow_surface = pygame.Surface(glow_size, pygame.SRCALPHA)
        glow_surface.fill((0, 150, 255, glow_alpha))  # Màu xanh dương trong suốt
        
        glow_rect = glow_surface.get_rect()
        glow_rect.center = (draw_x + clone_surface.get_width()//2, 
                           draw_y + clone_surface.get_height()//2)
        
        # Vẽ aura trước
        screen.blit(glow_surface, glow_rect)
        
        # Vẽ phân thân
        screen.blit(clone_surface, (draw_x, draw_y))
        
        # Vẽ thanh HP nhỏ phía trên đầu
        self._draw_health_bar(screen, draw_x, draw_y - 10, clone_surface.get_width())
        
    def _draw_health_bar(self, screen, x, y, width):
        """Vẽ thanh HP cho phân thân"""
        bar_width = min(width, 60)
        bar_height = 6
        
        # Background
        hp_bg_rect = pygame.Rect(x + (width - bar_width)//2, y, bar_width, bar_height)
        pygame.draw.rect(screen, (60, 60, 60), hp_bg_rect)
        
        # HP bar
        hp_ratio = self.hp / self.max_hp
        hp_width = int(bar_width * hp_ratio)
        if hp_width > 0:
            hp_rect = pygame.Rect(x + (width - bar_width)//2, y, hp_width, bar_height)
            # Màu đỏ cho HP thấp, xanh lá cho HP cao
            hp_color = (255, int(255 * hp_ratio), 0) if hp_ratio < 0.5 else (0, 255, 0)
            pygame.draw.rect(screen, hp_color, hp_rect)
            
    def get_remaining_time(self):
        """Lấy thời gian còn lại (giây)"""
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.creation_time
        remaining_ms = max(0, self.duration - elapsed)
        return remaining_ms / 1000.0

class CloneManager:
    """
    Quản lý tất cả phân thân trong game
    """
    def __init__(self):
        self.clones = []
        
    def add_clone(self, clone):
        """Thêm phân thân mới"""
        self.clones.append(clone)
        print(f"[CLONE_MANAGER] Thêm phân thân - Tổng số: {len(self.clones)}")
        
    def update(self, enemies, delta_time=16):
        """Cập nhật tất cả phân thân"""
        # Cập nhật các clone còn hoạt động
        for clone in self.clones[:]:  # Copy list để có thể remove safely
            clone.update(enemies, delta_time)
            
            # Remove inactive clones
            if not clone.active:
                self.clones.remove(clone)
                print(f"[CLONE_MANAGER] Xóa phân thân - Còn lại: {len(self.clones)}")
                
    def draw(self, screen, camera_x=0):
        """Vẽ tất cả phân thân"""
        for clone in self.clones:
            clone.draw(screen, camera_x)
            
    def get_active_count(self):
        """Lấy số lượng phân thân đang hoạt động"""
        return len([c for c in self.clones if c.active and not c.dead])
        
    def clear_all(self):
        """Xóa tất cả phân thân (khi chuyển màn, etc.)"""
        self.clones.clear()
        print("[CLONE_MANAGER] Đã xóa tất cả phân thân")