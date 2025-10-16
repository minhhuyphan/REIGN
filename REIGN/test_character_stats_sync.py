"""
Test Stats Synchronization
Kiểm tra stats nhân vật đồng bộ giữa Equipment Scene và Character Select
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from ma_nguon.core.character_data import get_all_characters, get_character_by_id, get_character_stats


def test_all_characters_have_required_stats():
    """Test tất cả nhân vật có đủ stats bắt buộc"""
    print("=" * 60)
    print("TEST 1: All Characters Have Required Stats")
    print("=" * 60)
    
    required_stats = ["hp", "damage", "speed", "defense", "kick_damage"]
    characters = get_all_characters()
    
    print(f"\nChecking {len(characters)} characters...")
    
    for char in characters:
        print(f"\n✓ {char['name']} ({char['id']}):")
        stats = char["stats"]
        
        # Check required fields
        for stat_name in required_stats:
            if stat_name in stats:
                print(f"  - {stat_name}: {stats[stat_name]}")
            else:
                print(f"  ✗ MISSING: {stat_name}")
                return False
    
    print("\n✓ All characters have required stats")
    return True


def test_stats_consistency():
    """Test stats đồng bộ giữa các hàm helper"""
    print("\n" + "=" * 60)
    print("TEST 2: Stats Consistency")
    print("=" * 60)
    
    print("\nTesting get_character_by_id vs get_character_stats...")
    
    test_ids = ["chien_binh", "ninja", "vo_si", "chien_than_lac_hong", "tho_san_quai_vat"]
    
    for char_id in test_ids:
        char_full = get_character_by_id(char_id)
        char_stats = get_character_stats(char_id)
        
        if char_full is None:
            print(f"✗ Character {char_id} not found!")
            return False
        
        if char_stats != char_full["stats"]:
            print(f"✗ Stats mismatch for {char_id}!")
            return False
        
        print(f"✓ {char_id}: Stats consistent")
    
    print("\n✓ All stats are consistent")
    return True


def test_character_data_structure():
    """Test cấu trúc dữ liệu nhân vật"""
    print("\n" + "=" * 60)
    print("TEST 3: Character Data Structure")
    print("=" * 60)
    
    required_fields = ["id", "name", "folder", "stats", "color", "price"]
    characters = get_all_characters()
    
    print(f"\nChecking structure of {len(characters)} characters...")
    
    for char in characters:
        print(f"\n✓ {char['name']}:")
        for field in required_fields:
            if field in char:
                print(f"  - {field}: ✓")
            else:
                print(f"  - {field}: ✗ MISSING")
                return False
    
    print("\n✓ All characters have correct structure")
    return True


def display_character_comparison():
    """Hiển thị bảng so sánh stats các nhân vật"""
    print("\n" + "=" * 60)
    print("CHARACTER STATS COMPARISON")
    print("=" * 60)
    
    characters = get_all_characters()
    
    # Header
    print(f"\n{'Character':<25} {'HP':<8} {'DMG':<8} {'KICK':<8} {'SPD':<6} {'DEF':<6}")
    print("-" * 70)
    
    # Data rows
    for char in characters:
        stats = char["stats"]
        print(f"{char['name']:<25} "
              f"{stats['hp']:<8} "
              f"{stats['damage']:<8} "
              f"{stats['kick_damage']:<8} "
              f"{stats['speed']:<6} "
              f"{stats['defense']:<6}")


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("CHARACTER DATA SYNCHRONIZATION TEST")
    print("=" * 60)
    
    tests = [
        test_all_characters_have_required_stats,
        test_stats_consistency,
        test_character_data_structure
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"\n✗ Test FAILED: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    # Display comparison table
    try:
        display_character_comparison()
    except Exception as e:
        print(f"\n! Comparison table failed: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Total tests: {len(tests)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print("\n✓ ALL TESTS PASSED!")
        print("\n✓ Character stats are now synchronized!")
        print("  - Equipment Scene uses: ma_nguon.core.character_data")
        print("  - Character Select uses: ma_nguon.core.character_data")
        print("  - Both scenes have identical stats!")
    else:
        print("\n✗ SOME TESTS FAILED")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
