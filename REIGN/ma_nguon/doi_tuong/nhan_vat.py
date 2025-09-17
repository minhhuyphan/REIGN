import pygame, os
from ma_nguon.core.quan_ly_tai_nguyen import load_images, load_sound_safe

class Character:
    def __init__(self, x, y, folder, controls, color=(255, 255, 255), auto=False):
        self.x = x
        self.y = y
        self.base_y = y
        self.flip = False
        self.hp = 100
        self.speed = 4
        self.controls = controls or {}
        self.color = color
        self.auto = auto

        # Load animations
        self.animations = {
            "dung_yen": load_images(os.path.join(folder, "dung_yen")),
            "chay": load_images(os.path.join(folder, "chay")),
            "danh": load_images(os.path.join(folder, "danh")),
            "da": load_images(os.path.join(folder, "da")),
            "nga": load_images(os.path.join(folder, "nga")),
            "do": load_images(os.path.join(folder, "do")),
            "nhay": load_images(os.path.join(folder, "nhay")),
        }

        # Âm thanh
        self.sound_punch = load_sound_safe("tai_nguyen/am_thanh/hieu_ung/danh.mp3", 1.0)
        self.sound_kick = load_sound_safe("tai_nguyen/am_thanh/hieu_ung/da.mp3", 1.0)
        self.sound_hit = load_sound_safe("tai_nguyen/am_thanh/hieu_ung/trung.mp3", 1.0)
        self.sound_run = load_sound_safe("tai_nguyen/am_thanh/hieu_ung/chay.mp3", 0.4)

        # Trạng thái
        self.state = "dung_yen"
        self.frame = 0
        self.image = self.animations[self.state][0]
        self.animation_cooldown = 120
        self.last_update = pygame.time.get_ticks()
        self.actioning = False
        self.action_type = ""
        self.jumping = False
        self.jump_vel = 0
        self.running_sound_playing = False

    def start_action(self, action_type):
        if self.actioning:
            return
        self.actioning = True
        self.action_type = action_type
        self.state = action_type
        self.frame = 0

        if action_type == "nhay" and not self.jumping:
            self.jumping = True
            self.jump_vel = -18
            if self.running_sound_playing and self.sound_run:
                self.sound_run.stop()
                self.running_sound_playing = False

        # phát âm thanh
        if action_type == "danh" and self.sound_punch:
            self.sound_punch.play()
        elif action_type == "da" and self.sound_kick:
            self.sound_kick.play()

    def play_animation(self):
        now = pygame.time.get_ticks()
        animation_done = False
        if now - self.last_update > self.animation_cooldown:
            self.last_update = now
            self.frame += 1
            if self.frame >= len(self.animations[self.state]):
                animation_done = True
                self.frame = 0
            self.image = self.animations[self.state][self.frame]
        return animation_done

    def update(self, keys=None, target=None):
        if self.state == "nga" and self.frame == len(self.animations["nga"]) - 1:
            return

        moving = False

        # --- Xử lý action khóa ---
        if self.actioning and self.action_type in ["danh", "da", "do"]:
            animation_done = self.play_animation()
            if animation_done:
                self.actioning = False
                self.action_type = ""
                self.state = "dung_yen"
            return

        # --- Input người chơi ---
        if not self.auto and keys and self.hp > 0:
            if self.controls.get("jump") and keys[self.controls["jump"]] and not self.jumping:
                self.start_action("nhay")
            elif self.controls.get("defend") and keys[self.controls["defend"]] and not self.actioning:
                self.start_action("do")
            elif keys[self.controls.get("attack", -1)] and not self.actioning:
                self.start_action("danh")
            elif keys[self.controls.get("kick", -1)] and not self.actioning:
                self.start_action("da")
            else:
                if keys[self.controls.get("right", -1)]:
                    self.state = "chay"
                    self.flip = False
                    self.x += self.speed
                    moving = True
                elif keys[self.controls.get("left", -1)]:
                    self.state = "chay"
                    self.flip = True
                    self.x -= self.speed
                    moving = True
                else:
                    if not self.jumping and not self.actioning:
                        self.state = "dung_yen"

        # --- Enemy auto ---
        if self.auto and self.hp > 0 and target and not self.actioning:
            distance = abs(self.x - target.x)
            if distance < 120:
                self.start_action("danh")
            else:
                self.state = "dung_yen"

        # --- Nhảy ---
        if self.jumping:
            self.y += self.jump_vel
            self.jump_vel += 2
            if self.y >= self.base_y:
                self.y = self.base_y
                self.jumping = False
                if self.actioning and self.action_type == "nhay":
                    self.actioning = False
                    self.action_type = ""
                    self.state = "dung_yen"

        # --- Âm thanh chạy ---
        if self.sound_run:
            if moving and not self.running_sound_playing and not self.actioning:
                self.sound_run.play(-1)
                self.running_sound_playing = True
            elif (not moving or (self.actioning and self.action_type != "nhay")) and self.running_sound_playing:
                self.sound_run.stop()
                self.running_sound_playing = False

        self.play_animation()

        if self.hp <= 0 and not (self.actioning and self.action_type == "nga"):
            self.start_action("nga")

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(img, (self.x, self.y))

        # thanh máu
        pygame.draw.rect(surface, (100, 100, 100), (self.x, self.y - 20, 100, 10))
        pygame.draw.rect(surface, self.color, (self.x, self.y - 20, self.hp, 10))
