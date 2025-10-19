# Hướng dẫn áp dụng bullet handler cho tất cả map

Để thêm chức năng bắn đạn cho tất cả map, làm theo 3 bước sau:

## Bước 1: Import bullet_handler
Thêm vào đầu file map (sau các import khác):
```python
from ma_nguon.tien_ich.bullet_handler import update_bullets, draw_bullets
```

## Bước 2: Cập nhật viên đạn trong hàm update()
Tìm đoạn code xử lý va chạm (thường sau `self.player.damaged = False`), thêm:
```python
# Cập nhật viên đạn của player
update_bullets(self.player, self.normal_enemies, self.current_boss)
```

Hoặc nếu map không có boss:
```python
# Cập nhật viên đạn của player
update_bullets(self.player, self.normal_enemies)
```

## Bước 3: Vẽ viên đạn trong hàm draw()
Tìm dòng `self.player.draw(screen, self.camera_x)`, thêm ngay sau đó:
```python
# Vẽ viên đạn
draw_bullets(self.player, screen, self.camera_x)
```

## Danh sách các map cần cập nhật:
- [ ] man2.py
- [ ] maprunglinhvuc.py
- [ ] map_cong_nghe.py
- [ ] map_ninja.py
- [ ] map_ninja_man1.py
- [ ] map_mua_thu.py
- [ ] map_mua_thu_man1.py
- [ ] map_mua_thu_man2.py
- [ ] map_mua_thu_man3.py

## Lưu ý:
- man1.py đã được cập nhật sẵn làm mẫu
- Một số map có thể có cấu trúc khác nhau, cần điều chỉnh linh hoạt
