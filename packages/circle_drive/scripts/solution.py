import cv2
import math
import numpy as np


def solution(obs):
    img = cv2.resize(cv2.cvtColor(np.ascontiguousarray(obs), cv2.COLOR_BGR2RGB), (640, 480))
    img2 = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    lower = np.array([50, 0, 85])
    upper = np.array([120, 255, 255])
    lower2 = np.array([0, 0, 160])
    upper2 = np.array([255, 255, 255])
    zero = np.zeros(img2.shape)
    zero = cv2.inRange(zero, np.array([255, 255, 255]), np.array([255, 255, 255]))
    zero[::, ::] = 255
    img2 = cv2.bitwise_or(cv2.inRange(img2, lower, upper),
                              cv2.bitwise_and(zero, cv2.inRange(img2, lower2, upper2)))
    img2 = cv2.erode(img2, None, iterations=4)
    img2 = cv2.dilate(img2, None, iterations=4)
    img2 = cv2.Canny(img2, 50, 200)
    img2[:300:, ::] = 0
    lines = cv2.HoughLinesP(img2, 1, np.pi / 180, 50, minLineLength=40, maxLineGap=40)
    aver = c = 0
    try:
        for i in range(0, len(lines)):
            for x1, y1, x2, y2 in lines[i]:
                img = cv2.line(img, (x1, y1), (x2, y2), (255, 255, 0), 5)
                aver += math.atan((x1 - x2) / (y1 - y2))
                c += 1
        aver /= c
    except Exception as e:
        pass
        # print(e)
    if aver > 0.1:
        action = [0.92, aver * 4.75]
        print(aver * 4.5)
    elif aver < -0.1:
        action = [0.92, aver * 4.5]
        print(aver * 4.5)
    else:
        action = [0.99, aver * 3]
        print(aver * 3)
    return action
