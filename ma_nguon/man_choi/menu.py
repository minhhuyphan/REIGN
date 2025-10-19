import pygame
import math
import random

class MenuScene:
    def __init__(self, game):
        self.game = game  # Tham chiếu đến GameManager hoặc SceneManager
        self.font = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 50)
        self.selected = 0

        # Dynamic menu based on login status; include leaderboard option
        if hasattr(game, 'current_user') and game.current_user:
            self.options = ["Chọn Map", "Trang bị", "Cửa hàng", "Xếp hạng", "Hướng dẫn", "Cài đặt", "Đăng xuất", "Thoát"]
        else:
            self.options = ["Chọn Map", "Trang bị", "Cửa hàng", "Xếp hạng", "Hướng dẫn", "Cài đặt", "Thoát"]

        # Animation variables
        self.bounce_offset = 0
        self.bounce_speed = 0.1
        self.title_scale = 0.5
        self.title_scale_speed = 0.02

        # Load background image
        try:
            self.background = pygame.image.load("Tai_nguyen/hinh_anh/giao_dien/bg.png")
            self.background = pygame.transform.scale(self.background, (self.game.WIDTH, self.game.HEIGHT))  # Scale to screen size
        except pygame.error:
            try:
                self.background = pygame.image.load("Tai_nguyen/hinh_anh/canh_nen/trang_sao.png")
                self.background = pygame.transform.scale(self.background, (self.game.WIDTH, self.game.HEIGHT))
            except pygame.error:
                self.background = None  # No background if both fail

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                # Dispatch by option label (safer than hard-coded indices)
                selected_text = self.options[self.selected]
                if selected_text == "Chọn Map":
                    self.game.change_scene("chon_map")
                elif selected_text == "Trang bị":
                    self.game.change_scene("equipment")
                elif selected_text == "Cửa hàng":
                    self.game.change_scene("shop")
                elif selected_text == "Xếp hạng":
                    self.game.change_scene("leaderboard")
                elif selected_text == "Hướng dẫn":
                    self.game.change_scene("help")
                elif selected_text == "Cài đặt":
                    self.game.change_scene("settings")
                elif selected_text == "Đăng xuất":
                    # logout
                    from ma_nguon.tien_ich import user_store
                    user_store.clear_session()
                    self.game.current_user = None
                    self.game.profile = None
                    self.game.change_scene('login')
                elif selected_text == "Thoát":
                    self.game.running = False


    def update(self):
        # Title scale animation
        if self.title_scale < 1.0:
            self.title_scale = min(1.0, self.title_scale + self.title_scale_speed)

        # Bounce animation for selected button
        self.bounce_offset = 5 * math.sin(pygame.time.get_ticks() * self.bounce_speed / 100)

    def draw(self, screen):
        # Draw background image if available, otherwise fill with solid color
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill((30, 30, 60))

        # Title with scaling animation and royal gold color
        title_color = (255, 215, 0)
        shadow_color = (139, 69, 19)

        # Create title with scaling animation
        title_surface = self.font.render("GAME PYGAME", True, title_color)
        scaled_width = int(title_surface.get_width() * self.title_scale)
        scaled_height = int(title_surface.get_height() * self.title_scale)
        title_scaled = pygame.transform.scale(title_surface, (scaled_width, scaled_height))

        # Create shadow with same scaling
        title_shadow_surface = self.font.render("GAME PYGAME", True, shadow_color)
        shadow_scaled_width = int(title_shadow_surface.get_width() * self.title_scale)
        shadow_scaled_height = int(title_shadow_surface.get_height() * self.title_scale)
        shadow_scaled = pygame.transform.scale(title_shadow_surface, (shadow_scaled_width, shadow_scaled_height))

        # Draw shadow and main title
        shadow_x = screen.get_width() // 2 - shadow_scaled.get_width() // 2 + 3
        shadow_y = 103
        screen.blit(shadow_scaled, (shadow_x, shadow_y))
        title_x = screen.get_width() // 2 - title_scaled.get_width() // 2
        title_y = 100
        screen.blit(title_scaled, (title_x, title_y))

        # Show current user at top-right and gold balance
        user_text = ''
        gold_text = ''
        if hasattr(self.game, 'current_user') and self.game.current_user:
            user_text = f"Người chơi: {self.game.current_user}"
            # load profile to get gold
            try:
                from ma_nguon.core import profile_manager
                profile = profile_manager.load_profile(self.game.current_user)
                gold_text = f"Vàng: {profile.get('gold', 0)}"
            except Exception:
                gold_text = ''
        else:
            user_text = "Chưa đăng nhập"
        user_surf = pygame.font.Font("tai_nguyen/font/Fz-Futurik.ttf", 20).render(user_text, True, (200,200,200))
        screen.blit(user_surf, (screen.get_width() - user_surf.get_width() - 20, 20))
        if gold_text:
            gold_surf = pygame.font.Font("tai_nguyen/font/Fz-Futurik.ttf", 18).render(gold_text, True, (255, 215, 0))
            screen.blit(gold_surf, (screen.get_width() - gold_surf.get_width() - 20, 44))
        
        # Menu options with medieval-themed colors and bounce effect
        # Use self.options directly without modification
        options = self.options

        for i, text in enumerate(options):
            # Calculate base position
            base_y = 250 + i*70
            option_y = base_y

            # Màu sắc đặc biệt cho Map Công Nghệ
            if text == "Map Công Nghệ":
                color = (0, 255, 255) if i == self.selected else (0, 191, 255)
            else:
                color = (255, 140, 0) if i == self.selected else (245, 245, 220)

            if i == self.selected:
                option_y += self.bounce_offset
                option_surface = self.font.render(text, True, color)
                bg_rect = pygame.Rect(0, 0, option_surface.get_width() + 40, option_surface.get_height() + 20)
                bg_rect.center = (screen.get_width() // 2, option_y + option_surface.get_height() // 2)

                # Nền & viền đặc biệt
                if text == "Map Công Nghệ":
                    pygame.draw.rect(screen, (30, 30, 80), bg_rect, border_radius=10)
                    pygame.draw.rect(screen, (0, 255, 255), bg_rect, 3, border_radius=10)
                    glow_color = (0, 255, 255)
                else:
                    pygame.draw.rect(screen, (80, 80, 100), bg_rect, border_radius=10)
                    pygame.draw.rect(screen, color, bg_rect, 3, border_radius=10)
                    glow_color = (255, 215, 0)

                glow_option = self.font.render(text, True, glow_color)
                screen.blit(glow_option, (screen.get_width() // 2 - glow_option.get_width() // 2 + 1, option_y + 1))
                screen.blit(glow_option, (screen.get_width() // 2 - glow_option.get_width() // 2 - 1, option_y - 1))

            option = self.font.render(text, True, color)
            screen.blit(option, (screen.get_width() // 2 - option.get_width() // 2, option_y))

        # Hiệu ứng hạt xung quanh Map Công Nghệ khi được chọn
        try:
            tech_map_index = options.index("Map Công Nghệ")
        except ValueError:
            tech_map_index = None
        if tech_map_index is not None and self.selected == tech_map_index:
            for _ in range(5):
                offset_x = random.randint(-100, 100)
                offset_y = random.randint(-20, 20)
                particle_x = screen.get_width() // 2 + offset_x
                particle_y = 230 + tech_map_index * 60 + offset_y + self.bounce_offset
                pygame.draw.circle(screen, (0, 255, 255), (int(particle_x), int(particle_y)), 2)
