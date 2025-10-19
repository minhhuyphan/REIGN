"""
Script để test và visualize equipment system
Chạy file này để xem preview các equipment và kiểm tra load hình ảnh
"""

import pygame
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ma_nguon.doi_tuong.equipment import get_equipment_manager

def test_equipment_display():
    """Display all equipment with their info"""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Equipment System Test")
    
    try:
        font = pygame.font.Font("tai_nguyen/font/Fz-Futurik.ttf", 20)
        title_font = pygame.font.Font("tai_nguon/font/Fz-Donsky.ttf", 32)
    except:
        font = pygame.font.Font(None, 20)
        title_font = pygame.font.Font(None, 32)
    
    eq_manager = get_equipment_manager()
    equipment_list = eq_manager.get_all_equipment()
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Draw
        screen.fill((30, 30, 50))
        
        # Title
        title = title_font.render("EQUIPMENT SYSTEM TEST", True, (255, 215, 0))
        screen.blit(title, (800//2 - title.get_width()//2, 20))
        
        # Draw equipment grid
        y_offset = 100
        for i, equipment in enumerate(equipment_list):
            x = 50
            y = y_offset + i * 120
            
            # Draw equipment box
            pygame.draw.rect(screen, (60, 60, 80), (x, y, 700, 100))
            pygame.draw.rect(screen, (255, 255, 255), (x, y, 700, 100), 2)
            
            # Draw equipment image
            if equipment.image:
                screen.blit(equipment.image, (x + 10, y + 20))
            
            # Draw equipment info
            name_text = font.render(equipment.name, True, (255, 215, 0))
            screen.blit(name_text, (x + 90, y + 10))
            
            type_text = font.render(f"Loại: {equipment.equipment_type}", True, (200, 200, 200))
            screen.blit(type_text, (x + 90, y + 35))
            
            # Draw stats
            stats_y = y + 60
            stats = []
            if equipment.attack_bonus > 0:
                stats.append(f"+{equipment.attack_bonus} Công")
            if equipment.defense_bonus > 0:
                stats.append(f"+{equipment.defense_bonus} Thủ")
            if equipment.hp_bonus > 0:
                stats.append(f"+{equipment.hp_bonus} HP")
            if equipment.speed_bonus > 0:
                stats.append(f"+{equipment.speed_bonus} Tốc độ")
            
            stats_text = font.render(" | ".join(stats), True, (100, 255, 100))
            screen.blit(stats_text, (x + 90, stats_y))
            
            # Draw special effects
            if equipment.has_slow_effect:
                effect = font.render("⚡ Làm chậm", True, (100, 200, 255))
                screen.blit(effect, (x + 500, y + 20))
            if equipment.has_burn_effect:
                effect = font.render("🔥 Thiêu đốt", True, (255, 100, 50))
                screen.blit(effect, (x + 500, y + 45))
            if equipment.has_revive_effect:
                effect = font.render("✨ Hồi sinh", True, (255, 255, 100))
                screen.blit(effect, (x + 500, y + 70))
        
        # Instructions
        instruction = font.render("Press ESC to exit", True, (150, 150, 150))
        screen.blit(instruction, (800//2 - instruction.get_width()//2, 550))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    print("\n✓ Equipment system test completed!")
    print(f"✓ Loaded {len(equipment_list)} equipment items")
    for eq in equipment_list:
        status = "✓" if eq.image else "✗"
        print(f"  {status} {eq.name} - Image loaded: {eq.image is not None}")

if __name__ == "__main__":
    print("Starting Equipment System Test...")
    print("This will display all equipment with their stats and special effects\n")
    test_equipment_display()
