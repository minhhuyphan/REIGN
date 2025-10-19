import pygame, os
from ma_nguon.core.quan_ly_tai_nguyen import load_images, load_sound_safe
from ma_nguon.core.settings_manager import get_settings_manager

class Character:
    def __init__(self, x, y, folder, controls=None, color=(0,255,0), auto=False, stats=None):
        self.x = x
        self.y = y
        self.base_y = y
        self.flip = False
        
        # Thêm stats để dễ tùy chỉnh từ màn chọn nhân vật
        if stats:
            self.hp = stats.get("hp", 500)
            self.max_hp = stats.get("hp", 500)
            self.speed = stats.get("speed", 5)
            self.damage = stats.get("damage", 30)
            self.kick_damage = stats.get("kick_damage", 20)
            self.defense = stats.get("defense", 2)
            self.regen_hp = stats.get("regen_hp", 0)
        else:
            self.hp = 1000
            self.max_hp = 1000
            self.speed = 5
            self.damage = 30
            self.kick_damage = 20
            self.defense = 2
            self.regen_hp = 0  # HP hồi mỗi giây
        
        # Lưu base stats để có thể reset khi thay đổi equipment
        self.base_hp = self.hp
        self.base_max_hp = self.max_hp
        self.base_speed = self.speed
        self.base_damage = self.damage
        self.base_defense = self.defense
        
        # Mana for skills
        self.max_mana = stats.get('max_mana', 200) if stats else 200
        self.mana = self.max_mana
        self.mana_regen = stats.get('mana_regen', 5) if stats else 5  # per second
        # Currency and potions
        self.gold = 0
        self.potions = {}
        
        # Equipment slots (3 slots: attack, defense, speed)
        self.equipped = {
            'attack': None,
            'defense': None,
            'speed': None
        }
        self.has_used_revive = False  # Track if revive effect has been used
        self.burn_effect_timer = 0  # Timer for burn effect
        self.burn_effect_active = False
        
        # Controls - sử dụng settings manager nếu không có controls được truyền vào
        self.settings_manager = get_settings_manager()
        if controls:
            self.controls = controls
        else:
            # Map từ settings controls sang character controls
            settings_controls = self.settings_manager.settings["controls"]
            self.controls = {
                "left": settings_controls["move_left"],
                "right": settings_controls["move_right"],
                "jump": settings_controls["jump"],
                "attack": settings_controls["attack"],
                "kick": settings_controls["kick"],
                "defend": settings_controls["defend"],
                "ban": pygame.K_f
            }
        self.color = color
        self.auto = auto
        self.folder = folder  # Lưu folder để tải lại animation nếu cần

        # Animation
        self.animations = self._load_animations(folder)
        self.state = "dung_yen"
        self.frame = 0
        self.image = self.animations[self.state][0] if self.animations[self.state] else None
        self.animation_cooldown = 100
        self.last_update = pygame.time.get_ticks()

        # Âm thanh - với volume từ settings
        sfx_volume = self.settings_manager.get_sfx_volume()
        self.sound_punch = load_sound_safe("tai_nguyen/am_thanh/hieu_ung/danh.mp3", sfx_volume)
        self.sound_kick = load_sound_safe("tai_nguyen/am_thanh/hieu_ung/da.mp3", sfx_volume)
        self.sound_hit = load_sound_safe("tai_nguyen/am_thanh/hieu_ung/trung.mp3", sfx_volume)
        self.sound_run = load_sound_safe("tai_nguyen/am_thanh/hieu_ung/chay.mp3", sfx_volume * 0.5)

        # Trạng thái động
        self.actioning = False
        self.action_type = ""
        self.jumping = False
        self.jump_vel = 0
        self.running_sound_playing = False
        self.damaged = False
        self.defending = False
        self.dead = False
        self.knockback_speed = 0
        
        # Danh sách viên đạn (chỉ cho tho_san_quai_vat)
        self.bullets = []
        
        # Load hình súng cho animation bắn (chỉ cho tho_san_quai_vat)
        self.weapon_image = None
        if "tho_san_quai_vat" in folder:
            try:
                weapon_path = os.path.join(folder, "chieu", "kiemkhi.png")
                self.weapon_image = pygame.image.load(weapon_path).convert_alpha()
                self.weapon_image = pygame.transform.scale(self.weapon_image, (80, 40))
            except Exception as e:
                print(f"Không load được hình súng: {e}")

    def _load_animations(self, folder):
        """Tải tất cả animation từ thư mục, đảm bảo tất cả có cùng kích thước"""
        animations = {}
        action_types = ["dung_yen", "chay", "danh", "da", "nga", "do", "nhay", "ban"]
        
        # Chuẩn hóa kích thước mặc định cho mọi animation
        base_width = 100
        base_height = 150
        
        # Lưu giữ kích thước gốc của mỗi animation
        self.animation_sizes = {}
        
        # Tải tất cả các animation trước
        raw_animations = {}
        for action in action_types:
            action_path = os.path.join(folder, action)
            try:
                images = load_images(action_path)
                if images:
                    raw_animations[action] = images
                    # Lưu kích thước gốc
                    self.animation_sizes[action] = (images[0].get_width(), images[0].get_height())
                else:
                    print(f"Warning: No images found for {action} in {action_path}")
                    # Tạo 1 hình ảnh giả làm placeholder
                    dummy = pygame.Surface((base_width, base_height), pygame.SRCALPHA)
                    dummy.fill((100, 100, 100, 150))
                    raw_animations[action] = [dummy]
                    self.animation_sizes[action] = (base_width, base_height)
            except Exception as e:
                print(f"Error loading animation {action}: {e}")
                # Tạo 1 hình ảnh giả làm placeholder
                dummy = pygame.Surface((base_width, base_height), pygame.SRCALPHA)
                dummy.fill((100, 100, 100, 150))
                raw_animations[action] = [dummy]
                self.animation_sizes[action] = (base_width, base_height)
        
        # Tìm kích thước trung bình của tất cả animation
        total_width = 0
        total_height = 0
        count = 0
        
        for action, images in raw_animations.items():
            if images:
                width, height = self.animation_sizes[action]
                total_width += width
                total_height += height
                count += 1
        
        # Tính kích thước trung bình
        if count > 0:
            avg_width = total_width // count
            avg_height = total_height // count
        else:
            avg_width = base_width
            avg_height = base_height
        
        # Scale tất cả animation về cùng kích thước trung bình
        for action, images in raw_animations.items():
            scaled_images = []
            for img in images:
                # Scale hình ảnh về kích thước trung bình
                scaled = pygame.transform.scale(img, (avg_width, avg_height))
                scaled_images.append(scaled)
            animations[action] = scaled_images
        
        return animations
    
    def start_action(self, action_type):
        if self.actioning and action_type != "nga":
            return
        
        # Kiểm tra nếu animation tồn tại
        if action_type not in self.animations:
            print(f"Warning: Animation {action_type} not found")
            return
            
        # Nếu là chiêu ban thì kiểm tra mana và xem có phải nhân vật tho_san_quai_vat không
        if action_type == "ban":
            # Chỉ nhân vật tho_san_quai_vat mới có chiêu này
            if "tho_san_quai_vat" not in self.folder:
                print("Nhân vật này không có chiêu bắn!")
                return
            mana_cost = 40
            if self.mana < mana_cost:
                print("Không đủ mana để dùng chiêu!")
                return
            self.mana -= mana_cost
            # Tạo viên đạn khi bắt đầu animation bắn
            self._create_bullet()
        
        self.actioning = True
        self.action_type = action_type
        self.state = action_type
        self.frame = 0
        self.damaged = False

        if action_type == "nhay" and not self.jumping:
            self.jumping = True
            self.jump_vel = -12
            if self.running_sound_playing and self.sound_run:
                self.sound_run.stop()
                self.running_sound_playing = False
        if action_type == "danh" and self.sound_punch:
            self.sound_punch.play()
        elif action_type == "da" and self.sound_kick:
            self.sound_kick.play()

    def play_animation(self):
        now = pygame.time.get_ticks()
        # Animation bắn chậm hơn các animation khác
        cooldown = 200 if self.state == "ban" else self.animation_cooldown
        if now - self.last_update > cooldown:
            self.last_update = now
            self.frame += 1

        # Đảm bảo animation tồn tại
        if self.state not in self.animations:
            self.state = "dung_yen"
            self.frame = 0
            
        # Đảm bảo frame luôn nằm trong khoảng hợp lệ
        max_frames = len(self.animations[self.state])
        
        # Kiểm tra và xử lý khi animation kết thúc
        if self.frame >= max_frames:
            if self.state in ["danh", "da", "do", "nhay", "ban"]:
                self.actioning = False
                self.state = "dung_yen"
                self.frame = 0
                self.damaged = False
            elif self.state == "nga":
                self.frame = max_frames - 1
            else:
                self.frame = 0

    def update(self, keys=None, target=None):
        # Xử lý knockback khi bị đánh
        if self.knockback_speed != 0:
            self.x += self.knockback_speed
            self.knockback_speed = int(self.knockback_speed * 0.8)  # Giảm dần tốc độ
            if abs(self.knockback_speed) < 1:
                self.knockback_speed = 0
        
        # Xử lý burn effect
        if self.burn_effect_active:
            current_time = pygame.time.get_ticks()
            if current_time - self.burn_effect_timer >= 1000:  # Mỗi giây
                burn_damage, _ = self.get_burn_effect()
                if burn_damage > 0:
                    self.hp -= burn_damage
                    self.burn_effect_timer = current_time
                    if self.hp <= 0 and not self.dead:
                        if self.can_revive():
                            self.trigger_revive()
                        else:
                            self.dead = True
                            self.start_action("nga")
        
        # Hồi máu nhỏ
        if self.hp > 0:
            max_hp_with_eq = self.get_max_hp_with_equipment()
            self.hp = min(self.hp + self.regen_hp, max_hp_with_eq)
        # Hồi mana theo thời gian (sử dụng ticks -> mỗi giây dựa trên clock tick)
        # We'll use pygame time to increment mana smoothly
        try:
            dt = max(0, pygame.time.get_ticks() - getattr(self, '_last_mana_tick', 0))
        except Exception:
            dt = 0
        if not hasattr(self, '_last_mana_tick'):
            self._last_mana_tick = pygame.time.get_ticks()
        now = pygame.time.get_ticks()
        elapsed = (now - self._last_mana_tick) / 1000.0
        if elapsed > 0:
            self.mana = min(self.max_mana, self.mana + self.mana_regen * elapsed)
            self._last_mana_tick = now

        # Nếu đã chết và animation ngã hết thì đứng yên
        if self.dead and self.frame == len(self.animations["nga"]) - 1:
            return

        moving = False
        self.defending = False
        
        # Get effective speed with equipment bonus
        effective_speed = self.get_effective_speed()

        # --- Xử lý action ---
        if self.actioning:
            if self.action_type == "nhay" and self.jumping:
                self.y += self.jump_vel
                self.jump_vel += 1
                if self.y >= self.base_y:
                    self.y = self.base_y
                    self.jumping = False
                    self.jump_vel = 0
                    self.actioning = False
                    self.action_type = ""
                    if keys and (self.controls.get("left") and keys[self.controls.get("left", pygame.K_LEFT)] or
                                 self.controls.get("right") and keys[self.controls.get("right", pygame.K_RIGHT)]):
                        self.state = "chay"
                    else:
                        self.state = "dung_yen"
            self.play_animation()
            return

        # --- Người chơi điều khiển ---
        if not self.auto and keys and self.hp > 0:
            if self.controls.get("jump") and keys[self.controls["jump"]] and not self.jumping:
                self.start_action("nhay")
            elif self.controls.get("defend") and keys[self.controls["defend"]]:
                self.start_action("do")
                self.defending = True
            elif self.controls.get("attack") and keys[self.controls["attack"]]:
                self.start_action("danh")
            elif self.controls.get("kick") and keys[self.controls["kick"]]:
                self.start_action("da")
            elif self.controls.get("ban") and keys[self.controls["ban"]]:
                self.start_action("ban")
            elif self.controls.get("right") and keys[self.controls["right"]]:
                self.state = "chay"
                self.flip = False
                self.x += effective_speed
                moving = True
            elif self.controls.get("left") and keys[self.controls["left"]]:
                self.state = "chay"
                self.flip = True
                self.x -= effective_speed
                moving = True
            else:
                self.state = "dung_yen"

        # --- Enemy auto ---
        if self.auto and self.hp > 0 and target:
            distance = abs(self.x - target.x)
            # Quái di chuyển đến gần người chơi
            if distance > 120:
                self.state = "chay"
                if self.x < target.x:
                    self.flip = False
                    self.x += effective_speed
                else:
                    self.flip = True
                    self.x -= effective_speed
                moving = True
            # Quái tấn công khi đủ gần
            elif distance < 120:
                # Random giữa đánh và đá
                import random
                if not self.actioning and random.random() < 0.03:  # 3% mỗi frame
                    action = random.choice(["danh", "da"])
                    self.start_action(action)
            else:
                self.state = "dung_yen"

        # --- Âm thanh chạy ---
        if self.sound_run:
            if moving and not self.running_sound_playing:
                self.sound_run.play(-1)
                self.running_sound_playing = True
            elif not moving and self.running_sound_playing:
                self.sound_run.stop()
                self.running_sound_playing = False

        self.play_animation()

        # --- Nếu chết ---
        if self.hp <= 0 and not self.dead:
            if self.can_revive():
                self.trigger_revive()
            else:
                self.dead = True
                self.start_action("nga")

    def draw(self, surface, camera_x=0):
        # Tính toán vị trí vẽ sau khi trừ camera offset
        draw_x = self.x - camera_x
        
        # Đảm bảo rằng chúng ta đang dùng frame hiện tại của animation
        if self.state in self.animations and 0 <= self.frame < len(self.animations[self.state]):
            self.image = self.animations[self.state][self.frame]
        else:
            # Nếu frame không hợp lệ, đặt lại về 0
            self.frame = 0
            if self.state in self.animations and len(self.animations[self.state]) > 0:
                self.image = self.animations[self.state][0]
        
        # Kiểm tra xem image có tồn tại không
        if self.image:
            # Lật ảnh nếu nhân vật đang hướng sang trái
            img = pygame.transform.flip(self.image, self.flip, False)
            
            # Vẽ nhân vật
            surface.blit(img, (draw_x, self.y))
        
        # Không vẽ thanh máu ở đây nữa, nó sẽ được vẽ ở góc màn hình

    # --- Mana and potion helpers ---
    def spend_mana(self, amount):
        if self.mana >= amount:
            self.mana -= amount
            return True
        return False

    def use_health_potion(self):
        if self.potions.get('hp', 0) > 0:
            self.potions['hp'] -= 1
            self.hp = min(self.max_hp, self.hp + 200)
            return True
        return False

    def use_mana_potion(self):
        if self.potions.get('mp', 0) > 0:
            self.potions['mp'] -= 1
            self.mana = min(self.max_mana, self.mana + 150)
            return True
        return False

    def take_damage(self, damage, attacker_flip):
        # Nếu đang đỡ, giảm damage
        if self.defending:
            damage = max(1, damage // 5)  # Chỉ nhận 20% damage khi đỡ
        
        if self.hp <= 0 or self.dead:
            return
            
        # Giảm damage bởi defense (bao gồm equipment bonus)
        total_defense = self.defense + self.get_defense_bonus()
        net_damage = max(damage - total_defense, 0)
        self.hp -= net_damage
        
        if self.sound_hit:
            self.sound_hit.play()
            
        # Khi nhận damage, reset trạng thái damaged
        self.damaged = True
        
        if self.hp <= 0:
            # Check revive effect from equipment
            if self.can_revive():
                self.trigger_revive()
            else:
                self.dead = True
                self.start_action("nga")
                # Té ngược
                self.knockback_speed = -15 if not attacker_flip else 15
        else:
            # Bị đẩy lùi khi trúng đòn
            self.knockback_speed = -5 if not attacker_flip else 5

    def _create_bullet(self):
        """Tạo viên đạn khi bắn"""
        from ma_nguon.doi_tuong.bullet import Bullet
        # Tính vị trí xuất phát của đạn (trước mặt nhân vật)
        direction = -1 if self.flip else 1
        bullet_x = self.x + (20 if not self.flip else -20)
        bullet_y = self.y + 40  # Chiều cao ngực nhân vật
        bullet = Bullet(bullet_x, bullet_y, direction, 100, self)  # Sát thương cố định 100
        self.bullets.append(bullet)
        print(f"[DEBUG] Tạo viên đạn tại ({bullet_x}, {bullet_y}), hướng: {direction}, damage: 100")

    # --- Equipment methods ---
    def equip_item(self, equipment):
        """Trang bị một item vào slot phù hợp"""
        if equipment and equipment.equipment_type in self.equipped:
            # Unequip current item in that slot
            old_equipment = self.equipped[equipment.equipment_type]
            if old_equipment:
                old_equipment.equipped_to = None
            
            # Equip new item
            self.equipped[equipment.equipment_type] = equipment
            equipment.equipped_to = getattr(self, 'character_name', 'unknown')
            
            # Apply stat bonuses
            self.apply_equipment_bonuses()
            return True
        return False
    
    def unequip_item(self, equipment_type):
        """Gỡ trang bị khỏi slot"""
        if equipment_type in self.equipped and self.equipped[equipment_type]:
            equipment = self.equipped[equipment_type]
            equipment.equipped_to = None
            self.equipped[equipment_type] = None
            
            # Recalculate stats
            self.apply_equipment_bonuses()
            return True
        return False
    
    def apply_equipment_bonuses(self):
        """Áp dụng bonus từ trang bị TRỰC TIẾP vào stats"""
        # Reset về base stats trước
        old_max_hp = self.max_hp
        self.max_hp = self.base_max_hp
        self.damage = self.base_damage
        self.defense = self.base_defense
        self.speed = self.base_speed
        
        # Cộng tất cả bonus từ equipment
        for equipment in self.equipped.values():
            if equipment:
                self.max_hp += equipment.hp_bonus
                self.damage += equipment.attack_bonus
                self.defense += equipment.defense_bonus
                self.speed += equipment.speed_bonus
        
        # Điều chỉnh HP hiện tại theo tỷ lệ
        if old_max_hp > 0:
            hp_ratio = self.hp / old_max_hp
            self.hp = int(self.max_hp * hp_ratio)
        else:
            self.hp = self.max_hp
    
    def get_attack_bonus(self):
        """Lấy bonus công từ trang bị"""
        bonus = 0
        for equipment in self.equipped.values():
            if equipment:
                bonus += equipment.attack_bonus
        return bonus
    
    def get_defense_bonus(self):
        """Lấy bonus thủ từ trang bị"""
        bonus = 0
        for equipment in self.equipped.values():
            if equipment:
                bonus += equipment.defense_bonus
        return bonus
    
    def get_hp_bonus(self):
        """Lấy bonus HP từ trang bị"""
        bonus = 0
        for equipment in self.equipped.values():
            if equipment:
                bonus += equipment.hp_bonus
        return bonus
    
    def get_speed_bonus(self):
        """Lấy bonus tốc độ từ trang bị"""
        bonus = 0
        for equipment in self.equipped.values():
            if equipment:
                bonus += equipment.speed_bonus
        return bonus
    
    def get_effective_damage(self):
        """Lấy sát thương thực tế (đã bao gồm equipment)"""
        return self.damage  # Damage đã được cộng equipment trong apply_equipment_bonuses()
    
    def get_effective_speed(self):
        """Lấy tốc độ thực tế (đã bao gồm equipment)"""
        return self.speed  # Speed đã được cộng equipment trong apply_equipment_bonuses()
    
    def get_max_hp_with_equipment(self):
        """Lấy max HP (đã bao gồm equipment)"""
        return self.max_hp  # Max HP đã được cộng equipment trong apply_equipment_bonuses()
    
    def can_revive(self):
        """Kiểm tra xem có thể hồi sinh không"""
        if self.has_used_revive:
            return False
        
        for equipment in self.equipped.values():
            if equipment and equipment.has_revive_effect:
                return True
        return False
    
    def trigger_revive(self):
        """Kích hoạt hiệu ứng hồi sinh"""
        for equipment in self.equipped.values():
            if equipment and equipment.has_revive_effect:
                max_hp = self.get_max_hp_with_equipment()
                self.hp = int(max_hp * equipment.revive_hp_percent / 100)
                self.has_used_revive = True
                self.dead = False
                print(f"Hồi sinh với {self.hp} HP!")
                return
    
    def has_slow_effect(self):
        """Kiểm tra xem có hiệu ứng làm chậm không"""
        for equipment in self.equipped.values():
            if equipment and equipment.has_slow_effect:
                return True
        return False
    
    def get_burn_effect(self):
        """Lấy thông tin hiệu ứng thiêu đốt"""
        for equipment in self.equipped.values():
            if equipment and equipment.has_burn_effect:
                return (equipment.burn_damage, equipment.burn_duration)
        return (0, 0)

    # --- Combat helpers ---
    def attack_hitbox(self):
        """Trả về Rect của vùng attack (hitbox) dựa trên vị trí, hướng, và loại đòn.
        Kích thước hitbox nhỏ hơn rect nhân vật để yêu cầu đứng gần mới trúng.
        """
        # Basic player rect (derive from current image size)
        if self.image:
            rect = self.image.get_rect(topleft=(self.x, self.y))
        else:
            rect = pygame.Rect(self.x, self.y, 40, 80)

        # Attack reach and size
        reach = 60  # pixels in front of player
        width = 50
        height = rect.height // 2
        # Vertical center aligned to upper half where hits register
        hit_y = self.y + rect.height // 4

        if getattr(self, 'flip', False):
            # facing left: hitbox to the left
            hit_x = self.x - reach
        else:
            # facing right: hitbox to the right
            hit_x = self.x + rect.width

        return pygame.Rect(hit_x, hit_y, width, height)
