import sys
sys.path.append(r'D:\New folder (2)\REIGN')
import pygame
pygame.init()
from ma_nguon.doi_tuong.nhan_vat.nhan_vat import Character
from ma_nguon.doi_tuong.bullet import ShurikenBullet
c = Character(100,300, folder='Tai_nguyen/hinh_anh/nhan_vat/sasuke')
print('special_skill=', c.special_skill)
c.mana = 9999
c.last_skill_time = -999999
ok = c.use_skill()
print('use_skill ok=', ok, 'bullets=', len(c.bullets))
for b in c.bullets:
    print('Bullet:', type(b), b.x, b.y, getattr(b, 'is_sasuke_skill', False))
pygame.quit()
