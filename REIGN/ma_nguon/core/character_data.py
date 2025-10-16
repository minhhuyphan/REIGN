"""
Character Data - Dữ liệu nhân vật chung cho toàn bộ game
Sử dụng bởi Equipment Scene, Character Select, và các scene khác
"""

# Danh sách tất cả nhân vật trong game với stats chuẩn
CHARACTERS = [
    {
        "id": "chien_binh",
        "name": "Chiến binh",
        "folder": "tai_nguyen/hinh_anh/nhan_vat/chien_binh",
        "stats": {
            "hp": 500,
            "damage": 30,
            "kick_damage": 20,
            "speed": 5,
            "defense": 2
        },
        "color": (0, 255, 0),
        "price": 0
    },
    {
        "id": "ninja",
        "name": "Ninja",
        "folder": "tai_nguyen/hinh_anh/nhan_vat/ninja",
        "stats": {
            "hp": 350,
            "damage": 25,
            "kick_damage": 18,
            "speed": 8,
            "defense": 1
        },
        "color": (0, 0, 255),
        "price": 300
    },
    {
        "id": "vo_si",
        "name": "Võ sĩ",
        "folder": "tai_nguyen/hinh_anh/nhan_vat/vo_si",
        "stats": {
            "hp": 1000,
            "damage": 100,
            "kick_damage": 80,
            "speed": 4,
            "defense": 3
        },
        "color": (255, 0, 0),
        "price": 400
    },
    {
        "id": "chien_than_lac_hong",
        "name": "Chiến Thần Lạc Hồng",
        "folder": "tai_nguyen/hinh_anh/nhan_vat/chien_than_lac_hong",
        "stats": {
            "hp": 5000,
            "damage": 1000,
            "kick_damage": 800,
            "speed": 10,
            "defense": 500
        },
        "color": (255, 200, 0),
        "price": 500
    },
    {
        "id": "tho_san_quai_vat",
        "name": "Thợ Săn Quái Vật",
        "folder": "tai_nguyen/hinh_anh/nhan_vat/tho_san_quai_vat",
        "stats": {
            "hp": 450,
            "damage": 35,
            "kick_damage": 28,
            "speed": 7,
            "defense": 2
        },
        "color": (128, 0, 128),
        "price": 250
    }
]


def get_character_by_id(character_id):
    """
    Lấy thông tin nhân vật theo ID
    
    Args:
        character_id: ID nhân vật
        
    Returns:
        Dictionary chứa thông tin nhân vật hoặc None nếu không tìm thấy
    """
    for char in CHARACTERS:
        if char["id"] == character_id:
            return char.copy()  # Return a copy để tránh modify original
    return None


def get_all_characters():
    """
    Lấy danh sách tất cả nhân vật
    
    Returns:
        List of character dictionaries
    """
    return [char.copy() for char in CHARACTERS]


def get_character_stats(character_id):
    """
    Lấy stats của nhân vật
    
    Args:
        character_id: ID nhân vật
        
    Returns:
        Dictionary chứa stats hoặc None nếu không tìm thấy
    """
    char = get_character_by_id(character_id)
    if char:
        return char["stats"].copy()
    return None
