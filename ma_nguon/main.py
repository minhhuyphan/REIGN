import sys
import os
import traceback

# Đặt project root (thư mục REIGN\REIGN) làm working directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(project_root)
if project_root not in sys.path:
    sys.path.append(project_root)

from ma_nguon.core.quan_ly_game import Game

if __name__ == "__main__":
    try:
        game = Game()
        game.run()
    except Exception:
        traceback.print_exc()
        print("Lỗi xảy ra khi chạy game. Kiểm tra trace bên trên.")