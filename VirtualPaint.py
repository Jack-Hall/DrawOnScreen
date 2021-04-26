import cv2
import numpy as np
Colors = {"pink": [130, 97, 78, 176, 255, 255], "green": [44, 138, 76, 88, 255, 166]}
ColorValues = {"pink": [255,102,255], "green":[153,255,51]}
points = [] #points are in the form xpos, ypos, colour title
def getContours(img):
    _, contours, hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 150:
            #cv2.drawContours(imgResult, cnt,-1,(255,0,0),3)
            #we calculate curve length
            peri = cv2.arcLength(cnt, True) #true is closed perimeter
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            objCor = len(approx)
            x, y, w, h = cv2.boundingRect(approx)
    return x + w // 2, y


def empty(one):
    pass
def findColor(img, title,imgResult):
    lower = np.array(Colors[title][0:3])
    upper = np.array(Colors[title][3:6])
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(imgHSV, lower, upper)
    x,y = getContours(mask)
    points.append([x,y, title])



cap = cv2.VideoCapture(0)
# cv2.namedWindow("track-bars")
# cv2.resizeWindow("track-bars", 640, 240)
# cv2.createTrackbar("Hue Min", "track-bars", 0, 179, empty)
# cv2.createTrackbar("Hue Max", "track-bars", 18, 179, empty)
# cv2.createTrackbar("Sat Min", "track-bars", 44, 255, empty)
# cv2.createTrackbar("Sat Max", "track-bars", 255, 255, empty)
# cv2.createTrackbar("Val Min", "track-bars", 139, 255, empty)
# cv2.createTrackbar("Val Max", "track-bars", 255, 255, empty)
# cap.set(3, 640)
# cap.set(4, 480)
# cap.set(10,100)

while True:
    success, img = cap.read(0)  # the parameter passed is the webcam id
    imgResult = img.copy()
    cap.set(3, 640)
    cap.set(4, 480)
    for key in Colors:
        findColor(img, key,imgResult)
    for point in points:
        cv2.circle(imgResult, (point[0], point[1]), 10, ColorValues[point[2]], cv2.FILLED)
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h_min = cv2.getTrackbarPos("Hue Min", "track-bars")
    h_max = cv2.getTrackbarPos("Hue Max", "track-bars")
    s_min = cv2.getTrackbarPos("Sat Min", "track-bars")
    s_max = cv2.getTrackbarPos("Sat Max", "track-bars")
    v_min = cv2.getTrackbarPos("Val Min", "track-bars")
    v_max = cv2.getTrackbarPos("Val Max", "track-bars")
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    #print(h_min, s_min, v_min, h_max, s_max, v_max)
    mask = cv2.inRange(imgHSV, lower, upper)
    ##imgResult = cv2.bitwise_and(img, img, mask=mask)
   # cv2.imshow("mask", mask)

    cv2.imshow("contours", cv2.flip(imgResult,1))

    # width is id 3 and height is id 4
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #cv2.imshow("Is Video?", imgHSV)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break;
