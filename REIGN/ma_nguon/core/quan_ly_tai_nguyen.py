import pygame, os

def load_images(folder, target_size=(150, 150)):
    images = []
    if not os.path.exists(folder):
        return [pygame.Surface(target_size, pygame.SRCALPHA)]
    for file in sorted(os.listdir(folder)):
        if not file.lower().endswith((".png", ".jpg")):
            continue
        path = os.path.join(folder, file)
        img = pygame.image.load(path).convert_alpha()

        # scale ảnh theo tỉ lệ nhưng không vượt quá target_size
        w, h = img.get_size()
        scale_ratio = min(target_size[0] / w, target_size[1] / h)
        new_size = (int(w * scale_ratio), int(h * scale_ratio))
        img = pygame.transform.scale(img, new_size)

        # tạo canvas rỗng với size chuẩn và đặt nhân vật xuống đáy
        canvas = pygame.Surface(target_size, pygame.SRCALPHA)
        x = (target_size[0] - new_size[0]) // 2
        y = target_size[1] - new_size[1]
        canvas.blit(img, (x, y))
        images.append(canvas)
    return images


# --- Hàm load âm thanh an toàn ---
def load_sound_safe(path, default_volume=1.0):
    try:
        s = pygame.mixer.Sound(path)
        s.set_volume(default_volume)
        return s
    except Exception:
        return None
