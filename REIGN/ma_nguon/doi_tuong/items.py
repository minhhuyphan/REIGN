import pygame
import random

class Item:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.picked = False
        self.image = None
        self.rect = pygame.Rect(self.x, self.y, 24, 24)

    def draw(self, screen, camera_x=0):
        # Default placeholder: small circle
        draw_x = self.x - camera_x
        pygame.draw.circle(screen, (200,200,0), (int(draw_x+12), int(self.y+12)), 10)

    def on_pickup(self, player):
        self.picked = True
        print(f"[DEBUG] {type(self).__name__} picked up by player at ({player.x},{player.y})")


class Gold(Item):
    def __init__(self, x, y, amount=10):
        super().__init__(x, y)
        self.amount = amount
        self.color = (212,175,55)
        self.rect = pygame.Rect(self.x, self.y, 20, 20)

    def draw(self, screen, camera_x=0):
        draw_x = self.x - camera_x
        pygame.draw.circle(screen, self.color, (int(draw_x+10), int(self.y+10)), 8)
        # draw amount small
        font = pygame.font.Font(None, 18)
        txt = font.render(str(self.amount), True, (0,0,0))
        screen.blit(txt, (draw_x+2, self.y+18))

    def on_pickup(self, player):
        if hasattr(player, 'gold'):
            player.gold += self.amount
        else:
            player.gold = self.amount
        self.picked = True


class HealthPotion(Item):
    def __init__(self, x, y, heal=200):
        super().__init__(x, y)
        self.heal = heal
        self.color = (200,50,50)
        self.rect = pygame.Rect(self.x, self.y, 20, 30)

    def draw(self, screen, camera_x=0):
        draw_x = self.x - camera_x
        pygame.draw.rect(screen, self.color, (draw_x+4, self.y, 12, 20), border_radius=3)
        font = pygame.font.Font(None, 16)
        txt = font.render('HP', True, (255,255,255))
        screen.blit(txt, (draw_x+6, self.y+2))

    def on_pickup(self, player):
        # add to player's inventory (simple count) or apply immediately
        if hasattr(player, 'potions'):
            player.potions['hp'] = player.potions.get('hp', 0) + 1
        else:
            player.potions = {'hp': 1}
        self.picked = True


class ManaPotion(Item):
    def __init__(self, x, y, mana=100):
        super().__init__(x, y)
        self.mana = mana
        self.color = (50,100,200)
        self.rect = pygame.Rect(self.x, self.y, 20, 30)

    def draw(self, screen, camera_x=0):
        draw_x = self.x - camera_x
        pygame.draw.rect(screen, self.color, (draw_x+4, self.y, 12, 20), border_radius=3)
        font = pygame.font.Font(None, 16)
        txt = font.render('MP', True, (255,255,255))
        screen.blit(txt, (draw_x+4, self.y+2))

    def on_pickup(self, player):
        if hasattr(player, 'potions'):
            player.potions['mp'] = player.potions.get('mp', 0) + 1
        else:
            player.potions = {'mp': 1}
        self.picked = True
