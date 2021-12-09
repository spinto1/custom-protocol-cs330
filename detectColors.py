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

    mask_sizes = [br_size, bl_size, g_size, r_size, y_size]
    dominant_color = max(mask_sizes)

    '''
    Return binary equivalent of color based on the mapping:
    Green:  "00"
    Red:    "01"
    Blue:   "10"
    Yellow: "11"
    Purple: 'start'
    Brown: 'end'    # Ended up using purple for both
    '''
    '''if dominant_color == p_size:
        print("Start frame detected...")
        return 'start'
    '''
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


def check_checksum(byt):
    checksum = byt[0]
    byte_val = byt[1:]
    if byte_val.count('1') % 2 == checksum:
        return False
    else:
        return True


# Adapted from https://www.kite.com/python/answers/how-to-convert-binary-string-to-and-from-ascii-text-in-python
def decode_binary(byt):
    binary_int = int(byt, 2)
    byte_number = binary_int.bit_length() + 7 // 8
    binary_array = binary_int.to_bytes(byte_number, "big")
    ascii_text = binary_array.decode()  # convert binary data to text
    return ascii_text


def detect_purple(mask):
    size = cv2.countNonZero(mask)
    print(size)
    if size > 1:
        print("Purple Detected")
        return 'start'


# Create subsections areas of camera
# Source: https://stackoverflow.com/questions/23720875/how-to-draw-a-rectangle-around-a-region-of-interest-in-python
upper_left_1 = (100, 100)
upper_left_2 = (400, 280)

upper_right_1 = (800, 100)
upper_right_2 = (950, 300)

bottom_left_1 = (100, 500)
bottom_left_2 = (400, 600)

bottom_right_1 = (800, 500)
bottom_right_2 = (1000, 600)

binary_data = ''

# set color ranges
lower_purple, upper_purple = set_color_range([145, 30, 180])  # starting frame color
lower_brown, upper_brown = set_color_range([170, 110, 40])  # ending frame color   # Ended up working well for purple...
lower_blue, upper_blue = set_color_range([0, 130, 200])
lower_green, upper_green = set_color_range([60, 180, 75])
lower_red, upper_red = set_color_range([230, 25, 75])
lower_yellow, upper_yellow = set_color_range([255, 225, 25])

while True:
    ret, frame = webcam.read()  # read frame of webcam

    # Create webcam subsection
    upper_left_frame = frame[upper_left_1[1]: upper_left_2[1], upper_left_1[0]: upper_left_2[0]]

    # convert each subsection frame to HSV
    ul_section = cv2.cvtColor(upper_left_frame, cv2.COLOR_BGR2HSV)
    # create masks
    purple_mask = create_mask(ul_section, lower_purple, upper_purple)
    brown_mask = create_mask(ul_section, lower_brown, upper_brown)
    blue_mask = create_mask(ul_section, lower_blue, upper_blue)
    green_mask = create_mask(ul_section, lower_green, upper_green)
    red_mask = create_mask(ul_section, lower_red, upper_red)
    yellow_mask = create_mask(ul_section, lower_yellow, upper_yellow)

    # find dominant color
    # binary_value = detect_dominant_color(purple_mask, brown_mask, blue_mask, green_mask, red_mask, yellow_mask)
    binary_value = detect_purple(purple_mask)
    # stops if purple is dominant color
    if binary_value == 'start':
        print(binary_data)
        break

    # display each subsection
    cv2.imshow('UL', upper_left_frame)

    print("-------------------")

cv2.destroyAllWindows()
time.sleep(1)

escape = False
while True:

    ret, frame = webcam.read()  # read frame of webcam
    # Get frame size:
    print('Resolution: ' + str(frame.shape[0]) + ' x ' + str(frame.shape[1]))

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

    subsections = [ul_section, ur_section, bl_section, br_section]

    # iterates through each subsection and identifies dominant color
    for subsection in subsections:

        # create masks
        purple_mask = create_mask(subsection, lower_purple, upper_purple)
        brown_mask = create_mask(subsection, lower_brown, upper_brown)
        blue_mask = create_mask(subsection, lower_blue, upper_blue)
        green_mask = create_mask(subsection, lower_green, upper_green)
        red_mask = create_mask(subsection, lower_red, upper_red)
        yellow_mask = create_mask(subsection, lower_yellow, upper_yellow)

        if subsection is ul_section:
            print('UPPER LEFT:')
        elif subsection is ur_section:
            print('UPPER RIGHT:')
        elif subsection is bl_section:
            print('BOTTOM LEFT:')
        elif subsection is br_section:
            print('BOTTOM RIGHT:')
        # find dominant color
        binary_value = detect_dominant_color(purple_mask, brown_mask, blue_mask, green_mask, red_mask, yellow_mask)

        # stops if brown is dominant color
        if binary_value == 'end':
            escape = True
            break
        # Don't want to add 'start' to our binary message... not good solution but for now...
        if binary_value == 'start':
            binary_value == '00'

        binary_data += binary_value  # appends binary value
        # print(binary_data)
        print(binary_value)

    # display each subsection
    cv2.imshow('full cam', frame)
    cv2.imshow('UL', upper_left_frame)
    cv2.imshow('UR', upper_right_frame)
    cv2.imshow('BL', bottom_left_frame)
    cv2.imshow('BR', bottom_right_frame)

    if escape:
        print(binary_data)
        break

    # pause between iteration for testing
    time.sleep(1)
    print("-------------------")

print("Length of binary data detected:", len(binary_data))

bytes_array = []
# Group each individual byte
for index in range(0, len(binary_data), 8):
    bytes_array.append(binary_data[index:index + 8])

first_half = bytes_array[:len(bytes_array) // 2]
second_half = bytes_array[len(bytes_array) // 2:]  

print(len(first_half), first_half)
print(len(second_half), second_half)

converted_message = ''
for i in range(len(first_half)):
    if check_checksum(first_half[i]):
        converted_message += decode_binary(first_half[i][1:])
    else:
        if check_checksum(second_half[i]):
            converted_message += decode_binary(second_half[i][1:])

print('Detected message:', converted_message)

# cleanup
webcam.release()
cv2.destroyAllWindows()

