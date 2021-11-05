import time
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

    # set color range of white
    lower_white = np.array([0, 0, 0])
    upper_white = np.array([0, 0, 255])

    # set color range of red
    lower_red = np.array([136, 87, 111])
    upper_red = np.array([180, 255, 255])

    # set color range of black
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([255, 255, 0])

    # creating masks for each color
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
    white_mask = cv2.inRange(hsv, lower_white, lower_white)
    red_mask = cv2.inRange(hsv, lower_red, upper_red)
    black_mask = cv2.inRange(hsv, lower_black, upper_black)

    # calculating sizes of masks
    blue_size = cv2.countNonZero(blue_mask)
    white_size = cv2.countNonZero(white_mask)
    red_size = cv2.countNonZero(red_mask)
    black_size = cv2.countNonZero(black_mask)

    # identify which color is most dominant and store value
    sizes = [blue_size, white_size, red_size, black_size]
    max_value = max(sizes)

    # print out dominant color
    if max_value == blue_size:
        result = cv2.bitwise_and(frame, frame, mask=blue_mask)
        print("blue is dominant")

    if max_value == white_size:
        result = cv2.bitwise_and(frame, frame, mask=white_mask)
        print("white is dominant")

    if max_value == red_size:
        result = cv2.bitwise_and(frame, frame, mask=red_mask)
        print("red is dominant")

    else:
        result = cv2.bitwise_and(frame, frame, mask=black_mask)
        print("black is dominant")

    cv2.imshow('Frame', result)

    if cv2.waitKey(1) == ord('q'):
        break

# cleanup
webcam.release()
cv2.destroyAllWindows()
