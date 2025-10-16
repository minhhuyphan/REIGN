import pygame
from ma_nguon.core import profile_manager


class SpinScene:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font("tai_nguyen/font/Fz-Futurik.ttf", 28)
        self.small_font = pygame.font.Font("tai_nguyen/font/Fz-Futurik.ttf", 18)

        # spin config
        self.equipment_pool = [
            'cung_bang_lam',
            'kiem_rong',
            'giap_anh_sang',
            'giay_thien_than'
        ]
        self.spin_cost = 200
        self.spinning = False
        self.spin_timer = 0
        self.spin_duration = 90
        self.spin_result = None
        self.spin_highlight_idx = 0
        self.spin_start_idx = 0
        self.spin_total_steps = 0

        self.message = ''
        self.msg_timer = 0

        # button rects
        self.back_rect = None
        self.spin_button_rect = None

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.change_scene('shop')
                return
            if event.key == pygame.K_p:
                self.start_spin()
                return
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            if self.back_rect and self.back_rect.collidepoint(mx, my):
                self.game.change_scene('shop')
                return
            if self.spin_button_rect and self.spin_button_rect.collidepoint(mx, my):
                self.start_spin()
                return

    def start_spin(self):
        user = getattr(self.game, 'current_user', None)
        if not user:
            self._set_message('Vui lòng đăng nhập để quay', 180)
            return
        profile = profile_manager.load_profile(user)
        gold = profile.get('gold', 0)
        if gold < self.spin_cost:
            self._set_message('Không đủ vàng để quay', 180)
            return
        # deduct and save
        profile['gold'] = gold - self.spin_cost
        profile_manager.save_profile(user, profile)
        self.game.profile = profile

        import random
        reward = random.choice(self.equipment_pool)
        self.spin_result = reward
        self.spinning = True
        self.spin_timer = 0
        self.spin_start_idx = self.spin_highlight_idx
        pool_len = max(1, len(self.equipment_pool))
        offset = (self.equipment_pool.index(reward) - self.spin_start_idx) % pool_len
        self.spin_total_steps = pool_len * 4 + offset
        self.spin_duration = 90
        self._set_message('Đang quay...', 60)

    def finish_spin(self):
        user = getattr(self.game, 'current_user', None)
        if user:
            profile = profile_manager.load_profile(user)
            owned = profile.get('owned_equipment', [])
            if self.spin_result and self.spin_result not in owned:
                owned.append(self.spin_result)
            profile['owned_equipment'] = owned
            profile_manager.save_profile(user, profile)
            self.game.profile = profile
        self._set_message(f'Bạn nhận được: {self.spin_result}', 240)
        self.spinning = False

    def _set_message(self, text: str, frames: int = 120):
        self.message = text
        self.msg_timer = frames

    def update(self):
        if self.msg_timer > 0:
            self.msg_timer -= 1
            if self.msg_timer == 0:
                self.message = ''
        if getattr(self, 'spinning', False):
            self.spin_timer += 1
            t = min(1.0, float(self.spin_timer) / max(1, getattr(self, 'spin_duration', 90)))
            total = getattr(self, 'spin_total_steps', len(self.equipment_pool))
            step = int(t * total)
            self.spin_highlight_idx = (getattr(self, 'spin_start_idx', 0) + step) % max(1, len(self.equipment_pool))
            if self.spin_timer >= getattr(self, 'spin_duration', 90):
                self.finish_spin()

    def draw(self, screen):
        screen.fill((18, 24, 40))
        title = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 44).render('Vòng Quay Trang Bị', True, (255, 215, 0))
        screen.blit(title, (screen.get_width()//2 - title.get_width()//2, 30))

        # back button
        self.back_rect = pygame.Rect(30, 30, 120, 40)
        pygame.draw.rect(screen, (80,80,120), self.back_rect)
        back_label = self.small_font.render('Quay lại', True, (255,255,255))
        screen.blit(back_label, (self.back_rect.x + self.back_rect.width//2 - back_label.get_width()//2, self.back_rect.y + 8))

        # draw pool
        pool_x = screen.get_width()//2 - 280
        pool_y = 140
        gap = 140
        item_w = 96
        for idx, eq in enumerate(self.equipment_pool):
            cx = pool_x + idx * gap
            rect = pygame.Rect(cx, pool_y, item_w, item_w)
            color = (120,120,120)
            if self.spinning and idx == self.spin_highlight_idx:
                color = (255,215,0)
            pygame.draw.rect(screen, color, rect, border_radius=8)
            lbl = self.small_font.render(eq, True, (240,240,240))
            screen.blit(lbl, (rect.x + rect.width//2 - lbl.get_width()//2, rect.y + rect.height + 6))

        # spin button
        self.spin_button_rect = pygame.Rect(screen.get_width()//2 - 80, pool_y + item_w + 60, 160, 44)
        pygame.draw.rect(screen, (180,50,50), self.spin_button_rect, border_radius=8)
        spin_label = self.font.render(f'Quay ({self.spin_cost})', True, (255,255,255))
        screen.blit(spin_label, (self.spin_button_rect.x + self.spin_button_rect.width//2 - spin_label.get_width()//2, self.spin_button_rect.y + 6))

        if self.message:
            msg_surf = self.small_font.render(self.message, True, (255,255,255))
            screen.blit(msg_surf, (screen.get_width()//2 - msg_surf.get_width()//2, screen.get_height() - 80))
