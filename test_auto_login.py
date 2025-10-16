"""
Test Auto-Login Feature
Kiểm tra tính năng tự động đăng nhập
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ma_nguon.tien_ich import user_store

print("=" * 60)
print("TEST AUTO-LOGIN FEATURE")
print("=" * 60)

# Test 1: Check session functions
print("\n1. Kiểm tra session functions:")
print(f"   Session file: {user_store.SESSION_FILE}")

# Test 2: Clear any existing session
print("\n2. Xóa session cũ (nếu có):")
user_store.clear_session()
current = user_store.load_current_user()
print(f"   ✓ Session sau khi clear: {current}")
assert current is None, "Session should be None after clear"

# Test 3: Create test user if not exists
print("\n3. Tạo test user (nếu chưa có):")
test_username = "test_auto_login"
test_password = "password123"

if test_username not in user_store.load_users():
    result = user_store.register_user(test_username, test_password)
    print(f"   ✓ Đăng ký user mới: {result}")
else:
    print(f"   ✓ User đã tồn tại: {test_username}")

# Test 4: Authenticate
print("\n4. Xác thực user:")
auth_result = user_store.authenticate(test_username, test_password)
print(f"   ✓ Xác thực thành công: {auth_result}")
assert auth_result, "Authentication should succeed"

# Test 5: Save session
print("\n5. Lưu session:")
user_store.save_current_user(test_username)
current = user_store.load_current_user()
print(f"   ✓ Session đã lưu: {current}")
assert current == test_username, f"Session should be {test_username}"

# Test 6: Load session (simulate reopening game)
print("\n6. Mô phỏng mở game lại:")
loaded_user = user_store.load_current_user()
print(f"   ✓ User tự động load: {loaded_user}")
assert loaded_user == test_username, "Should auto-load saved user"

# Test 7: Logout
print("\n7. Đăng xuất:")
user_store.clear_session()
current = user_store.load_current_user()
print(f"   ✓ Session sau logout: {current}")
assert current is None, "Session should be None after logout"

# Test 8: Verify session file
print("\n8. Kiểm tra file session:")
import json
user_store.save_current_user(test_username)
with open(user_store.SESSION_FILE, 'r') as f:
    session_data = json.load(f)
print(f"   ✓ Session data: {session_data}")
assert session_data.get('current_user') == test_username

# Cleanup
print("\n9. Cleanup:")
user_store.clear_session()
print("   ✓ Đã xóa session test")

print("\n" + "=" * 60)
print("✅ TẤT CẢ TEST PASSED!")
print("=" * 60)
print("\nHướng dẫn test thủ công:")
print("1. Chạy game: python ma_nguon/main.py")
print(f"2. Nếu có session → Tự động vào Menu")
print("3. Nếu không → Hiện màn hình Login")
print("4. Đăng nhập → Session được lưu")
print("5. Tắt game → Mở lại → Tự động vào Menu")
print("6. Click 'Đăng xuất' → Session bị xóa")
print("7. Mở lại game → Phải login lại")
print("=" * 60)
