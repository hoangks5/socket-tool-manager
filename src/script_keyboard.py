import keyboard
import pyautogui
import time


# tạo 1 hàm lắng nghe phím bấm sau đó trả về ký tự tương ứng
def listen_key():
    key = keyboard.read_event()
    if key.event_type == keyboard.KEY_DOWN:
        return key.name
    

