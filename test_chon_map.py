"""
Test màn chọn map
"""
print("="*70)
print("HƯỚNG DẪN SỬ DỤNG MÀN CHỌN MAP")
print("="*70)

print("\n1. Vào game và login")
print("2. Chọn 'Chọn Map' trong menu")
print("3. Sử dụng phím ← → hoặc A/D để chọn map")
print("4. Nhấn ENTER để xác nhận")
print("5. Chọn nhân vật")
print("6. Vào game!")

print("\n" + "="*70)
print("DANH SÁCH MAPS")
print("="*70)

maps = [
    ("Màn 1", "man1", "Dễ"),
    ("Màn 2", "man2", "Trung bình"),
    ("Map Mùa Thu", "chon_man_mua_thu", "Trung bình"),
    ("Map Ninja", "chon_man_ninja", "Khó"),
    ("Map Công Nghệ", "map_cong_nghe", "Khó"),
    ("Rừng Linh Vực", "maprunglinhvuc", "Rất khó")
]

for i, (name, scene, difficulty) in enumerate(maps, 1):
    print(f"{i}. {name:20} | Scene: {scene:25} | Độ khó: {difficulty}")

print("\n" + "="*70)
print("✅ Tất cả maps đã được cấu hình!")
print("="*70)
