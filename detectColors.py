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
def detect_dominant_color(section, b_mask, g_mask, r_mask, y_mask):
    # calculating size of masks
    b_size = cv2.countNonZero(b_mask)
    g_size = cv2.countNonZero(g_mask)
    r_size = cv2.countNonZero(r_mask)
    y_size = cv2.countNonZero(y_mask)

    mask_sizes = [b_size, g_size, r_size, y_size]
    max_color = max(mask_sizes)

    if max_color == b_size:
        print("Blue is dominant in")
        return

    if max_color == g_size:
        print("Green is dominant in")
        return

    if max_color == r_size:
        print("Red is dominant in")
        return

    if max_color == y_size:
        print("Yellow is dominant")
        return


# Create subsections areas of camera
# Source: https://stackoverflow.com/questions/23720875/how-to-draw-a-rectangle-around-a-region-of-interest-in-python
upper_left_1 = (0, 0)
upper_left_2 = (320, 240)

upper_right_1 = (320, 0)
upper_right_2 = (640, 240)

bottom_left_1 = (0, 240)
bottom_left_2 = (320, 480)

bottom_right_1 = (320, 240)
bottom_right_2 = (640, 480)

binary_data = ''

while True:
    # read frame of webcam
    ret, frame = webcam.read()
    # Get frame size:
    # print('Resolution: ' + str(frame.shape[0]) + ' x ' + str(frame.shape[1]))

    # Create webcam subsections
    upper_left_frame = frame[upper_left_1[1]: upper_left_2[1], upper_left_1[0]: upper_left_2[0]]
    upper_right_frame = frame[upper_right_1[1]: upper_right_2[1], upper_right_1[0]: upper_right_2[0]]
    bottom_left_frame = frame[bottom_left_1[1]: bottom_left_2[1], bottom_left_1[0]: bottom_left_2[0]]
    bottom_right_frame = frame[bottom_right_1[1]: bottom_right_2[1], bottom_right_1[0]: bottom_right_2[0]]

    # convert frame to HSV
    ul = cv2.cvtColor(upper_left_frame, cv2.COLOR_BGR2HSV)
    ur = cv2.cvtColor(upper_right_frame, cv2.COLOR_BGR2HSV)
    bl = cv2.cvtColor(bottom_left_frame, cv2.COLOR_BGR2HSV)
    br = cv2.cvtColor(bottom_right_frame, cv2.COLOR_BGR2HSV)

    # set color ranges
    lower_blue, upper_blue = set_color_range([0, 130, 200])
    lower_green, upper_green = set_color_range([60, 180, 75])
    lower_red, upper_red = set_color_range([230, 25, 75])
    lower_yellow, upper_yellow = set_color_range([255, 225, 25])

    subsections = [ul, ur, bl, br]  # list of subsections

    # creates mask and finds dominant color for each subsection
    for frame in subsections:
        # creating color masks
        blue_mask = create_mask(frame, lower_blue, upper_blue)
        green_mask = create_mask(frame, lower_green, upper_green)
        red_mask = create_mask(frame, lower_red, upper_red)
        yellow_mask = create_mask(frame, lower_yellow, upper_yellow)

        detect_dominant_color(frame, blue_mask, green_mask, red_mask, yellow_mask)

    cv2.imshow('Upper Left', upper_left_frame)
    cv2.imshow('Upper Right', upper_right_frame)
    cv2.imshow('Bottom Left', bottom_left_frame)
    cv2.imshow('Bottom Right', bottom_right_frame)

    # wait 5 seconds between each iteration for testing purposes
    time.sleep(5)
    print("-------------------")

    # kill program by pressing "q" key
    if cv2.waitKey(1) == ord('q'):
        break

# cleanup
webcam.release()
cv2.destroyAllWindows()
