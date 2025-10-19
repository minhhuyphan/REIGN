# Hướng Dẫn Hệ Thống Trang Bị Với Profile

## Cập Nhật Mới (16/10/2025)

Hệ thống trang bị đã được nâng cấp với các tính năng mới:

### ✨ Tính Năng Mới

1. **Chọn Nhân Vật Để Trang Bị**
   - Mỗi nhân vật có bộ trang bị riêng
   - Sử dụng phím ←/→ để chuyển giữa các nhân vật
   - Hiển thị avatar và tên nhân vật

2. **Lưu Trang Bị Vào Profile**
   - Trang bị được tự động lưu khi thoát màn hình
   - Mỗi user có profile riêng
   - Trang bị được lưu cho từng nhân vật

3. **Tự Động Load Trang Bị**
   - Khi chọn nhân vật để chơi, trang bị được tự động áp dụng
   - Stats và hiệu ứng có hiệu lực ngay trong game

### 📋 Quy Trình Sử Dụng

#### Bước 1: Đăng Nhập
```
Menu → Đăng xuất/Đăng nhập
```
- Đảm bảo bạn đã đăng nhập để lưu được trang bị

#### Bước 2: Trang Bị Cho Nhân Vật
```
Menu → Trang bị
```

**Trong màn hình trang bị:**

1. **Chọn nhân vật:**
   - Nhấn `←` để chuyển sang nhân vật trước
   - Nhấn `→` để chuyển sang nhân vật sau
   - Tên và avatar nhân vật hiển thị ở trên cùng

2. **Chọn trang bị:**
   - Click vào trang bị trong **KHO ĐỒ** (bên trái)
   - Trang bị được chọn sẽ có viền vàng

3. **Gắn trang bị:**
   - Click vào **SLOT** tương ứng (Công/Thủ/Tốc Độ) bên phải
   - Trang bị sẽ được gắn vào nhân vật hiện tại

4. **Gỡ trang bị:**
   - Click vào slot đã có trang bị để gỡ ra

5. **Lưu và thoát:**
   - Nhấn `ESC` hoặc `E`
   - Trang bị sẽ tự động được lưu vào profile

#### Bước 3: Chơi Game Với Trang Bị
```
Menu → Chọn màn chơi → Chọn nhân vật
```

- Khi chọn nhân vật, trang bị đã lưu sẽ **tự động được áp dụng**
- Stats được cộng thêm ngay lập tức:
  - Công = Công gốc + Bonus từ trang bị
  - Thủ = Thủ gốc + Bonus từ trang bị  
  - HP = HP gốc + Bonus từ trang bị
  - Tốc độ = Tốc độ gốc + Bonus từ trang bị

- Hiệu ứng đặc biệt hoạt động trong combat:
  - **Làm chậm** (Cung Băng Lãm): Icon băng xuất hiện trên địch
  - **Thiêu đốt** (Kiếm Rồng): Icon lửa xuất hiện, -1 HP/giây
  - **Hồi sinh** (Giáp Ánh Sáng): Tự động hồi sinh với 50% HP khi chết
  - **Tăng tốc** (Giày Thiên Thần): Di chuyển nhanh hơn

### 🎯 Ràng Buộc Trang Bị

**Quan trọng:** Mỗi trang bị chỉ có thể gắn cho **1 nhân vật duy nhất**

- Nếu trang bị đã được gắn cho nhân vật A, bạn cần **gỡ trang bị** khỏi nhân vật A trước khi gắn cho nhân vật B
- Trang bị đã gắn sẽ có dấu ✓ màu xanh trong kho đồ
- Hover chuột lên trang bị để xem nhân vật nào đang sử dụng

### 💾 Cấu Trúc Lưu Trữ

Trang bị được lưu trong file `du_lieu/save/profiles.json`:

```json
{
  "username": {
    "gold": 500,
    "purchased_characters": ["chien_binh", "ninja"],
    "character_equipment": {
      "chien_binh": {
        "attack": "Cung Băng Lãm",
        "defense": "Giáp Ánh Sáng",
        "speed": null
      },
      "ninja": {
        "attack": "Kiếm Rồng",
        "defense": null,
        "speed": "Giày Thiên Thần"
      }
    }
  }
}
```

### 🎮 Phím Tắt

**Trong màn hình trang bị:**
- `←` : Chuyển sang nhân vật trước
- `→` : Chuyển sang nhân vật sau
- `Click chuột` : Chọn/Trang bị/Gỡ trang bị
- `ESC` hoặc `E` : Lưu và thoát
- `Hover chuột` : Xem thông tin chi tiết (tooltip)

### 📊 Danh Sách Nhân Vật

1. **Chiến binh** (`chien_binh`)
   - HP: 500 | Tốc độ: 5 | Công: 30 | Thủ: 2

2. **Ninja** (`ninja`)
   - HP: 350 | Tốc độ: 8 | Công: 25 | Thủ: 1

3. **Võ sĩ** (`vo_si`)
   - HP: 1000 | Tốc độ: 4 | Công: 100 | Thủ: 3

4. **Chiến Thần Lạc Hồng** (`chien_than_lac_hong`)
   - HP: 2000 | Tốc độ: 4 | Công: 200 | Thủ: 8

5. **Thợ Săn Quái Vật** (`tho_san_quai_vat`)
   - HP: 450 | Tốc độ: 7 | Công: 35 | Thủ: 2

6. **Mị Ảnh** (`mi_anh`)
   - HP: 450 | Tốc độ: 9 | Công: 28 | Thủ: 1

7. **Vân Dao** (`van_dao`)
   - HP: 600 | Tốc độ: 8 | Công: 32 | Thủ: 2

### 🛠️ Ví Dụ Sử Dụng

#### Trang bị cho Ninja

1. Menu → Trang bị
2. Nhấn `→` để chọn **Ninja**
3. Click **Kiếm Rồng** trong kho đồ
4. Click slot **CÔNG** để gắn
5. Click **Giày Thiên Thần** trong kho đồ
6. Click slot **TỐC ĐỘ** để gắn
7. Nhấn `ESC` để lưu

**Kết quả:**
- Ninja giờ có:
  - Công: 25 + 10 = **35**
  - Tốc độ: 8 + 2 = **10**
  - HP: 350 + 50 = **400**
  - Hiệu ứng thiêu đốt khi đánh

#### Trang bị cho Chiến Binh

1. Menu → Trang bị
2. Nhấn `←` hoặc `→` để chọn **Chiến binh**
3. Click **Cung Băng Lãm** trong kho đồ
4. Click slot **CÔNG** để gắn
5. Click **Giáp Ánh Sáng** trong kho đồ
6. Click slot **THỦ** để gắn
7. Nhấn `ESC` để lưu

**Kết quả:**
- Chiến binh giờ có:
  - Công: 30 + 8 = **38**
  - HP: 500 + 200 = **700**
  - Hiệu ứng làm chậm địch
  - Hồi sinh 1 lần khi chết

### ❓ FAQ

**Q: Trang bị có mất khi thoát game không?**
A: Không, trang bị được lưu vào profile và sẽ được load lại khi bạn đăng nhập.

**Q: Có thể gắn 1 trang bị cho nhiều nhân vật không?**
A: Không, mỗi trang bị chỉ gắn được cho 1 nhân vật. Cần gỡ ra khỏi nhân vật hiện tại trước khi gắn cho nhân vật khác.

**Q: Làm sao biết trang bị nào đã được gắn?**
A: Trang bị đã gắn sẽ có dấu ✓ màu xanh trong kho đồ. Hover chuột lên để xem chi tiết.

**Q: Trang bị có reset khi chết không?**
A: Không, trang bị vẫn giữ nguyên. Chỉ có hiệu ứng hồi sinh là dùng 1 lần mỗi trận.

**Q: Có thể thay đổi trang bị trong lúc chơi không?**
A: Hiện tại chưa hỗ trợ. Cần về menu → Trang bị để thay đổi.

**Q: Trang bị có chia sẻ được cho người chơi khác không?**
A: Không, mỗi user có profile và trang bị riêng.

### 🐛 Troubleshooting

**Trang bị không được lưu:**
- Đảm bảo bạn đã đăng nhập
- Nhấn ESC (không phải đóng cửa sổ game đột ngột)
- Kiểm tra file `du_lieu/save/profiles.json`

**Trang bị không được áp dụng trong game:**
- Đảm bảo bạn đã lưu trang bị (ESC trong màn hình trang bị)
- Chọn đúng nhân vật mà bạn đã trang bị
- Restart game nếu cần

**Không thấy trang bị trong kho:**
- Kiểm tra thư mục `Tai_nguyen/hinh_anh/trang_bi/`
- Đảm bảo các file PNG tồn tại

### 🎓 Tips & Tricks

1. **Tối ưu build cho từng nhân vật:**
   - **Ninja** (nhanh nhưng yếu): Giày Thiên Thần + Giáp Ánh Sáng để bù HP
   - **Võ Sĩ** (mạnh nhưng chậm): Giày Thiên Thần để tăng tốc
   - **Chiến Binh** (cân bằng): Bất kỳ combo nào cũng phù hợp

2. **Ưu tiên gắn:**
   - Slot **CÔNG** trước (tăng damage)
   - Slot **THỦ** nếu bạn hay chết
   - Slot **TỐC ĐỘ** để dễ né tránh

3. **Combo mạnh:**
   - Kiếm Rồng + Giáp Ánh Sáng = Công mạnh + An toàn
   - Cung Băng Lãm + Giày Thiên Thần = Làm chậm + Tăng tốc

4. **Lưu ý hiệu ứng:**
   - Thiêu đốt của Kiếm Rồng kéo dài 30 giây → Rất mạnh với boss
   - Hồi sinh của Giáp chỉ dùng 1 lần → Dùng cho nhân vật chính
   - Làm chậm của Cung giúp dễ né tránh và kite

---

Chúc bạn chơi game vui vẻ! 🎮✨
