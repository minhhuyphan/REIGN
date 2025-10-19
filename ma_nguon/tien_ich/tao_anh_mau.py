import pygame
import os
import random

def create_sample_parallax_images():
    """Tạo các ảnh mẫu cho các lớp parallax"""
    
    # Tạo thư mục lưu ảnh nếu chưa có
    parallax_dir = os.path.join("tai_nguyen", "hinh_anh", "canh_nen")
    os.makedirs(parallax_dir, exist_ok=True)
    
    # Kích thước cơ bản cho ảnh
    width, height = 1600, 700
    
    # 1. Trăng và sao (bầu trời đêm)
    sky = pygame.Surface((width, 300), pygame.SRCALPHA)
    sky.fill((20, 20, 50, 255))  # Màu xanh đậm
    
    # Vẽ trăng
    pygame.draw.circle(sky, (240, 240, 240), (width//4, 100), 50)
    
    # Vẽ các ngôi sao
    for _ in range(100):
        x = random.randint(0, width-1)
        y = random.randint(0, 250)
        size = random.randint(1, 3)
        brightness = random.randint(180, 255)
        color = (brightness, brightness, brightness)
        pygame.draw.circle(sky, color, (x, y), size)
    
    # Lưu ảnh
    pygame.image.save(sky, os.path.join(parallax_dir, "trang_sao.png"))
    
    # 2. Mây
    clouds = pygame.Surface((width, 200), pygame.SRCALPHA)
    clouds.fill((0, 0, 0, 0))  # Trong suốt
    
    # Vẽ các đám mây
    for _ in range(10):
        x = random.randint(0, width-200)
        y = random.randint(20, 100)
        cloud_color = (250, 250, 250, 150)  # Màu trắng, hơi trong suốt
        
        # Mỗi đám mây là tập hợp các hình tròn
        for i in range(5):
            radius = random.randint(20, 40)
            offset_x = random.randint(-30, 30)
            offset_y = random.randint(-20, 20)
            pygame.draw.circle(clouds, cloud_color, (x + 50 + offset_x, y + offset_y), radius)
    
    # Lưu ảnh
    pygame.image.save(clouds, os.path.join(parallax_dir, "may.png"))
    
    # 3. Núi
    mountains = pygame.Surface((width, 250), pygame.SRCALPHA)
    mountains.fill((0, 0, 0, 0))  # Trong suốt
    
    # Vẽ dãy núi
    for i in range(0, width, 200):
        height_var = random.randint(-50, 50)
        points = [
            (i, 250),  # Góc dưới trái
            (i + 100, 100 + height_var),  # Đỉnh núi
            (i + 200, 250)  # Góc dưới phải
        ]
        mountain_color = (100, 80, 60)  # Màu nâu
        pygame.draw.polygon(mountains, mountain_color, points)
        
        # Vẽ tuyết trên đỉnh núi
        snow_points = [
            (i + 70, 130 + height_var),
            (i + 100, 100 + height_var),
            (i + 130, 130 + height_var)
        ]
        pygame.draw.polygon(mountains, (255, 255, 255), snow_points)
    
    # Lưu ảnh
    pygame.image.save(mountains, os.path.join(parallax_dir, "nui.png"))
    
    # 4. Cây xa
    far_trees = pygame.Surface((width, 300), pygame.SRCALPHA)
    far_trees.fill((0, 0, 0, 0))  # Trong suốt
    
    # Vẽ các cây
    for i in range(0, width, 100):
        tree_height = random.randint(100, 180)
        trunk_color = (90, 60, 30)  # Màu nâu thân cây
        leaves_color = (30, 100, 30)  # Màu xanh lá
        
        # Thân cây
        pygame.draw.rect(far_trees, trunk_color, (i + 45, 300 - tree_height, 10, tree_height))
        
        # Tán cây
        pygame.draw.circle(far_trees, leaves_color, (i + 50, 300 - tree_height), 40)
    
    # Lưu ảnh
    pygame.image.save(far_trees, os.path.join(parallax_dir, "cay_xa.png"))
    
    # 5. Nhà
    houses = pygame.Surface((width, 250), pygame.SRCALPHA)
    houses.fill((0, 0, 0, 0))  # Trong suốt
    
    # Vẽ các ngôi nhà
    for i in range(0, width, 300):
        house_width = random.randint(100, 150)
        house_height = random.randint(80, 120)
        house_x = i + random.randint(0, 100)
        house_y = 250 - house_height
        
        house_color = (
            random.randint(160, 220),
            random.randint(100, 160),
            random.randint(80, 140)
        )
        
        # Thân nhà
        pygame.draw.rect(houses, house_color, (house_x, house_y, house_width, house_height))
        
        # Mái nhà
        roof_points = [
            (house_x - 10, house_y),
            (house_x + house_width//2, house_y - 40),
            (house_x + house_width + 10, house_y)
        ]
        pygame.draw.polygon(houses, (160, 60, 30), roof_points)
        
        # Cửa
        door_width = house_width // 4
        door_height = house_height // 2
        door_x = house_x + (house_width - door_width) // 2
        door_y = house_y + house_height - door_height
        pygame.draw.rect(houses, (70, 40, 10), (door_x, door_y, door_width, door_height))
        
        # Cửa sổ
        window_size = house_width // 5
        window_x = house_x + house_width // 4
        window_y = house_y + house_height // 4
        pygame.draw.rect(houses, (200, 200, 255), (window_x, window_y, window_size, window_size))
        
        window_x = house_x + house_width - house_width // 4 - window_size
        pygame.draw.rect(houses, (200, 200, 255), (window_x, window_y, window_size, window_size))
    
    # Lưu ảnh
    pygame.image.save(houses, os.path.join(parallax_dir, "nha.png"))
    
    # 6. Mặt đất
    ground = pygame.Surface((800, 200), pygame.SRCALPHA)
    
    # Vẽ mặt đất (có thể lặp lại)
    ground_color = (80, 120, 30)  # Màu xanh đất
    ground.fill(ground_color)
    
    # Thêm chi tiết đất
    for _ in range(300):
        x = random.randint(0, 799)
        y = random.randint(0, 199)
        size = random.randint(1, 5)
        color_var = random.randint(-20, 20)
        color = (
            max(0, min(255, 80 + color_var)),
            max(0, min(255, 120 + color_var)),
            max(0, min(255, 30 + color_var))
        )
        pygame.draw.circle(ground, color, (x, y), size)
    
    # Lưu ảnh
    pygame.image.save(ground, os.path.join(parallax_dir, "mat_dat.png"))
    
    # 7. Cây gần (ở trên nhân vật)
    near_trees = pygame.Surface((width, 500), pygame.SRCALPHA)
    near_trees.fill((0, 0, 0, 0))  # Trong suốt
    
    # Vẽ các cây lớn ở gần
    for i in range(0, width, 400):
        x = i + random.randint(-50, 50)
        
        # Thân cây
        trunk_color = (60, 30, 10)
        trunk_width = random.randint(30, 50)
        trunk_height = random.randint(200, 300)
        pygame.draw.rect(near_trees, trunk_color, (x, 500-trunk_height, trunk_width, trunk_height))
        
        # Tán cây
        leaves_color = (0, 80, 0, 180)  # Xanh lá hơi trong suốt
        leaves_radius = random.randint(80, 120)
        
        # Tán cây gồm nhiều hình tròn chồng lên nhau
        for j in range(5):
            offset_x = random.randint(-30, 30)
            offset_y = random.randint(-80, 0)
            size_var = random.randint(-20, 20)
            pygame.draw.circle(near_trees, leaves_color, 
                            (x + trunk_width//2 + offset_x, 
                             500-trunk_height + offset_y), 
                            leaves_radius + size_var)
    
    # Lưu ảnh
    pygame.image.save(near_trees, os.path.join(parallax_dir, "cay_gan.png"))
    
    print("Đã tạo xong các ảnh mẫu cho parallax background")

# Khởi tạo pygame
pygame.init()

# Chạy hàm tạo ảnh
create_sample_parallax_images()

# Kết thúc pygame
pygame.quit()