"""Test script để kiểm tra tỷ lệ nhận nhân vật trong gacha"""
import random
from ma_nguon.doi_tuong.items import EQUIPMENT_DATA

def test_gacha_pool():
    """Mô phỏng gacha pool để kiểm tra tỷ lệ"""
    pool = []
    
    # Thêm nhân vật (giả sử chưa có)
    pool.append("CHARACTER:van_dao")
    pool.append("CHARACTER:mi_anh")
    
    # Thêm vàng (30 items = 15%)
    gold_amounts = [50, 100, 200, 500]
    for _ in range(30):
        amount = random.choice(gold_amounts)
        pool.append(f"GOLD:{amount}")
    
    # Thêm trang bị theo weight
    for item_id, item_data in EQUIPMENT_DATA.items():
        rarity = item_data.get("rarity", "common")
        
        if rarity == "common":
            weight = 60
        elif rarity == "rare":
            weight = 30
        elif rarity == "epic":
            weight = 8
        else:  # legendary
            weight = 2
        
        for _ in range(weight):
            pool.append(item_id)
    
    # Thống kê
    total = len(pool)
    van_dao_count = pool.count("CHARACTER:van_dao")
    mi_anh_count = pool.count("CHARACTER:mi_anh")
    total_char_count = van_dao_count + mi_anh_count
    gold_count = sum(1 for x in pool if x.startswith("GOLD:"))
    
    print("=" * 60)
    print("THỐNG KÊ GACHA POOL")
    print("=" * 60)
    print(f"Tổng số items trong pool: {total}")
    print(f"Số lượng vàng: {gold_count} ({gold_count/total*100:.2f}%)")
    print(f"Số lượng nhân vật: {total_char_count}")
    print(f"  - Vân Đao: {van_dao_count} ({van_dao_count/total*100:.2f}%)")
    print(f"  - Mị Ảnh: {mi_anh_count} ({mi_anh_count/total*100:.2f}%)")
    print(f"Tỷ lệ nhận BẤT KỲ nhân vật: {total_char_count/total*100:.2f}%")
    print()
    
    # Mô phỏng 1000 lượt quay
    print("=" * 60)
    print("MÔ PHỎNG 1000 LƯỢT QUAY")
    print("=" * 60)
    
    van_dao_rolls = 0
    mi_anh_rolls = 0
    
    for _ in range(1000):
        result = random.choice(pool)
        if result == "CHARACTER:van_dao":
            van_dao_rolls += 1
        elif result == "CHARACTER:mi_anh":
            mi_anh_rolls += 1
    
    print(f"Số lần nhận Vân Đao: {van_dao_rolls} ({van_dao_rolls/10:.1f}%)")
    print(f"Số lần nhận Mị Ảnh: {mi_anh_rolls} ({mi_anh_rolls/10:.1f}%)")
    print(f"Tổng nhân vật: {van_dao_rolls + mi_anh_rolls} ({(van_dao_rolls + mi_anh_rolls)/10:.1f}%)")
    print()
    
    # Tính xác suất nhận ít nhất 1 nhân vật trong 10 lượt
    prob_char = total_char_count / total
    prob_no_char_10 = (1 - prob_char) ** 10
    prob_at_least_1 = (1 - prob_no_char_10) * 100
    
    print("=" * 60)
    print("XÁC SUẤT NHẬN NHÂN VẬT")
    print("=" * 60)
    print(f"Xác suất nhận nhân vật mỗi lượt: {prob_char*100:.2f}%")
    print(f"Xác suất KHÔNG nhận nhân vật trong 10 lượt: {prob_no_char_10*100:.2f}%")
    print(f"Xác suất nhận ÍT NHẤT 1 nhân vật trong 10 lượt: {prob_at_least_1:.2f}%")
    print()
    
    # Số lượt trung bình cần quay
    expected_rolls = 1 / prob_char
    print(f"Số lượt trung bình để nhận 1 nhân vật: {expected_rolls:.1f} lượt")
    print(f"Chi phí trung bình (1 lượt = 100 vàng): {expected_rolls * 100:.0f} vàng")
    print()
    
    # Mô phỏng 100 người chơi, mỗi người quay 10 lượt
    print("=" * 60)
    print("MÔ PHỎNG 100 NGƯỜI CHƠI (mỗi người quay 10 lượt)")
    print("=" * 60)
    
    players_with_char = 0
    for _ in range(100):
        got_character = False
        for _ in range(10):
            result = random.choice(pool)
            if result.startswith("CHARACTER:"):
                got_character = True
                break
        if got_character:
            players_with_char += 1
    
    print(f"Số người nhận được nhân vật: {players_with_char}/100")
    print(f"Tỷ lệ: {players_with_char}%")
    print("=" * 60)

if __name__ == "__main__":
    test_gacha_pool()
