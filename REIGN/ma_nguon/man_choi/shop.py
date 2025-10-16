import pygame
import os
from ma_nguon.core import profile_manager


class ShopScene:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font("tai_nguyen/font/Fz-Futurik.ttf", 28)
        # Catalog mirrors character select (id, name, folder, price)
        self.catalog = [
            { 'id': 'chien_binh', 'name': 'Chiến binh', 'folder': 'tai_nguyen/hinh_anh/nhan_vat/chien_binh', 'price': 0 },
            { 'id': 'ninja', 'name': 'Ninja', 'folder': 'tai_nguyen/hinh_anh/nhan_vat/ninja', 'price': 300 },
            { 'id': 'vo_si', 'name': 'Võ sĩ', 'folder': 'tai_nguyen/hinh_anh/nhan_vat/vo_si', 'price': 400 },
            { 'id': 'chien_than_lac_hong', 'name': 'Chiến Thần Lạc Hồng', 'folder': 'tai_nguyen/hinh_anh/nhan_vat/chien_than_lac_hong', 'price': 500 },
            { 'id': 'tho_san_quai_vat', 'name': 'Thợ Săn Quái Vật', 'folder': 'tai_nguyen/hinh_anh/nhan_vat/tho_san_quai_vat', 'price': 350 }
        ]

        # load previews
        for item in self.catalog:
            preview_path = os.path.join(item['folder'], 'dung_yen', '0.png')
            try:
                item['preview'] = pygame.image.load(preview_path).convert_alpha()
            except Exception:
                s = pygame.Surface((100,150), pygame.SRCALPHA)
                s.fill((120,120,120,180))
                item['preview'] = s

        # layout state
        self.buttons = []  # buy button rects indexed by item index
        self.message = ''
        self.msg_timer = 0
        self.selected_idx = 0
        self.input_cooldown = 0
        # Spin wheel state
        # simple equipment pool for spin rewards (ids matching EquipmentManager.all_equipment keys)
        self.equipment_pool = [
            'cung_bang_lam',
            'kiem_rong',
            'giap_anh_sang',
            'giay_thien_than'
        ]
        self.spin_cost = 200  # vàng để quay
        self.spinning = False
        self.spin_timer = 0
        self.spin_duration = 90  # frames
        self.spin_result = None
        self.spin_highlight_idx = 0
        # navigation button rects
        self.go_spin_rect = None

    def create_buttons(self):
        # deprecated
        pass

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
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
                    # attempt purchase on selected
                    self.buy_by_index(self.selected_idx)
                    self.input_cooldown = 8
                    return
                elif event.key == pygame.K_p:
                    # press P to open spin (quick key)
                    self.start_spin()
                    return
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            # check buy buttons
            for idx, rect in enumerate(self.buttons):
                if rect.collidepoint(mx, my):
                    self.buy_by_index(idx)
                    self.selected_idx = idx
                    return
            # check navigation to SpinScene
            if getattr(self, 'go_spin_rect', None) and self.go_spin_rect.collidepoint(mx, my):
                self.game.change_scene('spin')
                return

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

    # --- Spin wheel methods ---
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
        # Deduct gold immediately
        profile['gold'] = gold - self.spin_cost
        # Save and update in-memory
        profile_manager.save_profile(user, profile)
        self.game.profile = profile
        # Choose reward now so we can animate to it
        import random
        reward = random.choice(self.equipment_pool)
        self.spin_result = reward
        # Start spin animation (deterministic end)
        self.spinning = True
        self.spin_timer = 0
        self.spin_start_idx = self.spin_highlight_idx
        # compute total steps so the pointer will land on reward at end
        try:
            reward_idx = self.equipment_pool.index(reward)
        except ValueError:
            reward_idx = 0
        pool_len = max(1, len(self.equipment_pool))
        offset = (reward_idx - self.spin_start_idx) % pool_len
        self.spin_total_steps = pool_len * 4 + offset
        self.spin_duration = 90
        self._set_message('Đang quay...', 60)

    def finish_spin(self):
        # persist reward (self.spin_result chosen at start_spin)
        user = getattr(self.game, 'current_user', None)
        if user:
            profile = profile_manager.load_profile(user)
            owned = profile.get('owned_equipment', [])
            reward = self.spin_result
            if reward and reward not in owned:
                owned.append(reward)
            profile['owned_equipment'] = owned
            profile_manager.save_profile(user, profile)
            self.game.profile = profile
        # show message
        self._set_message(f'Bạn nhận được: {self.spin_result}', 240)
        self.spinning = False

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
        # handle spinning animation
        if getattr(self, 'spinning', False):
            self.spin_timer += 1
            t = min(1.0, float(self.spin_timer) / max(1, getattr(self, 'spin_duration', 90)))
            # linear progress over total steps
            total = getattr(self, 'spin_total_steps', len(self.equipment_pool))
            step = int(t * total)
            self.spin_highlight_idx = (getattr(self, 'spin_start_idx', 0) + step) % max(1, len(self.equipment_pool))
            if self.spin_timer >= getattr(self, 'spin_duration', 90):
                # finish
                self.finish_spin()

    def draw(self, screen):
        screen.fill((30, 30, 60))
        title = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 48).render('Cửa hàng nhân vật', True, (255, 215, 0))
        screen.blit(title, (screen.get_width()//2 - title.get_width()//2, 30))

        # Draw gold balance
        user = getattr(self.game, 'current_user', None)
        gold = 0
        if user:
            profile = profile_manager.load_profile(user)
            gold = profile.get('gold', 0)
        gold_text = self.font.render(f'Vàng: {gold}', True, (255, 255, 0))
        screen.blit(gold_text, (screen.get_width() - gold_text.get_width() - 40, 20))

        # Navigation: Go to Spin Scene button
        self.go_spin_rect = pygame.Rect(40, 70, 140, 36)
        pygame.draw.rect(screen, (70, 130, 200), self.go_spin_rect, border_radius=6)
        spin_nav_label = pygame.font.Font("tai_nguyen/font/Fz-Futurik.ttf", 20).render('Vòng Quay', True, (255,255,255))
        screen.blit(spin_nav_label, (self.go_spin_rect.x + self.go_spin_rect.width//2 - spin_nav_label.get_width()//2, self.go_spin_rect.y + 6))

        # Draw character grid similar to selection screen
        num = len(self.catalog)
        spacing = screen.get_width() // (num + 1)
        self.buttons = []
        for i, item in enumerate(self.catalog):
            pos_x = spacing * (i + 1)
            pos_y = screen.get_height() // 2 - 80

            # frame
            main_rect = pygame.Rect(pos_x - 100, pos_y - 20, 200, 260)
            # highlight selected
            if i == getattr(self, 'selected_idx', 0):
                pygame.draw.rect(screen, (255, 215, 0), main_rect, 4)
            else:
                pygame.draw.rect(screen, (120,120,120), main_rect, 3)

            # name
            name_color = (255,215,0)
            name = self.font.render(item['name'], True, name_color)
            screen.blit(name, (pos_x - name.get_width()//2, pos_y - 50))

            # preview
            preview = item.get('preview')
            pv_scale = 0.4
            preview = pygame.transform.scale(preview, (int(preview.get_width()*pv_scale), int(preview.get_height()*pv_scale)))
            screen.blit(preview, (pos_x - preview.get_width()//2, pos_y - 10))

            # price / ownership
            cid = item['id']
            owned = False
            if user:
                profile = profile_manager.load_profile(user)
                owned = cid in profile.get('purchased_characters', [])
            else:
                owned = (item.get('price',0) == 0)

            stats_y = pos_y + 120
            font_stats = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 20)
            # draw buy button
            btn_rect = pygame.Rect(pos_x - 70, stats_y + 50, 140, 36)
            if owned:
                pygame.draw.rect(screen, (40,120,40), btn_rect)
                btn_text = self.font.render('Sở hữu', True, (255,255,255))
            else:
                pygame.draw.rect(screen, (120,40,40), btn_rect)
                price_label = 'Miễn phí' if item.get('price',0)==0 else str(item.get('price'))
                btn_text = self.font.render(f'Mua: {price_label}', True, (255,255,255))
            screen.blit(btn_text, (btn_rect.x + btn_rect.width//2 - btn_text.get_width()//2, btn_rect.y + 4))
            self.buttons.append(btn_rect)

            # if not owned draw translucent overlay hint
            if not owned:
                overlay = pygame.Surface((200,260), pygame.SRCALPHA)
                overlay.fill((0,0,0,120))
                screen.blit(overlay, (pos_x-100, pos_y-20))
                lock_text = font_stats.render(f'Mua: {item.get("price",0)} vàng', True, (255,215,0))
                screen.blit(lock_text, (pos_x - lock_text.get_width()//2, pos_y + 180))

        # draw message if any
        if self.message:
            msg_surf = pygame.font.Font("tai_nguyen/font/Fz-Futurik.ttf", 24).render(self.message, True, (255,255,255))
            screen.blit(msg_surf, (screen.get_width()//2 - msg_surf.get_width()//2, screen.get_height()-80))

        # Note: spin wheel UI removed from shop; use 'Vòng Quay' button to go to dedicated SpinScene.
