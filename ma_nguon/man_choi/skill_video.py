"""
Skill Video Player - Phát video kỹ năng trong game
"""
import pygame
import os

# Try importing cv2, make it optional
try:
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False
    print("[WARNING] OpenCV (cv2) not installed. Skill videos will show placeholder.")

class SkillVideoPlayer:
    """Phát video kỹ năng và xử lý callback sau khi video kết thúc"""
    
    def __init__(self, video_path, on_finish_callback=None):
        """
        Args:
            video_path: Đường dẫn tới file video
            on_finish_callback: Function sẽ được gọi khi video kết thúc
        """
        self.video_path = video_path
        self.on_finish_callback = on_finish_callback
        self.finished = False
        self.cap = None
        self.fps = 30
        self.frame_delay = 1000 // self.fps
        self.last_frame_time = pygame.time.get_ticks()
        self.current_frame = None
        
        # White flash effect khi video kết thúc - ENHANCED
        self.flash_active = False
        self.flash_start_time = 0
        self.flash_duration = 1000  # 1 giây flash trắng (tăng từ 500ms)
        self.full_white_duration = 300  # 300ms đầu là 100% trắng, sau đó mới fade
        
        # Audio support - tự động tìm và phát âm thanh
        self.audio_channel = None
        self._load_audio(video_path)
        
        # Check if video exists and cv2 is available
        if not HAS_CV2:
            print(f"[SKILL VIDEO] cv2 not available, skipping video: {video_path}")
            self.finished = True
            if self.on_finish_callback:
                self.on_finish_callback()
            return
            
        if not os.path.exists(video_path):
            print(f"[SKILL VIDEO] Video not found: {video_path}")
            self.finished = True
            if self.on_finish_callback:
                self.on_finish_callback()
            return
        
        # Initialize video capture
        try:
            self.cap = cv2.VideoCapture(video_path)
            if not self.cap.isOpened():
                print(f"[SKILL VIDEO] Failed to open video: {video_path}")
                self.finished = True
                if self.on_finish_callback:
                    self.on_finish_callback()
                return
            
            self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 30
            self.frame_delay = int(1000 / self.fps)
            print(f"[SKILL VIDEO] Loaded: {video_path} @ {self.fps} FPS")
            
            # Start audio playback if available
            self._play_audio()
            
        except Exception as e:
            print(f"[SKILL VIDEO] Error loading video: {e}")
            self.finished = True
            if self.on_finish_callback:
                self.on_finish_callback()
    
    def _load_audio(self, video_path):
        """Tự động tìm và load file audio tương ứng với video"""
        # Chuyển từ video path sang audio path
        # VD: Tai_nguyen/video/skill_chien_than.mp4 
        #  → Tai_nguyen/am_thanh/skill/skill_chien_than.mp3
        
        video_dir = os.path.dirname(video_path)
        video_filename = os.path.basename(video_path)
        video_name = os.path.splitext(video_filename)[0]  # skill_chien_than
        
        # Thử các định dạng audio
        audio_formats = ['.mp3', '.wav', '.ogg']
        
        for audio_ext in audio_formats:
            # Tìm trong thư mục skill audio
            audio_path = os.path.join(video_dir, '..', 'am_thanh', 'skill', video_name + audio_ext)
            audio_path = os.path.normpath(audio_path)
            
            if os.path.exists(audio_path):
                try:
                    self.audio_sound = pygame.mixer.Sound(audio_path)
                    print(f"[SKILL AUDIO] Loaded: {audio_path}")
                    return
                except Exception as e:
                    print(f"[SKILL AUDIO] Error loading {audio_path}: {e}")
        
        # Không tìm thấy audio - không sao, video vẫn phát
        self.audio_sound = None
        print(f"[SKILL AUDIO] No audio found for {video_filename} (optional)")
    
    def _play_audio(self):
        """Phát audio nếu có"""
        if self.audio_sound:
            try:
                self.audio_channel = self.audio_sound.play()
                print("[SKILL AUDIO] Playing audio...")
            except Exception as e:
                print(f"[SKILL AUDIO] Error playing audio: {e}")
    
    def update(self):
        """Cập nhật video frame"""
        # Cập nhật white flash effect
        if self.flash_active:
            now = pygame.time.get_ticks()
            if now - self.flash_start_time >= self.flash_duration:
                self.flash_active = False
                # Gọi callback sau khi flash kết thúc
                if self.on_finish_callback:
                    self.on_finish_callback()
            return
        
        if self.finished or not self.cap:
            return
        
        now = pygame.time.get_ticks()
        if now - self.last_frame_time >= self.frame_delay:
            self.last_frame_time = now
            
            ret, frame = self.cap.read()
            if not ret:
                # Video ended - Bắt đầu white flash
                self.finished = True
                self.cap.release()
                print("[SKILL VIDEO] Video finished - Starting white flash!")
                self.flash_active = True
                self.flash_start_time = pygame.time.get_ticks()
                return
            
            # Convert BGR to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Rotate 90 degrees and flip for correct orientation
            frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            self.current_frame = frame
    
    def draw(self, screen):
        """Vẽ video lên màn hình - FULL SCREEN"""
        screen_w, screen_h = screen.get_size()
        
        # Nếu đang flash trắng - ENHANCED VERSION
        if self.flash_active:
            now = pygame.time.get_ticks()
            elapsed = now - self.flash_start_time
            
            # GIAI ĐOẠN 1: 300ms đầu - 100% TRẮNG (alpha = 255)
            if elapsed < self.full_white_duration:
                alpha = 255
            # GIAI ĐOẠN 2: 700ms sau - fade out từ 255 -> 0
            else:
                fade_elapsed = elapsed - self.full_white_duration
                fade_duration = self.flash_duration - self.full_white_duration
                progress = fade_elapsed / fade_duration  # 0.0 -> 1.0
                alpha = int(255 * (1 - progress))
            
            # Vẽ màn hình trắng với alpha tính toán
            flash_surface = pygame.Surface((screen_w, screen_h))
            flash_surface.fill((255, 255, 255))
            flash_surface.set_alpha(alpha)
            screen.blit(flash_surface, (0, 0))
            return
        
        if self.finished or not self.current_frame:
            return
        
        # Stretch video to fill full screen
        scaled_frame = pygame.transform.scale(self.current_frame, (screen_w, screen_h))
        
        # Draw at (0, 0) to cover entire screen
        screen.blit(scaled_frame, (0, 0))
    
    def skip(self):
        """Bỏ qua video"""
        if self.cap:
            self.cap.release()
        # Stop audio if playing
        if self.audio_channel:
            self.audio_channel.stop()
        self.finished = True
        if self.on_finish_callback:
            self.on_finish_callback()
    
    def cleanup(self):
        """Dọn dẹp resources"""
        if self.cap:
            self.cap.release()
        # Stop audio if playing
        if self.audio_channel:
            self.audio_channel.stop()
        self.finished = True
