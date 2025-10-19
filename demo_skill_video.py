"""
Demo skill video full screen
Chạy: python demo_skill_video.py
"""
import pygame
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ma_nguon.man_choi.skill_video import SkillVideoPlayer

def main():
    print("🎬 DEMO SKILL VIDEO - FULL SCREEN MODE")
    print("=" * 60)
    
    # Initialize pygame
    pygame.init()
    
    # Create window
    WIDTH, HEIGHT = 1024, 768
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Skill Video Demo - Full Screen")
    
    clock = pygame.time.Clock()
    
    # Create video player
    video_finished = False
    
    def on_finish():
        global video_finished
        video_finished = True
        print("✅ Video finished!")
    
    video_path = "Tai_nguyen/video/skill_chien_than.mp4"
    player = SkillVideoPlayer(video_path, on_finish)
    
    print(f"📹 Playing: {video_path}")
    print(f"📐 Screen: {WIDTH}x{HEIGHT}")
    print(f"🎯 Mode: FULL SCREEN (stretched)")
    print(f"⚡ Effect: WHITE FLASH (ENHANCED) on finish")
    print(f"   - 300ms: 100% white (NO FADE)")
    print(f"   - 700ms: fade out (alpha 255→0)")
    print(f"   - Total: 1 second")
    print("\nPress ESC to skip, SPACE to exit when done")
    print("-" * 60)
    
    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("⏩ Video skipped!")
                    player.skip()
                    running = False
                elif event.key == pygame.K_SPACE and video_finished:
                    print("👋 Exiting...")
                    running = False
        
        # Update video
        player.update()
        
        # Draw
        screen.fill((0, 0, 0))  # Black background
        player.draw(screen)
        
        # Show message if finished
        if video_finished:
            font = pygame.font.Font(None, 36)
            text = font.render("Video Finished! Press SPACE to exit", True, (255, 255, 0))
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
        
        pygame.display.flip()
        clock.tick(60)
        
        # Auto exit when finished
        if player.finished and video_finished:
            pygame.time.wait(500)  # Wait a bit to show message
    
    # Cleanup
    player.cleanup()
    pygame.quit()
    
    print("-" * 60)
    print("✨ Demo complete!")

if __name__ == "__main__":
    main()
