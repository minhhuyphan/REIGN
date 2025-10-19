# Hệ Thống Trang Bị (Equipment System)

## Tổng Quan

Hệ thống trang bị cho phép người chơi trang bị đồ để tăng sức mạnh cho nhân vật. Mỗi nhân vật có thể trang bị tối đa 3 món đồ:
- **1 trang bị Công** (Attack)
- **1 trang bị Thủ** (Defense)  
- **1 trang bị Tốc Độ** (Speed)

## Cách Truy Cập

Từ menu chính, chọn **"Trang bị"** để mở màn hình quản lý trang bị.

## Giao Diện

### Bên Trái - Kho Đồ (Inventory)
- Hiển thị tất cả các trang bị có sẵn
- Click vào trang bị để chọn
- Trang bị đã được trang bị sẽ có dấu ✓ màu xanh

### Bên Phải - Slot Trang Bị
- 3 slot tương ứng: CÔNG, THỦ, TỐC ĐỘ
- Click vào trang bị đã chọn, sau đó click vào slot tương ứng để trang bị
- Click vào slot đã có đồ để gỡ trang bị

### Thông Số
Phía dưới các slot hiển thị thông số tổng hợp:
- **Công**: Sát thương gốc + bonus từ trang bị
- **Thủ**: Phòng thủ gốc + bonus từ trang bị
- **HP**: Máu tối đa gốc + bonus từ trang bị
- **Tốc độ**: Tốc độ di chuyển gốc + bonus từ trang bị

## Danh Sách Trang Bị

### 1. Cung Băng Lãm (Công)
- **Loại**: Trang bị công
- **Bonus**: +8 Công
- **Hiệu ứng đặc biệt**: Làm chậm kẻ địch khi tấn công (2 giây)
- **Icon**: ![Cung Băng Lãm](Tai_nguyen/hinh_anh/trang_bi/trang_bi_cong/cung_bang_lam.png)

### 2. Kiếm Rồng (Công)
- **Loại**: Trang bị công
- **Bonus**: +10 Công
- **Hiệu ứng đặc biệt**: Thiêu đốt kẻ địch 1 máu/giây trong 30 giây
- **Icon**: ![Kiếm Rồng](Tai_nguyen/hinh_anh/trang_bi/trang_bi_cong/kiem_rong.png)

### 3. Giáp Ánh Sáng (Thủ)
- **Loại**: Trang bị thủ
- **Bonus**: +200 HP
- **Hiệu ứng đặc biệt**: Hồi sinh nhân vật với 50% máu tối đa khi chết (1 lần duy nhất)
- **Icon**: ![Giáp Ánh Sáng](Tai_nguyen/hinh_anh/trang_bi/trang_bi_thu/giap_anh_sang.png)

### 4. Giày Thiên Thần (Tốc Độ)
- **Loại**: Trang bị tốc độ
- **Bonus**: +2 Tốc độ chạy, +50 HP
- **Icon**: ![Giày Thiên Thần](Tai_nguyen/hinh_anh/trang_bi/trang_bi_toc_chay/giay_thien_than.png)

## Hiệu Ứng Đặc Biệt

### Làm Chậm (Slow Effect)
- Xuất hiện khi sử dụng **Cung Băng Lãm**
- Giảm 50% tốc độ di chuyển của kẻ địch
- Thời gian: 2 giây
- **Chỉ báo**: Icon tinh thể băng màu xanh xuất hiện trên đầu kẻ địch

### Thiêu Đốt (Burn Effect)
- Xuất hiện khi sử dụng **Kiếm Rồng**
- Gây 1 sát thương/giây
- Thời gian: 30 giây
- **Chỉ báo**: Icon lửa màu cam/đỏ xuất hiện trên đầu kẻ địch

### Hồi Sinh (Revive Effect)
- Xuất hiện khi trang bị **Giáp Ánh Sáng**
- Tự động kích hoạt khi HP về 0
- Hồi sinh với 50% HP tối đa
- Chỉ hoạt động **1 lần duy nhất** trong mỗi trận đấu

## Cơ Chế Hoạt Động

### Trang Bị
1. Mở màn hình trang bị (ESC hoặc E để thoát)
2. Click vào trang bị trong kho đồ để chọn
3. Click vào slot tương ứng (Công/Thủ/Tốc Độ) để trang bị
4. Thông số sẽ được cập nhật ngay lập tức

### Gỡ Trang Bị
1. Click vào slot đã có trang bị
2. Trang bị sẽ quay về kho đồ
3. Thông số trở về mức cơ bản

### Ràng Buộc
- **Mỗi trang bị chỉ có thể gắn vào 1 nhân vật**
- Nếu trang bị đã được gắn, cần gỡ ra trước khi gắn cho nhân vật khác
- Mỗi slot chỉ chấp nhận đúng loại trang bị (Công/Thủ/Tốc Độ)

## Lưu Ý

- Trang bị được áp dụng **ngay lập tức** khi gắn vào slot
- Bonus sát thương được tính cả đòn đấm và đá
- Hiệu ứng đặc biệt chỉ kích hoạt khi **trang bị được gắn vào nhân vật**
- Kiểm tra thanh máu của kẻ địch để xem icon hiệu ứng (lửa cho burn, băng cho slow)

## Phím Tắt

- **E** hoặc **ESC**: Đóng màn hình trang bị
- **Click chuột**: Chọn/Trang bị/Gỡ trang bị
- **Hover chuột**: Xem thông tin chi tiết trang bị (tooltip)

## Kỹ Thuật

### Files Liên Quan
- `ma_nguon/doi_tuong/equipment.py` - Lớp equipment và equipment manager
- `ma_nguon/man_choi/equipment_screen.py` - UI màn hình trang bị
- `ma_nguon/doi_tuong/nhan_vat/nhan_vat.py` - Tích hợp equipment vào character
- `ma_nguon/doi_tuong/quai_vat/quai_vat.py` - Xử lý hiệu ứng trên enemies

### Cách Mở Rộng

Để thêm trang bị mới:

1. Tạo class kế thừa từ `Equipment` trong `equipment.py`:
```python
class TenTrangBi(Equipment):
    def __init__(self):
        super().__init__("Tên", "loai", "duong_dan_anh.png")
        self.attack_bonus = 10  # Tùy chỉnh
        # Thêm các bonus khác...
```

2. Thêm vào `EquipmentManager.initialize_equipment()`:
```python
self.all_equipment.append(TenTrangBi())
```

3. Thêm hình ảnh vào thư mục `Tai_nguyen/hinh_anh/trang_bi/`

## FAQ

**Q: Trang bị có mất khi chết không?**  
A: Không, trang bị vẫn giữ nguyên.

**Q: Có thể gắn 2 trang bị công không?**  
A: Không, mỗi loại chỉ được gắn 1 món.

**Q: Hiệu ứng hồi sinh có reset không?**  
A: Hiệu ứng hồi sinh chỉ hoạt động 1 lần mỗi trận. Sau khi sử dụng, cần bắt đầu trận mới để reset.

**Q: Các hiệu ứng có stack không?**  
A: Không, mỗi loại hiệu ứng chỉ áp dụng 1 lần. Nếu tấn công lại, thời gian sẽ được làm mới.
