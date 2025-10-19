import pygame
import os
from ma_nguon.tien_ich import user_store
from ma_nguon.man_choi.register import RegisterScene


class LoginScene:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(os.path.join('Tai_nguyen', 'font', 'Fz-Donsky.ttf'), 36)
        self.small_font = pygame.font.Font(os.path.join('Tai_nguyen', 'font', 'Fz-Donsky.ttf'), 24)
        self.username = ''
        self.password = ''
        self.active_field = 'username'  # or 'password'
        self.message = ''

        # Improved UI layout - centered card
        self.card = pygame.Rect(350, 180, 900, 380)
        self.input_rect = pygame.Rect(480, 260, 540, 48)
        self.pw_rect = pygame.Rect(480, 330, 540, 48)
        self.login_btn = pygame.Rect(520, 410, 200, 50)
        self.register_btn = pygame.Rect(760, 410, 200, 50)

        # caret timer for blinking cursor
        self.caret_visible = True
        self.last_caret_toggle = pygame.time.get_ticks()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                self.active_field = 'password' if self.active_field == 'username' else 'username'
            elif event.key == pygame.K_BACKSPACE:
                if self.active_field == 'username':
                    self.username = self.username[:-1]
                else:
                    self.password = self.password[:-1]
            elif event.key == pygame.K_RETURN:
                self.try_login()
            else:
                ch = event.unicode
                if ch and len(ch) == 1 and ord(ch) >= 32:
                    if self.active_field == 'username':
                        self.username += ch
                    else:
                        self.password += ch
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.login_btn.collidepoint(event.pos):
                self.try_login()
            elif self.register_btn.collidepoint(event.pos):
                self.game.change_scene('register')
            elif self.input_rect.collidepoint(event.pos):
                self.active_field = 'username'
            elif self.pw_rect.collidepoint(event.pos):
                self.active_field = 'password'

    def try_login(self):
        if not self.username or not self.password:
            self.message = 'Vui lòng nhập username và mật khẩu'
            return
        ok = user_store.authenticate(self.username, self.password)
        if ok:
            self.message = 'Đăng nhập thành công'
            # store current user in game
            self.game.current_user = self.username
            # persist session
            try:
                user_store.save_current_user(self.username)
            except Exception:
                pass
            # go to menu
            self.game.change_scene('menu')
        else:
            self.message = 'Sai username hoặc mật khẩu'

    def update(self):
        # blink caret
        now = pygame.time.get_ticks()
        if now - self.last_caret_toggle > 500:
            self.caret_visible = not self.caret_visible
            self.last_caret_toggle = now

    def draw_input_with_placeholder(self, screen, rect, text, placeholder, active):
        # Highlight active field
        bg_color = (255, 255, 200) if active else (235, 235, 235)
        pygame.draw.rect(screen, bg_color, rect, border_radius=6)
        
        # Draw golden border for active field
        if active:
            pygame.draw.rect(screen, (255, 215, 0), rect, 3, border_radius=6)
        
        display_text = text if text else placeholder
        color = (20,20,20) if text else (130,130,130)
        surf = self.small_font.render(display_text, True, color)
        screen.blit(surf, (rect.x + 12, rect.y + 10))
        
        # caret - blinking cursor
        if active and self.caret_visible:
            text_width = self.small_font.size(text)[0] if text else 0
            caret_x = rect.x + 12 + text_width
            caret_y = rect.y + 10
            pygame.draw.line(screen, (20,20,20), (caret_x, caret_y), (caret_x, caret_y + 32), 2)

    def draw(self, screen):
        screen.fill((20, 30, 50))

        # Card
        pygame.draw.rect(screen, (40, 50, 70), self.card, border_radius=10)
        pygame.draw.rect(screen, (255, 215, 0), self.card, 2, border_radius=10)

        title = self.font.render('Đăng nhập', True, (255, 215, 0))
        screen.blit(title, (self.card.x + 40, self.card.y + 20))

        # Inputs (masked password)
        self.draw_input_with_placeholder(screen, self.input_rect, self.username, 'Tên đăng nhập', self.active_field == 'username')
        masked = '*' * len(self.password)
        self.draw_input_with_placeholder(screen, self.pw_rect, masked, 'Mật khẩu', self.active_field == 'password')

        # Buttons
        pygame.draw.rect(screen, (100,180,100), self.login_btn, border_radius=8)
        l_text = self.small_font.render('Đăng nhập', True, (10,10,10))
        screen.blit(l_text, (self.login_btn.x + 50, self.login_btn.y + 14))

        pygame.draw.rect(screen, (100,100,180), self.register_btn, border_radius=8)
        r_text = self.small_font.render('Đăng ký', True, (10,10,10))
        screen.blit(r_text, (self.register_btn.x + 60, self.register_btn.y + 14))

        # message
        msg = self.small_font.render(self.message, True, (255, 100, 100))
        screen.blit(msg, (self.card.x + 40, self.card.y + 320))
