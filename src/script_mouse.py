import pyautogui 

# lắng nghe chuột khi click chuột trái thì trả về tọa độ chuột
def listen_mouse():
    if pyautogui.click():
       return pyautogui.position()
    else:
        return listen_mouse()
    

print(listen_mouse())