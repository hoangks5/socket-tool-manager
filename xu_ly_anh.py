import cv2
import numpy as np

# Đọc ảnh gốc và ảnh cắt
image = cv2.imread('1.png')
template = cv2.imread('2.png')

# Kích thước của mẫu
w, h = template.shape[1], template.shape[0]

# Tìm vị trí của ảnh cắt trong ảnh gốc
result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)

# Tìm điểm có độ tương đồng cao nhất
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

# max_loc là tọa độ trên góc trái của boundary
top_left = max_loc
bottom_right = (top_left[0] + w, top_left[1] + h)

# In tọa độ x, y và kích thước width, height
print(f"Tọa độ x, y: {top_left}")
print(f"Chiều rộng (width): {w}, Chiều cao (height): {h}")

# Vẽ hình chữ nhật lên ảnh gốc để đánh dấu boundary
cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)

# Hiển thị ảnh với boundary
cv2.imshow('Detected', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Lưu ảnh kết quả
cv2.imwrite('result.png', image)
