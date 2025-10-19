"""
Test script cho skill Chiến Thần Lạc Hồng
Chạy: python test_skill_chien_than.py
"""
import os
import sys

# Add root directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pygame
from ma_nguon.doi_tuong.nhan_vat.nhan_vat import Character

def test_skill_system():
    """Test các tính năng của skill system"""
    print("🧪 TESTING SKILL SYSTEM")
    print("=" * 60)
    
    # Initialize pygame
    pygame.init()
    
    # Tạo nhân vật Chiến Thần Lạc Hồng
    folder = "Tai_nguyen/hinh_anh/nhan_vat/chien_than_lac_hong"
    stats = {
        "hp": 2000,
        "speed": 4,
        "damage": 200,
        "defense": 8,
        "kick_damage": 150,
        "max_mana": 200,
        "mana_regen": 5
    }
    
    player = Character(100, 300, folder, stats=stats)
    
    print(f"\n1. ✅ Character created: {folder}")
    print(f"   HP: {player.hp}/{player.max_hp}")
    print(f"   Mana: {player.mana}/{player.max_mana}")
    print(f"   Damage: {player.damage}")
    
    # Test skill properties
    print(f"\n2. 🎯 Skill Properties:")
    print(f"   Cooldown: {player.skill_cooldown / 1000}s")
    print(f"   Mana Cost: {player.skill_mana_cost}")
    print(f"   Damage: {player.skill_damage}")
    print(f"   Range: {player.skill_range}px")
    
    # Test can use skill
    print(f"\n3. 🔍 Testing can_use_skill():")
    can_use = player.can_use_skill()
    print(f"   Can use skill: {can_use}")
    print(f"   Mana: {player.mana}/{player.skill_mana_cost}")
    print(f"   Cooldown remaining: {player.get_skill_cooldown_remaining()}s")
    
    if can_use:
        print(f"   ✅ Player can use skill!")
    else:
        print(f"   ❌ Player CANNOT use skill (expected on first check)")
    
    # Test use skill
    print(f"\n4. 💫 Testing use_skill():")
    result = player.use_skill()
    print(f"   Skill used: {result}")
    
    if result:
        print(f"   ✅ Skill activated successfully!")
        print(f"   Mana after: {player.mana}/{player.max_mana}")
        print(f"   Cooldown: {player.get_skill_cooldown_remaining():.1f}s")
    else:
        print(f"   ❌ Failed to use skill")
    
    # Test cooldown
    print(f"\n5. ⏱️  Testing cooldown:")
    can_use_again = player.can_use_skill()
    print(f"   Can use again immediately: {can_use_again}")
    
    if not can_use_again:
        print(f"   ✅ Cooldown working! Remaining: {player.get_skill_cooldown_remaining():.1f}s")
    else:
        print(f"   ❌ Cooldown NOT working!")
    
    # Test video file
    print(f"\n6. 🎬 Testing video file:")
    video_path = "Tai_nguyen/video/skill_chien_than.mp4"
    video_exists = os.path.exists(video_path)
    print(f"   Video path: {video_path}")
    print(f"   Video exists: {video_exists}")
    
    if video_exists:
        file_size = os.path.getsize(video_path) / (1024 * 1024)  # MB
        print(f"   ✅ Video found! Size: {file_size:.2f} MB")
    else:
        print(f"   ❌ Video NOT found!")
    
    # Test OpenCV
    print(f"\n7. 📦 Testing OpenCV (cv2):")
    try:
        import cv2
        print(f"   ✅ OpenCV installed! Version: {cv2.__version__}")
        
        if video_exists:
            cap = cv2.VideoCapture(video_path)
            if cap.isOpened():
                fps = cap.get(cv2.CAP_PROP_FPS)
                frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
                duration = frame_count / fps if fps > 0 else 0
                print(f"   Video FPS: {fps}")
                print(f"   Video frames: {frame_count}")
                print(f"   Video duration: {duration:.2f}s")
                print(f"   ✅ Video can be loaded!")
                cap.release()
            else:
                print(f"   ❌ Video cannot be opened!")
    except ImportError:
        print(f"   ⚠️  OpenCV NOT installed (video will be skipped)")
        print(f"   Install with: pip install opencv-python")
    
    print(f"\n" + "=" * 60)
    print(f"✨ SKILL SYSTEM TEST COMPLETE!")
    print(f"=" * 60)
    
    pygame.quit()

if __name__ == "__main__":
    test_skill_system()
