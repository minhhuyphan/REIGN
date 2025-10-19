"""
Utility functions để xử lý viên đạn cho tất cả các map
"""

def update_bullets(player, enemies, boss=None):
    """
    Cập nhật tất cả viên đạn của player và kiểm tra va chạm với quái/boss
    
    Args:
        player: Đối tượng nhân vật
        enemies: Danh sách quái vật
        boss: Boss (optional)
    """
    for bullet in player.bullets[:]:
        bullet.update()
        if not bullet.active:
            player.bullets.remove(bullet)
        else:
            # Kiểm tra va chạm đạn với quái thường
            bullet_rect = bullet.get_rect()
            for enemy in enemies:
                if enemy.hp <= 0:
                    continue
                enemy_rect = enemy.image.get_rect(topleft=(enemy.x, enemy.y))
                if bullet_rect.colliderect(enemy_rect) and bullet.active:
                    enemy.take_damage(bullet.damage, bullet.direction == 1, player)
                    bullet.active = False
                    break
            
            # Kiểm tra va chạm đạn với boss
            if boss and bullet.active and boss.hp > 0:
                boss_rect = boss.image.get_rect(topleft=(boss.x, boss.y))
                if bullet_rect.colliderect(boss_rect):
                    boss.take_damage(bullet.damage, bullet.direction == 1, player)
                    bullet.active = False


def draw_bullets(player, screen, camera_x=0):
    """
    Vẽ tất cả viên đạn của player
    
    Args:
        player: Đối tượng nhân vật
        screen: Surface để vẽ
        camera_x: Camera offset
    """
    for bullet in player.bullets:
        bullet.draw(screen, camera_x)
