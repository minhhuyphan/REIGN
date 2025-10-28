import pygame
import os
import math
from ma_nguon.core import profile_manager


class ShopScene:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font("tai_nguyen/font/Fz-Futurik.ttf", 28)
        
        # Animation
        self.hover_scale = {}
        self.particle_timer = 0
        self.title_pulse = 0
        
        # Gacha button
        self.gacha_button = None
        self.gacha_hover = 0.0
        
        # Character card rects for hover detection
        self.card_rects = []
        
        # Catalog mirrors character select (id, name, folder, price)
        self.catalog = [
            { 'id': 'chien_binh', 'name': 'Chiến binh', 'folder': 'tai_nguyen/hinh_anh/nhan_vat/chien_binh', 'price': 0 },
            { 'id': 'ninja', 'name': 'Ninja', 'folder': 'tai_nguyen/hinh_anh/nhan_vat/ninja', 'price': 300 },
            { 'id': 'vo_si', 'name': 'Võ sĩ', 'folder': 'tai_nguyen/hinh_anh/nhan_vat/vo_si', 'price': 400 },
            { 'id': 'chien_than_lac_hong', 'name': 'Chiến Thần Lạc Hồng', 'folder': 'tai_nguyen/hinh_anh/nhan_vat/chien_than_lac_hong', 'price': 100000000 },
            { 'id': 'tho_san_quai_vat', 'name': 'Thợ Săn Quái Vật', 'folder': 'tai_nguyen/hinh_anh/nhan_vat/tho_san_quai_vat', 'price': 350 }
        ]

        # load previews
        for i, item in enumerate(self.catalog):
            preview_path = os.path.join(item['folder'], 'dung_yen', '0.png')
            try:
                item['preview'] = pygame.image.load(preview_path).convert_alpha()
            except Exception:
                s = pygame.Surface((100,150), pygame.SRCALPHA)
                s.fill((120,120,120,180))
                item['preview'] = s
            
            # Initialize hover animation
            self.hover_scale[i] = 0.0

        # layout state
        self.buttons = []  # buy button rects indexed by item index
        self.message = ''
        self.msg_timer = 0
        self.selected_idx = 0
        self.input_cooldown = 0
        
        # Confirmation dialog
        self.show_confirmation = False
        self.confirm_item_idx = None
        self.yes_button = None
        self.no_button = None
        self.confirm_hover = {'yes': 0.0, 'no': 0.0}

    def create_buttons(self):
        # deprecated
        pass

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            # If confirmation dialog is open, handle Y/N keys
            if self.show_confirmation:
                if event.key == pygame.K_y or event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    # Yes - confirm purchase
                    self.buy_by_index(self.confirm_item_idx)
                    self.show_confirmation = False
                    self.confirm_item_idx = None
                    return
                elif event.key == pygame.K_n or event.key == pygame.K_ESCAPE:
                    # No - cancel purchase
                    self.show_confirmation = False
                    self.confirm_item_idx = None
                    return
            
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_s:
                self.game.change_scene('menu')
                return
            # keyboard navigation
            if self.input_cooldown == 0:
                if event.key == pygame.K_LEFT:
                    self.selected_idx = max(0, self.selected_idx - 1)
                    self.input_cooldown = 8
                    return
                elif event.key == pygame.K_RIGHT:
                    self.selected_idx = min(len(self.catalog)-1, self.selected_idx + 1)
                    self.input_cooldown = 8
                    return
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    # Show confirmation dialog
                    self._show_purchase_confirmation(self.selected_idx)
                    self.input_cooldown = 8
                    return
                elif event.key == pygame.K_g:
                    # Go to gacha scene
                    self.game.change_scene('gacha_trang_bi')
                    return
        
        # Mouse hover
        elif event.type == pygame.MOUSEMOTION:
            mx, my = event.pos
            
            # If confirmation dialog is open, handle its hover
            if self.show_confirmation:
                hovering_dialog = False
                
                if self.yes_button and self.yes_button.collidepoint(mx, my):
                    self.confirm_hover['yes'] = min(1.0, self.confirm_hover['yes'] + 0.2)
                    hovering_dialog = True
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    self.confirm_hover['yes'] = max(0.0, self.confirm_hover['yes'] - 0.2)
                
                if self.no_button and self.no_button.collidepoint(mx, my):
                    self.confirm_hover['no'] = min(1.0, self.confirm_hover['no'] + 0.2)
                    hovering_dialog = True
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    self.confirm_hover['no'] = max(0.0, self.confirm_hover['no'] - 0.2)
                
                if not hovering_dialog:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                return
            
            # Check if hovering over any card
            hovering_any = False
            
            # Update gacha button hover
            if self.gacha_button and self.gacha_button.collidepoint(mx, my):
                self.gacha_hover = min(1.0, self.gacha_hover + 0.2)
                hovering_any = True
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                self.gacha_hover = max(0.0, self.gacha_hover - 0.2)
            
            # Update card hover animations
            for idx in range(len(self.catalog)):
                if idx < len(self.card_rects) and self.card_rects[idx]:
                    if self.card_rects[idx].collidepoint(mx, my):
                        self.hover_scale[idx] = min(1.0, self.hover_scale[idx] + 0.15)
                        hovering_any = True
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        self.hover_scale[idx] = max(0.0, self.hover_scale[idx] - 0.15)
                else:
                    self.hover_scale[idx] = max(0.0, self.hover_scale[idx] - 0.15)
            
            # Update button hover (for additional feedback)
            for idx, rect in enumerate(self.buttons):
                if rect and rect.collidepoint(mx, my):
                    hovering_any = True
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            
            # Reset cursor if not hovering anything
            if not hovering_any:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            
            # If confirmation dialog is open, handle button clicks
            if self.show_confirmation:
                if self.yes_button and self.yes_button.collidepoint(mx, my):
                    # Confirm purchase
                    self.buy_by_index(self.confirm_item_idx)
                    self.show_confirmation = False
                    self.confirm_item_idx = None
                    return
                elif self.no_button and self.no_button.collidepoint(mx, my):
                    # Cancel purchase
                    self.show_confirmation = False
                    self.confirm_item_idx = None
                    return
                else:
                    # Click outside dialog - close it
                    self.show_confirmation = False
                    self.confirm_item_idx = None
                    return
            
            # Check gacha button
            if self.gacha_button and self.gacha_button.collidepoint(mx, my):
                self.game.change_scene('gacha_trang_bi')
                return
            
            # Check character cards (click anywhere on card to show confirmation)
            for idx in range(len(self.catalog)):
                if idx < len(self.card_rects) and self.card_rects[idx]:
                    if self.card_rects[idx].collidepoint(mx, my):
                        self.selected_idx = idx
                        # Show confirmation dialog instead of buying directly
                        self._show_purchase_confirmation(idx)
                        return
            
            # Fallback: check buy buttons specifically
            for idx, rect in enumerate(self.buttons):
                if rect and rect.collidepoint(mx, my):
                    self.buy_by_index(idx)
                    self.selected_idx = idx
                    return

    def _show_purchase_confirmation(self, idx: int):
        """Show confirmation dialog for purchase"""
        item = self.catalog[idx]
        user = getattr(self.game, 'current_user', None)
        if not user:
            self._set_message('Vui lòng đăng nhập để mua', 180)
            return
        
        profile = profile_manager.load_profile(user)
        purchased = profile.get('purchased_characters', [])
        
        # If already owned, don't show confirmation
        if item['id'] in purchased:
            self._set_message('Đã sở hữu', 120)
            return
        
        # Show confirmation dialog
        self.show_confirmation = True
        self.confirm_item_idx = idx

    def buy_character(self, cid):
        # legacy entrypoint (not used)
        return

    def buy_by_index(self, idx: int):
        item = self.catalog[idx]
        cid = item['id']
        user = getattr(self.game, 'current_user', None)
        if not user:
            self._set_message('Vui lòng đăng nhập để mua', 180)
            return
        profile = profile_manager.load_profile(user)
        purchased = profile.get('purchased_characters', [])
        if cid in purchased:
            self._set_message('Đã sở hữu', 120)
            return
        price = item.get('price', 0)
        gold = profile.get('gold', 0)
        if gold < price:
            self._set_message('Không đủ vàng', 180)
            return
        # Deduct and save
        profile['gold'] = gold - price
        purchased.append(cid)
        profile['purchased_characters'] = purchased
        profile_manager.save_profile(user, profile)
        # update in-memory profile
        self.game.profile = profile
        self._set_message(f'Mua thành công {item.get("name")}', 180)

    def _set_message(self, text: str, frames: int = 120):
        self.message = text
        self.msg_timer = frames

    def update(self):
        # message timer
        if self.msg_timer > 0:
            self.msg_timer -= 1
            if self.msg_timer == 0:
                self.message = ''
        # input cooldown for keyboard navigation
        if getattr(self, 'input_cooldown', 0) > 0:
            self.input_cooldown -= 1
        
        # Title pulse animation
        self.title_pulse = math.sin(pygame.time.get_ticks() * 0.003) * 5
        
        # Particle timer
        self.particle_timer += 1

    def draw(self, screen):
        # Gradient background
        for y in range(screen.get_height()):
            progress = y / screen.get_height()
            r = int(15 + (35 - 15) * progress)
            g = int(15 + (25 - 15) * progress)
            b = int(45 + (65 - 45) * progress)
            pygame.draw.line(screen, (r, g, b), (0, y), (screen.get_width(), y))
        
        # Vẽ stars background
        import random
        random.seed(42)
        for _ in range(80):
            x = random.randint(0, screen.get_width())
            y = random.randint(0, screen.get_height() // 2)
            size = random.randint(1, 3)
            alpha = random.randint(100, 255)
            star_surf = pygame.Surface((size, size), pygame.SRCALPHA)
            star_surf.fill((255, 255, 255, alpha))
            screen.blit(star_surf, (x, y))
        
        # Title với shadow và animation
        title_font = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 56)
        title_text = 'CỬA HÀNG NHÂN VẬT'
        
        # Shadow
        title_shadow = title_font.render(title_text, True, (0, 0, 0))
        shadow_x = screen.get_width()//2 - title_shadow.get_width()//2 + 3
        shadow_y = 23 + int(self.title_pulse)
        screen.blit(title_shadow, (shadow_x, shadow_y))
        
        # Main title
        title = title_font.render(title_text, True, (255, 215, 0))
        title_x = screen.get_width()//2 - title.get_width()//2
        title_y = 20 + int(self.title_pulse)
        screen.blit(title, (title_x, title_y))

        # Draw gold balance với design đẹp
        user = getattr(self.game, 'current_user', None)
        gold = 0
        if user:
            profile = profile_manager.load_profile(user)
            gold = profile.get('gold', 0)
        
        # Gold panel với background
        gold_panel = pygame.Surface((280, 60), pygame.SRCALPHA)
        pygame.draw.rect(gold_panel, (40, 30, 10, 200), gold_panel.get_rect(), border_radius=12)
        pygame.draw.rect(gold_panel, (255, 215, 0, 150), gold_panel.get_rect(), 3, border_radius=12)
        screen.blit(gold_panel, (screen.get_width() - 300, 95))
        
        gold_icon = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 32).render('💰', True, (255, 215, 0))
        screen.blit(gold_icon, (screen.get_width() - 290, 103))
        
        gold_text = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 28).render(f'{gold:,}', True, (255, 215, 0))
        screen.blit(gold_text, (screen.get_width() - 245, 113))
        
        # Draw GACHA button (nâng cấp design với hover effect)
        gacha_w, gacha_h = 240, 55
        
        # Hover scale effect
        hover_boost = int(self.gacha_hover * 8)
        gacha_scaled_w = gacha_w + hover_boost
        gacha_scaled_h = gacha_h + int(hover_boost * 0.5)
        
        self.gacha_button = pygame.Rect(screen.get_width() - gacha_w - 30 - hover_boost//2, 
                                        170 - int(hover_boost * 0.25), 
                                        gacha_scaled_w, gacha_scaled_h)
        
        # Gradient background cho button
        gacha_surf = pygame.Surface((gacha_scaled_w, gacha_scaled_h), pygame.SRCALPHA)
        for y in range(gacha_scaled_h):
            progress = y / gacha_scaled_h
            # Brighter colors when hovering (clamp to 0-255)
            brightness = int(self.gacha_hover * 30)
            r = min(255, int(80 + brightness + (120 - 80 + brightness) * progress))
            g = min(255, int(40 + brightness//2 + (60 - 40 + brightness//2) * progress))
            b = min(255, int(150 + brightness + (200 - 150 + brightness) * progress))
            pygame.draw.line(gacha_surf, (r, g, b, 220), (0, y), (gacha_scaled_w, y))
        
        screen.blit(gacha_surf, (self.gacha_button.x, self.gacha_button.y))
        
        # Border với glow effect khi hover (clamp to 0-255)
        border_color = (min(255, 150 + int(self.gacha_hover * 50)), 
                       min(255, 80 + int(self.gacha_hover * 80)), 
                       255)
        border_width = 3 + int(self.gacha_hover * 2)
        pygame.draw.rect(screen, border_color, self.gacha_button, border_width, border_radius=12)
        
        # Shine effect
        shine_offset = (pygame.time.get_ticks() // 100) % 40 - 20
        shine_surf = pygame.Surface((gacha_scaled_w, gacha_scaled_h), pygame.SRCALPHA)
        shine_alpha = 80 + int(self.gacha_hover * 40)
        pygame.draw.line(shine_surf, (255, 255, 255, shine_alpha), 
                        (shine_offset, 0), (shine_offset + 30, gacha_scaled_h), 3)
        screen.blit(shine_surf, (self.gacha_button.x, self.gacha_button.y))
        
        gacha_text = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 24).render('🎰 VÒNG QUAY', True, (255, 255, 255))
        screen.blit(gacha_text, (self.gacha_button.centerx - gacha_text.get_width()//2, 
                                 self.gacha_button.centery - gacha_text.get_height()//2))

        # Draw character grid với thiết kế đẹp hơn
        num = len(self.catalog)
        card_w = 220
        card_h = 320
        gap = 25
        total_width = num * card_w + (num - 1) * gap
        start_x = (screen.get_width() - total_width) // 2
        
        self.buttons = []
        self.card_rects = []  # Reset card rects
        
        for i, item in enumerate(self.catalog):
            pos_x = start_x + i * (card_w + gap) + card_w // 2
            pos_y = screen.get_height() // 2 - 20
            
            # Hover scale effect
            scale_factor = 1.0 + self.hover_scale.get(i, 0) * 0.05
            scaled_w = int(card_w * scale_factor)
            scaled_h = int(card_h * scale_factor)
            
            # Main card rect for click detection
            main_rect = pygame.Rect(pos_x - scaled_w // 2, pos_y, scaled_w, scaled_h)
            self.card_rects.append(main_rect)  # Store for hover detection
            
            # Shadow
            shadow_offset = 8
            shadow_rect = pygame.Rect(pos_x - scaled_w // 2 + shadow_offset, 
                                      pos_y + shadow_offset, scaled_w, scaled_h)
            shadow_surf = pygame.Surface((scaled_w, scaled_h), pygame.SRCALPHA)
            pygame.draw.rect(shadow_surf, (0, 0, 0, 100), (0, 0, scaled_w, scaled_h), border_radius=15)
            screen.blit(shadow_surf, (shadow_rect.x, shadow_rect.y))
            
            # Check ownership
            cid = item['id']
            owned = False
            if user:
                profile = profile_manager.load_profile(user)
                owned = cid in profile.get('purchased_characters', [])
            else:
                owned = (item.get('price',0) == 0)
            
            # Card background với gradient
            card_surf = pygame.Surface((scaled_w, scaled_h), pygame.SRCALPHA)
            
            for y in range(scaled_h):
                progress = y / scaled_h
                if i == self.selected_idx:
                    # Gold gradient cho selected
                    r = int(50 + (70 - 50) * progress)
                    g = int(40 + (55 - 40) * progress)
                    b = int(10 + (20 - 10) * progress)
                    alpha = 230
                elif owned:
                    # Green gradient cho owned
                    r = int(20 + (30 - 20) * progress)
                    g = int(50 + (70 - 50) * progress)
                    b = int(30 + (45 - 30) * progress)
                    alpha = 220
                else:
                    # Blue gradient cho chưa mua
                    r = int(25 + (35 - 25) * progress)
                    g = int(35 + (50 - 35) * progress)
                    b = int(55 + (75 - 55) * progress)
                    alpha = 210
                pygame.draw.line(card_surf, (r, g, b, alpha), (0, y), (scaled_w, y))
            
            screen.blit(card_surf, (main_rect.x, main_rect.y))
            
            # Multi-layer border effect cho selected với pulse animation
            if i == self.selected_idx:
                pulse = math.sin(pygame.time.get_ticks() * 0.004) * 0.5 + 0.5  # 0 to 1
                
                for layer in range(3):
                    border_offset = layer * 2 + int(pulse * 3)
                    border_alpha = int((100 - layer * 25) * (0.7 + pulse * 0.3))
                    border_rect = pygame.Rect(main_rect.x - border_offset, main_rect.y - border_offset,
                                             scaled_w + border_offset * 2, scaled_h + border_offset * 2)
                    pygame.draw.rect(screen, (255, 215, 0, border_alpha), border_rect, 2, border_radius=15)
                
                # Main border với animated width
                main_border_width = 4 + int(pulse * 2)
                pygame.draw.rect(screen, (255, 215, 0), main_rect, main_border_width, border_radius=15)
            else:
                border_color = (100, 200, 150) if owned else (100, 150, 200)
                pygame.draw.rect(screen, border_color, main_rect, 3, border_radius=15)
            
            # Name với shadow
            name_font = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 24)
            name_color = (255, 215, 0) if i == self.selected_idx else (220, 220, 255) if owned else (180, 180, 200)
            
            name_shadow = name_font.render(item['name'], True, (0, 0, 0))
            screen.blit(name_shadow, (pos_x - name_shadow.get_width()//2 + 2, pos_y - 38))
            
            name = name_font.render(item['name'], True, name_color)
            screen.blit(name, (pos_x - name.get_width()//2, pos_y - 40))

            # Preview image
            preview = item.get('preview')
            pv_scale = 0.45
            preview = pygame.transform.scale(preview, (int(preview.get_width()*pv_scale), int(preview.get_height()*pv_scale)))
            screen.blit(preview, (pos_x - preview.get_width()//2, pos_y + 10))

            # Price label và button với design mới
            stats_y = pos_y + scaled_h - 85
            btn_y = pos_y + scaled_h - 55
            
            # Draw buy button với gradient và shadow
            btn_rect = pygame.Rect(pos_x - 90, btn_y, 180, 42)
            
            # Hover brightness boost for button
            is_btn_hovered = self.hover_scale.get(i, 0) > 0.3
            brightness_boost = int(self.hover_scale.get(i, 0) * 40) if is_btn_hovered else 0
            
            # Button shadow
            btn_shadow = pygame.Surface((180, 42), pygame.SRCALPHA)
            pygame.draw.rect(btn_shadow, (0, 0, 0, 80), (3, 3, 180, 42), border_radius=10)
            screen.blit(btn_shadow, (btn_rect.x, btn_rect.y))
            
            # Button gradient
            btn_surf = pygame.Surface((180, 42), pygame.SRCALPHA)
            for y in range(42):
                progress = y / 42
                if owned:
                    # Green gradient (clamp values to 0-255)
                    r = min(255, int(40 + brightness_boost + (60 - 40 + brightness_boost) * progress))
                    g = min(255, int(150 + brightness_boost + (200 - 150 + brightness_boost) * progress))
                    b = min(255, int(60 + brightness_boost//2 + (90 - 60 + brightness_boost//2) * progress))
                else:
                    # Red/Orange gradient (clamp values to 0-255)
                    r = min(255, int(180 + brightness_boost + (220 - 180 + brightness_boost) * progress))
                    g = min(255, int(60 + brightness_boost//2 + (90 - 60 + brightness_boost//2) * progress))
                    b = min(255, int(50 + brightness_boost//2 + (70 - 50 + brightness_boost//2) * progress))
                pygame.draw.line(btn_surf, (r, g, b, 255), (0, y), (180, y))
            
            screen.blit(btn_surf, (btn_rect.x, btn_rect.y))
            
            # Button border (thicker when hovering)
            border_color = (80, 255, 100) if owned else (255, 180, 80)
            border_width = 3 + (1 if is_btn_hovered else 0)
            pygame.draw.rect(screen, border_color, btn_rect, border_width, border_radius=10)
            
            # Button text
            btn_font = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 22)
            if owned:
                btn_text = btn_font.render('✓ SỞ HỮU', True, (255, 255, 255))
            else:
                price_label = 'MIỄN PHÍ' if item.get('price',0) == 0 else f'{item.get("price"):,} 💰'
                btn_text = btn_font.render(price_label, True, (255, 255, 255))
            
            screen.blit(btn_text, (btn_rect.centerx - btn_text.get_width()//2, 
                                  btn_rect.centery - btn_text.get_height()//2))
            self.buttons.append(btn_rect)

            # Locked character overlay với gradient
            if not owned:
                overlay = pygame.Surface((scaled_w, scaled_h), pygame.SRCALPHA)
                for y in range(scaled_h):
                    alpha = int(80 + (160 - 80) * (y / scaled_h))
                    pygame.draw.line(overlay, (0, 0, 0, alpha), (0, y), (scaled_w, y))
                screen.blit(overlay, (main_rect.x, main_rect.y))
                
                # Large centered lock icon
                lock_font = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 72)
                lock_text = lock_font.render('🔒', True, (200, 200, 200))
                lock_shadow = lock_font.render('🔒', True, (0, 0, 0))
                screen.blit(lock_shadow, (pos_x - lock_text.get_width()//2 + 2, pos_y + 52))
                screen.blit(lock_text, (pos_x - lock_text.get_width()//2, pos_y + 50))

        # Draw message với styled panel
        if self.message:
            msg_font = pygame.font.Font("tai_nguyen/font/Fz-Futurik.ttf", 26)
            msg_surf = msg_font.render(self.message, True, (255, 255, 255))
            
            # Background panel với gradient
            panel_w = msg_surf.get_width() + 60
            panel_h = msg_surf.get_height() + 30
            panel = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
            
            # Panel gradient
            for y in range(panel_h):
                progress = y / panel_h
                r = int(40 + (50 - 40) * progress)
                g = int(40 + (55 - 40) * progress)
                b = int(60 + (80 - 60) * progress)
                pygame.draw.line(panel, (r, g, b, 220), (0, y), (panel_w, y))
            
            # Border
            pygame.draw.rect(panel, (100, 150, 200, 180), panel.get_rect(), 3, border_radius=12)
            
            panel_x = screen.get_width()//2 - panel_w//2
            panel_y = screen.get_height() - 100
            
            # Panel shadow
            shadow = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
            pygame.draw.rect(shadow, (0, 0, 0, 100), (0, 0, panel_w, panel_h), border_radius=12)
            screen.blit(shadow, (panel_x + 3, panel_y + 3))
            
            screen.blit(panel, (panel_x, panel_y))
            screen.blit(msg_surf, (panel_x + 30, panel_y + 15))

        # Draw confirmation dialog
        if self.show_confirmation and self.confirm_item_idx is not None:
            item = self.catalog[self.confirm_item_idx]
            
            # Semi-transparent overlay
            overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            
            # Dialog box
            dialog_w, dialog_h = 500, 280
            dialog_x = screen.get_width()//2 - dialog_w//2
            dialog_y = screen.get_height()//2 - dialog_h//2
            
            # Dialog shadow
            shadow_surf = pygame.Surface((dialog_w, dialog_h), pygame.SRCALPHA)
            pygame.draw.rect(shadow_surf, (0, 0, 0, 150), (0, 0, dialog_w, dialog_h), border_radius=20)
            screen.blit(shadow_surf, (dialog_x + 5, dialog_y + 5))
            
            # Dialog background với gradient
            dialog_surf = pygame.Surface((dialog_w, dialog_h), pygame.SRCALPHA)
            for y in range(dialog_h):
                progress = y / dialog_h
                r = int(30 + (50 - 30) * progress)
                g = int(40 + (60 - 40) * progress)
                b = int(70 + (100 - 70) * progress)
                pygame.draw.line(dialog_surf, (r, g, b, 255), (0, y), (dialog_w, y))
            
            screen.blit(dialog_surf, (dialog_x, dialog_y))
            
            # Dialog border
            pygame.draw.rect(screen, (100, 150, 255), 
                           pygame.Rect(dialog_x, dialog_y, dialog_w, dialog_h), 4, border_radius=20)
            
            # Title
            title_font = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 32)
            title_text = title_font.render('XÁC NHẬN MUA', True, (255, 215, 0))
            title_shadow = title_font.render('XÁC NHẬN MUA', True, (0, 0, 0))
            screen.blit(title_shadow, (dialog_x + dialog_w//2 - title_text.get_width()//2 + 2, dialog_y + 27))
            screen.blit(title_text, (dialog_x + dialog_w//2 - title_text.get_width()//2, dialog_y + 25))
            
            # Character name
            name_font = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 28)
            name_text = name_font.render(f'"{item["name"]}"', True, (200, 220, 255))
            screen.blit(name_text, (dialog_x + dialog_w//2 - name_text.get_width()//2, dialog_y + 75))
            
            # Question text
            question_font = pygame.font.Font("tai_nguyen/font/Fz-Futurik.ttf", 24)
            question_text = question_font.render('Bạn có muốn mua nhân vật này?', True, (220, 220, 220))
            screen.blit(question_text, (dialog_x + dialog_w//2 - question_text.get_width()//2, dialog_y + 115))
            
            # Price display
            price = item.get('price', 0)
            if price > 0:
                price_font = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 26)
                price_text = price_font.render(f'Giá: {price:,} 💰', True, (255, 215, 0))
                screen.blit(price_text, (dialog_x + dialog_w//2 - price_text.get_width()//2, dialog_y + 150))
            else:
                free_font = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 26)
                free_text = free_font.render('MIỄN PHÍ', True, (100, 255, 100))
                screen.blit(free_text, (dialog_x + dialog_w//2 - free_text.get_width()//2, dialog_y + 150))
            
            # Buttons
            btn_w, btn_h = 180, 50
            btn_gap = 30
            yes_x = dialog_x + dialog_w//2 - btn_w - btn_gap//2
            no_x = dialog_x + dialog_w//2 + btn_gap//2
            btn_y = dialog_y + dialog_h - 75
            
            self.yes_button = pygame.Rect(yes_x, btn_y, btn_w, btn_h)
            self.no_button = pygame.Rect(no_x, btn_y, btn_w, btn_h)
            
            # YES button
            yes_scale = 1.0 + self.confirm_hover['yes'] * 0.1
            yes_brightness = int(self.confirm_hover['yes'] * 30)
            yes_surf = pygame.Surface((btn_w, btn_h), pygame.SRCALPHA)
            for y in range(btn_h):
                progress = y / btn_h
                r = min(255, int(50 + yes_brightness + (100 - 50 + yes_brightness) * progress))
                g = min(255, int(180 + yes_brightness + (230 - 180 + yes_brightness) * progress))
                b = min(255, int(80 + yes_brightness//2 + (120 - 80 + yes_brightness//2) * progress))
                pygame.draw.line(yes_surf, (r, g, b, 255), (0, y), (btn_w, y))
            
            screen.blit(yes_surf, (yes_x, btn_y))
            pygame.draw.rect(screen, (100, 255, 150), self.yes_button, 3, border_radius=12)
            
            yes_text = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 28).render('✓ CÓ', True, (255, 255, 255))
            screen.blit(yes_text, (yes_x + btn_w//2 - yes_text.get_width()//2, 
                                  btn_y + btn_h//2 - yes_text.get_height()//2))
            
            # NO button
            no_scale = 1.0 + self.confirm_hover['no'] * 0.1
            no_brightness = int(self.confirm_hover['no'] * 30)
            no_surf = pygame.Surface((btn_w, btn_h), pygame.SRCALPHA)
            for y in range(btn_h):
                progress = y / btn_h
                r = min(255, int(180 + no_brightness + (220 - 180 + no_brightness) * progress))
                g = min(255, int(60 + no_brightness//2 + (80 - 60 + no_brightness//2) * progress))
                b = min(255, int(60 + no_brightness//2 + (80 - 60 + no_brightness//2) * progress))
                pygame.draw.line(no_surf, (r, g, b, 255), (0, y), (btn_w, y))
            
            screen.blit(no_surf, (no_x, btn_y))
            pygame.draw.rect(screen, (255, 120, 120), self.no_button, 3, border_radius=12)
            
            no_text = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 28).render('✗ KHÔNG', True, (255, 255, 255))
            screen.blit(no_text, (no_x + btn_w//2 - no_text.get_width()//2, 
                                 btn_y + btn_h//2 - no_text.get_height()//2))
