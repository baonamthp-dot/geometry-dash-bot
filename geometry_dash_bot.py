import pyautogui
import time
import keyboard
from PIL import ImageGrab
import numpy as np

# Cấu hình
GAME_WINDOW_X = 400  # Vị trí X của cửa sổ game
GAME_WINDOW_Y = 100  # Vị trí Y của cửa sổ game
GAME_WIDTH = 800
GAME_HEIGHT = 600

class GeometryDashBot:
    def __init__(self):
        self.is_running = False
        self.jump_pressed = False
        
    def start_bot(self):
        """Bắt đầu bot"""
        print("🎮 Geometry Dash Bot đã khởi động!")
        print("Nhấn 'S' để bắt đầu, 'Q' để dừng")
        
        while True:
            if keyboard.is_pressed('q'):
                print("❌ Bot dừng lại")
                break
            if keyboard.is_pressed('s'):
                self.is_running = True
                print("✅ Bot bắt đầu chơi...")
                self.play_game()
                
    def play_game(self):
        """Logic chơi game"""
        time.sleep(1)
        
        while self.is_running:
            try:
                # Chụp màn hình
                screenshot = ImageGrab.grab(bbox=(GAME_WINDOW_X, GAME_WINDOW_Y, 
                                                 GAME_WINDOW_X + GAME_WIDTH, 
                                                 GAME_WINDOW_Y + GAME_HEIGHT))
                
                # Chuyển thành numpy array
                screen_array = np.array(screenshot)
                
                # Phát hiện vật cản (màu đen/tối)
                obstacle_detected = self.detect_obstacle(screen_array)
                
                if obstacle_detected:
                    print("🔴 Phát hiện vật cản! Nhảy!")
                    pyautogui.press('space')  # Nhấn space để nhảy
                    time.sleep(0.05)
                    pyautogui.keyUp('space')
                
                time.sleep(0.01)  # Kiểm tra mỗi 10ms
                
                # Dừng nếu nhấn Q
                if keyboard.is_pressed('q'):
                    self.is_running = False
                    print("⏸️ Bot tạm dừng")
                    break
                    
            except Exception as e:
                print(f"❌ Lỗi: {e}")
                break
    
    def detect_obstacle(self, screen_array):
        """Phát hiện vật cản bằng phân tích màu"""
        # Chuyển sang grayscale
        gray = np.dot(screen_array[...,:3], [0.2989, 0.5870, 0.1140])
        
        # Nếu phía trước có màu tối (giá trị < 100), có vật cản
        # Kiểm tra phần phía trước (2/3 bên phải của màn hình)
        front_area = gray[:, int(screen_array.shape[1] * 0.5):]
        
        # Nếu có quá nhiều pixel tối, có vật cản
        dark_pixels = np.sum(front_area < 100)
        threshold = (front_area.shape[0] * front_area.shape[1]) * 0.1
        
        return dark_pixels > threshold

class SimpleBot:
    """Bot đơn giản - chỉ nhấn space tự động"""
    def __init__(self):
        self.is_running = False
        
    def start_simple(self):
        """Bot đơn giản nhấn space định kỳ"""
        print("🎮 Simple Bot - Nhấn S để bắt đầu, Q để dừng")
        
        while True:
            if keyboard.is_pressed('q'):
                break
            if keyboard.is_pressed('s'):
                self.is_running = True
                print("✅ Bot chơi...")
                self.simple_play()
                
    def simple_play(self):
        """Nhấn space liên tục"""
        interval = 0.5  # Nhấn space mỗi 0.5 giây
        
        while self.is_running:
            try:
                pyautogui.press('space')
                time.sleep(interval)
                
                if keyboard.is_pressed('q'):
                    self.is_running = False
                    print("⏸️ Bot dừng")
                    break
                    
            except:
                break

def main():
    print("=" * 50)
    print("🎮 GEOMETRY DASH BOT 🎮")
    print("=" * 50)
    print("\n1. Bot thông minh (AI phát hiện vật cản)")
    print("2. Bot đơn giản (nhấn space tự động)")
    print("\nChọn (1 hoặc 2): ", end="")
    
    choice = input().strip()
    
    try:
        if choice == "1":
            bot = GeometryDashBot()
            bot.start_bot()
        elif choice == "2":
            bot = SimpleBot()
            bot.start_simple()
        else:
            print("❌ Lựa chọn không hợp lệ!")
    except KeyboardInterrupt:
        print("\n✋ Dừng bot")

if __name__ == "__main__":
    main()
