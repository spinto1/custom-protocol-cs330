import time
import cv2
import numpy as np

# capturing video of webcam
webcam = cv2.VideoCapture(0)


# takes RGB input and create HSV range for color
# source: https://stackoverflow.com/questions/36817133/identifying-the-range-of-a-color-in-hsv-using-opencv
def set_color_range(bgr_color_value):
    color = np.uint8([[bgr_color_value]])
    hsv_color = cv2.cvtColor(color, cv2.COLOR_RGB2HSV)

    lower_bound = hsv_color[0][0][0] - 10, 100, 100
    upper_bound = hsv_color[0][0][0] + 10, 255, 255

    return np.array(lower_bound), np.array(upper_bound)


# create color masks
def create_mask(src, lower, upper):
    mask = cv2.inRange(src, lower, upper)
    return mask


# determine dominant color in frame
def detect_dominant_color(b_mask, g_mask, r_mask, y_mask):
    # calculating size of masks
    b_size = cv2.countNonZero(b_mask)
    g_size = cv2.countNonZero(g_mask)
    r_size = cv2.countNonZero(r_mask)
    y_size = cv2.countNonZero(y_mask)

    mask_sizes = [b_size, g_size, r_size, y_size]
    max_color = max(mask_sizes)

    # identify dominant color mask
    if max_color == b_size:
        output = cv2.bitwise_and(frame, frame, mask=b_mask)
        print("blue is dominant")
        return output

    if max_color == g_size:
        output = cv2.bitwise_and(frame, frame, mask=g_mask)
        print("green is dominant")
        return output

    if max_color == r_size:
        output = cv2.bitwise_and(frame, frame, mask=r_mask)
        print("red is dominant")
        return output

    if max_color == y_size:
        output = cv2.bitwise_and(frame, frame, mask=y_mask)
        print("yellow is dominant")
        return output


while True:
    # read frame of webcam
    ret, frame = webcam.read()

    # convert frame to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # set color ranges
    lower_blue, upper_blue = set_color_range([0, 130, 200])
    lower_green, upper_green = set_color_range([60, 180, 75])
    lower_red, upper_red = set_color_range([230, 25, 75])
    lower_yellow, upper_yellow = set_color_range([255, 225, 25])

    # creating color masks
    blue_mask = create_mask(hsv, lower_blue, upper_blue)
    green_mask = create_mask(hsv, lower_green, upper_green)
    red_mask = create_mask(hsv, lower_red, upper_red)
    yellow_mask = create_mask(hsv, lower_yellow, upper_yellow)

    result = detect_dominant_color(blue_mask, green_mask, red_mask, yellow_mask)

    # displaying color detection for testing purposes
    cv2.imshow('Frame', result)

    # kill program by pressing "q" key
    if cv2.waitKey(1) == ord('q'):
        break

# cleanup
webcam.release()
cv2.destroyAllWindows()
