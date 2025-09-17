import pygame, os, sys

pygame.init()
pygame.mixer.init()

# Kích thước cửa sổ
WIDTH, HEIGHT = 1600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Có Âm Thanh Chuẩn Thư Mục")
clock = pygame.time.Clock()

# --- Load ảnh nền ---
bg_image = pygame.image.load("Tai_nguyen/hinh_anh/giao_dien/bg.png").convert()
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

# --- Load nhạc nền ---
pygame.mixer.music.load("Tai_nguyen/am_thanh/nhac/bg.crdownload")
pygame.mixer.music.play(-1)  # phát lặp vô hạn

# Hàm load ảnh + scale
def load_images(folder, target_size=(300, 300)):
    images = []
    if not os.path.exists(folder):
        return [pygame.Surface(target_size, pygame.SRCALPHA)]
    for file in sorted(os.listdir(folder), key=lambda x: int(x.split(".")[0])):
        path = os.path.join(folder, file)
        img = pygame.image.load(path).convert_alpha()

        # scale ảnh theo tỉ lệ nhưng không vượt quá target_size
        w, h = img.get_size()
        scale_ratio = min(target_size[0] / w, target_size[1] / h)
        new_size = (int(w * scale_ratio), int(h * scale_ratio))
        img = pygame.transform.scale(img, new_size)

        # tạo canvas rỗng với size chuẩn
        canvas = pygame.Surface(target_size, pygame.SRCALPHA)
        # căn giữa ngang, và "đặt chân" nhân vật ở đáy
        x = (target_size[0] - new_size[0]) // 2
        y = target_size[1] - new_size[1]
        canvas.blit(img, (x, y))
        images.append(canvas)
    return images


# Class Nhân vật
class Character:
    def __init__(self, x, y, folder, controls, color=(255,255,255), auto=False):
        self.x = x
        self.y = y
        self.base_y = y  # Lưu vị trí y gốc để nhảy
        self.flip = False
        self.hp = 100
        self.speed = 4
        self.controls = controls or {}
        self.color = color
        self.auto = auto

        # Load animations (nếu folder không có thì trả surface rỗng)
        self.animations = {
            "dung_yen": load_images(os.path.join(folder, "dung_yen")),
            "chay":     load_images(os.path.join(folder, "chay")),
            "danh":     load_images(os.path.join(folder, "danh")),
            "da":       load_images(os.path.join(folder, "da")),
            "nga":      load_images(os.path.join(folder, "nga")),
            "do":       load_images(os.path.join(folder, "do")),
            "nhay":     load_images(os.path.join(folder, "nhay")),
        }

        # Âm thanh RIÊNG cho mỗi nhân vật (nếu file không tồn tại, catch exception)
        def load_sound_safe(path, default_volume=1.0):
            try:
                s = pygame.mixer.Sound(path)
                s.set_volume(default_volume)
                return s
            except Exception:
                return None

        self.sound_punch = load_sound_safe("Tai_nguyen/am_thanh/hieu_ung/danh.mp3", 1.0)
        self.sound_kick  = load_sound_safe("Tai_nguyen/am_thanh/hieu_ung/da.mp3", 1.0)
        self.sound_hit   = load_sound_safe("Tai_nguyen/am_thanh/hieu_ung/trung.mp3", 1.0)
        self.sound_run   = load_sound_safe("Tai_nguyen/am_thanh/hieu_ung/chay.mp3", 0.4)

        # Trạng thái action tổng quát
        self.state = "dung_yen"
        self.frame = 0
        self.image = self.animations[self.state][0]
        self.animation_cooldown = 120
        self.last_update = pygame.time.get_ticks()
        self.actioning = False       # đang thực hiện action khóa (danh/da/do/nhay)
        self.action_type = ""        # loại action hiện tại
        self.jumping = False
        self.jump_vel = 0
        self.running_sound_playing = False

    def start_action(self, action_type):
        """Bắt đầu 1 action (danh/da/do/nhay). Nếu đang action thì bỏ qua."""
        if self.actioning:
            return
        self.actioning = True
        self.action_type = action_type
        self.state = action_type
        self.frame = 0
        # nếu bắt đầu nhảy thì bật vật lý nhảy
        if action_type == "nhay":
            if not self.jumping:
                self.jumping = True
                self.jump_vel = -18
        # tắt tiếng chạy nếu đang phát
        if self.running_sound_playing and self.sound_run:
            self.sound_run.stop()
            self.running_sound_playing = False
        # phát âm thanh tương ứng (chỉ một lần khi action bắt đầu)
        if action_type == "danh" and self.sound_punch:
            self.sound_punch.play()
        elif action_type == "da" and self.sound_kick:
            self.sound_kick.play()
        elif action_type == "do":  # optional sound for block
            pass

    def play_animation(self):
        """Cập nhật frame animation; trả về True nếu vòng animation kết thúc (animation_done)."""
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
        # Nếu đã ngã hoàn toàn thì đứng yên
        if self.state == "nga" and self.frame == len(self.animations["nga"]) - 1:
            return

        moving = False

        # --- Nếu đang action khóa kiểu tấn công/đỡ (danh/da/do) thì chỉ cho play animation ---
        if self.actioning and self.action_type in ["danh", "da", "do"]:
            animation_done = self.play_animation()
            if animation_done:
                # kết thúc action -> trả về idle
                self.actioning = False
                self.action_type = ""
                if self.state in ["danh", "da", "do"]:
                    self.state = "dung_yen"
            return

        # --- Xử lý input (chỉ nếu không đang action khác) ---
        if not self.auto and keys and self.hp > 0:
            # Nhảy (bắt đầu action nhay nhưng vẫn cho phép di chuyển ngang trong lúc nhảy)
            if self.controls.get("jump") and keys[self.controls["jump"]] and not self.actioning and not self.jumping:
                self.start_action("nhay")
            # Đỡ (bắt đầu action "do")
            elif self.controls.get("defend") and keys[self.controls["defend"]] and not self.actioning:
                self.start_action("do")
            # Tấn công/đá
            elif keys[self.controls.get("attack", -1)] and not self.actioning:
                self.start_action("danh")
            elif keys[self.controls.get("kick", -1)] and not self.actioning:
                self.start_action("da")
            # Di chuyển (chỉ khi không đang action khóa khác; cho phép di chuyển khi đang nhảy)
            else:
                # nếu đang nhảy nhưng không actioning (shouldn't happen), vẫn cho di chuyển
                if keys[self.controls.get("right", -1)] and (not self.actioning or self.action_type == "nhay"):
                    self.state = "chay"
                    self.flip = False
                    self.x += self.speed
                    moving = True
                elif keys[self.controls.get("left", -1)] and (not self.actioning or self.action_type == "nhay"):
                    self.state = "chay"
                    self.flip = True
                    self.x -= self.speed
                    moving = True
                else:
                    # nếu không di chuyển và không đang nhảy -> idle
                    if not self.jumping and not self.actioning:
                        self.state = "dung_yen"

        # --- Enemy auto logic (nếu là enemy và không đang action) ---
        if self.auto and self.hp > 0 and target and not self.actioning:
            distance = abs(self.x - target.x)
            if distance < 120:
                self.start_action("danh")
            else:
                self.state = "dung_yen"

        # --- Xử lý nhảy vật lý ---
        if self.jumping:
            self.y += self.jump_vel
            self.jump_vel += 2  # trọng lực
            # Cho phép di chuyển ngang khi nhảy (nếu phím đang giữ)
            if keys and keys[self.controls.get("right", -1)]:
                self.x += self.speed
                self.flip = False
            if keys and keys[self.controls.get("left", -1)]:
                self.x -= self.speed
                self.flip = True
            if self.y >= self.base_y:
                self.y = self.base_y
                self.jumping = False
                # nếu animation nhay cũng đã kết thúc, hủy action
                if self.actioning and self.action_type == "nhay":
                    # chờ cho play_animation trả về animation_done
                    pass

        # Nếu hết máu thì ngã
        if self.hp <= 0 and not (self.actioning and self.action_type == "nga"):
            self.start_action("nga")

        # --- Điều khiển âm thanh chạy ---
        if self.sound_run:
            if moving and not self.running_sound_playing and not self.actioning:
                # chỉ phát chạy khi có di chuyển và không đang action khóa (trừ nhay mình cho phép)
                self.sound_run.play(-1)
                self.running_sound_playing = True
            elif (not moving or self.actioning and self.action_type != "nhay") and self.running_sound_playing:
                # dừng khi không di chuyển hoặc khi bắt đầu action khác (ngoại trừ nhay)
                self.sound_run.stop()
                self.running_sound_playing = False

        # --- Cập nhật animation chung ---
        animation_done = self.play_animation()

        # Nếu đang nhảy và vừa hạ đất + animation nhảy đã xong => kết thúc action nhay
        if self.actioning and self.action_type == "nhay":
            if (not self.jumping) and animation_done:
                self.actioning = False
                self.action_type = ""
                self.state = "dung_yen"

        # Nếu đang defend (do) nhưng user muốn nó chạy cả vòng: handled earlier in actioning block

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(img, (self.x, self.y))
        # Thanh máu
        pygame.draw.rect(surface, (100,100,100), (self.x, self.y-20, 100, 10)) # nền
        pygame.draw.rect(surface, self.color, (self.x, self.y-20, self.hp, 10)) # máu


# --- Khởi tạo nhân vật ---
folder = "Tai_nguyen/hinh_anh/nhan_vat"

controls_p1 = {
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT,
    "attack": pygame.K_a,
    "kick": pygame.K_s,
    "defend": pygame.K_d,   # phím đỡ
    "jump": pygame.K_w,     # phím nhảy
}
player1 = Character(100, 300, folder, controls_p1, color=(0,255,0))
enemy = Character(700, 300, folder, {}, color=(255,0,0), auto=True)

# --- Game loop ---
running = True
while running:
    clock.tick(60)
    # Vẽ ảnh nền
    screen.blit(bg_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player1.update(keys)
    enemy.update(keys, target=player1)

    # Kiểm tra va chạm
    rect1 = player1.image.get_rect(topleft=(player1.x, player1.y))
    rect2 = enemy.image.get_rect(topleft=(enemy.x, enemy.y))

    if rect1.colliderect(rect2):
        # Nếu enemy đang đỡ thì không bị trừ máu
        if player1.state in ["danh", "da"] and enemy.hp > 0 and not enemy.actioning:
            enemy.hp -= 1
            if player1.sound_hit:
                player1.sound_hit.play()
        # Nếu player1 đang đỡ thì không bị trừ máu
        if enemy.state in ["danh", "da"] and player1.hp > 0 and not player1.actioning:
            player1.hp -= 1
            if enemy.sound_hit:
                enemy.sound_hit.play()

    player1.draw(screen)
    enemy.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()
