#!/usr/bin/env python3
"""
Test script để kiểm tra clone AI có thể di chuyển full map
"""
import pygame
import sys
import os

# Add the ma_nguon directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'ma_nguon'))

from ma_nguon.doi_tuong.nhan_vat.nhan_vat import Character
from ma_nguon.doi_tuong.nhan_vat.clone import CloneManager
from ma_nguon.doi_tuong.quai_vat.quai_vat import QuaiVat

pygame.init()

# Screen setup
WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Clone Full Map Test")
clock = pygame.time.Clock()

# Create player với clone skill
player = Character(100, 300, folder="tai_nguyen/hinh_anh/nhan_vat/chien_binh")
player.special_skill = "clone_summon"
player.skill_mana_cost = 50
player.mana = 100  # Đủ mana để test

# Tạo clone manager
from ma_nguon.doi_tuong.nhan_vat.clone import CloneManager
player.clone_manager = CloneManager()

# Tạo enemies ở xa nhau khắp map
enemies = []
map_width = 5000
for i in range(5):
    x_pos = 500 + i * (map_width // 6)  # Spread enemies across map
    enemy = QuaiVat(x_pos, 300, "tai_nguon/hinh_anh/quai_vat/quai_vat", None)
    enemies.append(enemy)
    print(f"Enemy {i+1} tạo tại x={x_pos}")

print(f"\n=== TEST CLONE FULL MAP ===")
print("Nhấn F để tạo clone")
print("Nhấn SPACE để kích hoạt clone skill")
print("ESC để thoát")

camera_x = 0
running = True
skill_activated = False

while running:
    dt = clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_f and not skill_activated:
                # Activate clone skill
                if player.clone_manager:
                    success = player.clone_manager.create_clones(player.x, player.y, enemies)
                    if success:
                        skill_activated = True
                        print("🔥 Clone skill activated! Clones sẽ di chuyển khắp map tìm enemies!")
    
    # Update
    keys = pygame.key.get_pressed()
    
    # Player movement
    if keys[pygame.K_LEFT] and player.x > 0:
        player.x -= 5
        camera_x = max(0, player.x - WIDTH//2)
    elif keys[pygame.K_RIGHT] and player.x < map_width:
        player.x += 5
        camera_x = min(map_width - WIDTH, player.x - WIDTH//2)
    
    # Update enemies
    for enemy in enemies:
        if enemy.hp > 0:
            enemy.update()
    
    # Update clones với enemies reference
    if player.clone_manager:
        living_enemies = [e for e in enemies if e.hp > 0]
        player.clone_manager.update(living_enemies)
    
    # Draw
    screen.fill((50, 100, 50))  # Green background
    
    # Draw enemies
    for enemy in enemies:
        if enemy.hp > 0:
            draw_x = enemy.x - camera_x
            if -100 < draw_x < WIDTH + 100:  # Only draw if visible
                pygame.draw.rect(screen, (255, 0, 0), (draw_x, enemy.y, 50, 80))
                pygame.draw.circle(screen, (255, 255, 255), (int(draw_x + 25), int(enemy.y - 20)), 15)
    
    # Draw player
    player_draw_x = player.x - camera_x
    pygame.draw.rect(screen, (0, 0, 255), (player_draw_x, player.y, 50, 80))
    
    # Draw clones
    if player.clone_manager:
        for clone in player.clone_manager.clones:
            clone_draw_x = clone.x - camera_x
            if -100 < clone_draw_x < WIDTH + 100:  # Only draw if visible
                pygame.draw.rect(screen, (0, 255, 255), (clone_draw_x, clone.y, 50, 80))
                # Draw target line if exists
                if clone.target_enemy and not clone.target_enemy.dead:
                    target_x = clone.target_enemy.x - camera_x
                    pygame.draw.line(screen, (255, 255, 0), 
                                   (clone_draw_x + 25, clone.y + 40), 
                                   (target_x + 25, clone.target_enemy.y + 40), 2)
    
    # UI Text
    font = pygame.font.Font(None, 36)
    text_lines = [
        f"Camera: {camera_x:.0f}",
        f"Player X: {player.x:.0f}",
        f"Enemies alive: {sum(1 for e in enemies if e.hp > 0)}",
        f"Clones active: {len(player.clone_manager.clones) if player.clone_manager else 0}",
        "Press F to create clones" if not skill_activated else "Clones hunting across map!"
    ]
    
    for i, line in enumerate(text_lines):
        color = (255, 255, 255) if i < 4 else (0, 255, 0)
        text = font.render(line, True, color)
        screen.blit(text, (10, 10 + i * 40))
    
    pygame.display.flip()

pygame.quit()
print("Test kết thúc!")