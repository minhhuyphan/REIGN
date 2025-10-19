import pygame
import os
from ma_nguon.tien_ich import user_store


class RegisterScene:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(os.path.join('Tai_nguyen', 'font', 'Fz-Donsky.ttf'), 36)
        self.small_font = pygame.font.Font(os.path.join('Tai_nguyen', 'font', 'Fz-Donsky.ttf'), 24)
        self.username = ''
        self.password = ''
        self.confirm = ''
        self.active_field = 'username'  # or 'password' or 'confirm'
        self.message = ''

        # simple UI layout
        self.card = pygame.Rect(350, 180, 900, 380)
        self.input_rect = pygame.Rect(480, 240, 540, 48)
        self.pw_rect = pygame.Rect(480, 310, 540, 48)
        self.confirm_rect = pygame.Rect(480, 380, 540, 48)
        self.register_btn = pygame.Rect(560, 460, 200, 50)
        self.cancel_btn = pygame.Rect(800, 460, 200, 50)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                if self.active_field == 'username':
                    self.active_field = 'password'
                elif self.active_field == 'password':
                    self.active_field = 'confirm'
                else:
                    self.active_field = 'username'
            elif event.key == pygame.K_BACKSPACE:
                if self.active_field == 'username':
                    self.username = self.username[:-1]
                elif self.active_field == 'password':
                    self.password = self.password[:-1]
                else:
                    self.confirm = self.confirm[:-1]
            elif event.key == pygame.K_RETURN:
                self.try_register()
            else:
                ch = event.unicode
                if ch and len(ch) == 1 and ord(ch) >= 32:
                    if self.active_field == 'username':
                        self.username += ch
                    elif self.active_field == 'password':
                        self.password += ch
                    else:
                        self.confirm += ch
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.register_btn.collidepoint(event.pos):
                self.try_register()
            elif self.cancel_btn.collidepoint(event.pos):
                self.game.change_scene('menu')
            elif self.input_rect.collidepoint(event.pos):
                self.active_field = 'username'
            elif self.pw_rect.collidepoint(event.pos):
                self.active_field = 'password'
            elif self.confirm_rect.collidepoint(event.pos):
                self.active_field = 'confirm'

    def try_register(self):
        if not self.username or not self.password or not self.confirm:
            self.message = 'Vui lòng điền tất cả trường'
            return
        if self.password != self.confirm:
            self.message = 'Mật khẩu xác nhận không khớp'
            return
        ok = user_store.register_user(self.username, self.password)
        if ok:
            self.message = 'Đăng ký thành công'
            self.game.current_user = self.username
            try:
                user_store.save_current_user(self.username)
            except Exception:
                pass
            self.game.change_scene('menu')
        else:
            self.message = 'Username đã tồn tại'

    def update(self):
        pass

    def draw(self, screen):
        # Draw background
        screen.fill((20, 30, 50))

        # Card
        pygame.draw.rect(screen, (40, 50, 70), self.card, border_radius=10)
        pygame.draw.rect(screen, (255, 215, 0), self.card, 2, border_radius=10)

        title = self.font.render('Đăng ký tài khoản', True, (255, 215, 0))
        screen.blit(title, (self.card.x + 40, self.card.y + 20))

        # Inputs
        pygame.draw.rect(screen, (230,230,230), self.input_rect, border_radius=6)
        pygame.draw.rect(screen, (230,230,230), self.pw_rect, border_radius=6)
        pygame.draw.rect(screen, (230,230,230), self.confirm_rect, border_radius=6)

        u_text = self.small_font.render(self.username or 'Tên đăng nhập', True, (30,30,30) if self.username else (120,120,120))
        screen.blit(u_text, (self.input_rect.x + 12, self.input_rect.y + 10))
        p_text = self.small_font.render('*' * len(self.password) or 'Mật khẩu', True, (30,30,30) if self.password else (120,120,120))
        screen.blit(p_text, (self.pw_rect.x + 12, self.pw_rect.y + 10))
        c_text = self.small_font.render('*' * len(self.confirm) or 'Xác nhận mật khẩu', True, (30,30,30) if self.confirm else (120,120,120))
        screen.blit(c_text, (self.confirm_rect.x + 12, self.confirm_rect.y + 10))

        # Buttons
        pygame.draw.rect(screen, (100,200,100), self.register_btn, border_radius=8)
        r_text = self.small_font.render('Đăng ký', True, (10,10,10))
        screen.blit(r_text, (self.register_btn.x + 50, self.register_btn.y + 12))

        pygame.draw.rect(screen, (200,100,100), self.cancel_btn, border_radius=8)
        c_text = self.small_font.render('Hủy', True, (10,10,10))
        screen.blit(c_text, (self.cancel_btn.x + 80, self.cancel_btn.y + 12))

        # Message
        msg = self.small_font.render(self.message, True, (255,100,100))
        screen.blit(msg, (self.card.x + 40, self.card.y + 320))
