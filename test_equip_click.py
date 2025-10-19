"""Test click detection cho equip slots"""
import pygame

pygame.init()
screen = pygame.display.set_mode((1400, 800))
clock = pygame.time.Clock()

# Constants (same as equipment_screen.py)
SLOT_SIZE = 80
SLOT_MARGIN = 20

# Equip slots position
equip_slots_y_start = 320
equip_slots = ['attack', 'defense', 'speed']

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            print(f"Click at: ({mx}, {my})")
            
            # Check equip slot clicks
            for i, slot_type in enumerate(equip_slots):
                slot_x = 580
                slot_y = equip_slots_y_start + i * (SLOT_SIZE + SLOT_MARGIN)
                slot_rect = pygame.Rect(slot_x, slot_y, SLOT_SIZE, SLOT_SIZE)
                
                print(f"  Slot {slot_type}: x={slot_x}-{slot_x+SLOT_SIZE}, y={slot_y}-{slot_y+SLOT_SIZE}")
                
                if slot_rect.collidepoint(mx, my):
                    print(f"  >>> HIT! Clicked on {slot_type} slot!")
    
    screen.fill((20, 20, 40))
    
    # Draw equip slots for visual reference
    for i, slot_type in enumerate(equip_slots):
        slot_x = 580
        slot_y = equip_slots_y_start + i * (SLOT_SIZE + SLOT_MARGIN)
        pygame.draw.rect(screen, (80, 80, 120), (slot_x, slot_y, SLOT_SIZE, SLOT_SIZE))
        pygame.draw.rect(screen, (200, 200, 200), (slot_x, slot_y, SLOT_SIZE, SLOT_SIZE), 2)
        
        font = pygame.font.Font(None, 24)
        text = font.render(slot_type.upper(), True, (255, 255, 255))
        screen.blit(text, (slot_x + 5, slot_y + 30))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
print("Test completed")
