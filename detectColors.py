import time
import cv2
import numpy as np

webcam = cv2.VideoCapture(0)  # capturing video of webcam


# takes RGB input and create HSV range for color
# source: https://stackoverflow.com/questions/36817133/identifying-the-range-of-a-color-in-hsv-using-opencv
def set_color_range(bgr_value):
    color = np.uint8([[bgr_value]])
    hsv_color = cv2.cvtColor(color, cv2.COLOR_RGB2HSV)

    lower_bound = hsv_color[0][0][0] - 10, 100, 100
    upper_bound = hsv_color[0][0][0] + 10, 255, 255

    return np.array(lower_bound), np.array(upper_bound)


# creates color mask from input ranges
def create_mask(src, lower_bound, upper_bound):
    mask = cv2.inRange(src, lower_bound, upper_bound)
    return mask


# determines dominant color in a frame
def detect_dominant_color(p_mask, br_mask, bl_mask, g_mask, r_mask, y_mask):
    # calculating size of masks
    p_size = cv2.countNonZero(p_mask)
    br_size = cv2.countNonZero(br_mask)
    bl_size = cv2.countNonZero(bl_mask)
    g_size = cv2.countNonZero(g_mask)
    r_size = cv2.countNonZero(r_mask)
    y_size = cv2.countNonZero(y_mask)

    mask_sizes = [p_size, br_size, bl_size, g_size, r_size, y_size]
    dominant_color = max(mask_sizes)

    '''
    Return binary equivalent of color based on the mapping:
    Green:  "00"
    Red:    "01"
    Blue:   "10"
    Yellow: "11"
    Purple: ''
    Brown: 'end'
    '''
    if dominant_color == p_size:
        print("Start frame detected...")
        return 'start'

    if dominant_color == br_size:
        print("End frame detected...")
        return 'end'

    if dominant_color == bl_size:
        print("Blue is dominant")
        return '10'

    if dominant_color == g_size:
        print("Green is dominant")
        return '00'

    if dominant_color == r_size:
        print("Red is dominant")
        return '01'

    if dominant_color == y_size:
        print("Yellow is dominant")
        return '11'


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

    ret, frame = webcam.read()  # read frame of webcam
    # Get frame size:
    # print('Resolution: ' + str(frame.shape[0]) + ' x ' + str(frame.shape[1]))

    # Create webcam subsections
    upper_left_frame = frame[upper_left_1[1]: upper_left_2[1], upper_left_1[0]: upper_left_2[0]]
    upper_right_frame = frame[upper_right_1[1]: upper_right_2[1], upper_right_1[0]: upper_right_2[0]]
    bottom_left_frame = frame[bottom_left_1[1]: bottom_left_2[1], bottom_left_1[0]: bottom_left_2[0]]
    bottom_right_frame = frame[bottom_right_1[1]: bottom_right_2[1], bottom_right_1[0]: bottom_right_2[0]]

    # convert each subsection frame to HSV
    ul_section = cv2.cvtColor(upper_left_frame, cv2.COLOR_BGR2HSV)
    ur_section = cv2.cvtColor(upper_right_frame, cv2.COLOR_BGR2HSV)
    bl_section = cv2.cvtColor(bottom_left_frame, cv2.COLOR_BGR2HSV)
    br_section = cv2.cvtColor(bottom_right_frame, cv2.COLOR_BGR2HSV)

    # set color ranges
    lower_purple, upper_purple = set_color_range([145, 30, 180])  # starting frame color
    lower_brown, upper_brown = set_color_range([170, 110, 40])  # ending frame color
    lower_blue, upper_blue = set_color_range([0, 130, 200])
    lower_green, upper_green = set_color_range([60, 180, 75])
    lower_red, upper_red = set_color_range([230, 25, 75])
    lower_yellow, upper_yellow = set_color_range([255, 225, 25])

    subsections = [ul_section, ur_section, bl_section, br_section]

    # iterates through each subsection and identifies dominant color
    for frame in subsections:

        # create masks
        purple_mask = create_mask(frame, lower_purple, upper_purple)
        brown_mask = create_mask(frame, lower_brown, upper_brown)
        blue_mask = create_mask(frame, lower_blue, upper_blue)
        green_mask = create_mask(frame, lower_green, upper_green)
        red_mask = create_mask(frame, lower_red, upper_red)
        yellow_mask = create_mask(frame, lower_yellow, upper_yellow)

        # find dominant color
        binary_value = detect_dominant_color(purple_mask, brown_mask, blue_mask, green_mask, red_mask, yellow_mask)

        # stops if brown is dominant color
        if binary_value == 'end':
            print(binary_data)
            break

        binary_data += binary_value  # appends binary value
        print(binary_data)

    # display each subsection
    cv2.imshow('Upper Left', upper_left_frame)
    cv2.imshow('Upper Right', upper_right_frame)
    cv2.imshow('Bottom Left', bottom_left_frame)
    cv2.imshow('Bottom Right', bottom_right_frame)

    # pause between iteration for testing
    time.sleep(1)
    print("-------------------")

    # kill program by pressing "q" key
    # Test only. Delete before final presentation
    if cv2.waitKey(1) == ord('q'):
        break

binary_int = int(binary_data, 2)
byte_number = binary_int.bit_length() + 7 // 8
binary_array = binary_int.to_bytes(byte_number, "big")
ascii_text = binary_array.decode()  # convert binary data to text

print("Binary data:", binary_data)
print("Converted to text:", ascii_text)

# cleanup
webcam.release()
cv2.destroyAllWindows()
