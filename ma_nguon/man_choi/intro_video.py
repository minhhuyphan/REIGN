# ma_nguon/man_choi/intro_video.py


import pygame
import os
import cv2

class IntroVideoScene:
    def __init__(self, game):
        self.game = game
        self.video_path = os.path.join("Tai_nguyen", "video", "intro.mp4")
        self.audio_path = os.path.join("tai_nguyen", "am_thanh", "nhac", "intro.mp3")
        self.finished = False
        self.skipped = False
        self.current_frame = None
        # Tắt nhạc nền game
        try:
            pygame.mixer.music.stop()
        except Exception:
            pass
        # Phát nhạc intro.mp3
        if os.path.exists(self.audio_path):
            try:
                pygame.mixer.music.load(self.audio_path)
                pygame.mixer.music.play()
            except Exception as e:
                print(f"[WARNING] Không phát được nhạc intro: {e}")
        else:
            print(f"[WARNING] Không tìm thấy file nhạc intro: {self.audio_path}")
        # Mở video bằng OpenCV
        if not os.path.exists(self.video_path):
            print(f"[WARNING] Video intro không tìm thấy: {self.video_path}")
            self.finished = True
            self._restore_game_music()
            return
        self.cap = cv2.VideoCapture(self.video_path)
        if not self.cap.isOpened():
            print("[WARNING] Không thể mở video intro")
            self.finished = True
            self._restore_game_music()
            return
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.frame_delay = 1000 / self.fps if self.fps > 0 else 33
        self.last_frame_time = pygame.time.get_ticks()
        self.video_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.video_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        screen_width = self.game.WIDTH
        screen_height = self.game.HEIGHT
        scale_w = screen_width / self.video_width
        scale_h = screen_height / self.video_height
        scale = min(scale_w, scale_h)
        self.scaled_width = int(self.video_width * scale)
        self.scaled_height = int(self.video_height * scale)
        self.video_x = (screen_width - self.scaled_width) // 2
        self.video_y = (screen_height - self.scaled_height) // 2
        print(f"[INFO] Intro video loaded: {self.fps} fps, {self.video_width}x{self.video_height}")



    def _restore_game_music(self):
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("tai_nguyen/am_thanh/nhac/bg.mp3")
            pygame.mixer.music.play(-1)
            print("[INFO] Game background music restored")
        except Exception as e:
            print(f"[WARNING] Không thể khôi phục nhạc nền: {e}")

    def handle_event(self, event):
        # Không cho phép skip video bằng phím hoặc chuột nữa
        pass

    def skip_video(self):
        print("[INFO] Video intro skipped")
        self.skipped = True
        self.finished = True
        if hasattr(self, 'cap') and self.cap:
            self.cap.release()
        self._restore_game_music()

    def update(self):
        if self.finished:
            self._restore_game_music()
            self.game.change_scene("menu")
            return
        current_time = pygame.time.get_ticks()
        if current_time - self.last_frame_time >= self.frame_delay:
            self.last_frame_time = current_time
            ret, frame = self.cap.read()
            if not ret:
                print("[INFO] Video intro finished")
                self.finished = True
                self.cap.release()
                self._restore_game_music()
                return
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            if (self.scaled_width != self.video_width or self.scaled_height != self.video_height):
                frame = cv2.resize(frame, (self.scaled_width, self.scaled_height))
            frame = frame.swapaxes(0, 1)
            self.current_frame = pygame.surfarray.make_surface(frame)

    def draw(self, screen):
        screen.fill((0, 0, 0))
        if self.finished:
            return
        if hasattr(self, 'current_frame') and self.current_frame:
            frame_surface = pygame.transform.scale(self.current_frame, (self.game.WIDTH, self.game.HEIGHT))
            screen.blit(frame_surface, (0, 0))
        # Vẽ thanh loading màu trắng phía dưới video
        try:
            total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT)) if hasattr(self, 'cap') and self.cap else 1
            current_frame_idx = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES)) if hasattr(self, 'cap') and self.cap else 0
            progress = current_frame_idx / total_frames if total_frames > 0 else 0
            bar_width = int(self.game.WIDTH * progress)
            bar_height = 8
            bar_x = 0
            bar_y = self.game.HEIGHT - bar_height - 8
            pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height))
        except Exception:
            pass
        # Hiển thị phần trăm tiến trình phía trên thanh loading
        try:
            total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT)) if hasattr(self, 'cap') and self.cap else 1
            current_frame_idx = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES)) if hasattr(self, 'cap') and self.cap else 0
            percent = int((current_frame_idx / total_frames) * 100) if total_frames > 0 else 0
            font = pygame.font.Font(None, 28)
            percent_text = font.render(f"{percent}%", True, (255, 255, 255))
            percent_rect = percent_text.get_rect()
            percent_rect.centerx = self.game.WIDTH // 2
            percent_rect.bottom = self.game.HEIGHT - 16
            screen.blit(percent_text, percent_rect)
        except Exception:
            pass
