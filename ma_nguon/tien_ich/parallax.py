import pygame
import os

class ParallaxBackground:
    def __init__(self, screen_width, screen_height, map_width):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.map_width = map_width
        self.layers = []
        
    def add_layer(self, image_path, speed_factor=1.0, y_pos=0, scale_factor=1.0, repeat_x=True, above_player=False):
        """
        Thêm một lớp nền vào hệ thống parallax
        
        :param image_path: Đường dẫn đến file ảnh
        :param speed_factor: Tốc độ di chuyển tương đối so với camera (0: đứng yên, 1: cùng tốc độ camera)
        :param y_pos: Vị trí y trên màn hình (0 là trên cùng)
        :param scale_factor: Hệ số tỷ lệ, ảnh sẽ được co giãn theo tỷ lệ này
        :param repeat_x: Có lặp lại ảnh theo chiều ngang không
        :param above_player: Lớp này có hiển thị phía trên nhân vật không
        """
        try:
            # Nếu caller truyền sẵn một Surface, dùng trực tiếp
            if isinstance(image_path, pygame.Surface):
                image = image_path
            else:
                # Load ảnh từ đường dẫn
                image = pygame.image.load(image_path).convert_alpha()

            # Co giãn ảnh theo tỷ lệ
            original_width, original_height = image.get_size()
            scaled_height = int(original_height * scale_factor)

            # Nếu repeat_x, giữ tỷ lệ và mở rộng khi cần; nếu không, kéo dài ảnh cho bằng map_width
            if repeat_x:
                scaled_width = int(original_width * scale_factor)
                image = pygame.transform.scale(image, (scaled_width, scaled_height))
            else:
                # Với ảnh không lặp lại, cần đảm bảo ảnh đủ rộng
                if speed_factor > 0:
                    # Nếu layer di chuyển, cần đảm bảo ảnh đủ rộng để không lộ ra khoảng trống
                    required_width = max(self.map_width, self.screen_width * 2)
                    image = pygame.transform.scale(image, (required_width, scaled_height))
                else:
                    # Với ảnh tĩnh, kích thước màn hình là đủ
                    image = pygame.transform.scale(image, (self.screen_width, scaled_height))

            # Thêm lớp vào danh sách
            self.layers.append({
                'image': image,
                'width': image.get_width(),
                'height': image.get_height(),
                'speed_factor': speed_factor,
                'y_pos': y_pos,
                'repeat_x': repeat_x,
                'above_player': above_player
            })

            print(f"Đã thêm lớp {image_path} với tốc độ {speed_factor}")

        except Exception as e:
            print(f"Lỗi khi load ảnh {image_path}: {e}")
    
    def draw_background_layers(self, surface, camera_x):
        """Vẽ các lớp phía sau nhân vật"""
        for layer in self.layers:
            if not layer['above_player']:
                self._draw_layer(surface, layer, camera_x)
    
    def draw_foreground_layers(self, surface, camera_x):
        """Vẽ các lớp phía trước nhân vật"""
        for layer in self.layers:
            if layer['above_player']:
                self._draw_layer(surface, layer, camera_x)
    
    def _draw_layer(self, surface, layer, camera_x):
        # Tính toán vị trí x dựa trên tốc độ di chuyển của lớp
        # Đảm bảo rằng camera_x là số không âm để tránh lỗi
        cam_x = max(0, camera_x)
        x_offset = int(-cam_x * layer['speed_factor'])
        
        # Defensive: ensure layer['image'] is a pygame Surface before blitting
        img = layer.get('image')
        if not isinstance(img, pygame.Surface):
            print(f"Warning: parallax layer has invalid image (type={type(img)}). Skipping layer.")
            return

        if layer['repeat_x']:
            # Tính toán vị trí bắt đầu để lặp lại ảnh đúng cách
            start_x = x_offset % layer['width']
            if start_x > 0:
                start_x -= layer['width']
            
            # Vẽ ảnh lặp lại cho đến khi phủ hết màn hình
            current_x = start_x
            while current_x < self.screen_width:
                surface.blit(img, (current_x, layer['y_pos']))
                current_x += layer['width']
        else:
            # Vẽ ảnh không lặp lại - cố định vị trí trong khoảng hiển thị
            # Giới hạn x_offset để ảnh không di chuyển ra khỏi vùng hiển thị
            if layer['speed_factor'] == 0:
                # Nếu layer không di chuyển, luôn vẽ tại vị trí (0, y_pos)
                surface.blit(img, (0, layer['y_pos']))
            else:
                # Nếu layer di chuyển, giới hạn khoảng di chuyển
                max_offset = 0
                min_offset = -layer['width'] + self.screen_width
                x_pos = max(min_offset, min(max_offset, x_offset))
                surface.blit(img, (x_pos, layer['y_pos']))