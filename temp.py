# --------------------- ADD MOUSE MOVE RANDOM IMAGE ---------------------
import pyautogui
import random
import time
import math
import base64
from PIL import Image, ImageGrab
from io import BytesIO
import cv2
import numpy as np

def get_x_y_w_h_from_base64(base64_string):
    # Capture the full screenshot
    screenshot = ImageGrab.grab()
    # Save the screenshot to a temporary file
    screenshot.save('1.png')
    
    # Save the base64 image to a temporary file
    with open('2.png', 'wb') as file:
        file.write(base64.b64decode(base64_string))
    
    # Load the images for template matching
    image = cv2.imread('1.png')
    template = cv2.imread('2.png')
    w, h = template.shape[1], template.shape[0]
    
    # Perform template matching
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    # Set a threshold to consider matches
    threshold = 0.8
    match_locations = np.where(result >= threshold)
    
    # Draw rectangles and count matching points
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
    
    # Add text with coordinates and match count
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    font_color = (0, 255, 0)
    font_thickness = 1
    text = 'TL: ' + str(top_left) + ' BR: ' + str(bottom_right) + ' Matches: ' + str(len(match_locations[0]))
    
    # Calculate text size
    text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
    text_w, text_h = text_size
    text_x = top_left[0]
    text_y = top_left[1] - 10  # Position text above the rectangle
    
    # Draw text on the image
    cv2.putText(image, text, (text_x, text_y), font, font_scale, font_color, font_thickness, cv2.LINE_AA)
    
    # Show the result image with the rectangle and text
    cv2.imshow('Detected', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    # Save the result image
    cv2.imwrite('result.png', image)


get_x_y_w_h_from_base64('iVBORw0KGgoAAAANSUhEUgAAADUAAAAsCAIAAABKXWd0AAADI0lEQVR4nO1YPY6rMBD2Pr2Cbm9gOndcgJVLqvgCKHTpfAFWbtJF4QKUqRblAtDRWZsLuHTl0V4i3StGa1mJQlaY6G2Rr4qMfz7GM9984eV8PpNfjD//m8AdPPnF4ckvDk9+cfjt/P4+YlMAcM4BAKWUcx6z1cL8AODj46NpGj9CKS3LUik1b8OXBfsbAGRZ5jnhIHKllLZtCwCEkPV6/X/4vb6+EkLqug6jpbWWUiIzBF76+/s7pfTunovd7263uya32+18/HxET6dT13Va67Zt72fnORrW2u12myRJkiR+cBxHxliSJIyxw+FwseRwOOAja+305rH8PLMkSTabDQ4WRYEj2+02fI3rheGE5fnhGUVRjOPo+eHvoihCZpvN5iKW1lrGGGNs+oj5+qy1bpqGc973fZqmF0/7vvcpmGUZANR1DQBSSiEESmOapgAQls415tfH8XgkhNR1fWtC13VSSkJI27aoKVVVoTquVitfLtNVPJ+f1poQcqsAhRDOubquv76+9vu9c04pRSlVSlVVJaUMNXwCUf13Qh3yPDfGKKXatm3b9ng8ZlmGGoRajYGnlE7f73x+aZo65249DVWQc16WJQA0TZNlmdYaA+kz8iH88jwHALxlQgilVGvddd2t+ZxzY0xZlkIInKaU4pxrrf0mS/KrqooQgm9PKR2GoSxLLM9bSzBshJDPz08cyfN8+pT5/CileEEoH3i2MQYTC1MNobXGYr8GZvBECkbVB8oeAKxWK5/7yPJ0OmFBCCGEENcCiZgujlh+WB8oxZj7YYWSb3NljLl1j/v9nkzqwAL+Pk3TYRjwWj1LNIJ93/d9f0uBtdYAsF6vpyQ6pv9iq/U93hsZxljY+NHL+I6MndrPnD4iip+19vqM0KdYa9HLMMbGcfRLEH7wUfzO3xbmOgyhKQxj6Z3fXWeFWMDfo0lGh4x16pzztnkYhjC9UIyMMT8x97H5F0YR3XKIiwj5u/5h5BaLnwe2O2x0GFHO+dvbWxhR9Is/33NJfhdcpZRhY533R/hR/BDeQMz+kPBYfvH47d+Hnvzi8OQXhye/OPwDQaDi+c/AJrQAAAAASUVORK5CYII=')

# Pause for a moment before exiting
time.sleep(1)

# --------------------------------------------------------