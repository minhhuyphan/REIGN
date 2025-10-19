"""
Character Stats Configuration
Định nghĩa stats cơ bản cho tất cả nhân vật
File này được dùng chung bởi chon_nhan_vat.py và equipment_screen.py
"""

CHARACTER_STATS = {
    "chien_binh": {
        "name": "Chiến binh",
        "hp": 500,
        "speed": 5,
        "damage": 30,
        "defense": 2,
        "kick_damage": 20,
        "color": (0, 255, 0),
        "price": 0
    },
    "ninja": {
        "name": "Ninja",
        "hp": 350,
        "speed": 8,
        "damage": 25,
        "defense": 1,
        "kick_damage": 18,
        "color": (0, 0, 255),
        "price": 300
    },
    "vo_si": {
        "name": "Võ sĩ",
        "hp": 1000,
        "speed": 4,
        "damage": 100,
        "defense": 3,
        "kick_damage": 80,
        "color": (255, 0, 0),
        "price": 400
    },
    "chien_than_lac_hong": {
        "name": "Chiến Thần Lạc Hồng",
        "hp": 2000,
        "speed": 4,
        "damage": 200,
        "defense": 8,
        "kick_damage": 150,
        "color": (255, 200, 0),
        "price": 500
    },
    "tho_san_quai_vat": {
        "name": "Thợ Săn Quái Vật",
        "hp": 450,
        "speed": 7,
        "damage": 35,
        "defense": 2,
        "kick_damage": 25,
        "color": (128, 0, 128),
        "price": 250
    },
    "mi_anh": {
        "name": "Mị Ảnh",
        "hp": 450,
        "speed": 9,
        "damage": 28,
        "defense": 1,
        "kick_damage": 20,
        "color": (100, 100, 255),
        "price": 350
    },
    "van_dao": {
        "name": "Vân Dao",
        "hp": 600,
        "speed": 8,
        "damage": 32,
        "defense": 2,
        "kick_damage": 24,
        "color": (255, 100, 200),
        "price": 370
    }
}

def get_character_stats(character_id):
    """Lấy stats của nhân vật theo ID"""
    return CHARACTER_STATS.get(character_id, {
        "name": "Unknown",
        "hp": 100,
        "speed": 5,
        "damage": 10,
        "defense": 1,
        "kick_damage": 5,
        "color": (255, 255, 255),
        "price": 0
    })

def get_all_characters():
    """Lấy danh sách tất cả nhân vật"""
    return CHARACTER_STATS.keys()
