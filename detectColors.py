import cv2
import numpy as np

# capturing video of webcam
webcam = cv2.VideoCapture(0)

while True:

    # read frame of webcam
    ret, frame = webcam.read()
    width = int(webcam.get(3))
    height = int(webcam.get(4))

    # convert frame to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # set color range of blue
    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([130, 255, 255])

    # set color range of red
    lower_red = np.array([136, 87, 111])
    upper_red = np.array([180, 255, 255])

    # set color range of green
    lower_green = np.array([25, 52, 72])
    upper_green = np.array([102, 255, 255])

    # creating masks for each color
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    red_mask = cv2.inRange(hsv, lower_red, upper_red)

    # calculating sizes of masks
    blue_size = cv2.countNonZero(blue_mask)
    green_size = cv2.countNonZero(green_mask)
    red_size = cv2.countNonZero(red_mask)

    # identify which mask is largest
    sizes = [blue_size, green_size, red_size]
    max_value = max(sizes)

    # print out dominant color
    if max_value == blue_size:
        result = cv2.bitwise_and(frame, frame, mask=blue_mask)
        print("blue is dominant")

    if max_value == green_size:
        result = cv2.bitwise_and(frame, frame, mask=green_mask)
        print("green is dominant")

    if max_value == red_size:
        result = cv2.bitwise_and(frame, frame, mask=red_mask)
        print("red is dominant")

    cv2.imshow('Frame', result)

    if cv2.waitKey(1) == ord('q'):
        break

# cleanup
webcam.release()
cv2.destroyAllWindows()
