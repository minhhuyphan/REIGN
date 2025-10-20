import pygame
import random
import os

# Hàm tự động load trang bị từ thư mục
def load_equipment_from_folder():
    """Tự động scan thư mục trang_bi và tạo EQUIPMENT_DATA theo rarity"""
    equipment_data = {}
    base_path = os.path.join("tai_nguyen", "hinh_anh", "trang_bi")
    
    if not os.path.exists(base_path):
        return equipment_data
    
    # Mapping tên file (không dấu) -> tên hiển thị (có dấu)
    name_mapping = {
        # Vũ khí vàng (Legendary)
        "kiem_rong": "Kiếm Rồng",
        "cung_bang_lam": "Cung Băng Lãm",
        "bua_sam": "Búa Sấm",
        "riu_lua": "Rìu Lửa",
        "giao_phong_ba": "Giáo Phong Ba",
        "kiem_thanh_long": "Kiếm Thanh Long",
        
        # Giáp vàng (Legendary)
        "giap_anh_sang": "Giáp Ánh Sáng",
        "khien_vang": "Khiên Vàng",
        "ao_giap_rong": "Áo Giáp Rồng",
        
        # Giày vàng (Legendary)
        "giay_thien_than": "Giày Thiên Thần",
        "giay_phong_van": "Giày Phong Vân",
        "nhan_ma_thuat": "Nhẫn Ma Thuật",
        
        # Vũ khí tím (Epic)
        "no_set": "Nỏ Sét",
        "kiem_thep": "Kiếm Thép",
        "bua_da": "Búa Đá",
        "cung_kim": "Cung Kim",
        
        # Giáp tím (Epic)
        "giap_thep": "Giáp Thép",
        "khien_dong": "Khiên Đồng",
        "ao_giap_kim": "Áo Giáp Kim",
        
        # Giày tím (Epic)
        "giay_kiem": "Giày Kiếm",
        "nhan_suc_manh": "Nhẫn Sức Mạnh",
        
        # Vũ khí xanh (Rare)
        "kiem_sat": "Kiếm Sắt",
        "cung_sat": "Cung Sắt",
        "giao_sat": "Giáo Sắt",
        "bua_sat": "Búa Sắt",
        
        # Giáp xanh (Rare)
        "giap_sat": "Giáp Sắt",
        "khien_sat": "Khiên Sắt",
        "ao_sat": "Áo Sắt",
        
        # Giày xanh (Rare)
        "giay_sat": "Giày Sắt",
        "giay_da": "Giày Da",
        
        # Vũ khí trắng (Common)
        "kiem_go": "Kiếm Gỗ",
        "cung_go": "Cung Gỗ",
        "giao_go": "Giáo Gỗ",
        "bua_go": "Búa Gỗ",
        
        # Giáp trắng (Common)
        "giap_vai": "Giáp Vải",
        "khien_go": "Khiên Gỗ",
        "ao_vai": "Áo Vải",
        
        # Giày trắng (Common)
        "giay_vai": "Giày Vải",
        "dep_cao_su": "Dép Cao Su",
    }
    
    # Định nghĩa mapping thư mục rarity -> rarity level và stats
    rarity_folders = {
        "trang_bi_trang": {  # Common (Trắng/Xám)
            "rarity": "common",
            "attack_bonus": 3,
            "hp_bonus": 50,
            "speed_bonus": 1
        },
        "trang_bi_xanh": {  # Rare (Xanh)
            "rarity": "rare",
            "attack_bonus": 6,
            "hp_bonus": 100,
            "speed_bonus": 1.5
        },
        "trang_bi_tim": {  # Epic (Tím)
            "rarity": "epic",
            "attack_bonus": 10,
            "hp_bonus": 150,
            "speed_bonus": 2
        },
        "trang_bi_vang": {  # Legendary (Vàng)
            "rarity": "legendary",
            "attack_bonus": 15,
            "hp_bonus": 250,
            "speed_bonus": 3
        }
    }
    
    # Định nghĩa mapping thư mục loại -> type
    type_folders = {
        "trang_bi_cong": "attack",
        "trang_bi_thu": "defense",
        "trang_bi_toc_chay": "speed"
    }
    
    # Định nghĩa trang bị vàng (legendary) với hiệu ứng đặc biệt
    legendary_effects = {
        # Tự động gán effect cho trang bị vàng dựa trên tên
        "rồng": ["burn"],
        "rong": ["burn"],  # Không dấu
        "dragon": ["burn"],
        "lửa": ["burn"],
        "lua": ["burn"],  # Không dấu
        "fire": ["burn"],
        
        "băng": ["slow"],
        "bang": ["slow"],  # Không dấu
        "ice": ["slow"],
        "lãm": ["slow"],
        "lam": ["slow"],  # Không dấu
        
        "sấm": ["lightning"],
        "sam": ["lightning"],  # Không dấu
        "thunder": ["lightning"],
        
        "ánh sáng": ["revive"],
        "anh sang": ["revive"],  # Không dấu
        "anh_sang": ["revive"],  # Format file
        "light": ["revive"],
        
        "thiên thần": ["double_jump"],
        "thien than": ["double_jump"],  # Không dấu
        "angel": ["double_jump"],
        
        "ma thuật": ["mana_regen"],
        "ma thuat": ["mana_regen"],  # Không dấu
        "magic": ["mana_regen"],
        
        "khiên": ["shield"],
        "khien": ["shield"],  # Không dấu
        "shield": ["shield"],
    }
    
    # Scan từng thư mục rarity
    for rarity_folder, rarity_config in rarity_folders.items():
        rarity_path = os.path.join(base_path, rarity_folder)
        if not os.path.exists(rarity_path):
            continue
        
        rarity = rarity_config["rarity"]
        
        # Scan từng thư mục loại (cong, thu, toc_chay)
        for type_folder, equip_type in type_folders.items():
            type_path = os.path.join(rarity_path, type_folder)
            if not os.path.exists(type_path):
                continue
            
            # Lấy danh sách file PNG
            files = [f for f in os.listdir(type_path) if f.lower().endswith('.png')]
            
            for filename in files:
                # Lấy tên trang bị (bỏ extension)
                item_id = os.path.splitext(filename)[0]
                # Đường dẫn tương đối từ thư mục trang_bi
                image_path = os.path.join(rarity_folder, type_folder, filename)
                
                # Lấy tên hiển thị (có dấu) từ mapping, nếu không có thì capitalize tên file
                item_name = name_mapping.get(item_id, item_id.replace("_", " ").title())
                
                # Xác định stats dựa trên rarity và type
                attack_bonus = rarity_config["attack_bonus"] if equip_type == "attack" else 0
                hp_bonus = rarity_config["hp_bonus"] if equip_type == "defense" else 0
                speed_bonus = rarity_config["speed_bonus"] if equip_type == "speed" else 0
                
                # Xác định effects (chỉ legendary có effect đặc biệt)
                effects = []
                if rarity == "legendary":
                    # Tìm effect dựa trên tên (search trong cả item_id và item_name)
                    name_lower = item_name.lower()  # Tên có dấu
                    id_lower = item_id.lower()      # Tên không dấu
                    
                    for keyword, effect_list in legendary_effects.items():
                        # Search trong cả tên hiển thị và tên file
                        if keyword in name_lower or keyword in id_lower:
                            effects = effect_list
                            # Debug print (comment để tránh Unicode error trên Windows)
                            # print(f"[ITEMS] >>> {item_name}: Detected effect '{effect_list}' from keyword '{keyword}'")
                            break
                    
                    # Nếu không tìm thấy, dùng effect mặc định
                    if not effects:
                        effects = ["special_power"]
                        # print(f"[ITEMS] WARNING: {item_name}: No effect matched, using default 'special_power'")
                
                # Sử dụng item_name làm key thay vì item_id
                equipment_data[item_name] = {
                    "name": item_name,
                    "type": equip_type,
                    "rarity": rarity,
                    "image_path": image_path,
                    "effects": effects,
                    "attack_bonus": attack_bonus,
                    "hp_bonus": hp_bonus,
                    "speed_bonus": speed_bonus,
                }
    
    print(f"[ITEMS] Loaded {len(equipment_data)} equipment items from folders")
    return equipment_data

# Load equipment data tự động
EQUIPMENT_DATA = load_equipment_from_folder()

# Fallback data nếu không có file
if not EQUIPMENT_DATA:
    EQUIPMENT_DATA = {
        "Kiếm Gỗ": {
            "name": "Kiếm Gỗ",
            "type": "attack",
            "rarity": "common",
            "attack_bonus": 3,
            "hp_bonus": 0,
            "speed_bonus": 0,
            "effects": []
        }
    }


class Item:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.picked = False
        self.image = None
        self.rect = pygame.Rect(self.x, self.y, 24, 24)

    def draw(self, screen, camera_x=0):
        # Default placeholder: small circle
        draw_x = self.x - camera_x
        pygame.draw.circle(screen, (200,200,0), (int(draw_x+12), int(self.y+12)), 10)

    def on_pickup(self, player):
        self.picked = True
        print(f"[DEBUG] {type(self).__name__} picked up by player at ({player.x},{player.y})")


class Gold(Item):
    def __init__(self, x, y, amount=10):
        super().__init__(x, y)
        self.amount = amount
        self.color = (212,175,55)
        self.rect = pygame.Rect(self.x, self.y, 20, 20)

    def draw(self, screen, camera_x=0):
        draw_x = self.x - camera_x
        pygame.draw.circle(screen, self.color, (int(draw_x+10), int(self.y+10)), 8)
        # draw amount small
        font = pygame.font.Font(None, 18)
        txt = font.render(str(self.amount), True, (0,0,0))
        screen.blit(txt, (draw_x+2, self.y+18))

    def on_pickup(self, player):
        if hasattr(player, 'gold'):
            player.gold += self.amount
        else:
            player.gold = self.amount
        self.picked = True


class HealthPotion(Item):
    def __init__(self, x, y, heal=200):
        super().__init__(x, y)
        self.heal = heal
        self.color = (200,50,50)
        self.rect = pygame.Rect(self.x, self.y, 20, 30)

    def draw(self, screen, camera_x=0):
        draw_x = self.x - camera_x
        pygame.draw.rect(screen, self.color, (draw_x+4, self.y, 12, 20), border_radius=3)
        font = pygame.font.Font(None, 16)
        txt = font.render('HP', True, (255,255,255))
        screen.blit(txt, (draw_x+6, self.y+2))

    def on_pickup(self, player):
        # add to player's inventory (simple count) or apply immediately
        if hasattr(player, 'potions'):
            player.potions['hp'] = player.potions.get('hp', 0) + 1
        else:
            player.potions = {'hp': 1}
        self.picked = True


class ManaPotion(Item):
    def __init__(self, x, y, mana=100):
        super().__init__(x, y)
        self.mana = mana
        self.color = (50,100,200)
        self.rect = pygame.Rect(self.x, self.y, 20, 30)

    def draw(self, screen, camera_x=0):
        draw_x = self.x - camera_x
        pygame.draw.rect(screen, self.color, (draw_x+4, self.y, 12, 20), border_radius=3)
        font = pygame.font.Font(None, 16)
        txt = font.render('MP', True, (255,255,255))
        screen.blit(txt, (draw_x+4, self.y+2))

    def on_pickup(self, player):
        if hasattr(player, 'potions'):
            player.potions['mp'] = player.potions.get('mp', 0) + 1
        else:
            player.potions = {'mp': 1}
        self.picked = True
