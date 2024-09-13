# --------------------- ADD MOUSE MOVE RANDOM IN BOUNDARY ---------------------
import pyautogui
import random
import time
import math
def move_like_human(x_start, y_start, x_end, y_end, duration):
    steps = random.randint(1, 7)  # Giảm số bước để di chuyển nhanh hơn
    sleep_time = duration / steps
    for step in range(steps):
        t = step / (steps - 1)  # Đảm bảo t = 1 ở bước cuối cùng
        ease_t = (math.sin((t - 0.5) * math.pi) + 1) / 2  # Hiệu ứng di chuyển mượt
        x = x_start + (x_end - x_start) * ease_t
        y = y_start + (y_end - y_start) * ease_t
        
        pyautogui.moveTo(x, y)
        time.sleep(sleep_time)  # Thời gian nghỉ giữa mỗi bước
    pyautogui.moveTo(x_end, y_end)

x_start, y_start = pyautogui.position()
x_end = random.randint(3, 44)
y_end = random.randint(279, 316)
move_like_human(x_start, y_start, x_end, y_end, duration=0.02)
time.sleep(1)
# --------------------------------------------------------